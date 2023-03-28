import RANGE
import copy
import functools
import math
import re
import csv
import json
import sys

from DATA import *
from RULE import *
from RANGE import *
cnt = 0
# Numerics
Seed = 937162211


def show(node, what=None, cols=None, nPlaces=None, lvl=0):
    if node is not None:
        lvl = lvl or 0
        # if node.left is None or lvl == 0:
        print("|.." * lvl, end="")
        if node.left is None:
            print(o(node.rows[-1].cells[-1]))
        else:
            # print("|.." * lvl)
            print("%.f" % rnd(100 * node.c))
        show(node.left, what, cols, nPlaces, lvl + 1)
        show(node.right, what, cols, nPlaces, lvl + 1)


def rint(lo, hi=None):
    i = rand(lo, hi)
    return math.floor(0.5 + i)


def rand(lo=None, hi=None):
    global Seed
    lo = lo or 0
    if hi is None:
        hi = 1
    Seed = (16807 * Seed) % 2147483647
    return lo + (hi - lo) * Seed / 2147483647


def rnd(n, nPlaces=2):
    mult = 10 ** nPlaces
    return math.floor(n * mult + 0.5) / mult


def cosine(a, b, c):
    x1 = (a ** 2 + c ** 2 - b ** 2) / (2 * c)
    x2 = max(0, min(1, x1))
    y = (a ** 2 - x2 ** 2) ** 0.5
    return x2, y


# Lists
def fMap(t, fun):
    u = []
    if type(t) == dict:
        for k, v in t.items():
            v, k = fun(v)
            u[k or (1 + len(u))] = v
    elif type(t) == list:
        for v in t:
            new_v = fun(v)
            u.append(new_v)
    else:
        print("error in fMap, t is neither a list nor dict")
    return u


def fKap(t, fun):
    u = []
    if type(t) == dict:
        u = {}
        for k, v in t.items():
            v, k = fun(k, v)
            u[k] = v
    elif type(t) == list:
        for v in t:
            v = fun(v)
            u.append(v)

    return u


def fSort(t, fun):
    return sorted(t, key=functools.cmp_to_key(fun))


# Return the key string to sort on
def lt(x):
    def fun(a, b):
        try:
            # return a[x] < b[x]
            if a[x] < b[x]:
                return -1
            elif a[x] > b[x]:
                return 1
            else:
                return 0
        except TypeError:
            # For debug purpose
            print(a[x])
            print(b[x])

    return fun


def push(t, x):
    t.append(x)


def fKeys(t):
    x = t.keys().sort()
    return x


# Randomly return one item
def any(t):
    i = rint(len(t) - 1, 0)
    return t[i]


# Randomly return some items
def many(t, n):
    u = []
    for i in range(n):
        u.append(any(t))
    return u


# Strings

def fmt(sControl, *arg):
    return sControl.format(*arg)


def o(t):
    cnt = 0
    ret = "{"
    if type(t) == dict:
        xs = sorted(t.items(), key=lambda item: item[0])

        for k, v in xs:
            ret += ":"
            ret += k
            ret += " "

            if type(v) == bool:
                v = str(v)
            else:
                v = str(v)
            ret += v
            cnt += 1

            if cnt < len(xs):
                ret += " "
    elif type(t) == list:
        xs = t

        for v in xs:
            # ret += ":"
            # ret += k
            # ret += " "

            if type(v) == bool:
                v = "false"
            else:
                v = str(v)
            ret += v
            cnt += 1

            if cnt < len(xs):
                ret += " "
    else:
        return str(t)
    ret += "}"

    return ret


def oo(t):
    print(o(t))
    return t


def coerce(s):
    def fun(val):
        if val == "true":
            return True
        elif val == "false":
            return False
        else:
            return val

    try:
        if type(s) == float:
            return s
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return fun(s)


def fcsv(filename, *func):
    global cnt
    with open(filename) as f:
        reader = csv.reader(f)
        for line in reader:
            converted = []
            for item in line:
                converted.append(coerce(item))
            cnt += len(converted)
            if (len(func) > 0):
                func[0](converted)


def convert_to_json_key(match_obj):
    result_key = ""
    if match_obj.group() is not None:
        result_key = match_obj.group()
        result_key = result_key.replace(" ", "")
        result_key = result_key.replace("=", "")
        result_key = "\"" + result_key + "\":"
    return result_key

