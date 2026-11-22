"""Session 7, the numbers that page 11 (Section 7.11, MERA and PEPS beyond MPS) states and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here or in the
figure script that draws it. The caption of critical_entropy (3002 sites, 1.49 at l=10, 2.96 at l=1000, the line
1/3 log l + 0.73 up to l=316, about 0.5 for the dimerized chain, the chain three times longer than the block) and the growth
of about 1.5 of the feedback figure of the first quiz are asserted in figures/session07/critical_entropy.py, which runs the
pyqula script of 3002 sites, about two minutes, so it is not run again here. The feedback numbers of the picture quiz are
asserted in g5_quiz_entropy_*.py, and this script checks them again together with the alt texts, from the same helper on 402
sites, in about ten seconds. It also checks the key box, the steps fold, the first two quizzes, the problem and the lab box.
A second route with numpy on the open chain, with no pyqula, checks the numbers of the caption on 3002 sites and of the
pictures on 402 sites, in about thirty seconds, and an exact diagonalization of a Heisenberg ring of 16 spins checks the
c=1 of the reading of the lab box. Added on 2026-11-22: the count of the Schmidt weights of a block of the infinite XX chain
for the problem (M >= 10 and 69 for a dropped weight 1e-6), a random MPS for the ranks M and M^2 of the fold and the problem,
the sine modes of longer open chains for the cause in the caption, a maximum flow on a binary MERA for the best cut of the
fold, the two numbers of the stored lab source, and the old feedback of quiz 2, whose 0.77 and 2.3 are (1/3) log l alone.
Corrected on 2026-11-22: the feedback of quiz 2 now says that the entropy grows by about 1.5, the key box names the two
ends of the block and the c/6 of one end, the problem names M_min, the lab box says what the abstract reports, and the
try-it says that the peak of the scan of the Ising chain sits below B_x = 0.5, checked here with free fermions and an
exact diagonalization of 12 sites.

Run it from anywhere:  python3 webnotes/checks/session07/g5_11_mera_and_peps.py"""
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures', 'session07'))


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def entropy(C):
    nu = np.linalg.eigvalsh(C)
    nu = nu[(nu > 1e-13) & (nu < 1 - 1e-13)]
    return -np.sum(nu * np.log(nu) + (1 - nu) * np.log(1 - nu))


# ---- key box: c=1 for the XX chain, the slope 1/3 of the infinite chain of free fermions at half filling
L = 1000
d = np.arange(L)[:, None] - np.arange(L)[None, :]
with np.errstate(all='ignore'):
    C = np.where(d == 0, 0.5, np.sin(np.pi * d / 2) / (np.pi * d))
ells = np.array([10, 32, 100, 316, 1000])
S = np.array([entropy(C[:l, :l]) for l in ells])
slope, const = np.polyfit(np.log(ells), S, 1)
check('key: the XX chain (free fermions, hopping 1, half filling) has the slope c/3 with c=1', abs(slope - 1 / 3) < 2e-3, round(slope, 4))
check('caption: the constant of the infinite chain is 0.73', abs(const - 0.73) < 5e-3, round(const, 4))

# ---- steps fold: log2 l layers, 10 layers for l=1024, bound 10 log M, log2(l) log M = (log M/log 2) log l
check('fold and quiz 2: l=1024 needs log2(1024)=10 layers', np.log2(1024) == 10, np.log2(1024))
for M in (2, 4, 16):
    check(f'fold: log2(l) log M = (log M / log 2) log l for M={M}', abs(np.log2(1024) * np.log(M) - np.log(M) / np.log(2) * np.log(1024)) < 1e-12, round(10 * np.log(M), 4))
n, l = 0, 1024
while l > 1:
    l //= 2; n += 1
check('fold: halving 1024 sites gives one site after 10 layers', n == 10, n)

