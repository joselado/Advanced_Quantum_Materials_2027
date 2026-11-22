# Ribbons of a superconductor on the triangular lattice, with s-wave, chiral p-wave and nodal f-wave pairing, Section 5.14
import numpy as np
from pyqula import geometry, ribbon

g = geometry.triangular_lattice()  # triangular lattice, first-neighbor hopping 1
gr = ribbon.bulk2ribbon(g, n=20)  # ribbon 20 sites wide, periodic along x
modes = ["swave", "chiral_pwave", "nodal_fwave"]  # the three pairings
nk = 200  # number of momenta along the ribbon
ks = np.linspace(-0.5, 0.5, nk, endpoint=False)  # momentum along the ribbon, in units of 2 pi
kpath = [[k, 0., 0.] for k in ks]  # the k-path of the ribbon
energies, positions = [], []  # bands and positions, one entry per pairing
for mode in modes:
    h = gr.get_hamiltonian()  # Hamiltonian of the ribbon, with the two spins
    h.add_onsite(-3.0)  # the Fermi level at 3, so the empty states form a pocket around Gamma
    h.add_pairing(mode=mode, delta=0.4)  # pairing of this symmetry
    (ik, e, y) = h.get_bands(operator="yposition", kpath=kpath)  # bands with the position of each state
    energies.append(np.array(e).reshape(nk, -1))  # energy of band n at momentum k
    positions.append(np.array(y).reshape(nk, -1))  # where each state sits across the ribbon
cherns = []  # Chern number of the bulk, for the two pairings with a full gap
for mode in modes[:2]:
    hb = g.get_hamiltonian()  # the two-dimensional bulk
    hb.add_onsite(-3.0)  # the same Fermi level
    hb.add_pairing(mode=mode, delta=0.4)  # the same pairing
    cherns.append(hb.get_chern())  # Chern number of the BdG bands below zero, 0 and -2
width = gr.y.max() - gr.y.min()  # width of the ribbon, the edges are at y = -width/2 and width/2
