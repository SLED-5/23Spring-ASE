import math

class SYM:

    def __init__(self, at, txt):
        """"Init"""
        self.at, self.txt = at or 0, txt or ""
        self.n = 0
        self.has = {}
        self.most, self.mode = 0, None

    def add(self, x):
        if x != "?":
            self.n += 1
            if x in self.has:
                self.has[x] += 1
            else:
                self.has[x] = 1

            if self.has[x] > self.most:
                self.most, self.mode = self.has[x], x

    def mid(self):
        return self.mode


    def div(self):
        def fun(p):
            return p * math.log2(p)
        e = 0
        for k in self.has.values():
            e += fun(k/self.n)
        return -e