"""Session 8, picture quiz of 8.2, six sites paired into three singlets, which has S_tot = 0."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g1_spins

s2, sz, eigen = _g1_spins.draw(__file__, singlets=((0, 1), (2, 3), (4, 5)))
assert eigen and abs(s2) < 1e-12 and abs(sz) < 1e-12          # S(S+1) = 0, so S = 0
