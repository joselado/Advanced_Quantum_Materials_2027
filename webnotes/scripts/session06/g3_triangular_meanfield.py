# Noncollinear mean field of the Hubbard model on the triangular lattice, Section 6.10
import numpy as np
from pyqula import geometry

g = geometry.triangular_lattice().get_supercell((3, 3))  # cell of nine sites, which holds the 120 degree order
a1, a2 = np.array(g.a1), np.array(g.a2)  # lattice vectors of the cell
pairs = [(i, j) for i in range(9) for j in range(9) for n1 in (-1, 0, 1) for n2 in (-1, 0, 1)
         if i < j and abs(np.linalg.norm(g.r[j] + n1*a1 + n2*a2 - g.r[i]) - 1.) < 1e-6]  # first-neighbor bonds
U = 10.  # strong Hubbard interaction, in units of the hopping
moments, angles, energies = [], [], []  # one entry for each random guess
for seed in range(4):  # the guess mf="XY" is random, so we try four of them
    np.random.seed(seed)  # fixes the random guess
    h = g.get_hamiltonian()  # spinful Hamiltonian with first-neighbor hopping 1, at half filling
    (hmf, e) = h.get_mean_field_hamiltonian(U=U, mf="XY", mix=0.9, maxite=4000, nk=8, return_total_energy=True)  # solve it
    m = np.array([np.real(hmf.get_vev(o, nk=8)) for o in ("mx", "my", "mz")]).T  # moment of each site, same k-mesh
    size = np.linalg.norm(m, axis=1)  # length of each moment
    cosines = np.array([m[i] @ m[j]/(size[i]*size[j]) for (i, j) in pairs])  # cosine of the angle on each bond
    moments.append(m)  # the moments of this guess
    angles.append(np.degrees(np.arccos(np.clip(cosines, -1., 1.))))  # angles between neighbors, in degrees
    energies.append(e)  # mean-field energy per cell of nine sites
