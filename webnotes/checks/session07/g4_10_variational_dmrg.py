"""Session 7, the numbers and statements that page 10 (Section 7.10) quotes and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. dmrg_sweeps.py asserts its three caption values and the options of the picture
quiz assert their changes by hand, and build.py --verify runs only this folder, so the sweeps run here again through
figures/session07/_g4_sweeps.py, which writes no file. For the 50 random starts of the caption and for the two-site
update, which the full-state code of _g4_sweeps.py makes too slow, this script has its own one-site sweep on MPO
environments, with the same random tensors and the same order of the updates, and it asserts first that this sweep
gives the curves of _g4_sweeps.py for M = 2, 4 and 8. This script holds, in the order of the page: the bound E >= E0 of
the key box on random states, the rise of the two-site update after its truncation, the 2M^2 numbers, the
normalization N = 1 in an orthonormal gauge and the lowest eigenvalue of the fold, the simplest case H_eff = H, the
caption values, the range over 50 random starts and the level that all of them reach, the feedback of the two
quizzes, and the numbers of the problem. It finds the repository from its own path and writes no file.

Run it from anywhere:  python3 webnotes/checks/session07/g4_10_variational_dmrg.py"""
import os
import sys
sys.dont_write_bytecode = True
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_v, '2')          # small matrices, many threads only fight on a busy machine

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, '..', '..', 'figures', 'session07')
sys.path.insert(0, FIG)
sys.path.insert(0, os.path.join(FIG, '..'))
import _g4_sweeps as sw  # noqa: E402


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


H, E0, L = sw.H, sw.E0, sw.L
rng = np.random.default_rng(7)

# the key box: E[psi] >= E0 for every state, here for 200 random states of the chain of 10 sites
Es = []
for _ in range(200):
    v = rng.normal(size=2 ** L) + 1j * rng.normal(size=2 ** L)
    Es.append((v.conj() @ H @ v).real / (v.conj() @ v).real)
check('key box, the Rayleigh quotient of 200 random states is above E0 = -4.258035', min(Es) > E0
      and abs(E0 + 4.258035) < 1e-6, (round(E0, 6), round(min(Es), 4)))



# the one-site sweep of _g4_sweeps.sweep, written with the MPO of the Heisenberg chain and its environments, and the
# two-site update with a truncation to M after each step, which is the default update of dmrgpy
SP = np.array([[0, 1], [0, 0.]])
W = np.zeros((5, 5, 2, 2))
W[0, 0] = W[4, 4] = np.eye(2)
W[1, 0], W[2, 0], W[3, 0] = SP, SP.T, np.diag([0.5, -0.5])
W[4, 1], W[4, 2], W[4, 3] = SP.T / 2, SP / 2, np.diag([0.5, -0.5])
WS = [W[4:5]] + [W] * (L - 2) + [W[:, 0:1]]                   # W[a, b, out, in]


def lenv(Le, A, Wk):                                           # Le[ket, mpo, bra]
    return np.einsum('xyz,xta,ywst,zsb->awb', Le, A, Wk, A)


def renv(Re, A, Wk):
    return np.einsum('xyz,asx,wyts,btz->awb', Re, A, Wk, A)


def heff(Le, Wk, Re):
    h = np.einsum('awb,wyts,xyc->btcasx', Le, Wk, Re)
    n = h.shape[0] * h.shape[1] * h.shape[2]
    return h.reshape(n, n)


def start(M, seed):
    """The random MPS of _g4_sweeps.sweep, brought to the right-orthonormal form, which does not change the state."""
    rng_s = np.random.default_rng(seed)
    D = [1] + [min(M, 2 ** min(k, L - k)) for k in range(1, L)] + [1]
    A = [rng_s.normal(size=(D[k], 2, D[k + 1])) for k in range(L)]
    for k in range(L - 1, 0, -1):
        q, r = np.linalg.qr(A[k].reshape(A[k].shape[0], -1).T)
        A[k] = q.T.reshape(-1, 2, A[k].shape[2])
        A[k - 1] = np.einsum('asb,cb->asc', A[k - 1], r)
    Le = [np.ones((1, 1, 1))] + [None] * L
    Re = [None] * L + [np.ones((1, 1, 1))]
    for k in range(L - 1, 0, -1):
        Re[k] = renv(Re[k + 1], A[k], WS[k])
    return A, Le, Re


