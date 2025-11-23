import pytest
from ec.elliptic_curve import EllipticCurve


@pytest.mark.parametrize('a,b,p,G,x,y,period', [
    (7, 1, 101, (0, 1), 0, 1, 116),
    (-10, 21, 557, (2, 3), 2, 3, 189),
    (7, 12, 103, (-1, 2), -1, 2, 13),
])
def test_period_of_point(a, b, p, G, x, y, period):
    ec = EllipticCurve(a=a, b=b, p=p, G=G)
    p = ec.create_point()
    p0 = ec.create_point(x=x, y=y)
    for _ in range(period - 1):
        p = p + p0
        assert not p.is_zero
    assert (p + p0).is_zero


@pytest.mark.parametrize('a,b,p,G,x,y', [
    (7, 1, 101, (0, 1), 0, 1),
    (-10, 21, 557, (2, 3), 2, 3),
    (7, 12, 103, (-1, 2), -1, 2),
])
def test_sub_of_point(a, b, p, G, x, y):
    ec = EllipticCurve(a=a, b=b, p=p, G=G)
    p1 = ec.create_point(x, y)
    p2 = ec.create_point(x, y)
    assert (p1 - p2).is_zero