def RULE(ranges, maxSize):
    t = {}
    for range_inner in ranges:
        txt = range_inner.txt
        t[txt] = t.get(txt, [])
        t[txt].append({'lo': range_inner.lo, 'hi': range_inner.hi, 'at': range_inner.at})
    return prune(t, maxSize)

def prune(rule, maxSize):
    n = 0
    new_rule = {}
    for txt, ranges in rule.items():
        n += 1
        if len(ranges) == maxSize[txt]:
            n += 1
            # del rule[txt]
        else:
            new_rule[txt] = ranges
    if n > 0:
        return new_rule


def xpln(data, best, rest):
    def v(has):
        return value(has, len(best.rows), len(rest.rows), "best")
    
    def score(ranges):
        rule_inner = RULE(ranges, maxSizes)
        if rule_inner:
            oo(showRule(rule_inner))
            bestr = selects(rule_inner, best.rows)
            restr = selects(rule_inner, rest.rows)
            if len(bestr) + len(restr) > 0:
                return v({"best": len(bestr), "rest": len(restr)}), rule_inner
            
    tmp, maxSizes = [], {}
    range_result = bins(data.cols.x, {"best": best.rows, "rest": rest.rows})
    for ranges in range_result:
        maxSizes[ranges[0].txt] = len(ranges)
        print("")
        for _, range in enumerate(ranges):
            print(range.txt, range.lo, range.hi)
            tmp.append({"range": range, "max": len(ranges), "val": v(range.y.has_list)})
            
    rule, most = firstN(sorted(tmp, key=lambda k: k["val"], reverse=True), score)
    return rule, most


def firstN(sortedRanges, scoreFun):
    print("")
    # map(lambda r: print(r["range"].txt, r["range"].lo, r["range"].hi, rnd(r["val"]), o(r["range"].y.has)), sortedRanges)
    fMap(sortedRanges, lambda r: print(r["range"].txt, r["range"].lo, r["range"].hi, rnd(r["val"]), o(r["range"].y.has_list)))

    first = sortedRanges[0]["val"]
    
    def useful(range_inner):
        if range_inner["val"] > 0.05 and range_inner["val"] > first / 10:
            return range_inner
        
    # sortedRanges = list(filter(None, map(useful, sortedRanges))) # reject useless ranges
    sortedRanges = list(filter(None, fMap(sortedRanges, useful))) # reject useless ranges
    most, out = -1, None
    
    for n in range(1, len(sortedRanges) + 1):
        # tmp, rule = scoreFun(list(map(lambda r: r["range"], sortedRanges[:n])))
        tmp, rule = scoreFun(list(fMap(sortedRanges[:n], lambda r: r["range"])))
        if tmp and tmp > most:
            out, most = rule, tmp
            
    return out, most

def showRule(rule):
    def pretty(range):
        return range["lo"] if range["lo"] == range["hi"] else [range["lo"], range["hi"]]
    
    def merges(attr, ranges):
        # return list(map(pretty, mergeInner(sorted(ranges, key=lambda k: k["lo"])))), attr
        return list(fMap(mergeInner(sorted(ranges, key=lambda k: k["lo"])), pretty)), attr

    def mergeInner(t0):
        t, j = [], 0
        
        while j < len(t0):
            left, right = t0[j], t0[j + 1] if j + 1 < len(t0) else None
            
            if right and left["hi"] == right["lo"]:
                left["hi"] = right["hi"]
                j += 1
                
            t.append({"lo": left["lo"], "hi": left["hi"]})
            j += 1
            
        return t if len(t0) == len(t) else merge(t)
    
    return fKap(rule, merges)

def selects(rule, rows):
    def disjunction(ranges, row):
        for range in ranges:
            lo, hi, at = range["lo"], range["hi"], range["at"]
            x = row[at]
            
            if x == "?":
                return True
            elif lo == hi == x:
                return True
            elif lo <= x < hi:
                return True
            
        return False
    
    def conjunction(row):
        for _, ranges in rule.items():
            if not disjunction(ranges, row):
                return False
            
        return True
    
    return list(filter(None, fMap(rows, lambda r: r if conjunction(r) else None)))


