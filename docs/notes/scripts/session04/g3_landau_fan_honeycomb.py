# Landau levels of the honeycomb lattice against the magnetic flux, Section 4.10
import numpy as np
from pyqula import geometry

ns = np.arange(10, 61) # cells of the magnetic supercell
fluxes = 1/(3*np.sqrt(3)*ns) # one flux quantum through the cell of area 3 sqrt(3) n, in units of h/e
nstates = 14 # states closest to zero energy, two per Landau level
levels = [] # the levels around zero energy for each flux
for n in ns:
    g = geometry.honeycomb_lattice_square_cell().rotate(90) # rectangular cell of 4 sites, bond length 1
    g = g.get_supercell((n, 1)) # magnetic supercell of 4n sites
    h = g.get_hamiltonian(has_spin=False) # spinless Hamiltonian with first-neighbor hopping 1
    h.add_orbital_magnetic_field(1/(3*np.sqrt(3)*n)) # flux per unit area, in flux quanta
    e = np.linalg.eigvalsh(h.get_hk_gen()([0., 0., 0.])) # energies at k = 0
    levels.append(np.sort(e[np.argsort(np.abs(e))[:nstates]])) # the levels 0, +-1, +-2 and +-3
levels = np.array(levels) # levels[i] are the states closest to zero energy at the flux fluxes[i]
E1 = 3*np.sqrt(np.pi*fluxes) # the first level of (4.7), with hbar v = 3/2 for the bond length 1
