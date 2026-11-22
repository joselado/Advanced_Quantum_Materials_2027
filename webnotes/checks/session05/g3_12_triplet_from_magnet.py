"""Session 5, the numbers that page 12 (Section 5.12) quotes, checked again here in the order of the page.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here or
in the figure script that draws it. The bands of the figure spin_split_pairing and of the picture quiz come from the
pyqula script scripts/session05/g3_exchange_chain_bands.py, and figures/session05/_g3_spinbands.py asserts them against
eps(k) -+ h. This script asserts the same numbers with numpy, the sign of the exchange field of pyqula with the Bloch
Hamiltonian, which writes no file, the problem, the lab box (its sentences in the stored abstract, our reading of the
Pauli limit as about Delta/sqrt2 by two routes, and the Zeeman energy) and the try-it box. It finds the repository from
its own path and writes no file.

Run it from anywhere:  python3 webnotes/checks/session05/g3_12_triplet_from_magnet.py"""
import os, sys
sys.dont_write_bytecode = True
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
assert os.path.exists(os.path.join(REPO, 'webnotes', 'pages', 'session05'))

import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def kf(t, mu, h, s):
    """The Fermi momentum of the band -2t cos k - mu - s h, s = +1 for up and -1 for down, or None."""
    c = -(mu + s * h) / (2 * t)
    return float(np.arccos(c)) if abs(c) < 1 else None


# the key box: the exchange field -h(n_up - n_dn) of the page is add_exchange([0, 0, -h]) of pyqula, eps_up = eps - h
from pyqula import geometry
g = geometry.chain()
for hfield in (0.6, -1.2):
    H = g.get_hamiltonian(tij=[-1.])
    H.add_exchange([0., 0., -hfield])
    hk = H.get_hk_gen()
    ok = True
    for k in np.linspace(-0.5, 0.5, 11):
        m = hk([k, 0., 0.])
        eps = -2 * np.cos(2 * np.pi * k)
        ok = ok and abs(m[0, 0] - (eps - hfield)) < 1e-12 and abs(m[1, 1] - (eps + hfield)) < 1e-12 and abs(m[0, 1]) < 1e-12
    check(f'key box, h={hfield}: the up entry of pyqula is eps - h and the down entry eps + h, with no spin mixing', ok, True)

# the fold and the caption: t=1, mu=0, h=0.6
t, mu, h = 1.0, 0.0, 0.6
ku, kd = kf(t, mu, h, 1), kf(t, mu, h, -1)
check('fold and caption, k_F up = 1.875 and k_F down = 1.266', round(ku, 3) == 1.875 and round(kd, 3) == 1.266, (round(ku, 4), round(kd, 4)))
partner = -2 * t * np.cos(-ku) - mu + h
check('fold and caption, the down partner at -k_F up sits at 2h = 1.2', abs(partner - 1.2) < 1e-12, partner)
check('fold, eps(k_F up) = h', abs(-2 * t * np.cos(ku) - mu - h) < 1e-12, -2 * t * np.cos(ku) - mu)

# the first quiz: the up band -2t cos k - mu - h still has the bandwidth 4t, for mu inside and outside the band
k = np.linspace(-np.pi, np.pi, 2001)
for mu_q in (0.0, -1.5, 0.7, 3.0):
    band = -2 * t * np.cos(k) - mu_q - 0.6
    check(f'quiz, mu={mu_q}: the up band -2t cos k - mu - h in the field has the bandwidth 4t',
          abs(band.max() - band.min() - 4 * t) < 1e-12, band.max() - band.min())

# the picture quiz: mu = -1.5 t and h = 0.2, 1.2, -1.2
mu = -1.5
check('picture quiz, h=0.2: both bands cross, k_F up = 0.863 and k_F down = 0.555',
      round(kf(t, mu, 0.2, 1), 3) == 0.863 and round(kf(t, mu, 0.2, -1), 3) == 0.555, (kf(t, mu, 0.2, 1), kf(t, mu, 0.2, -1)))
ku02 = kf(t, mu, 0.2, 1)
mismatch = -2 * t * np.cos(-ku02) - mu + 0.2                      # the down band at -k_F up
check('picture quiz, h=0.2: the down partner at -k_F up of an up electron sits at the mismatch 2h = 0.4 t',
      abs(mismatch - 0.4) < 1e-12, mismatch)
