"""Session 1, Section 1.10, a picture option of the quiz on the lowest level of the honeycomb island: the sixth level."""
import os, sys
sys.dont_write_bytecode = True  # no __pycache__ next to the figures
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import style
import _g2_island

_g2_island.option(__file__, style.run_script('session01/g2_honeycomb_island.py'), 5)
