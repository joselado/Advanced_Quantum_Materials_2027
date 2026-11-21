"""Session 3, section 3.11b, a picture option of the quiz on time reversal: the helical edge with a Rashba coupling 0.1 t.

The Rashba coupling mixes the spins and keeps time reversal. The two branches of the lower edge stay degenerate at k=pi, and the
spectrum of the edge is the same at pi+q and at pi-q."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g4_ribbon as r

d = r.load(r.style.run_script('session03/g4_edge_rashba.py'))
mid = len(d['energy']) // 2
pair = d['energy'][mid][(d['lower'][mid]) & (np.abs(d['energy'][mid]) < 0.3)]
print('rashba, lower edge at k=pi:', pair)
assert len(pair) == 2 and abs(pair[0] - pair[1]) < 1e-9                           # the Kramers pair
for j in (5, 12, 20):                                                             # the mirror symmetry around k = pi
    a = d['energy'][mid + j][(d['lower'][mid + j]) & (np.abs(d['energy'][mid + j]) < 0.4)]
    b = d['energy'][mid - j][(d['lower'][mid - j]) & (np.abs(d['energy'][mid - j]) < 0.4)]
    assert len(a) == 2 and np.allclose(a, b, atol=1e-9), (a, b)
k, e, s = r.edge(d, 0.3)
print('rashba, smallest |s_z| of the drawn states away from the crossing', round(np.abs(s[np.abs(k - np.pi) > 0.05]).min(), 3))
r.edge_option(__file__, d)
