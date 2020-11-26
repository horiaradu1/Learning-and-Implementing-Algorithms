import speller
import sys
import config

config.set_type = config.SetType.DARRAY
config.prog_name = "speller_darray.py"
sys.setrecursionlimit(1000000000)
speller.spelling(sys.argv)
