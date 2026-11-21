# Bands of a ribbon in a magnetic field, in the opposite field and without field, Section 3.6
import numpy as np
from pyqula import geometry

W = 20 # width of the ribbon, in unit cells
Bs = [0.04, -0.04, 0.] # magnetic field, as in the notebook
nk = 201 # number of momenta
ks = np.linspace(-0.5, 0.5, nk) # momentum along the ribbon, in units of 2 pi
kpath = [[k, 0., 0.] for k in ks] # k-path from -pi to pi

g = geometry.triangular_ribbon(W) # create a ribbon of the triangular lattice
nbands = len(g.r) # number of bands, one per site of the unit cell
energies = [] # bands for each field
positions = [] # position across the ribbon for each field
for B in Bs:
    h = g.get_hamiltonian(has_spin=False, tij=[-1.]) # create the Hamiltonian
    h.add_onsite(4.) # shift the energies, as in the notebook
    h.add_orbital_magnetic_field(B) # add the magnetic field
    (ik, e, y) = h.get_bands(operator="yposition", kpath=kpath) # compute the bands
    energies.append(np.array(e).reshape(nk, nbands)) # energy of band n at momentum k
    positions.append(np.array(y).reshape(nk, nbands)) # where each state sits across the ribbon
