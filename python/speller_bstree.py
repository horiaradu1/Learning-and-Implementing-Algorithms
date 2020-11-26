import speller
import sys
import config

config.set_type = config.SetType.BSTREE
config.prog_name = "speller_bstree.py"
sys.setrecursionlimit(1000000000)
speller.spelling(sys.argv)
