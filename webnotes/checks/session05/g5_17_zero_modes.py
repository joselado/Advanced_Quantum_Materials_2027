"""Session 5, the numbers that page 17 (Section 5.17, topological zero modes) states and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here or in the
figure script that draws it. The caption of kitaev_spectrum (1.4t at mu=0, below 0.003t up to |mu|=1.9t, 0.04t at |mu|=2t) is
asserted in figures/session05/kitaev_spectrum.py, the caption of zero_mode_profile (0.51t) in zero_mode_profile.py, the 0.011t
and 2e-5 t of majorana_splitting in majorana_splitting.py, and the three pictures of the quiz on the profiles in
g5_quiz_profile_*.py. This script checks the key box, the steps fold, the quizzes, the problem and the try-it box, with numpy
and with the pyqula chain of the notebook, whose matrix is read from h.intra with no file written.

Run it from anywhere:  python3 webnotes/checks/session05/g5_17_zero_modes.py"""
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures', 'session05'))
import _g5_kitaev as kc


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


t = 1.0
k = np.linspace(-np.pi, np.pi, 20001)


def Ek(mu, D):
    return np.sqrt((2 * t * np.cos(k) + mu)**2 + 4 * D**2 * np.sin(k)**2)


# ---- the bulk energy against the BdG matrix of a ring, so that the fold may use only |Delta(k)| = 2 Delta |sin k|
N = 16
for (mu, D) in ((0.4, 0.3), (-1.3, 0.8), (2.6, 0.5)):
    H = kc.bdg(N, t, mu, D)
    H[0, N - 1] = H[N - 1, 0] = -t                       # close the ring, hopping and pairing on the bond (N, 1)
    H[N, 2 * N - 1] = H[2 * N - 1, N] = t
    H[N - 1 + N, 0] = H[0, N - 1 + N] = 0
    d = D * (np.eye(N, k=-1) - np.eye(N, k=1)); d[0, N - 1] = D; d[N - 1, 0] = -D
    H[:N, N:] = d; H[N:, :N] = d.conj().T
    e = np.sort(np.abs(np.linalg.eigvalsh(H)))
    kk = 2 * np.pi * np.arange(N) / N
    ref = np.sort(np.r_[np.sqrt((2 * t * np.cos(kk) + mu)**2 + 4 * D**2 * np.sin(kk)**2)] * np.ones((2, 1)), axis=None)
    check(f'fold: a ring of 16 sites has E(k)^2 = (2t cos k + mu)^2 + 4 Delta^2 sin^2 k, mu={mu}, Delta={D}',
          np.abs(e - ref).max() < 1e-12, round(np.abs(e - ref).max(), 15))

# ---- the fold and the key box, where the gap closes
check('fold: at Delta=t, mu=0 the bulk is flat at 2t', np.allclose(Ek(0.0, 1.0), 2 * t), 2)
for D in (0.1, 0.5, 1.3, -0.7):
    for mu, kz in ((-2.0, 0.0), (2.0, np.pi)):
        E = Ek(mu, D)
        check(f'key: Delta={D}, mu={mu}: E=0 only at |k|={kz:.4f}', E.min() < 1e-12 and np.all(np.abs(np.abs(k[E < 1e-6]) - kz) < 1e-3),
              round(abs(k[np.argmin(E)]), 4))
kg = np.linspace(-np.pi, np.pi, 2001)
Eg = lambda mu, D: np.sqrt((2 * t * np.cos(kg) + mu)**2 + 4 * D**2 * np.sin(kg)**2)
mus = np.linspace(-1.98, 1.98, 100)
Ds = np.linspace(0.05, 1.5, 30)
gmin = min(Eg(m, D).min() for m in mus for D in Ds)
check('fold: inside |mu|<2t (to 1.98) and for Delta from 0.05 to 1.5 the gap never closes', gmin > 1e-3, round(gmin, 5))
gmin = min(Eg(m, D).min() for m in np.r_[np.linspace(-6, -2.02, 50), np.linspace(2.02, 6, 50)] for D in Ds)
check('fold: outside the window, for |mu| from 2.02t to 6t, the gap never closes either', gmin > 1e-3, round(gmin, 5))
E = Ek(1.0, 0.0)
check('fold: at Delta=0 and |mu|<2t the chain is a metal, the gap closes at the Fermi points', E.min() < 1e-3, round(E.min(), 5))


