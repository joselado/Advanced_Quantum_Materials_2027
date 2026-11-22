# Bands of a square ribbon and of a honeycomb ribbon in a magnetic field, Section 4.11
import numpy as np
from pyqula import geometry

nk = 201 # number of momenta
ks = np.linspace(-0.5, 0.5, nk) # momentum along the ribbon, in units of 2 pi over its period
kpath = [[k, 0., 0.] for k in ks] # k-path from -pi to pi

g = geometry.square_ribbon(40) # ribbon of the square lattice, 40 sites wide
square_edge = np.max(g.y) # the edges are at y = -19.5 and 19.5
h = g.get_hamiltonian(has_spin=False, tij=[-1.]) # first-neighbor hopping -1, band bottom at -4
h.add_orbital_magnetic_field(0.02) # flux per plaquette, in flux quanta
(ik, e, y) = h.get_bands(operator="yposition", kpath=kpath) # bands with the position of each state
square_energies = np.array(e).reshape(nk, -1) # energy of band n at momentum k
square_positions = np.array(y).reshape(nk, -1) # where each state sits across the ribbon

g = geometry.honeycomb_armchair_ribbon(30) # armchair ribbon of the honeycomb lattice, bond length 1
honeycomb_edge = np.max(g.y) # the edges are at y = -25.5 and 25.5
h = g.get_hamiltonian(has_spin=False) # first-neighbor hopping 1
h.add_orbital_magnetic_field(0.005) # flux per unit area, in flux quanta
(ik, e, y) = h.get_bands(operator="yposition", kpath=kpath) # bands with the position of each state
honeycomb_energies = np.array(e).reshape(nk, -1)
honeycomb_positions = np.array(y).reshape(nk, -1)

h = g.get_hamiltonian(has_spin=False) # the same honeycomb ribbon, with no field
(ik, e, y) = h.get_bands(operator="yposition", kpath=kpath)
nofield_energies = np.array(e).reshape(nk, -1)
nofield_positions = np.array(y).reshape(nk, -1)
