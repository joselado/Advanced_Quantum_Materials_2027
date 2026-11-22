"""Session 8, picture quiz of 8.2, six spins up with one flipped down, which has S^z_tot = 2, so S_tot >= 2."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g1_spins

s2, sz, eigen = _g1_spins.draw(__file__, spins={0: 1, 1: 1, 2: -1, 3: 1, 4: 1, 5: 1})
# S^z = 2, so the total spin is at least 2. The flip on one site is not an eigenstate of S_tot^2, it mixes S = 3
# (weight 1/6) and S = 2 (weight 5/6), so <S_tot^2> = 12/6 + 6*5/6 = 7.
assert abs(sz - 2) < 1e-12 and not eigen and abs(s2 - 7) < 1e-12