# ---- quiz 1: the premise S = (1/3) log l, with no constant
check('quiz 1: (1/3) log 10 is 0.77', abs(np.log(10) / 3 - 0.77) < 5e-3, round(np.log(10) / 3, 4))
check('quiz 1: (1/3) log 1000 is 2.3', abs(np.log(1000) / 3 - 2.3) < 5e-3, round(np.log(1000) / 3, 4))
check('quiz 1: the growth (1/3) log 100 is about 1.5', abs(np.log(100) / 3 - 1.5) < 0.05, round(np.log(100) / 3, 4))
check('quiz 1: 2.3 is about three times 0.77', abs(np.log(1000) / np.log(10) - 3) < 1e-12, np.log(1000) / np.log(10))
check('quiz 1: l grows by a factor 100 from 10 to 1000', 1000 / 10 == 100, 100)
check('quiz 1 feedback figure: the infinite chain also grows by about 1.5 with the constant', abs(S[-1] - S[0] - 1.5) < 0.05, round(S[-1] - S[0], 4))

# ---- quiz 2: a volume law of a block of 1024 sites, about 1000 log 2
check('quiz 2: 1024 log 2 is about 1000 log 2', abs(1024 / 1000 - 1) < 0.03, 1024)
# quiz 2, feedback of option 1, corrected on 2026-11-22: the old 0.77 and 2.3 were the term (1/3) log l alone, while the
# entropy of a block of the critical chain is 1.49 at l=10 and 3.03 at l=1000 (infinite chain), so the feedback now says
# that the entropy grows by about 1.5, which holds with the constant, for the infinite chain and for the figure
check('quiz 2, option 1: the entropy of the block grows by about 1.5 from l=10 to 1000, (1/3) log 100 = 1.535',
      abs(S[-1] - S[0] - 1.5) < 0.05 and abs(np.log(100) / 3 - 1.5) < 0.05, round(S[-1] - S[0], 4))
check('quiz 2, option 1, the old numbers: 0.77 and 2.3 are (1/3) log l at l=10 and 1000, not the entropy of the block',
      abs(np.log(10) / 3 - 0.77) < 5e-3 and abs(np.log(1000) / 3 - 2.3) < 5e-3 and abs(S[0] - 1.49) < 5e-3 and abs(S[-1] - 3.03) < 5e-3,
      (round(np.log(10) / 3, 4), round(np.log(1000) / 3, 4), round(S[0], 4), round(S[-1], 4)))

# ---- quiz 3, the picture options, and their alt texts, from the helper of the three pictures
import _g5_entropycurves as ec
l, Sg = ec.dimerized()
check('quiz 3, gapped: 0.39 at l=2', abs(Sg[0] - 0.39) < 5e-3, round(Sg[0], 4))
check('quiz 3, gapped: about 0.5 from l=6 on', np.all(np.abs(Sg[l >= 6] - 0.5) < 0.012), np.round(Sg[l >= 6], 4))
l, Sc = ec.critical()
sl = np.polyfit(np.log(l), Sc, 1)[0]
check('quiz 3, critical: the slope is 0.33', abs(sl - 0.33) < 5e-3, round(sl, 4))
check('quiz 3, critical: about 2.2 at l=100', l[-1] == 100 and abs(Sc[-1] - 2.2) < 0.05, round(Sc[-1], 4))
check('quiz 3, critical alt: about 0.9 at the smallest block, l=2', l[0] == 2 and abs(Sc[0] - 0.9) < 0.05, round(Sc[0], 4))
lv, Sv = ec.volume()
check('quiz 3, volume: leaves the frame S=2.5 at l=3.6, before 4', abs(2.5 / np.log(2) - 3.6) < 0.01 and lv[-1] < 4, round(2.5 / np.log(2), 4))
check('quiz 3, volume alt: about 1.4 at l=2', abs(2 * np.log(2) - 1.4) < 0.02, round(2 * np.log(2), 4))
check('quiz 3, volume: a critical chain grows by (1/3) log 2 = 0.23 when l doubles', abs(np.log(2) / 3 - 0.23) < 5e-3, round(np.log(2) / 3, 4))

