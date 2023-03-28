import math
import random
from NUM import *

the = {'bootstrap': 512, 'conf': 0.05, 'cliff': 0.4, 'cohen': 0.35,
       'Fmt': '%6.2f', 'width': 40}


def erf(x):
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911
    # Save the sign of x
    sign = 1
    if x < 0:
        sign = -1
    x = abs(x)
    # A&S formula 7.1.26
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
    return sign * y


def gaussian(mu=0, sd=1):
    # return a sample from a Gaussian with mean `mu` and sd `sd`
    return mu + sd * math.sqrt(-2 * math.log(random.random())) * math.cos(2 * math.pi * random.random())


def samples(t, n=None):
    u = []
    for i in range(n or len(t)):
        u.append(random.choice(t))
    return u


def cliffsDelta(ns1, ns2):
    # true if different by a trivial amount
    n, gt, lt = 0, 0, 0
    if len(ns1) > 128:
        ns1 = samples(ns1, 128)
    if len(ns2) > 128:
        ns2 = samples(ns2, 128)
    for x in ns1:
        for y in ns2:
            n += 1
            if x > y:
                gt += 1
            if x < y:
                lt += 1
    return abs(lt - gt) / n <= the['cliff']


def bootstrap(y0, z0):
    n, x, y, z, xmu, ymu, zmu, yhat, zhat, tobs = 0, NUM(), NUM(), NUM(), 0, 0, 0, [], [], 0
    for y1 in y0:
        x.add(y1)
        y.add(y1)
    for z1 in z0:
        x.add(z1)
        z.add(z1)
    xmu, ymu, zmu = x.mu, y.mu, z.mu
    for y1 in y0:
        yhat.append(y1 - ymu + xmu)
    for z1 in z0:
        zhat.append(z1 - zmu + xmu)
    tobs = y.delta(z)
    for _ in range(the['bootstrap']):
        # Note here
        if NUM(samples(yhat)).delta(NUM(samples(zhat))) > tobs:
            n += 1
    return n / the['bootstrap'] >= the['conf']

def RX(t, s=None):
    t = sorted(t)
    return {"name": s or "", "rank": 0, "n": len(t), "show": "", "has": t}

def mid(t, n=None):
    t = t.get('has', t)
    print(t)
    n = len(t) // 2
    print("len" + str(len(t)))
    if len(t) > 0:
        return (t[n - 1] + t[n]) / 2 if len(t) % 2 == 0 else t[n]

