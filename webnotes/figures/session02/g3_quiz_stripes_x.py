"""Session 2, Section 2.8, a picture option of the quiz on the hopping along y: the band -2t cos(phi_x), which does not
change along phi_y. This is the right option. numpy, see _g3_maps.stripes_x."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g3_maps as maps

Z = maps.stripes_x()
assert np.allclose(Z, Z[:, :1]) and np.isclose(Z.min(), -2) and np.isclose(Z.max(), 2)
maps.option(__file__, Z)
