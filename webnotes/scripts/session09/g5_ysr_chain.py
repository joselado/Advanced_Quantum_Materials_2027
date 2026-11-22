# A magnetic impurity in an s-wave superconducting chain, the density of states against the exchange J
import numpy as np
from pyqula import geometry, embedding

g = geometry.chain().get_supercell(3)  # chain with three sites per cell, the impurity sits on one of them
delta = 0.2  # s-wave pairing, the gap of the clean chain
eta = delta/40  # broadening of the density of states
Js = np.linspace(0., 4., 41)  # exchange J S of the impurity
energies = np.linspace(-1.5*delta, 1.5*delta, 121)  # energies inside the gap and around it
h0 = g.get_hamiltonian()  # the normal chain, two spins, half filling
normal = embedding.Embedding(h0, m=h0).multidos(es=[0.], delta=eta, nk=400)[1][0]  # DOS of the cell at E_F
dos = []  # one row per J
for J in Js:
    h = g.get_hamiltonian()  # the same chain
    h.add_swave(delta)  # s-wave superconductor, this builds the BdG Hamiltonian
    hv = h.copy()  # the chain with the impurity
    m = np.zeros((3, 3))  # one exchange vector per site of the cell
    m[0, 2] = J  # J S along z on site 0, onsite energies +J and -J for the two spins
    hv.add_exchange(m)  # the magnetic impurity
    eb = embedding.Embedding(h, m=hv)  # one impurity in the infinite chain
    (e, d) = eb.multidos(es=energies, delta=eta, nk=400)  # DOS of the cell of the impurity
    dos.append(d)  # store it
dos = np.array(dos)/(2*normal)  # in units of the normal state, the BdG Hamiltonian counts each state twice
