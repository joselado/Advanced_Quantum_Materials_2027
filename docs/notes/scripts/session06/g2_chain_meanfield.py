# Mean field of the Hubbard chain at U=4t, Sections 6.4 and 6.5
# a ferromagnet at n=0.2 with one site per cell, and an antiferromagnet at half filling with two
import numpy as np
from pyqula import geometry

U = 4. # Hubbard interaction, in units of t
ks = np.linspace(-np.pi, np.pi, 241) # momentum along the chain, in units of the inverse lattice constant

h1 = geometry.chain().get_hamiltonian(tij=[-1.]) # one site per cell, both spins, hopping -1 as in (6.1)
seed = h1.copy() # the guess of the loop
seed.clean() # remove its hopping, keep only the field below
seed.add_zeeman([0., 0., -0.1]) # a small field that favors spin up
hfm = h1.get_mean_field_hamiltonian(U=U, filling=0.1, mf=seed, mix=0.9, nk=300) # filling=0.1 is n=0.2
m_fm = hfm.get_vev("mz", nk=300)[0] # n_up - n_dn, which is n=0.2 when only spin up is filled
onsite = np.real(np.diag(hfm.intra)) # onsite energies of spin up and spin down
splitting = onsite[1] - onsite[0] # the exchange splitting U m
hk1 = hfm.get_hk_gen() # Bloch Hamiltonian, energies measured from the Fermi level
bands_fm = np.array([np.real(np.diag(hk1([k/(2*np.pi), 0., 0.]))) for k in ks]) # spin up and spin down

h2 = geometry.bichain().get_hamiltonian(tij=[-1.]) # the same chain with two sites per cell
haf = h2.get_mean_field_hamiltonian(U=U, mf="antiferro", mix=0.9, nk=200) # half filling, the default
m_afm = haf.get_vev("mz", nk=200) # n_up - n_dn on the two sites, with opposite signs
gap = haf.get_gap() # the gap at the Fermi level, U|m|
hk0 = h2.get_hk_gen() # Bloch Hamiltonian at U=0, the cell is two sites long
hk2 = haf.get_hk_gen() # Bloch Hamiltonian of the antiferromagnet
bands_pm = np.array([np.linalg.eigvalsh(hk0([k/np.pi, 0., 0.])) for k in ks]) # U=0, two bands that cross
bands_afm = np.array([np.linalg.eigvalsh(hk2([k/np.pi, 0., 0.])) for k in ks]) # the gapped bands
