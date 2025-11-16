from .elliptic_curve import EllipticCurve
from .elliptic_point import ECPoint

def koblitz_encoding(curve: EllipticCurve, message: str) -> ECPoint:
    # это проверка что к этой кривой применим данных метод коблитза
    if curve.p % 4 != 3:
        raise Exception('Метод не применим!')

    # это подсчет размера так, чтобы точно не превысить допустимые границы для метода
    message = message.encode('utf-8')
    curve_bytes = curve.p.bit_length() // 8
    print(len(message), curve_bytes)
    if len(message) >= curve_bytes:
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


def koblitz_decoding(curve: EllipticCurve, point: ECPoint) -> str:
    message = point.x // 100
    byte_length = (message.bit_length() + 7) // 8
    return message.to_bytes(byte_length, 'big').decode('utf-8')


def point_mult(point: ECPoint, k: int) -> ECPoint:
    bit_length = k.bit_length()
    p = point.curve.create_point()

    for i in range(bit_length - 1, -1, -1):
        p = p + p
        if (k >> i) & 1:
            p = p + point

    return p


def write_point_to_file(filename, point):
    with open(filename, 'wb') as f:
        if point.y % 2 == 0:
            f.write(b'\x00')
        else:
            f.write(b'\x01')
        f.write(point.x.to_bytes((point.x.bit_length() + 7) // 8, 'big'))


def read_point_from_file(filename, curve):
    with open(filename, 'rb') as f:
        even = f.read(1) == b'\x00'
        x = int.from_bytes(f.read(), 'big')

    p, a, b = curve.p, curve.a, curve.b
    s = (pow(x, 3, p) + a*x + b) % p
    y = pow(s, (p + 1) // 4, p)

    if even ^ (y % 2 == 0):
       y = p - y

    return curve.create_point(x=x, y=y)


def write_pair_point_to_file(filename, point1, point2):
    x1 = point1.x.to_bytes((point1.x.bit_length() + 7) // 8, 'big')
    x2 = point2.x.to_bytes((point2.x.bit_length() + 7) // 8, 'big')
    y1 = b'\x00' if point1.y % 2 == 0 else b'\x01'
    y2 = b'\x00' if point2.y % 2 == 0 else b'\x01'

    x1_bl = len(x1)
    x2_bl = len(x2)

    with open(filename, 'wb') as f:
        f.write(x1_bl.to_bytes(4, 'big'))
        f.write(y1)
        f.write(x1)

        f.write(x2_bl.to_bytes(4, 'big'))
        f.write(y2)
        f.write(x2)


def read_pair_point_from_file(filename, curve):
    p, a, b = curve.p, curve.a, curve.b

    with open(filename, 'rb') as f:
        bytes_to_read = int.from_bytes(f.read(4), 'big')
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

    return curve.create_point(x=x1, y=y1), \
           curve.create_point(x=x2, y=y2)