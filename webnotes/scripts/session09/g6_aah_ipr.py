# Mean inverse participation ratio of the Aubry-Andre ring against the strength of the potential, Section 9.10a
import numpy as np
from pyqula import geometry

g = geometry.chain()  # chain with one site per cell
h0 = g.get_hamiltonian(has_spin=False, tij=[-1.])  # spinless, hopping -t with t=1
sizes = [55, 233, 987]  # rings with a Fibonacci number of sites
qs = [34/55, 144/233, 610/987]  # ratios of two Fibonacci numbers, close to (sqrt(5)-1)/2
phi = 0.3  # phase of the potential
V0s = np.linspace(0., 4., 41)  # strengths of the potential, in units of t
ipr = np.zeros((len(sizes), len(V0s)))  # mean IPR, one row per ring
for (i, N) in enumerate(sizes):
    ring = h0.set_finite_system(n=N, periodic=True)  # ring of N sites
    for (j, V0) in enumerate(V0s):
        h = ring.copy()  # the clean ring
        h.add_onsite(V0*np.cos(2*np.pi*qs[i]*np.arange(N) + phi))  # quasiperiodic onsite energy
        (energies, iprs) = h.get_ipr()  # the IPR of every eigenstate
        ipr[i, j] = np.mean(iprs)  # its mean over all the eigenstates

print(sizes[2]*ipr[2, 10])  # N times the IPR at V0=t, about 2 for the real eigenvectors of this ring, 1 for a plane wave
