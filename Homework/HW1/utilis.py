import math
import random


# Numerics
Seed = 937162211

def rint(lo, hi):
    return math.floor(0.5 + random.random(lo, hi))

def rand(lo, hi):
    global Seed
    lo, hi = lo or 0, hi or 1
    Seed = (16807 * Seed) % 2147483647
    return lo + (hi - lo) * Seed / 2147483647

def rnd(n, nPlaces):
    mult = 10**(nPlaces or 3)
    return math.floor(n*mult+0.5) / mult

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
### TODO: format

def o(t):
    xs = sorted(t.items(), key=lambda item:item[0])
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

        if cnt != len(xs)-1:
            ret += " "

    ret += "}"

    return ret

def oo(t):
    print(o(t))
    return t


