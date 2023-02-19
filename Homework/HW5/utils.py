import RANGE
import copy
import functools
import math
import re
import csv
import json
import sys

from DATA import *

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


def rnd(n, nPlaces=3):
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
        for k, v in t.items():
            v, k = fun(k, v)
            u[k or (1 + len(u))] = v
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
    for _, col in enumerate(cols):
        ranges = {}
        for y, rows in enumerate(rowss):
            for _, row in enumerate(rows):
                x, k = row[col["at"]]
                if x != "?":
                    k = bin(col, x)
                    if k not in ranges:
                        ranges[k] = RANGE.RANGE(col["at"], col["txt"], x)
                        ranges[k].extend(x, y)
        ranges = sorted(map(ranges, itself), key=lambda r: r["lo"])
        out.append(col["isSym"] and ranges or mergeAny(ranges))
    return out

def bin(col, x):
    if x == "?" or col.isSym:
        return x
    tmp = (col.hi - col.lo)/(the.bins - 1)
    return col.hi == col.lo and 1 or math.floor(x/tmp + .5)*tmp

def mergeAny(ranges0):
    def noGaps(t):
        for j in range(1, len(t)):
            t[j].lo = t[j - 1].hi
            t[1].lo = -math.inf
            t[len(t)].hi = math.inf
            return t
    ranges1, j = [], 1
    left, right, y = None, None, None
    while j < len(ranges0):
        left, right = ranges0[j], ranges0[j + 1]
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
    if col1.isSym:
        for x, n in enumerate(col2.has):
            col1.add(new, x, n)
    else:
        for n in col2.has:
            col2.add(new, n)
        new.lo = min(col1.lo, col2.lo)
        new.hi = max(col1.hi, col2.hi)
    return new

def itself(x):
    return x

def cliffsDelta(ns1, ns2):
    if len(ns1 > 256):
        ns1 = many(ns1, 256)
    if len(ns2 > 256):
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
    return abs(lt - gt)/n > the.cliffs

def diffs(nums1, nums2):
    def fun(k, nums):
        return cliffsDelta(nums.has, nums2[k].has), nums.txt
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
    return t[max(0, min(len(t), p-1))]

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

def value():
    pass

def showTree():
    pass
