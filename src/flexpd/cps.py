"""Cyber-physical integration layer for the self-powered photodetector model.

This module treats the detector as the physical sensing plant and adds a small,
inspectable cyber layer: edge filtering, state classification, event-triggered
telemetry, a simple lossy/latent communication channel, and actuator commands.
It is a systems research scaffold, not a validated embedded controller.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Mapping
import numpy as np

STATE_IDLE = 0
STATE_MONITOR = 1
STATE_PROTECT = 2
STATE_FAULT = 3

STATE_NAMES = {
    STATE_IDLE: "IDLE",
    STATE_MONITOR: "MONITOR",
    STATE_PROTECT: "PROTECT",
    STATE_FAULT: "FAULT",
}

@dataclass(frozen=True)
class CPSConfig:
    """Configuration for the edge/network/decision layer.

    Thresholds are illustrative and must be calibrated to the sensor, readout,
    use case, and safety requirements before deployment.
    """
    filter_alpha: float = 0.25
    light_current_threshold_a: float = 1.0e-6
    strain_alert_threshold: float = 8.0e-3
    thermal_rate_alert_k_s: float = 3.0
    heartbeat_stride: int = 25
    packet_loss_probability: float = 0.02
    communication_latency_ms: float = 20.0
    random_seed: int = 7

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


def _validate_config(config: CPSConfig) -> None:
    if not 0.0 < config.filter_alpha <= 1.0:
        raise ValueError("filter_alpha must be in (0, 1]")
    if config.light_current_threshold_a < 0:
        raise ValueError("light_current_threshold_a must be non-negative")
    if config.strain_alert_threshold < 0:
        raise ValueError("strain_alert_threshold must be non-negative")
    if config.thermal_rate_alert_k_s < 0:
        raise ValueError("thermal_rate_alert_k_s must be non-negative")
    if config.heartbeat_stride <= 0:
        raise ValueError("heartbeat_stride must be positive")
    if not 0.0 <= config.packet_loss_probability <= 1.0:
        raise ValueError("packet_loss_probability must be between 0 and 1")
    if config.communication_latency_ms < 0:
        raise ValueError("communication_latency_ms must be non-negative")


def _require_vector(transient: Mapping[str, np.ndarray], key: str, n: int | None = None) -> np.ndarray:
    if key not in transient:
        raise KeyError(f"transient is missing required field: {key}")
    arr = np.asarray(transient[key], dtype=float)
    if arr.ndim != 1:
        raise ValueError(f"{key} must be one-dimensional")
    if n is not None and len(arr) != n:
        raise ValueError("all transient arrays must have equal length")
    return arr


def run_cps(transient: Mapping[str, np.ndarray], config: CPSConfig | None = None) -> dict[str, np.ndarray]:
    """Run the cyber-physical layer over a detector transient.

    State policy:
    - FAULT: any required sensor value is non-finite.
    - PROTECT: strain or thermal-rate threshold is exceeded.
    - MONITOR: filtered detector current exceeds the light/event threshold.
    - IDLE: none of the above.

    The actuator code mirrors the state code. Telemetry is event-triggered:
    non-IDLE states transmit every sample, while IDLE sends heartbeat packets.
    """
    cfg = config or CPSConfig()
    _validate_config(cfg)

    time = _require_vector(transient, "time_s")
    n = len(time)
    current = _require_vector(transient, "total_current_a", n)
    strain = _require_vector(transient, "strain", n)
    temp_rate = _require_vector(transient, "temperature_rate_k_s", n)
    if n == 0:
        raise ValueError("transient must contain at least one sample")

    filtered = np.empty(n, dtype=float)
    state = np.empty(n, dtype=int)
    packet_requested = np.zeros(n, dtype=int)
    packet_delivered = np.zeros(n, dtype=int)
    packet_arrival_s = np.full(n, np.nan, dtype=float)

    rng = np.random.default_rng(cfg.random_seed)
    latency_s = cfg.communication_latency_ms / 1000.0
    previous_state = STATE_IDLE

    for i in range(n):
        sample_finite = np.isfinite(current[i]) and np.isfinite(strain[i]) and np.isfinite(temp_rate[i])
        if i == 0 or not np.isfinite(filtered[i - 1]):
            filtered[i] = current[i] if np.isfinite(current[i]) else np.nan
        elif np.isfinite(current[i]):
            filtered[i] = cfg.filter_alpha * current[i] + (1.0 - cfg.filter_alpha) * filtered[i - 1]
        else:
            filtered[i] = np.nan

        if not sample_finite:
            state[i] = STATE_FAULT
        elif abs(strain[i]) >= cfg.strain_alert_threshold or abs(temp_rate[i]) >= cfg.thermal_rate_alert_k_s:
            state[i] = STATE_PROTECT
        elif filtered[i] >= cfg.light_current_threshold_a:
            state[i] = STATE_MONITOR
        else:
            state[i] = STATE_IDLE

        changed = state[i] != previous_state
        request = state[i] != STATE_IDLE or changed or (i % cfg.heartbeat_stride == 0)
        packet_requested[i] = int(request)
        if request and rng.random() >= cfg.packet_loss_probability:
            packet_delivered[i] = 1
            packet_arrival_s[i] = time[i] + latency_s
        previous_state = int(state[i])

    return {
        "time_s": time.copy(),
        "raw_current_a": current.copy(),
        "filtered_current_a": filtered,
        "strain": strain.copy(),
        "temperature_rate_k_s": temp_rate.copy(),
        "cps_state_code": state,
        "actuator_command_code": state.copy(),
        "packet_requested": packet_requested,
        "packet_delivered": packet_delivered,
        "packet_arrival_s": packet_arrival_s,
    }


def cps_summary(result: Mapping[str, np.ndarray]) -> dict[str, float | int]:
    """Return compact system-level CPS metrics for one simulation run."""
    state = np.asarray(result["cps_state_code"], dtype=int)
    requested = np.asarray(result["packet_requested"], dtype=int)
    delivered = np.asarray(result["packet_delivered"], dtype=int)
    if len(state) == 0:
        raise ValueError("result must contain samples")
    transitions = int(np.count_nonzero(np.diff(state)))
    requested_count = int(requested.sum())
    delivered_count = int(delivered.sum())
    delivery_ratio = delivered_count / requested_count if requested_count else 1.0
    return {
        "samples": int(len(state)),
        "state_transitions": transitions,
        "idle_fraction": float(np.mean(state == STATE_IDLE)),
        "monitor_fraction": float(np.mean(state == STATE_MONITOR)),
        "protect_fraction": float(np.mean(state == STATE_PROTECT)),
        "fault_fraction": float(np.mean(state == STATE_FAULT)),
        "packets_requested": requested_count,
        "packets_delivered": delivered_count,
        "packet_delivery_ratio": float(delivery_ratio),
    }
