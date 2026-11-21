# Gap and Chern number of the Haldane model along three deformations, Section 3.7
import numpy as np
from pyqula import geometry

g = geometry.honeycomb_lattice()  # honeycomb lattice
h = g.get_hamiltonian(has_spin=False)  # Hamiltonian with first-neighbor hopping 1
h.add_haldane(0.1)  # Haldane coupling, a gap that breaks time reversal
gap_haldane = h.get_gap()  # gap of the Haldane coupling alone, it gives 0.9
m_closing = gap_haldane/2  # staggered potential where the gap closes

m_start = [0., 0., 1.2*m_closing]  # staggered potential at the start of each deformation
m_end = [0.8*m_closing, 2*m_closing, 2*m_closing]  # staggered potential at its end
lambdas = np.linspace(0., 1., 11)  # parameter of the deformation
gaps = []  # gap along each deformation
cherns = []  # Chern number at the two ends of each deformation
for (m0, m1) in zip(m_start, m_end):
    gap = []
    chern = []
    for lam in lambdas:
        h = g.get_hamiltonian(has_spin=False)  # the same lattice again
        h.add_haldane(0.1)  # Haldane coupling
        h.add_sublattice_imbalance(m0 + lam*(m1 - m0))  # staggered potential
        gap.append(h.get_gap())  # gap of the bulk
        if lam in [0., 1.]: chern.append(h.get_chern(nk=30))  # Chern number at the two ends
    gaps.append(np.array(gap))
    cherns.append(np.array(chern))

print(np.round(gaps, 2), np.round(cherns, 2))
