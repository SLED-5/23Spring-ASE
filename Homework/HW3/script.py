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

def main(options, help):
	eg.runTest()
	egs = eg.egs
	
	saved, fails = {}, 0
	b4 = {}
	curr_settings = config.settings(help)
	config_cli = config.cli(curr_settings)
	for k, v in config_cli.items():
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
					
main(eg.the, config.help)