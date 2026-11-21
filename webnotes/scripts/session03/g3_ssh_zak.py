# Zak phase of the SSH chain and levels of the open chain, against the intracell hopping, Section 3.9c
import numpy as np
from pyqula import geometry, topology

ts = np.linspace(0., 2., 41) # intracell hopping, the intercell hopping is 1
N = 20 # number of unit cells of the open chain
g = geometry.bichain() # create the chain, with two sites per unit cell

zak_phase = [] # Zak phase of the lower band
gap = [] # gap of the infinite chain
end_level = [] # level of the open chain closest to zero
for t in ts:
    h = g.get_hamiltonian(has_spin=False) # create the Hamiltonian
    h.intra = t*h.intra # intracell hopping t
    gap.append(h.get_gap()) # compute the gap, it closes at t=1
    if gap[-1] > 1e-6: zak_phase.append(topology.berry_phase(h, nk=100)) # Berry phase across the zone
    else: zak_phase.append(np.nan) # no Zak phase without a gap
    hf = h.set_finite_system(n=N) # open chain of N cells
    end_level.append(np.min(np.abs(hf.get_bands()[1]))) # smallest |E| of the open chain
zak_phase = np.abs(zak_phase) # the phase is defined modulo 2 pi, so pi and -pi are the same
