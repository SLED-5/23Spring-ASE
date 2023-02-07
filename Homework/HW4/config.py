import re
import utils as ut
import sys

the = {}
help = '''[[   
cluster.lua : an example csv reader script
(c)2022, Tim Menzies <timm@ieee.org>, BSD-2 

USAGE: cluster.lua  [OPTIONS] [-g ACTION]

OPTIONS:
  -d  --dump    on crash, dump stack   = false
  -f  --file    name of file           = ./etc/data/repgrid1.csv
  -g  --go      start-up action        = all
  -h  --help    show help              = false
  -p  --p       distance coefficient   = 2
  -s  --seed    random number seed     = 937162211

ACTIONS:
]]
'''

def settings(s):
    t = {}
    pattern = re.compile("\n[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)")
    matches = re.finditer(pattern, s)
    for match in matches:
        k = match.groups(0)[0]
        v = match.groups(0)[1]
        t[k] = ut.coerce(v)
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
        options[k] = ut.coerce(v)
    return options