# ---- problem: 2 log M >= (c/3) log l + const, so M grows as l^(c/6), a factor 100^(1/6) from l=10 to 1000
c = 1.0
Mmin = lambda l: np.exp((c / 3 * np.log(l) + const) / 2)
ratio = Mmin(1000) / Mmin(10)
check('problem: M_min(1000)/M_min(10) = 100^(1/6) = 2.15, with M_min the smallest M that the bound allows', abs(ratio - 100 ** (1 / 6)) < 1e-12 and abs(ratio - 2.15) < 5e-3, round(ratio, 4))
check('problem: the bound asks for at least about twice larger M for a block one hundred times longer', 1.5 < ratio < 2.5 and 1000 / 10 == 100, round(ratio, 4))
for l in (10, 100, 1000):
    check(f'problem: with S <= 2 log M the bound is reached at M = e^(const/2) l^(1/6), l={l}',
          abs(2 * np.log(Mmin(l)) - (np.log(l) / 3 + const)) < 1e-12, round(Mmin(l), 4))
for l in (4, 10, 20):
    check(f'problem: a volume law l log 2 needs M >= 2^(l/2), l={l}', abs(2 * np.log(2 ** (l / 2)) - l * np.log(2)) < 1e-12, 2 ** (l / 2))


# ---- problem: the bound is only a lower bound. The Schmidt weights of a block of the infinite XX chain (free fermions,
# hopping 1, half filling) are the products over the modes nu of nu or 1-nu. An MPS keeps at most M^2 of them for a block
# with two ends, so a dropped weight of at most 1e-6 needs M >= ceil(sqrt(count)).
def schmidt_count(nu, eps):
    """Number of the largest many-body Schmidt weights whose sum reaches 1 - eps, by a best-first walk over the products."""
    import heapq
    p = np.maximum(nu, 1 - nu)
    r = np.sort((1 - p) / p)[::-1]
    heap, tot, n = [(-np.prod(p), -1)], 0.0, 0
    while tot < 1 - eps:
        w, last = heapq.heappop(heap)
        tot -= w; n += 1
        if last + 1 < len(r):
            heapq.heappush(heap, (w * r[last + 1], last + 1))
            if last >= 0:
                heapq.heappush(heap, (w / r[last] * r[last + 1], last + 1))
    return n


def modes(C):
    nu = np.linalg.eigvalsh(C)
    return nu[(nu > 1e-13) & (nu < 1 - 1e-13)]


nu10, nu1000 = modes(C[:10, :10]), modes(C[:1000, :1000])
# second route at l=10: all 2^10 products of the ten modes, sorted
prods = np.ones(1)
for x in nu10:
    prods = np.concatenate([prods * x, prods * (1 - x)])
prods = np.sort(prods)[::-1]
n_brute = int(np.searchsorted(np.cumsum(prods), 1 - 1e-6) + 1)
n10, n1000 = schmidt_count(nu10, 1e-6), schmidt_count(nu1000, 1e-6)
check('problem: l=10 has 10 modes and the walk counts the 2^10 products as the brute force does', len(nu10) == 10 and n10 == n_brute, (n10, n_brute))
M10, M1000 = int(np.ceil(np.sqrt(n10))), int(np.ceil(np.sqrt(n1000)))
check('problem: a dropped weight of at most 1e-6 needs M >= 10 at l=10 (82 weights)', n10 == 82 and M10 == 10, (n10, M10))
check('problem: a dropped weight of at most 1e-6 needs M >= 69 at l=1000 (4747 weights)', n1000 == 4747 and M1000 == 69, (n1000, M1000))
check('problem: a factor of about 7, faster than the factor 2.15 of the bound', abs(M1000 / M10 - 7) < 0.15 and M1000 / M10 > ratio, M1000 / M10)
check('problem: still far from the volume law, 69 against 2^(l/2) = 2^500 at l=1000', np.log2(M1000) < 1000 / 2 / 50, round(np.log2(M1000), 3))

