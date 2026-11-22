# Levels of a hexagonal island of the honeycomb lattice and the density of three of them, Section 1.10
import numpy as np
from pyqula import islands

g = islands.get_geometry(name="honeycomb", n=4, nedges=6, rot=0)  # hexagonal island of 96 sites with zigzag edges
h = g.get_hamiltonian(has_spin=False, tij=[-1.])  # first-neighbor hopping -t with t = 1, the sign of H = -t sum c_i^dag c_j
(energies, states) = np.linalg.eigh(h.intra)  # all the levels, lowest first, and one state per column
x, y = g.x, g.y  # positions of the sites, in units of the bond length

levels = np.unique(np.round(energies, 8))  # the distinct levels, a degenerate level counted once
density = {}  # density of a level on each site, averaged over its degenerate states
for n in [0, 1, 5]:  # the lowest, the second and the sixth level
    same = np.abs(energies - levels[n]) < 1e-6  # the states of this level
    density[n] = np.mean(np.abs(states[:, same])**2, axis=1)

print(levels[[0, 1, 5]])  # -2.91, -2.76 and -2.34
