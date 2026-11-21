"""Session 3, section 3.11b, a picture option of the quiz on time reversal: the helical edge with an exchange field 0.1 t along z.

The field breaks time reversal but it keeps s_z, so the two branches still cross. The crossing is no longer at k=pi, and the
spectrum is not the same at pi+q and at pi-q."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g4_ribbon as r

d = r.load(r.style.run_script('session03/g4_edge_exchange_z.py'))
k, e, s = r.edge(d, 0.4)
assert np.abs(s).min() > 0.999                                                    # s_z is conserved
ku, eu = k[s > 0], e[s > 0]; kd, ed = k[s < 0], e[s < 0]
ou, od = np.argsort(ku), np.argsort(kd)
grid = np.linspace(np.pi - 0.8, np.pi + 0.8, 3201)
diff = np.interp(grid, ku[ou], eu[ou]) - np.interp(grid, kd[od], ed[od])
i = np.where(np.sign(diff[:-1]) != np.sign(diff[1:]))[0]
kc = grid[i[0]]
print('exchange z, the branches cross at k - pi =', np.round(grid[i] - np.pi, 3), 'E =', round(np.interp(kc, ku[ou], eu[ou]), 3))
assert len(i) == 1 and abs(kc - np.pi + 0.2) < 0.01                               # one crossing, at k = pi - 0.2
r.edge_option(__file__, d)
