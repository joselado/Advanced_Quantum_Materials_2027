# Antiferromagnet of the Hubbard chain (1.7) in mean field, at half filling
import numpy as np
from pyqula import geometry

g = geometry.bichain()  # chain with two sites per cell
h = g.get_hamiltonian()  # with the two spins, first-neighbor hopping +1
nk = 400  # cells of the mesh, the same for the loop and for the moments
Us = np.array([0., 1., 1.5, 2., 2.5, 3., 3.5, 4., 5., 6., 7., 8.])  # onsite repulsion U, in units of the hopping
moment, gap = [], []
for U in Us:
    # mean field of U n_up n_dn, one electron per site, starting from an antiferromagnetic guess
    hmf = h.get_mean_field_hamiltonian(U=U, mf="antiferro", mix=0.9, nk=nk)
    m = hmf.get_vev("mz", nk=nk)  # n_up - n_dn on the two sites, the m of (1.8)
    moment.append(abs(m[0]))  # the local moment, the same on both sites with opposite signs
    gap.append(hmf.get_gap())  # the gap of the mean-field bands
