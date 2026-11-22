"""Session 7, section 7.10, a picture option of the quiz on a DMRG sweep: the computed sweep of M = 4 shifted down by
hand by 0.5 J, so that its last points lie below E0."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g4_sweeps as q

e = q.E - q.SHIFT
assert q.SHIFT == 0.5 and np.all(e[-20:] < q.E0 - 0.4)                      # the last points are below the line
q.option(__file__, e)
