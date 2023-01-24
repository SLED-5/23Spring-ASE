from COLS import *
import utils
from ROW import *
import COLS
class DATA:
    def __init__(self, src):
        self.rows, self.cols = {}, None

        def fun(x):
            self.add(x)

        if type(src) == str:
            utils.csv(src, fun)
        else:
            utils.fMap(src or {}, fun)


    def add(self, t):
        if self.cols:
            t = t.cells and t and ROW(t)
            utils.push(self.rows, t)
            self.cols.add(t)
        else:
            self.cols = COLS(t)


    def clone(self, init):
        data = DATA({self.cols.names})

        def fun(x):
            data.add(x)

        utils.fMap(init or {}, fun)
        return data

    def stats(self, what, cols, n):
        def fun(k, col):
            # what's getmetatable and what's nPlaces
            return col.rnd(getmetatable(col)[what or "mid"](col), nPlaces), col.txt

        return utils.fKap(cols or self.cols.y, fun)


