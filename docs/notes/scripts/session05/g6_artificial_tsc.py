# Artificial topological superconductor of the notebook, the transition with the exchange field, Section 5.18
import numpy as np
from pyqula import geometry

g = geometry.triangular_lattice()  # triangular lattice, first-neighbor hopping +1, which is t=-1 of the notes
ks = np.linspace(-0.5, 0.5, 1001)  # the line M, Gamma, M, in units of the reciprocal vectors
Js = np.linspace(0., 0.6, 41)  # exchange fields
emin = []  # smallest quasiparticle energy on the line, for each J
for J in Js:
    h = g.get_hamiltonian()  # Hamiltonian with the two spins
    h.add_onsite(-5.7)  # the band at Gamma, its top before the Rashba term, comes down to 0.3
    h.add_rashba(1.0)  # Rashba spin-orbit coupling
    h.add_zeeman([0., 0., J])  # exchange field along z
    h.add_swave(0.3)  # s-wave pairing Delta=0.3
    hk = h.get_hk_gen()  # Bloch Hamiltonian, the BdG matrix at each momentum
    e = [np.linalg.eigvalsh(hk([k, 0., 0.])) for k in ks]  # BdG levels on the line
    emin.append(np.min(np.abs(e)))  # smallest quasiparticle energy
Jc = [0.3, 0.6]  # two exchange fields, below and above the closing
cherns = []  # Chern number of the BdG bands below zero
for J in Jc:
    h = g.get_hamiltonian()  # the same model again
    h.add_onsite(-5.7)  # the band at Gamma at 0.3
    h.add_rashba(1.0)  # Rashba spin-orbit coupling
    h.add_zeeman([0., 0., J])  # exchange field along z
    h.add_swave(0.3)  # s-wave pairing
    cherns.append(h.get_chern(nk=40))  # it gives 0 and then 1
