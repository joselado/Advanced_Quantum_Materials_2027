# Bands of the Kondo lattice (8.21) on a chain, for several hybridizations gamma_K
import numpy as np
from pyqula import geometry
from pyqula.specialhamiltonian import H2HFH

nk = 201  # number of momenta
kpath = [[k, 0., 0.] for k in np.linspace(-0.5, 0.5, nk)]  # momentum from -pi to pi, in units of 2 pi
gammas = [0., 0.5, 0.6, 1.]  # the hybridization gamma_K, in units of the hopping t
energies = []  # the four bands at each momentum, the two spins of c and of f
weights = []  # weight of each state on the conduction electrons, from 0 to 1
for gamma in gammas:
    g = geometry.chain()  # chain of conduction sites
    h = g.get_hamiltonian(tij=[-1.])  # hopping -t with t=1, so the band is -2t cos k, with the two spins
    h = H2HFH(h, JK=gamma)  # one f site per site with its level at zero, mixed with c by the hopping JK
    (ik, e, c) = h.get_bands(operator="dispersive_electrons", kpath=kpath)  # bands and their weight on c
    energies.append(np.array(e).reshape(nk, -1))  # energy of band n at momentum i, sorted
    weights.append(np.array(c).reshape(nk, -1))  # weight on c of band n at momentum i
direct = [np.min(e[:, 2] - e[:, 1]) for e in energies]  # smallest gap at one momentum, it is 2 gamma_K
indirect = [e[:, 2].min() - e[:, 1].max() for e in energies]  # gap between the two bands, 2(sqrt(t^2+gamma_K^2)-t)
