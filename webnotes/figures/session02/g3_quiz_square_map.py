"""Session 2, Section 2.8, a picture option of the quiz on the hopping along y: the full band (2.14) of the square
lattice, from the pyqula script webnotes/scripts/session02/g3_square_lattice.py, -4 at Gamma and 4 at M. A wrong
option."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
import _g3_maps as maps

xs, ys, band = maps.grid(style.run_script('session02/g3_square_lattice.py'))
assert np.isclose(band.min(), -4) and np.isclose(band.max(), 4)
maps.option(__file__, band)
