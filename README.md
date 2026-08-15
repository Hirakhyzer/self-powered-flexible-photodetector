# Self-Powered Flexible Photodetectors Enabled by Coupled Piezo–Pyro Effects

[![CI](https://github.com/Hirakhyzer/self-powered-flexible-photodetector/actions/workflows/ci.yml/badge.svg)](https://github.com/Hirakhyzer/self-powered-flexible-photodetector/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-research%20prototype-orange)

A reproducible research-code framework for exploring **self-powered flexible ZnO/perovskite/ZnO photodetectors** whose zero-bias photoresponse is modulated by coupled piezoelectric and pyroelectric effects.

> **Research-status notice:** this repository contains a physics-inspired reduced-order model and synthetic simulation outputs. It does **not** claim experimental validation, a fabricated device, or measured performance. Model parameters must be calibrated against experiments or trusted literature before quantitative scientific use.

## Project motivation

The target device concept is a flexible ZnO/perovskite/ZnO heterostructure operated at zero external bias. ZnO provides a non-centrosymmetric wurtzite semiconductor platform in which mechanical deformation and transient thermal changes can alter interfacial electrostatics. The perovskite absorber supplies strong visible-light absorption and photocarrier generation. The research hypothesis is that piezoelectric and pyroelectric polarization can jointly modify carrier separation/transport at the interfaces and thereby improve self-powered photodetection.

Potential application directions include wearable health monitoring, low-power IoT sensing, and human–machine interfaces.

## What this repository provides

- A transparent reduced-order device model for zero-bias photoresponse.
- Separate piezoelectric, pyroelectric, and coupled response terms.
- Time-domain simulation under chopped illumination.
- Responsivity, EQE, and shot-noise-limited specific detectivity calculations.
- Parameter sweeps over strain, optical power, and thermal transients.
- CSV/PNG result generation for reproducible figures.
- Unit tests and GitHub Actions continuous integration.
- Experimental validation protocol and PhD-oriented research roadmap.

## Repository structure

```text
self-powered-flexible-photodetector/
├── configs/                # Example simulation configuration
├── data/                   # Place raw/processed experimental data here
├── docs/                   # Model assumptions, protocol, roadmap
├── examples/               # Small programmatic examples
├── results/                # Generated outputs (not committed by default)
├── scripts/                # Command-line simulation/sweep scripts
├── src/flexpd/             # Python package
├── tests/                  # Unit tests
├── .github/workflows/      # CI
├── pyproject.toml
└── README.md
```

## Quick start

```bash
git clone https://github.com/Hirakhyzer/self-powered-flexible-photodetector.git
cd self-powered-flexible-photodetector
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Run the baseline simulation:

```bash
python scripts/run_simulation.py --config configs/baseline.json --out results/baseline
```

Run a strain sweep:

```bash
python scripts/run_sweep.py --config configs/baseline.json --parameter strain --start -0.01 --stop 0.01 --points 41 --out results/strain_sweep.csv
```

Run tests:

```bash
pytest
```

## Model overview

The package uses a deliberately compact model so each assumption is inspectable.

1. **Baseline photovoltaic response**

   The unity-gain responsivity is calculated from external quantum efficiency \(\eta\):

   \[
   R_0 = \eta \frac{q\lambda}{hc}.
   \]

2. **Piezoelectric modulation**

   An effective strain-dependent interfacial potential is represented by a calibrated coefficient. The sign of strain therefore matters.

3. **Pyroelectric contribution**

   A transient pyroelectric current is calculated as

   \[
   I_{pyro}=pA\frac{dT}{dt},
   \]

   where \(p\) is an effective pyroelectric coefficient and \(A\) is active area.

4. **Coupled carrier-separation gain**

   The polarization-induced interfacial potential modulates the baseline zero-bias photocurrent through a bounded exponential gain. This term is phenomenological and should be fitted to measured strain/temperature-dependent data.

5. **Detectivity**

   A shot-noise-limited estimate is provided:

   \[
   D^*=\frac{R\sqrt{A}}{\sqrt{2qI_{dark}}}.
   \]

See [`docs/MODEL.md`](docs/MODEL.md) for assumptions, units, limitations, and calibration guidance.

## Example output columns

The transient simulator writes:

```text
time_s, light_on, temperature_rise_k, temperature_rate_k_s,
strain, polarization_voltage_v, coupling_gain, photocurrent_a,
pyro_current_a, total_current_a
```

No pre-generated “experimental-looking” data are committed. Generate your own synthetic runs with the scripts, then replace/augment them with real measurements under `data/`.

## Suggested experimental programme

A strong validation programme should compare at least four conditions:

- dark vs illuminated at zero bias;
- flat vs tensile/compressive bending;
- steady temperature vs controlled heating/cooling transients;
- uncoupled controls vs the full ZnO/perovskite/ZnO device.

The repository includes a more detailed protocol in [`docs/EXPERIMENT_PROTOCOL.md`](docs/EXPERIMENT_PROTOCOL.md).

## Literature anchors

The repository design is motivated by published reports showing: (i) self-powered ZnO/perovskite heterojunction photodetection, (ii) piezo-phototronic modulation at flexible ZnO/perovskite interfaces, and (iii) pyroelectric/pyro-phototronic enhancement in ZnO-based heterojunction photodetectors. These papers are **context**, not validation of this exact ZnO/perovskite/ZnO HBPT architecture.

1. *A high-performance self-powered broadband photodetector based on vertical MAPbBr3/ZnO heterojunction*, Materials Science in Semiconductor Processing 169 (2024) 107943. DOI: `10.1016/j.mssp.2023.107943`.
2. G. Hu et al., *Enhanced performances of flexible ZnO/perovskite solar cells by piezo-phototronic effect*, Nano Energy 23 (2016) 27–33. DOI: `10.1016/j.nanoen.2016.02.057`.
3. *Light-Triggered Pyroelectric Nanogenerator Based on a pn-Junction for Self-Powered Near-Infrared Photosensing*, ACS Nano (2017). DOI: `10.1021/acsnano.7b03560`.
4. *Pyro-Phototronic Effect-Enhanced Photocurrent of a Self-Powered Photodetector Based on ZnO Nanofiber Arrays/BaTiO3 Films*, ACS Applied Materials & Interfaces 15 (2023) 46031–46040. DOI: `10.1021/acsami.3c08880`.

## Research questions

- How strongly does strain-induced polarization alter band bending and carrier extraction at each ZnO/perovskite interface?
- Under what illumination modulation frequencies does the pyroelectric transient materially contribute to the detector signal?
- Are piezo and pyro effects additive, antagonistic, or nonlinear under simultaneous mechanical and thermal excitation?
- Which layer thicknesses, contact work functions, and encapsulation strategies maximize zero-bias responsivity while preserving flexibility and stability?
- How does performance evolve under repeated bending and environmental aging?

## Reproducibility and scientific integrity

- Keep raw measurements immutable under `data/raw/`.
- Record device ID, geometry, illumination wavelength/power, bend radius, temperature history, and instrument settings for each run.
- Report measured values separately from fitted model parameters.
- Do not present synthetic outputs from this repository as experimental measurements.
- Add uncertainty estimates and repeat-device statistics before drawing performance conclusions.

## Contributing

Research contributions are welcome through issues and pull requests. Please include units, provenance for material parameters, and a short validation note for any new physical model.

## Citation

If this repository contributes to an academic output, cite the specific release/commit used and the primary experimental literature supporting any material parameters.