def one_site(M, nsweeps=3, seed=1):
    A, Le, Re = start(M, seed)
    order = (list(range(L)) + list(range(L - 2, 0, -1))) * nsweeps
    out = []
    for i, k in enumerate(order):
        w, v = np.linalg.eigh(heff(Le[k], WS[k], Re[k + 1]))
        A[k] = v[:, 0].reshape(A[k].shape)
        out.append(w[0])
        if i + 1 == len(order):
            break
        if order[i + 1] > k:                                   # move the center to the right
            q, r = np.linalg.qr(A[k].reshape(-1, A[k].shape[2]))
            A[k] = q.reshape(A[k].shape[0], 2, -1); A[k + 1] = np.einsum('ab,bsc->asc', r, A[k + 1])
            Le[k + 1] = lenv(Le[k], A[k], WS[k])
        else:                                                  # or to the left
            q, r = np.linalg.qr(A[k].reshape(A[k].shape[0], -1).T)
            A[k] = q.T.reshape(-1, 2, A[k].shape[2]); A[k - 1] = np.einsum('asb,cb->asc', A[k - 1], r)
            Re[k] = renv(Re[k + 1], A[k], WS[k])
    return np.array(out)


def two_site(M, nsweeps=6, seed=1):
    """For every step, the energy of the local minimum over the pair and the energy after the truncation to M."""
    A, Le, Re = start(M, seed)
    out = []
    for _ in range(nsweeps):
        for right, ks in ((True, range(L - 1)), (False, range(L - 2, -1, -1))):
            for k in ks:
                W2 = np.einsum('abst,bcuv->acsutv', WS[k], WS[k + 1]).reshape(WS[k].shape[0], WS[k + 1].shape[1], 4, 4)
                h = heff(Le[k], W2, Re[k + 2])
                w, v = np.linalg.eigh(h)
                da, dc = A[k].shape[0], A[k + 1].shape[2]
                U, sv, Vt = np.linalg.svd(v[:, 0].reshape(da * 2, 2 * dc), full_matrices=False)
                m = min(M, int(np.sum(sv > 1e-14 * sv[0])))
                t = ((U[:, :m] * sv[:m]) @ Vt[:m]).reshape(-1)
                out.append((w[0], t @ h @ t / (t @ t)))
                sv = sv[:m] / np.linalg.norm(sv[:m])
                if right:
                    A[k] = U[:, :m].reshape(da, 2, m); A[k + 1] = (sv[:, None] * Vt[:m]).reshape(m, 2, dc)
                    Le[k + 1] = lenv(Le[k], A[k], WS[k])
                else:
                    A[k] = (U[:, :m] * sv).reshape(da, 2, m); A[k + 1] = Vt[:m].reshape(m, 2, dc)
                    Re[k + 1] = renv(Re[k + 2], A[k + 1], WS[k + 1])
    return np.array(out)


curves = {2: sw.sweep(2), 4: sw.E, 8: sw.sweep(8)}
same = max(np.abs(one_site(Mx) - e).max() for Mx, e in curves.items())
check('this script, its one-site sweep on MPO environments gives the curves of _g4_sweeps.py for M = 2, 4, 8',
      same < 1e-10, same)

# the key box and the first quiz: the two-site update truncates after each step, so its energy can go up a little, by
# about 1e-4 J for M = 4 on the chain of 10 sites (seeds 1 to 8, six sweeps), while the local minimum itself is never
# above the energy of the step before
rises, opt_up, ends2 = [], [], []
for sd in range(1, 9):
    o = two_site(4, seed=sd)
    rises.append(np.diff(o[:, 1]).max())
    opt_up.append(np.max(o[1:, 0] - o[:-1, 1]))
    ends2.append(o[-1, 1] - E0)
check('key box and first quiz, the two-site update with M = 4 goes up after its truncation, by at most about 1e-4 J, '
      'and never in the local minimum', 5e-5 < max(rises) < 2e-4 and min(rises) > 1e-8 and max(opt_up) < 1e-12,
      (float('%.3g' % max(rises)), float('%.3g' % min(rises)), float('%.2g' % max(opt_up)),
       float('%.3g' % min(ends2)), float('%.3g' % max(ends2))))

