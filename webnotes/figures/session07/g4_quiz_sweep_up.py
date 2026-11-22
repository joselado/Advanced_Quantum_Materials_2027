"""Session 7, section 7.10, a picture option of the quiz on a DMRG sweep: the computed sweep of M = 4 changed by hand
at one update, where the energy goes up by 1.5 J and then comes back."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g4_sweeps as q

e = q.E.copy()
e[q.K_UP] += q.UP
d = np.diff(e)
assert np.sum(d > 1e-9) == 1 and abs(d[q.K_UP - 1] - q.UP - (q.E[q.K_UP] - q.E[q.K_UP - 1])) < 1e-12
assert q.UP == 1.5 and e[q.K_UP] - e[q.K_UP - 1] > 1.4                     # the feedback says up by 1.5 J
q.option(__file__, e)