def div(t):
    t = t.get('has', t)
    return (t[len(t) * 9 // 10] - t[len(t) * 1 // 10]) / 2.56

def merge(rx1, rx2):
    rx3 = RX([], rx1["name"])
    for t in [rx1["has"], rx2["has"]]:
        for x in t:
            rx3["has"].append(x)
    rx3["has"].sort()
    rx3["n"] = len(rx3["has"])
    return rx3

def scottKnot(rxs):
    def merges(i, j):
        out = RX({}, rxs[i]['name'])
        for k in range(i, j+1):
            print("rxs" + str(len(rxs)))
            print(j)
            out = merge(out, rxs[j - 1])
        return out

    def same(lo, cut, hi):
        l = merges(lo, cut)
        r = merges(cut + 1, hi)
        return cliffsDelta(l['has'], r['has']) and bootstrap(l['has'], r['has'])

    def recurse(lo, hi, rank):
        b4 = merges(lo, hi)
        best = 0
        for j in range(lo, hi + 1):
            if j < hi:
                l = merges(lo, j)
                r = merges(j + 1, hi)
                now = (l['n'] * (mid(l) - mid(b4)) ** 2 + r['n'] * (mid(r) - mid(b4)) ** 2) / (l['n'] + r['n'])
                if now > best:
                    if abs(mid(l) - mid(r)) >= cohen:
                        cut, best = j, now
        if 'cut' in locals() and not same(lo, cut, hi):
            rank = recurse(lo, cut, rank) + 1
            rank = recurse(cut + 1, hi, rank)
        else:
            for i in range(lo, hi + 1):
                rxs[i]['rank'] = rank
        return rank

    rxs.sort(key=lambda x: mid(x))
    cohen = div(merges(1, len(rxs))) * the['cohen']
    recurse(1, len(rxs) - 1, 1)
    return rxs

def tiles(rxs):
    lo, hi = math.inf, -math.inf
    for rx in rxs:
        lo = min(lo, rx['has'][1])
        hi = max(hi, rx['has'][-1])
    for rx in rxs:
        t, u = rx['has'], [" "] * the['width']
        def of(x, most): return max(1, min(most, math.floor(x)))
        def at(x): return t[of(len(t)*x//1, len(t)-1)]
        def pos(x): return math.floor(of(the['width']*(x-lo)/(hi-lo+1E-32)//1, the['width']))
        a, b, c, d, e = at(.1), at(.3), at(.5), at(.7), at(.9)
        A, B, C, D, E = pos(a), pos(b), pos(c), pos(d), pos(e)
        u[A:B+1] = ["-"]*(B-A+1)
        u[D:E+1] = ["-"]*(E-D+1)
        u[the['width']//2] = "|"
        u[C] = "*"
        rx['show'] = ''.join(u) + str(the["Fmt"]).format(str(a))
        for x in [b, c, d, e]:
            rx['show'] += ", " + str(the["Fmt"]).format(str(x))
        rx['show'] += "}"
    return rxs

eg = {}

def ok(n=None):
    random.seed(n or 1)
eg["ok"] = ok

def sample():
    for i in range(10):
        print("", "".join(samples(["a", "b", "c", "d", "e"])))
eg["sample"] = sample

def num():
    n = NUM([1,2,3,4,5,6,7,8,9,10])
    print("", n.n, n.mu, n.sd)
eg["num"] = num

def gauss():
    t, n = [], None
    for i in range(10**4):
        t.append(gaussian(10, 2))
    n = NUM(t)
    print("", n.n, n.mu, n.sd)
eg["gauss"] = gauss

def bootmu():
    a, b, cl, bs = [], [], None, None
    for i in range(100):
        a.append(gaussian(10, 1))
    print("","mu","sd","cliffs","boot","both")
    print("","--","--","------","----","----")
    for mu in range(100, 110, 1):
        mu /= 10
        for i in range(100):
            b.append(gaussian(mu, 1))
        cl = cliffsDelta(a, b)
        bs = bootstrap(a, b)
        print("", mu, 1, cl, bs, cl and bs)
eg["bootmu"] = bootmu

def eg_basic():
    print("\t\ttruee", bootstrap([8, 7, 6, 2, 5, 8, 7, 3], [8, 7, 6, 2, 5, 8, 7, 3]), cliffsDelta([8, 7, 6, 2, 5, 8, 7, 3], [8, 7, 6, 2, 5, 8, 7, 3]))
    print("\t\tfalse", bootstrap([8, 7, 6, 2, 5, 8, 7, 3], [9, 9, 7, 8, 10, 9, 6]), cliffsDelta([8, 7, 6, 2, 5, 8, 7, 3], [9, 9, 7, 8, 10, 9, 6]))
    print("\t\tfalse", bootstrap([0.34, 0.49, 0.51, 0.6, 0.34, 0.49, 0.51, 0.6], [0.6, 0.7, 0.8, 0.9, 0.6, 0.7, 0.8, 0.9]), cliffsDelta([0.34, 0.49, 0.51, 0.6, 0.34, 0.49, 0.51, 0.6], [0.6, 0.7, 0.8, 0.9, 0.6, 0.7, 0.8, 0.9]))
eg["basic"] = eg_basic

def pre():
    print("\neg3")
    d = 1
    for i in range(1, 11):
        t1, t2 = [], []
        for j in range(1, 33):
            t1.append(gaussian(10, 1))
            t2.append(gaussian(d * 10, 1))
        print("\t", d, "true" if d < 1.1 else "false", bootstrap(t1, t2), bootstrap(t1, t1))
        d += 0.05
eg["pre"] = pre

def five():
    for rx in tiles(scottKnot([
        RX([0.34, 0.49, 0.51, 0.6, .34, .49, .51, .6], "rx1"),
        RX([0.6, 0.7, 0.8, 0.9, .6, .7, .8, .9], "rx2"),
        RX([0.15, 0.25, 0.4, 0.35, 0.15, 0.25, 0.4, 0.35], "rx3"),
        RX([0.6, 0.7, 0.8, 0.9, 0.6, 0.7, 0.8, 0.9], "rx4"),
        RX([0.1, 0.2, 0.3, 0.4, 0.1, 0.2, 0.3, 0.4], "rx5")
    ])):
        print(rx['name'], rx['rank'], rx['show'])
eg["five"] = five

def six():
    for rx in tiles(scottKnot([
        RX([101, 100, 99, 101, 99.5, 101, 100, 99, 101, 99.5], "rx1"),
        RX([101, 100, 99, 101, 100, 101, 100, 99, 101, 100], "rx2"),
        RX([101, 100, 99.5, 101, 99, 101, 100, 99.5, 101, 99], "rx3"),
        RX([101, 100, 99, 101, 100, 101, 100, 99, 101, 100], "rx4")
    ])):
        print(rx['name'], rx['rank'], rx['show'])
eg["six"] = six

def eg_tiles():
    rxs,a,b,c,d,e,f,g,h,j,k=[],[],[],[],[],[],[],[],[],[],[]
    for i in range(1000):
        a.append(gaussian(10,1))
    for i in range(1000):
        b.append(gaussian(10.1,1))
    for i in range(1000):
        c.append(gaussian(20,1))
    for i in range(1000):
        d.append(gaussian(30,1))
    for i in range(1000):
        e.append(gaussian(30.1,1))
    for i in range(1000):
        f.append(gaussian(10,1))
    for i in range(1000):
        g.append(gaussian(10,1))
    for i in range(1000):
        h.append(gaussian(40,1))
    for i in range(1000):
        j.append(gaussian(40,3))
    for i in range(1000):
        k.append(gaussian(10,1))

    for k, v in enumerate([a, b, c, d, e, f, g, h, j, k]):
        rxs.append(RX(v, "rx{}".join(str(k))))
    def func(a, b):
        return mid(a) < mid(b)
    rxs_sorted = sorted(rxs, key=func)
    for rx in tiles(rxs_sorted):
        print("", rx["name"], rx["show"])
eg['tiles'] = eg_tiles

for k, fun in eg.items():
    eg["ok"]()
    print("\n" + k)
    fun()
