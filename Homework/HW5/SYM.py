import math


class SYM:

    def __init__(self, at, txt):
        """"Init"""
        self.at, self.txt = at or 0, txt or ""
        self.n = 0
        self.has = {}
        self.most, self.mode = 0, None

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

    def mid(self):
        return self.mode


    def div(self):
        def fun(p):
            return p * math.log(p, 2)
        e = 0
        for k in self.has.values():
            e -= fun(k/self.n)
        return e

    # def rnd(self, x, n):
    #     return x

    def dist(self, s1, s2):
        if s1 == "?" and s2 == "?":
            return 1
        if s1 == s2:
            return 0
        else:
            return 1