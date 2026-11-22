"""Session 6, Section 6.16, a picture option of the quiz on the magnon ribbons: the Dzyaloshinskii-Moriya hopping DS = 0.1.

The gap of the bulk is 6 sqrt(3) DS = 1.04 at K, and one branch of each edge crosses it, with opposite slopes on the two edges, so
the lower band has |C| = 1. The data come from webnotes/scripts/session06/g5_magnon_ribbon.py, see _g5_ribbonquiz.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g5_ribbonquiz as r

m = r.load(r.style.run_script('session06/g5_magnon_ribbon.py'))[0]
assert m['DS'] == 0.1 and m['M'] == 0.0
assert abs((m['hi'] - m['lo']) - 1.0392) < 5e-5 and abs(m['hi'] - m['lo'] - r.GAP) < 1e-12
for level in (2.75, 3.25):                                  # one branch per edge at each energy of the gap, opposite slopes
    lo, up = r.branch_slopes(m, 'lower', level), r.branch_slopes(m, 'upper', level)
    print('DS=0.1, at E=%.2f lower edge' % level, np.round(lo, 3).tolist(), 'upper edge', np.round(up, 3).tolist())
    assert len(lo) == 1 and len(up) == 1 and lo[0][1] * up[0][1] < 0
r.option(__file__, m)
