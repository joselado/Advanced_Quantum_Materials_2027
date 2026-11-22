"""Session 6, Section 6.16, a picture option of the quiz on the magnon ribbons: an onsite energy 2M on one sublattice, M = 0.52.

It opens a gap of the bulk from 3|J|S to 3|J|S + 2M = 4.04|J|S, the same size 1.04 as the Dzyaloshinskii-Moriya term, and no
state crosses it. The flat edge branches sit at its two borders, 3.0 at the lower edge and 4.04 at the upper edge. The Chern number
of the lower band is 0, which webnotes/checks/session06/g5_16_topological_magnons.py asserts. The data come from
webnotes/scripts/session06/g5_magnon_ribbon.py, see _g5_ribbonquiz.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g5_ribbonquiz as r

m = r.load(r.style.run_script('session06/g5_magnon_ribbon.py'))[2]
assert m['DS'] == 0.0 and m['M'] == 0.52
assert abs(m['lo'] - 3.0) < 1e-12 and abs(m['hi'] - 4.04) < 1e-12
E = m['E']
inside = (E > m['lo'] + 1e-6) & (E < m['hi'] - 1e-6)
print('M=0.52, states strictly inside the gap', inside.sum(), 'flat edge branches at', np.unique(np.round(E[m['lower']], 6)),
      np.unique(np.round(E[m['upper']], 6)))
assert inside.sum() == 0
assert np.allclose(E[m['lower']], 3.0, atol=1e-6) and np.allclose(E[m['upper']], 4.04, atol=1e-6)
assert m['lower'].sum() > 20 and m['upper'].sum() > 20
r.option(__file__, m)
