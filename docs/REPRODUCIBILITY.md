# Reproducibility Guide

This checklist is intended for figures, experiments, theses, and publications produced with this repository.

## Record the exact software state

Always record:

- Git commit SHA or release tag;
- Python version and operating system;
- installed package versions;
- configuration file used;
- random seed for stochastic CPS/network experiments;
- command used to generate each result.

## Baseline commands

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
python scripts/run_simulation.py --config configs/baseline.json --out results/baseline
python scripts/run_cps_demo.py --config configs/cps_demo.json --out results/cps_demo
```

## Minimum experiment metadata

For detector/device studies record wavelength, optical power or power density, active area, strain convention and magnitude, temperature history, modulation frequency, sampling interval, and every fitted/calibrated parameter.

For CPS studies additionally record packet-loss probability, latency, filter/controller thresholds, telemetry cadence, state definitions, and random seed.

## Provenance rules

- Raw experimental measurements must remain immutable.
- Synthetic outputs must be labeled as simulation data.
- Fitted parameters must be separated from directly measured quantities.
- Literature-derived parameters should include a citation and units.
- Generated figures should be traceable to a script/config pair.

## Recommended result bundle

For each publishable experiment, preserve:

```text
experiment_name/
├── config.json
├── environment.txt
├── command.txt
├── metrics.json
├── timeseries.csv
└── figure.png
```

The goal is that another researcher can reproduce the reported result from the recorded commit without guessing hidden settings.
