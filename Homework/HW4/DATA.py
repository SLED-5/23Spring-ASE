import copy
import utils

from COLS import *
from ROW import *
from config import the
class DATA:
    def __init__(self, src):
        self.rows, self.cols = [], None
        self.A, self.B, self.left, self.right, self.mid, self.c = None, None, None, None, None, None

        def fun(x):
            self.add(x)

        if type(src) == str:
            utils.fcsv(src, fun)
        else:
            utils.fMap(src, fun)
            # self.cols = COLS(src)

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
        # return copy.deepcopy(self)
        data = DATA([self.cols.name])

        def fun(x):
            data.add(x)

        utils.fMap(init[0] if len(init) > 0 else {}, fun)
        return data

    def stats(self, what, cols, nPlaces):
        def fun(col):
            # what's getmetatable and what's nPlaces
            return col.rnd(getattr(col, what if what else "mid")(), nPlaces), col.txt

        return utils.fKap(cols or self.cols.y, fun)

    def better(self, row1, row2):
        s1, s2, ys= 0, 0, self.cols.y
        for col in ys:
            x = col.norm(row1.cells[col.at])
            y = col.norm(row2.cells[col.at])
            s1 -= math.exp(col.w * (x - y) / len(ys))
            s2 -= math.exp(col.w * (y - x) / len(ys))

        return s1/len(ys) < s2/len(ys)

    def dist(self, row1, row2, cols=None):
        if cols is None:
            cols = self.cols.x

        n, d = 0, 0
        for col in cols:
            n += 1
            tmp_result = col.dist(row1.cells[col.at], row2.cells[col.at]) ** the["p"]
            # print(tmp_result)
            d += tmp_result

        return (d/n) ** (1/the["p"])

    def around(self, row1, cols=None, rows=None):
        if rows is None:
            rows = self.rows
        def fun(row2):
            return {"row": row2, "dist": self.dist(row1, row2, cols)}

        # d = utils.fMap(rows, fun)
        return utils.fSort(utils.fMap(rows, fun), utils.lt("dist"))

    def half(self, rows=None, cols=None, above=None):
        if rows is None:
            rows = self.rows

        def project(row):
            x, y = utils.cosine(self.dist(row, A), self.dist(row, B), c)
            row.x = row.x or x
            row.y = row.y or y
            return {'row': row, 'x': x, 'y': y}

        def d(row1, row2):
            return self.dist(row1, row2, cols)

        A = above
        if above is None:
            A = utils.any(rows)
        B = self.furthest(A, rows)["row"]
        c = d(A, B)
        left, right = [], []

        for n, tmp in enumerate(utils.fSort(utils.fMap(rows, project), utils.lt("x"))):
            if n + 1 <= len(rows) // 2:
                left.append(tmp["row"])
                mid = tmp["row"]
            else:
                right.append(tmp["row"])

        return [left, right, A, B, mid, c]

    def cluster(self, rows=None, cols=None, above=None):
        if rows is None:
            rows = self.rows

        if cols is None:
            cols = self.cols.x

        node = self.clone(rows)
        if len(rows) > 2:
            left, right, node.A, node.B, node.mid, node.c = node.half(rows, cols, above)
            node.left = node.cluster(left, cols, node.A)
            node.right = node.cluster(right, cols, node.B)

        return node

    def furthest(self, row1=None, rows=None, cols=None):
        t = self.around(row1, cols, rows)
        return t[-1]