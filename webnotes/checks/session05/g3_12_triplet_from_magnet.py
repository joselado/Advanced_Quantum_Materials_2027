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

# decided on 2026-11-22 and corrected after the independent check of the same day, the text: "The pairing that survives is
# spin-triplet once the exchange field is of the order of the smallest quasiparticle energy of the singlet, or when only one spin
# band crosses the Fermi level." The singlet part of this, on a chain with t=1, mu=0.5 and an onsite attraction U=-2, which has
# no triplet channel. The mean-field energy per site of a uniform singlet Delta, with zero pair momentum, in the field h is
# mean_k[xi - max(E, |h|)] - Delta^2/U, with E = sqrt(xi^2 + Delta^2), since the BdG levels are +-E +- h. First route, this
# formula against the 4x4 BdG matrix of the spinor (5.6), with the exchange -h sigma_z in both blocks, at a few momenta. Second
# route, the minimum over Delta: it is at Delta > 0 for h = 0.5 h_P, and at Delta = 0 for h = 1.2 h_P and 2 h_P, with h_P about
# Delta_0/sqrt2, and for h = 2, where only the spin-down band crosses the Fermi level (the up band lies in (-4.5, -0.5)). A
# singlet with a pair momentum q is not covered by this assert: in this onsite model it still lowers the energy at 1.2 h_P (by
# 5.3e-4 per site at q=0.3), so "gone" here means the uniform singlet. The triplet part is the bond model below.
def E_singlet(xi, U, D, h):
    return np.mean(xi - np.maximum(np.sqrt(xi ** 2 + D ** 2), abs(h))) - D ** 2 / U


def E_bdg(xi, U, D, h):
    """The same energy from the 4x4 BdG matrices, E0 = (1/2) Tr h_e - (1/2) sum of the positive levels, plus -Delta^2/U."""
    out = 0.0
    for x in xi:
        he = np.diag([x - h, x + h])
        m = np.block([[he, D * np.eye(2)], [D * np.eye(2), np.diag([-x - h, -x + h])]])
        e = np.linalg.eigvalsh(m)
        out += 0.5 * np.trace(he) - 0.5 * e[e > 0].sum()
    return out / len(xi) - D ** 2 / U


kch = 2 * np.pi * np.arange(400) / 400
xi_ch = -2 * np.cos(kch) - 0.5
U_ch = -2.0
check('text, the singlet energy in a field: the formula mean[xi - max(E,|h|)] - Delta^2/U equals the 4x4 BdG matrices',
      all(abs(E_singlet(xi_ch[::10], U_ch, D_, h_) - E_bdg(xi_ch[::10], U_ch, D_, h_)) < 1e-12
          for D_, h_ in ((0.3, 0.1), (0.3, 0.5), (0.0, 0.4), (0.6, 2.0))), 'ok')
D0, hP_ch = pauli(xi_ch, U_ch)
Dgrid = np.linspace(0, 2 * D0, 801)
best = {}
for name, h_ in (('0.5 h_P', 0.5 * hP_ch), ('1.2 h_P', 1.2 * hP_ch), ('2 h_P', 2 * hP_ch), ('h=2', 2.0)):
    best[name] = Dgrid[np.argmin([E_singlet(xi_ch, U_ch, D_, h_) for D_ in Dgrid])]
up_band = (xi_ch - 2.0).min(), (xi_ch - 2.0).max()
dn_band = (xi_ch + 2.0).min(), (xi_ch + 2.0).max()
check(f'text, chain t=1, mu=0.5, onsite U=-2: Delta_0={D0:.3f} and h_P={hP_ch:.3f}, about Delta_0/sqrt2; the uniform singlet '
      '(zero pair momentum) survives at 0.5 h_P and is gone at 1.2 h_P, at 2 h_P and at h=2, where only the spin-down band crosses '
      'the Fermi level',
      abs(hP_ch / D0 - 1 / np.sqrt(2)) < 0.03 and abs(D0 - 0.351) < 5e-4 and abs(hP_ch - 0.250) < 5e-4 and best['0.5 h_P'] > 0.9 * D0 and best['1.2 h_P'] == 0 and best['2 h_P'] == 0
      and best['h=2'] == 0 and up_band[1] < 0 and dn_band[0] < 0 < dn_band[1],
      {k_: round(v_, 4) for k_, v_ in best.items()})


