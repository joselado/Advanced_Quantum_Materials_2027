"""Session 9, Section 9.8, a picture option of the quiz on a vacancy: the Haldane model with t2 = 0.15t, C = 1.

One level in the gap of 1.56t, at E = 0, with 0.45 of its weight on the three neighbors of the vacancy."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g5_vacancy as gv

d = gv.option(__file__, 'chern')
gap, e, w = d['gaps']['chern'], d['levels']['chern'], d['weights']['chern']
inside = np.abs(e) < gap / 2 - 1e-3
assert abs(round(gap, 2) - 1.56) < 1e-12 and inside.sum() == 1 and abs(e[inside][0]) < 1e-9 and abs(w[inside][0] - 0.45) < 0.005
