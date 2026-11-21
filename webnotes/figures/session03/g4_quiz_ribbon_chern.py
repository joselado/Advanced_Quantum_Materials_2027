"""Session 3, section 3.11, a picture option of the quiz on the ribbon spectra: a Chern insulator with both spins.

The Haldane coupling is the same for both spins, and a Zeeman field 0.08 t shifts the two spins by 0.16 t. The lower edge has one
branch of each spin inside the gap, and both have the same sign of the velocity."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g4_ribbon as r

d = r.load(r.style.run_script('session03/g4_ribbon_chern.py'))
up, down = r.crossings(*r.edge(d, 0.4), level=0.0)
print('chern, lower edge at E=0: up', np.round(up, 3), 'down', np.round(down, 3))
assert len(up) == 1 and len(down) == 1 and up[0][1] > 0 and down[0][1] > 0        # one branch per spin, both to the right
k, e, s = r.edge(d, 0.3)
ku, eu = k[s > 0], e[s > 0]; kd, ed = k[s < 0], e[s < 0]
split = eu[np.argmin(np.abs(ku - 3.0))] - ed[np.argmin(np.abs(kd - 3.0))]
print('chern, splitting of the two spins at the same momentum', round(split, 4))
assert abs(abs(split) - 0.16) < 1e-6                                              # twice the Zeeman field 0.08 t
r.ribbon_option(__file__, d)
