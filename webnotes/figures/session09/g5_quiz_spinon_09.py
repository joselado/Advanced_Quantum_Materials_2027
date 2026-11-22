"""Session 9, Section 9.9, a picture option of the quiz on three gapped spinon chains: chi alternating 1 and 0.9, gap 0.2.

The shallowest of the three: on the sites of one sublattice the moment falls from 1.1e-4 at n = 10 to 7.8e-7 at n = 40,
two decades over 30 sites, and every point stays above 1e-8."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g5_spinon as gs

m, c = gs.option(__file__, 0.9)
a = np.abs(m[c:c + 41])
assert abs(a[10] / 1.1e-4 - 1) < 0.05 and abs(a[40] / 7.8e-7 - 1) < 0.01 and a[1:].min() > 1e-8
assert abs(np.log10(a[10] / a[40]) - 2.1) < 0.05