# the same onsite model with a pair momentum q, Delta e^{iqn} c+_nup c+_ndn: the block (c_{k+q/2 up}, c+_{-k+q/2 dn}) with the
# self-consistency Delta = -U mean_k <c_{k+q/2 up} c_{-k+q/2 dn}>, and the energy sum_{E<0} E + sum eps_dn - Delta^2/U per site
def onsite_q(mu, h, U, q, Nk=4000, D=0.3):
    kq = 2 * np.pi * (np.arange(Nk) + 0.5) / Nk
    a, b = -2 * np.cos(kq + q / 2) - mu - h, -2 * np.cos(-kq + q / 2) - mu + h
    for _ in range(3000):
        Hq = np.zeros((Nk, 2, 2)); Hq[:, 0, 0] = a; Hq[:, 1, 1] = -b; Hq[:, 0, 1] = Hq[:, 1, 0] = D
        E, V = np.linalg.eigh(Hq)
        new = -U * np.mean(np.sum(V[:, 0, :] * V[:, 1, :] * (E > 0), axis=1))
        err, D = abs(new - D), 0.5 * (new + D)
        if err < 1e-11:
            break
    e0 = -2 * np.cos(kq) - mu
    En = np.mean(np.minimum(e0 - h, 0) + np.minimum(e0 + h, 0))
    return D, np.mean(np.sum(np.where(E < 0, E, 0), axis=1)) + np.mean(b) - D ** 2 / U - En, err


Dq, dEq, errq = onsite_q(0.5, 1.2 * hP_ch, U_ch, 0.3)
check('check comment, onsite U=-2 at 1.2 h_P: a singlet with the pair momentum q=0.3 is below the normal state by about 5.3e-4 per site',
      errq < 1e-10 and Dq > 0.1 and abs(dEq + 5.3e-4) < 2e-5, (round(Dq, 4), '%.2e' % dEq))

