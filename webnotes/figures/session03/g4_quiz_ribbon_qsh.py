"""Session 3, section 3.11, a picture option of the quiz on the ribbon spectra: the quantum spin Hall insulator.

The lower edge has one branch of each spin inside the gap, with opposite velocities, and the two cross at k=pi and E close to 0."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g4_ribbon as r

d = r.load(r.style.run_script('session03/g4_ribbon_qsh.py'))
up, down = r.crossings(*r.edge(d, 0.4), level=0.2)
print('qsh, lower edge at E=0.2: up', np.round(up, 3), 'down', np.round(down, 3))
assert len(up) == 1 and len(down) == 1 and up[0][1] > 0 > down[0][1]              # one branch per spin, spin up to the right
assert abs(up[0][0] + down[0][0] - 2 * np.pi) < 0.02                              # mirror images around k = pi
assert abs(abs(up[0][1]) - 0.44) < 0.01 and abs(abs(down[0][1]) - 0.44) < 0.01     # the slopes at E = 0.2 t, which the feedback quotes with this energy
mid = len(d['energy']) // 2
pair = d['energy'][mid][d['lower'][mid]]
pair = pair[np.abs(pair) < 0.3]
print('qsh, lower edge at k=pi:', pair)
assert len(pair) == 2 and abs(pair[0] - pair[1]) < 1e-9 and abs(pair[0]) < 0.05   # the crossing, closed
r.ribbon_option(__file__, d)
