# Berry curvature and Chern number of two gapped honeycomb lattices
from pyqula import geometry

g = geometry.honeycomb_lattice()  # honeycomb lattice

h = g.get_hamiltonian(has_spin=False)  # Hamiltonian with first-neighbor hopping 1
h.add_haldane(0.1)  # Haldane coupling, a gap that breaks time reversal
(kx, ky, omega_haldane) = h.get_berry_curvature(nk=120)  # Berry curvature of the filled band
chern_haldane = h.get_chern(nk=60)  # Chern number, it gives 1

h = g.get_hamiltonian(has_spin=False)  # the same lattice again
h.add_sublattice_imbalance(0.5)  # staggered potential, a gap that keeps time reversal
(kx, ky, omega_staggered) = h.get_berry_curvature(nk=120)  # Berry curvature of the filled band
chern_staggered = h.get_chern(nk=60)  # Chern number, it gives 0

print(chern_haldane, chern_staggered)
