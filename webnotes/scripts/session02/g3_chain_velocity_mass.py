# Band, group velocity and inverse effective mass of the chain
import numpy as np
from pyqula import geometry

g = geometry.chain()  # chain with one site per cell, a = 1
h = g.get_hamiltonian(has_spin=False, tij=[-1.0])  # first-neighbor hopping -1, the sign of (2.5)
ks = np.linspace(-0.5, 0.5, 801)  # momentum in units of 2 pi, one zone
(ik, e) = h.get_bands(kpath=[[k, 0., 0.] for k in ks])  # the band, one energy per momentum
phi = 2*np.pi*ks  # the Bloch phase, from -pi to pi
velocity = np.gradient(e, phi, edge_order=2)  # the slope of the band, (2.17) in units of t a/hbar
inverse_mass = np.gradient(velocity, phi, edge_order=2)  # the curvature, (2.18) in units of t a^2/hbar^2
