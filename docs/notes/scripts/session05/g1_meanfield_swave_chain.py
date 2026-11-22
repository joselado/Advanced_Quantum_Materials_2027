# Self-consistent s-wave pairing of the attractive Hubbard chain, Section 5.5
# for the pyqula of GitHub, whose loop keeps the density at filling=0.1
import numpy as np
from pyqula import geometry

g = geometry.chain() # chain with one site per cell
h = g.get_hamiltonian(tij=[-1.]) # Hamiltonian with the two spins, hopping -1, the sign of (5.2) with t=1
h.setup_nambu_spinor() # Nambu spinor, with no pairing yet
Us = [-0.75, -1.0, -1.25, -1.5, -1.75, -2.0] # attractive interactions U, in units of t
ks = np.linspace(-0.5, 0.5, 801) # momenta across the zone, in units of 2 pi
deltas = [] # the pairing Delta = U <c_dn c_up> for each U
smallest = [] # the smallest quasiparticle energy for each U
bands = [] # the BdG energies along ks for each U
for U in Us:
    hscf = h.get_mean_field_hamiltonian(U=U, filling=0.1, nk=100, mix=0.5, mf="swave") # 0.2 electrons per site
    deltas.append(abs(hscf.intra[0, 2])) # |Delta|, an energy
    hk = hscf.get_hk_gen() # BdG Hamiltonian as a function of the momentum
    e = np.array([np.linalg.eigvalsh(hk([k, 0., 0.])) for k in ks]) # the four BdG bands
    bands.append(e)
    smallest.append(np.min(np.abs(e)))
deltas = np.array(deltas)
smallest = np.array(smallest)
