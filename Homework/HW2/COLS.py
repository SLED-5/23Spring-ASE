from NUM import *
from SYM import *
import utils

class COLS:

    def __init__(self, t):
        self.name, self.all, self.x, self.y, self.klass = t, {}, {}, {}, {}
        for n,s in enumerate(t):
            col = s.find("^[A-Z]+") and NUM(n, s) or SYM(n, s)
            utils.push(self.all, col)
            if not s.find("X$"):
                if s.find("!$"):
                    self.klass = col
                utils.push(s.find("[!+-]") and self.y or self.x, col)

    def add(self, row):
        for x in self.x:
            for t in self.y:
                for col in t.values():
                    col.add(row.cells[col.at])


