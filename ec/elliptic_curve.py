from .named_curves import get_curve, find_curve
from .elliptic_point import ECPoint


class EllipticCurve:
    def __init__(self, name=None,  a=None, b=None, p=None, G=None):
        if name is not None and not find_curve(name):
            raise Exception('Нет кривой с таким именем')

        params = get_curve(name) if name else (a, b, p, G)
        if not all([p is not None for p in params]):
            raise Exception('Не хватает параметров')

        self.a, self.b, self.p = params[:3]
        self.G = self.create_point(params[3][0], params[3][1])
        if not self.G.on_curve():
            raise Exception('Генератор не на кривой')


    def create_point(self, x=None, y=None):
        return ECPoint(self, x, y)


    def __repr__(self):
        return f'y² = x³ + ax + b (mod p)\n' + \
               f'a = {self.a:x}\n' + \
               f'b = {self.b:x}\n' + \
               f'p = {self.p:x}'