# ---- the key box and the fold for Delta<0: the point Delta=-t, its free halves gamma_2 and gamma_{2N-1}, and the gauge c -> ic
def fermions(N):
    """Annihilation operators c_1..c_N on the 2^N states, with the Jordan-Wigner string."""
    a, z, one = np.array([[0., 1.], [0., 0.]]), np.diag([1., -1.]), np.eye(2)
    ops = []
    for n in range(N):
        m = np.array([[1.]])
        for j in range(N):
            m = np.kron(m, z if j < n else (a if j == n else one))
        ops.append(m)
    return ops


def kitaev(c, t, mu, D):
    """The Hamiltonian (5.19) on an open chain, as a matrix on the Fock space."""
    dg = lambda o: o.conj().T
    H = sum(-mu * dg(cn) @ cn for cn in c)
    for n in range(len(c) - 1):
        H = H - t * (dg(c[n]) @ c[n + 1] + dg(c[n + 1]) @ c[n]) + D * (c[n] @ c[n + 1] + dg(c[n + 1]) @ dg(c[n]))
    return H


for Nf in (4, 5):
    cf = fermions(Nf)
    gf = [None]
    for cn in cf:
        gf += [cn + cn.conj().T, -1j * (cn - cn.conj().T)]      # gamma_{2n-1}, gamma_{2n} of (5.17)
    for tt in (1.0, 0.6):
        H = kitaev(cf, tt, 0.0, -tt)
        Hm = sum(-1j * tt * gf[2 * n - 1] @ gf[2 * n + 2] for n in range(1, Nf))
        comm = [np.abs(H @ gf[i] - gf[i] @ H).max() < 1e-12 for i in range(1, 2 * Nf + 1)]
        free = [i for i in range(1, 2 * Nf + 1) if comm[i - 1]]
        check(f'key and fold: at Delta=-t={-tt}, mu=0, N={Nf} the chain is -it sum gamma_(2n-1) gamma_(2n+2), and only gamma_2 and '
              f'gamma_(2N-1) commute with it', np.abs(H - Hm).max() < 1e-12 and free == [2, 2 * Nf - 1], free)
    U = np.diag(np.exp(0.5j * np.pi * np.array([bin(s).count('1') for s in range(2**Nf)])))   # U^dag c_n U = i c_n
    ok = all(np.abs(U @ kitaev(cf, 1.0, m, Dg) @ U.conj().T - kitaev(cf, 1.0, m, -Dg)).max() < 1e-12
             for (m, Dg) in ((0.0, 1.0), (0.7, 0.4), (-1.3, 0.9)))
    check(f'fold: the gauge c_n -> i c_n changes Delta into -Delta and keeps the hopping and mu, N={Nf}', ok, Nf)
for (mu, D) in ((0.0, 1.0), (1.0, 0.5), (-1.5, 0.3), (3.0, 0.5)):
    check(f'fold: both signs of Delta give the same levels on 30 sites, mu={mu}, |Delta|={D}',
          np.allclose(kc.levels(30, t, mu, D), kc.levels(30, t, mu, -D), atol=1e-12), mu)
