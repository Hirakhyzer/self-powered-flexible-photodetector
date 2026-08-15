#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from dataclasses import replace
from pathlib import Path

import numpy as np

from flexpd.io import load_config
from flexpd.model import static_response


def main() -> None:
    parser = argparse.ArgumentParser(description="Sweep a reduced-order model parameter.")
    parser.add_argument("--config", default="configs/baseline.json")
    parser.add_argument("--parameter", choices=["strain", "power_density_mw_cm2", "temperature_rise_k"], required=True)
    parser.add_argument("--start", type=float, required=True)
    parser.add_argument("--stop", type=float, required=True)
    parser.add_argument("--points", type=int, default=41)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    if args.points < 2:
        raise SystemExit("--points must be at least 2")

    params, op, _ = load_config(args.config)
    destination = Path(args.out)
    destination.parent.mkdir(parents=True, exist_ok=True)

    values = np.linspace(args.start, args.stop, args.points)
    rows = []
    for value in values:
        updated = replace(op, **{args.parameter: float(value)})
        result = static_response(params, updated)
        rows.append({args.parameter: float(value), **result})

    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} points to {destination}")


if __name__ == "__main__":
    main()
