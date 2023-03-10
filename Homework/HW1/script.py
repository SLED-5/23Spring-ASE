import re
import sys
import math
import utils as ut
import config
from NUM import *
from SYM import *
import getopt

the = {}
help = '''[[   
script.lua : an example script with help text and a test suite
(c)2022, Tim Menzies <timm@ieee.org>, BSD-2 

USAGE:   script.lua  [OPTIONS] [-g ACTION]

OPTIONS:
  -d  --dump  on crash, dump stack = false
  -g  --go    start-up action      = data
  -h  --help  show help            = false
  -s  --seed  random number seed   = 937162211

ACTIONS:
]]'''

egs = {}

# main

def main(options, help):
	global egs
	
	saved, fails = {}, 0
	b4 = {}
	for k, v in config.cli(config.settings(help)).items():
		options[k] = v
		saved[k] = v
	if options["help"]:
		print(help)
	else :
		for what in egs.items():
			if options['go'] == "all" or what[0] == options['go']:
				for k, v in saved.items():
					options[k] = v
				ut.Seed = options["seed"]
				if not what[1]():
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
	help = help + ut.fmt("  -g  {}\t{}\n",key,str)


##TODO: debug this
def randEgFunc():
	num1, num2 = NUM(), NUM()
	ut.Seed = the["seed"]
	for i in range(1, 1001):
		num1.add(ut.rand(0,1))
	ut.Seed = the["seed"]
	for i in range(1, 1001):
		num2.add(ut.rand(0,1))
	m1, m2 = ut.rnd(num1.mid(), 10), ut.rnd(num2.mid(), 10)
	return m1 == m2 and ut.rnd(m1, 1) == 0.5


def symEgFunc():
	sym = SYM()
	pairs = ["a","a","a","a","b","b","c"]
	for x in pairs:
		sym.add(x)
	return sym.mid() == "a" and ut.rnd(sym.div()) == 1.379


def numEgFunc():
	num = NUM()
	pairs = [1,1,1,1,2,2,3]
	for x in pairs:
		num.add(x)
	return num.mid() == 11/7 and ut.rnd(num.div()) == 0.787


def packedOO():
	return ut.oo(the)


eg ('the', "show settings", packedOO)
eg ('rand', "generate, reset, regenerate same", randEgFunc)
eg ('sym', "check syms", symEgFunc)
eg('num', "check nums", numEgFunc)

main(the,help)




	