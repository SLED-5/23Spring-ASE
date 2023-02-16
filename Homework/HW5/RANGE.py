from SYM import *
class RANGE:
    
    def __init__(self, at, txt, lo, hi):
        self.at, self.txt = at, txt
        self.lo = lo
        self.hi = lo or hi or lo
        y = SYM()
