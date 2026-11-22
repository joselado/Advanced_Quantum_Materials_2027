"""Checks of webnotes/conventions/session10.md, with numbers. Every line of the sheet has one check here, in the order
of the sheet, and every number of the line is asserted. It prints one line per check and exits 0 when all hold.

The figure scripts of webnotes/figures/session10/ write their SVG when they run, so the checks never run them. Where a
line quotes a figure, the check repeats the computation of the script with its seed and its parameters, and where a
line quotes the widget netfit, the check calls the compute function of webnotes/widgets/defs/netfit.py. The Monte
Carlo numbers are asserted with tolerances wider than their statistical error, and the numbers that depend on a seed
are asserted as ranges over the seeds that the sheet names.

Not asserted, since they are not a short calculation or not a number: the sentences on the release 0.0.96 of pyqula,
which were read in its code and not run, the units of (10.8), the Fashion-MNIST accuracies of Section 10.4, which
the check of that page reads on the slides of the lecture, the sizes of the trained classifiers of Section 10.6,
which are in the figures of the same slides, and the SVG of ham_learning.py that is not the same file at every run, of which the check asserts only the levels on the edges of
the bins, which were not shown to be the cause.

The numbers that break first when pyqula, numpy or the BLAS library change are the magnetic state of the mean field
from the seed 0, the moment of 5e-7 of the guess mf="potential", the Monte Carlo of the figures with their seeds and
the side of the bin edge on which the levels at 0.7 fall. Their tolerances are tight, so a failure there asks for a
new number on the sheet and not for a new convention.

Run it from anywhere:  python3 webnotes/checks/session10/conventions.py"""
import os, sys, io, re, contextlib, importlib, importlib.util, runpy, tempfile, time
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_v, '1')     # small matrices, threads only cost time on a busy machine
import numpy as np

WEBNOTES = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COUNT = [0]
SX = np.array([[0.0, 1.0], [1.0, 0.0]])
SY = np.array([[0.0, -1j], [1j, 0.0]])
SZ = np.diag([1.0, -1.0])


def check(name, ok, detail):
    """Prints one line for a check and stops the script when it does not hold."""
    print(('ok    ' if ok else 'FAIL  ') + name + ': ' + detail, flush=True)
    assert ok, name
    COUNT[0] += 1


def quiet(f, *args, **kwargs):
    """Calls f with its printed output thrown away, for dmrgpy and pyqula, which print progress."""
    with contextlib.redirect_stdout(io.StringIO()):
        return f(*args, **kwargs)


# ---------------------------------------------------------------------------------------------- spins in (10.2)
# The configuration of index b has the spin s_i = +1 (up) when the bit L-1-i of b is 0, which is the order of np.kron
# with the site 0 first and the up state first.

def configurations(L):
    b = np.arange(2 ** L)
    return 1 - 2 * ((b[:, None] >> np.arange(L - 1, -1, -1)) & 1)


def mask(i, L):
    return 1 << (L - 1 - i)


def heisenberg(L, periodic=False, J=1.0):
    """J sum S_i.S_j with S = sigma/2, built element by element in the basis of (10.2)."""
    S, n = configurations(L), 2 ** L
    H = np.zeros((n, n))
    for i in range(L if periodic else L - 1):
        j = (i + 1) % L
        H[np.arange(n), np.arange(n)] += J / 4 * S[:, i] * S[:, j]
        anti = np.nonzero(S[:, i] != S[:, j])[0]
        H[anti, anti ^ (mask(i, L) | mask(j, L))] += J / 2
    return H


def site(o, i, L):
    out = np.array([[1.0]])
    for j in range(L):
        out = np.kron(out, o if j == i else np.eye(2))
    return out


def heisenberg_kron(L, J=1.0):
    """The same open chain from Kronecker products of the Pauli matrices, a second route."""
    return sum(J / 4 * site(o, i, L) @ site(o, i + 1, L) for i in range(L - 1) for o in (SX, SY, SZ)).real


def tfim(L, J=1.0, h=1.0):
    """-J sum sigma^z_i sigma^z_i+1 - h sum sigma^x_i on a ring, in the basis of (10.2)."""
    S, n = configurations(L), 2 ** L
    H = np.diag(-J * sum(S[:, i] * S[:, (i + 1) % L] for i in range(L)).astype(float))
    for i in range(L):
        H[np.arange(n), np.arange(n) ^ mask(i, L)] += -h
    return H


def jordan_wigner(L, J=1.0, h=1.0):
    k = (2 * np.arange(L) + 1) * np.pi / L
    return -np.sum(np.sqrt(J ** 2 + h ** 2 - 2 * J * h * np.cos(k)))


# -------------------------------------------------------------------------------- the restricted Boltzmann machine

def rbm(par, L, M, S):
    """C(s) = exp(sum_i a_i s_i) prod_j 2 cosh(theta_j), theta_j = b_j + sum_i W_ji s_i, and the theta_j."""
    a, b, W = par[:L], par[L:L + M], par[L + M:].reshape(M, L)
    th = b[None, :] + S @ W.T
    return np.exp(S @ a) * np.prod(2 * np.cosh(th), axis=1), th


def rbm_O(par, L, M, S):
    """O_k = d ln C / d theta_k, in the order a, b, W."""
    t = np.tanh(rbm(par, L, M, S)[1])
    return np.hstack([S, t, (t[:, :, None] * S[:, None, :]).reshape(len(S), -1)])


def energy(H, C):
    return float(np.real(np.vdot(C, H @ C)) / np.real(np.vdot(C, C)))


def force(H, C, O):
    """F_k = <E_loc O_k*> - <E_loc><O_k*> with p = |C|^2 / sum |C|^2."""
    p = np.abs(C) ** 2 / np.sum(np.abs(C) ** 2)
    El = (H @ C) / C
    return p @ (El[:, None] * O.conj()) - (p @ El) * (p @ O.conj())


# ---------------------------------------------------------------------------------------------- the other helpers

def figure_ising_sizes():
    """The computation of figures/session10/ising_sizes.py, with its seed, its order of the random numbers and its
    1500 + 3000 sweeps, which returns <|m|> at every temperature for L = 8, 16 and 32."""
    rng = np.random.default_rng(7)
    Ts = np.linspace(1.5, 3.5, 21)
    out = {}
    for L in (8, 16, 32):
        s = np.ones((L, L), dtype=int)
        mk = (np.add.outer(np.arange(L), np.arange(L)) % 2).astype(bool)
        m = []
        for T in Ts:
            acc = 0.0
            for sweep in range(4500):
                for sub in (mk, ~mk):
                    nb = np.roll(s, 1, 0) + np.roll(s, -1, 0) + np.roll(s, 1, 1) + np.roll(s, -1, 1)
                    flip = sub & (rng.random((L, L)) < np.exp(-2 * s * nb / T))
                    s[flip] *= -1
                if sweep >= 1500:
                    acc += abs(s.mean())
            m.append(acc / 3000)
        out[L] = dict(zip(np.round(Ts, 2), m))
    return out


def ising_snapshots(T, rng, L=16, nth=500, ns=1500, every=2):
    """Checkerboard Metropolis from all spins up, the m of a snapshot every `every` sweeps after nth sweeps, as in
    figures/session10/igt_hist.py."""
    s = np.ones((L, L), dtype=int)
    mk = (np.add.outer(np.arange(L), np.arange(L)) % 2).astype(bool)
    out = []
    for sweep in range(nth + ns * every):
        for sub in (mk, ~mk):
            nb = np.roll(s, 1, 0) + np.roll(s, -1, 0) + np.roll(s, 1, 1) + np.roll(s, -1, 1)
            flip = sub & (rng.random((L, L)) < np.exp(-2 * s * nb / T))
            s[flip] *= -1
        if sweep >= nth and (sweep - nth) % every == 0:
            out.append(s.mean())
    return np.array(out)


def gauge_links(L, bits):
    """The link spins of an L x L torus from the bits of a configuration, h[x, y] from (x, y) to (x+1, y) and v[x, y]
    from (x, y) to (x, y+1), as in igt_hist.py. bits has the shape (number of configurations, 2 L^2)."""
    s = 1 - 2 * bits
    return s[:, :L * L].reshape(-1, L, L), s[:, L * L:].reshape(-1, L, L)


def plaquettes(h, v):
    """The plaquette at (x, y) is h[x, y] v[x+1, y] h[x, y+1] v[x, y], on the last two axes."""
    return h * np.roll(v, -1, -2) * np.roll(h, -1, -1) * v


def torus_index(L):
    """The indices of the four links of every star and of every plaquette of the L x L torus, with h[x, y] at the index
    x L + y and v[x, y] at L^2 + x L + y, the order of gauge_links."""
    hi_ = lambda x, y: (x % L) * L + (y % L)
    vi_ = lambda x, y: L * L + (x % L) * L + (y % L)
    stars = [[hi_(x, y), hi_(x - 1, y), vi_(x, y), vi_(x, y - 1)] for x in range(L) for y in range(L)]
    plaqs = [[hi_(x, y), vi_(x + 1, y), hi_(x, y + 1), vi_(x, y)] for x in range(L) for y in range(L)]
    return stars, plaqs


def enumerate_torus(L):
    n = 2 * L * L
    bits = ((np.arange(2 ** n)[:, None] >> np.arange(n)) & 1).astype(np.int8)
    h, v = gauge_links(L, bits)
    return h, v, plaquettes(h, v).reshape(len(bits), -1)


def rank_gf2(A):
    A = (A.copy() % 2).astype(np.int8)
    r = 0
    for c in range(A.shape[1]):
        piv = np.nonzero(A[r:, c])[0]
        if len(piv) == 0:
            continue
        A[[r, r + piv[0]]] = A[[r + piv[0], r]]
        for i in np.nonzero(A[:, c])[0]:
            if i != r:
                A[i] ^= A[r]
        r += 1
        if r == A.shape[0]:
            break
    return r