# the triplet part, on the model of the page: the bond attraction U sum_<ij> sum_ss' c+_is c+_js' c_js' c_is, decoupled in the
# pairing channel only, D[s,s'] = U <c_{n+1 s'} c_{n s}>, with eps_up,dn = -2t cos k - mu -+ h. Route 1, the 4x4 BdG of
# (c_kup, c_kdn, c+_-kup, c+_-kdn), started from random D, with its energy in two forms, (1/2) sum_{E<0} E + (1/2) sum Tr xi +
# sum |D|^2/|U| and <kinetic> + U sum |<P>|^2. Route 2, the sectors: opposite spins in (c_{k+q/2 up}, c+_{-k+q/2 dn}), also with a
# pair momentum q, and one spin in (c_ks, c+_-ks). On mu=-1.6, cos k_F = 0.8, where the bond singlet 2D cos k is the strong one.
# Weak attraction |U|=1.5: at h=0 every start gives the pure singlet, with the smallest quasiparticle energy 0.2875, and also at
# h=0.1, 0.35 times it, while at h=0.3, 1.04 times it and with both spin bands crossing the Fermi level, every start gives the
# pure equal-spin triplet. So the pairing changes at a field of the order of this energy, and below the gap 2 x 0.2875. Strong attraction
# |U|=3 at h=0.6: only the up band crosses (the down band starts at 0.2), every start gives the pure up-up triplet, and every
# opposite-spin state with q from 0 to 1.6 lies above it.
def bond_route1(mu, h, U, D, Nk=1000):
    kb = 2 * np.pi * (np.arange(Nk) + 0.5) / Nk
    e = -2 * np.cos(kb) - mu
    ph = np.exp(1j * kb)[:, None, None]
    H = np.zeros((Nk, 4, 4), complex)
    H[:, 0, 0], H[:, 1, 1], H[:, 2, 2], H[:, 3, 3] = e - h, e + h, -(e - h), -(e + h)
    D = np.array(D, complex)
    for _ in range(4000):
        Dk = D[None] * ph - D.T[None] / ph
        H[:, :2, 2:] = Dk; H[:, 2:, :2] = np.conj(np.transpose(Dk, (0, 2, 1)))
        E, V = np.linalg.eigh(H)
        Pp = np.einsum('kin,kjn,kn->kij', V, V.conj(), (E > 0).astype(float))
        Pair = np.mean(ph * np.transpose(Pp[:, :2, 2:], (0, 2, 1)), axis=0)          # <c_{n+1 s'} c_{n s}>[s, s']
        err = np.abs(U * Pair - D).max()
        D = 0.6 * U * Pair + 0.4 * D
        if err < 1e-10:
            break
    En = np.mean(np.minimum(e - h, 0) + np.minimum(e + h, 0))
    E1 = 0.5 * np.mean(np.sum(np.where(E < 0, E, 0), axis=1)) + np.mean(e) + np.sum(np.abs(D) ** 2) / abs(U)
    n = 1 - np.real(np.einsum('kii->ki', Pp[:, :2, :2]))
    E2 = np.mean((e - h) * n[:, 0] + (e + h) * n[:, 1]) + U * np.sum(np.abs(Pair) ** 2)
    return D, E1 - En, E2 - En, np.abs(E).min(), err


def bond_opp(mu, h, U, Dud, Ddu, q=0.0, Nk=1000):
    kb = 2 * np.pi * (np.arange(Nk) + 0.5) / Nk
    a, b = -2 * np.cos(kb + q / 2) - mu - h, -2 * np.cos(-kb + q / 2) - mu + h
    for _ in range(4000):
        Dq = Dud * np.exp(1j * kb) - Ddu * np.exp(-1j * kb)
        H = np.zeros((Nk, 2, 2), complex); H[:, 0, 0] = a; H[:, 1, 1] = -b; H[:, 0, 1] = Dq; H[:, 1, 0] = np.conj(Dq)
        E, V = np.linalg.eigh(H)
        F = np.sum(V[:, 0, :] * V[:, 1, :].conj() * (E > 0), axis=1)
        nud, ndu = -U * np.mean(np.exp(-1j * kb) * F), U * np.mean(np.exp(1j * kb) * F)
        err = max(abs(nud - Dud), abs(ndu - Ddu))
        Dud, Ddu = 0.6 * nud + 0.4 * Dud, 0.6 * ndu + 0.4 * Ddu
        if err < 1e-10:
            break
    e0 = -2 * np.cos(kb) - mu
    En = np.mean(np.minimum(e0 - h, 0) + np.minimum(e0 + h, 0))
    return np.mean(np.sum(np.where(E < 0, E, 0), axis=1)) + np.mean(b) + (abs(Dud) ** 2 + abs(Ddu) ** 2) / abs(U) - En, err


def bond_one(mu, hs, U, D, Nk=1000):
    kb = 2 * np.pi * (np.arange(Nk) + 0.5) / Nk
    x = -2 * np.cos(kb) - mu + hs
    for _ in range(4000):
        Dk = 2j * D * np.sin(kb)
        H = np.zeros((Nk, 2, 2), complex); H[:, 0, 0] = x; H[:, 1, 1] = -x; H[:, 0, 1] = Dk; H[:, 1, 0] = np.conj(Dk)
        E, V = np.linalg.eigh(H)
        new = U * np.mean(np.exp(1j * kb) * np.sum(V[:, 0, :] * V[:, 1, :].conj() * (E > 0), axis=1))
        err, D = abs(new - D), 0.6 * new + 0.4 * D
        if err < 1e-10:
            break
    return 0.5 * np.mean(np.sum(np.where(E < 0, E, 0), axis=1)) + 0.5 * np.mean(x) + abs(D) ** 2 / abs(U) - np.mean(np.minimum(x, 0)), err


