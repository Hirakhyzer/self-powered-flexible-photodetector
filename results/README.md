# Results Directory

Simulation scripts write generated CSV/JSON/PNG outputs here. Most generated files are ignored by Git to avoid mixing reproducible code with derived artifacts.

Example:

```bash
python scripts/run_simulation.py --config configs/baseline.json --out results/baseline
```

Synthetic simulation results must not be represented as experimental measurements.