def doFile(filename):
    result_str = '{'
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        start_flag = False
        key_pattern = re.compile(r" *.*=")
        for row in spamreader:
            if start_flag:
                curr_row = ', '.join(row)
                new_row = re.sub(key_pattern, convert_to_json_key, curr_row)
                result_str += new_row
            else:
                for col in row:
                    if "return" in col:
                        start_flag = True
                        break
        old = '{'
        new = '['
        result_str = new.join(result_str.rsplit(old))
        result_str = old.join(result_str.split(new, 1))
        old = '}'
        new = ']'
        result_str = new.join(result_str.rsplit(old))
        result_str = old.join(result_str.rsplit(new, 1))
        result_str = "\" \"".join(result_str.rsplit("_"))
        result_str = "\"".join(result_str.rsplit("\'"))

        # print(result_str)
        data = json.loads(result_str)
        return data


def transpose(t):
    u = []
    for i in range(len(t[0])):
        u.append([])
        for j in range(len(t)):
            u[i].append(t[j][i])

    return u


# def repCols(cols):
#     cols = fCopy(cols)
#     for col in cols:
#         col[-1] = col[0] + ":" + col[-1]
#         for j in range(1, len(col)):
#             col[j - 1] = col[j]
#         del col[-1]
#
#     def fun(k):
#         return "Num" + str(k)
#
#     cols.insert(0, fKap(cols[0], fun))
#     cols[0][len(cols[0]) - 1] = "thingX"
#
#     return DATA(cols)  # ?
#
#
# def repRows(t, rows):
#     rows = fCopy(rows)
#     for j, s in enumerate(rows[-1]):
#         rows[0][j] = str(rows[0][j]) + ":" + str(s)
#     # rows.remove(rows[-1])
#     del rows[-1]
#     for n, row in enumerate(rows):
#         if n == 0:
#             row.append("thingX")
#         else:
#             u = t["rows"][len(t["rows"]) - n]
#             row.append(u[-1])
#
#     return DATA(rows)  # ?: 写法可能不对
#
#
# def repPlace(data):
#     n, g = 20, []
#     for i in range(n + 1):
#         g.append([])
#         for j in range(n + 1):
#             g[i].append(" ")
#
#     maxy = 0
#     print("")
#
#     for r, row in enumerate(data.rows):
#         c = chr(65 + r)
#         print(c, row.cells[-1])
#         x, y = int(row.x * n // 1), int(row.y * n // 1)
#         maxy = max(maxy, y + 1)
#         g[y][x] = c
#     print("")
#
#     for y in range(maxy):
#         oo(g[y])
#
#
# def repGrid(sFile):
#     t = doFile(sFile)
#     rows = repRows(t, transpose(t["cols"]))
#     cols = repCols(t["cols"])
#     show(rows.cluster())
#     show(cols.cluster())
#     repPlace(rows)


def fCopy(t):
    u = copy.deepcopy(t)
    return u

def bins(cols, rowss):
    out = []
    def rangeCmp(a, b):
        if a.lo < b.lo:
            return -1
        elif a.lo > b.lo:
            return 1
        else:
            return 0
    for _, col in enumerate(cols):
        ranges = {}
        for y, rows in rowss.items():
            for row in rows:
                x = row[col.at]
                if x != "?":
                    k = bin(col, x)
                    if k not in ranges:
                        ranges[k] = RANGE(col.at, col.txt, x, None)
                    ranges[k].extend(x, y)
        ranges_list = []
        for k, v in ranges.items():
            ranges_list.append(v)
        ranges_list = fSort(ranges_list, rangeCmp)
        # sorted(map(ranges, itself), key=lambda r: r["lo"])
        if type(col) == SYM:
            out.append(ranges_list)
        else:
            out.append(mergeAny(ranges_list))
    return out

def bin(col, x):
    if x == "?" or type(col) == SYM:
        return x
    tmp = (col.hi - col.lo)/(Is["bins"] - 1)
    if col.hi == col.lo:
        return 1
    else:
        return math.floor(x/tmp + .5)*tmp

