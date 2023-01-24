from NUM import *
from SYM import *
class COLS:

    def __init__(self, t, col, cols):
        self.name, self.all, self.x, self.y, self.klass = t, {}, {}, {}
        for n,s in enumerate(t):
            num = NUM(n, s)
            sym = SYM(n, s)
            col = s.find("^[A-Z]+") and num or sym




