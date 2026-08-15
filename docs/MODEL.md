# Reduced-Order Model

## Purpose

This model is designed for **transparent hypothesis testing and parameter sensitivity analysis**. It is not a drift-diffusion solver, density-functional model, or TCAD implementation. Its parameters should be fitted or replaced using measurements from the actual device stack.

## State variables and inputs

- illumination wavelength, `wavelength_nm`;
- incident optical power density, `power_density_mw_cm2`;
- active area, `active_area_mm2`;
- engineering strain, `strain`;
- transient temperature rise, `temperature_rise_k`;
- dark current at zero bias.

## Baseline responsivity

For an external quantum efficiency `eta`, the unity-gain responsivity is

`R0 = eta * q * lambda / (h*c)`.

This relation is exact for a detector where each collected electron-hole pair contributes one elementary charge and `eta` captures the collected carrier fraction. Any effective EQE above unity in the reduced-order output should therefore be interpreted as an **effective gain representation**, not automatically as true primary quantum efficiency.

## Polarization representation

The interface modulation is condensed to

`Vpol = Kpiezo * strain + Kpyro * DeltaT`.

`Kpiezo` and `Kpyro` are **effective coefficients**, not fundamental ZnO constants. They absorb geometry, screening, crystallographic orientation, interface charge, electrode boundary conditions, and field partitioning across the heterostructure.

The carrier-separation gain is

`G = exp(clip(alpha * Vpol, -Gmax, +Gmax))`.

The clipping is a numerical/phenomenological guard against unphysical runaway in a model that omits space-charge and transport saturation.

## Pyroelectric transient current

The transient current is calculated from

`Ipyro = p_eff * A * dT/dt`.

The default `p_eff = 1e-5 C m^-2 K^-1` is an **illustrative placeholder**, not a claimed measured coefficient for the proposed device. Replace it with a value appropriate to the ZnO morphology, orientation, temperature range, and device geometry being studied.

## Thermal model

Illumination drives a first-order temperature response:

`d(DeltaT)/dt = (DeltaT_target - DeltaT) / tau_th`.

This is sufficient to study frequency dependence qualitatively. Real devices may require spatial heat diffusion, substrate heat capacity, convection/radiation, and wavelength-dependent absorption.

## Detectivity

The package reports a shot-noise-limited estimate:

`D* = R*sqrt(A_cm2) / sqrt(2*q*Idark)`.

This is optimistic unless shot noise dominates. Experimental analysis should measure noise spectral density and include 1/f, Johnson, generation-recombination, instrumentation, and environmental noise.

## Calibration strategy

1. Measure zero-bias dark current and illuminated current at zero strain and quasi-steady temperature.
2. Fit baseline EQE/responsivity without piezo/pyro terms.
3. Apply known tensile/compressive strain at steady temperature and fit `Kpiezo` and coupling strength.
4. Hold strain fixed and use controlled temperature ramps or chopped illumination to fit thermal time constant and `p_eff`.
5. Test simultaneous strain and thermal excitation **without refitting** to evaluate whether the additive polarization assumption is sufficient.
6. If systematic residuals remain, add a nonlinear cross-term only when supported by data.

## Limitations

The model currently omits explicit band offsets, trap dynamics, ionic migration, hysteresis, contact resistance, recombination kinetics, ferroelectric effects in the absorber, wavelength-dependent absorption, bending-induced cracking, and long-term degradation. These should be introduced incrementally and validated against measurements.