# the fold: an MPS of 8 sites with M = 4, the tensor of the bulk site k = 4 has 2 M^2 = 32 numbers, the state is linear
# in it, and in the mixed gauge (left tensors left-orthonormal, right tensors right-orthonormal) N = 1
Lf, M, k = 8, 4, 4
D = [1] + [min(M, 2 ** min(j, Lf - j)) for j in range(1, Lf)] + [1]
A = [rng.normal(size=(D[j], 2, D[j + 1])) for j in range(Lf)]
for j in range(k):                                             # left-orthonormal by QR, the rest pushed to the right
    q, r = np.linalg.qr(A[j].reshape(D[j] * 2, D[j + 1]))
    A[j] = q.reshape(D[j], 2, D[j + 1])
    A[j + 1] = np.einsum('ab,bsc->asc', r, A[j + 1])
for j in range(Lf - 1, k, -1):                                 # right-orthonormal from the right
    q, r = np.linalg.qr(A[j].reshape(D[j], 2 * D[j + 1]).T)
    A[j] = q.T.reshape(D[j], 2, D[j + 1])
    A[j - 1] = np.einsum('asb,cb->asc', A[j - 1], r)


def full(As):
    c = np.ones((1, 1))
    for a in As:
        c = np.einsum('xa,asb->xsb', c, a).reshape(-1, a.shape[2])
    return c[:, 0]


nA = A[k].size
phis = []
for j in range(nA):
    e = np.zeros(nA)
    e[j] = 1
    phis.append(full(A[:k] + [e.reshape(A[k].shape)] + A[k + 1:]))
Phi = np.array(phis).T
SXs, SYs, SZs = sw.sx, sw.sy, sw.sz


def site(o, i, n):
    m = np.eye(1)
    for j in range(n):
        m = np.kron(m, o if j == i else np.eye(2))
    return m


Hf = sum(site(s, i, Lf) @ site(s, i + 1, Lf) for i in range(Lf - 1) for s in (SXs, SYs, SZs)).real
psi = full(A)
Nmat = Phi.T @ Phi
Heff = Phi.T @ Hf @ Phi
lin = np.abs(Phi @ A[k].reshape(-1) - psi).max()
check('fold, the bulk tensor has 2 M^2 = 32 numbers, the state is linear in it, and N = 1 in the orthonormal gauge',
      nA == 2 * M ** 2 == 32 and lin < 1e-10 and np.abs(Nmat - np.eye(nA)).max() < 1e-10, (nA, lin, np.abs(Nmat - np.eye(nA)).max()))
a = A[k].reshape(-1)
Eold = a @ Heff @ a / (a @ Nmat @ a)
Eold_full = psi @ Hf @ psi / (psi @ psi)
wl, vl = np.linalg.eigh(Heff)
Anew = vl[:, 0]
psin = Phi @ Anew
check('fold, E = A H_eff A / A N A, and the lowest eigenvalue of H_eff A = E A is the energy of the new state, at most the old one',
      abs(Eold - Eold_full) < 1e-10 and abs(wl[0] - psin @ Hf @ psin / (psin @ psin)) < 1e-10 and wl[0] <= Eold + 1e-12,
      (round(Eold, 6), round(wl[0], 6)))
# the simplest case: one tensor that is the whole state, with a physical leg of dimension 2^Lf, built with the code of
# the fold. Then the |phi_j> are the basis states, H_eff = H, N = 1, and the lowest eigenvalue is the ground energy
whole = rng.normal(size=(1, 2 ** Lf, 1))
Phi1 = np.array([full([np.eye(2 ** Lf)[j].reshape(whole.shape)]) for j in range(2 ** Lf)]).T
check('fold, the simplest case, a tensor that is the whole state, has H_eff = H and N = 1, and gives the ground energy',
      np.abs(Phi1.T @ Hf @ Phi1 - Hf).max() < 1e-14 and np.abs(Phi1.T @ Phi1 - np.eye(2 ** Lf)).max() < 1e-14
      and abs(np.linalg.eigvalsh(Phi1.T @ Hf @ Phi1)[0] - np.linalg.eigvalsh(Hf)[0]) < 1e-12,
      round(np.linalg.eigvalsh(Hf)[0], 6))

