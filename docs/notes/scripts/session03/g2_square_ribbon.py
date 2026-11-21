# Bands of a ribbon of the square lattice in a magnetic field, Section 3.6b
import numpy as np
from pyqula import geometry

W = 40 # width of the ribbon, in sites
Bs = [0., 0.01, 0.015, 0.02] # magnetic flux per plaquette, in flux quanta
nk = 201 # number of momenta
ks = np.linspace(-0.5, 0.5, nk) # momentum along the ribbon, in units of 2 pi
kpath = [[k, 0., 0.] for k in ks] # k-path from -pi to pi

g = geometry.square_ribbon(W) # create the ribbon
energies = [] # bands for each field
positions = [] # position across the ribbon for each field
for B in Bs:
    h = g.get_hamiltonian(has_spin=False, tij=[-1.]) # create the Hamiltonian
    h.add_orbital_magnetic_field(B) # add the magnetic field
    (ik, e, y) = h.get_bands(operator="yposition", kpath=kpath) # compute the bands
    energies.append(np.array(e).reshape(nk, W)) # energy of band n at momentum k
    positions.append(np.array(y).reshape(nk, W)) # where each state sits
