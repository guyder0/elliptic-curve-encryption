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