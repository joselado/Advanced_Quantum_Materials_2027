# Bands of three honeycomb ribbons with the same bulk gap, Section 3.10b
import numpy as np
from pyqula import geometry

W = 20 # width of the ribbon
nk = 240 # number of momenta
ks = np.linspace(-0.5, 0.5, nk) # momentum along the ribbon, in units of 2 pi
kpath = [[k, 0., 0.] for k in ks] # k-path from -pi to pi
haldane = [0.1, 0., 0.1] # Haldane coupling of each ribbon
imbalance = [0., 0.45, 0.9] # sublattice imbalance of each ribbon

g = geometry.honeycomb_armchair_ribbon(W) # create the ribbon, with armchair edges
gb = geometry.honeycomb_lattice() # create the infinite lattice
energies = [] # bands of each ribbon
positions = [] # position across the ribbon of each state
bulk_gap = [] # gap of the infinite lattice
chern = [] # Chern number of the infinite lattice
for (t2, m) in zip(haldane, imbalance):
    h = g.get_hamiltonian(has_spin=False) # create the Hamiltonian of the ribbon
    h.add_haldane(t2) # add the Haldane coupling
    h.add_sublattice_imbalance(m) # add the sublattice imbalance
    (ik, e, y) = h.get_bands(operator="yposition", kpath=kpath) # compute the bands
    energies.append(np.array(e).reshape(nk, -1)) # energy of band n at momentum k
    positions.append(np.array(y).reshape(nk, -1)) # where each state sits
    hb = gb.get_hamiltonian(has_spin=False) # create the Hamiltonian of the infinite lattice
    hb.add_haldane(t2) # add the Haldane coupling
    hb.add_sublattice_imbalance(m) # add the sublattice imbalance
    bulk_gap.append(hb.get_gap()) # compute the gap
    chern.append(hb.get_chern(nk=40)) # compute the Chern number