Nb = 12
eN = lambda n: np.eye(Nb)[n]
for (D, vecs) in ((1.0, (np.r_[eN(0), eN(0)], np.r_[eN(Nb - 1), -eN(Nb - 1)])), (-1.0, (np.r_[eN(0), -eN(0)], np.r_[eN(Nb - 1), eN(Nb - 1)]))):
    H = kc.bdg(Nb, t, 0.0, D)
    check(f'key: in the BdG matrix of 12 sites at Delta={D}t, mu=0 the zero levels are the Nambu vectors of '
          + ('gamma_1 and gamma_2N' if D > 0 else 'gamma_2 and gamma_(2N-1)'),
          all(np.abs(H @ v).max() < 1e-12 for v in vecs) and np.sum(np.abs(kc.levels(Nb, t, 0.0, D)) < 1e-12) == 2, D)
w, nz = kc.zero_weight(40, t, 1.0, -0.5, tol=1e-9)
check('key: for Delta=-0.5t and mu=t the open chain of 40 sites has two levels at zero at its two ends',
      nz == 2 and w[:5].sum() + w[-5:].sum() > 0.99, (nz, round(w[:5].sum() + w[-5:].sum(), 6)))

# ---- the first quiz, the sign of mu: mu=t and mu=-t have the same levels on an open chain
for Nq in (8, 40):
    a, b = kc.levels(Nq, t, 1.0, 0.5), kc.levels(Nq, t, -1.0, 0.5)
    check(f'quiz: the open chain of {Nq} sites with Delta=0.5t has the same levels for mu=t and mu=-t', np.allclose(a, b, atol=1e-12),
          round(np.sort(np.abs(a))[0], 12))

# ---- the second quiz and the caption of majorana_splitting
lo = {n: np.sort(np.abs(kc.levels(n, t, 1.0, 0.5))) for n in range(4, 31, 2)}
check('quiz: the end modes of N=8 are at 0.011t', abs(lo[8][0] - 0.011) < 5e-4, round(lo[8][0], 5))
check('quiz: the end modes of N=20 are at 2e-5 t', abs(lo[20][0] - 2e-5) < 1e-6 * 5, lo[20][0])
check('quiz: the smallest bulk energy of the infinite chain is 0.82t', abs(Ek(1.0, 0.5).min() - 0.82) < 0.005, round(Ek(1.0, 0.5).min(), 4))
first = np.array([lo[n][2] for n in lo])
check('caption: the first bulk level comes down from 1.02t at N=4 to 0.83t at N=30, close to the bulk value 0.82t',
      round(first[0], 2) == 1.02 and round(first[-1], 2) == 0.83 and first.min() > 0.8165 and np.all(np.diff(first) < 0.002)
      and round(Ek(1.0, 0.5).min(), 2) == 0.82, (round(first[0], 4), round(first[-1], 4)))
check('alt text: on the log axis from 1e-8 to 3 the first bulk level is a nearly flat line close to 1, within 0.1 decade',
      np.abs(np.log10(first)).max() < 0.1 and np.ptp(np.log10(first)) <0.1 * np.log10(3 / 1e-8),
      (round(float(np.log10(first).min()), 4), round(float(np.log10(first).max()), 4)))

# ---- the problem
x = -2 / 3
check('problem: E^2/t^2 = 3x^2 + 4x + 2 with x = cos k, at mu=t and Delta=0.5t',
      np.allclose(Ek(1.0, 0.5)**2, 3 * np.cos(k)**2 + 4 * np.cos(k) + 2), 0)
Emin = np.sqrt(3 * x**2 + 4 * x + 2)
check('problem: the minimum is at cos k = -2/3, k = 2.30, with E = sqrt(2/3) t = 0.82t',
      abs(Emin - np.sqrt(2 / 3)) < 1e-15 and abs(np.sqrt(2 / 3) - 0.8165) < 1e-4 and abs(np.arccos(x) - 2.30) < 0.005
      and abs(abs(k[np.argmin(Ek(1.0, 0.5))]) - np.arccos(x)) < 1e-3, (round(Emin, 4), round(np.arccos(x), 4)))
check('problem: the two branches are 1.63t apart there', abs(2 * Emin - 1.633) < 5e-4, round(2 * Emin, 4))
check('problem: the first bulk level of the open chain is 0.89t at N=8 and 0.83t at N=20',
      abs(lo[8][2] - 0.89) < 0.005 and abs(lo[20][2] - 0.83) < 0.005, (round(lo[8][2], 4), round(lo[20][2], 4)))

