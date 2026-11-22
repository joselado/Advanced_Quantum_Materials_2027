# Magnon bands of a honeycomb ferromagnet on a ribbon with zigzag edges, with the position of each state
import numpy as np
from pyqula import geometry

nk = 201  # number of momenta
ks = np.linspace(0., 1., nk)  # momentum along the ribbon, in units of 2 pi over the period
kpath = [[k, 0., 0.] for k in ks]  # k-path from 0 to 2 pi
models = [(0.1, 0.), (-0.1, 0.), (0., 0.52), (0., 0.)]  # (DS, M), the Dzyaloshinskii-Moriya coupling and an onsite energy 2M on one sublattice

g = geometry.honeycomb_zigzag_ribbon(12)  # ribbon with zigzag edges, 48 sites across
energy, position = [], []  # one entry per model
for (DS, M) in models:
    h = g.get_hamiltonian(has_spin=False, tij=[-1.])  # magnon hopping -|J|S, with |J|S = 1
    h.add_haldane(-2*DS/np.sqrt(3))  # the Dzyaloshinskii-Moriya hopping, add_haldane(x) gives DS = -sqrt(3) x/2
    h.add_sublattice_imbalance(M)  # onsite energy +M on one sublattice and -M on the other
    h.add_onsite(3. + M)  # the onsite energy 3|J|S of the bulk, also on the sites of the edge, and M so that no energy is negative
    (ik, e, y) = h.get_bands(kpath=kpath, operator="yposition")  # bands with the position of each state
    energy.append(np.array(e).reshape(nk, -1))  # energy of band n at momentum k
    position.append(np.array(y).reshape(nk, -1))  # where each state sits across the ribbon
momentum = 2*np.pi*ks  # momentum times the period of the ribbon
width = g.y.max() - g.y.min()  # the edges are at y = -width/2 and width/2
