from .elliptic_curve import EllipticCurve
from .elliptic_point import ECPoint
from .named_curves import get_curve_order

from random import seed, randint
from time import time

def koblitz_encoding(curve: EllipticCurve, message: str | bytes) -> ECPoint:
    # это проверка что к этой кривой применим данных метод коблитза
    if curve.p % 4 != 3:
        raise Exception('Метод не применим!')

    # это подсчет размера так, чтобы точно не превысить допустимые границы для метода
    if isinstance(message, str):
        message = message.encode('utf-8')
    elif not isinstance(message, bytes):
        raise Exception('Неверный формат message')
    max_message_length = curve.p.bit_length() // 8 - 1
    #print(len(message), curve_bytes)
    if len(message) > max_message_length:
        raise Exception('Сообщение слишком длинное')

    a, b, p = curve.a, curve.b, curve.p
    message = int.from_bytes(message, 'big')

    xj = 100 * message
    for j in range(100):
        sj = xj**3 + a*xj + b
        if pow(sj, (p - 1) // 2, p) == 1:
            yj = pow(sj, (p + 1) // 4, p)
            return curve.create_point(x=xj, y=yj)
        xj += 1

    raise Exception('Не удалось закодировать сообщение')


def koblitz_decoding(curve: EllipticCurve, point: ECPoint) -> bytes:
    message = point.x // 100
    byte_length = (message.bit_length() + 7) // 8
    return message.to_bytes(byte_length, 'big')


def point_mult(point: ECPoint, k: int) -> ECPoint:
    bit_length = k.bit_length()
    p = point.curve.create_point()

    for i in range(bit_length - 1, -1, -1):
        p = p + p
        if (k >> i) & 1:
            p = p + point

    return p


def encrypt_point(curve: EllipticCurve, point: ECPoint, key: ECPoint) -> tuple[ECPoint, ECPoint]:
    seed(time())
    k = randint(0, get_curve_order(curve.curve_name) - 1)

    M1 = point_mult(curve.G, k)
    M2 = point + point_mult(key, k)

    return M1, M2


def decrypt_point(point1: ECPoint, point2: ECPoint, key: int) -> ECPoint:
    return point2 - point_mult(point1, key)


def write_point_to_file(filename, point):
    curve_name = point.curve.curve_name.encode('utf-8')
    len_curve_name = len(curve_name).to_bytes()

    with open(filename, 'wb') as f:
        f.write(len_curve_name)
        f.write(curve_name)

        if point.y % 2 == 0:
            f.write(b'\x00')
        else:
            f.write(b'\x01')
        f.write(point.x.to_bytes((point.x.bit_length() + 7) // 8, 'big'))


def read_point_from_file(filename):
    with open(filename, 'rb') as f:
        len_curve_name = int.from_bytes(f.read(1))
        curve_name = f.read(len_curve_name).decode('utf-8')

        even = f.read(1) == b'\x00'
        x = int.from_bytes(f.read(), 'big')

    curve = EllipticCurve(curve_name)
    p, a, b = curve.p, curve.a, curve.b
    s = (pow(x, 3, p) + a*x + b) % p
    y = pow(s, (p + 1) // 4, p)

    if even ^ (y % 2 == 0):
       y = p - y

    return curve.create_point(x=x, y=y)


def write_pair_point_to_file(filename, point1, point2):
    if isinstance(point1, list):
        num = len(point1)
        p1 = point1[0]
        p2 = point2[0]
    else:
        num = 1
        p1 = point1
        p2 = point2

    curve_name = p1.curve.curve_name.encode('utf-8')
    len_curve_name = len(curve_name).to_bytes()

    with open(filename, 'wb') as f:
        f.write(len_curve_name)
        f.write(curve_name)

        for i in range(num):
            x1 = p1.x.to_bytes((p1.x.bit_length() + 7) // 8, 'big')
            x2 = p2.x.to_bytes((p2.x.bit_length() + 7) // 8, 'big')
            y1 = b'\x00' if p1.y % 2 == 0 else b'\x01'
            y2 = b'\x00' if p2.y % 2 == 0 else b'\x01'

            x1_bl = len(x1)
            x2_bl = len(x2)

            f.write(x1_bl.to_bytes(4, 'big'))
            f.write(y1)
            f.write(x1)

            f.write(x2_bl.to_bytes(4, 'big'))
            f.write(y2)
            f.write(x2)

            p1 = point1[i+1] if i+1 < num else None
            p2 = point2[i+1] if i+1 < num else None


def read_pair_point_from_file(filename):
    with open(filename, 'rb') as f:
        len_curve_name = int.from_bytes(f.read(1))
        curve_name = f.read(len_curve_name).decode('utf-8')
        curve = EllipticCurve(curve_name)

        points = []
        while True:
            p, a, b = curve.p, curve.a, curve.b
            read_bytes = f.read(4)
            if not read_bytes:
                break
            bytes_to_read = int.from_bytes(read_bytes, 'big')
            even1 = f.read(1) == b'\x00'
            x1 = int.from_bytes(f.read(bytes_to_read), 'big')

            bytes_to_read = int.from_bytes(f.read(4), 'big')
            even2 = f.read(1) == b'\x00'
            x2 = int.from_bytes(f.read(bytes_to_read), 'big')

            s1 = (pow(x1, 3, p) + a*x1 + b) % p
            y1 = pow(s1, (p + 1) // 4, p)
            s2 = (pow(x2, 3, p) + a*x2 + b) % p
            y2 = pow(s2, (p + 1) // 4, p)

            if even1 ^ (y1 % 2 == 0):
                y1 = p - y1
            if even2 ^ (y2 % 2 == 0):
                y2 = p - y2

            points.append((curve.create_point(x=x1, y=y1),
                           curve.create_point(x=x2, y=y2)))

    if len(points) == 1:
        return points[0]
    else:
        return points