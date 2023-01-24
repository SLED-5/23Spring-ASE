import utils
from NUM import *
from SYM import *
from ROW import *
from COLS import *
from DATA import *

egs = {}

the = {}
help = '''[[   
data.lua : an example csv reader script
(c)2022, Tim Menzies <timm@ieee.org>, BSD-2 

USAGE:   data.lua  [OPTIONS] [-g ACTION]

OPTIONS:
	-d  --dump  on crash, dump stack = false
	-f  --file  name of file         = ../../etc/data/auto93.csv
	-g  --go    start-up action      = data
	-h  --help  show help            = false
	-s  --seed  random number seed   = 937162211

ACTIONS:
]]'''

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
	pairs = [1,1,1,1,2,2,3]
	for x in pairs:
		num.add(x)
	return num.mid() == 11/7 and utils.rnd(num.div()) == 0.787

def crfc():
	return utils.cnt == 8 * 399

def drdc():
	data = DATA(the["file"])
	return len(data.rows) == 398 and data.cols.y[0].w == -1 and data.cols.x[0].at == 1 and len(data.cols.x) == 4

def ssfd():
	data = DATA(the["file"])
	for k, cols in zip(data.cols.y, data.cols.x):
		print(k, "mid", utils.o(data.stats("mid", cols, 2)))
		print("", "div", utils.o(data.stats("div", cols, 2)))

def runTest():
	eg ('the', "show settings", packedOO)
	eg('csv',"read from csv", crfc)
	eg('data',"read DATA csv", drdc)
	eg ('sym', "check syms", symEgFunc)
	eg('num', "check nums", numEgFunc)
	