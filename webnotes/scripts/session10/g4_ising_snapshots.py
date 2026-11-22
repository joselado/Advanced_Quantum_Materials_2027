# Snapshots of the Ising model (10.9) on a 16 x 16 lattice from Monte Carlo, Sections 10.6a and 10.6b
import numpy as np
from pyqula import geometry
from pyqula.latticeising import LatticeIsing

g = geometry.square_lattice().get_supercell(16)  # square lattice of 16 x 16 sites, periodic
n = len(g.r)  # 256 spins, and one sweep is n attempted flips
temps = [1.5, 2.27, 3.5]  # k_B T in units of J, below, at and above T_c = 2.27 J
absm = {}  # |m| of 1000 snapshots at each temperature
for T in temps:
    model = LatticeIsing(g, m=1.)  # classical spins +1 and -1 on the sites, all up
    model.add_interaction(Jij=[0.5])  # first neighbors, the J=1 of (10.9), since pyqula counts every bond twice
    np.random.seed(1)  # the Metropolis updates are random, and this fixes them
    (es, ms) = model.optimize_energy(temp=T, ntries=n*2500)  # 2500 sweeps of single flips of Metropolis
    absm[T] = np.abs(ms[n*500::n*2])/n  # |m| every two sweeps, after 500 sweeps to thermalize