# ---- a second route, the pyqula chain of the notebook, for the levels of the profiles and of the try-it box
from pyqula import geometry


def pyqula_levels(L, onsite, delta, d):
    g = geometry.chain().get_supercell(L)  # L sites
    g.dimensionality = 0  # open chain
    h = g.get_hamiltonian()  # two spins
    h.add_onsite(4.0)  # every energy up by 4
    h.add_exchange([0., 0., 4.])  # spin up 8 above, spin down back to 2 cos k
    h.add_onsite(onsite)  # mu = -onsite for the spin-down band
    h.add_pairing(mode="pwave", delta=delta, d=d)  # Delta = delta |d_x + i d_y|
    m = h.intra.todense() if hasattr(h.intra, 'todense') else h.intra
    return np.sort(np.abs(np.linalg.eigvalsh(np.array(m))))


for (mu, expect, tol) in ((0.0, 0.0, 1e-9), (-1.5, 0.0, 1e-9), (3.0, 1.008, 5e-4), (1.0, 0.0, 1e-9), (2.5, 0.51, 5e-3)):
    a = pyqula_levels(40, -mu, 0.5, [1., 0., 0.])[0]
    b = np.sort(np.abs(kc.levels(40, t, mu, 0.5)))[0]
    check(f'second route: the lowest level of 40 sites with Delta=0.5t at mu={mu} is {expect}t, by pyqula and by numpy',
          abs(a - b) < 1e-12 and abs(a - expect) < tol, a)
for (mu, which, expect, tol) in ((0.0, 2, 1.40, 0.005), (1.9, 0, 0.0022, 1e-4), (2.0, 0, 0.037, 5e-4), (-2.0, 0, 0.037, 5e-4)):
    a = pyqula_levels(60, -mu, 0.7, [1., 0., 0.])[which]
    b = np.sort(np.abs(kc.levels(60, t, mu, 0.7)))[which]
    check(f'second route: kitaev_spectrum, 60 sites with Delta=0.7t at mu={mu}, level {which} is {expect}t, by pyqula and by numpy',
          abs(a - b) < 1e-10 and abs(a - expect) < tol, a)
for (m, expect, tol) in ((0.3, 1.65e-3, 5e-5), (1.0, 1.39e-3, 5e-5), (2.5, 0.506, 5e-4)):
    a = pyqula_levels(40, m, 0.1, [1., 1., 0.])[0]
    b = np.sort(np.abs(kc.levels(40, t, -m, 0.1 * np.sqrt(2))))[0]
    check(f'try-it: the notebook cell with delta=0.1, d=[1,1,0], L=40 and mu={m} has its lowest level at {expect}', abs(a - expect) < tol
          and abs(a - b) < 1e-12, a)
# the try-it box, decided on 2026-11-22: "the line mu = 0.3 sets the chemical potential through h.add_onsite, which is mu=-0.3 in
# (5.19)". First route, the matrix: add_onsite(0.3) of the cell puts the spin-down electron at +0.3 on every site, which is the
# term -mu c^dag c of (5.19) with mu = -0.3. Second route, the levels: the cell with mu = 0.3 is the exact chain with mu = -0.3 at
# every length of the cell, 4 to 40 (the levels do not depend on the sign of mu, so this route checks the size of mu only)
gs_ = geometry.chain().get_supercell(3); gs_.dimensionality = 0
hs_ = gs_.get_hamiltonian(); hs_.add_onsite(4.0); hs_.add_exchange([0., 0., 4.]); hs_.add_onsite(0.3)
ms_ = np.array(hs_.intra.todense() if hasattr(hs_.intra, 'todense') else hs_.intra)
ok = ms_.shape == (6, 6) and all(abs(ms_[2 * i + 1, 2 * i + 1] - 0.3) < 1e-12 for i in range(3))  # no pairing yet: up, down per site
ok = ok and all(np.abs(pyqula_levels(L, 0.3, 0.1, [1., 1., 0.])[:L] - np.sort(np.abs(kc.levels(L, t, -0.3, 0.1 * np.sqrt(2))))[:L]).max()
                < 1e-10 for L in range(4, 42, 2))
