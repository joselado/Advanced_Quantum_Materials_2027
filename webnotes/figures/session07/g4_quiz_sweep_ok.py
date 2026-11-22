"""Session 7, section 7.10, a picture option of the quiz on a DMRG sweep: the computed sweep of M = 4, which never goes
up and ends 6.1e-3 above E0, on the line at this scale."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g4_sweeps as q

e = q.E.copy()
assert np.all(np.diff(e) < 1e-9) and np.all(e >= q.E0 - 1e-9) and e[-1] - q.E0 < 0.01
q.option(__file__, e)
