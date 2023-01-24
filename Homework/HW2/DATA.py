import pandas as pd
from COLS import *
import utils
import ROW
import COLS
class DATA:
    def __init__(self, src, fun):
        self.rows, self.cols = {}, None
        if type(src) == str:
            pd.read_csv(src, self.add())
        else:
            utils.fMap(src or {}, fun)


    def add(self, t):
        if self.cols:
            row_t = ROW()
            t = t.cells and t and row_t
            utils.push(self.rows, t)
        else:
            self.cols = COLS(t)


    def clone(self, init):
        data = DATA({self.cols.names})
        x = self.fun1(data)
        utils.fMap(init or {}, x)
        return data

    def fun1(self, x):
        return self.add(x)

    def stats(self, what, cols, n):
        fun = {}
        # function fun(k, col) return col:rnd(getmetatable(col)[what or "mid"](col), nPlaces), col.txt end
        return utils.fKap(cols or self.cols.y, fun)

    def fun2(self, k, col):
        return 1


