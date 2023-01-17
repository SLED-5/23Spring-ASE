import re
import sys

the = {}
help = "script.lua : an example script with help text and a test suite\n(c)2022, Tim Menzies <timm@ieee.org>, BSD-2 \nUSAGE:   script.lua  [OPTIONS] [-g ACTION]\n\n\nOPTIONS:\n	-d  --dump  on crash, dump stack = false\n	-g  --go    start-up action      = data\n	-h  --help  show help            = false\n	-s  --seed  random number seed   = 937162211\nACTIONS:"
egs = {}
main(the,help, egs)

def settings(s):
	matches = re.finditer(r"\n[%s]+[-][%S]+[%s]+[-][-]([%S]+)[^\n]+= ([%S]+)", s)
	for match in matches:
		k, v = match.groups()
		t[k] = coerce(v)
	return t

def cli(options):
	for k, v in options.items():
		v = str(v)
		for n, x in enumerate(sys.argv):
			if x == "-" + k[0] or x == "--" + k:
				if v == "false":
					v = "true"
				elif v == "true":
					v = "false"
				else:
					v = sys.argv[n]
		options[k] = coerce(v)
	return options

def main(options, help, funs):
	print("hello world")
	saved, fails = {}, 0
	b4 = {}
	for k, v in sys.argv:
		options[k] = v
		
	for k, v in cli(settings(help)).items():
		options[k] = v
		saved[k] = v
	if options["help"]:
		print(help)
	else :
		for what, fun in funs.items():
			if options["go"] == "all" or what == options["go"]:
				for k, v in saves.items():
					options[k] = v
				Seed = options["seed"]
				if not funs["what"]():
					fails = fails + 1
					print("❌ fail:" + what)
				else:
					print("✅ pass:" + what)
	for k, v in sys.argv:
		if not b4[k]:
			print(fmt("#W ?%s %s",k,type(v)))
	os.exit(fails)
	
				