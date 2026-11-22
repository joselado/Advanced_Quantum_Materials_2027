"""Session 4, section 4.17, a picture option of the quiz on the quasihole: the Laughlin state with m = 3 and a quasihole at
the origin, the factor prod_i z_i of (4.14) with w = 0.

The mean of four Metropolis runs of 20 electrons, seeds 51 to 54, the blue curve of g4_quasihole_dimple.py. The density
times 2 pi l_B^2 vanishes at the origin, below 0.01 in the first bin, and it is back at 1/3 within 0.01 for 4 l_B < r < 7 l_B.
The bump of the edge is near 9 l_B, between 8.5 and 9.5. The charge of the dip, about 1/3 in the discs of radius 5 to 8 l_B,
is asserted in g4_quasihole_dimple.py with the same runs."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g4_quizdensity as q

rc, nu = q.mean_density([0j], (51, 52, 53, 54))
sel = (rc > 4) & (rc < 7)
print('first bin', round(nu[0], 4), 'filling for 4 < r < 7', round(nu[sel].mean(), 3))
assert nu[0] < 0.01 and abs(nu[sel].mean() - 1 / 3) < 0.01     # zero at the quasihole, 1/3 away from it
assert 8.5 < rc[np.argmax(nu)] < 9.5                            # the bump of the edge near 9 l_B
q.option(__file__, rc, nu)
