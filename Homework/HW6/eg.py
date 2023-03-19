from SYM import SYM
from NUM import NUM
from DATA import *
import config
import utils

egs = {}
eg_help = ""


def go(key, xplain, fun):
    global eg_help
    global egs
    eg_help += utils.fmt("  -g  {}\t{}\n", key, xplain)
    egs[key] = fun


def no(_, __, ___):
    return True


def isEgFunc():
    return utils.oo(config.Is)


def randEgFunc():
    t = []
    for i in range(1000):
        utils.Seed = 1
        utils.push(t, utils.rint(100))
    u = []
    for i in range(1000):
        utils.Seed = 1
        utils.push(u, utils.rint(100))
    for k, v in enumerate(t):
        assert v == u[k]
    return True


def someEgfunc():
    config.Is["Max"] = 32
    num1 = NUM.NUM(None, None)
    for i in range(1, 10001):
        num1.add(i)
    return utils.oo(num1.has())


def numsEgFunc():
    num1 = NUM.NUM(None, None)
    num2 = NUM.NUM(None, None)
    for i in range(1, 10001):
        num1.add(utils.rand())
    for i in range(1, 10001):
        num2.add(utils.rand() ** 2)
    print(1, utils.rnd(num1.mid()), utils.rnd(num1.div()))
    print(1, utils.rnd(num2.mid()), utils.rnd(num2.div()))
    return 0.5 == utils.rnd(num1.mid()) and num1.mid() > num2.mid()


def symsEgFunc():
    sym = SYM.adds(SYM(None, None), ["a", "a", "a", "a", "b", "b", "c"])
    print(sym.mid(), utils.rnd(sym.div()))
    return 1.38 == utils.rnd(sym.div())


def csvEgFunc():
    n = 0
    def fun(t):
        nonlocal n
        n += len(t)

    utils.fcsv(config.Is["file"], fun)
    return 3192 == n


def dataEgFunc():
    data = DATA(config.Is["file"])  # note
    col = data.cols.x[0]
    print(col.lo, col.hi, col.mid(), col.div())
    utils.oo(data.stats())
    return True


def cloneEgFunc():
    data1 = DATA(config.Is["file"])
    data2 = DATA(data1, data1.rows)
    utils.oo(data1.stats())
    utils.oo(data2.stats())
    return True


def cliffsEgFunc():
    assert utils.cliffsDelta([8, 7, 6, 2, 5, 8, 7, 3], [8, 7, 6, 2, 5, 8, 7, 3]) is False
    assert utils.cliffsDelta([8, 7, 6, 2, 5, 8, 7, 3], [9, 9, 7, 8, 10, 9, 6]) is True
    t1, t2 = [], []
    for i in range(1000):
        utils.push(t1, utils.rand())
    for i in range(1000):
        utils.push(t2, utils.rand() ** 0.5)
    assert utils.cliffsDelta(t1, t1) is False
    assert utils.cliffsDelta(t1, t2) is True

    diff, j = False, 1.0

    def fun(x):
        return x * j

    while not diff:
        t3 = utils.fMap(t1, fun)
        diff = utils.cliffsDelta(t1, t3)
        print(">", utils.rnd(j), diff)
        j *= 1.025
    return True


def distEgFunc():
    data = DATA(config.Is["file"])
    num = NUM.NUM(None, None)
    for _, row in enumerate(data.rows):
        # attention: here maybe num.add(data.dist(row, data.rows[0]))
        num.add(data.dist(row, data.rows[0]))
    utils.oo({'lo': num.lo, 'hi': num.hi, 'mid': utils.rnd(num.mid()), 'div': utils.rnd(num.div())})
    return True

def halfEgFunc():
    data = DATA(config.Is["file"])
    left, right, A, B, c, other = data.half()
    print(len(left), len(right))
    l, r = DATA(data, left), DATA(data, right)
    print("l", utils.o(l.stats()))
    print("r", utils.o(r.stats()))
    return True


def treeEgFunc():
    data = DATA(config.Is["file"])
    utils.showTree(data.tree())
    return True


def swayEgFunc():
    data = DATA(config.Is["file"])
    best, rest, _ = data.sway()
    print("\nall ", utils.o(data.stats()))
    print("    ", utils.o(data.stats(data.div, None)))
    print("\nbest", utils.o(best.stats()))
    print("    ", utils.o(best.stats(best.div)))
    print("\nrest", utils.o(rest.stats()))
    print("    ", utils.o(rest.stats(rest.div)))

    data_col_y_dict = utils.listToDict(data.cols.y)
    best_col_y_dict = utils.listToDict(best.cols.y)
    rest_col_y_dict = utils.listToDict(rest.cols.y)

    print("\nall ~= best?", utils.o(utils.diffs(best_col_y_dict, data_col_y_dict)))
    print("best ~= rest?", utils.o(utils.diffs(best_col_y_dict, rest_col_y_dict)))
    return True


def binsEgFunc():
    data = DATA(config.Is["file"])
    best, rest, other = data.sway()
    print("all", "", "", "", utils.o({'best': len(best.rows), 'rest': len(rest.rows)}))
    for k, t in enumerate(utils.bins(data.cols.x, ({'best': best.rows, 'rest': rest.rows}))):
        for _, it_range in enumerate(t):
            # if it_range.txt != b4:
            #     print("")
            b4 = it_range.txt
            print(it_range.txt, it_range.lo, it_range.hi,
                  utils.rnd(utils.value(it_range.y.has(), len(best.rows), len(rest.rows), "best")),
                  utils.o(it_range.y.has()))
    return True


def xplnEgFun():
    data = DATA(config.Is["file"])
    best, rest, evals = data.sway()
    rule, most = data.xpln(best, rest)
    print("\n-----------\nexplain=", utils.o(utils.showRule(rule)))

    data1 = DATA(data, utils.selects(rule, data.rows))
    print("all               ", utils.o(data.stats()), utils.o(data.stats(data.div)))
    print(utils.fmt("sway with %5s evals", evals), utils.o(best.stats()), utils.o(best.stats(best.div)))
    print(utils.fmt("xpln on   %5s evals", evals), utils.o(data1.stats()), utils.o(data1.stats(data1.div)))

    top, _ = data.betters(len(best.rows))
    top = DATA(data, top)
    print(utils.fmt("sort with %5s evals", len(data.rows)), utils.o(top.stats()), utils.o(top.stats(top.div)))
    return True


def runTest():
    go('is', "show options", isEgFunc)
    go('rand', "demo random number generation", randEgFunc)
    go('some', "demo of reservoir sampling", someEgfunc)
    go('nums', "demo of NUM", numsEgFunc)
    go('syms', "demo SYMS", symsEgFunc)
    go('csv', "reading csv files", csvEgFunc)
    go('data', "showing data sets", dataEgFunc)
    go('clone', "replicate structure of a DATA", cloneEgFunc)
    go('cliffs', "stats tests", cliffsEgFunc)
    go('dist', "distance test", distEgFunc)
    go('half', "divide data in half", halfEgFunc)
    go('tree', "make snd show tree of clusters", treeEgFunc)
    go('sway', "optimizing", swayEgFunc)
    go('bins', "find deltas between best and rest", binsEgFunc)
    go('xpln', "explore explanation sets", xplnEgFun)
