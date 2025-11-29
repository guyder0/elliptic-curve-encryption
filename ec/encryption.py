from ec.named_curves import get_curve_order
from ec.algorithms import *
from ec.elliptic_curve import EllipticCurve

from random import seed, randbytes
from time import time


class ECC_encryption:
    def __init__(self, curve_name):
        self.curve = EllipticCurve(curve_name)
        self.curve_name = curve_name
        self.block_length = self.curve.p.bit_length() // 8 - 1
        self.private_key = None
        self.public_key = None


    def generate_key_pair(self, passphrase, private_key_filename, public_key_filename):
        if len(passphrase) < 8: raise Exception('Пароль недостаточной длины')
        if private_key_filename is None: raise Exception('Не выбран путь для сохранения закрытого ключа')
        if public_key_filename is None: raise Exception('Не выбран путь для сохранения открытого ключа')

        seed(time())
        max_message_length = self.curve.p.bit_length() // 8 - 1
        curve_order = get_curve_order(self.curve_name).bit_length() // 8

        signed = (b'ECC' + randbytes(max_message_length - 3))

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
            private1, private2 = read_pair_point_from_file(filename)
        except:
            raise Exception('Не удалось считать закрытый ключ из файла')
        if private1.curve.curve_name != self.curve_name:
            raise Exception('Несоответсвие выбранной кривой и записанной в файл точки')
        sk = decrypt_point(private1, private2, key)
        sk = koblitz_decoding(self.curve, sk)

        if sk[:3] != b'ECC':
            raise Exception('Неверная парольная фраза или выбранный ключ')
        else:
            self.private_key = int.from_bytes(sk[3:])


    def select_public_key(self, filename):
        try:
            public = read_point_from_file(filename)
        except:
            raise Exception('Не удалось считать открытый ключ из файла')
        if public.curve.curve_name != self.curve_name:
            raise Exception('Несоответсвие выбранной кривой и записанной в файл точки')
        self.public_key = public


    def encrypt_message(self, source, target):
        if self.public_key is None: raise Exception('Не выбран открытый ключ')
        if source is None: raise Exception('Не выбран файл для шифрования')
        if target is None: raise Exception('Не выбран путь для сохранения зашифрованного файла')

        with open(source, 'r') as f:
            message = f.read().encode('utf-8')
            len_message = len(message)
            num_blocks = len_message // self.block_length
            num_blocks += 1 if len_message % self.block_length != 0 else 0

        point1 = [None] * num_blocks
        point2 = [None] * num_blocks
        for i in range(num_blocks):
            block = message[i*self.block_length:(i+1)*self.block_length]
            point = koblitz_encoding(self.curve, block)
            point1[i], point2[i] = encrypt_point(self.curve, point, self.public_key)
        write_pair_point_to_file(target, point1, point2)


    def decrypt_message(self, source, target):
        if self.private_key is None: raise Exception('Не выбран секретный ключ')
        if source is None: raise Exception('Не выбран файл для расшифрования')
        if target is None: raise Exception('Не выбран путь для сохранения расшифрованного файла')

        points = read_pair_point_from_file(source)
        if not isinstance(points, list):
            points = [points]

        if points[0][0].curve.curve_name != self.curve_name:
            raise Exception('Файл зашифрован на другой эллиптической кривой!')

        msg = b''
        for point1, point2 in points:
            point = decrypt_point(point1, point2, self.private_key)
            msg += koblitz_decoding(self.curve, point)

        with open(target, 'w') as f:
            try:
                f.write(msg.decode('utf-8'))
            except Exception:
                raise Exception('Не удалось преобразовать расшифрованное сообщение по кодировке utf-8.' +
                                'Возможно, этот файл был зашифрован с другими ключами.')