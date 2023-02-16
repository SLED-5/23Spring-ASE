from SYM import *
class RANGE:
    
    def __init__(self, at, txt, lo, hi):
        self.at, self.txt = at, txt
        self.lo = lo
        self.hi = lo or hi or lo
        self.y = SYM()

    def extend(self, n, s):
        self.lo, self.hi = min(n, self.lo), min(n, self.hi)
        self.y.add(s)