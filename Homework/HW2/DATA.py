from COLS import *
from ROW import *
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
            # this place is not sure
            t = ROW(t)
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

    def stats(self, what, cols, nPlaces):
        def fun(k, col):
            # what's getmetatable is not sure
            return col.rnd(getattr(col, what or "mid"), nPlaces), col.txt

        return utils.fKap(cols or self.cols.y, fun)


