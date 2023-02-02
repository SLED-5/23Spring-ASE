import functools
import math
import re
from ROW import *
import csv

cnt = 0
# Numerics
Seed = 937162211

def show(node, what, cols, nPlaces, lvl=0):
    if node:
        lvl = lvl or 0
        # if node.left is None or lvl == 0:
        if not node.left or lvl == 0:
            print("| " * lvl + str(len(node.rows)) + "  ", end="")
            print(o(node.stats("mid", node.cols.y, nPlaces)))
        else:
            print("| " * lvl + str(len(node.rows)) + "  ")
        show(node.left, what, cols, nPlaces, lvl + 1)
        show(node.right, what, cols, nPlaces, lvl + 1)


def rint(lo, hi=None):
    return math.floor(0.5 + rand(lo, hi))


def rand(lo, hi):
    global Seed
    lo, hi = lo or 0, hi or 1
    Seed = (16807 * Seed) % 2147483647
    return lo + (hi - lo) * Seed / 2147483647


def rnd(n, nPlaces=3):
    mult = 10 ** nPlaces
    return math.floor(n * mult + 0.5) / mult

def cosine(a, b, c):
    x1 = (a**2 + c**2 - b**2) / (2 * c)
    x2 = max(0, min(1, x1))
    y = (a**2 - x2**2)**0.5
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
    # if type(t) == dict:
    # t.sort(key=fun)
    return sorted(t, key=functools.cmp_to_key(fun))
    # elif type(t) == list:
    #     t.sort(key=fun)
    # return t


# Return a function that sorts ascending on 'x'
def lt(x):
    def fun(a, b):
        # print("compare " + str(a[x]) + " and " + str(b[x]))
        if a[x] < b[x]:
            return -1
        elif a[x] > b[x]:
            return 1
        else:
            return 0

    return fun


def push(t, x):
    t.append(x)


def fKeys(t):
    x = t.keys().sort()
    return x

# Randomly return one item
def any(t):
    return t[rint(max(0, len(t) - 1))]

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
                v = "false"
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

