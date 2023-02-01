import math
import utils
class NUM:

    def __init__(self, at, txt):
        self.at, self.txt = at or 0, txt or ""
        self.n, self.mu, self.m2 = 0, 0, 0
        self.lo, self.hi = float('inf'), float('-inf')
        self.w = self.txt.find("-$" ) and -1 or 1

    def add(self,n):
        if n != "?":
            self.n += 1
            d = n - self.mu
            self.mu += d/self.n
            self.m2 += d*(n - self.mu)
            self.lo = min(n, self.lo)
            self.hi = max(n, self.hi)

    def mid(self):
        return self.mu

    def div(self):
        return (self.m2<0 or self.n<2) and 0 or (self.m2/(self.n-1))**0.5

    def rnd(self, x, n):
        if x == "?":
            return x
        return utils.rnd(x,n)

    # 1E-32不确定，我推测是e**-32
    def norm(self, n):
        return n == "?" and n or (n - self.lo)/(self.hi - self.lo + math.exp(-32))

    def dist(self, n1, n2):
        if n1 == "?" and n2 == "?":
            return 1
        n1, n2 = self.norm(n1), self.norm(n2)

        if n1 == "?":
            n1 = n2 < 0.5 and 1 or 0
        if n2 == "?":
            n2 = n1 < 0.5 and 1 or 0

        return abs(n1 - n2)