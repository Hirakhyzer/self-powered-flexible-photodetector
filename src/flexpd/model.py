"""Physics-inspired reduced-order model for a coupled piezo-pyro photodetector.

The model is intentionally simple and parameterized. It is suitable for hypothesis
exploration, sensitivity studies, and fitting to measured data; it is not a TCAD
replacement and should not be interpreted as predicting a fabricated device without
calibration.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np

from .metrics import detectivity_jones, eqe_from_responsivity, responsivity_from_eqe


@dataclass(frozen=True)
class DeviceParams:
    wavelength_nm: float = 525.0
    external_quantum_efficiency: float = 0.70
    active_area_mm2: float = 1.0
    dark_current_a: float = 1e-10

    # Effective reduced-order polarization parameters. Defaults are illustrative.
    piezo_voltage_per_strain_v: float = 8.0
    pyro_voltage_per_k_v: float = 0.015
    coupling_strength_per_v: float = 1.5
    max_coupling_exponent: float = 1.25

    # Effective pyroelectric coefficient used for transient current, C m^-2 K^-1.
    pyroelectric_coefficient_c_m2k: float = 1.0e-5

    # First-order photothermal response.
    thermal_rise_k_at_reference_power: float = 1.5
    reference_power_density_mw_cm2: float = 1.0
    thermal_time_constant_s: float = 0.25

    @property
    def active_area_m2(self) -> float:
        return self.active_area_mm2 * 1e-6

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class OperatingPoint:
    power_density_mw_cm2: float = 1.0
    strain: float = 0.0  # engineering strain, e.g. 0.005 = 0.5%
    temperature_rise_k: float = 0.0


def _validate(params: DeviceParams, op: OperatingPoint) -> None:
    if params.wavelength_nm <= 0:
        raise ValueError("wavelength_nm must be positive")
    if params.external_quantum_efficiency < 0:
        raise ValueError("external_quantum_efficiency must be non-negative")
    if params.active_area_mm2 <= 0:
        raise ValueError("active_area_mm2 must be positive")
    if params.dark_current_a <= 0:
        raise ValueError("dark_current_a must be positive")
    if params.reference_power_density_mw_cm2 <= 0:
        raise ValueError("reference_power_density_mw_cm2 must be positive")
    if params.thermal_time_constant_s <= 0:
        raise ValueError("thermal_time_constant_s must be positive")
    if op.power_density_mw_cm2 < 0:
        raise ValueError("power_density_mw_cm2 must be non-negative")


def optical_power_w(power_density_mw_cm2: float, active_area_m2: float) -> float:
    """Convert mW/cm^2 over an active area in m^2 to optical power in watts."""
    power_density_w_m2 = power_density_mw_cm2 * 10.0
    return power_density_w_m2 * active_area_m2


def polarization_voltage_v(
    params: DeviceParams,
    strain: float,
    temperature_rise_k: float,
) -> float:
    """Effective interface potential from piezoelectric and pyroelectric polarization."""
    return (
        params.piezo_voltage_per_strain_v * strain
        + params.pyro_voltage_per_k_v * temperature_rise_k
    )


def coupling_gain(params: DeviceParams, polarization_voltage: float) -> float:
    """Bounded phenomenological carrier-separation gain."""
    exponent = np.clip(
        params.coupling_strength_per_v * polarization_voltage,
        -params.max_coupling_exponent,
        params.max_coupling_exponent,
    )
    return float(np.exp(exponent))


def static_response(params: DeviceParams, op: OperatingPoint) -> dict[str, float]:
    """Calculate zero-bias steady-state metrics for one operating point."""
    _validate(params, op)
    r0 = responsivity_from_eqe(params.external_quantum_efficiency, params.wavelength_nm)
    vpol = polarization_voltage_v(params, op.strain, op.temperature_rise_k)
    gain = coupling_gain(params, vpol)
    responsivity = r0 * gain
    p_opt = optical_power_w(op.power_density_mw_cm2, params.active_area_m2)
    photocurrent = responsivity * p_opt
    dstar = detectivity_jones(responsivity, params.active_area_m2, params.dark_current_a)
    eqe_effective = eqe_from_responsivity(responsivity, params.wavelength_nm)

    return {
        "baseline_responsivity_a_w": r0,
        "polarization_voltage_v": vpol,
        "coupling_gain": gain,
        "responsivity_a_w": responsivity,
        "optical_power_w": p_opt,
        "photocurrent_a": photocurrent,
        "dark_current_a": params.dark_current_a,
        "detectivity_jones_shot_noise_limited": dstar,
        "effective_eqe_fraction": eqe_effective,
    }


def simulate_transient(
    params: DeviceParams,
    op: OperatingPoint,
    duration_s: float = 5.0,
    dt_s: float = 0.002,
    modulation_hz: float = 1.0,
    duty_cycle: float = 0.5,
) -> dict[str, np.ndarray]:
    """Simulate chopped illumination, first-order heating, and pyro transient current."""
    _validate(params, op)
    if duration_s <= 0 or dt_s <= 0:
        raise ValueError("duration_s and dt_s must be positive")
    if modulation_hz <= 0:
        raise ValueError("modulation_hz must be positive")
    if not 0 < duty_cycle < 1:
        raise ValueError("duty_cycle must lie between 0 and 1")

    time = np.arange(0.0, duration_s + 0.5 * dt_s, dt_s)
    phase = (time * modulation_hz) % 1.0
    light_on = (phase < duty_cycle).astype(float)

    target_delta_t = (
        params.thermal_rise_k_at_reference_power
        * (op.power_density_mw_cm2 / params.reference_power_density_mw_cm2)
        * light_on
    )

    temperature_rise = np.zeros_like(time)
    for i in range(1, len(time)):
        dtemp_dt = (
            target_delta_t[i - 1] - temperature_rise[i - 1]
        ) / params.thermal_time_constant_s
        temperature_rise[i] = temperature_rise[i - 1] + dtemp_dt * dt_s

    temperature_rate = np.gradient(temperature_rise, dt_s)
    vpol = (
        params.piezo_voltage_per_strain_v * op.strain
        + params.pyro_voltage_per_k_v * temperature_rise
    )
    exponents = np.clip(
        params.coupling_strength_per_v * vpol,
        -params.max_coupling_exponent,
        params.max_coupling_exponent,
    )
    gains = np.exp(exponents)

    r0 = responsivity_from_eqe(params.external_quantum_efficiency, params.wavelength_nm)
    incident_power = optical_power_w(op.power_density_mw_cm2, params.active_area_m2)
    photocurrent = r0 * gains * incident_power * light_on
    pyro_current = (
        params.pyroelectric_coefficient_c_m2k
        * params.active_area_m2
        * temperature_rate
    )
    total_current = photocurrent + pyro_current + params.dark_current_a

    return {
        "time_s": time,
        "light_on": light_on,
        "temperature_rise_k": temperature_rise,
        "temperature_rate_k_s": temperature_rate,
        "strain": np.full_like(time, op.strain),
        "polarization_voltage_v": vpol,
        "coupling_gain": gains,
        "photocurrent_a": photocurrent,
        "pyro_current_a": pyro_current,
        "total_current_a": total_current,
    }
