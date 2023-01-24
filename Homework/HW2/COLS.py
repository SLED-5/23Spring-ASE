from NUM import *
from SYM import *
import utils
import re

class COLS:

    def __init__(self, t):
        self.name, self.all, self.x, self.y, self.klass = t, [], [], [], []
        for n,s in enumerate(t):
            col =NUM(n, s) if s.find("^[A-Z]+") else SYM(n, s)
            utils.push(self.all, col)
            if not re.search("X$", s):
                if re.search("!$", s):
                    self.klass = col
                utils.push(self.y if re.search("[!+-]$", s) else self.x, col)

    def add(self, row):
        for t in [self.x, self.y]:
            for col in t:
                col.add(row.cells[col.at])
            


