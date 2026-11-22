# Fermi surface of the square lattice at three chemical potentials, Section 9.4b
import numpy as np
from pyqula import geometry

g = geometry.square_lattice()  # square lattice, lattice constant 1
mus = [0., -1., -3.]  # chemical potentials, in units of t
nk = 81  # points per side of the window, which goes from -2 pi to 2 pi
maps = []  # the spectral weight at the Fermi level for each mu
for mu in mus:
    h = g.get_hamiltonian(has_spin=False, tij=[-1.])  # spinless, the band -2t(cos kx + cos ky) with t=1
    h.add_onsite(-mu)  # every energy goes down by mu, so the Fermi level at zero is mu
    (kx, ky, w) = h.get_fermi_surface(e=0., delta=0.1, nk=nk)  # weight of the states at the Fermi level
    maps.append(np.array(w))
kx, ky = np.array(kx), np.array(ky)  # momenta in units of 2 pi, both ends of the window included
