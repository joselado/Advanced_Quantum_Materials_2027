"""Session 3, section 3.9b, a picture option of the quiz on the levels of open chains: the chain that ends with a strong bond."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g3_levels
from _g3_levels import style

_g3_levels.option(__file__, style.run_script('session03/g3_ssh_chains.py'), 'levels_strong_ends')
