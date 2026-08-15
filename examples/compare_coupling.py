"""Compare flat, strained, heated, and jointly coupled operating points."""

from flexpd.model import DeviceParams, OperatingPoint, static_response

params = DeviceParams()
conditions = {
    "baseline": OperatingPoint(),
    "tensile_0.5pct": OperatingPoint(strain=0.005),
    "thermal_plus_2K": OperatingPoint(temperature_rise_k=2.0),
    "coupled": OperatingPoint(strain=0.005, temperature_rise_k=2.0),
}

for label, op in conditions.items():
    result = static_response(params, op)
    print(
        f"{label:18s} R={result['responsivity_a_w']:.4f} A/W "
        f"gain={result['coupling_gain']:.3f} "
        f"D*={result['detectivity_jones_shot_noise_limited']:.3e} Jones"
    )
