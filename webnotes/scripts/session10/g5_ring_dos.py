# The observable of Hamiltonian learning, the density of states of a disordered ring
import numpy as np
from pyqula import geometry, algebra

g = geometry.chain()  # chain with one site per cell
bins = np.linspace(-3.5, 3.5, 41)  # 40 bins of energy, in units of the hopping t
rng = np.random.default_rng(3)  # the disorder is random, and the seed fixes it
observables = {}  # the observable O for each second-neighbor hopping t2 and disorder strength W
for t2 in (0.05, 0.35):
    for W in (0.0, 0.7, 1.4):
        h = g.get_hamiltonian(has_spin=False, tij=[-1., -t2])  # matrix elements -t and -t2, with t=1
        h = h.set_finite_system(n=200, periodic=True)  # ring of 200 sites
        h.add_onsite(rng.uniform(-W, W, 200))  # onsite energy of each site, uniform in [-W, W], the hidden variable
        levels = np.linalg.eigvalsh(algebra.todense(h.intra).real)  # the 200 levels
        levels = np.round(levels, 8)  # a level that sits on a bin edge falls in the same bin at every run
        observables[(t2, W)] = np.histogram(levels, bins=bins)[0]/200  # fraction of the levels in each bin
