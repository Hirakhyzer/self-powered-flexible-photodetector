# Contributing

Contributions are welcome when they improve scientific clarity, reproducibility, testing, documentation, or the reduced-order/CPS models.

## Before opening a pull request

1. Create a focused branch and keep the change small enough to review.
2. Run `pytest` and any simulation script affected by the change.
3. Document units for every new physical parameter.
4. Provide provenance for material/device parameters from measurements or literature.
5. Clearly distinguish measured data, fitted parameters, and synthetic simulation output.
6. Add or update tests when behavior changes.

## Scientific-model changes

For new equations or coupling terms, explain the physical assumption, dimensional consistency, expected validity range, and calibration strategy. A phenomenological term must be labeled as such rather than presented as a first-principles law.

## Data contributions

Do not overwrite raw measurements. Store raw data separately from processed outputs, record device/sample identifiers and experimental conditions, and avoid committing large generated result files unless they are intentionally curated examples.

## CPS changes

Network, estimator, controller, or telemetry changes should state assumptions about latency, packet loss, sampling rate, thresholds, and failure handling. Safety-critical claims require evidence beyond this simulation scaffold.

## Style

Prefer readable Python, explicit names with units where useful, deterministic random seeds for experiments, and documentation that lets another researcher reproduce the result from a clean checkout.
