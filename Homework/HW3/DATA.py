"""
diff: Line 143 - 205
"""
import copy

from COLS import *
from ROW import *
import utils
# from eg import the
from config import the
class DATA:
    def __init__(self, src):
        self.rows, self.cols = [], None
        self.A, self.B, self.left, self.right, self.mid = None, None, None, None, None

        def fun(x):
            self.add(x)

        if type(src) == str:
            utils.fcsv(src, fun)
        else:
            self.cols = COLS(src)
            # utils.fMap(src or {}, fun)

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
        data = DATA(self.cols.name)

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

    def dist(self, row1, row2, cols=None):  #注意调用顺序
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
        # if cols == None:
        #     cols = self.cols
        def fun(row2):
            return {"row": row2, "dist": self.dist(row1, row2, cols)}

        # d = utils.fMap(rows, fun)
        return utils.fSort(utils.fMap(rows, fun), utils.lt("dist"))
        # return dict(sorted(d.items(), key=lambda x: x[1]))    # 最后可能要改，看utils怎么写的吧，逻辑是这样的, line 98也是
        # if rows == None:
        #     rows = self.rows
        #
        # return sorted(utils.fMap(rows, ))

    def half(self, rows=None, cols=None, above=None):
        if rows is None:
            rows = self.rows

        def project(row):
            return {"row": row, "dist": utils.cosine(d(row, A), d(row, B), c)[1]}

        def d(row1, row2):
            return self.dist(row1, row2, cols)

        some = utils.many(rows, the["Sample"])
        A = above
        if above is None:
            A = utils.any(some)
        B = self.around(A, None, some)[int(the["Far"] * len(rows))//1]["row"]
        c = d(A, B)
        left, right = [], []

        for n, tmp in enumerate(utils.fSort(utils.fMap(rows, project), utils.lt("dist"))):
            if n + 1 <= len(rows) // 2:
                left.append(tmp["row"])
                mid = tmp["row"]
            else:
                right.append(tmp["row"])

        return [left, right, A, B, mid, c]

    def cluster(self, rows=None, minn=None, cols=None, above=None):
        if rows is None:
            rows = self.rows
        if minn is None:
            minn = len(rows) ** the["min"]
        if cols is None:
            cols = self.cols.x

        node = self.clone(rows)
        if len(rows) > 2*minn:
            left, right, node.A, node.B, node.mid, others = node.half(rows, cols, above)
            node.left = node.cluster(left, minn, cols, node.A)
            node.right = node.cluster(right, minn, cols, node.B)

        return node

    def sway(self, above=None, rows=None, minn=None, cols=None):
        if rows is None:
            rows = self.rows
        if minn is None:
            minn = len(rows) ** the["min"]
        if cols is None:
            cols = self.cols.x

        node = self.clone(rows)
        if len(rows) > 2 * minn:
            left, right, node.A, node.B, node.mid, others = self.half(rows, cols, above)
            if self.better(node.B, node.A):
                left, right, node.A, node.B = right, left, node.B, node.A
            node.left = self.sway(node.A, left, minn, cols)

        return node
