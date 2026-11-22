# Charge density wave of the spinless chain (1.6) in mean field, at half filling
import numpy as np
from pyqula import geometry

g = geometry.bichain()  # chain with two sites per cell
h = g.get_hamiltonian(has_spin=False)  # spinless, first-neighbor hopping +1
nk = 400  # cells of the mesh, the same for the loop and for the charges
Vs = np.array([0., 0.5, 0.75, 1., 1.5, 2., 2.5, 3., 4., 5., 6.])  # repulsion V between neighbors, in units of the hopping
charges, imbalance, gap = [], [], []
for V in Vs:
    # Hartree mean field of V n_i n_(i+1), one electron per cell, starting from a charge density wave
    hmf = h.get_mean_field_hamiltonian(V1=V, mf="CDW", filling=0.5, mix=0.9, nk=nk, compute_cross=False, write=False)
    n = hmf.get_vev(nk=nk)  # charge <n_i> on the two sites of the cell
    charges.append(n)
    imbalance.append(abs(n[0] - n[1]))  # the charge imbalance, between 0 and 1
    gap.append(hmf.get_gap())  # the gap of the mean-field bands
