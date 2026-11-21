# Hall conductivity of the Haldane model against the chemical potential
import numpy as np
from pyqula import geometry

g = geometry.honeycomb_lattice()  # honeycomb lattice
h = g.get_hamiltonian(has_spin=False)  # Hamiltonian with first-neighbor hopping 1
h.add_haldane(0.1)  # Haldane coupling, it opens a gap of 0.9
mu = np.linspace(-3.3, 3.3, 201)  # chemical potentials
temperatures = [0.02, 0.1, 0.2]  # k_B T in units of the hopping
sigma_xy = []  # Hall conductivity in units of e^2/h, one curve per temperature
for T in temperatures:
    sigma_xy.append(h.get_anomalous_hall_conductivity(fermi=mu, T=T, nk=100))
