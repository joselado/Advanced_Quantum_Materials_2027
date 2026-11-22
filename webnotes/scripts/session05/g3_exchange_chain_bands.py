# Bands of a chain with an exchange field, for each spin, Section 5.12
import numpy as np
from pyqula import geometry

g = geometry.chain()  # chain with one site per cell
nk = 401  # number of momenta
kpath = [[k, 0., 0.] for k in np.linspace(-0.5, 0.5, nk)]  # momentum in units of 2 pi
cases = [(0., 0.6), (-1.5, 0.2), (-1.5, 1.2), (-1.5, -1.2)]  # pairs of chemical potential mu and exchange field h
energies = []  # the two bands at each momentum, for each case
spins = []  # the spin s_z of each state, +1 for up and -1 for down
for (mu, field) in cases:
    h = g.get_hamiltonian(tij=[-1.])  # two spins, the band -2t cos k with t=1
    h.add_onsite(-mu)  # chemical potential mu
    h.add_exchange([0., 0., -field])  # the term -h (n_up - n_dn), spin up moves down by h
    (ik, e, sz) = h.get_bands(operator="sz", kpath=kpath)  # bands and the spin of each state
    energies.append(np.array(e).reshape(nk, -1))  # energy of band n at momentum k
    spins.append(np.array(sz).reshape(nk, -1))  # s_z of band n at momentum k
