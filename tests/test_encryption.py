import pytest, os
from ec.encryption import *
from ec.elliptic_curve import EllipticCurve
from ec.named_curves import registered_curves


@pytest.mark.parametrize('name', [name for name in registered_curves()])
def test_file_work(name):
    pass