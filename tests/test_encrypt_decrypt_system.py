import pytest, os
from ec.algorithms import *
from ec.elliptic_curve import EllipticCurve
from ec.named_curves import registered_curves
import time, random


@pytest.mark.parametrize('name,message',
                         [(name, message)
                          for name in registered_curves()
                          for message in ['message', 'hello world']])
def test_encrypt_decrypt_system(name, message):
    curve = EllipticCurve(name)
    random.seed(time.time())

    M = koblitz_encoding(curve, message)
    SK = random.randint(0, get_curve_order(name) - 1)
    PK = point_mult(curve.G, SK)

    M1, M2 = encrypt_point(curve, M, PK)
    new_M = decrypt_point(M1, M2, SK)
    new_message = koblitz_decoding(curve, new_M).decode('utf-8')

    assert message == new_message