# Data Directory

This repository does not include fabricated experimental data.

Recommended layout:

```text
data/
├── raw/          # Immutable instrument exports
├── processed/    # Cleaned/derived tables
└── metadata/     # Device, instrument, calibration, environment metadata
```

Do not overwrite raw measurements. Store scripts/parameters used for processing so every plotted point can be traced back to its source measurement.
