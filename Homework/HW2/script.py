from NUM import *
from SYM import *
from COLS import *
from ROW import *
from DATA import *

import re
import sys
import math
import utils as ut
import config
import getopt
import eg

the = {}
help = '''[[   
data.lua : an example csv reader script
(c)2022, Tim Menzies <timm@ieee.org>, BSD-2 

USAGE:   data.lua  [OPTIONS] [-g ACTION]

OPTIONS:
	-d  --dump  on crash, dump stack = false
	-f  --file  name of file         = ../etc/data/auto93.csv
	-g  --go    start-up action      = data
	-h  --help  show help            = false
	-s  --seed  random number seed   = 937162211

ACTIONS:
]]'''

def main(options, help):
	eg.runTest()
	egs = eg.egs
	
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
					
main(the, help)