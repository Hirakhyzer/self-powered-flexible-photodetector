# Experimental Validation Protocol

## Objective

Determine whether piezoelectric and pyroelectric effects measurably and reproducibly enhance the zero-bias response of a flexible ZnO/perovskite/ZnO photodetector, and separate those contributions from ordinary photovoltaic, photoconductive, thermal, and mechanical artifacts.

## Device metadata to record

For every device, record substrate, electrode materials, ZnO deposition/growth method and thickness, perovskite composition/thickness, encapsulation, active area, device orientation, batch, and fabrication date. Preserve microscopy/XRD/optical characterization links where available.

## Minimum electrical/optical characterization

1. Dark I–V and illuminated I–V over a small symmetric bias range, emphasizing 0 V.
2. Zero-bias current under repeated light on/off cycles.
3. Spectral response across the intended wavelength range.
4. Power-dependent photocurrent over multiple illumination intensities.
5. Noise current spectral density if detectivity will be reported quantitatively.

## Piezoelectric isolation experiment

- Stabilize device temperature before each measurement.
- Use a calibrated bending fixture or tensile stage.
- Record bend radius and convert it to strain using the actual multilayer neutral-axis geometry where possible.
- Measure both strain polarities/orientations if the architecture permits.
- Repeat flat → strained → flat cycles to test reversibility and drift.
- Include a mechanically similar control device lacking the intended piezo-active contribution.

## Pyroelectric isolation experiment

- Keep mechanical strain fixed.
- Apply controlled temperature ramps or modulated illumination while independently measuring device temperature near the active area.
- Compare current with `dT/dt`, not only absolute temperature.
- Sweep modulation frequency to determine whether transient peaks follow the thermal time constant.
- Distinguish thermoelectric/contact effects by reversing geometry or using suitable controls.

## Coupled experiment

Use a factorial design with at least:

| Condition | Light | Strain | Thermal transient |
|---|---:|---:|---:|
| A | off/on | 0 | minimal |
| B | off/on | +strain | minimal |
| C | off/on | 0 | controlled |
| D | off/on | +strain | controlled |
| E | off/on | -strain | controlled |

Analyze whether condition D can be predicted from independently calibrated piezo and pyro terms. A systematic interaction residual is evidence to test a true coupling term.

## Flexible-device reliability

Perform repeated bending cycles at specified radius/strain and periodically re-measure dark current, zero-bias responsivity, rise/fall time, and spectral response. Report the number of devices and device-to-device distribution, not only the best device.

## Recommended raw-data schema

Each time-series CSV should include:

`timestamp_s, device_id, wavelength_nm, power_density_mw_cm2, bias_v, strain, bend_radius_mm, temperature_k, current_a, light_state`

A separate metadata file should include instrument models, calibration dates, sampling rates, filters, and environmental conditions.

## Scientific controls

Potential confounders include photothermal Seebeck voltages, contact-barrier changes under bending, piezoresistance, microcracking, ionic migration/hysteresis in the perovskite, humidity/oxygen exposure, and instrument offsets. Controls should be designed so these effects can be identified rather than folded into a single enhancement factor.
