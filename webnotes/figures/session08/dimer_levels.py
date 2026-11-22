"""Session 8, the levels of the Ising dimer (8.1) and of the Heisenberg dimer (8.2), from the 4x4 matrices, with the
energy in units of J on the vertical axis."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _dimerlevels as dl

# the numbers of the caption: Ising -1/4 and +1/4 twice each, Heisenberg singlet -3/4 and triplet +1/4, a gap of J
assert dl.levels(dl.ISING) == [(-0.25, 2), (0.25, 2)]
assert dl.levels(dl.HEIS) == [(-0.75, 1), (0.25, 3)]
assert dl.levels(dl.HEIS)[1][0] - dl.levels(dl.HEIS)[0][0] == 1.0
lv = dl.plot(__file__, [
    (dl.ISING, 'Ising dimer', [r'$|{\uparrow\downarrow}\rangle$, $|{\downarrow\uparrow}\rangle$',
                               r'$|{\uparrow\uparrow}\rangle$, $|{\downarrow\downarrow}\rangle$']),
    (dl.HEIS, 'Heisenberg dimer', ['singlet', 'triplet']),
], r'$E/J$', width_cm=10.5, xlabel_gap=2.35, right=1.25)
assert lv == [[(-0.25, 2), (0.25, 2)], [(-0.75, 1), (0.25, 3)]]
