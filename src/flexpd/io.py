"""Configuration and CSV helpers."""

from __future__ import annotations

import csv
import json
from dataclasses import fields
from pathlib import Path
from typing import Any

import numpy as np

from .model import DeviceParams, OperatingPoint


def load_config(path: str | Path) -> tuple[DeviceParams, OperatingPoint, dict[str, Any]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    valid_device = {f.name for f in fields(DeviceParams)}
    valid_op = {f.name for f in fields(OperatingPoint)}
    unknown_device = set(payload.get("device", {})) - valid_device
    unknown_op = set(payload.get("operating_point", {})) - valid_op
    if unknown_device or unknown_op:
        raise ValueError(
            f"Unknown config keys: device={sorted(unknown_device)}, operating_point={sorted(unknown_op)}"
        )
    return (
        DeviceParams(**payload.get("device", {})),
        OperatingPoint(**payload.get("operating_point", {})),
        payload.get("transient", {}),
    )


def write_timeseries_csv(path: str | Path, data: dict[str, np.ndarray]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    keys = list(data)
    n = len(data[keys[0]])
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(keys)
        for i in range(n):
            writer.writerow([float(data[k][i]) for k in keys])
