"""Session 8, picture quiz of 8.2, two singlets and two free spins that both point up, which has S_tot = 1."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g1_spins

s2, sz, eigen = _g1_spins.draw(__file__, singlets=((1, 2), (3, 4)), spins={0: 1, 5: 1})
assert eigen and abs(s2 - 2) < 1e-12 and abs(sz - 1) < 1e-12   # S(S+1) = 2, so S = 1, with S^z = 1
