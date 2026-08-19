"""Models for self-powered flexible photodetectors and CPS integration."""
from .cps import (
    CPSConfig,
    STATE_FAULT,
    STATE_IDLE,
    STATE_MONITOR,
    STATE_NAMES,
    STATE_PROTECT,
    cps_summary,
    run_cps,
)
from .metrics import detectivity_jones, eqe_from_responsivity
from .model import DeviceParams, OperatingPoint, simulate_transient, static_response

__all__ = [
    "DeviceParams",
    "OperatingPoint",
    "static_response",
    "simulate_transient",
    "detectivity_jones",
    "eqe_from_responsivity",
    "CPSConfig",
    "run_cps",
    "cps_summary",
    "STATE_IDLE",
    "STATE_MONITOR",
    "STATE_PROTECT",
    "STATE_FAULT",
    "STATE_NAMES",
]

__version__ = "0.2.0"
