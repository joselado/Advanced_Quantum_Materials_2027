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
check('caption: the first bulk level stays near 0.8t, from 1.02t at N=4 down to 0.83t at N=30, above 0.8165t',
      first.max() < 1.02 and first.min() > 0.8165 and abs(first[-1] - 0.826) < 0.001 and np.all(np.diff(first) < 0.002),
      (round(first.max(), 4), round(first.min(), 4)))

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
print('all checks of page 17 hold')
