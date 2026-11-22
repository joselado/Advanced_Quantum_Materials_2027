# Magnon bands and Chern number of a honeycomb ferromagnet with a Dzyaloshinskii-Moriya term, in linear spin-wave theory
import numpy as np
from pyqula import geometry

DS = 0.1  # the Dzyaloshinskii-Moriya coupling D S, in units of |J|S
nodes = np.array([[0., 0., 0.], [1/3, 1/3, 0.], [0.5, 0., 0.], [0., 0., 0.]])  # Gamma, K, M, Gamma, in units of the reciprocal vectors
kpath = [nodes[i] + (nodes[i+1] - nodes[i])*j/100 for i in range(3) for j in range(100)] + [nodes[3]]  # 301 momenta

g = geometry.honeycomb_lattice()  # honeycomb lattice, bond length 1
h = g.get_hamiltonian(has_spin=False, tij=[-1.])  # magnon hopping -|J|S, with |J|S = 1
h.add_onsite(3.)  # the onsite energy z|J|S with z = 3, so that the lower band starts at zero
(k, e) = h.get_bands(kpath=kpath)  # the bands without the Dzyaloshinskii-Moriya term
bands_plain = np.array(e).reshape(-1, 2)  # the two bands at each momentum, they touch at K

h.add_haldane(-2*DS/np.sqrt(3))  # the Dzyaloshinskii-Moriya hopping, add_haldane(x) gives DS = -sqrt(3) x/2
(k, e) = h.get_bands(kpath=kpath)  # the magnon bands with the Dzyaloshinskii-Moriya term
bands = np.array(e).reshape(-1, 2)  # the two bands at each momentum, with a gap at K
h.set_filling(0.5)  # zero energy moved into the gap, with the lower band below it
chern = h.get_chern()  # Chern number of the lower magnon band
