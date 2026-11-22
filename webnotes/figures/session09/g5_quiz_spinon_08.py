"""Session 9, Section 9.9, a picture option of the quiz on three gapped spinon chains: chi alternating 1 and 0.8, gap 0.4.

Between the two others: on the sites of one sublattice the moment is 2.9e-5 at n = 10 and 1.6e-8 at n = 36, the last point
of that sublattice above the floor 1e-8 of the picture, and the points of the other sublattice stay above the floor up to
n = 39, so only one line reaches the bottom of the axis."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g5_spinon as gs

m, c = gs.option(__file__, 0.8)
a = np.abs(m[c:c + 41])
assert abs(a[10] / 2.9e-5 - 1) < 0.02 and abs(round(a[36] * 1e8, 1) - 1.6) < 1e-12
drawn = [[n for n in range(p, 41, 2) if a[n] >= 1e-8] for p in (2, 1)]
assert drawn[0][-1] == 36 and a[38] < 1e-8 and drawn[1][-1] == 39 and a[39] > 10 * 1e-8
