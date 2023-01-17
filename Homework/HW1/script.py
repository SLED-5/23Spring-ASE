import re
import sys
import math
from utils import *
from NUM import *
from SYM import *
import getopt

the = {}
help = "script.lua : an example script with help text and a test suite\n(c)2022, Tim Menzies <timm@ieee.org>, BSD-2 \n\nUSAGE:   script.lua  [OPTIONS] [-g ACTION]\n\nOPTIONS:\n  -d  --dump  on crash, dump stack = false\n  -g  --go    start-up action      = data\n  -h  --help  show help            = false\n  -s  --seed  random number seed   = 937162211\nACTIONS:\n"
egs = {}


#TODO: config.py
def settings(s):
	t = {}
	pattern = re.compile("\n[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)")
	matches = re.finditer(pattern, s)
	for match in matches:
		k = match.groups(0)[0]
		v = match.groups(0)[1]
		t[k] = coerce(v)
	return t

def cli(options):
	argumentList = sys.argv[1:]
	for k, v in options.items():
		if type(v) == bool:
			if v:
				v = "true"
			else:
				v = "false"
				
		for i in range(0, len(argumentList)):
			x = argumentList[i]
			if x == "-" + k[0] or x == "--" + k:
				if v == "false":
					v = "true"
				elif v == "true":
					v = "false"
				else:
					if (len(argumentList) > i + 1):
						v = argumentList[i + 1]
		options[k] = coerce(v)
	return options

# main

def main(options, help):
	global egs
	
	saved, fails = {}, 0
	b4 = {}
	for k, v in cli(settings(help)).items():
		options[k] = v
		saved[k] = v
	if options["help"]:
		print(help)
	else :
		for what in egs.items():
			if options['go'] == "all" or what[0] == options['go']:
				for k, v in saved.items():
					options[k] = v
				Seed = options["seed"]
				if not egs[what[0]]():
					fails = fails + 1
					print("❌ fail:" + what[0])
				else:
					print("✅ pass:" + what[0])

# Test suite
# TODO: test.py
def eg(key, str, fun):
	global help
	global egs
	egs[key] = fun
	help = help + fmt("  -g  {}\t{}\n",key,str)
	
##TODO: debug this
def randEgFunc():
	num1, num2 = NUM(), NUM()
	Seed = the["seed"]
	for i in range(1, 100):
		num1.add(rand(0,1))
		num2.add(rand(0,1))
	m1, m2 = rnd(num1.mid(), 10), rnd(num2.mid(), 10)
	return m1 == m2 and rnd(m1, 1) == 0.5

def symEgFunc():
	sym = SYM()
	pairs = ["a","a","a","a","b","b","c"]
	for x in pairs:
		sym.add(x)
	return sym.mid() == "a" and rnd(sym.div()) == 1.379

def numEgFunc():
	num = NUM()
	pairs = [1,1,1,1,2,2,3]
	for x in pairs:
		num.add(x)
	return num.mid() == 11/7 and rnd(num.div()) == 0.787

def packedOO():
	return oo(the)
	
eg ('the', "show settings", packedOO)
eg ('rand',"generate, reset, regenerate same", randEgFunc)
eg ('sym',"check syms", symEgFunc)
eg('num', "check nums", numEgFunc)

main(the,help)


	