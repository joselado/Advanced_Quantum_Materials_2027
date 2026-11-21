"""Session 3, section 3.10b, a picture option of the quiz on the ribbons with the same gap: the Haldane coupling and a larger sublattice imbalance."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g3_ribbons
from _g3_ribbons import style

_g3_ribbons.option(__file__, style.run_script('session03/g3_haldane_ribbons.py'), 2)
