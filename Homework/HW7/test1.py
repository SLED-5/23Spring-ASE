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
        u[i] = (random.choice(t))
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
        if NUM.NUM(samples(yhat)).delta(NUM.NUM(samples(zhat))) > tobs:
            n += 1
    return n / the['bootstrap'] >= the['conf']

