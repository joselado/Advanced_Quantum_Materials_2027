# Landau levels of the square lattice as flat bands, and the Hall conductivity that counts them
import numpy as np
from pyqula import geometry

kx = np.linspace(-0.5, 0.5, 121)  # momentum along x in units of 2 pi, at ky = 0
bands, levels, sigma_xy = {}, {}, {}  # results for each flux 1/q
for q in (10, 20, 40):  # plaquettes per flux quantum
    g = geometry.square_lattice().get_supercell((1, q))  # magnetic cell of q sites along y
    h = g.get_hamiltonian(has_spin=False, tij=[-1.])  # spinless, first-neighbor hopping -1
    h.add_orbital_magnetic_field(1/q)  # flux 1/q per plaquette, one flux quantum through the cell
    hk = h.get_hk_gen()  # Bloch Hamiltonian, the momentum in units of the reciprocal vectors
    bands[q] = np.array([np.linalg.eigvalsh(hk([k, 0., 0.])) for k in kx])  # bands against kx
    levels[q] = bands[q].mean(axis=0)  # the energy of each band
    nlevels = np.sum(levels[q] < -2.)  # number of levels below the energy -2
    sigma_xy[q] = [0.]  # Hall conductivity in units of e^2/h, below the lowest level
    for n in range(nlevels):
        hf = h.copy()  # the same Hamiltonian
        hf.add_onsite(-(levels[q][n] + levels[q][n+1])/2)  # zero of energy in the gap above level n
        sigma_xy[q].append(hf.get_chern(nk=20))  # Chern number of the filled levels, it gives n + 1
