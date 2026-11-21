# The ring of five sites, with and without a second-neighbor hopping, Section 2.4
import numpy as np
from pyqula import geometry

t2 = 0.8  # second-neighbor hopping, in units of the first-neighbor hopping t
g = geometry.chain().get_supercell(5)  # a chain with five sites per cell, at k=0 it is a ring of five sites

h = g.get_hamiltonian(has_spin=False, tij=[-1.0])  # first-neighbor hopping -t, the sign of the notes
ring_first = h.get_hk_gen()([0., 0., 0.])  # the Bloch Hamiltonian at k=0, the matrix of the ring
levels_first = np.linalg.eigvalsh(ring_first)  # the five levels of the ring

h = g.get_hamiltonian(has_spin=False, tij=[-1.0, -t2])  # first-neighbor hopping -t and second-neighbor hopping -t2
ring_second = h.get_hk_gen()([0., 0., 0.])  # the matrix of the ring with the second-neighbor hopping
levels_second = np.linalg.eigvalsh(ring_second)  # the five levels of this ring