def tree_count(n, D=10, d=2, label=2, cut=False, separate=False, halving=False):
    """The parameters of a binary tree tensor network on n pixels. The tree pairs neighbors level by level, an odd one
    carried up, or with halving=True splits the pixels into two halves again and again. The top tensor carries the
    label leg, or with separate=True it has a bond D and a separate D x label tensor follows. With cut=True a bond
    has min(D, product of the legs below) in place of D."""
    def bond(a, b, top):
        if top and not separate:
            return label
        return min(D, a * b) if cut else D
    if halving:
        def rec(m, top):
            if m == 1:
                return 0, d
            ta, la = rec(m // 2, False)
            tb, lb = rec(m - m // 2, False)
            out = bond(la, lb, top)
            return ta + tb + la * lb * out, out
        total, top = rec(n, True)
    else:
        legs, total = [d] * n, 0
        while len(legs) > 1:
            new = []
            for i in range(0, len(legs) - 1, 2):
                out = bond(legs[i], legs[i + 1], len(legs) == 2)
                total += legs[i] * legs[i + 1] * out
                new.append(out)
            if len(legs) % 2:
                new.append(legs[-1])
            legs = new
        top = legs[0]
    return total + (top * label if separate else 0)


def ks_toy(U=2.0, alpha=0.3, N=60, NE=40):
    """The loop of figures/session10/ks_loop.py: an open chain with hopping -1, the well, the Hartree term U n(i) on the
    total density, the uniform density as the start and the new density mixed with the weight alpha."""
    x = np.arange(N)
    vext = -2.0 * np.exp(-((x - 29.5) / 7.0) ** 2)
    T = -np.eye(N, k=1) - np.eye(N, k=-1)

    def new(n):
        w = np.linalg.eigh(T + np.diag(vext + U * n))[1]
        return 2 * (np.abs(w[:, :NE // 2]) ** 2).sum(axis=1)
    n, hist, res = np.full(N, NE / N), [], []
    hist.append(n.copy())
    for it in range(200):
        nn = new(n)
        res.append(np.abs(nn - n).max())
        n = (1 - alpha) * n + alpha * nn
        hist.append(n.copy())
        if res[-1] < 1e-10:
            break
    return np.array(hist), np.array(res), vext, new


def uhf(vext, U, start, NE=40, mix=0.3, tol=1e-10):
    """A collinear Hubbard mean field in numpy, the lowest NE of the levels of both spins filled. Returns the densities
    of the two spins and the energy sum of the filled levels minus U sum n_up n_down."""
    N = len(vext)
    T = -np.eye(N, k=1) - np.eye(N, k=-1)
    nu, nd = start

    def step(nu, nd):
        eu, wu = np.linalg.eigh(T + np.diag(vext + U * nd))
        ed, wd = np.linalg.eigh(T + np.diag(vext + U * nu))
        e = np.concatenate([eu, ed])
        k = np.argsort(e)[:NE]
        return ((np.abs(wu[:, k[k < N]]) ** 2).sum(1), (np.abs(wd[:, k[k >= N] - N]) ** 2).sum(1),
                e[k].sum() - U * np.sum(nu * nd))
    for it in range(20000):
        a, b, E = step(nu, nd)
        err = max(np.abs(a - nu).max(), np.abs(b - nd).max())
        nu, nd = (1 - mix) * nu + mix * a, (1 - mix) * nd + mix * b
        if err < tol:
            break
    return nu, nd, step(nu, nd)[2]


def moments(hmf, NE=40):
    """The density and the local moment vector of each site from the filled states of a spinful pyqula Hamiltonian,
    with the orbitals 2i and 2i+1 the spin up and the spin down of the site i."""
    from pyqula import algebra
    w = np.linalg.eigh(algebra.todense(hmf.intra))[1][:, :NE]
    rho = w @ w.conj().T
    n = np.real(np.diag(rho))
    m = np.array([[2 * np.real(rho[2 * i, 2 * i + 1]), 2 * np.imag(rho[2 * i + 1, 2 * i]), n[2 * i] - n[2 * i + 1]]
                  for i in range(len(n) // 2)])
    return n[0::2] + n[1::2], m


def ring(N, t, t2, onsite=None):
    i = np.arange(N)
    H = np.diag(np.zeros(N) if onsite is None else onsite)
    H[i, (i + 1) % N] = H[(i + 1) % N, i] = -t
    H[i, (i + 2) % N] = H[(i + 2) % N, i] = -t2
    return H


def ham_learning(seed):
    """The computation of figures/session10/ham_learning.py with the seed: the test set of 200 disordered rings, then
    the training on 600 clean rings and on 600 rings with W in [0, 1.5], in the order of the random numbers of the
    script. Returns the three errors, the design matrices and the fraction of the levels outside the window."""
    rng = np.random.default_rng(seed)
    N, edges = 200, np.linspace(-3.5, 3.5, 41)
    H1, H2 = ring(N, 1.0, 0.0), ring(N, 0.0, 1.0)
    sets, outside = [], 0.0
    for n, wmax in ((200, 1.5), (600, 0.0), (600, 1.5)):
        lam, W = rng.uniform(0, 0.4, n), rng.uniform(0, wmax, n)
        O = []
        for a, b in zip(lam, W):
            lv = np.linalg.eigvalsh(H1 + a * H2 + np.diag(rng.uniform(-b, b, N)))
            outside = max(outside, np.mean(np.abs(lv) > 3.5))
            O.append(np.histogram(lv, bins=edges)[0] / N)
        sets.append((np.hstack([np.array(O), np.ones((n, 1))]), lam, W))
    (Xt, lt, Wt) = sets[0]
    out = []
    for X, lam, W in sets[1:]:
        theta = np.linalg.lstsq(X, lam, rcond=None)[0]
        err = Xt @ theta - lt
        out.append((np.sqrt(np.mean(err ** 2)), np.sqrt(np.mean(err[Wt > 1] ** 2)), theta))
    return out[0][0], out[0][1], out[1][0], sets, out, outside


def main():
    """Runs every check. The pyqula and dmrgpy calls may write files, so the caller runs this in a temporary folder."""
    from pyqula import geometry, algebra
    from pyqula.latticeising import LatticeIsing
    from dmrgpy import spinchain
    t0 = time.time()
    rng = np.random.default_rng(2026)

    # Units and signs
    e2, v2 = np.linalg.eigh(-np.kron(SZ, SZ))
    ground = sorted(np.nonzero(np.abs(v2[:, :2]).sum(1) > 1e-9)[0])
    dimer = sum(np.kron(o, o) for o in (SX, SY, SZ)).real
    eh, ep = np.linalg.eigvalsh(dimer / 4), np.linalg.eigvalsh(dimer)
    sc = spinchain.Spin_Chain(['S=1/2'] * 2)
    sc.set_hamiltonian(sum(getattr(sc, o)[0] * getattr(sc, o)[1] for o in ('Sx', 'Sy', 'Sz')))
    edm = quiet(sc.gs_energy, mode='ED')
    ok = np.allclose(e2[:2], -1) and ground == [0, 3] and np.allclose(eh, [-0.75, 0.25, 0.25, 0.25])
    is81 = np.kron(SZ, SZ) / 4                        # (8.1) of Session 8, S^z_0 S^z_1, in the basis up up, up dn, dn up, dn dn
    ok = ok and np.allclose(np.diag(is81), [0.25, -0.25, -0.25, 0.25]) and np.abs(is81 - (-(-0.25)) * np.kron(SZ, SZ)).max() < 1e-15
    check('the sign of J in (10.9) and in (6.5)', ok and np.allclose(ep, [-3, 1, 1, 1]) and abs(edm + 0.75) < 1e-9,
          '-J s1 s2 with J=1 has its two ground states, up up and down down, at %.0f, J S1.S2 with S = sigma/2 has the '
          'singlet at %.2f and the triplet at %+.2f (dmrgpy %.4f), and with Pauli matrices %.0f and %+.0f, and (8.1) has '
          '%s, which is -J s1 s2 with J = -1/4' % (e2[0], eh[0], eh[1], edm, ep[0], ep[1], np.diag(is81).tolist()))

    # The loss and gradient descent of Section 10.2
    def descent(eta, kappa=1.0, n=6):
        th, out = 1.0, [1.0]
        for _ in range(n):
            g = (kappa * (th + 1e-6) ** 2 / 2 - kappa * (th - 1e-6) ** 2 / 2) / 2e-6
            th -= eta * g
            out.append(th)
        return np.array(out)
    d05, d1, d2, d25 = descent(0.5), descent(1.0), descent(2.0), descent(2.5)
    c6, c7 = descent(0.6, 3.0, 40), descent(0.7, 3.0, 40)
    ok = np.allclose(d05, 0.5 ** np.arange(7), atol=1e-8) and np.allclose(d1[1:], 0, atol=1e-8)
    ok = ok and np.allclose(d2, (-1.0) ** np.arange(7), atol=1e-7) and np.allclose(d25, (-1.5) ** np.arange(7), rtol=1e-7)
    check('gradient descent on L = theta^2/2', ok and abs(c6[-1]) < 1e-3 and abs(c7[-1]) > 10,
          'a numerical gradient gives theta -> (1 - eta) theta, eta=0.5 halves theta, eta=1 reaches 0 in one step, '
          'eta=2 jumps between +1 and -1, eta=2.5 multiplies theta by %.2f and the loss by %.2f, and with the curvature 3 '
          'eta=0.6 converges (%.0e after 40 steps) and eta=0.7 does not (%.0f)'
          % (d25[1], (d25[2] / d25[1]) ** 2, abs(c6[-1]), abs(c7[-1])))

    from scipy.optimize import linprog
    P4 = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], float)
    y4 = np.array([0, 1, 1, 0], float)
    sg = 2 * y4 - 1
    # maximize the margin t with sg (w.x + b) >= t and |w|, |b| <= 1; a separating line would give t > 0
    lp = linprog([0, 0, 0, -1], A_ub=np.hstack([-sg[:, None] * np.hstack([P4, np.ones((4, 1))]), np.ones((4, 1))]),
                 b_ub=np.zeros(4), bounds=[(-1, 1)] * 3 + [(None, 1)])
    X4 = np.hstack([P4, np.ones((4, 1))])
    fit = X4 @ np.linalg.lstsq(X4, y4, rcond=None)[0]
    step = lambda z: (z > 0).astype(float)
    xor = step(P4.sum(1) - 0.5) - step(P4.sum(1) - 1.5)
    check('XOR', lp.status == 0 and abs(lp.x[3]) < 1e-9 and np.allclose(fit, 0.5) and abs(np.sum((fit - y4) ** 2) - 1) < 1e-12
          and np.array_equal(xor, y4),
          'the largest margin of a line is %.0e, so no line separates the classes, the best linear fit is %.2f at the four '
          'corners with the loss (10.1) equal to %.2f, and the two step neurons x+y=1/2 and x+y=3/2 with the output '
          'their difference give %s' % (abs(lp.x[3]), fit[0], np.sum((fit - y4) ** 2), xor.astype(int)))

    spec = importlib.util.spec_from_file_location('netfit', os.path.join(WEBNOTES, 'widgets', 'defs', 'netfit.py'))
    netfit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(netfit)
    loss, npar = {}, {}
    for H in range(1, 13):
        r = netfit.compute({'H': H})
        loss[H] = 10 ** r['panels'][1]['series'][0]['y'][-1] - 1e-12
        npar[H] = int(re.search(r'neurons, (\d+) parameters', r['text']).group(1))
    npts, nsteps = len(r['panels'][0]['series'][1]['x']), int(r['panels'][1]['series'][0]['x'][-1])
    xs = np.linspace(-1, 1, 41)
    zero = np.mean(np.sin(3 * np.pi * xs) ** 2)
    xe = (np.arange(-6, 6) + 0.5) / 3
    extrema = np.sum((xe >= -1) & (xe <= 1))
    par = netfit.META['params'][0]
    ok = all(npar[H] == 3 * H + 1 for H in loss) and extrema == 6 and (par['min'], par['max'], par['value']) == (1, 12, 3)
    ok = ok and (npts, nsteps) == (41, 4000) and np.allclose(r['panels'][0]['series'][1]['x'], xs)
    ok = ok and all(abs(loss[H] - v) < 0.005 for H, v in ((1, 0.46), (2, 0.38), (3, 0.23))) and abs(zero - 0.49) < 0.005
    ok = ok and all(loss[H] < 1e-2 for H in range(4, 13)) and loss[7] > loss[5] and loss[6] > loss[5]
    ok = ok and all(abs(loss[H] / v - 1) < 0.07 for H, v in ((4, 7.3e-3), (5, 3.0e-3), (6, 3.4e-3), (7, 5.0e-3), (12, 2.3e-4)))
    check('the widget netfit', ok,
          'sin(3 pi x) has %d extrema on [-1, 1], the widget trains on %d points, has 3H+1 parameters and starts at H=%d, '
          'and the mean squared error after %d steps of Adam is %s for H=1 to 12, against %.3f for an output that is zero'
          % (extrema, npts, par['value'], nsteps, ' '.join('%.1e' % loss[H] for H in range(1, 13)), zero))

    # The table of coefficients and the variational principle
    largest = lambda nbytes: int(np.floor(np.log2(nbytes / 16)))
    b40, b30, b26, b20 = (16 * 2.0 ** L for L in (40, 30, 26, 20))
    Lmps = max(L for L in range(1, 1000) if L * 2 * 100 * 16 < 1e6)
    ok = (largest(16e9), largest(1e12), largest(16 * 2 ** 30), largest(2 ** 40)) == (29, 35, 30, 36)
    ok = ok and 2 ** 30 * 16 == 16 * 2 ** 30 and abs(b40 / 1e12 - 17.59) < 0.01 and b40 / 2 ** 40 == 16
    ok = ok and abs(b30 / 1e9 - 17.18) < 0.01 and abs(b26 / 1e9 - 1.07) < 0.005 and abs(b20 / 1e6 - 16.8) < 0.05
    check('the memory of the table of (10.2)', ok and 300 * 3200 == 960000 and Lmps == 312,
          '16 bytes per coefficient, so 16e9 bytes hold L=%d and 1e12 bytes L=%d, 16 GiB and 1 TiB hold L=30 and 36 '
          'exactly, L=40 needs %.3e bytes, %.1f TB or %.0f TiB, L=30 needs %.1f GB, L=26 %.2f GB, L=20 %.1f MB, and the MPS '
          'with D=10, d=2 is 960000 bytes at L=300, below 1e6 bytes up to L=%d'
          % (largest(16e9), largest(1e12), b40, b40 / 1e12, b40 / 2 ** 40, b30 / 1e9, b26 / 1e9, b20 / 1e6, Lmps))

    H8 = heisenberg(8)
    E8, V8 = np.linalg.eigh(H8)
    ek = np.linalg.eigvalsh(heisenberg_kron(8))[0]
    sc = spinchain.Spin_Chain(['S=1/2'] * 8)
    sc.set_hamiltonian(sum(getattr(sc, o)[i] * getattr(sc, o)[i + 1] for i in range(7) for o in ('Sx', 'Sy', 'Sz')))
    e8dm = quiet(sc.gs_energy, mode='ED')
    c = rng.normal(size=(2000, 256)) + 1j * rng.normal(size=(2000, 256))
    Er = np.real(np.einsum('ni,ij,nj->n', c.conj(), H8, c)) / np.sum(np.abs(c) ** 2, axis=1)
    cn = c @ V8.conj()
    Eb = (np.abs(cn) ** 2 @ E8) / np.sum(np.abs(cn) ** 2, axis=1)
    ok = abs(E8[0] + 3.374933) < 1e-6 and abs(ek - E8[0]) < 1e-10 and abs(e8dm - E8[0]) < 1e-6
    check('the variational principle (10.3)', ok and np.abs(Er - Eb).max() < 1e-14 and -0.3 < Er.min() and Er.max() < 0.3,
          'the open Heisenberg chain of 8 spins has E0 = %.6f J in the basis of (10.2), %.6f J from Kronecker products and '
          '%.6f J in dmrgpy, and 2000 random complex states have E from %.3f to %.3f, each equal to sum |c_n|^2 E_n / '
          'sum |c_n|^2 to %.0e' % (E8[0], ek, e8dm, Er.min(), Er.max(), np.abs(Er - Eb).max()))

    # The restricted Boltzmann machine
    L6, M4 = 6, 4
    S6 = configurations(L6)
    pc = rng.normal(0, 0.4, L6 + M4 + L6 * M4) + 1j * rng.normal(0, 0.4, L6 + M4 + L6 * M4)
    C6 = rbm(pc, L6, M4, S6)[0]
    a, b, W = pc[:L6], pc[L6:L6 + M4], pc[L6 + M4:].reshape(M4, L6)
    hid = configurations(M4)
    explicit = np.array([np.sum(np.exp(s @ a + hid @ b + hid @ (W @ s))) for s in S6])
    check('the RBM amplitude', np.abs(explicit / C6 - 1).max() < 1e-14 and 40 + 40 + 40 * 40 == 1680,
          'the sum over the 2^%d hidden spins of exp(a.s + b.h + h.W s) is exp(a.s) prod_j 2 cosh(b_j + W_j.s) to %.0e, and '
          'N + M + NM is %d for N = M = 40' % (M4, np.abs(explicit / C6 - 1).max(), 40 + 40 + 40 * 40))

    S8 = configurations(8)
    real_min = min(rbm(rng.normal(0, 0.5, 80), 8, 8, S8)[0].min() for _ in range(5))
    cplx_min = min(np.abs(rbm(rng.normal(0, 0.5, 80) + 1j * rng.normal(0, 0.5, 80), 8, 8, S8)[0]).min() for _ in range(20))
    pz = rng.normal(0, 0.5, 80) + 1j * rng.normal(0, 0.5, 80)
    s0 = S8[77]
    pz[8] = 1j * np.pi / 2 - pz[16:24] @ s0          # theta_0 = i pi/2 at the configuration s0
    Cz = rbm(pz, 8, 8, S8)[0]
    check('real and complex parameters', real_min > 0 and cplx_min > 0.08 and abs(Cz[77]) < 1e-12 * np.abs(Cz).max(),
          'real parameters give C(s) > 0 on all 256 configurations (smallest %.1e in 5 draws), 20 draws of complex '
          'parameters give |C(s)| at least %.1e, and the fine-tuned theta_0 = i pi/2 at one configuration gives |C| = '
          '%.0e of the largest' % (real_min, cplx_min, abs(Cz[77]) / np.abs(Cz).max()))

    O6, err = rbm_O(pc, L6, M4, S6), 0.0
    for k in range(len(pc)):
        dp = np.zeros(len(pc)); dp[k] = 1e-6
        fd = np.log(rbm(pc + dp, L6, M4, S6)[0] / rbm(pc - dp, L6, M4, S6)[0]) / 2e-6
        err = max(err, np.abs(fd - O6[:, k]).max())
    check('O_k of the RBM', err < 1e-8,
          'd ln C/d a_i = s_i, d ln C/d b_j = tanh theta_j and d ln C/d W_ji = s_i tanh theta_j agree with finite '
          'differences to %.0e for complex parameters' % err)

    # The local energy, the sampled energy and the gradient
    H10, H10p = heisenberg(10), heisenberg(10, periodic=True)
    off = H10[~np.eye(1024, dtype=bool)]
    row, rowp, total = (H10 != 0).sum(1).max(), (H10p != 0).sum(1).max(), int((H10 != 0).sum())
    diag_ok = np.allclose(np.sort(np.unique(np.round(np.diag(H10) * 4))), np.arange(-9, 10, 2))
    sfig = np.array([1, -1, -1, 1, 1, -1])
    b6 = int(''.join('0' if q > 0 else '1' for q in sfig), 2)
    nfig = int((heisenberg(6)[b6] != 0).sum()) - 1
    ok = np.allclose(np.unique(off[off != 0]), 0.5) and diag_ok and row == 10 and rowp == 11
    check('the matrix elements of the Heisenberg chain', ok and total == 11 * 2 ** 9 == 5632 and nfig == 3,
          'a swap of an antiparallel pair has the element +J/2 and each bond gives +-J/4 on the diagonal, the open chain '
          'of 10 sites has at most %d elements in a row and the periodic one %d, the open one has %d = (L+1) 2^(L-1) in '
          'all, and the s of the figure local_energy is connected to %d other configurations' % (row, rowp, total, nfig))

    pr = rng.normal(0, 0.3, 80) + 1j * rng.normal(0, 0.3, 80)
    Cr = rbm(pr, 8, 8, S8)[0]
    p = np.abs(Cr) ** 2 / np.sum(np.abs(Cr) ** 2)
    El = (H8 @ Cr) / Cr
    Et = energy(H8, Cr)
    gs = np.linalg.eigh(tfim(8))[1][:, 0]
    Elg = (tfim(8) @ gs) / gs
    check('the local energy (10.4)', abs(np.sum(p * El) - Et) < 1e-14 and np.ptp(np.real(Elg)) < 1e-12,
          'sum_s p(s) E_loc(s) = %.6f is E[theta] to %.0e for a complex RBM on the open Heisenberg chain of 8 spins, and '
          'for the ground state of the transverse-field chain E_loc(s) is %.6f at every s, spread %.0e'
          % (np.real(np.sum(p * El)), abs(np.sum(p * El) - Et), np.real(Elg[0]), np.ptp(np.real(Elg))))

    errs, devs = [], []
    for seed in range(5):
        idx = np.random.default_rng(100 + seed).choice(256, size=4000, p=p)
        x = np.real(El[idx])
        errs.append(x.std() / np.sqrt(4000))
        devs.append(abs(x.mean() - Et) / errs[-1])
    check('the sampled energy', max(devs) < 2 and 0.008 < min(errs) and max(errs) < 0.013 and abs(Et + 0.50) < 0.005,
          '4000 configurations drawn from p(s) give E[theta] = %.4f with a statistical error from %.4f to %.4f in 5 runs, '
          'and the mean is at most %.1f errors away' % (Et, min(errs), max(errs), max(devs)))

    H6 = heisenberg(6)
    F = force(H6, C6, O6)
    Fwrong = (lambda q, El6: q @ (El6[:, None] * O6) - (q @ El6) * (q @ O6))(np.abs(C6) ** 2 / np.sum(np.abs(C6) ** 2), (H6 @ C6) / C6)
    ex, ey, ew = 0.0, 0.0, 0.0
    for k in range(len(pc)):
        for shift, ref in ((1e-6, 2 * np.real(F[k])), (1e-6j, 2 * np.imag(F[k]))):
            dp = np.zeros(len(pc), complex); dp[k] = shift
            fd = (energy(H6, rbm(pc + dp, L6, M4, S6)[0]) - energy(H6, rbm(pc - dp, L6, M4, S6)[0])) / 2e-6
            if np.isreal(shift):
                ex = max(ex, abs(fd - ref)); ew = max(ew, abs(fd - 2 * np.real(Fwrong[k])))
            else:
                ey = max(ey, abs(fd - ref))
    check('the gradient (10.5)', ex < 1e-9 and ey < 1e-9 and 1.3 < ew < 1.5,
          'for a complex RBM on the open chain of 6 sites, d E/d x_k = 2 Re F_k to %.0e and d E/d y_k = 2 Im F_k to %.0e '
          'for theta_k = x_k + i y_k, with F_k = <E_loc O_k*> - <E_loc><O_k*>, while O_k in place of O_k* is off by up '
          'to %.2f' % (ex, ey, ew))

    # The signs of the ground states and a trained network
    g8 = V8[:, 0]
    nz = np.abs(g8) > 1e-10
    up_odd = np.sum(S8[:, 1::2] > 0, axis=1)
    marshall = np.sign(g8[nz]) * (-1.0) ** up_odd[nz]
    gp = np.linalg.eigh(tfim(8, h=1.0))[1][:, 0]
    gm = np.linalg.eigh(tfim(8, h=-1.0))[1][:, 0]
    gp = gp * np.sign(gp[0])
    prod = np.prod(S8, axis=1)
    same = min(np.abs(gm - gp * prod).max(), np.abs(gm + gp * prod).max())
    check('the signs of the ground states', nz.sum() == 70 and np.ptp(marshall) == 0 and gp.min() > 0 and same < 1e-10,
          'the open Heisenberg chain of 8 spins has %d non-zero amplitudes, of both signs, which follow (-1)^(number of up '
          'spins on the odd sites), the transverse-field chain with h=1 has all 256 positive (smallest %.1e), and h=-1 '
          'gives the same state times prod_i s_i to %.0e' % (nz.sum(), gp.min(), same))

    Ht = tfim(8)
    Et0 = np.linalg.eigvalsh(Ht)[0]
    jw = [jordan_wigner(8, h=x) for x in (1.0, 0.5, 2.0)]
    ed = [np.linalg.eigvalsh(tfim(8, h=x))[0] for x in (1.0, 0.5, 2.0)]
    sc = spinchain.Spin_Chain(['S=1/2'] * 8)
    sc.set_hamiltonian(sum(-4 * sc.Sz[i] * sc.Sz[(i + 1) % 8] - 2 * sc.Sx[i] for i in range(8)))
    etdm = quiet(sc.gs_energy, mode='ED')
    long = jordan_wigner(4000) / 4000
    sc7 = spinchain.Spin_Chain(['S=1/2'] * 8)            # the form of the notebook of Session 7 at B_x = 0.5
    sc7.set_hamiltonian(sum(-sc7.Sz[i] * sc7.Sz[(i + 1) % 8] + 0.5 * sc7.Sx[i] for i in range(8)))
    e7 = quiet(sc7.gs_energy, mode='ED')
    same7 = np.abs(np.linalg.eigvalsh(tfim(8, h=-1.6)) / 4 - np.linalg.eigvalsh(tfim(8, h=1.6)) / 4).max()
    ok = abs(Et0 + 10.251662) < 1e-6 and np.allclose(jw, ed, atol=1e-10) and abs(Et0 + 2 / np.sin(np.pi / 16)) < 1e-10
    ok = ok and abs(e7 + 2.562915) < 1e-6 and abs(e7 - Et0 / 4) < 1e-8 and same7 < 1e-12
    check('the transverse-field Ising chain', ok and abs(etdm - Et0) < 1e-6 and abs(long + 4 / np.pi) < 1e-6,
          'the ring of 8 sites with J=h=1 has E0 = %.6f by exact diagonalization, %.6f = -2/sin(pi/16) from the free '
          'fermions and %.6f in dmrgpy with -4 Sz Sz - 2 Sx, the free fermions give %.6f and %.6f for h=0.5 and 2 as the '
          'diagonalization does, a long chain has %.4f = -4/pi per site, and the form -Sz Sz + Bx Sx of Session 7 at '
          'Bx=0.5 has %.6f = E0/4 in dmrgpy, the same levels for h and -h' % (Et0, jw[0], etdm, jw[1], jw[2], long, e7))

    rel = {2000: [], 3000: []}
    for seed in range(3):
        q = np.random.default_rng(seed).normal(0, 0.01, 80)
        for it in range(1, 3001):
            C = rbm(q, 8, 8, S8)[0]
            q = q - 0.05 * 2 * np.real(force(Ht, C, rbm_O(q, 8, 8, S8)))
            if it in rel:
                rel[it].append((energy(Ht, rbm(q, 8, 8, S8)[0]) - Et0) / abs(Et0))
    check('an RBM trained on the chain', np.allclose([min(rel[2000]), max(rel[2000]), min(rel[3000]), max(rel[3000])], [7.4e-5, 9.2e-5, 4.7e-5, 7.2e-5], atol=0.06e-5),
          'real a, b and W with M = L = 8, 80 parameters, from small random values, with (10.5) on the exact sums over '
          'the 256 configurations and eta=0.05, end %.1e to %.1e above E0 in relative terms after 2000 steps and %.1e to '
          '%.1e after 3000, in 3 runs' % (min(rel[2000]), max(rel[2000]), min(rel[3000]), max(rel[3000])))

    # Tomography and the fidelity
    r3 = np.random.default_rng(3)
    psi3 = r3.uniform(0.5, 1.0, 8) * np.exp(2j * np.pi * r3.uniform(size=8))
    psi3 /= np.linalg.norm(psi3)
    counts = np.bincount(r3.choice(8, size=1000, p=np.abs(psi3) ** 2), minlength=8)
    z = np.zeros(8)
    for it in range(4000):
        q = np.exp(z) / np.exp(z).sum()
        z += 2.0 * (counts / 1000 - q)
    q = np.exp(z) / np.exp(z).sum()
    up, dn = np.array([1.0, 0.0]), np.array([0.0, 1.0])
    plus, minus = (up + dn) / np.sqrt(2), (up - dn) / np.sqrt(2)
    alongz = [np.abs(plus) ** 2, np.abs(minus) ** 2]
    alongx = [[abs(plus @ plus) ** 2, abs(minus @ plus) ** 2], [abs(plus @ minus) ** 2, abs(minus @ minus) ** 2]]
    ok = counts.min() > 0 and np.abs(q - counts / 1000).max() < 1e-15
    check('the likelihood of Section 10.3.1', ok and np.allclose(alongz, 0.5) and np.allclose(alongx, [[1, 0], [0, 1]]),
          'gradient ascent of sum n(s) ln p(s) with p free on the 8 configurations of 3 spins ends at the frequencies of '
          '1000 shots to %.0e, and (up +- down)/sqrt 2 give 0.5 and 0.5 along z and (1, 0) and (0, 1) along x'
          % np.abs(q - counts / 1000).max())

    fid = lambda x, y: abs(np.vdot(x, y)) ** 2 / (np.vdot(x, x).real * np.vdot(y, y).real)
    phased = psi3 * np.exp(2j * np.pi * r3.uniform(size=8))
    check('the fidelity', abs(fid(plus, minus)) < 1e-15 and abs(fid(psi3, np.exp(0.7j) * psi3) - 1) < 1e-12
          and abs(fid(psi3, phased) - 0.054) < 0.001 and np.allclose(np.abs(phased) ** 2, np.abs(psi3) ** 2),
          'F = |<psi|phi>|^2 / (<psi|psi><phi|phi>) is 0 for (up + down)/sqrt 2 and (up - down)/sqrt 2, 1 for a global '
          'phase, and %.3f for a random phase on each configuration of the state of 3 spins, whose counts along z are the '
          'same' % fid(psi3, phased))

    singlet = np.array([0, 1, -1, 0]) / np.sqrt(2)
    f_s = fid(np.sqrt(np.abs(singlet) ** 2), singlet)
    mod = np.abs(g8)
    f_h = fid(mod, g8)
    f_m = fid(mod * (-1.0) ** up_odd, g8)
    check('a state from measurements along z alone', f_s < 1e-15 and abs(f_h - 0.0038) < 5e-5 and abs(f_m - 1) < 1e-12,
          'sqrt p(s) has F = %.0f with the singlet and F = %.4f with the ground state of the open Heisenberg chain of 8 '
          'spins, and F = %.6f once the sign (-1)^(up spins on the odd sites) is put in' % (f_s, f_h, f_m))

    # Matrix product states and the classifier
    n_mps, n_open = 100 * 2 * 10 ** 2, 2 * 2 * 10 + 98 * 2 * 10 ** 2
    orders = np.log10(2.0 ** 100 / n_mps)
    check('the parameters of (10.6)', n_mps == 20000 and n_open == 19640 and abs(2.0 ** 100 / 1.2677e30 - 1) < 1e-4
          and abs(orders - 25.8) < 0.05 and 100 * 2 == 200 and 40 * 2 == 80,
          'L d D^2 = %d for L=100, d=2, D=10, the open form (7.5) with vectors at the ends %d, 2^100 = %.3e, so %.1f '
          'orders of magnitude more, and D=1 gives L d = 200 numbers, 80 for 40 spins' % (n_mps, n_open, 2.0 ** 100, orders))

    sv = np.linalg.svd(singlet.reshape(2, 2), compute_uv=False)
    ent = -np.sum(sv ** 2 * np.log(sv ** 2))
    A = {1: np.diag([1.0, 0.0]), -1: np.diag([0.0, 1.0])}
    B = {1: -np.diag([0.0, 1.0]), -1: np.diag([1.0, 0.0])}
    tr = np.array([np.trace(A[s1] @ B[s2]) for s1, s2 in configurations(2)])
    mats = rng.normal(size=(8, 2, 2, 2)) + 1j * rng.normal(size=(8, 2, 2, 2))
    Ctr = np.array([np.trace(np.linalg.multi_dot([mats[i, (1 - s[i]) // 2] for i in range(8)])) for s in S8])
    rk = np.linalg.matrix_rank(Ctr.reshape(16, 16), tol=1e-10 * np.abs(Ctr).max())
    v10 = rng.normal(size=1024) + 1j * rng.normal(size=1024)
    rk10 = np.linalg.matrix_rank(v10.reshape(32, 32))
    check('the singlet and the trace form of (10.6)', np.allclose(sv, 1 / np.sqrt(2)) and abs(ent - np.log(2)) < 1e-12
          and np.allclose(tr, [0, 1, -1, 0]) and rk == 4 and rk10 == 32,
          'the singlet has the Schmidt values %.4f and %.4f and the entropy ln 2, the trace form with A = diag(1,0), '
          'diag(0,1) and B = -diag(0,1), diag(1,0) gives it, a random trace form of 8 sites with D=2 has the Schmidt '
          'rank %d = D^2 across half of the ring, and a random state of 10 spins has the rank %d at the middle'
          % (sv[0], sv[1], rk, rk10))

    phi = lambda x: np.array([np.cos(np.pi * x / 2), np.sin(np.pi * x / 2)])
    Dt = 3
    bot = rng.normal(size=(4, 2, 2, Dt)); mid = rng.normal(size=(2, Dt, Dt, Dt)); top = rng.normal(size=(Dt, Dt, 2))

    def tree(vs):
        v = [np.einsum('a,b,abc->c', vs[2 * k], vs[2 * k + 1], bot[k]) for k in range(4)]
        u = [np.einsum('a,b,abc->c', v[2 * k], v[2 * k + 1], mid[k]) for k in range(2)]
        return np.einsum('a,b,abc->c', u[0], u[1], top)
    pix = rng.uniform(0, 1, 8)
    vecs = [phi(x) for x in pix]
    Wfull = np.array([tree([np.eye(2)[(n >> (7 - i)) & 1] for i in range(8)]) for n in range(256)])
    big = vecs[0]
    for vv in vecs[1:]:
        big = np.kron(big, vv)
    dbl = [2 * vecs[0]] + vecs[1:]
    check('the classifier of Figure 10.3', np.allclose(big @ Wfull, tree(vecs)) and np.allclose(tree(dbl), 2 * tree(vecs))
          and abs(np.linalg.norm(big) - 1) < 1e-12 and np.allclose(phi(0), [1, 0]) and np.allclose(phi(1), [0, 1]),
          'a tree of 8 pixels gives the same two numbers by contraction and as a 256 x 2 matrix times the tensor product '
          'of the pixel vectors (cos(pi x/2), sin(pi x/2)), which has norm %.6f, twice one pixel vector gives twice the '
          'output, and the map sends white, x=0, to up and black, x=1, to down' % np.linalg.norm(big))

    counts_tree = {k: tree_count(100, **kw) for k, kw in (('top', {}), ('separate', dict(separate=True)),
                   ('halving', dict(halving=True)), ('top cut', dict(cut=True)), ('separate cut', dict(cut=True, separate=True)),
                   ('halving cut', dict(cut=True, halving=True)))}
    ok = (counts_tree['top'], counts_tree['separate'], counts_tree['halving']) == (50200, 51020, 41240)
    ok = ok and (counts_tree['top cut'], counts_tree['separate cut'], counts_tree['halving cut']) == (28000, 28820, 28088)
    check('the parameters of a tree', ok and all(1e4 < v < 1e5 for v in counts_tree.values()),
          'a binary tree on 100 pixels with D=10 and a label leg of 2 has %d numbers when neighbors are paired level by '
          'level and the top tensor carries the label, %d with a separate 10 x 2 tensor for the label, and %d when the '
          'pixels are split in halves, and %d, %d and %d when a bond is cut at min(D, product of the legs below)'
          % tuple(counts_tree[k] for k in ('top', 'separate', 'halving', 'top cut', 'separate cut', 'halving cut')))

    # The Kohn-Sham toy of Section 10.5
    hist, res, vext, new = ks_toy()
    n_free = ks_toy(U=0.0)[3](np.zeros(60))
    q = res[1:] / res[:-1]
    ok = len(res) == 36 and abs(hist[-1][30] - 0.9895) < 5e-5 and abs(hist[-1][29] - hist[-1][30]) < 1e-12
    ok = ok and abs(n_free[30] - 1.2143) < 5e-5 and abs(hist[1][30] - 0.831) < 5e-4 and abs(hist[3][30] - 0.949) < 5e-4
    out_in = np.abs(new(hist[0]) - hist[0]).max()
    stored = np.abs(hist[1] - hist[0]).max()
    ok = ok and abs(res[0] - out_in) < 1e-15 and abs(stored - 0.3 * out_in) < 1e-12
    check('the loop of the figure ks_loop', ok and abs(hist[-1].sum() - 40) < 1e-9 and 0.47 < q.min() and q.max() < 0.54,
          'the density at the center, the sites 29 and 30, is %.4f at convergence and %.4f with no Hartree term, %.3f and '
          '%.3f after the iterations 1 and 3, the largest difference between the density out and the density in is below '
          '1e-10 at the iteration %d, the ratio of two of them stays between %.2f and %.2f, and the stored density changes '
          'by %.2f times it' % (hist[-1][30], n_free[30], hist[1][30], hist[3][30], len(res), q.min(), q.max(),
                                stored / out_in))

    out = {}
    for name, kw in (('constraint', dict(constrains=['no_magnetism'])), ('guess', dict(mf='potential'))):
        h = geometry.chain().get_hamiltonian(tij=[-1.]).set_finite_system(n=60)
        h.add_onsite(vext)
        np.random.seed(0)
        hmf, Etot = quiet(h.get_mean_field_hamiltonian, U=4., filling=40 / 120, mix=0.3, maxerror=1e-8,
                          return_total_energy=True, **kw)
        dens, mom = moments(hmf)
        on = np.real(np.diag(algebra.todense(hmf.intra)))[0::2] - vext - 2 * dens
        h0 = geometry.chain().get_hamiltonian(tij=[-1.], has_spin=False).set_finite_system(n=60)
        lev = np.linalg.eigvalsh(np.asarray(algebra.todense(h0.intra)) + np.diag(vext + 2 * dens))
        out[name] = (np.abs(dens - hist[-1]).max(), np.abs(mom).max(), np.ptp(on), np.mean(on), Etot, (lev[19] + lev[20]) / 2)
    ok = out['constraint'][0] < 1e-10 and out['constraint'][1] < 1e-12 and out['constraint'][2] < 1e-9
    ok = ok and abs(out['constraint'][3] - 0.0477) < 5e-4 and abs(out['constraint'][3] + out['constraint'][5]) < 1e-6
    ok = ok and out['guess'][0] < 1e-10 and 1e-8 < out['guess'][1] < 1e-5
    check('the same loop in pyqula', ok,
          'a spinful open chain of 60 sites with tij=[-1.], the well in add_onsite and get_mean_field_hamiltonian(U=4, '
          'filling=40/120, mix=0.3) gives the density of the toy to %.0e with constrains=["no_magnetism"], where the '
          'onsite energy is v_ext + 2 n(i) + %.4f, minus the middle %.4f of the gap between the levels 20 and 21 of '
          'v_ext + 2 n(i), and to %.0e with the guess mf="potential", where a moment of %.0e appears'
          % (out['constraint'][0], out['constraint'][3], out['constraint'][5], out['guess'][0], out['guess'][1]))

    h = geometry.chain().get_hamiltonian(tij=[-1.]).set_finite_system(n=60)
    h.add_onsite(vext)
    np.random.seed(0)
    hmf, Emag = quiet(h.get_mean_field_hamiltonian, U=4., filling=40 / 120, mix=0.3, return_total_energy=True)
    dm, mm = moments(hmf)
    para = uhf(vext, 4.0, (np.full(60, 1 / 3), np.full(60, 1 / 3)))
    start = np.random.default_rng(0).uniform(0, 1, (2, 60))
    mag = uhf(vext, 4.0, tuple(start * 40 / start.sum()))
    kick = 1e-6 * np.random.default_rng(1).normal(size=60)
    kicked = uhf(vext, 4.0, (para[0] + kick, para[1] - kick))
    ok = abs(para[2] - out['constraint'][4]) < 1e-6 and abs(para[2] + 58.0094) < 5e-5 and abs(Emag + 61.79) < 0.01
    ok = ok and abs(np.linalg.norm(mm, axis=1).max() - 0.769) < 0.002 and abs(np.abs(mm[:, 2]).max() - 0.352) < 0.002
    ok = ok and abs(np.abs(mag[0] - mag[1]).max() - 0.769) < 0.002 and abs(mag[2] + 61.4175) < 0.001
    ok = ok and abs(np.abs(kicked[0] - kicked[1]).max() - 0.769) < 0.002 and abs(kicked[2] + 61.80) < 0.005
    check('a random start of the mean field', ok,
          'the default random guess with the seed 0 ends at the total energy %.4f, below %.4f of the state with equal '
          'spins, with a local moment up to %.3f along an axis of its own (%.3f along z), and a collinear loop in numpy '
          'gives %.4f for equal spins, %.4f with the moment %.3f from a random start, and %.4f with the moment %.3f '
          'from equal spins with a kick of 1e-6'
          % (Emag, out['constraint'][4], np.linalg.norm(mm, axis=1).max(), np.abs(mm[:, 2]).max(), para[2], mag[2],
             np.abs(mag[0] - mag[1]).max(), kicked[2], np.abs(kicked[0] - kicked[1]).max()))

    # The Ising model of Section 10.6a
    Tc = 2 / np.log(1 + np.sqrt(2))
    exact = lambda T: (1 - np.sinh(2 / T) ** -4) ** 0.125
    mex = [exact(T) for T in (1.5, 2.0, 2.1, 2.2)]
    check('T_c and the exact order parameter', abs(Tc - 2.2692) < 5e-5 and abs(np.sinh(2 / Tc) - 1) < 1e-12
          and np.allclose(mex, [0.9865, 0.9113, 0.8687, 0.7848], atol=5e-5),
          'T_c = 2/ln(1+sqrt 2) = %.4f J, where sinh(2J/T_c) = 1, and |m| = %.4f, %.4f, %.4f and %.4f at T = 1.5, 2.0, 2.1 '
          'and 2.2' % (Tc, *mex))

    g16 = geometry.square_lattice().get_supercell(16)
    mi = LatticeIsing(g16, m=1.)
    mi.add_interaction(Jij=[0.5])
    e_up = mi.get_energy()
    mi.s[0] = -1
    e_flip = mi.get_energy() - e_up
    m2 = LatticeIsing(g16, m=1.)
    m2.add_interaction(Jij=[1.])
    e_up2 = m2.get_energy()
    mi.s = np.ones(256)
    np.random.seed(1)
    es, ms = mi.optimize_energy(temp=1.5, ntries=256 * 1000)
    m15 = np.mean(np.abs(ms[256 * 300::256])) / 256
    mi.s = np.ones(256)
    es, ms = mi.optimize_energy(temp=3.5, ntries=256 * 2000)
    m35 = np.mean(np.abs(ms[256 * 300::256])) / 256
    ok = abs(e_up + 512) < 1e-9 and abs(e_flip - 8) < 1e-9 and abs(e_up2 + 1024) < 1e-9 and abs(m15 - 0.986) < 0.006
    check('LatticeIsing of pyqula', ok and abs(m35 - 0.13) < 0.01 and abs(m15 - 0.987) < 0.0006 and abs(2 * Tc - 4.54) < 0.005,
          'on 16 x 16 with add_interaction(Jij=[0.5]) all spins up have %.0f = -2N and one flip costs %.0f, the 8J of '
          '(10.9) with J=1, Jij=[1.] gives %.0f, twice the energy and T_c at %.2f, and optimize_energy gives the mean '
          '|m| %.3f at T=1.5 and %.3f at T=3.5' % (e_up, e_flip, e_up2, 2 * Tc, m15, m35))

    rand = rng.choice([-1.0, 1.0], size=(2000, 4096)).mean(axis=1)
    m64 = ising_snapshots(3.5, np.random.default_rng(5), L=64, nth=300, ns=3000, every=1)
    rms64 = np.sqrt(np.mean(m64 ** 2))
    ok = abs(1 / np.sqrt(4096) - 0.0156) < 5e-5 and abs(np.sqrt(2 / (np.pi * 4096)) - 0.0125) < 5e-5
    ok = ok and abs(rand.std() / 0.015625 - 1) < 0.05 and abs(np.abs(rand).mean() / 0.012466 - 1) < 0.06
    check('the quiz of a snapshot with |m| = 0.93', ok and abs(0.93 * 64 - 59.5) < 0.05 and abs(rms64 - 0.038) < 0.0005 and round(0.93 / rms64) == 24,
          'N = 4096 independent spins have the root mean square 1/sqrt N = 0.0156 and <|m|> = sqrt(2/(pi N)) = 0.0125 '
          '(%.4f and %.4f from 2000 samples), so 0.93 is %.1f standard deviations, and at T=3.5 on 64 x 64 the root mean '
          'square of m is %.4f, so 0.93 is %.0f of it' % (rand.std(), np.abs(rand).mean(), 0.93 * 64, rms64, 0.93 / rms64))

    fs = figure_ising_sizes()
    low = (1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1)
    dev = {L: {T: fs[L][T] - exact(T) for T in low + (2.2,)} for L in fs}
    ok = all(abs(dev[L][T]) < 0.0066 for L in fs for T in low)
    ok = ok and np.allclose([dev[8][2.2], dev[16][2.2], dev[32][2.2]], [0.031, 0.012, -0.013], atol=0.0006)
    check('the figure ising_sizes below T_c', ok,
          'with its seed, at the seven temperatures from T=1.5 to 2.1 the three sizes are at most %.4f from the exact '
          'value, and at T=2.2 L=8, 16 and 32 are %+.3f, %+.3f and %+.3f away'
          % (max(abs(dev[L][T]) for L in fs for T in low), dev[8][2.2], dev[16][2.2], dev[32][2.2]))

    m30 = [fs[L][3.0] for L in (8, 16, 32)]
    Lm = [L * m for L, m in zip((8, 16, 32), m30)]
    ind = [m / np.sqrt(2 / (np.pi * L * L)) for L, m in zip((8, 16, 32), m30)]
    check('the figure ising_sizes above T_c', np.allclose(m30, [0.352, 0.170, 0.086], atol=0.002) and 2.6 < min(Lm)
          and max(Lm) < 2.9 and 3.3 < min(ind) and max(ind) < 3.6,
          'at T=3.0 <|m|> = %.3f, %.3f and %.3f for L = 8, 16 and 32, so L <|m|> is %.2f, %.2f and %.2f, and it is %.2f to '
          '%.2f times the sqrt(2/(pi N)) of independent spins' % (*m30, *Lm, min(ind), max(ind)))

    # corrected on 2026-11-22: the Ising side of igt_hist is the pyqula script, with its seed
    absm = quiet(runpy.run_path, os.path.join(WEBNOTES, 'scripts', 'session10', 'g4_ising_snapshots.py'))['absm']
    lo, hi = absm[1.5], absm[3.5]
    longrun = np.abs(ising_snapshots(3.5, np.random.default_rng(101), nth=500, ns=8000, every=1))
    blocks = longrun.reshape(16, -1).mean(1)
    ok = len(lo) == len(hi) == 1000 and round(lo.min(), 3) == 0.922 and lo.max() == 1.0 and round(hi.max(), 3) == 0.508
    ok = ok and hi.min() < 0.005 and hi.max() < lo.min() and hi.max() > 0.5
    check('the figure igt_hist, the Ising side', ok and round(lo.mean(), 3) == 0.987 and round(hi.mean(), 3) == 0.125
          and abs(longrun.mean() - 0.124) < 0.0006,
          'the pyqula script with its seed, 1000 snapshots on 16 x 16, has |m| from %.3f to %.3f with the mean %.3f at '
          'T=1.5, and from %.3f to %.3f with the mean %.3f at T=3.5, so they do not overlap, and a checkerboard run of 8000 '
          'sweeps gives %.3f +- %.3f at T=3.5' % (lo.min(), lo.max(), lo.mean(), hi.min(), hi.max(), hi.mean(),
                                                  longrun.mean(), blocks.std() / np.sqrt(16)))

    # The Ising gauge theory of Section 10.6b
    ok = True
    for L in (3, 4, 5, 6):
        h0, v0 = rng.choice([-1, 1], size=(2, L, L))
        P0 = plaquettes(h0, v0)
        st, pq = torus_index(L)
        held = np.array([[len(set(a_) & set(b_)) for b_ in pq] for a_ in st])     # star links in each plaquette
        ok = ok and all(sorted(r_) == [0] * (L * L - 4) + [2] * 4 for r_ in held)
        for x in range(L):
            for y in range(L):
                h1, v1 = h0.copy(), v0.copy()
                h1[x, y] *= -1; h1[(x - 1) % L, y] *= -1; v1[x, y] *= -1; v1[x, (y - 1) % L] *= -1
                ok = ok and np.array_equal(P0, plaquettes(h1, v1))
        h1 = h0.copy(); h1[0, 0] *= -1
        ok = ok and int(np.sum(plaquettes(h1, v0) != P0)) == 2
    check('the star flip', ok,
          'flipping the four links at any vertex keeps every plaquette on the tori of 3, 4, 5 and 6 sites per side, four '
          'plaquettes hold two of the four links each and the others none, and one flipped link changes two plaquettes')

    tor = {L: enumerate_torus(L) for L in (2, 3)}
    good = {L: np.all(tor[L][2] == 1, axis=1) for L in tor}
    hh, vv = tor[3][0][good[3]], tor[3][1][good[3]]
    sectors = np.unique(np.stack([np.prod(hh[:, :, 0], axis=1), np.prod(vv[:, 0, :], axis=1)], 1), axis=0, return_counts=True)[1]
    ok = good[2].sum() == 2 ** 5 and good[3].sum() == 2 ** 10 == 1024 and list(sectors) == [256] * 4
    check('the ground states of (10.10) on the torus', ok,
          '%d of the 2^8 configurations of the 2 x 2 torus and %d of the 2^18 of the 3 x 3 torus have every plaquette at '
          '+1, which is 2^(L^2+1), and the 3 x 3 ones fall in four sectors of the two loops around the torus with %d '
          'each, 2^(L^2-1) gauge copies' % (good[2].sum(), good[3].sum(), sectors[0]))

    form = lambda T, N: (np.tanh(1 / T) + np.tanh(1 / T) ** (N - 1)) / (1 + np.tanh(1 / T) ** N)
    err_t = 0.0
    for L in (2, 3):
        Psum = tor[L][2].sum(1)
        for T in (0.2, 0.7, 1.0, 5.0):
            w = np.exp((Psum - Psum.max()) / T)
            err_t = max(err_t, abs(np.sum(w * Psum) / w.sum() / (L * L) - form(T, L * L)))
    # the open lattice of 2 x 2 plaquettes: 12 links on a 3 x 3 grid of vertices
    bits = ((np.arange(2 ** 12)[:, None] >> np.arange(12)) & 1)
    s = 1 - 2 * bits
    hx, vy = s[:, :6].reshape(-1, 2, 3), s[:, 6:].reshape(-1, 3, 2)
    Pop = np.stack([hx[:, x, y] * vy[:, x + 1, y] * hx[:, x, y + 1] * vy[:, x, y] for x in (0, 1) for y in (0, 1)], 1)
    err_o, Pop1 = 0.0, None
    for T in (0.2, 0.7, 1.0, 5.0):
        w = np.exp((Pop.sum(1) - 4) / T)
        val = np.sum(w[:, None] * Pop) / w.sum() / 4
        err_o = max(err_o, abs(val - np.tanh(1 / T)))
        Pop1 = val if T == 1.0 else Pop1
    f_open = [(1 - np.tanh(1 / T)) / 2 for T in (0.2, 5.0)]
    f_tor = [(1 - form(T, 256)) / 2 for T in (0.2, 5.0)]
    ok = err_t < 1e-14 and err_o < 1e-14 and abs(Pop1 - 0.761594) < 1e-6 and abs(form(1.0, 9) - 0.8054) < 5e-5
    ok = ok and abs(f_open[0] - 4.5e-5) < 0.06e-5 and abs(f_open[1] - 0.40) < 0.005 and abs(f_tor[1] - 0.40) < 0.005
    check('the plaquette average', ok and 4.5e-7 < f_tor[0] < 5.5e-7,
          'enumeration on the open lattice of 2 x 2 plaquettes gives tanh(J/T) to %.0e, %.6f at T=J, and on the tori of '
          '2 x 2 and 3 x 3 (t + t^(N-1))/(1 + t^N) with t = tanh(J/T) to %.0e, at T = 0.2, 0.7, 1 and 5, so the fraction '
          'of plaquettes at -1 is %.2e and %.4f at T = 0.2 and 5 on an open lattice and %.1e and %.4f on the 16 x 16 torus'
          % (err_o, Pop1, err_t, f_open[0], f_open[1], f_tor[0], f_tor[1]))

    h3, v3, P3 = tor[3]
    m3 = (h3.reshape(len(h3), -1).sum(1) + v3.reshape(len(v3), -1).sum(1)) / 18
    mom = []
    for T in (0.2, 1.0, 5.0):
        w = np.exp((P3.sum(1) - 9) / T)
        mom.append((np.sum(w * m3) / w.sum(), np.sum(w * m3 ** 2) / w.sum()))
    rs = np.random.default_rng(12)
    gsamp = []
    for zero_t in (True, False):
        if zero_t:      # every plaquette +1: a random gauge g_i g_j of the vertex spins and a random sector
            gv = rs.choice(np.array([-1, 1], np.int8), size=(10000, 16, 16))
            hl, vl = gv * np.roll(gv, -1, 1), gv * np.roll(gv, -1, 2)
            hl[:, -1, :] *= rs.choice(np.array([-1, 1], np.int8), size=(10000, 1))
            vl[:, :, -1] *= rs.choice(np.array([-1, 1], np.int8), size=(10000, 1))
            ok_p = np.all(plaquettes(hl, vl) == 1)
        else:           # infinite temperature: every link at random
            hl, vl = rs.choice(np.array([-1, 1], np.int8), size=(2, 10000, 16, 16))
        mm = (hl.sum((1, 2)) + vl.sum((1, 2))) / 512
        gsamp.append((np.abs(mm).mean(), np.sqrt(np.mean(mm ** 2))))
    ok = all(abs(a) < 1e-12 and abs(b - 1 / 18) < 1e-12 for a, b in mom) and ok_p
    ok = ok and all(abs(a - 0.0353) < 0.001 and abs(b - 0.0442) < 0.001 for a, b in gsamp)
    check('the magnetization of (10.10)', ok,
          'enumeration on the 3 x 3 torus gives <m> = 0 and <m^2> = 1/18, one over the number of links, at T = 0.2, 1 and '
          '5, and on the 16 x 16 torus of 512 links 10000 configurations with every plaquette at +1 in a random gauge give '
          '<|m|> = %.4f and the root mean square %.4f, and random links give %.4f and %.4f, against sqrt(2/(512 pi)) = '
          '%.4f and 1/sqrt 512 = %.4f' % (*gsamp[0], *gsamp[1], np.sqrt(2 / (512 * np.pi)), 1 / np.sqrt(512)))

    stars, plaqs = torus_index(2)
    nb = np.arange(256)
    sz = 1 - 2 * ((nb[:, None] >> np.arange(8)) & 1)
    Htc = np.zeros((256, 256))
    for st in stars:
        Htc[nb, nb ^ sum(1 << l for l in st)] -= 1
    for pq in plaqs:
        Htc[nb, nb] -= np.prod(sz[:, pq], axis=1)
    etc = np.linalg.eigvalsh(Htc)
    Av = [np.eye(256)[nb ^ sum(1 << l for l in st)] for st in stars]
    Bp = [np.diag(np.prod(sz[:, pq], axis=1)).astype(float) for pq in plaqs]
    comm = max(np.abs(a_ @ b_ - b_ @ a_).max() for a_ in Av for b_ in Bp)
    st3, pq3 = torus_index(3)
    inc_s, inc_p = np.zeros((9, 18), int), np.zeros((9, 18), int)
    for i, (st, pq) in enumerate(zip(st3, pq3)):
        inc_s[i, st] = 1; inc_p[i, pq] = 1
    shared = np.unique(inc_s @ inc_p.T)
    rs3, rp3 = rank_gf2(inc_s), rank_gf2(inc_p)
    ok = comm < 1e-12 and np.allclose(etc[:4], -8) and etc[4] > -8 + 1 and set(shared) <= {0, 2}
    check('the star and plaquette terms', ok and rs3 == 8 and rp3 == 8,
          'A_v, the product of sigma^x on the four links of a star, and B_p, the product of sigma^z around a plaquette, '
          'commute and share 0 or 2 links, -sum A_v - sum B_p on the 2 x 2 torus has 4 ground states at %.0f and the next '
          'level at %.0f, and on the 3 x 3 torus %d of the 9 stars and %d of the 9 plaquettes are independent, which '
          'leaves 18 - 16 = 2 qubits and 4 ground states' % (etc[0], etc[4], rs3, rp3))

    # Hamiltonian learning of Section 10.7
    kk = np.linspace(-np.pi, np.pi, 200001)
    band = lambda k, t2: -2 * np.cos(k) - 2 * t2 * np.cos(2 * k)
    ext = {t2: (band(kk, t2).min(), band(kk, t2).max()) for t2 in (0.2, 0.4)}
    kr = 2 * np.pi * np.arange(200) / 200
    err_r = max(np.abs(np.linalg.eigvalsh(ring(200, 1.0, t2)) - np.sort(band(kr, t2))).max() for t2 in (0.05, 0.2, 0.4))
    chain = geometry.chain()
    gen_m, gen_p = (chain.get_hamiltonian(has_spin=False, tij=tij).get_hk_gen() for tij in ([-1., -0.3], [1., 0.3]))
    kq = [0.0, 0.13, 0.25, 0.41]
    err_p = max(abs(np.real(algebra.todense(gen_m([k, 0, 0]))[0, 0]) - band(2 * np.pi * k, 0.3)) for k in kq)
    err_m = max(abs(np.real(algebra.todense(gen_p([k, 0, 0]))[0, 0]) + band(2 * np.pi * k, 0.3)) for k in kq)
    ok = np.allclose(ext[0.2], (-2.4, 1.6), atol=1e-9) and np.allclose(ext[0.4], (-2.8, 1.425), atol=1e-8)
    check('the band of the toy ring', ok and abs(0.8 + 1 / 1.6 - 1.425) < 1e-12 and err_r < 1e-14 and err_p < 1e-14 and err_m < 1e-14,
          'the matrix elements -1 and -t2 give -2 cos k - 2 t2 cos 2k on the ring of 200 sites to %.0e, from %.1f to %.1f at '
          't2=0.2 and from %.3f to %.3f = 2 t2 + 1/(4 t2) at t2=0.4, pyqula gives it with tij=[-1., -t2] to %.0e, and '
          'tij=[1., t2] gives minus it to %.0e' % (err_r, *ext[0.2], *ext[0.4], err_p, err_m))

    w = np.random.default_rng(1).uniform(-1, 1, 200)
    hf = chain.get_hamiltonian(has_spin=False, tij=[-1., -0.3]).set_finite_system(n=200, periodic=True)
    hf.add_onsite(w)
    hs = chain.get_hamiltonian(has_spin=False, tij=[-1., -0.3]).get_supercell(200)
    hs.add_onsite(w)
    ref = ring(200, 1.0, 0.3, onsite=w)
    e_f = np.abs(algebra.todense(hf.intra) - ref).max()
    e_s = np.abs(algebra.todense(hs.get_hk_gen()([0., 0., 0.])) - ref).max()
    check('the ring of the toy in pyqula', e_f < 1e-14 and e_s < 1e-14,
          'set_finite_system(n=200, periodic=True) and get_supercell(200) at k=0, each with add_onsite(w) and an array '
          'w, give the matrix of the script with -1, -0.3 and the onsite energies w, to %.0e and %.0e' % (e_f, e_s))

    lv = {(t, t2): np.linalg.eigvalsh(ring(200, t, t2)) for t, t2 in ((1, 0.3), (-1, 0.3), (1, -0.3))}
    same_t = np.abs(lv[1, 0.3] - lv[-1, 0.3]).max()
    mirror = np.abs(lv[1, -0.3] + lv[1, 0.3][::-1]).max()
    E3 = np.array([0.0, 1.0, 1.5])
    dos = {}
    for key, kw in (('t', dict(has_spin=False, tij=[-1.])), ('-t', dict(has_spin=False, tij=[1.])),
                    ('spin', dict(tij=[-1.]))):
        dos[key] = np.array(quiet(chain.get_hamiltonian(**kw).get_dos, energies=E3, delta=0.005, nk=20000, write=False)[1])
    closed = 1 / (np.pi * np.sqrt(4 - E3 ** 2))
    ok = same_t < 1e-14 and mirror < 1e-14 and np.abs(dos['t'] - closed).max() < 1e-3 and abs(dos['t'][0] - 0.159) < 0.001
    check('the sign of t and the density of states', ok and np.abs(dos['-t'] - dos['t']).max() < 1e-9
          and np.abs(dos['spin'] / dos['t'] - 2).max() < 1e-9,
          'the ring levels for t and -t agree to %.0e at t2=0.3 and t2 -> -t2 gives minus them to %.0e, and get_dos with '
          'delta=0.005 and nk=20000 gives %s per site at E = 0, 1, 1.5 against 1/(pi sqrt(4-E^2)) = %s, the same for tij=[1.] '
          'and twice it with the spin' % (same_t, mirror, ' '.join('%.4f' % x for x in dos['t']),
                                          ' '.join('%.4f' % x for x in closed)))

    runs = {seed: ham_learning(seed) for seed in range(10)}
    clean, wide, dis = (np.array([runs[s][i] for s in runs]) for i in range(3))
    sets, fits, outside = runs[3][3], runs[3][4], max(runs[s][5] for s in runs)
    ranks = [np.linalg.matrix_rank(X) for X, lam, W in sets[1:]]
    sv_c, Vt_c = np.linalg.svd(sets[1][0])[1:]
    null = Vt_c[sv_c < 1e-10 * sv_c[0]] if len(sv_c) == 41 else None
    # of the vectors of norm 1 in the null space of the clean fit, the one that moves the test predictions most
    vec = null.T @ np.linalg.svd(sets[0][0] @ null.T)[2][0]
    other = np.sqrt(np.mean((sets[0][0] @ (fits[0][2] + vec) - sets[0][1]) ** 2))
    ok = abs(clean[3] - 0.0635) < 5e-5 and abs(wide[3] - 0.1027) < 5e-5 and abs(dis[3] - 0.0043) < 5e-5
    ok = ok and abs(clean.min() - 0.0577) < 5e-5 and abs(clean.max() - 0.0739) < 5e-5 and abs(wide.min() - 0.0933) < 5e-5
    ok = ok and abs(wide.max() - 0.1209) < 5e-5 and abs(dis.min() - 0.0040) < 5e-5 and abs(dis.max() - 0.0054) < 5e-5
    ok = ok and ranks == [27, 38] and outside <= 0.01 and abs(other - 0.0936) < 0.0005
    check('the figure ham_learning', ok,
          'the seed 3 of the script gives the errors %.4f trained on clean rings, %.4f on the test rings with W>1 and %.4f '
          'trained with disorder, the seeds 0 to 9 give %.4f to %.4f, %.4f to %.4f and %.4f to %.4f, the two fits have the '
          'rank %d and %d of 41, so another least-squares solution of the clean fit, with a vector of norm 1 of its null '
          'space added, gives %.4f in place of %.4f, and at most %.1f percent of the levels of a ring fall outside '
          '[-3.5, 3.5]'
          % (clean[3], wide[3], dis[3], clean.min(), clean.max(), wide.min(), wide.max(), dis.min(), dis.max(),
             ranks[0], ranks[1], other, clean[3], 100 * outside))

    edges = np.linspace(-3.5, 3.5, 41)
    on_edge = {t2: int(np.sum(np.min(np.abs(np.linalg.eigvalsh(ring(200, 1.0, t2))[:, None] - edges[None, :]), 1) < 1e-12))
               for t2 in (0.05, 0.35)}
    at = {0.05: abs(band(0.0, 0.05) + 2.1), 0.35: abs(band(np.pi / 2, 0.35) - 0.7)}
    lv35 = np.linalg.eigvalsh(ring(200, 1.0, 0.35))
    sides = np.digitize(lv35[np.abs(lv35 - 0.7) < 1e-12], edges)
    # the side of the edge on which these levels fall changes from one process to another, so it is printed and not
    # asserted: in six small processes with one thread and in one run of this check the two levels at 0.7 fell in the
    # bins 24 and 25, and in another run of this check they did not
    check('the SVG of ham_learning', on_edge == {0.05: 1, 0.35: 2} and max(at.values()) < 1e-14 and len(sides) == 2,
          'the clean rings of the left panel have levels exactly on a bin edge, %d at -2.1 for t2=0.05 and %d at 0.7 for '
          't2=0.35, so rounding decides their bin, and in this process the two levels at 0.7 fall in the bins %d and %d'
          % (on_edge[0.05], on_edge[0.35], sides[0], sides[1]))

    yy = np.linspace(-2, 2, 4001)
    lsum = (yy - 1) ** 2 + (yy + 1) ** 2
    check('the quiz of two labels with one input', abs(yy[np.argmin(lsum)]) < 1e-12 and abs(lsum.min() - 2) < 1e-12,
          'the pairs (O, t) and (O, -t) with t=1 give the smallest squared loss at the output %.0f, where the sum of (10.12) '
          'is %.0f = 2 t^2 and the mean over the two pairs is %.0f = t^2' % (yy[np.argmin(lsum)], lsum.min(), lsum.min() / 2))

    # pyqula
    errs_imp = []
    for mod in ('pyqula.spinchain', 'pyqula.nnqs'):
        try:
            importlib.import_module(mod)
            errs_imp.append('imported')
        except ModuleNotFoundError as e:
            errs_imp.append(str(e))
    try:
        LatticeIsing(geometry.square_lattice().get_supercell(4)).add_tensor(lambda r1, r2, r3, r4: 1.0)
        terr = 'no error'
    except TypeError as e:
        terr = str(e)
    check('what pyqula does not do', errs_imp == ["No module named 'pyqula.spinchain'", "No module named 'pyqula.nnqs'"]
          and "missing 2 required positional arguments: 'r3' and 'r4'" in terr,
          '%s, %s, and add_tensor with a function of four positions gives "%s"' % (*errs_imp, terr))

    # Points of the old text, corrected on 2026-11-22
    check('the quiz on the memory of Section 10.3a', round(b40 / 1e12, 1) == 17.6 and b40 / 2 ** 40 == 16,
          'the table of L=40 is %.1f TB, the "about 17.6 terabytes" of the option, and 16 TiB' % (b40 / 1e12))
    check('the text of the widget netfit', loss[3] > 0.2 and loss[7] > loss[5] and round(loss[3], 2) == 0.23
          and loss[12] < loss[5] < loss[1],
          'three neurons give %.2f, and the error rises from %.1e at H=5 to %.1e at H=7 while it falls from %.2f at H=1 '
          'to %.1e at H=12' % (loss[3], loss[5], loss[7], loss[1], loss[12]))
    check('the second quiz of Section 10.7', abs(lsum.min() - 2) < 1e-12,
          'the sum (10.12) over the two pairs is %.0f t^2 at its smallest, t^2 per pair' % lsum.min())
    check('the gradient (10.5) on the page', ex < 1e-8 and ey < 1e-8,
          '(10.5) is the derivative along a real parameter, and 2 Im F_k the one along the imaginary part')
    check('the caption of ham_learning', round(clean.min(), 2) == 0.06 and round(clean.max(), 2) == 0.07
          and round(wide.min(), 1) == 0.1 and round(wide.max(), 1) == 0.1 and round(dis.min(), 3) == 0.004
          and round(dis.max(), 3) == 0.005,
          'the seeds 0 to 9 give %.3f to %.3f, %.3f to %.3f and %.4f to %.4f, the 0.06 to 0.07, about 0.1 and 0.004 to '
          '0.005 of the caption' % (clean.min(), clean.max(), wide.min(), wide.max(), dis.min(), dis.max()))
    check('the caption of ising_sizes', round(dev[8][2.2], 2) == 0.03
          and round(max(abs(dev[L][T]) for L in fs for T in low), 3) <= 0.007,
          'up to T=2.1 the three sizes are within %.4f, and at T=2.2 the lattice of 8 is %+.3f from the exact curve'
          % (max(abs(dev[L][T]) for L in fs for T in low), dev[8][2.2]))
    print('%d checks hold, %.1f s' % (COUNT[0], time.time() - t0))


if __name__ == '__main__':
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            main()
        finally:
            os.chdir(cwd)
