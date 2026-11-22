"""Session 6, the numbers that page 15 (Section 6.15) quotes and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. The band of square_magnon is asserted in figures/session06/square_magnon.py,
the curves of afm_bogoliubov in afm_bogoliubov.py, and the three picture options in _g4_dispersions.py. This script
holds the rest, each by two routes where it can.

- (6.8): the bosonic hopping -|J|S and onsite z|J|S give |J|Sz(1 - gamma), and the exact one-magnon block of a 4x4
  torus of spins 1/2 gives 0, 4|J|S, 8|J|S at Gamma, X, M, the same as the pyqula script g4_magnon_square.py.
- (6.9) and the steps fold: the commutator matrix gives sqrt(eps^2 - Delta^2) and u^2, v^2; an exact diagonalization
  of the two-mode boson Hamiltonian gives the same excitation and v^2 = <a^dagger a> in its ground state, 1.19 at
  k = 0.3 on the chain and 0 at k = pi/2; a real-space bosonic Bogoliubov ring gives 2JS|sin k|; the same steps with
  fermions give sqrt(eps^2 + Delta^2), as (5.9), and the sign comes from the commutators of the pair term; v^2 ~ 1/(2|k|), its average over the chain grows as log of the
  number of k-points, and on the square lattice it converges to 0.1966, about 0.2, which leaves 0.30 of S = 1/2.
- The lab box: (6.9) is zero at (pi, pi) of the square lattice, the two numbers are read from the stored abstract,
  and 72 micro-eV is 0.072 meV.
- The quizzes and the problem: 0.0050, 0.0199, 0.0998, 0.1987, the ratios 4 and 2, gamma and E at (0,0), (pi,0),
  (pi,pi), 0.005, 0.020 and 0.2 of the picture quiz, the zero at k = 0 for any J > 0, |J|Sk^2, 2JS|k| and
  2 sqrt(2) JS|k|, the isotropy, and the velocity factor Z_c = 1 + r/(2S) = 1.158 of the first order in 1/S, from the
  Wick counts of the decoupling and r = 0.158 by quadrature, with n + m = -r/2 on a mesh as a check of the algebra.

The sign is the one of webnotes/conventions/session06.md, H = J sum_<ij> S_i . S_j with each bond once, J < 0 for the
ferromagnet and J > 0 for the antiferromagnet. It finds the repository from its own path, runs pyqula in a temporary
folder and writes no file."""
import os
import re
import runpy
import tempfile

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as sla
from scipy import integrate

COUNT = [0]
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name
    COUNT[0] += 1


