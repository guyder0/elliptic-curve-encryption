import pytest, os
from ec.algorithms import *
from ec.elliptic_curve import EllipticCurve
from ec.named_curves import registered_curves

@pytest.mark.parametrize('message,curve,err',
    [('hello world!', name, False) for name in registered_curves()] +
    [('hello world!' * 10, name, 'Сообщение слишком длинное') for name in registered_curves()]
)
def test_koblitz_method(message, curve, err):
    ec = EllipticCurve(curve)

    if err:
        try:
            koblitz_encoding(ec, message)
            assert not 'требуется срабатывание ошибки'
        except Exception as e:
            assert e.args[0] == err

    else:

        point_from_message = koblitz_encoding(ec, message)
        assert point_from_message.on_curve()

        message_from_point = koblitz_decoding(ec, point_from_message).decode('utf-8')
        assert message == message_from_point


@pytest.mark.parametrize('name,k', [
    (name, k) for name in registered_curves() for k in [3, 40, 100]
])
def test_point_mult(name, k):
    curve = EllipticCurve(name)
    point = curve.G.copy()

    point_from_alg = point_mult(point, k)
    point_from_for = curve.create_point()

    for _ in range(k):
        point_from_for = point_from_for + point

    assert [point_from_alg.x, point_from_alg.y] == [point_from_for.x, point_from_for.y]


@pytest.mark.parametrize('name', [name for name in registered_curves()])
def test_file_onepoint_work(name):
    curve = EllipticCurve(name)
    point = curve.G.copy()

    write_point_to_file('temp', point)
    point_t = read_point_from_file('temp')
    os.remove('temp')

    assert [point_t.x, point_t.y] == [point.x, point.y]


@pytest.mark.parametrize('name', [name for name in registered_curves()])
def test_file_twopoints_work(name):
    curve = EllipticCurve(name)
    point1 = curve.G.copy()
    point2 = point1 + point1

    write_pair_point_to_file('temp', point1, point2)
    point1_t, point2_t = read_pair_point_from_file('temp')
    os.remove('temp')

    assert [point1_t.x, point1_t.y, point2_t.x, point2_t.y] == \
           [point1.x,   point1.y,   point2.x,   point2.y]