rng_b = np.random.default_rng(7)
starts = [(rng_b.normal(size=(2, 2)) + 1j * rng_b.normal(size=(2, 2))) * 0.4 for _ in range(3)]
singlet_part = lambda D: abs(D[0, 1] - D[1, 0]) / 2
runs = {(U_, h_): [bond_route1(-1.6, h_, U_, D_) for D_ in starts] for U_, h_ in ((-1.5, 0.0), (-1.5, 0.1), (-1.5, 0.3), (-3.0, 0.6))}
ok = all(r[4] < 1e-9 and abs(r[1] - r[2]) < 1e-9 for v in runs.values() for r in v)
ok = ok and all(abs(r[1] - v[0][1]) < 1e-9 for v in runs.values() for r in v)              # every start, the same state
w0, w1, w3, s6 = runs[(-1.5, 0.0)][0], runs[(-1.5, 0.1)][0], runs[(-1.5, 0.3)][0], runs[(-3.0, 0.6)][0]
Es0, err_s = bond_opp(-1.6, 0.0, -1.5, 0.5, -0.5)
Et3 = bond_one(-1.6, -0.3, -1.5, 0.3)[0] + bond_one(-1.6, 0.3, -1.5, 0.3)[0]
Eu6 = bond_one(-1.6, -0.6, -3.0, 0.5)[0]
ok = ok and abs(Es0 - w0[1]) < 1e-9 and abs(Et3 - w3[1]) < 1e-9 and abs(Eu6 - s6[1]) < 1e-9 and err_s < 1e-9
check('text, bond model, routes: the 4x4 energy in its two forms equals the sector energies of the pure singlet and the pure triplets',
      ok, (round(w0[1], 5), round(w3[1], 5), round(s6[1], 5)))
ok = singlet_part(w0[0]) > 0.15 and np.abs(np.diag(w0[0])).max() < 1e-6 and abs(w0[0][0, 1] + w0[0][1, 0]) < 1e-6 and abs(w0[3] - 0.2875) < 1e-3
ok = ok and singlet_part(w3[0]) < 1e-6 and abs(w3[0][0, 1]) < 1e-6 and abs(w3[0][1, 0]) < 1e-6 and abs(w3[0][0, 0]) > 0.1 and w3[1] < -1e-3
ok = ok and singlet_part(w1[0]) > 0.15 and np.abs(np.diag(w1[0])).max() < 1e-6 and abs(0.1 / w0[3] - 0.35) < 5e-3
ok = ok and (-2 - (-1.6) + 0.3) < 0 and abs(0.3 / w0[3] - 1.04) < 5e-3
check('text, bond model mu=-1.6, |U|=1.5: pure singlet at h=0 with the smallest quasiparticle energy 0.2875 and at h=0.1 = 0.35 '
      'times it, pure equal-spin triplet at h=0.3 = 1.04 times it, with both spin bands at the Fermi level', ok,
      (round(singlet_part(w0[0]), 4), round(w0[3], 4), round(abs(w3[0][0, 0]), 4), round(abs(w3[0][1, 1]), 4)))
