"""Session 9, Section 9.9, a picture option of the quiz on three gapped spinon chains: chi alternating 1 and 0.6, gap 0.8.

The steepest of the three: the moment falls below 1e-8 from n = 20 on the sites of one sublattice and from n = 27 on the
other, so the points stop before n = 30, and the last points drawn above the floor are at n = 18 and n = 25."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g5_spinon as gs

m, c = gs.option(__file__, 0.6)
a = np.abs(m[c:c + 41])
first = [next(n for n in range(p, 41, 2) if a[n] < 1e-8) for p in (2, 1)]
assert first == [20, 27]
last = [[n for n in range(p, 41, 2) if a[n] >= 1e-8][-1] for p in (2, 1)]
assert last == [18, 25]
