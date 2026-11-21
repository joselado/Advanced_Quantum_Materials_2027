# Bands of a quantum spin Hall ribbon, with the spin and the position of each state, Section 3.11
import numpy as np
from pyqula import geometry

nk = 201 # number of momenta
ks = np.linspace(0., 1., nk) # momentum along the ribbon, in units of 2 pi
kpath = [[k, 0., 0.] for k in ks] # k-path from 0 to 2 pi

g = geometry.honeycomb_zigzag_ribbon(10) # create the ribbon, with zigzag edges
h = g.get_hamiltonian() # create the Hamiltonian
h.add_soc(-0.1) # add the intrinsic spin-orbit coupling
h.add_onsite(0.002*g.y) # small bias across the ribbon, to tell the two edges apart
(ik, energy, spin, position) = h.get_bands(kpath=kpath, operator=["sz", "yposition"]) # compute the bands
momentum = 2*np.pi*ik/(nk-1) # momentum of each state, times the lattice constant
width = g.y.max() - g.y.min() # width of the ribbon, the edges are at y = -width/2 and width/2
