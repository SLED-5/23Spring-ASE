from NUM import *
from SYM import *
from COLS import *
from DATA import *

import re
import sys
import math
import utils as ut
import config
import getopt
import eg
import copy


def main(options, main_help):
    # y, n, saved = 0, 0, copy.deepcopy(the)
    pass_cases = 0
    eg.runTest()
    egs = eg.egs

    saved, fails = {}, 0
    b4 = {}
    curr_settings = config.settings(main_help)
    config_cli = config.cli(curr_settings)
    for k, v in config_cli.items():
        options[k] = v
        saved[k] = v
    if options["help"]:
        print(main_help)
    else:
        for what in egs.items():
            if options['go'] == "all" or what[0] == options['go']:
                for k, v in saved.items():
                    options[k] = v
                ut.Seed = options["seed"]
                if not what[1]():
                    fails = fails + 1
                    print("❌ fail:" + what[0])
                else:
                    pass_cases += 1
                    print("✅ pass:" + what[0])
    if pass_cases + fails > 0:
        print("🔆 %s", utils.o({"pass": pass_cases, "fail": fails, "success": 100*pass_cases/(pass_cases+fails)//1}))

main(config.Is, config.help)