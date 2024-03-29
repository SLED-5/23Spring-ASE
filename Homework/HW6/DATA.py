from COLS import *
from config import Is
from SYM import SYM


class DATA:

    def __init__(self, src=None, rows=None):
        if rows is None:
            rows = []
        self.rows, self.cols = [], None
        self.A, self.B, self.left, self.right, self.mid, self.c = None, None, None, None, None, None

        def add(t):
            self.row(t)     #: ?:不确定对不对，因为lua中t凭空来的，感觉是lambda的意思
        if src is None:
            return
        if type(src) == str:
            utils.fcsv(src, add)
        else:
            self.cols = COLS(src.cols.name)

        utils.fMap(rows or [], add)

    # def add(self, col, x, n):
    #     if x != "?":
    #         n = n or 1
    #         col.n += n
    #
    #         col.lo, col.hi = min(x, col.lo), min(x, col.hi)
    #         all = len(col.has)
    #         pos = (all < the.Max and all + 1) or (utils.rand() < the.Max / col.n and utils.rint(1, all))
    #
    #         if pos:
    #             col.has[pos] = x
    #             col.ok = False

    def row(self, t):
        if self.cols:
            self.rows.append(t)
            for cs in [self.cols.x, self.cols.y]:
                for c in cs:
                    c.add(t[c.at])
                    # self.add(c, t[c.at])
        else:
            self.cols = COLS(t)

        return self

    def read(self, sFile):
        data = DATA()
        utils.fcsv(sFile, data.row)  # 源代码t依赖于新版的fcsv，建议新fcsv把DATA.row()拿过去用，然后入参为sFile和data

        return data

    def clone(self, ts):
        data1 = DATA()
        data1.row(self.cols.name)
        for t in ts or []:
            data1.row(t)
        return data1

    def stats(self, fun=None, nPlaces=None, cols=None):  # changed the order
        if cols is None:
            cols = self.cols.y

        def func(col):
            if type(col) == SYM:
                if fun is not None:
                    return utils.rnd(fun(col)), col.txt
                else:
                    return utils.rnd(SYM.mid(col)), col.txt
            if type(col) == NUM.NUM:
                if fun is not None:
                    return utils.rnd(fun(col)), col.txt
                else:
                    return utils.rnd(NUM.NUM.mid(col)), col.txt

        tmp = utils.fKap(cols, func)
        res_dict = {}
        for i in tmp:
            # first is value, second is the key
            res_dict[str(i[1])] = i[0]
        res_dict["N"] = len(self.rows)
        return res_dict

        # if type(cols[0]) == SYM:
        #     return tmp, utils.fMap(cols, SYM.mid)
        # if type(cols[0]) == NUM.NUM:
        #     return tmp, utils.fMap(cols, NUM.NUM.mid)

    def dist(self, t1, t2, cols=None):
        def dist1(col, n1, n2):
            if n1 == "?" and n2 == "?":
                return 1
            if type(col) == SYM:
                if n1 == n2:
                    return 0
                return 1
            else:
                n1, n2 = col.norm(n1), col.norm(n2)
                if n1 == "?":
                    n1 = (n2 < 0.5) and 1 or 0
                if n2 == "?":
                    n2 = (n1 < 0.5) and 1 or 0

                return abs(n1 - n2)

        if cols is None:
            cols = self.cols.x

        d, n = 0, 0
        for c in cols:
            n += 1
            d += dist1(c, t1[c.at], t2[c.at]) ** Is["p"]

        return (d / n) ** (1 / Is["p"])

    def better(self, row1, row2):
        s1, s2, ys = 0, 0, self.cols.y
        for col in ys:
            x = col.norm(row1[col.at])
            y = col.norm(row2[col.at])
            s1 -= math.exp(col.w * (x - y) / len(ys))
            s2 -= math.exp(col.w * (y - x) / len(ys))

        return s1 / len(ys) < s2 / len(ys)

    def betters(self, n):
        def fun(r1, r2):
            return self.better(r1, r2)

        tmp = utils.fSort(self.rows, fun)

        return n and utils.slice(tmp, 1, n), utils.slice(tmp, n+1) or tmp

    def half(self, rows=None, cols=None, above=None):
        if rows is None:
            rows = self.rows
        some = utils.many(rows, Is["Halves"])
        A = (Is["Reuse"] and above) or utils.any(some)

        def gap(r1, r2):
            return self.dist(r1, r2, cols)

        def cos(a, b, c):
            return (a ** 2 + c ** 2 - b ** 2) / (2 * c)

        def proj(r):
            return {'row': r, 'x': cos(gap(r, A), gap(r, B), c)}

        def func(r):
            return {'row': r, 'd': gap(r, A)}

        tmp = utils.fSort(utils.fMap(some, func), utils.lt("d"))
        far = tmp[int((len(tmp) * Is["Far"]) // 1) - 1]
        B, c = far["row"], far["d"]

        left, right = [], []
        it_dict = utils.fSort(utils.fMap(rows, proj), utils.lt("x"))
        for n, two in zip(range(len(it_dict)), it_dict):
            if n + 1 <= len(rows) // 2:
                left.append(two["row"])
            else:
                right.append(two["row"])

        # evals = Is["Reuse"] and above and 1 or 2
        if Is["Reuse"] and above and 1:
            evals = 1
        else:
            evals = 2

        return [left, right, A, B, c, evals]

    def tree(self, cols=None, above=None, rows=None):  # changed the order
        if rows is None:
            rows = self.rows

        here = {'data': self.clone(rows)}
        if len(rows) >= 2 * (len(self.rows)) ** Is["min"]:
            left, right, A, B, other1, other2 = self.half(rows, cols, above)
            here["left"] = self.tree(cols, A, left)
            here["right"] = self.tree(cols, B, right)

        return here

    def sway(self):
        def worker(rows, worse, evals0, above=None):
            if len(rows) <= len(self.rows) ** Is["min"]:
                return rows, utils.many(worse, Is["rest"] * len(rows)), evals0
            else:
                l, r, A, B, c, evals = self.half(rows, None, above)
                if self.better(B, A):
                    l, r, A, B = r, l, B, A

                def func(row):
                    worse.append(row)

                utils.fMap(r, func)
            return worker(l, worse, evals+evals0, [])   # ?:[]不是A吗

        best, rest, evals = worker(self.rows, [], 0)
        return self.clone(best), self.clone(rest), evals

    def div(self, col):
        if type(col) == NUM.NUM:
            return col.div()
        elif type(col) == SYM:
            return col.div()
        else:
            print("error in data.div")
        return 0
