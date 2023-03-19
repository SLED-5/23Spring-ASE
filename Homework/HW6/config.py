import re
import sys
import utils as ut

Is = {}
help = '''[[

xpln: multi-goal semi-supervised explanation
(c) 2023 Tim Menzies <timm@ieee.org> BSD-2

USAGE: lua xpln.lua [OPTIONS] [-g ACTIONS]

OPTIONS:
  -b  --bins    initial number of bins       = 16
  -c  --cliffs  cliff's delta threshold      = .147
  -d  --d       different is over sd*d       = .35
  -f  --file    data file                    = ../../etc/data/auto93.csv
  -F  --Far     distance to distant          = .95
  -g  --go      start-up action              = all
  -h  --help    show help                    = false
  -H  --Halves  search space for clustering  = 512
  -m  --min     size of smallest cluster     = .5
  -M  --Max     numbers                      = 512
  -p  --p       dist coefficient             = 2
  -r  --rest    how many of rest to sample   = 4
  -R  --Reuse   child splits reuse a parent pole = true
  -s  --seed    random number seed           = 937162211
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