opp6 = min(bond_opp(-1.6, 0.6, -3.0, *st, q=q_)[0] for q_ in np.linspace(0, 1.6, 9) for st in ((0.5, -0.5), (0.5, 0.0)))
ok = singlet_part(s6[0]) < 1e-6 and abs(s6[0][0, 1]) < 1e-6 and abs(s6[0][1, 1]) < 1e-6 and abs(s6[0][0, 0]) > 0.5
ok = ok and (-2 - (-1.6) + 0.6) > 0 and (-2 - (-1.6) - 0.6) < 0 < (2 - (-1.6) - 0.6) and opp6 > s6[1] + 0.02
# an open point for the coordinator, listed in "Not applied" of the plan: at |U|=3 the clause "or when only one spin band crosses
# the Fermi level" does not hold just above h=0.4, where the down band leaves the Fermi level. At h=0.45 (down band from +0.05) a
# state with the singlet part 0.38 lies below the pure triplet, while at h=0.6 the pure triplet wins, as asserted next
m45 = bond_route1(-1.6, 0.45, -3.0, [[0.5, 0.4], [-0.4, 0.3]])
t45 = bond_one(-1.6, -0.45, -3.0, 0.5)[0] + bond_one(-1.6, 0.45, -3.0, 0.5)[0]
check('open point, bond model mu=-1.6, |U|=3, h=0.45: only the up band crosses, and a state with a singlet part 0.38 is below the '
      'pure triplet', m45[4] < 1e-9 and abs(singlet_part(m45[0]) - 0.38) < 5e-3 and m45[1] < t45 - 1e-3 and (-2 + 1.6 + 0.45) > 0,
      (round(singlet_part(m45[0]), 4), round(m45[1], 5), round(t45, 5)))
check('text, bond model mu=-1.6, |U|=3, h=0.6: only the up band crosses the Fermi level, the ground state is the pure up-up triplet, '
      'and every opposite-spin state with a pair momentum q from 0 to 1.6 lies above it', ok,
      (round(abs(s6[0][0, 0]), 4), round(s6[1], 5), round(opp6, 5)))

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
# Fermi level touches the two bands at their edges, k = pi and k = 0. The try-it says so since 2026-11-22, "At 1.0 each
# spin has its own Fermi momentum, and at 2.0 each band touches zero energy only at its edge". The second route is the
# pyqula matrix of the cell, with the momentum of pyqula in units of 2 pi
for J in (1.0, 2.0):
    H = g.get_hamiltonian()
    H.add_exchange([0., 0., J])
    qq = np.linspace(0., 1., 2001)
    ee = np.array([np.linalg.eigvalsh(H.get_hk_gen()([q, 0., 0.])) for q in qq])
    up, dn = ee[:, 1], ee[:, 0]
    if J == 1.0:
        zs = sorted(2 * np.pi * qq[i] for i in range(len(qq) - 1) for b in (up, dn) if b[i] * b[i + 1] < 0)
        check('try-it, J=1, pyqula: each band crosses zero, at k = pi/3 and 2 pi/3 in 0 < k < pi',
              len(zs) == 4 and abs(zs[0] - np.pi / 3) < 5e-3 and abs(zs[1] - 2 * np.pi / 3) < 5e-3, np.round(zs[:2], 4))
    else:
        check('try-it, J=2, pyqula: the upper band has its minimum 0 at k=pi and the lower band its maximum 0 at k=0',
              abs(up.min()) < 1e-12 and abs(2 * qq[np.argmin(up)] - 1) < 1e-9 and abs(dn.max()) < 1e-12
              and (abs(2 * qq[np.argmax(dn)]) < 1e-9 or abs(2 * qq[np.argmax(dn)] - 2) < 1e-9), (up.min(), dn.max()))
k1 = (float(np.arccos(-1 / 2)), float(np.arccos(1 / 2)))
check('try-it, J=1: the Fermi momenta of the two spins are 2 pi/3 and pi/3', np.allclose(k1, (2 * np.pi / 3, np.pi / 3)), k1)
check('try-it, J=2: 2 cos k + 2 >= 0 and 2 cos k - 2 <= 0, both bands touch zero only at a band edge',
      (2 * np.cos(k) + 2).min() > -1e-12 and (2 * np.cos(k) - 2).max() < 1e-12, True)
