#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt

from flexpd.io import load_config, write_timeseries_csv
from flexpd.model import static_response, simulate_transient


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a coupled piezo-pyro photodetector simulation.")
    parser.add_argument("--config", default="configs/baseline.json")
    parser.add_argument("--out", default="results/baseline")
    args = parser.parse_args()

    params, op, transient = load_config(args.config)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    metrics = static_response(params, op)
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    series = simulate_transient(params, op, **transient)
    write_timeseries_csv(out_dir / "transient.csv", series)

    plt.figure(figsize=(8, 4.5))
    plt.plot(series["time_s"], series["total_current_a"] * 1e6, label="total")
    plt.plot(series["time_s"], series["photocurrent_a"] * 1e6, label="photo", alpha=0.8)
    plt.plot(series["time_s"], series["pyro_current_a"] * 1e6, label="pyro", alpha=0.8)
    plt.xlabel("Time (s)")
    plt.ylabel("Current (µA)")
    plt.title("Synthetic zero-bias coupled piezo–pyro response")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "current_vs_time.png", dpi=180)
    plt.close()

    print(json.dumps(metrics, indent=2))
    print(f"Wrote outputs to {out_dir}")


if __name__ == "__main__":
    main()