# ---- problem and fold: an MPS keeps at most M^2 Schmidt weights of a block with two ends, one for each pair of values of
# the two bonds, and M at one cut. A random MPS with M=3 on 10 sites: rank 9 for the sites 3 to 6, rank 3 for the first 5 sites.
rng = np.random.default_rng(7)
Mb, Lr = 3, 10
Dr = [min(Mb, 2 ** i, 2 ** (Lr - i)) for i in range(Lr + 1)]
psi = np.ones((1, 1))
for i in range(Lr):
    A = rng.normal(size=(Dr[i], 2, Dr[i + 1]))
    psi = np.einsum('xa,asb->xsb', psi, A).reshape(-1, Dr[i + 1])
psi = psi.reshape([2] * Lr)
rank_block = np.linalg.matrix_rank(np.transpose(psi, (3, 4, 5, 6, 0, 1, 2, 7, 8, 9)).reshape(16, -1), tol=1e-10)
rank_cut = np.linalg.matrix_rank(psi.reshape(2 ** 5, -1), tol=1e-10)
check('fold and problem: a block with two ends of an MPS with M=3 has rank M^2 = 9, so S <= 2 log M', rank_block == 9, rank_block)
check('fold: one cut of the same MPS has rank M = 3, so S <= log M', rank_cut == 3, rank_cut)

# ---- lab box: k_B T / J = 0.03 with J = 0.90 meV is about 0.3 K, our conversion
kB = 8.617333262e-2  # meV per K
T = 0.03 * 0.90 / kB
check('lab: 0.03 J with J=0.90 meV is about 0.3 K', abs(T - 0.3) < 0.02, round(T, 4))
# the two numbers of the source, read in the stored abstract (labsource --check lists only the first)
src = os.path.join(HERE, '..', '..', 'sources', 'session07', 'hammar1998_arxivcond-mat-9809068.txt')
with open(src) as f:
    text = ' '.join(f.read().split())
check('lab: the stored abstract states J=0.90(1) meV', 'exchange constant J=0.90(1) meV' in text, 'J=0.90(1) meV')
check('lab: the stored abstract states gapless and paramagnetic for k_B T/J at least down to 0.03',
      'remains gapless and paramagnetic' in text and 'k_B T/J at least down to 0.03' in text, '0.03')
check('lab, our reading: the abstract measures the specific heat and does not name an entanglement entropy',
      'specific heat' in text and 'entangle' not in text.lower(), 'no entanglement entropy')


