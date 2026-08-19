import numpy as np
import pytest
from flexpd.cps import CPSConfig, STATE_MONITOR, STATE_PROTECT, run_cps, cps_summary
from flexpd.model import DeviceParams, OperatingPoint, simulate_transient

def test_cps_output_lengths_and_delivery():
    transient = simulate_transient(DeviceParams(), OperatingPoint(), duration_s=0.2, dt_s=0.01)
    result = run_cps(transient, CPSConfig(packet_loss_probability=0.0, heartbeat_stride=5))
    n = len(transient["time_s"])
    assert all(len(v) == n for v in result.values())
    assert np.all(result["packet_delivered"] <= result["packet_requested"])
    assert np.all(result["packet_delivered"] == result["packet_requested"])

def test_strain_triggers_protect_state():
    transient = simulate_transient(DeviceParams(), OperatingPoint(strain=0.01), duration_s=0.1, dt_s=0.01)
    result = run_cps(transient, CPSConfig(strain_alert_threshold=0.008, thermal_rate_alert_k_s=1e9))
    assert np.all(result["cps_state_code"] == STATE_PROTECT)

def test_light_signal_enters_monitor_state_when_protection_disabled():
    transient = simulate_transient(DeviceParams(), OperatingPoint(), duration_s=0.1, dt_s=0.01)
    result = run_cps(transient, CPSConfig(light_current_threshold_a=1e-9, strain_alert_threshold=1.0, thermal_rate_alert_k_s=1e9))
    assert np.any(result["cps_state_code"] == STATE_MONITOR)

def test_full_packet_loss_is_reported():
    transient = simulate_transient(DeviceParams(), OperatingPoint(), duration_s=0.1, dt_s=0.01)
    result = run_cps(transient, CPSConfig(packet_loss_probability=1.0, heartbeat_stride=1))
    summary = cps_summary(result)
    assert summary["packets_requested"] > 0
    assert summary["packets_delivered"] == 0
    assert summary["packet_delivery_ratio"] == 0.0

def test_invalid_packet_loss_rejected():
    transient = simulate_transient(DeviceParams(), OperatingPoint(), duration_s=0.1, dt_s=0.01)
    with pytest.raises(ValueError):
        run_cps(transient, CPSConfig(packet_loss_probability=1.1))