# the bottoms of the bands from the Bloch Hamiltonian of pyqula, with add_onsite(-mu) for the mu of the page
kgrid = np.linspace(-0.5, 0.5, 401)                               # in units of 2 pi, k = 0 is on the grid
for hfield in (1.2, -1.2):
    H = g.get_hamiltonian(tij=[-1.])
    H.add_onsite(-mu)
    H.add_exchange([0., 0., -hfield])
    hk = H.get_hk_gen()
    up = np.array([hk([kk, 0., 0.])[0, 0].real for kk in kgrid])
    dn = np.array([hk([kk, 0., 0.])[1, 1].real for kk in kgrid])
    empty = dn if hfield > 0 else up
    full = up if hfield > 0 else dn
    check(f'picture quiz, h={hfield}: the bottom of the band that does not cross is 0.7 t above the Fermi level, from the pyqula bands',
          abs(empty.min() - 0.7) < 1e-12 and full.min() < 0 < full.max(), round(empty.min(), 12))
check('picture quiz, h=1.2: only the up band crosses, at k_F up = 1.420', round(kf(t, mu, 1.2, 1), 3) == 1.420 and kf(t, mu, 1.2, -1) is None,
      kf(t, mu, 1.2, 1))
check('picture quiz, h=-1.2: only the down band crosses, at k_F down = 1.420',
      kf(t, mu, -1.2, 1) is None and round(kf(t, mu, -1.2, -1), 3) == 1.420, True)

# the problem: t=1, mu=0, h=0.5
t, mu, h = 1.0, 0.0, 0.5
ku, kd = kf(t, mu, h, 1), kf(t, mu, h, -1)
check('problem, cos k_F up = -0.25 and cos k_F down = 0.25', abs(np.cos(ku) + 0.25) < 1e-12 and abs(np.cos(kd) - 0.25) < 1e-12, True)
check('problem, k_F up = 1.823, k_F down = 1.318, a difference of 0.505',
      round(ku, 3) == 1.823 and round(kd, 3) == 1.318 and round(ku - kd, 3) == 0.505, (round(ku, 4), round(kd, 4), round(ku - kd, 4)))
check('problem, the down partner at -k_F up has the energy 1.0 = 2h', abs(-2 * np.cos(-ku) + 0.5 - 1.0) < 1e-12, -2 * np.cos(-ku) + 0.5)

# the lab box, the source: the tracked file holds the arXiv abstract whole, with the factor 2 to 3, the violation over
# the whole superconducting phase, the re-entrant superconductivity and the suggestion, in separate sentences
src = ' '.join(open(os.path.join(REPO, 'webnotes', 'sources', 'session05', 'cao2021_s41586-021-03685-y.txt'),
                    encoding='utf-8').read().split())
check('lab box, the stored abstract states 10 T and a (2~3 times) violation of the Pauli limit of spin-singlet superconductors',
      'in-plane magnetic fields in excess of 10 T, which represents a large (2~3 times) violation of the Pauli limit for '
      'conventional spin-singlet superconductors' in src, 'found')
check('lab box, the stored abstract states the violation over the entire superconducting phase and re-entrant '
      'superconductivity at large magnetic fields',
      'the Pauli limit violation is observed over the entire superconducting phase' in src
      and 'we observe reentrant superconductivity at large magnetic fields' in src, 'found')
check('lab box, the stored abstract says "These findings suggest ... likely driven by a mechanism resulting in non-spin-singlet '
      'Cooper pairs"', 'These findings suggest that the superconductivity in MATTG is likely driven by a mechanism resulting in '
      'non-spin-singlet Cooper pairs' in src, 'found')

