"""Session 5, section 5.8, a picture option of the quiz on the BdG bands of the square lattice: add_swave(0.4).

The bands come from webnotes/scripts/session05/g2_nambu_square.py, the notebook cell with set_filling(0.2), and the helper
_g2_bdg.square_option asserts that the two branches come closest at +-Delta, at both crossings of the path."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g2_bdg

_g2_bdg.square_option(__file__, 2)
