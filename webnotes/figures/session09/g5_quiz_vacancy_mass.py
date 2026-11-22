"""Session 9, Section 9.8, a picture option of the quiz on a vacancy: the sublattice mass M = 0.78t, C = 0.

The same gap 1.56t as the Chern insulator, and no level inside it."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g5_vacancy as gv

d = gv.option(__file__, 'trivial')
gap, e = d['gaps']['trivial'], d['levels']['trivial']
assert abs(gap - 1.56) < 1e-9 and not np.any(np.abs(e) < gap / 2 - 1e-3)
