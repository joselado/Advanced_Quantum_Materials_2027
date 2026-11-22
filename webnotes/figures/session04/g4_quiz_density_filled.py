"""Session 4, section 4.17, a picture option of the quiz on the quasihole: the filled lowest level of 20 electrons.

The density of the orbitals m = 0 to 19 of (4.10), times 2 pi l_B^2. It is 1 within 0.002 from the origin to 4 l_B, with no dip, and drops
through 1/2 at 6.27 l_B, near sqrt(2N) = 6.32."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g4_quizdensity as q

r = np.linspace(0, 12.5, 501)
nu = q.mc.filled_filling(q.N, r)
assert np.abs(nu[r <= 4] - 1).max() < 0.002                 # flat at 1 from the origin, no dip
assert abs(r[np.argmin(np.abs(nu - 0.5))] - 6.3) < 0.1      # it drops to zero near 6 l_B, through 1/2 at 6.27
q.option(__file__, r, nu)
