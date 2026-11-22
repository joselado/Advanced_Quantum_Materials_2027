# Energy of the ferromagnet against the antiferromagnet of the half-filled Hubbard chain at large U, Section 6.5
import numpy as np
from pyqula import geometry

h = geometry.bichain().get_hamiltonian(tij=[-1.]) # two sites per cell, both spins, hopping -1 as in (6.1)
Us = np.array([6., 8., 10., 14., 20., 28., 40., 60.]) # interactions, in units of t
nk = 20 # cells of the k-mesh
e_fm, e_afm, m_fm, m_afm = [], [], [], [] # energies per cell of two sites, and the moments
for U in Us:
    seed = h.copy() # the guess of the ferromagnet
    seed.clean() # remove its hopping, keep only the field below
    seed.add_zeeman([0., 0., -U/2]) # the exchange field of the saturated ferromagnet, spin up below spin down
    (hf, ef) = h.get_mean_field_hamiltonian(U=U, mf=seed, nk=nk, mix=0.9, return_total_energy=True) # ferromagnet
    (ha, ea) = h.get_mean_field_hamiltonian(U=U, mf="antiferro", nk=nk, mix=0.9, return_total_energy=True) # Neel
    e_fm.append(ef)
    e_afm.append(ea)
    m_fm.append(hf.get_vev("mz", nk=nk)) # 1 on both sites, the saturated ferromagnet with spin up
    m_afm.append(ha.get_vev("mz", nk=nk)) # opposite moments on the two sites
difference = np.array(e_fm) - np.array(e_afm) # E_FM - E_AFM per cell of two sites
product = Us*difference # close to 4 t^2 at large U
