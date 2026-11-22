# One mechanism for two gaps on a chain, the Kondo lattice (8.21) and an s-wave superconductor
import numpy as np
from pyqula import geometry
from pyqula.specialhamiltonian import H2HFH

nk = 201  # number of momenta
kpath = [[k, 0., 0.] for k in np.linspace(-0.5, 0.5, nk)]  # momentum from -pi to pi, in units of 2 pi
gamma, delta = 0.6, 0.5  # the hybridization gamma_K and the pairing Delta, in units of the hopping t
kondo, swave = [], []  # bands without and with the mixing, the four energies at each momentum
for x in [0., gamma]:
    h = geometry.chain().get_hamiltonian(tij=[-1.])  # hopping -t with t=1, the band -2t cos k, two spins
    h = H2HFH(h, JK=x)  # one f site per site with its level at zero, mixed with c by the hopping JK
    (ik, e) = h.get_bands(kpath=kpath)  # bands of c and f
    kondo.append(np.array(e).reshape(nk, -1))  # energy of band n at momentum i, sorted
for x in [0., delta]:
    h = geometry.chain().get_hamiltonian(tij=[-1.])  # the same chain, half filled at zero energy
    h.add_swave(x)  # Nambu spinor and s-wave pairing Delta
    (ik, e) = h.get_bands(kpath=kpath)  # Bogoliubov-de Gennes bands of electrons and holes
    swave.append(np.array(e).reshape(nk, -1))  # energy of band n at momentum i, sorted
gap_kondo = kondo[1][:, 2].min() - kondo[1][:, 1].max()  # indirect gap, 2(sqrt(t^2+gamma^2)-t)
gap_swave = swave[1][:, 2].min() - swave[1][:, 1].max()  # gap of the superconductor, 2 Delta
