def RX(t, s=None):
    t = sorted(t)
    return {"name": s or "", "rank": 0, "n": len(t), "show": "", "has": t}

def mid(t):
    t = t["has"] if "has" in t else t
    n = len(t) // 2
    return (t[n] + t[n + 1]) / 2 if len(t) % 2 == 0 else t[n + 1]

def div(t):
    t = t["has"] if "has" in t else t
    return (t[len(t) * 9 // 10] - t[len(t) * 1 // 10]) / 2.56

def merge(rx1, rx2):
    rx3 = RX([], rx1["name"])
    for t in [rx1["has"], rx2["has"]]:
        for x in t:
            rx3["has"].append(x)
    rx3["has"].sort()
    rx3["n"] = len(rx3["has"])
    return rx3

def scottKnot(rxs, all, cohen):
    def merges(i, j):
        out = RX({}, rxs[i].name)
        for k in range(i, j + 1):
            out = merge(out, rxs[j])
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
    cohen = div(merges(1, len(rxs))) * the.cohen
    recurse(0, len(rxs) - 1, 1)
    return rxs

def tiles(rxs):
    lo, hi = math.inf, -math.inf
    for rx in rxs:
        lo = min(lo, rx['has'][1])
        hi = max(hi, rx['has'][-1])
    for rx in rxs:
        t, u = rx['has'], [" "] * the.width
        def of(x, most): return max(1, min(most, math.floor(x)))
        def at(x): return t[of(len(t)*x//1, len(t)-1)]
        def pos(x): return math.floor(of(the.width*(x-lo)/(hi-lo+1E-32)//1, the.width))
        a, b, c, d, e = at(.1), at(.3), at(.5), at(.7), at(.9)
        A, B, C, D, E = pos(a), pos(b), pos(c), pos(d), pos(e)
        u[A:B+1] = ["-"]*(B-A+1)
        u[D:E+1] = ["-"]*(E-D+1)
        u[the.width//2] = "|"
        u[C] = "*"
        rx['show'] = "".join(u) + " {" + the.Fmt.format(a)
        for x in [b, c, d, e]:
            rx['show'] += ", " + the.Fmt.format(x)
        rx['show'] += "}"
    return rxs
