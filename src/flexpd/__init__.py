"""Reduced-order models for coupled piezo-pyro flexible photodetectors."""

from .metrics import detectivity_jones, eqe_from_responsivity
from .model import DeviceParams, OperatingPoint, static_response, simulate_transient

__all__ = [
    "DeviceParams",
    "OperatingPoint",
    "static_response",
    "simulate_transient",
    "detectivity_jones",
    "eqe_from_responsivity",
]

__version__ = "0.1.0"
