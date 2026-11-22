# Static Lindhard function of the square lattice over the zone of q, Section 9.4b
import numpy as np
from pyqula import geometry

g = geometry.square_lattice()  # square lattice, lattice constant 1
T = 0.1  # temperature, in units of t
n = 20  # points of q per side of the zone
nk = 31  # points of the k-mesh per side, odd for the nesting vector (1/2, 1/2)
qs = [(i/n, j/n) for i in range(n//2 + 1) for j in range(i + 1)]  # q in units of 2 pi, with 0 <= qy <= qx <= 1/2
mus = [-3., 0.]  # chemical potentials, low filling and half filling
chi = []  # chi_0(q) for each mu, at the points qs
for mu in mus:
    h = g.get_hamiltonian(has_spin=False, tij=[-1.])  # spinless, the band -2t(cos kx + cos ky) with t=1
    h.add_onsite(-mu)  # every energy goes down by mu, so the Fermi level at zero is mu
    c = [h.get_chi(energies=[0.], q=[qx, qy, 0.], nk=nk, delta=1e-3, T=T, integration="triangle")[1][0]
         for (qx, qy) in qs]  # static response, with the bands interpolated in the triangles of the k-mesh
    chi.append(-np.real(c))  # minus the result of pyqula is the Lindhard function (9.4), positive
ratio = chi[1][-1]/chi[1][0]  # chi_0(pi,pi)/chi_0(0) at half filling
