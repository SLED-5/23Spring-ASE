import math


class SYM:

    def __init__(self, at, txt):
        """"Init"""
        self.at, self.txt = at or 0, txt or ""
        self.n = 0
        self.has_list = {}
        self.most, self.mode = 0, None

    def add(self, x, n=None):
        if x != "?":
            n = n or 1
            self.n += n
            self.has_list[x] = n + (0 if x not in self.has_list else self.has_list[x])
            if self.has_list[x] > self.most:
                self.most, self.mode = self.has_list[x], x

    def adds(self, t):
        for x in t or []:
            self.add(x)
        return self

    def mid(self):
        return self.mode


    def div(self):
        def fun(p):
            return p * math.log(p, 2)
        e = 0
        for k in self.has_list.values():
            e -= fun(k/self.n)
        return e

    def has(self):
        return self.has_list

    # def rnd(self, x, n):
    #     return x

    def dist(self, s1, s2):
        if s1 == "?" and s2 == "?":
            return 1
        if s1 == s2:
            return 0
        else:
            return 1

    def bin(self, x):
        return x