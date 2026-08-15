import numpy as np
import pytest

from flexpd.model import DeviceParams, OperatingPoint, simulate_transient, static_response


def test_positive_tensile_default_increases_gain():
    params = DeviceParams()
    flat = static_response(params, OperatingPoint(strain=0.0))
    tensile = static_response(params, OperatingPoint(strain=0.005))
    assert tensile["coupling_gain"] > flat["coupling_gain"]
    assert tensile["responsivity_a_w"] > flat["responsivity_a_w"]


def test_negative_strain_changes_response_direction():
    params = DeviceParams()
    compressed = static_response(params, OperatingPoint(strain=-0.005))
    tensile = static_response(params, OperatingPoint(strain=0.005))
    assert compressed["polarization_voltage_v"] < tensile["polarization_voltage_v"]


def test_transient_has_pyro_sign_change():
    data = simulate_transient(DeviceParams(), OperatingPoint(strain=0.0), duration_s=2.0, dt_s=0.002, modulation_hz=1.0)
    pyro = data["pyro_current_a"]
    assert np.max(pyro) > 0
    assert np.min(pyro) < 0


def test_transient_shapes_match():
    data = simulate_transient(DeviceParams(), OperatingPoint(), duration_s=1.0, dt_s=0.01)
    lengths = {len(v) for v in data.values()}
    assert lengths == {101}


def test_negative_power_rejected():
    with pytest.raises(ValueError):
        static_response(DeviceParams(), OperatingPoint(power_density_mw_cm2=-1.0))
