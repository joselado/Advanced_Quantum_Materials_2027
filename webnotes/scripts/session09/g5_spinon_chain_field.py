# A field on one site of a mean-field spinon chain, the moment that it induces around it
import numpy as np
from pyqula import geometry, algebra

N = 2000  # sites of the open chain
c = N//2  # the site of the field, far from both ends
field = 0.1  # the field h, which couples to S^z of site c, in units of the strong hopping
chis = [1.0, 0.6, 0.8, 0.9]  # the weak hopping chi_2 between the cells, 1.0 is the uniform chain
moments = {}  # the moment <S^z_n> on every site, for each chi_2
for chi2 in chis:
    h0 = geometry.bichain().get_hamiltonian(has_spin=False)  # one spinon species, hopping 1 inside each cell
    h0.inter = chi2*h0.inter  # hopping chi_2 between the cells
    h0 = h0.set_finite_system(n=N//2)  # open chain of N sites
    density = {}  # spinons per site, for each species
    for s in (1, -1):  # spin up and spin down
        h = h0.copy()  # the same chain
        v = np.zeros(N)  # onsite energy of each site
        v[c] = -s*field/2  # -h S^z gives -h/2 to the up spinons and +h/2 to the down ones
        h.add_onsite(v)  # the field on site c
        e, w = np.linalg.eigh(algebra.todense(h.intra).real)  # levels and states of the open chain
        density[s] = np.sum(w[:, e < 0]**2, axis=1)  # half filling, one spinon per site for the two species
    moments[chi2] = (density[1] - density[-1])/2  # the moment <S^z_n> = (n_up - n_down)/2
