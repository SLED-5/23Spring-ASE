import utils, Lists, Strings, classes

def eg(key, str, fun):
	global help
	global egs
	egs[key] = fun
	help = help + utils.fmt("  -g  {}\t{}\n",key,str)

def packedOO():
	return utils.oo(the)

def symEgFunc():
	sym = classes.SYM()
	pairs = ["a","a","a","a","b","b","c"]
	for x in pairs:
		sym.add(x)
	return sym.mid() == "a" and utils.rnd(sym.div()) == 1.379

def numEgFunc():
	num = classes.NUM()
	pairs = [1,1,1,1,2,2,3]
	for x in pairs:
		num.add(x)
	return num.mid() == 11/7 and utils.rnd(num.div()) == 0.787

def crfc():
	return Strings.cnt == 8 * 399

def drdc():
	data = classes.DATA(the.file)
	return len(data.rows) == 398 and data.cols.y[1].w == -1 and data.cols.x[1].at == 1 and len(data.cols.x) == 4

def ssfd():
	data = classes.DATA(the.file)
	for k, cols in zip(data.cols.y, data.cols.x):
		print(k, "mid", utils.o(data.stats("mid", cols, 2)))
		print("", "div", utils.o(data.stats("div", cols, 2)))

eg ('the', "show settings", packedOO)
eg("csv","read from csv", crfc)
eg("data","read DATA csv", drdc)
eg ('sym', "check syms", symEgFunc)
eg('num', "check nums", numEgFunc)