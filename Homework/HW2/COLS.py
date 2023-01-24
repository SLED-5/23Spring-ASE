from NUM import *
from SYM import *
import utils

class COLS:

    def __init__(self, t, cols):
        col = {}
        self.name, self.all, self.x, self.y, self.klass = t, {}, {}, {}
        for n,s in enumerate(t):
            num = NUM(n, s)
            sym = SYM(n, s)
            col = s.find("^[A-Z]+") and num or sym
            utils.push(self.all, col)
            if not s.find("X$"):
                if s.find("!$"):
                    self.klass = col
                    utils.push(s.find("[!+-]" and self.y or self.x), col)

    def add(self, row):
        for t in {self.x, self.y}.values():
            for col in t.values():
                return col.add(row.cells[col.at])