# ---- second route for the caption and for quiz 3: numpy on the open chain, with no pyqula, the same blocks in the middle
def open_chain_C(N, t_even, t_odd):
    """Correlation matrix of the half-filled open chain with hopping t_even on the bonds (2n, 2n+1) and t_odd on the others."""
    H = np.zeros((N, N))
    for i in range(N - 1):
        H[i, i + 1] = H[i + 1, i] = -(t_even if i % 2 == 0 else t_odd)
    w, v = np.linalg.eigh(H)
    assert w[N // 2 - 1] < -1e-9 and w[N // 2] > 1e-9   # no level at zero energy
    return v[:, :N // 2] @ v[:, :N // 2].T


for N, ell in [(402, [2, 4, 6, 8, 10, 14, 20, 28, 40, 56, 80, 100]), (3002, [10, 32, 100, 316, 1000])]:
    st = [2 * ((N // 2 - x // 2) // 2) for x in ell]
    Cc, Cd = open_chain_C(N, 1.0, 1.0), open_chain_C(N, 1.0, 0.6)
    Sn = np.array([entropy(Cc[s:s + x, s:s + x]) for s, x in zip(st, ell)])
    Dn = np.array([entropy(Cd[s:s + x, s:s + x]) for s, x in zip(st, ell)])
    ell = np.array(ell, float)
    if N == 402:
        check('quiz 3, critical: the open chain of the pictures has 402 sites', ec.N == 402 == N, ec.N)
        check('numpy, quiz 3: the helper of the pictures (pyqula) gives the numpy critical chain', np.allclose(Sn, Sc, atol=1e-6), np.round(Sn, 4))
        check('numpy, quiz 3: the helper of the pictures (pyqula) gives the numpy dimerized chain', np.allclose(Dn, Sg, atol=1e-6), np.round(Dn, 4))
    else:
        line = np.log(ell) / 3 + const
        check('numpy, caption: 1.49 at l=10 on 3002 sites', abs(Sn[0] - 1.49) < 5e-3, round(Sn[0], 4))
        check('numpy, caption: 2.96 at l=1000 (2.9649, close to the rounding edge 2.965)', abs(Sn[-1] - 2.96) < 5e-3 and round(Sn[-1], 2) == 2.96, round(Sn[-1], 5))
        check('numpy, caption: on the line 1/3 log l + 0.73 up to l=316', np.all(np.abs(Sn[:-1] - line[:-1]) < 0.01), np.round(Sn - line, 4))
        check('numpy, caption: a little below the line at l=1000', -0.08 < Sn[-1] - line[-1] < -0.04, round(Sn[-1] - line[-1], 4))
        check('numpy, caption: the dimerized chain stays at about 0.5', np.all(np.abs(Dn - 0.5) < 5e-3), np.round(Dn, 4))
        check('numpy, quiz 1 figure: the critical chain grows by about 1.5 from l=10 to 1000', abs(Sn[-1] - Sn[0] - 1.5) < 0.05, round(Sn[-1] - Sn[0], 4))

# ---- fold: one end of a block gives half of the logarithm of two ends, c/6 against c/3, so the two ends double the bound
Ls = np.array([100, 200, 400, 800])
half = np.array([entropy(open_chain_C(n, 1.0, 1.0)[:n // 2, :n // 2]) for n in Ls])
s1 = np.polyfit(np.log(Ls), half, 1)[0]
check('fold and key box: one end, the left half of an open chain, grows as (1/6) log L', abs(s1 - 1 / 6) < 5e-3, round(s1, 4))
check('fold: a block with two ends grows twice as fast as one end', abs(slope / s1 - 2) < 0.06, round(slope / s1, 4))


# ---- caption: the point at l=1000 is below the line since the chain is only three times longer than the block. The uniform
# open chain of N sites has the modes sqrt(2/(N+1)) sin(pi k (i+1)/(N+1)), k=1..N/2 filled, so longer chains are cheap.
def open_block_entropy(N, l):
    s = 2 * ((N // 2 - l // 2) // 2)
    Phi = np.sqrt(2 / (N + 1)) * np.sin(np.pi * np.outer(np.arange(s, s + l) + 1, np.arange(1, N // 2 + 1)) / (N + 1))
    return entropy(Phi @ Phi.T)


check('caption: the chain of 3002 sites is three times longer than the block of 1000', abs(3002 / 1000 - 3) < 0.01, 3002 / 1000)
dev = [open_block_entropy(Nn, 1000) - (np.log(1000) / 3 + const) for Nn in (3002, 6002, 30002)]
check('caption: the sine modes give the 2.9649 of the eigenvectors on 3002 sites', abs(dev[0] + np.log(1000) / 3 + const - Sn[-1]) < 1e-8, round(dev[0], 4))
check('caption: the point at l=1000 goes to the line as the chain grows, so the finite chain is the cause',
      dev[0] < dev[1] < dev[2] < 0 and dev[0] < -0.05 and abs(dev[2]) < 2e-3, np.round(dev, 4))


# ---- fold: the cut of a MERA. Every cut that separates the block from the rest gives a bound, and the best one has the
# fewest bonds, which is a minimal cut. A binary MERA on a ring of 2^11 sites, disentanglers on the positions (2j+1, 2j+2)
# and isometries on (2j, 2j+1), every bond of capacity 1, and the minimal cut of a block from a maximum flow.
def mera_mincuts(n, ells, offsets):
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import maximum_flow
    Nm = 2 ** n
    edges, below, nid, Nt = [], list(range(Nm)), Nm, Nm
    while Nt > 1:
        nu_ = Nt // 2
        u, w = list(range(nid, nid + nu_)), list(range(nid + nu_, nid + 2 * nu_))
        nid += 2 * nu_
        for j in range(nu_):
            edges += [(below[2 * j + 1], u[j]), (below[(2 * j + 2) % Nt], u[j]), (u[j], w[j]), (u[j], w[((2 * j + 2) % Nt) // 2])]
        below, Nt = w, nu_
    edges.append((below[0], nid)); nid += 1
    src, snk = nid, nid + 1
    out = {}
    for l in ells:
        cuts = []
        for a in offsets:
            cap = {}
            for x, y in edges:
                cap[(x, y)] = cap.get((x, y), 0) + 1
                cap[(y, x)] = cap.get((y, x), 0) + 1
            for p in range(Nm):
                cap[(src, p) if a <= p < a + l else (p, snk)] = 10 ** 6
            keys = list(cap)
            G = csr_matrix(([cap[k] for k in keys], ([k[0] for k in keys], [k[1] for k in keys])), shape=(nid + 2, nid + 2), dtype=np.int32)
            cuts.append(maximum_flow(G, src, snk).flow_value)
        out[l] = cuts
    return out


cuts = mera_mincuts(11, (16, 64, 256), range(600, 608))
for l, cl in cuts.items():
    check(f'fold: the best cut of a block of {l} sites crosses 2 log2 l +- 1 bonds, about one per layer at each end',
          all(abs(x - 2 * np.log2(l)) <= 1 for x in cl), (2 * np.log2(l), cl))


# ---- lab box, our reading: c=1 for the spin-1/2 Heisenberg chain, from exact diagonalization of a ring of 16 spins
def heisenberg_ring_ground(L):
    import scipy.sparse as sp
    import scipy.sparse.linalg as sla
    states = np.arange(2 ** L)
    rows, cols, vals, diag = [], [], [], np.zeros(2 ** L)
    for i in range(L):
        j = (i + 1) % L
        bi, bj = (states >> i) & 1, (states >> j) & 1
        diag += np.where(bi == bj, 0.25, -0.25)
        s = states[bi != bj]
        rows.append(s ^ ((1 << i) | (1 << j))); cols.append(s); vals.append(np.full(s.size, 0.5))
    rows.append(states); cols.append(states); vals.append(diag)
    H = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(2 ** L, 2 ** L))
    w, v = sla.eigsh(H, k=1, which='SA', tol=1e-10)
    return w[0], v[:, 0]


Lh = 16
E0, psi = heisenberg_ring_ground(Lh)
check('lab: the ring of 16 spins has the energy per site -0.44639 of the conventions sheet', abs(E0 / Lh + 0.44639) < 1e-5, round(E0 / Lh, 6))
Sh = []
for x in range(1, Lh // 2 + 1):
    p = np.linalg.svd(psi.reshape(-1, 2 ** x), compute_uv=False) ** 2   # site i is bit i, so the first x sites
    p = p[p > 1e-14]
    Sh.append(-np.sum(p * np.log(p)))
xs = np.arange(1, Lh // 2 + 1)
chord = np.log(Lh / np.pi * np.sin(np.pi * xs / Lh))   # a block of a ring, l replaced by (L/pi) sin(pi l/L)
ch = 3 * np.polyfit(chord[xs >= 2], np.array(Sh)[xs >= 2], 1)[0]
check('lab: the Heisenberg chain has c=1, a fit on the ring of 16 spins gives c within 0.06 of 1', abs(ch - 1) < 0.06, round(ch, 4))


# ---- try-it, corrected on 2026-11-22: the transverse-field Ising chain of the notebook, -sum S^z S^z + B_x sum S^x on an
# open chain, at the cut of the notebook after L/2 + 1 sites. Route 1: the Majorana correlation matrix of the free fermions
# of Jordan-Wigner. Route 2: exact diagonalization of 12 sites. The exact entropy is largest below B_x = 0.5, on the ordered
# side, at 0.37 for 20 sites and 0.44 for 40 sites, where it is close to ln 2, the even superposition of the two
# ferromagnetic states, and it has fallen at 0.5
def tfim_majorana(L, Bx):
    n = 2 * L
    A = np.zeros((n, n))
    for i in range(L):
        A[2 * i, 2 * i + 1] = Bx / 2
    for i in range(L - 1):
        A[2 * i + 1, 2 * i + 2] = -0.25
    A = A - A.T
    w, v = np.linalg.eigh(1j * A)
    G = 2 * (v[:, w < 0] @ v[:, w < 0].conj().T) - np.eye(n)
    l = L // 2 + 1
    nu = np.clip(np.linalg.eigvalsh(G[:2 * l, :2 * l]), 0, 1)
    p = (1 + nu[nu > 1e-12]) / 2
    p = p[p < 1 - 1e-14]
    return float(-np.sum(p * np.log(p) + (1 - p) * np.log(1 - p)))


def tfim_ed(L, Bx):
    import scipy.sparse as sps, scipy.sparse.linalg as spl
    sx = sps.csr_matrix([[0, 0.5], [0.5, 0]]); sz = sps.csr_matrix([[0.5, 0], [0, -0.5]])
    op = lambda o, i: sps.kron(sps.kron(sps.identity(2 ** i), o), sps.identity(2 ** (L - i - 1)), format='csr')
    H = sum(-op(sz, i) @ op(sz, i + 1) for i in range(L - 1)) + Bx * sum(op(sx, i) for i in range(L))
    w, v = spl.eigsh(H, k=1, which='SA', tol=1e-12)
    p = np.linalg.svd(v[:, 0].reshape(2 ** (L // 2 + 1), -1), compute_uv=False) ** 2
    p = p[p > 1e-15]
    return float(-np.sum(p * np.log(p)))


two = [abs(tfim_majorana(12, b) - tfim_ed(12, b)) for b in (0.3, 0.5, 0.8)]
check('try-it, the free fermions of the Ising chain give the exact diagonalization of 12 sites', max(two) < 1e-8, max(two))
grid = np.round(np.arange(0.20, 0.705, 0.01), 2)
peak = {}
for Lt in (20, 40):
    St = np.array([tfim_majorana(Lt, b) for b in grid])
    k = int(np.argmax(St))
    peak[Lt] = (grid[k], St[k], St[list(grid).index(0.30)], St[list(grid).index(0.50)])
check('try-it, the exact peak is below B_x = 0.5, at 0.37 for 20 sites and 0.44 for 40 sites, and near ln 2 on the ordered side',
      peak[20][0] == 0.37 and peak[40][0] == 0.44 and all(abs(peak[L][2] - np.log(2)) < 0.01 for L in peak)
      and abs(peak[20][3] - 0.4427) < 5e-4 and abs(peak[40][3] - 0.5050) < 5e-4, peak)
# the notebook box, corrected on 2026-11-22: the cell scans B_x for one length, L = 40, and its quiz asks to make the
# system smaller. At large B_x the exact entropy at the cut is the same for 20 and 40 sites, and at the transition it grows
nbtxt = open(os.path.join(HERE, '..', '..', '..', 'jupyter-notebooks', 'session7.ipynb'), encoding='utf-8').read()
same = [abs(tfim_majorana(20, b) - tfim_majorana(40, b)) for b in (0.8, 1.0)]
grow = tfim_majorana(40, 0.5) - tfim_majorana(20, 0.5)
check('notebook box, at B_x = 0.8 and 1 the entropy is the same for 20 and 40 sites, at 0.5 it grows by 0.062',
      max(same) < 1e-3 and abs(grow - 0.0623) < 5e-4 and 'L = 40 # length of the system' in nbtxt
      and 'Make the system smaller, what happens and why?' in nbtxt, (max(same), round(grow, 4)))
print('all checks of page 11 hold')