def one_magnon_torus(L, J):
    """E_0 and the exact matrix of H = J sum S_i . S_j on the L*L states with one spin 1/2 down, on an L x L torus,
    from the sparse many-body Hamiltonian, with the check that H keeps these states closed."""
    N = L * L
    sz = sp.csr_matrix(np.diag([0.5, -0.5]))
    spl = sp.csr_matrix(np.array([[0.0, 1.0], [0.0, 0.0]]))

    def site(op, i):
        return sp.kron(sp.kron(sp.identity(2 ** i), op), sp.identity(2 ** (N - i - 1)), format='csr')

    idx = lambda x, y: (x % L) * L + (y % L)
    bonds = [(idx(x, y), idx(x + 1, y)) for x in range(L) for y in range(L)] + \
            [(idx(x, y), idx(x, y + 1)) for x in range(L) for y in range(L)]
    Sz = [site(sz, i) for i in range(N)]
    Sp = [site(spl, i) for i in range(N)]
    H = sp.csr_matrix((2 ** N, 2 ** N))
    for i, j in bonds:
        H = H + J * (Sz[i] @ Sz[j] + 0.5 * (Sp[i] @ Sp[j].T + Sp[i].T @ Sp[j]))
    full = np.zeros(2 ** N); full[0] = 1.0
    P = np.array([Sp[i].T @ full for i in range(N)])
    HP = H @ P.T
    closed = np.abs(HP - P.T @ (P @ HP)).max()
    pos = np.array([(i // L, i % L) for i in range(N)])
    return full @ (H @ full), P @ HP, closed, pos


def two_mode(eps, delta, q, nmax=300):
    """The levels of eps (n_a + n_b) + delta (a b + a^dagger b^dagger) in the sector n_a - n_b = q, on the states
    |n + q, n> with n < nmax, and the occupation <n_a> of the lowest one."""
    n = np.arange(nmax)
    diag = eps * (2 * n + q)
    off = delta * np.sqrt((n[:-1] + 1 + q) * (n[:-1] + 1))
    h = np.diag(diag) + np.diag(off, 1) + np.diag(off, -1)
    w, v = np.linalg.eigh(h)
    return w, np.sum(v[:, 0] ** 2 * (n + q))


def fermion_pair(xi, delta):
    """The levels of xi (n_a + n_b) + delta (a b + b^dagger a^dagger) for two fermion modes, with Jordan-Wigner."""
    c = np.array([[0.0, 1.0], [0.0, 0.0]])
    zz = np.diag([1.0, -1.0])
    a = np.kron(c, np.eye(2)); b = np.kron(zz, c)
    assert np.allclose(a @ b + b @ a, 0) and np.allclose(a @ a.T + a.T @ a, np.eye(4))
    H = xi * (a.T @ a + b.T @ b) + delta * (a @ b + b.T @ a.T)
    return H, a.T @ a + b.T @ b


def main():
    # the recall box and (6.8): onsite z|J|S plus -|J|S e^{ik.delta} is |J|Sz(1 - gamma), on the chain and the square
    JS = 0.7
    k = np.linspace(-np.pi, np.pi, 41)
    kx, ky = np.meshgrid(k, k)
    chain = 2 * JS - JS * (np.exp(1j * k) + np.exp(-1j * k))
    square = 4 * JS - JS * (np.exp(1j * kx) + np.exp(-1j * kx) + np.exp(1j * ky) + np.exp(-1j * ky))
    check('(6.8): z|J|S - |J|S sum_delta e^{ik.delta} = |J|Sz(1 - gamma) on the chain and the square lattice',
          np.allclose(chain, 2 * JS * (1 - np.cos(k))) and np.allclose(square, 4 * JS * (1 - 0.5 * (np.cos(kx) + np.cos(ky)))), 'ok')

    # (6.8) is exact for one magnon: the 4x4 torus of spins 1/2, plane waves at Gamma, X, M with 0, 4|J|S, 8|J|S,
    # and the pyqula script of the figure gives the same numbers in units of |J|S
    J = -1.0
    E0, h1, closed, pos = one_magnon_torus(4, J)
    vals, res = [], 0.0
    for q in ((0, 0), (np.pi, 0), (np.pi, np.pi)):
        psi = np.exp(1j * (pos @ np.array(q))) / 4.0
        hp = h1 @ psi
        e = np.real(np.vdot(psi, hp))
        res = max(res, np.abs(hp - e * psi).max())
        vals.append(e - E0)
    S = 0.5
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as d:
        os.chdir(d)
        try:
            g = runpy.run_path(os.path.join(ROOT, 'webnotes', 'scripts', 'session06', 'g4_magnon_square.py'))
        finally:
            os.chdir(cwd)
    e = np.asarray(g['e'], float)
    ok = closed < 1e-12 and res < 1e-12 and np.allclose(vals, np.array([0, 4, 8]) * abs(J) * S)
    ok &= np.allclose(e[[0, 100, 200]], np.array(vals) / (abs(J) * S))
    check('(6.8) exact for one magnon on a 4x4 torus: 0, 4|J|S, 8|J|S at Gamma, X, M, as the pyqula script gives',
          ok, (np.round(vals, 12).tolist(), e[[0, 100, 200]].tolist()))

    # the key box of (6.8): quadratic at small k, |J|S k^2 on the chain and on the square lattice, along x and the diagonal
    q = 1e-3
    efm_chain = 2 * abs(J) * S * (1 - np.cos(q))
    efm_sq_x = 4 * abs(J) * S * (1 - 0.5 * (np.cos(q) + 1))
    efm_sq_d = 4 * abs(J) * S * (1 - np.cos(q / np.sqrt(2)))
    check('(6.8) at small k: |J|S k^2 on the chain and on the square lattice, the same along x and along the diagonal',
          np.allclose([efm_chain, efm_sq_x, efm_sq_d], abs(J) * S * q ** 2, rtol=1e-5), (efm_chain / q ** 2, efm_sq_x / q ** 2))

    # the steps fold: the commutator matrix [[eps, -Delta], [Delta, -eps]] has +-sqrt(eps^2 - Delta^2), and its
    # eigenvector normalized with u^2 - v^2 = 1 has u^2 = (eps/omega + 1)/2 and v^2 = (1/sqrt(1 - gamma^2) - 1)/2
    Jp, S, z = 1.0, 0.5, 2
    eps = Jp * S * z
    ok, worst = True, 0.0
    for kk in (0.3, 0.9, 1.4, 2.5):
        gam = np.cos(kk)
        delta = eps * gam
        M = np.array([[eps, -delta], [delta, -eps]])
        w, V = np.linalg.eig(M)
        i = np.argmax(w.real)
        u, v = V[:, i].real / np.sqrt(V[0, i].real ** 2 - V[1, i].real ** 2)
        om = np.sqrt(eps ** 2 - delta ** 2)
        ok &= np.isclose(w[i].real, om) and np.isclose(np.sort(w.real)[0], -om) and np.isclose(om, Jp * S * z * np.sqrt(1 - gam ** 2))
        ok &= np.isclose(u * u, 0.5 * (eps / om + 1)) and np.isclose(v * v, 0.5 * (1 / np.sqrt(1 - gam ** 2) - 1))
    check('fold: the commutator matrix gives omega = JSz sqrt(1 - gamma^2), u^2 = (eps/omega+1)/2, v^2 = (1/sqrt(1-gamma^2)-1)/2', ok, 'ok')

    # the commutators of the fold, on a truncated two-mode Fock space, away from the cut
    nm = 12
    a1 = np.diag(np.sqrt(np.arange(1, nm)), 1)
    A, B = np.kron(a1, np.eye(nm)), np.kron(np.eye(nm), a1)
    eps, delta = 1.0, 0.6
    Hk = eps * (A.T @ A + B.T @ B) + delta * (A @ B + A.T @ B.T)
    low = np.kron(np.diag(np.arange(nm) < nm - 3), np.diag(np.arange(nm) < nm - 3)).astype(float)
    c1 = (A @ Hk - Hk @ A) - (eps * A + delta * B.T)
    c2 = (B.T @ Hk - Hk @ B.T) - (-eps * B.T - delta * A)
    check('fold: [a, H] = eps a + Delta b^dagger and [b^dagger, H] = -eps b^dagger - Delta a',
          np.abs(c1 @ low).max() < 1e-12 and np.abs(c2 @ low).max() < 1e-12, (np.abs(c1 @ low).max(), np.abs(c2 @ low).max()))

    # the fold by a second route: the exact levels of the two-mode boson Hamiltonian. The lowest level of n_a - n_b = 1
    # is omega above the ground state, and the ground state holds v^2 bosons a, 1.19 at k = 0.3 on the chain and 0
    # at k = pi/2, where gamma = 0 and a is already the magnon with the energy JSz
    rows, ok = [], True
    for kk in (0.3, 1.0, np.pi / 2):
        gam = np.cos(kk)
        w0, n0 = two_mode(eps, eps * gam, 0)
        w1, _ = two_mode(eps, eps * gam, 1)
        om = eps * np.sqrt(1 - gam ** 2)
        v2 = 0.5 * (1 / np.sqrt(1 - gam ** 2) - 1)
        ok &= np.isclose(w1[0] - w0[0], om, atol=1e-10) and np.isclose(n0, v2, atol=1e-10)
        rows.append((round(kk, 4), round(w1[0] - w0[0], 10), round(n0, 10)))
    v203 = 0.5 * (1 / np.sin(0.3) - 1)
    ok &= np.isclose(round(v203, 2), 1.19) and np.isclose(rows[2][2], 0, atol=1e-12) and np.isclose(rows[2][1], eps)
    check('fold: exact two-mode levels give omega and v^2, 1.19 at k = 0.3 and 0 at k = pi/2 with the energy JSz', ok, rows)

    # the fold: with fermions the same steps give sqrt(eps^2 + Delta^2), the root of (5.9)
    xi, dl = 1.0, 0.7
    Hf, Nf = fermion_pair(xi, dl)
    w, V = np.linalg.eigh(Hf)
    par = np.round(np.diag(V.T @ Nf @ V)) % 2
    even, odd = w[par == 0].min(), w[par == 1].min()
    check('fold: two fermion modes have the lowest excitation sqrt(xi^2 + Delta^2), the root of (5.9)',
          np.isclose(odd - even, np.sqrt(xi ** 2 + dl ** 2)) and not np.isclose(odd - even, np.sqrt(xi ** 2 - dl ** 2)),
          round(odd - even, 10))

    # the reason of the fold: the sign comes from the pair term. Bosons have [a, a^dagger b^dagger] = +b^dagger and
    # [b^dagger, a b] = -a, so the matrix is not symmetric; fermions, with the pair term a b + b^dagger a^dagger, have
    # [a, b^dagger a^dagger] = -b^dagger and [b^dagger, a b] = -a, so it is symmetric. [b^dagger, b^dagger b] = -b^dagger
    # holds for both, so it is not what separates them
    c = np.array([[0.0, 1.0], [0.0, 0.0]])
    fa, fb = np.kron(c, np.eye(2)), np.kron(np.diag([1.0, -1.0]), c)
    com = lambda x, y: x @ y - y @ x
    ok = np.allclose(com(fa, fb.T @ fa.T), -fb.T) and np.allclose(com(fb.T, fa @ fb), -fa)
    ok &= np.allclose(com(fa, Hf), xi * fa - dl * fb.T) and np.allclose(com(fb.T, Hf), -xi * fb.T - dl * fa)
    ok &= np.allclose(com(fb.T, fb.T @ fb), -fb.T)
    ok &= np.abs((com(A, A.T @ B.T) - B.T) @ low).max() < 1e-12 and np.abs((com(B.T, A @ B) + A) @ low).max() < 1e-12
    ok &= np.abs((com(B.T, B.T @ B) + B.T) @ low).max() < 1e-12
    fm = np.array([[xi, -dl], [-dl, -xi]])                          # the fermion matrix of the same steps
    ok &= np.allclose(fm, fm.T) and np.allclose(np.sort(np.linalg.eigvalsh(fm)), [-np.sqrt(xi ** 2 + dl ** 2), np.sqrt(xi ** 2 + dl ** 2)])
    check('fold: the pair term gives +b^dagger for bosons and -b^dagger for fermions, [b^dagger, b^dagger b] = -b^dagger for both',
          ok, 'ok')

    # (6.9) by a third route: a real-space bosonic Bogoliubov ring of 2M sites, A = JSz + h on every site and B = JS
    # on every bond, whose dynamical matrix sigma_z M has the energies sqrt((JSz + h)^2 - (JSz cos k)^2), so 2JS|sin k|
    # for h -> 0; h = 1e-3 keeps the two zero modes, at k = 0 and pi, away from zero
    N, h = 24, 1e-3
    Amat = (Jp * S * 2 + h) * np.eye(N)
    Bmat = np.zeros((N, N))
    for i in range(N):
        Bmat[i, (i + 1) % N] = Bmat[(i + 1) % N, i] = Jp * S
    M = np.block([[Amat, Bmat], [Bmat, Amat]])
    w = np.linalg.eigvals(np.diag(np.r_[np.ones(N), -np.ones(N)]) @ M)
    pos_w = np.sort(w.real[w.real > 0])
    ks = 2 * np.pi * np.arange(N) / N
    ref = np.sort(np.sqrt((Jp * S * 2 + h) ** 2 - (Jp * S * 2 * np.cos(ks)) ** 2))
    small = np.sort(2 * Jp * S * np.abs(np.sin(ks)))
    check('(6.9) from a real-space bosonic Bogoliubov ring, 2JS|sin k| up to the regulator h = 1e-3',
          np.allclose(np.abs(w.imag), 0, atol=1e-9) and np.allclose(pos_w, ref, atol=1e-9) and np.allclose(pos_w, small, atol=0.05),
          np.round(pos_w[:4], 6).tolist())

    # the key box of (6.9) and the lab box: zero at k = 0 and, on the square lattice, at (pi, pi); linear at small k
    sq = lambda qx, qy: Jp * S * 4 * np.sqrt(max(0.0, 1 - (0.5 * (np.cos(qx) + np.cos(qy))) ** 2))
    check('(6.9) on the square lattice: gamma(pi,pi) = -1, so the band is zero at (pi,pi) and at 0',
          np.isclose(0.5 * (np.cos(np.pi) + np.cos(np.pi)), -1) and sq(np.pi, np.pi) == 0 and sq(0, 0) == 0, (sq(np.pi, np.pi), sq(0, 0)))
    # the lab box: the two numbers are read from the stored abstract, and the gap is converted from micro-eV to meV
    src = os.path.join(ROOT, 'webnotes', 'sources', 'session06', 'lumsden2006_arxivcond-mat-0609775.txt')
    with open(src, encoding='utf-8') as fh:
        text = fh.read()
    sentence = ('A small energy gap of 72+/-9 micro-eV is observed at the antiferromagnetic zone center and the '
                'near-neighbor exchange constant is determined to be 1.08+/-0.03 meV.')
    gap_uev = float(re.search(r'gap of (\d+)\+/-(\d+) micro-eV', text).group(1))
    jx = re.search(r'determined to be ([\d.]+)\+/-([\d.]+) meV', text)
    gap_mev = gap_uev * 1e-6 / 1e-3
    check('lab box: the source states 72+/-9 micro-eV and 1.08+/-0.03 meV, and 72 micro-eV is 0.072 meV',
          sentence in ' '.join(text.split()) and gap_uev == 72 and float(jx.group(1)) == 1.08
          and float(jx.group(2)) == 0.03 and np.isclose(gap_mev, 0.072), (gap_uev, jx.group(0), gap_mev))

    # the fold: v^2 ~ 1/(2|k|) near 0, its mean over the chain grows by (ln 10)/pi = 0.733 per decade of k-points,
    # and on the square lattice the mean converges to 0.1966, about 0.2, which leaves 0.30 of S = 1/2
    qs = np.array([1e-3, 1e-4])
    near = 0.5 * (1 / np.abs(np.sin(qs)) - 1) * 2 * qs
    means = []
    for Nk in (100, 1000, 10000):
        kk = 2 * np.pi * (np.arange(Nk) + 0.5) / Nk - np.pi
        means.append(np.mean(0.5 * (1 / np.abs(np.sin(kk)) - 1)))
    steps = np.diff(means)
    sqm = []
    for nk in (400, 800):
        kk = 2 * np.pi * (np.arange(nk) + 0.5) / nk - np.pi
        gx, gy = np.meshgrid(kk, kk)
        gam = 0.5 * (np.cos(gx) + np.cos(gy))
        sqm.append(np.mean(0.5 * (1 / np.sqrt(1 - gam ** 2) - 1)))
    limit = 2 * sqm[1] - sqm[0]                      # the error falls as 1/nk, so this removes its leading part
    ok = np.allclose(near, 1, atol=1e-3) and np.allclose(steps, np.log(10) / np.pi, rtol=1e-3)
    ok &= abs(limit - 0.1966) < 2e-4 and np.isclose(round(limit, 1), 0.2) and np.isclose(round(0.5 - limit, 2), 0.30)
    check('fold: v^2 ~ 1/(2|k|), chain average grows by 0.733 per decade, square lattice 0.1966 so S = 1/2 keeps 0.30',
          ok, (np.round(means, 3).tolist(), np.round(sqm, 5).tolist(), round(limit, 5)))

    # quiz 1: 0.0050, 0.0199 for 1 - cos k and 0.0998, 0.1987 for |sin k| at k = 0.1, 0.2, ratios about 4 and 2
    f1, f2, a1_, a2_ = 1 - np.cos(0.1), 1 - np.cos(0.2), np.sin(0.1), np.sin(0.2)
    ok = [round(f1, 4), round(f2, 4), round(a1_, 4), round(a2_, 4)] == [0.0050, 0.0199, 0.0998, 0.1987]
    ok &= round(f2 / f1) == 4 and round(a2_ / a1_) == 2
    check('quiz 1: 0.0050, 0.0199, 0.0998, 0.1987, ratios about 4 and 2', ok, (f1, f2, a1_, a2_, f2 / f1, a2_ / a1_))

    # quiz 2: gamma = 1, 0, -1 at (0,0), (pi,0), (pi,pi), so E = 0, 4|J|S, 8|J|S for z = 4
    gam = lambda qx, qy: 0.5 * (np.cos(qx) + np.cos(qy))
    Es = [4 * (1 - gam(*p)) for p in ((0, 0), (np.pi, 0), (np.pi, np.pi))]
    check('quiz 2: gamma 1, 0, -1 and E 0, 4|J|S, 8|J|S = 2|J|Sz at (0,0), (pi,0), (pi,pi)',
          np.allclose([gam(0, 0), gam(np.pi, 0), gam(np.pi, np.pi)], [1, 0, -1]) and np.allclose(Es, [0, 4, 8]), Es)

    # quiz 3: the chain with J > 0, S = 1/2 has 2JS|sin k| = |sin k| for J = 1, 2JS|k| at small k; the parabola is
    # 0.005 and 0.020 at k = 0.1 and 0.2; the gapped curve is 0.2 at k = 0, while the uniform rotation costs zero
    ok = np.isclose(2 * 1.0 * 0.5 * abs(np.sin(0.4)), abs(np.sin(0.4))) and np.isclose(2 * 1.0 * 0.5 * np.sin(q) / q, 1, rtol=1e-6)
    ok &= round(f1, 3) == 0.005 and round(f2, 3) == 0.020
    check('quiz 3: 2JS|sin k| = |sin k| for S = 1/2, J = 1, slope 2JS; the parabola 0.005 and 0.020', ok, 'ok')

    # quiz 3, feedback of the gapped option: in linear spin-wave theory the magnon at k = 0 has zero energy for any
    # J > 0. The real-space Bogoliubov ring of 24 sites, with the regulator h on every site, has its lowest mode at
    # sqrt(2 JSz h + h^2), which goes to zero with h for J = 0.3, 1 and 2.5
    lows = []
    for Jg in (0.3, 1.0, 2.5):
        row = []
        for hg in (1e-4, 1e-6):
            Am = (Jg * 0.5 * 2 + hg) * np.eye(24)
            Bm = np.zeros((24, 24))
            for i in range(24):
                Bm[i, (i + 1) % 24] = Bm[(i + 1) % 24, i] = Jg * 0.5
            wg = np.linalg.eigvals(np.diag(np.r_[np.ones(24), -np.ones(24)]) @ np.block([[Am, Bm], [Bm, Am]]))
            low = np.sort(wg.real[wg.real > 0])[0]
            row.append(low)
            assert np.isclose(low, np.sqrt(2 * Jg * 0.5 * 2 * hg + hg ** 2), rtol=1e-4)
        lows.append(row)
    lows = np.array(lows)
    check('quiz 3: the k = 0 magnon of linear spin-wave theory goes to zero for J = 0.3, 1, 2.5, as sqrt(2 JSz h)',
          np.all(lows[:, 1] < 3e-3) and np.allclose(lows[:, 0] / lows[:, 1], 10, rtol=1e-3), np.round(lows, 6).tolist())

    # the problem: 2JS|k| on the chain, 2 sqrt(2) JS|k| on the square lattice along x and along the diagonal
    Jp, S = 1.0, 0.5
    afm_chain = Jp * S * 2 * np.sqrt(1 - np.cos(q) ** 2) / q
    afm_x = Jp * S * 4 * np.sqrt(1 - gam(q, 0) ** 2) / q
    afm_d = Jp * S * 4 * np.sqrt(1 - gam(q / np.sqrt(2), q / np.sqrt(2)) ** 2) / q
    ok = np.isclose(afm_chain, 2 * Jp * S, rtol=1e-6) and np.allclose([afm_x, afm_d], 2 * np.sqrt(2) * Jp * S, rtol=1e-6)
    ok &= np.isclose(4 / np.sqrt(2), 2 * np.sqrt(2))
    check('problem: 2JS|k| on the chain and 2 sqrt(2) JS|k| on the square lattice, isotropic', ok, (afm_chain, afm_x, afm_d))

    # the problem, last paragraph: at first order in 1/S the quartic terms, decoupled with n = <a^dagger a> and
    # m = <a_i b_j>, multiply both the density term and the pair term of each bond by 1 - (n + m)/S, so the velocity
    # by Z_c = 1 + r/(2S) with r = 1 - <sqrt(1 - gamma^2)>. First the Wick counts on a Gaussian two-mode state,
    # <a^dagger a a b> = 2 n m and <a^dagger a b^dagger b> = n^2 + m^2, which give the factors of the decoupling
    nw = 60
    aw = np.diag(np.sqrt(np.arange(1, nw)), 1)
    Aw, Bw = sp.csr_matrix(np.kron(aw, np.eye(nw))), sp.csr_matrix(np.kron(np.eye(nw), aw))
    Hw = 1.0 * (Aw.T @ Aw + Bw.T @ Bw) + 0.6 * (Aw @ Bw + Aw.T @ Bw.T)
    gw = sla.eigsh(Hw, k=1, which='SA')[1][:, 0]
    ev = lambda O: gw @ (O @ gw)
    nw_, mw_ = ev(Aw.T @ Aw), ev(Aw @ Bw)
    ok = np.isclose(ev(Aw.T @ Aw @ Aw @ Bw), 2 * nw_ * mw_) and np.isclose(ev(Aw.T @ Aw @ Bw.T @ Bw), nw_ ** 2 + mw_ ** 2)
    ok &= np.isclose(mw_, -0.6 / (2 * np.sqrt(1 - 0.36)))                          # <a b> = -Delta/(2 omega)
    # then r by adaptive quadrature, and n, m separately on midpoint meshes of 400 and 800 with the 1/nk part removed
    val = integrate.dblquad(lambda y, x: np.sqrt(max(0.0, 1 - (0.5 * (np.cos(x) + np.cos(y))) ** 2)),
                            0, np.pi, 0, np.pi, epsabs=1e-9, epsrel=1e-9)[0]
    r = 1 - val / np.pi ** 2
    nm_ = []
    for nk in (400, 800):
        kk = 2 * np.pi * (np.arange(nk) + 0.5) / nk - np.pi
        gx, gy = np.meshgrid(kk, kk)
        gm = 0.5 * (np.cos(gx) + np.cos(gy))
        sq_ = np.sqrt(1 - gm ** 2)
        nm_.append((np.mean(0.5 * (1 / sq_ - 1)), np.mean(-gm ** 2 / (2 * sq_))))
    n_ = 2 * nm_[1][0] - nm_[0][0]
    m_ = 2 * nm_[1][1] - nm_[0][1]
    Zc = 1 - (n_ + m_) / 0.5
    ok &= abs(r - 0.15795) < 1e-5 and abs((n_ + m_) + r / 2) < 1e-6 and np.isclose(Zc, 1 + r / (2 * 0.5), atol=1e-6)
    ok &= round(100 * (Zc - 1)) == 16
    check('problem: Z_c = 1 + r/(2S) = 1.158 for S = 1/2 on the square lattice, r = 0.158, so about 16 percent',
          ok, (round(r, 6), round(n_, 6), round(m_, 6), round(Zc, 6)))

    # corrected on 2026-11-22, the caption of afm_bogoliubov (b): v_k^2 = (1/sqrt(1 - cos^2 k) - 1)/2 is zero only at
    # k = +-pi/2, where gamma_k = cos k = 0, and positive everywhere else on the chain, by the closed form and by the
    # numerical Bogoliubov matrix of the fold at each k
    kk = np.linspace(-np.pi, np.pi, 2001)[1:-1]
    kk = kk[np.abs(np.abs(kk) - np.pi) > 1e-6]
    kk = kk[np.abs(kk) > 1e-6]
    v2c = 0.5 * (1 / np.abs(np.sin(kk)) - 1)
    zero = kk[v2c < 1e-9]
    v2n = []
    for k in (0.3, 1.0, np.pi / 2, 2.0, 2.9):
        gam = np.cos(k)
        M = np.array([[1.0, -gam], [gam, -1.0]])                     # [[eps, -Delta], [Delta, -eps]] in units of JSz
        w, vec = np.linalg.eig(M)
        u, v = vec[:, np.argmax(w.real)].real
        v2n.append(v ** 2 / (u ** 2 - v ** 2))                         # normalized to u^2 - v^2 = 1
    check('caption of afm_bogoliubov (b): v_k^2 is zero only at k = +-pi/2 and positive elsewhere, closed form and '
          'Bogoliubov matrix', len(zero) == 2 and np.allclose(np.abs(zero), np.pi / 2) and np.all(v2c[np.abs(np.abs(kk) - np.pi / 2) > 1e-3] > 0)
          and np.allclose(v2n, [0.5 * (1 / abs(np.sin(k)) - 1) for k in (0.3, 1.0, np.pi / 2, 2.0, 2.9)], atol=1e-12),
          (np.round(zero, 6).tolist(), np.round(v2n, 4).tolist()))

    print(f'{COUNT[0]} checks, all OK')


if __name__ == '__main__':
    main()
