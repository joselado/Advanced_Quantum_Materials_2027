# A vacancy in honeycomb insulators on a torus, the local density of states next to it
import numpy as np
from pyqula import geometry, algebra

g = geometry.honeycomb_lattice().get_supercell(18)  # torus of 18 x 18 cells, 648 sites, no edges
v = np.argmin(np.sum((g.r - np.mean(g.r, axis=0))**2, axis=1))  # the site that we remove, close to the center
keep = np.array([i != v for i in range(len(g.r))])  # every site but the vacancy
energies = np.linspace(-1.6, 1.6, 801)  # energies in units of the first-neighbor hopping t
eta = 0.03  # broadening of each level
models = {"chern": (0.3/np.sqrt(3), 0.), "trivial": (0., 0.78), "both": (0.3/np.sqrt(3), 1.)}  # add_haldane and M
ldos, ldos_clean, levels, weights, gaps = {}, {}, {}, {}, {}
for name, (x, M) in models.items():
    h = g.get_hamiltonian(has_spin=False)  # first-neighbor hopping 1
    h.add_haldane(x)  # second-neighbor hopping t2 = (sqrt(3)/2) x, so 0.15 or 0
    h.add_sublattice_imbalance(M)  # onsite energy +M on one sublattice and -M on the other
    hv = h.copy()  # the same torus
    hv.remove_sites(keep)  # with the vacancy
    H = algebra.todense(h.get_hk_gen()([0., 0., 0.]))  # the clean torus, each hopping with its periodic image
    Hv = algebra.todense(hv.get_hk_gen()([0., 0., 0.]))  # the torus with the vacancy
    nbr = np.where((np.abs(np.abs(H[v]) - 1.) < 1e-9) & (np.arange(len(H)) != v))[0]  # the three first neighbors of the vacancy, not the vacancy itself
    e0, w0 = np.linalg.eigh(H)  # levels and states without the vacancy
    e, w = np.linalg.eigh(Hv)  # levels and states with the vacancy
    gaps[name] = e0[e0 > 0].min() - e0[e0 < 0].max()  # the bulk gap
    levels[name], weights[name] = e, np.sum(np.abs(w[nbr - (nbr > v)])**2, axis=0)  # weight on the neighbors
    lor = eta/np.pi/((energies[:, None] - e[None, :])**2 + eta**2)  # a Lorentzian for each level
    ldos[name] = lor @ weights[name]  # LDOS summed on the three neighbors
    lor0 = eta/np.pi/((energies[:, None] - e0[None, :])**2 + eta**2)  # the same without the vacancy
    ldos_clean[name] = lor0 @ np.sum(np.abs(w0[nbr])**2, axis=0)
