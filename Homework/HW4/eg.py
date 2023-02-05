import utils
import config
from SYM import *
from NUM import *

egs = {}
eg_help = ""

def eg(key, str, fun):
	global eg_help
	global egs
	egs[key] = fun
	eg_help = eg_help + utils.fmt("  -g  {}\t{}\n",key,str)

def packedOO():
	return utils.oo(config.the)

def copyEgFunc():
	t1 = {'a': 1, 'b': {'c': 2, 'd': [3]}}
	t2 = utils.copy(t1)
	t2['b']['d'][0] = 10000
	print("b4", utils.o(t1), "\nafter", utils.o(t2))

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

def repEgFunc():
	utils.repgrid(config.the["file"])

def runTest():
	eg('the', "show settings", packedOO)
	eg('copy',"check copy", copyEgFunc())
	eg('sym', "check syms", symEgFunc)
	eg('num', "check nums", numEgFunc)
	eg('rep', "checking repgrid", repEgFunc())