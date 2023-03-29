import math

class NUM:
    def __init__(self, t=[]):
        self.n, self.mu, self.m2, self.sd = 0, 0, 0, 0
        for x in t:
            self.add(x)

    # This part not sure
    def NUM(self, t):
        self.n, self.mu, self.m2, self.sd = 0, 0, 0, 0
        if t is not None:
            for x in enumerate(t):
                self.add(x)
        return self

    def add(self, x):
        self.n += 1
        d = x - self.mu
        self.mu = self.mu + d/self.n
        self.m2 += d * (x - self.mu)
        if self.n < 2:
            self.sd = 0
        else:
            self.sd = math.pow((self.m2 / (self.n - 1)), 0.5)

    def delta(self, other):
        e, y, z = 1e-32, self, other
        return abs(y.mu - z.mu) / ((e + y.sd ** 2 / y.n + z.sd ** 2 / z.n) ** 0.5)

