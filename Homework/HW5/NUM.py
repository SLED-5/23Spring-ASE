import math
import utils
from config import the
class NUM:

    def __init__(self, at, txt):
        self.at, self.txt = at or 0, txt or ""
        self.n = 0
        self.lo, self.hi = float('inf'), -float('inf')
        self.w = self.txt.find("-$" ) and -1 or 1
        self.ok = True
        self.has = []

    def add(self, col, x, n):
        if x != "?":
            n = n or 1
            col.n += n

            col.lo, col.hi = min(x, col.lo), min(x, col.hi)
            all = len(col.has)
            pos = (all < the.Max and all + 1) or (utils.rand() < the.Max / col.n and utils.rint(1, all))

            if pos:
                col.has[pos] = x
                col.ok = False

    def adds(self, col, t):
        for x in t or []:
            self.add(x)
        return col

    def has(self):  # ?: self.ok or 写个参数col, col.ok?
        if not self.ok:
            self.has = sorted(self.has)
        else:
            self.ok = True

        return self.has

    def mid(self):
        return utils.per(self.has(), 0.5)

    def div(self):
        return (utils.per(self.has(), 0.9) - utils.per(self.has(), 0.1)) / 2.58

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


