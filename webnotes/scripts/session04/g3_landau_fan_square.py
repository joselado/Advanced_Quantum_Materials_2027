# Landau levels of the square lattice against the magnetic flux, Section 4.9
import numpy as np
from pyqula import geometry

qs = np.arange(10, 61) # plaquettes per flux quantum
fluxes = 1/qs # flux per plaquette, in units of the flux quantum h/e
nlevels = 6 # number of Landau levels that we keep
levels = [] # the lowest levels for each flux
for q in qs:
    g = geometry.square_lattice().get_supercell((1, q)) # magnetic cell of q sites along y
    h = g.get_hamiltonian(has_spin=False, tij=[-1.]) # first-neighbor hopping -1, band bottom at -4
    h.add_orbital_magnetic_field(1/q) # one flux quantum through the cell
    e = np.linalg.eigvalsh(h.get_hk_gen()([0., 0., 0.])) # energies at k = 0, the levels are flat bands
    levels.append(e[:nlevels]) # the lowest Landau levels
levels = np.array(levels) # levels[i, n] is the level n at the flux fluxes[i]
continuum = -4 + 4*np.pi*np.outer(fluxes, np.arange(nlevels) + 0.5) # levels of (4.6), hbar omega_c = 4 pi flux t
