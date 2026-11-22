"""Session 8, quiz of 8.3, the levels of H = J S0.S1 for J=1 and J=-1, from the 4x4 matrix, with the energy in units
of |J| on the vertical axis."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _dimerlevels as dl

# J = 1: the singlet at -3/4 below the triplet at +1/4; J = -1: the triplet at -1/4 below the singlet at +3/4
assert dl.levels(dl.HEIS) == [(-0.75, 1), (0.25, 3)]
assert dl.levels(-dl.HEIS) == [(-0.25, 3), (0.75, 1)]
lv = dl.plot(__file__, [
    (dl.HEIS, r'$J=1$', ['singlet', 'triplet']),
    (-dl.HEIS, r'$J=-1$', ['triplet', 'singlet']),
], r'$E/|J|$', width_cm=8.6)
assert lv == [[(-0.75, 1), (0.25, 3)], [(-0.25, 3), (0.75, 1)]]
