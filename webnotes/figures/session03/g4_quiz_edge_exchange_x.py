"""Session 3, section 3.11b, a picture option of the quiz on time reversal: the helical edge with an exchange field 0.1 t along x.

The field breaks time reversal and couples the two spins, so it opens a gap at the crossing at k=pi."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g4_ribbon as r

d = r.load(r.style.run_script('session03/g4_edge_exchange_x.py'))
mid = len(d['energy']) // 2
E = np.where(d['lower'] & (np.abs(d['energy']) < 0.4), d['energy'], np.nan)
top, bottom = np.nanmin(np.where(E > -0.01, E, np.nan), axis=1), np.nanmax(np.where(E < -0.01, E, np.nan), axis=1)
gap = np.nanmin(top) - np.nanmax(bottom)
pair = d['energy'][mid][(d['lower'][mid]) & (np.abs(d['energy'][mid]) < 0.3)]
print('exchange x, lower edge at k=pi:', pair, 'gap of the edge', round(gap, 4))
assert len(pair) == 2 and abs((pair[1] - pair[0]) - gap) < 1e-3 and abs(gap - 0.19) < 0.005   # the gap is at k = pi, about 0.19 t
r.edge_option(__file__, d)
