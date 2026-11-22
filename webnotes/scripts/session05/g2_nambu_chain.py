# BdG bands of a chain without and with s-wave pairing, with the electron weight, Section 5.8
import numpy as np
from pyqula import geometry

nk = 241  # number of momenta
kpath = [[k, 0., 0.] for k in np.linspace(-0.5, 0.5, nk)]  # momentum in units of 2 pi
deltas = [0., 0.45]  # pairing Delta, without and with superconductivity
energies = []  # the four BdG bands at each momentum, for each Delta
weights = []  # electron weight of each state, from 0 to 1
for delta in deltas:
    g = geometry.chain()  # chain with one site per cell
    h = g.get_hamiltonian(tij=[-1.])  # first-neighbor hopping -1, the band -2t cos k with t=1
    h.add_onsite(1.0)  # every electron energy goes up by 1, which is mu=-1
    h.add_swave(delta)  # Nambu spinor and s-wave pairing Delta
    (ik, e, c) = h.get_bands(operator="electron", kpath=kpath)  # BdG bands and their electron weight
    energies.append(np.array(e).reshape(nk, -1))  # energy of band n at momentum k
    weights.append(np.array(c).reshape(nk, -1))  # electron weight of band n at momentum k
smallest = [np.min(np.abs(e)) for e in energies]  # smallest quasiparticle energy, 0 and then Delta
