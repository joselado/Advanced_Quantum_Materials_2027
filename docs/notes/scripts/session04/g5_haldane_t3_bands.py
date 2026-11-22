# Bands and Chern numbers of three honeycomb lattices at zero field, Section 4.20
import numpy as np
from pyqula import geometry

# (t2, phi, t3, M): second-neighbor hopping t2 exp(i phi), third-neighbor hopping t3, staggered potential M
models = [(0.1, np.pi/2, 0., 0.), # the Haldane model with t2 = 0.1, a dispersive band with C = 1
          (0.3, 0.4*np.pi, -0.2, 0.), # a flat band with C = 1
          (0.2, 0., 0., 1.5)] # real hoppings and a staggered potential, a flat band with C = 0
nodes = np.array([[0., 0., 0.], [1/3, 1/3, 0.], [0.5, 0., 0.], [0., 0., 0.]]) # Gamma, K, M, Gamma, in reduced units
kpath = [nodes[i] + (nodes[i+1] - nodes[i])*j/100 for i in range(3) for j in range(100)] + [nodes[3]] # 301 momenta
ks = np.arange(48)/48 # k-mesh of the zone, a multiple of 3 holds K and K'
bands, width, gap, chern = [], [], [], [] # one entry per model
for (t2, phi, t3, M) in models:
    g = geometry.honeycomb_lattice() # honeycomb lattice, bond length 1
    h = g.get_hamiltonian(has_spin=False, tij=[1., t2*np.cos(phi), t3]) # first, second and third-neighbor hoppings
    h.add_haldane(2*t2*np.sin(phi)/np.sqrt(3)) # imaginary second-neighbor hopping t2 sin(phi), pyqula takes it times 2/sqrt(3)
    h.add_sublattice_imbalance(M) # onsite energy +M on one sublattice and -M on the other
    hk = h.get_hk_gen() # Bloch Hamiltonian
    bands.append(np.array([np.linalg.eigvalsh(hk(k)) for k in kpath])) # the two bands along the path
    e = np.array([np.linalg.eigvalsh(hk([kx, ky, 0.])) for kx in ks for ky in ks]) # the two bands on the k-mesh
    width.append(e[:, 0].max() - e[:, 0].min()) # width of the lower band
    gap.append(e[:, 1].min() - e[:, 0].max()) # gap between the two bands
    chern.append(h.get_chern(nk=40)) # Chern number of the states below zero energy, the lower band here
