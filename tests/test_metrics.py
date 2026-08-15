import math

import pytest

from flexpd.metrics import detectivity_jones, eqe_from_responsivity, responsivity_from_eqe


def test_responsivity_eqe_round_trip():
    r = responsivity_from_eqe(0.7, 525.0)
    assert r > 0
    assert eqe_from_responsivity(r, 525.0) == pytest.approx(0.7)


def test_detectivity_positive():
    dstar = detectivity_jones(0.3, 1e-6, 1e-10)
    assert math.isfinite(dstar)
    assert dstar > 1e10


def test_invalid_dark_current():
    with pytest.raises(ValueError):
        detectivity_jones(0.3, 1e-6, 0.0)
