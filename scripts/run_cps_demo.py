#!/usr/bin/env python3
"""Run the photodetector physical model through the CPS edge/network/controller layer."""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from flexpd.cps import CPSConfig, STATE_NAMES, cps_summary, run_cps
from flexpd.io import load_config
from flexpd.model import simulate_transient


def write_csv(path: Path, data: dict[str, np.ndarray]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    keys = list(data)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(keys)
        for i in range(len(data[keys[0]])):
            writer.writerow([data[key][i] for key in keys])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/baseline.json")
    parser.add_argument("--cps-config", default="configs/cps_demo.json")
    parser.add_argument("--out", default="results/cps_demo")
    args = parser.parse_args()

    params, op, transient_cfg = load_config(args.config)
    cps_payload = json.loads(Path(args.cps_config).read_text(encoding="utf-8"))
    cps_cfg = CPSConfig(**cps_payload)

    physical = simulate_transient(params, op, **transient_cfg)
    result = run_cps(physical, cps_cfg)
    summary = cps_summary(result)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "cps_timeseries.csv", result)
    (out / "cps_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(result["time_s"], result["filtered_current_a"] * 1e6, label="filtered current (µA)")
    ax2 = ax.twinx()
    ax2.step(result["time_s"], result["cps_state_code"], where="post", label="CPS state")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Detector current (µA)")
    ax2.set_ylabel("State code")
    ax2.set_yticks(sorted(STATE_NAMES))
    ax2.set_yticklabels([STATE_NAMES[i] for i in sorted(STATE_NAMES)])
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(out / "cps_overview.png", dpi=180)
    plt.close(fig)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
