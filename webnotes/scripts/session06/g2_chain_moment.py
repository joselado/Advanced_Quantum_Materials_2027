# Moment and double occupancy of the half-filled Hubbard chain in mean field, Section 6.7
import numpy as np
from pyqula import geometry

h = geometry.bichain().get_hamiltonian(tij=[-1.]) # two sites per cell, both spins, hopping -1 as in (6.1)
Us = np.concatenate([np.linspace(1., 4., 13), np.linspace(4.5, 10., 12), np.linspace(11., 24., 14)]) # U in units of t
nk = 400 # cells of the k-mesh, since the gap is small at small U
moment = [] # |n_up - n_dn| on a site
for U in Us:
    hmf = h.get_mean_field_hamiltonian(U=U, mf="antiferro", mix=0.9, nk=nk) # antiferromagnet at half filling
    moment.append(abs(hmf.get_vev("mz", nk=nk)[0])) # moment of the first site, on the mesh of the loop
moment = np.array(moment)
double = 1 - moment**2 # 4 <n_up n_dn> in mean field, since <n_up> and <n_dn> are (1 + m)/2 and (1 - m)/2
