# d-wave pairing on the square lattice, its sign over the zone and its nodes on the Fermi surface, Section 5.13
import numpy as np
from pyqula import geometry

g = geometry.square_lattice()  # square lattice with one site per cell
h = g.get_hamiltonian(tij=[-1.])  # two spins, the band -2t (cos kx + cos ky) with t=1
h.add_onsite(1.0)  # chemical potential mu=-t
h.setup_nambu_spinor()  # Nambu spinor, with no pairing yet
hs = h.copy()  # the same metal, for s-wave pairing
h.add_pairing(mode="dx2y2", delta=0.1)  # d-wave pairing, Delta_0 = 2 delta = 0.2
hs.add_swave(0.2)  # s-wave pairing of the same size, Delta = 0.2
hk, hks = h.get_hk_gen(), hs.get_hk_gen()  # BdG Hamiltonians, the momentum in units of 2 pi
ks = np.linspace(-0.5, 0.5, 101)  # momenta along each axis
pairing = np.array([[hk([kx, ky, 0.])[0, 2].real for ky in ks] for kx in ks])  # Delta_d(k), first index along kx
band = np.array([[hk([kx, ky, 0.])[0, 0].real for ky in ks] for kx in ks])  # eps(k), the Fermi surface is band=0
thetas = np.linspace(0., 2*np.pi, 73)  # directions from Gamma, every 5 degrees
rs = np.linspace(0., 0.5, 2001)  # distance from Gamma along each direction, in units of 2 pi
rays = [[[r*np.cos(a), r*np.sin(a), 0.] for r in rs] for a in thetas]  # the momenta of each direction
smallest_d = np.array([np.abs(np.linalg.eigvalsh(np.array([hk(k) for k in ray]))).min() for ray in rays])
smallest_s = np.array([np.abs(np.linalg.eigvalsh(np.array([hks(k) for k in ray]))).min() for ray in rays])
