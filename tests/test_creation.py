import pytest
from ec.elliptic_curve import EllipticCurve
from ec.named_curves import registered_curves


# проверка создания именованных кривых
@pytest.mark.parametrize('name,error_expected',
    [(name, False) for name in registered_curves()] + [
    ('abc', 'Нет кривой с таким именем'),
], ids=['secp256r1', 'secp384r1', 'secp521r1', 'error'])
def test_named_curve_creation(name, error_expected):
    try:
        ec = EllipticCurve(name, a=1, b=1, p=1, G=(1,1))
        assert [not error_expected, ec.a != 1, ec.b != 1, ec.p != 1, ec.G.x != 1, ec.G.y != 1]
    except Exception as e:
        assert e.args[0] == error_expected


# проверка создания параметризованных кривых
@pytest.mark.parametrize('a,b,p,G,error_expected', [
    (-10, 21, 557, (2, 3), False),
    (4, None, 6, None, 'Не хватает параметров'),
    (-10, 21, 557, (1, 1), 'Точка не на кривой'),
], ids=['correct', 'error1', 'error2'])
def test_unnamed_curve_creation(a, b, p, G, error_expected):
    try:
        ec = EllipticCurve(a=a, b=b, p=p, G=G)
        assert [not error_expected, ec.a == a, ec.b == b, ec.p == p, ec.G.x == G[0], ec.G.y == G[1]]
    except Exception as e:
        assert e.args[0] == error_expected


# проверка создания нулевых точек эллиптических кривых
@pytest.mark.parametrize('a,b,p,G,error_expected', [
    (-10, 21, 557, (2, 3), False),
], ids=['correct'])
def test_zero_ec_point_creation(a, b, p, G, error_expected):
    try:
        ec = EllipticCurve(a=a, b=b, p=p, G=G)
        point = ec.create_point()
        assert point.is_zero
    except Exception as e:
        assert e.args[0] == error_expected


@pytest.mark.parametrize('a,b,p,G,x,y,on_curve', [
    (-10, 21, 557, (2, 3), 2, 3, True),
    (-10, 21, 557, (2, 3), 0, 0, False)
], ids=['correct', 'error'])
def test_ec_point_creation(a, b, p, G, x, y, on_curve):
    ec = EllipticCurve(a=a, b=b, p=p, G=G)
    try:
        point = ec.create_point(x=x, y=y)
        assert on_curve
    except Exception as e:
        assert not on_curve and e.args[0] == 'Точка не на кривой'