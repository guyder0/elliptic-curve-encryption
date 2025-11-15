class ECPoint:
    def __init__(self, curve, x=None, y=None):
        self.curve = curve
        if x is None or y is None:
            self.is_zero = True
            self.x, self.y = None, None
        else:
            self.is_zero = False
            self.x, self.y = x % self.curve.p, y % self.curve.p

    def copy(self):
        return ECPoint(self.curve, self.x, self.y)

    def on_curve(self):
        if self.is_zero:
            return True

        left_part = self.y ** 2 % self.curve.p
        right_part = (self.x ** 3 + self.curve.a * self.x + self.curve.b) % self.curve.p
        if left_part == right_part:
            return True
        else:
            return False


    def __repr__(self):
        str1 = 'Point ' + ('ZERO' if self.is_zero else f'({self.x}, {self.y})') + '\n'
        str2 = f'On curve: {hash(self.curve)}' if self.on_curve() else 'Not on curve'
        return str1 + str2


    def __add__(self, other):
        # сложение определено только между точками эллиптической кривой
        if not isinstance(other, ECPoint) or not self.on_curve() or not other.on_curve():
            return NotImplemented

        # сложение с нулевой точкой
        if self.is_zero:
            return other.copy()
        elif other.is_zero:
            return self.copy()

        x1 = self.x; y1 = self.y
        x2 = other.x; y2 = other.y
        p = self.curve.p

        # случай, когда в результате получается 0
        if x1 == x2 and y1 == -y2 % p:
            return ECPoint(self.curve)

        if x1 == x2: # в силу структуры эллиптической группы, это сразу ведет к тому, что точки совпадают
            s = (3 * x1**2 + self.curve.a) * pow(2 * y1, -1, p) % p
        else:
            s = (y1 - y2) * pow(x1 - x2, -1, p) % p

        xr = (s**2 - x1 - x2) % p
        yr = (-y1 + s * (x1 - xr)) % p

        return ECPoint(self.curve, xr, yr)