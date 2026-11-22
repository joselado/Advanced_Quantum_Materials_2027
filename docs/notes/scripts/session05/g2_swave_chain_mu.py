# Quasiparticle energy of a chain with s-wave pairing at three chemical potentials, Section 5.9
import numpy as np
from pyqula import geometry

nk = 401  # number of momenta
kpath = [[k, 0., 0.] for k in np.linspace(0., 0.5, nk)]  # momentum from 0 to pi, in units of 2 pi
mus = [-1.2, 0., 1.2]  # chemical potentials, in units of t
energies = []  # the quasiparticle energy E(k) for each mu
for mu in mus:
    g = geometry.chain()  # chain with one site per cell
    h = g.get_hamiltonian(tij=[-1.])  # first-neighbor hopping -1, the band -2t cos k with t=1
    h.add_onsite(-mu)  # every electron energy goes down by mu
    h.add_swave(0.3)  # s-wave pairing Delta=0.3
    (ik, e) = h.get_bands(kpath=kpath)  # the four BdG bands at each momentum
    e = np.array(e).reshape(nk, -1)  # energy of band n at momentum k
    energies.append(np.min(np.abs(e), axis=1))  # the positive branch E(k), the smallest |E| at each k
gaps = [np.min(E) for E in energies]  # the minimum of E(k), it is Delta for every mu
