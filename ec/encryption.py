from ec.named_curves import get_curve_order
from ec.algorithms import *
from ec.elliptic_curve import EllipticCurve
import random, time


class ECC_encryption:
    def __init__(self, curve_name):
        self.curve = EllipticCurve(curve_name)
        self.curve_name = curve_name
        self.private_key = None
        self.public_key = None


    def generate_key_pair(self, passphrase, private_key_filename, public_key_filename):
        if len(passphrase) < 8:
            raise Exception('Пароль недостаточной длины')

        random.seed(time.time())
        max_message_length = self.curve.p.bit_length() // 8 - 1
        curve_order = get_curve_order(self.curve_name).bit_length() // 8

        signed = (b'ECC' + random.randbytes(max_message_length - 3))

        private_key = int.from_bytes(signed[3:]) # смотрим что извлекается из сигнатуры+ключа
        public_key = point_mult(self.curve.G, private_key)

        esk_private_key = int.from_bytes(passphrase.encode('utf-8')[:curve_order])
        esk_public_key = point_mult(self.curve.G, esk_private_key)
        esk_point = koblitz_encoding(self.curve, signed)
        private1, private2 = encrypt_point(self.curve, esk_point, esk_public_key)

        write_pair_point_to_file(private_key_filename, private1, private2)
        write_point_to_file(public_key_filename, public_key)


    def select_private_key(self, passphrase, filename):
        curve_order = get_curve_order(self.curve_name).bit_length() // 8
        key = int.from_bytes(passphrase.encode('utf-8')[:curve_order])

        try:
            private1, private2 = read_pair_point_from_file(filename, self.curve)
            sk = decrypt_point(private1, private2, key)
            sk = koblitz_decoding(self.curve, sk)
        except Exception:
            raise Exception('Скорее всего для этого секретного ключа выбрана не та кривая!')

        if sk[:3] != b'ECC':
            raise Exception('Неверная парольная фраза')
        else:
            self.private_key = int.from_bytes(sk[3:])


    def select_public_key(self, filename):
        self.public_key = read_point_from_file(filename, self.curve)


    def encrypt_message(self, source, target):
        if self.public_key is None:
            raise Exception('Не выбран открытый ключ')

        with open(source, 'r') as f:
            point = koblitz_encoding(self.curve, f.read())
        point1, point2 = encrypt_point(self.curve, point, self.public_key)
        write_pair_point_to_file(target, point1, point2)


    def decrypt_message(self, source, target):
        if self.private_key is None:
            raise Exception('Не выбран секретный ключ')

        point1, point2 = read_pair_point_from_file(source, self.curve)
        point = decrypt_point(point1, point2, self.private_key)
        msg = koblitz_decoding(self.curve, point).decode('utf-8')

        with open(target, 'w') as f:
            f.write(msg)