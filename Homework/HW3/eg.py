import utils
import config
from SYM import *
from NUM import *
from DATA import *

# import DATA

egs = {}
eg_help = ""

def eg(key, str, fun):
	global eg_help
	global egs
	egs[key] = fun
	eg_help = eg_help + utils.fmt("  -g  {}\t{}\n",key,str)

def packedOO():
	return utils.oo(config.the)

def symEgFunc():
	sym = SYM(None, None)
	pairs = ["a","a","a","a","b","b","c"]
	for x in pairs:
		sym.add(x)
	return sym.mid() == "a" and utils.rnd(sym.div()) == 1.379

def numEgFunc():
	num = NUM(None, None)
	pairs = [1, 1, 1, 1, 2, 2, 3]
	for x in pairs:
		num.add(x)
	return num.mid() == 11 / 7 and utils.rnd(num.div()) == 0.787

def dataEgFunc():
	data = DATA(config.the["file"])
	return len(data.rows) == 398 and data.cols.y[0].w == -1 and data.cols.x[0].at == 0 and len(data.cols.x) == 4

def cloneEgFunc():
	data1 = DATA(config.the["file"])
	data2 = data1.clone(data1.rows)
	return len(data1.rows) == len(data2.rows) \
		and data1.cols.y[0].w == data2.cols.y[0].w \
		and data1.cols.x[0].at == data2.cols.x[0].at \
		and len(data1.cols.x) == len(data2.cols.x)

def aroundEgFunc():
	data = DATA(config.the["file"])
	print(0, 0, utils.o(data.rows[0].cells))
	tmp_data = data.around(data.rows[0])
	for n,t in enumerate(tmp_data):
		if (n + 1) % 50 == 0:
			print(n, utils.rnd(t["dist"], 2), utils.o(t["row"].cells))
	return True

def halfEgFunc():
	data = DATA(config.the["file"])
	left, right, A, B, mid, c = data.half()
	print(len(left), len(right), len(data.rows))
	print(utils.o(A.cells), c)
	print(utils.o(mid.cells))
	print(utils.o(B.cells))
	return True


def clusterEgFunc():
	data = DATA(config.the["file"])
	# utils.show(data.clustet(), "mid", data.clos.y, 0)
	utils.show(data.cluster(), "mid", data.cols.y, 1)
	return True


def optimizeEgFunc():
	data = DATA(config.the["file"])
	# utils.show(data.sway(), "mid", data.clos.y, 0)
	utils.show(data.sway(), "mid", data.cols.y, 1)
	return True


def runTest():
	eg('the', "show settings", packedOO)
	eg('sym', "check syms", symEgFunc)
	eg('num', "check nums", numEgFunc)
	eg('data', "read DATA csv", dataEgFunc)
	eg('clone', "duplicate structure", cloneEgFunc)
	eg('around', "sorting nearest neighbors", aroundEgFunc)
	eg('half', "1-level bi-clustering", halfEgFunc)
	eg('cluster', "N-level bi-clustering", clusterEgFunc)
	eg('optimize', "semi-supervised optimization", optimizeEgFunc)


