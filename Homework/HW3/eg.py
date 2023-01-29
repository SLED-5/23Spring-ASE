import utils

egs = {}
the = {}
help = '''[[   
cluster.lua : an example csv reader script
(c)2022, Tim Menzies <timm@ieee.org>, BSD-2 

USAGE: cluster.lua  [OPTIONS] [-g ACTION]

OPTIONS:
  -d  --dump    on crash, dump stack   = false
  -f  --file    name of file           = ../etc/data/auto93.csv
  -F  --Far     distance to "faraway"  = .95
  -g  --go      start-up action        = data
  -h  --help    show help              = false
  -m  --min     stop clusters at N^min = .5
  -p  --p       distance coefficient   = 2
  -s  --seed    random number seed     = 937162211
  -S  --Sample  sampling data size     = 512

ACTIONS:
]]
'''

def eg(key, str, fun):
	global help
	global egs
	egs[key] = fun
	help = help + utils.fmt("  -g  {}\t{}\n",key,str)

def packedOO():
	return utils.oo(the)

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
	data = DATA(the["file"])
	return len(data.rows) == 398 and data.cols.y[0].w == -1 and data.cols.x[0].at == 0 and len(data.cols.x) == 4

def cloneEgFunc():
	data1 = DATA(the["file"])
	data2 = data1.clone(data1.rows)
	return len(data1.rows) == len(data2.rows) \
		and data1.cols.y[0].w == data2.cols.y[0].w \
		and data1.cols.x[0].at == data2.cols.x[0].at \
		and len(data1.cols.x) == len(data2.cols.x)

def aroundEgFunc():
	data = DATA(the["file"])
	print(0, 0, utils.o(data.rows[0].cells))
	for n,t in data.around(data.rows[0]):
		if n % 50 == 0:
			print(n, utils.rnd(t.dist, 2), utils.o(t.row.cells))

def halfEgFunc():
	data = DATA(the["file"])
	left, right, A, B, mid, c = data.half()
	print(len(left), len(right), len(data.row))
	print(utils.o(A.cells), c)
	print(utils.o(mid.cells))
	print(utils.o(B.cells))

def clusterEgFunc():
	data = DATA(the["file"])
	# utils.show(data.clustet(), "mid", data.clos.y, 0)
	utils.show(data.clustet(), "mid", data.clos.y, 1)

def optimizeEgFunc():
	data = DATA(the["file"])
	# utils.show(data.sway(), "mid", data.clos.y, 0)
	utils.show(data.sway(), "mid", data.cols.y, 1)


def runTest():
	eg('the', "show settings", packedOO)
	eg('sym', "check syms", symEgFunc)
	eg('num', "check nums", numEgFunc)
	eg('data', "read DATA csv", dataEgFunc)
	eg('clone', "duplicate structure", cloneEgFunc)
	eg('around', "sorting nearest neighbors", aroundEgFunc)
	eg('half', "1-level bi-clustering", halfEgFunc)
	eg('cluster', "N-level bi-clustering", clusterEgFunc())
	eg('optimize', "semi-supervised optimization", optimizeEgFunc())


