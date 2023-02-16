import math
import utils
class NUM:

    def __init__(self, at, txt):
        self.at, self.txt = at or 0, txt or ""
        self.n = 0
        self.lo, self.hi = float('inf'), -float('inf')
        self.w = self.txt.find("-$" ) and -1 or 1
        self.ok = True
        self.has = []

    def add(self, x, n=None):
        if x != "?":
            n = n or 1
            self.n += n
            self.has[x] = n + (self.has[x] or 0)
            if self.has[x] > self.most:
                self.most, self.mode = self.has[x], x

    def adds(self, col, t):
        for x in t or []:
            self.add(x)
        return col

    def has(self):
        if not self.ok:
            self.has = sorted(self.has)
        return self.has

    def mid(self):
        return self.mu

    def div(self):
        return (self.m2<0 or self.n<2) and 0 or (self.m2/(self.n-1))**0.5

    def rnd(self, x, n):
        if x == "?":
            return x
        return utils.rnd(x,n)

    def norm(self, n):
        return n == "?" and n or (n - self.lo)/(self.hi - self.lo + 1E-32)

    def dist(self, n1, n2):
        if n1 == "?" and n2 == "?":
            return 1
        n1, n2 = self.norm(n1), self.norm(n2)

        if n1 == "?":
            n1 = (n2 < 0.5) and 1 or 0
        if n2 == "?":
            n2 = (n1 < 0.5) and 1 or 0

        return abs(n1 - n2)