def mergeAny(ranges0):
    def noGaps(t):
        for j in range(1, len(t)):
            t[j].lo = t[j - 1].hi
        t[0].lo = -math.inf
        t[len(t) - 1].hi = math.inf
        return t
    ranges1, j = [], 0
    left, right, y = None, None, None
    while j < len(ranges0):
        left, right = ranges0[j], None
        if j + 1 < len(ranges0):
            right = ranges0[j + 1]
        if right:
            y = merge2(left.y, right.y)
            if y is not None:
                j += 1
                left.hi, left.y = right.hi, y
        ranges1.append(left)
        j += 1
    return noGaps(ranges0) if len(ranges0) == len(ranges1) else mergeAny(ranges1)

def merge2(col1, col2):
    new = merge(col1, col2)
    if new.div() <= (col1.div() * col1.n + col2.div() * col2.n)/new.n:
        return new

def merge(col1, col2):
    new = copy(col1)
    if type(col1) == SYM:
        for x, n in col2.has_list.items():
            new.add(x, n)
    else:
        for n in col2.has_list:
            new.add(n)
        new.lo = min(col1.lo, col2.lo)
        new.hi = max(col1.hi, col2.hi)
    return new

def itself(x, y=None):
    return x

def cliffsDelta(ns1, ns2):
    if len(ns1) > 256:
        ns1 = many(ns1, 256)
    if len(ns2) > 256:
        ns2 = many(ns2, 256)
    if len(ns1) > 10 * len(ns2):
        ns1 = many(ns1, 10 * len(ns2))
    if len(ns2) > 10 * len(ns1):
        ns2 = many(ns1, 10 * len(ns1))
    
    n, gt, lt = 0, 0, 0
    for x in ns1:
        for y in ns2:
            n = n + 1
            if x > y:
                gt = gt + 1
            if x < y:
                lt = lt + 1
    return abs(lt - gt)/n > Is["cliffs"]

def diffs(nums1, nums2):
    def fun(k, nums):
        return cliffsDelta(nums.has_list, nums2[k].has_list), nums.txt
    return fKap(nums1, fun)
    
def cells(s, t):
    t = []
    for s1 in s.split(','):
        t.append(coerce(s1))
    return t

def lines(sFilename, fun):
    src = open(sFilename)
    while True:
        s = src.readline()
        if s:
            fun(s)
        else:
            src.close()
            return


def per(t, p=0.5):
    p = math.floor((p * len(t)) + 0.5)
    return t[max(0, min(len(t), p) - 1)]

def copy(t):
    if not isinstance(t, dict) and not isinstance(t, list):
        return t
    u = copy.deepcopy(t)

def slice(t, go=1, stop=None, inc=1):
    if go is not None and go < 0:
        go = len(t) + go
    if stop is not None and stop < 0:
        stop = len(t) + stop
    u = []
    for j in range(go, stop or len(t), inc):
        u.append(t[j])
    return u


def listToDict(li):
    if type(li) == list:
        res = {}
        for i in range(len(li)):
            res[i] = li[i]
        return res
    else:
        return li

def say(*args):
    sys.stderr.write("".join(map(str, args)))

def sayln(*args):
    sys.stderr.write("".join(map(str, args)) + "\n")

# Should these be here?
def norm(num, n):   # ?: 哪来的x
    # if x == "?":
    #     return x
    # else:
    return (n - num.lo)/(num.hi - num.lo + 1/float("inf"))


def value(has, nB, nR, sGoal):
    sGoal, nB, nR = sGoal or True, nB or 1, nR or 1
    b, r = 0, 0
    for x, n in has.items():
        if x == sGoal:
            b = b + n
        else:
            r = r + n
    b, r = b / (nB + 1 / math.inf), r / (nR + 1 / math.inf)
    return b ** 2 / (b + r)


def showTree(tree, lvl = None):
    if tree is not None:
        if lvl is None:
            lvl = 0
        # print("[{0}]".format(len(tree["data"].rows)) + "|.." * lvl, end="")
        if lvl == 0 or "left" not in tree or tree["left"] is None:
            print("|.." * lvl + "[{0}]".format(len(tree["data"].rows)), end="")
            print(o(tree["data"].stats()))
        else:
            print("|.." * lvl + "[{0}]".format(len(tree["data"].rows)))
        if "left" in tree:
            showTree(tree["left"], lvl + 1)
        if "right" in tree:
            showTree(tree["right"], lvl + 1)

def rogues(b4):
    for k, v in globals().items():
        if k not in b4:
            print(f"#W ?{k} {type(v)}")