check('try-it: mu = 0.3 of the cell enters through add_onsite as +0.3 on the spin-down electron, so it is mu=-0.3 of (5.19)', ok,
      round(ms_[1, 1].real, 12))
# the point on the Kitaev figures, decided on 2026-11-22 (numpy stays): the pyqula chain of the notebook with delta=0.5 and
# d=[1,1,0] at mu=0 has its first bulk level at 1.418 on 40 sites, and so does the exact chain (5.19) with Delta=0.707, so the
# 0.3% against the bulk value 2 Delta = 1.414 is the finite size of the chain, and not a difference between the two models
a = pyqula_levels(40, 0.0, 0.5, [1., 1., 0.])[2]
b = np.sort(np.abs(kc.levels(40, t, 0.0, 0.5 * np.sqrt(2))))[2]
check('Kitaev figures: 40 sites, delta=0.5, d=[1,1,0], mu=0, first bulk level 1.418 by pyqula and by (5.19), bulk value 1.414',
      abs(a - b) < 1e-10 and abs(a - 1.418) < 5e-4 and abs(2 * 0.5 * np.sqrt(2) - 1.414) < 5e-4, round(a, 5))
# the old text "for example with N=100 sites" gives no mu and no Delta, so it is checked at the point (5.21), Delta=t and mu=0, at
# the parameters of the profile figure, Delta=0.5t and mu=t, and at two more points inside the window: two levels at zero on the
# ten end sites, and the first bulk level within 1% of the smallest bulk energy of the periodic chain
for (mu, D) in ((0.0, 1.0), (1.0, 0.5), (0.0, 0.7), (-1.5, 0.5)):
    w, nz = kc.zero_weight(100, t, mu, D, tol=1e-9)
    first = np.sort(np.abs(kc.levels(100, t, mu, D)))[2]
    gap = Ek(mu, D).min()
    check(f'text: an open chain of 100 sites with mu={mu}t, Delta={D}t has two levels at zero at the two ends, and keeps the gap {gap:.4f}t',
          nz == 2 and w[:5].sum() + w[-5:].sum() > 0.99 and abs(first - gap) < 0.01 * gap,
          (nz, round(w[:5].sum() + w[-5:].sum(), 6), round(first, 4)))

# ---- the old text corrected on 2026-11-22
# the smallest bulk energy, the formula of the sheet, Delta sqrt(4 - mu^2/(t^2 - Delta^2)) for Delta<t and |mu| t <= 2(t^2 - Delta^2),
# and |2t - |mu|| otherwise, as a second route to the minimum over k
def Eform(mu, D):
    if D < t and abs(mu) * t <= 2 * (t**2 - D**2):
        return D * np.sqrt(4 - mu**2 / (t**2 - D**2))
    return abs(2 * t - abs(mu))


check('quiz 2: "the smallest bulk energy is 0.82t" at Delta=0.5t, mu=t, by the minimum over k and by the formula',
      abs(Ek(1.0, 0.5).min() - Eform(1.0, 0.5)) < 1e-6 and round(Eform(1.0, 0.5), 2) == 0.82, round(Eform(1.0, 0.5), 5))
