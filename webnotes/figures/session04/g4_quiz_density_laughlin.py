"""Session 4, section 4.17, a picture option of the quiz on the quasihole: the Laughlin state with m = 3 and no quasihole.

The mean of four Metropolis runs of 20 electrons, seeds 1 to 4, the grey curve of g4_quasihole_dimple.py. The density times
2 pi l_B^2 is 1/3 within 0.02 in every bin for r < 4 l_B, the first bin included, so there is no dip at the origin, and it
has the bump of the edge near 9 l_B, between 8.5 and 9.5."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g4_quizdensity as q

rc, nu = q.mean_density([], (1, 2, 3, 4))
print('filling for r < 2', round(nu[rc < 2].mean(), 3), 'first bin', round(nu[0], 3), 'largest deviation for r < 4', round(np.abs(nu[rc < 4] - 1 / 3).max(), 4))
assert abs(nu[rc < 2].mean() - 1 / 3) < 0.01 and abs(nu[0] - 1 / 3) < 0.02    # flat at 1/3 down to the origin
assert np.abs(nu[rc < 4] - 1 / 3).max() < 0.02                  # no bin of the first 4 l_B draws a dip
assert 8.5 < rc[np.argmax(nu)] < 9.5                            # the bump of the edge near 9 l_B
q.option(__file__, rc, nu)