# the lab box, our reading: in BCS theory at zero temperature the singlet state loses to the polarized normal state when
# h reaches about Delta/sqrt2. First route: the mean field of an onsite attraction on the square lattice. For h < Delta
# the BdG levels are E_k +- h, all positive, so the ground energy of the singlet does not change with h, while the
# normal state gains energy from the polarization. Second route: a constant density of states N0 per spin, where the
# condensation energy N0 Delta^2/2 equals the polarization energy N0 h^2 at h = Delta/sqrt2.
def singlet(xi, U):
    """The self-consistent Delta and the ground energy per site sum_k (xi - E) - Delta^2/U of the onsite attraction U."""
    lo, hi = 1e-8, 2.0                                # the gap equation 1 = -U mean(1/2E) is monotonic in Delta
    for _ in range(60):
        D = 0.5 * (lo + hi)
        lo, hi = (D, hi) if -U * np.mean(1 / (2 * np.sqrt(xi ** 2 + D ** 2))) > 1 else (lo, D)
    D = 0.5 * (lo + hi)
    assert abs(-U * np.mean(1 / (2 * np.sqrt(xi ** 2 + D ** 2))) - 1) < 1e-9
    return D, np.mean(xi - np.sqrt(xi ** 2 + D ** 2)) - D ** 2 / U


def polarized(xi, h):
    """The ground energy per site of the normal state with the two spin bands xi -+ h."""
    return np.mean(np.minimum(xi - h, 0) + np.minimum(xi + h, 0))


def pauli(xi, U):
    """Delta and the field h_P where the polarized normal state reaches the energy of the singlet state."""
    D, Es = singlet(xi, U)
    lo, hi = 0.0, D                                   # polarized(xi, 0) > Es > polarized(xi, D) in weak coupling
    assert polarized(xi, lo) > Es > polarized(xi, hi)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if polarized(xi, mid) > Es else (lo, mid)
    return D, 0.5 * (lo + hi)


Lc = 200
kc = 2 * np.pi * np.arange(Lc) / Lc
KX, KY = np.meshgrid(kc, kc, indexing='ij')
for U, mu_c in ((-2.0, -1.0), (-1.5, -0.5)):
    D, hP = pauli((-2 * (np.cos(KX) + np.cos(KY)) - mu_c).ravel(), U)
    check(f'lab box, our reading, square lattice t=1, mu={mu_c}, U={U}: Delta={D:.4f}, and the Pauli field is about Delta/sqrt2',
          abs(hP / D - 1 / np.sqrt(2)) < 0.02, round(hP / D, 4))
xi_flat = np.linspace(-1, 1, 400001)                  # a constant density of states on (-1, 1)
D, hP = pauli(xi_flat, -0.4)
check(f'lab box, our reading, constant density of states, Delta={D:.4f}: the Pauli field is Delta/sqrt2',
      abs(hP / D - 1 / np.sqrt(2)) < 2e-3, round(hP / D, 5))

# the lab box, our conversion: h = mu_B B at 10 T with g = 2
mu_B = 5.7883818060e-5                     # eV/T, CODATA 2018
EZ = mu_B * 10 * 1e3
check('lab box, ours: mu_B B at 10 T is 0.58 meV', round(EZ, 2) == 0.58, round(EZ, 4))

# the try-it box: add_exchange([0,0,J]) of the notebook cell splits the bands of the chain by 2J, 2 for J=1 and 4 for J=2
for J in (1.0, 2.0):
    H = g.get_hamiltonian()
    H.add_exchange([0., 0., J])
    e = np.array([np.linalg.eigvalsh(H.get_hk_gen()([kk, 0., 0.])) for kk in np.linspace(-0.5, 0.5, 21)])
    check(f'try-it, J={J}: the two bands are {2 * J:.0f} apart at every momentum', np.allclose(e[:, 1] - e[:, 0], 2 * J, atol=1e-12), 2 * J)
# with the hopping +1 of the cell, the bands are 2 cos k +- J: for J=1 the Fermi momenta are 2 pi/3 and pi/3, for J=2 the
# Fermi level touches the two bands at their edges, k = pi and k = 0 (reported, the try-it text is left as it is)
k1 = (float(np.arccos(-1 / 2)), float(np.arccos(1 / 2)))
check('try-it, J=1: the Fermi momenta of the two spins are 2 pi/3 and pi/3', np.allclose(k1, (2 * np.pi / 3, np.pi / 3)), k1)
check('try-it, J=2: 2 cos k + 2 >= 0 and 2 cos k - 2 <= 0, both bands touch zero only at a band edge',
      (2 * np.cos(k) + 2).min() > -1e-12 and (2 * np.cos(k) - 2).max() < 1e-12, True)
