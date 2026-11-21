# Berry curvature of three gapped honeycomb lattices
from pyqula import geometry

g = geometry.honeycomb_lattice()  # honeycomb lattice

h = g.get_hamiltonian(has_spin=False)  # Hamiltonian with first-neighbor hopping 1
h.add_sublattice_imbalance(0.5)  # staggered potential
(kx, ky, omega_staggered) = h.get_berry_curvature(nk=90)  # Berry curvature of the filled band
chern_staggered = h.get_chern(nk=60)  # Chern number

h = g.get_hamiltonian(has_spin=False)
h.add_haldane(-0.1)  # Haldane coupling with the opposite sign
(kx, ky, omega_haldane) = h.get_berry_curvature(nk=90)
chern_haldane = h.get_chern(nk=60)

h = g.get_hamiltonian(has_spin=False)
h.add_haldane(0.1)  # Haldane coupling
h.add_sublattice_imbalance(0.8)  # and a larger staggered potential
(kx, ky, omega_both) = h.get_berry_curvature(nk=90)
chern_both = h.get_chern(nk=60)

print(chern_staggered, chern_haldane, chern_both)
