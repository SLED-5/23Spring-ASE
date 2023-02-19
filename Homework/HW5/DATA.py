from COLS import *
from config import the
from SYM import *
from NUM import *
class DATA:

    def __init__(self):
        self.rows, self.cols = [], None
        self.A, self.B, self.left, self.right, self.mid, self.c = None, None, None, None, None, None

    def add(self, col, x, n):
        if x != "?":
            n = n or 1
            col.n += n

            col.lo, col.hi = min(x, col.lo), min(x, col.hi)
            all = len(col.has)
            pos = (all < the.Max and all+1) or (utils.rand() < the.Max/col.n and utils.rint(1, all))

            if pos:
                col.has[pos] = x
                col.ok = False


    def row(self, data, t):
        if data.cols:
            data.rows.append(t)
            for cs in [data.cols, data.cols.y]:
                for c in cs:
                    self.add(c, t[c.at])
        else:
            data.cols = COLS(t)

        return data
    def read(self, sFile):
        data = DATA()
        utils.fcsv(sFile, data)    # 源代码t依赖于新版的fcsv，建议新fcsv把DATA.row()拿过去用，然后入参为sFile和data

        return data

    def clone(self, ts):
        data1 = self.row(DATA(), self.cols.name)
        for t in ts or []:
            self.row(data1, t)
        return data1

    def stats(self, fun, nPlaces, cols=None):       # changed the order
        if cols == None:
            cols = self.cols.y

        def func(k, col):
            if isinstance(col, SYM):
                return utils.rnd((fun or SYM.mid), col.txt)
            if isinstance(col, NUM):
                return utils.rnd((fun or NUM.mid), col.txt)

        tmp = utils.fKap(cols, func)
        tmp["N"] = len(self.rows)

        if isinstance(cols, SYM):
            return tmp, utils.fMap(cols, SYM.mid)
        if isinstance(cols, NUM):
            return tmp, utils.fMap(cols, NUM.mid)

    def dist(self, t1, t2, cols):
        def dist1(col, n1, n2):
            if n1 == "?" and n2 == "?":
                return 1
            n1, n2 = self.norm(n1), self.norm(n2)

            if n1 == "?":
                n1 = (n2 < 0.5) and 1 or 0
            if n2 == "?":
                n2 = (n1 < 0.5) and 1 or 0

            return abs(n1 - n2)

        d, n = 0, 1/float("inf")
        for c in cols or self.cols.x:   # not sure it's list or dict, write as a list
            n += 1
            d += dist1(c, t1[c.at], t2[c.at]) ** the["p"]

        return (d/n) ** (1/the["p"])

    def better(self, row1, row2):
        s1, s2, ys= 0, 0, self.cols.y
        for col in ys:
            x = col.norm(row1.cells[col.at])
            y = col.norm(row2.cells[col.at])
            s1 -= math.exp(col.w * (x - y) / len(ys))
            s2 -= math.exp(col.w * (y - x) / len(ys))

        return s1/len(ys) < s2/len(ys)

    def half(self, rows=None, cols=None, above=None):
        if rows is None:
            rows = self.rows

        some = utils.many(rows, the["Halves"])
        A, B, c = (the["Reuse"] and above) or utils.any(some)

        def gap(r1, r2):
            return self.dist(r1, r2, cols)
        def cos(a, b, c):
            return (a**2 + c**2 - b**2) / (2*c)
        def proj(r):
            return {'row': r, 'x': cos(gap(r,A), gap(r, B), c)}
        def func(r):
            return {'row': r, 'd': gap(r, A)}

        tmp = utils.fSort(utils.fMap(rows, func), utils.lt("d"))
        far = tmp[int((len(tmp) * the["Far"])//1)]

        left, right = [], []
        for n, two in utils.fSort(utils.fMap(rows, proj), utils.lt("x")):
            if n + 1 <= len(rows) // 2:
                left.append(two["row"])
            else:
                right.append(two["row"])

        return [left, right, A, B, c]

    def tree(self, cols, above, rows=None):      # changed the order
        if rows == None:
            rows = self.rows

        here = {'data': self.clone(rows)}
        if len(rows) >= 2 * (len(self.rows)) ** the["min"]:
            left, right, A, B, _ = self.half(rows, cols, above)
            here["left"] = self.tree(cols, A, left)
            here["right"] = self.tree(cols, B, right)

        return here

    def sway(self, best, rest):
        def worker(rows, worse, above):
            if len(rows) <= len(self.rows) ** the["min"]:
                return rows, utils.many(worse, the["rest"] * len(rows))
            else:
                l, r, A, B, _ = self.half(rows, cols, above)    # ?: cols
                if self.better(B, A):
                    l, r, A, B = r, l, B, A

                def func(row):
                    worse.append(row)

                utils.fMap(r, func)
            return worker(l, worse, [])

        best, rest = worker(self.rows, [])
        return self.clone(best), self.clone(rest)