# the caption: the sweeps of dmrg_sweeps.py, repeated by _g4_sweeps.sweep with the same steps
end = {Mx: e[-1] - E0 for Mx, e in curves.items()}
check('caption, one sweep is 18 updates, and three sweeps end at 0.2, 6e-3 and 1.5e-5 in units of J for M = 2, 4, 8',
      len(sw.E) == 3 * 18 and 2 * L - 2 == 18 and abs(end[2] - 0.2) < 0.005 and abs(end[4] - 6e-3) < 3e-4
      and abs(end[8] - 1.5e-5) < 1e-6, {Mx: float('%.4g' % v) for Mx, v in end.items()})
# the caption: for M = 4, the 50 random starts of the seeds 1 to 50, the one of the figure among them, end between
# 6.1e-3 and 1.1e-2 after three sweeps, and after eight sweeps all of them sit at the same 6.1e-3
runs = np.array([one_site(4, nsweeps=8, seed=sd) for sd in range(1, 51)]) - E0
three, eight = runs[:, 3 * 18 - 1], runs[:, -1]
check('caption, for M = 4 the 50 random starts end between 6.1e-3 and 1.1e-2 after three sweeps',
      6.05e-3 <= three.min() < 6.15e-3 and 1.05e-2 <= three.max() < 1.15e-2 and abs(three[0] - end[4]) < 1e-12,
      (float('%.4g' % three.min()), float('%.4g' % three.max()), int(np.sum(three > 9e-3))))
check('caption, after eight sweeps all 50 starts reach the same 6.1e-3', eight.max() - eight.min() < 1e-6
      and 6.05e-3 <= eight.min() and eight.max() < 6.15e-3, (float('%.6g' % eight.min()), float('%.3g' % (eight.max() - eight.min()))))
mono = max(np.diff(e).max() for e in curves.values())
check('caption and first quiz, no curve ever goes up', mono < 1e-9, mono)

# the first quiz: the right option ends 6e-3 J above E0, which is on the line on an axis of 5.6 J, and the two wrong ones
check('first quiz, M = 4 ends 6e-3 J above E0, less than 1/500 of the 5.6 J of the axis', abs(end[4] - 6e-3) < 3e-4
      and end[4] / 5.6 < 1 / 500, end[4])
up = sw.E.copy()
up[sw.K_UP] += sw.UP
below = sw.E - sw.SHIFT
check('first quiz, the option changed by hand goes up by 1.5 J at one update, the shifted one ends 0.5 J lower, below E0',
      sw.UP == 1.5 and np.sum(np.diff(up) > 1e-9) == 1 and sw.SHIFT == 0.5 and below[-1] < E0,
      (sw.K_UP, round(below[-1] - E0, 4)))

# the second quiz
check('second quiz, 2^40 is about 1e12, 2 x 100^2 = 2e4 and 2 x 100 = 200', abs(2 ** 40 / 1e12 - 1.1) < 0.01
      and 2 * 100 ** 2 == 20000 and 2 * 100 == 200, (2 ** 40, 2 * 100 ** 2))

# the problem: two levels E0 = -1, E1 = 0 and the equal superposition give E = -0.5, and an amplitude delta in the excited
# level gives an error of order delta^2
c = np.array([1, 1]) / np.sqrt(2)
En = np.array([-1.0, 0.0])
Ep = np.sum(np.abs(c) ** 2 * En) / np.sum(np.abs(c) ** 2)
errs = []
for d in (1e-1, 1e-2, 1e-3):
    cc = np.array([1, d])
    errs.append((np.sum(cc ** 2 * En) / np.sum(cc ** 2) - En[0]) / d ** 2)
check('problem, E = -0.5, 0.5 above E0, and the error over delta^2 tends to E1 - E0 = 1', abs(Ep + 0.5) < 1e-15
      and abs(Ep - En[0] - 0.5) < 1e-15 and abs(errs[-1] - 1) < 1e-5, (Ep, np.round(errs, 6)))
print('all checks of page 10 passed')
