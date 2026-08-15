"""Photodetector performance metrics with explicit SI/unit conversions."""

from __future__ import annotations

import math

Q_E = 1.602176634e-19  # C
H = 6.62607015e-34  # J s
C = 299792458.0  # m s^-1


def responsivity_from_eqe(eqe_fraction: float, wavelength_nm: float) -> float:
    """Return A/W for a unity-gain detector from EQE as a fraction (0..1 typical)."""
    if eqe_fraction < 0:
        raise ValueError("eqe_fraction must be non-negative")
    if wavelength_nm <= 0:
        raise ValueError("wavelength_nm must be positive")
    wavelength_m = wavelength_nm * 1e-9
    return eqe_fraction * Q_E * wavelength_m / (H * C)


def eqe_from_responsivity(responsivity_a_w: float, wavelength_nm: float) -> float:
    """Return EQE as a fraction, assuming no separate internal gain correction."""
    if responsivity_a_w < 0:
        raise ValueError("responsivity_a_w must be non-negative")
    if wavelength_nm <= 0:
        raise ValueError("wavelength_nm must be positive")
    wavelength_m = wavelength_nm * 1e-9
    return responsivity_a_w * H * C / (Q_E * wavelength_m)


def detectivity_jones(
    responsivity_a_w: float,
    active_area_m2: float,
    dark_current_a: float,
) -> float:
    """Shot-noise-limited specific detectivity in Jones (cm Hz^0.5 / W).

    This is an optimistic estimate when 1/f, Johnson, generation-recombination,
    and readout noise are not negligible.
    """
    if responsivity_a_w < 0:
        raise ValueError("responsivity_a_w must be non-negative")
    if active_area_m2 <= 0:
        raise ValueError("active_area_m2 must be positive")
    if dark_current_a <= 0:
        raise ValueError("dark_current_a must be positive")

    area_cm2 = active_area_m2 * 1e4
    shot_noise_a_hz05 = math.sqrt(2.0 * Q_E * dark_current_a)
    return responsivity_a_w * math.sqrt(area_cm2) / shot_noise_a_hz05
