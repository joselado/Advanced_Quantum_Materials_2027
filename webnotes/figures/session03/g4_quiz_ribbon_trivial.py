"""Session 3, section 3.11, a picture option of the quiz on the ribbon spectra: an ordinary insulator.

The gap comes from a sublattice imbalance 0.45 t, so it is 0.9 t as in the other two options, minus the splitting 0.06 t of a small
Zeeman field that separates the two spins in the picture. The zigzag edge has a flat band of each spin, which stays at the top of
the valence band, close to E=-0.45 t, and no state is inside the gap."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g4_ribbon as r

d = r.load(r.style.run_script('session03/g4_ribbon_trivial.py'))
k, e, s = r.edge(d, 0.62)
print('trivial, lower edge states: energies from', round(e.min(), 3), 'to', round(e.max(), 3), 'smallest |E|', round(np.abs(e).min(), 3))
assert np.abs(e).min() > 0.4 and abs(e.mean() + 0.475) < 0.02 and (s > 0.5).any() and (s < -0.5).any()   # a flat band of each spin
assert np.abs(d['energy']).min() > 0.4                                            # no state at all with |E| < 0.4 t
r.ribbon_option(__file__, d)
