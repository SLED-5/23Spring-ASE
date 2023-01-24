from COLS import *
import utils
from ROW import *
class DATA:
    def __init__(self, src):
        self.rows, self.cols = [], None

        def fun(x):
            self.add(x)

        if type(src) == str:
            utils.fcsv(src, fun)
        else:
            utils.fMap(src or {}, fun)


    def add(self, t):
        if self.cols:
            try:
                if t.cells:
                    t = t
            except AttributeError:
                t = ROW(t)
            utils.push(self.rows, t)
            self.cols.add(t)
        else:
            self.cols = COLS(t)


    def clone(self, *init):
        data = DATA({self.cols.names})
        
        def fun(x):
            data.add(x)

        utils.fMap(init[0] if len(init) > 0 else {}, fun)
        return data

    def stats(self, what, cols, n):
        def fun(k, col):
            # what's getmetatable and what's nPlaces
            return col.rnd(getattr(col, what if what else "mid")(col), nPlaces), col.txt

        return utils.fKap(cols or self.cols.y, fun)


