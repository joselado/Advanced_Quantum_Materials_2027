"""Session 6, Section 6.16, a picture option of the quiz on the magnon ribbons: the plain ferromagnet, DS = 0 and M = 0.

The ribbon has no gap: every energy of the window of the other two pictures, 2.48 to 3.52, is reached by some band, and the
lower and the upper bands meet at a flat branch at 3|J|S around k = pi, the zigzag edge state. With no gap no state is drawn in
color. The data come from webnotes/scripts/session06/g5_magnon_ribbon.py,
see _g5_ribbonquiz.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g5_ribbonquiz as r

m = r.load(r.style.run_script('session06/g5_magnon_ribbon.py'))[3]
assert m['DS'] == 0.0 and m['M'] == 0.0
E, k = m['E'], m['k']
levels = np.sort(E[(E > 2.48) & (E < 3.52)])
empty = np.max(np.diff(np.concatenate([[2.48], levels, [3.52]])))   # the largest empty interval in the window of the other gaps
flat = np.abs(E - 3.0) < 1e-3
print('no gap: largest empty interval in [2.48, 3.52]', round(empty, 4), 'flat branch at 3 from k =', round(k[flat.any(1)].min(), 3),
      'to', round(k[flat.any(1)].max(), 3))
assert empty < 0.03 and k[flat.any(1)].min() < 2.6 and k[flat.any(1)].max() > 3.7
assert not m['lower'].any() and not m['upper'].any()
r.option(__file__, m)
