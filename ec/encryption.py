from ec.named_curves import get_curve_order
from ec.algorithms import *
from ec.elliptic_curve import EllipticCurve
import random, time


def generate_key_pair(curve_name, private_key_filename, public_key_filename):
    random.seed(time.time())
    curve = EllipticCurve(curve_name)

    private_key = random.randint(0, get_curve_order(curve_name) - 1)
    public_key = point_mult(curve.G, private_key)

    with open(private_key_filename, 'wb') as f:
        f.write(private_key.to_bytes((private_key.bit_length + 7) // 8, 'big'))
        write_point_to_file(public_key_filename, public_key)


def encrypt_message():
    pass