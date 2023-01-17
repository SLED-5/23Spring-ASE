class NUM:

    def __init__(self):
        self.n, self.mu, self.m2 = 0, 0, 0
        self.lo, self.hi = float('inf'), float('-inf')

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
