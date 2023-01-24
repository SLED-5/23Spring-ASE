import math
import re

# Numerics
Seed = 937162211


def rint(lo, hi):
    return math.floor(0.5 + rand(lo, hi))


def rand(lo, hi):
    # Seed need to be reseted before each generation
    global Seed
    lo, hi = lo or 0, hi or 1
    Seed = (16807 * Seed) % 2147483647
    return lo + (hi - lo) * Seed / 2147483647


def rnd(n, *nPlaces):
    if len(nPlaces) != 0:
        mult = 10 ** nPlaces[0]
    else:
        mult = 10 ** 3
    return math.floor(n * mult + 0.5) / mult


# Lists
def fMap(t, fun):
    u = {}
    for k, v in t.items():
        v, k = fun(v)
    u[k or (1 + len(u))] = v

    return u


def fKap(t, fun):
    u = {}
    for k, v in t.items():
        v, k = fun(k, v)
    u[k or (1 + len(u))] = v

    return u


def fSort(t, fun):
    t.sort(key=fun)
    return t


def fKeys(t):
    x = t.keys().sort()
    return x


# Strings

def fmt(sControl, *arg):
    return sControl.format(*arg)


def o(t):
    xs = sorted(t.items(), key=lambda item: item[0])
    cnt = 0
    ret = "{"

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
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return fun(s)


def csv(filename, func):
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            if line:
                pattern = re.compile("[^,]+")
                matches = re.finditer(pattern, line)
                cols_in_a_row = []
                for match in matches:
                    cols_in_a_row.append(coerce(match))
                func(cols_in_a_row)