# the first paragraph: the periodic chain with Delta != 0 and |mu| < 2t is fully gapped, with a gap that depends on Delta and mu,
# and its Zak phase is pi, while for |mu| > 2t the Zak phase is 0. Second route, the sign of eps(0) eps(pi), -1 inside the window
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures'))
import physcheck
gaps = {mu: (Ek(mu, 0.5).min(), Eform(mu, 0.5)) for mu in (0.0, 1.0, 1.9, 3.0)}
check('text: at Delta=0.5t the smallest bulk energy is 1.0t, 0.8165t and 0.1t for mu=0, t and 1.9t, so it is set by Delta and mu',
      all(abs(a - b) < 1e-6 for a, b in gaps.values()) and abs(gaps[0.0][1] - 1.0) < 1e-12 and abs(gaps[1.0][1] - 0.8165) < 1e-4
      and abs(gaps[1.9][1] - 0.1) < 1e-9, {m: round(v[1], 4) for m, v in gaps.items()})


def bloch(mu, D):
    return lambda q: np.array([[-2 * t * np.cos(float(np.ravel(q)[0])) - mu, -2j * D * np.sin(float(np.ravel(q)[0]))],
                               [2j * D * np.sin(float(np.ravel(q)[0])), 2 * t * np.cos(float(np.ravel(q)[0])) + mu]])


zak = {mu: physcheck.zak_phase(bloch(mu, 0.5), np.array([2 * np.pi]), bands=0, nk=400) for mu in (0.0, 1.0, 1.5, -1.5, 2.5, 3.0)}
sgn = {mu: np.sign((-2 * t - mu) * (2 * t - mu)) for mu in zak}
check('text: the Zak phase of the periodic chain at Delta=0.5t is pi for |mu|<2t and 0 for |mu|>2t, as the sign of eps(0) eps(pi)',
      all((abs(abs(z) - np.pi) < 1e-9) == (abs(mu) < 2) and (abs(z) < 1e-9) == (abs(mu) > 2) and (sgn[mu] < 0) == (abs(mu) < 2)
          for mu, z in zak.items()), {m: round(z, 4) for m, z in zak.items()})
# "the hopping between neighboring sites dominates over the onsite term, |mu| < 2t, and then any pairing Delta != 0 gives this
# phase, also a weak one": with Delta=0.1t, much smaller than mu=1.5t and 1.9t, an open chain of 400 sites has two levels at zero
# with their weight on the 40 sites at each end, and at mu=2.1t it has none. Second route, the pyqula chain of 200 sites
for (mu, D, topo) in ((1.5, 0.1, True), (1.9, 0.1, True), (2.1, 0.1, False)):
    nz = int(np.sum(np.abs(kc.levels(400, t, mu, D)) < 1e-9))
    a = pyqula_levels(200, -mu, D, [1., 0., 0.])[:2]
    if topo:
        w, nz = kc.zero_weight(400, t, mu, D, tol=1e-9)
        ok = nz == 2 and w[:40].sum() + w[-40:].sum() > 0.999 and a.max() < 1e-9
    else:
        ok = nz == 0 and a.min() > 0.09
    check(f'text: Delta={D}t and mu={mu}t on an open chain, {"two end modes at zero" if topo else "no level at zero"}, by numpy and by pyqula',
          ok, (nz, np.round(a, 12)))
# the widget, 30 sites with t=Delta=1: the two levels sit at zero away from |mu|=2t and move away from zero near it, while they
# stay below the bulk value |2t-|mu||. Second route, the compute() of the widget itself
sys.path.insert(0, os.path.join(HERE, '..', '..', 'widgets', 'defs'))
import kitaevbdg
for (mu, expect, tol) in ((1.0, 0.0, 1e-8), (1.5, 1.56e-4, 1e-6), (1.9, 0.0475, 5e-4)):
    a = np.sort(np.abs(kc.levels(30, t, mu, 1.0)))[0]
    b = np.sort(np.abs(kitaevbdg.compute(dict(mu=mu))['panels'][0]['series'][0]['y']))[0]
    check(f'widget: 30 sites, t=Delta=1, mu={mu}, the lowest level is {expect}, below the bulk value {abs(2 - mu):.1f}',
          abs(a - b) < 1e-12 and abs(a - expect) < tol and a < abs(2 * t - mu), a)
print('all checks of page 17 hold')
