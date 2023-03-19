import random

eg = {}

def ok(n=None):
    random.seed(n or 1)
eg["ok"] = ok

def sample():
    for i in range(10):
        print("", "".join(random.choices(["a", "b", "c", "d", "e"], k=10)))
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

def five():
    for rx in tiles(scottKnot([
        RX([0.34, 0.49, 0.51, 0.6, .34, .49, .51, .6], "rx1"),
        RX([0.6, 0.7, 0.8, 0.9, .6, .7, .8, .9], "rx2"),
        RX([0.15, 0.25, 0.4, 0.35, 0.15, 0.25, 0.4, 0.35], "rx3"),
        RX([0.6, 0.7, 0.8, 0.9, 0.6, 0.7, 0.8, 0.9], "rx4"),
        RX([0.1, 0.2, 0.3, 0.4, 0.1, 0.2, 0.3, 0.4], "rx5")
    ])):
        print(rx['name'], rx['rank'], rx['show'])


def six():
    for rx in tiles(scottKnot([
        RX([101, 100, 99, 101, 99.5, 101, 100, 99, 101, 99.5], "rx1"),
        RX([101, 100, 99, 101, 100, 101, 100, 99, 101, 100], "rx2"),
        RX([101, 100, 99.5, 101, 99, 101, 100, 99.5, 101, 99], "rx3"),
        RX([101, 100, 99, 101, 100, 101, 100, 99, 101, 100], "rx4")
    ])):
        print(rx['name'], rx['rank'], rx['show'])


def tiles():
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

def tiles():
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
    for rx in tiles(scottKnot(rxs)):
        print("", rx["rank"], rx["name"], rx["show"])

for k, fun in enumerate(eg):
    eg["ok"]
    print("\n".join(str(k)))
    fun()
