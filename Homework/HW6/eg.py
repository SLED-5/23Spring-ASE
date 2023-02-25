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
    # lua code is : egs[1+#egs] = {key=key,fun=fun}
    egs[key] = fun
    # egs.append({'key': key, 'fun': fun})


def no(_, __, ___):
    return True


def packedOO():
    return utils.oo(config.the)


def randEgFunc():
    # the rand's logics is not sure
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
    config.the["Max"] = 32
    num1 = NUM.NUM(None, None)
    for i in range(1, 10001):
        num1.add(i)
    return utils.oo(num1.has())


def numsEgFunc():
    num1 = NUM.NUM(None, None)
    num2 = NUM.NUM(None, None)
    # the rand function here needs at one para, but lua code is unclear
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

    # not sure where's the t come from
    def fun(t):
        nonlocal n
        n += len(t)

    utils.fcsv(config.the["file"], fun)
    return 3192 == n


# under here is all about DATA, needs to double-check after DATA done
def dataEgFunc():
    data = DATA.read(DATA(), config.the["file"])
    col = data.cols.x[0]
    print(col.lo, col.hi, col.mid(), col.div())
    utils.oo(data.stats())
    return True


def cloneEgFunc():
    data1 = DATA.read(DATA(), config.the["file"])
    data2 = DATA.clone(data1, data1.rows)
    utils.oo(data1.stats())
    utils.oo(data2.stats())
    return True


def cliffsEgFunc():
    assert utils.cliffsDelta([8, 7, 6, 2, 5, 8, 7, 3], [8, 7, 6, 2, 5, 8, 7, 3]) is False
    assert utils.cliffsDelta([8, 7, 6, 2, 5, 8, 7, 3], [9, 9, 7, 8, 10, 9, 6]) is True
    t1, t2 = [], []
    for i in range(1000):
        # same issue, here the rand should have at least one para
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
    data = DATA.read(DATA(), config.the["file"])
    num = NUM.NUM(None, None)
    for _, row in enumerate(data.rows):
        # attention: here maybe num.add(data.dist(row, data.rows[0]))
        num.add(data.dist(row, data.rows[0]))
    utils.oo({'lo': num.lo, 'hi': num.hi, 'mid': utils.rnd(num.mid()), 'div': utils.rnd(num.div())})
    return True

def halfEgFunc():
    data = DATA.read(DATA(), config.the["file"])
    left, right, A, B, c = data.half()
    print(len(left), len(right))
    l, r = DATA.clone(data, left), DATA.clone(data, right)
    print("l", utils.o(l.stats()))
    print("r", utils.o(r.stats()))
    return True


def treeEgFunc():
    data = DATA.read(DATA(), config.the["file"])
    utils.showTree(data.tree())
    return True


def swayEgFunc():
    data = DATA.read(DATA(), config.the["file"])
    best, rest = data.sway()
    # here not sure where the div come form
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
    data = DATA.read(DATA(), config.the["file"])
    best, rest = data.sway()
    print("all", "", "", "", utils.o({'best': len(best.rows), 'rest': len(rest.rows)}))
    # here is not sure
    for k, t in enumerate(utils.bins(data.cols.x, ({'best': best.rows, 'rest': rest.rows}))):
        for _, it_range in enumerate(t):
            # if it_range.txt != b4:
            #     print("")
            b4 = it_range.txt
            print(it_range.txt, it_range.lo, it_range.hi,
                  utils.rnd(utils.value(it_range.y.has(), len(best.rows), len(rest.rows), "best")),
                  utils.o(it_range.y.has()))
    return True


def runTest():
    go('the', "show options", packedOO)
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
