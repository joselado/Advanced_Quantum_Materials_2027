"""Session 10, the numbers that page 03b (Section 10.3b, training the network and tomography) quotes.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. The probabilities of the feedback figure tomo_phase are asserted in
figures/session10/tomo_phase.py and again here. The spin operators are S = sigma/2, so the two-site Heisenberg model
J S1.S2 has the element -J/4 on the diagonal for antiparallel spins and +J/2 between up-down and down-up. The network
is a restricted Boltzmann machine, C(s) = exp(sum_i a_i s_i) prod_j 2 cosh(b_j + sum_i W_ji s_i), as on the
conventions sheet. It finds the repository from its own path, imports nothing of it, and writes no file."""
import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def configurations(L):
    """s_i = +1 for up, in the order of np.kron with site 0 first and up first."""
    b = np.arange(2 ** L)
    return 1 - 2 * ((b[:, None] >> np.arange(L - 1, -1, -1)) & 1)


def heisenberg(L, J=1.0):
    """The open chain J sum S_i.S_i+1 with S = sigma/2 in the basis of (10.2)."""
    S, n = configurations(L), 2 ** L
    H = np.zeros((n, n))
    for i in range(L - 1):
        H[np.arange(n), np.arange(n)] += J / 4 * S[:, i] * S[:, i + 1]
        anti = np.nonzero(S[:, i] != S[:, i + 1])[0]
        H[anti, anti ^ ((1 << (L - 1 - i)) | (1 << (L - 2 - i)))] += J / 2
    return H


def rbm(par, L, M, S):
    a, b, W = par[:L], par[L:L + M], par[L + M:].reshape(M, L)
    th = b[None, :] + S @ W.T
    return np.exp(S @ a) * np.prod(2 * np.cosh(th), axis=1), th


def rbm_O(par, L, M, S):
    """O_k = d ln C / d theta_k, in the order a, b, W."""
    t = np.tanh(rbm(par, L, M, S)[1])
    return np.hstack([S, t, (t[:, :, None] * S[:, None, :]).reshape(len(S), -1)])


def energy(H, C):
    return float(np.real(np.vdot(C, H @ C)) / np.real(np.vdot(C, C)))


rng = np.random.default_rng(1)

# ------------------------------------------------------------------- the schematic local_energy and the short sum
s = np.array([1, -1, -1, 1, 1, -1])
anti = int(np.sum(s[:-1] != s[1:]))
check('the s of local_energy, six spins, has three antiparallel bonds, so three s\' besides s', anti == 3, anti)
for L in (6, 10):
    H = heisenberg(L)
    offdiag = np.count_nonzero(H - np.diag(np.diag(H)), axis=1)
    check('open Heisenberg chain of %d spins, a row has at most L-1 = %d elements off the diagonal, so at most L terms'
          % (L, L - 1), offdiag.max() == L - 1 and np.count_nonzero(H, axis=1).max() <= L, offdiag.max())


def swaps(k, L):
    """The configurations s' != s that the hopping part of the open Heisenberg chain reaches from the bit string k, one
    per bond with antiparallel spins, without building the matrix. Bit L-1-i is the spin of site i."""
    out = []
    for i in range(L - 1):
        a, b = (k >> (L - 1 - i)) & 1, (k >> (L - 2 - i)) & 1
        if a != b:
            out.append(k ^ ((1 << (L - 1 - i)) | (1 << (L - 2 - i))))
    return out


H10 = heisenberg(10)
same = all(sorted(swaps(k, 10)) == sorted(np.nonzero(H10[k])[0][np.nonzero(H10[k])[0] != k].tolist())
           for k in range(2 ** 10))
check('the count without the matrix agrees with the rows of the open chain of 10 spins, all 1024 s', same, same)
neel = int('01' * 20, 2)
rand40 = [int(x) for x in np.random.default_rng(4).integers(0, 2 ** 40, size=200, dtype=np.int64)]
n_neel = len(set(swaps(neel, 40)))
n_rand = [len(set(swaps(k, 40))) for k in rand40]
check('an open chain of 40 spins has 39 bonds, each changes s into at most one other configuration, 39 for the Neel '
      'configuration and at most 39 for 200 random ones', n_neel == 39 and max(n_rand) <= 39
      and all(len(swaps(k, 40)) == len(set(swaps(k, 40))) for k in rand40), (n_neel, max(n_rand)))

# ------------------------------------------------------------------- the network has no zero amplitude
L, M = 6, 6
S = configurations(L)
Cr = [rbm(rng.normal(scale=0.5, size=L + M + L * M), L, M, S)[0] for _ in range(20)]
check('a network with real parameters has C(s) > 0 on every configuration, 20 draws', all(np.all(c > 0) for c in Cr),
      min(c.min() for c in Cr))
Cc = [rbm(rng.normal(scale=0.3, size=L + M + L * M) + 1j * rng.normal(scale=0.3, size=L + M + L * M), L, M, S)[0]
      for _ in range(20)]
check('a network with random complex parameters has no zero amplitude, 20 draws', min(np.abs(c).min() for c in Cc) > 1e-3,
      min(np.abs(c).min() for c in Cc))

# ------------------------------------------------------------------- the steps: (10.4) and (10.5)
L, M = 8, 4
S = configurations(L)
H = heisenberg(L)
par = rng.normal(scale=0.2, size=L + M + L * M) + 1j * rng.normal(scale=0.2, size=L + M + L * M)
C = rbm(par, L, M, S)[0]
p = np.abs(C) ** 2 / np.sum(np.abs(C) ** 2)
El = (H @ C) / C
check('(10.4), the average of E_loc over p(s) is E of (10.3), complex network on the open chain of 8 spins',
      abs(p @ El - energy(H, C)) < 1e-12 and abs(np.imag(p @ El)) < 1e-12, abs(p @ El - energy(H, C)))
O = rbm_O(par, L, M, S)
F = p @ (El[:, None] * O.conj()) - (p @ El) * (p @ O.conj())
h = 1e-6
dx, dy = [], []
for k in range(len(par)):
    e = np.zeros(len(par)); e[k] = h
    dx.append((energy(H, rbm(par + e, L, M, S)[0]) - energy(H, rbm(par - e, L, M, S)[0])) / (2 * h))
    dy.append((energy(H, rbm(par + 1j * e, L, M, S)[0]) - energy(H, rbm(par - 1j * e, L, M, S)[0])) / (2 * h))
dx, dy = np.array(dx), np.array(dy)
check('(10.5), dE/dx_k = 2 Re F_k for the real part x_k of each parameter, finite differences',
      np.max(np.abs(dx - 2 * F.real)) < 1e-7, np.max(np.abs(dx - 2 * F.real)))
check('and dE/dy_k = 2 Im F_k for the imaginary part y_k, the complex case of the steps',
      np.max(np.abs(dy - 2 * F.imag)) < 1e-7, np.max(np.abs(dy - 2 * F.imag)))
G = p @ (El[:, None] * O) - (p @ El) * (p @ O)
check('with O_k in place of O_k* the gradient is wrong', np.max(np.abs(dx - 2 * G.real)) > 0.05,
      np.max(np.abs(dx - 2 * G.real)))
# The condition of the steps: the complex case needs a C that is an analytic function of theta_k, so that
# dC/dy_k = i dC/dx_k = i O_k C. The restricted Boltzmann machine has it, a C with conj(theta) in it does not.
cr = []
for k in range(len(par)):
    e = np.zeros(len(par)); e[k] = h
    dCx = (rbm(par + e, L, M, S)[0] - rbm(par - e, L, M, S)[0]) / (2 * h)
    dCy = (rbm(par + 1j * e, L, M, S)[0] - rbm(par - 1j * e, L, M, S)[0]) / (2 * h)
    cr.append(max(np.max(np.abs(dCy - 1j * dCx)), np.max(np.abs(dCx - O[:, k] * C))) / np.max(np.abs(C)))
check('the restricted Boltzmann machine is analytic, dC/dy_k = i dC/dx_k = i O_k C for every parameter',
      max(cr) < 1e-7, max(cr))
K = 10
f_na = rng.normal(scale=0.3, size=(2 ** L, K))
g_na = rng.normal(scale=0.3, size=(2 ** L, K))
t_na = rng.normal(scale=0.3, size=K) + 1j * rng.normal(scale=0.3, size=K)
C_na = lambda t: np.exp(f_na @ t + g_na @ np.conj(t))
Cn = C_na(t_na)
pn = np.abs(Cn) ** 2 / np.sum(np.abs(Cn) ** 2)
Eln = (H @ Cn) / Cn
Fn = pn @ (Eln[:, None] * f_na.conj()) - (pn @ Eln) * (pn @ f_na.conj())
dxn = np.array([(energy(H, C_na(t_na + h * np.eye(K)[k])) - energy(H, C_na(t_na - h * np.eye(K)[k]))) / (2 * h)
                for k in range(K)])
dyn = np.array([(energy(H, C_na(t_na + 1j * h * np.eye(K)[k])) - energy(H, C_na(t_na - 1j * h * np.eye(K)[k])))
                / (2 * h) for k in range(K)])
miss = max(np.max(np.abs(dxn - 2 * Fn.real)), np.max(np.abs(dyn - 2 * Fn.imag)))
check('a C = exp(theta.f + conj(theta).g), which is not analytic, misses 2 Re F and 2 Im F with O_k = f_k',
      miss > 0.01, miss)
parr = rng.normal(scale=0.2, size=L + M + L * M)
Cr = rbm(parr, L, M, S)[0]
pr = Cr ** 2 / np.sum(Cr ** 2)
Elr = (H @ Cr) / Cr
Or = rbm_O(parr, L, M, S)
Fr = 2 * (pr @ (Elr[:, None] * Or) - (pr @ Elr) * (pr @ Or))
dr = []
for k in range(len(parr)):
    e = np.zeros(len(parr)); e[k] = h
    dr.append((energy(H, rbm(parr + e, L, M, S)[0]) - energy(H, rbm(parr - e, L, M, S)[0])) / (2 * h))
check('the simplest case, real C and real parameters, dE/dtheta = 2(<E_loc O> - <E_loc><O>)',
      np.max(np.abs(np.array(dr) - Fr)) < 1e-7, np.max(np.abs(np.array(dr) - Fr)))

# ------------------------------------------------------------------- the two-site model, quiz and problem
H2 = heisenberg(2)
uu, ud, du, dd = 0, 1, 2, 3
check('two sites, H(ud,ud) = -J/4 and H(ud,du) = +J/2', abs(H2[ud, ud] + 0.25) < 1e-15 and abs(H2[ud, du] - 0.5) < 1e-15,
      (H2[ud, ud], H2[ud, du]))
singlet = np.array([0, 1, -1, 0]) / np.sqrt(2)
Els = {x: (H2[x] @ singlet) / singlet[x] for x in (ud, du)}
check('the singlet has E_loc = -3J/4 at up-down and at down-up', all(abs(v + 0.75) < 1e-14 for v in Els.values()), Els)
opt2 = H2[ud] @ singlet * singlet[ud]
opt3 = H2[ud] @ (np.abs(singlet) ** 2) / abs(singlet[ud]) ** 2
check('the quiz, sum H C(s\') C(s) gives -3J/8 at up-down', abs(opt2 + 0.375) < 1e-14, opt2)
check('the quiz, sum H |C(s\')|^2/|C(s)|^2 gives +J/4 at up-down, the triplet energy', abs(opt3 - 0.25) < 1e-14
      and abs(np.linalg.eigvalsh(H2)[-1] - 0.25) < 1e-14, opt3)
trial = np.array([0, 2, -1, 0]) / np.sqrt(5)
Elt = {x: (H2[x] @ trial) / trial[x] for x in (ud, du)}
pt = trial ** 2
check('the solution, the ratios C(du)/C(ud) = -1/2 and C(ud)/C(du) = -2, and the weights p = 4/5 and 1/5',
      abs(trial[du] / trial[ud] + 0.5) < 1e-14 and abs(trial[ud] / trial[du] + 2) < 1e-14
      and abs(pt[ud] - 0.8) < 1e-14 and abs(pt[du] - 0.2) < 1e-14 and abs(pt.sum() - 1) < 1e-14,
      (trial[du] / trial[ud], trial[ud] / trial[du], pt[ud], pt[du]))
mean =pt[ud] * Elt[ud] + pt[du] * Elt[du]
spread = np.sqrt(pt[ud] * (Elt[ud] - mean) ** 2 + pt[du] * (Elt[du] - mean) ** 2)
check('the state (2|ud> - |du>)/sqrt5 has E_loc = -J/2 at up-down and -5J/4 at down-up',
      abs(Elt[ud] + 0.5) < 1e-14 and abs(Elt[du] + 1.25) < 1e-14, Elt)
check('their average over p is its energy -0.65J, with a spread of 0.3J', abs(mean + 0.65) < 1e-14
      and abs(mean - trial @ H2 @ trial) < 1e-14 and abs(spread - 0.3) < 1e-14, (mean, spread))
check('and -0.65J lies between E0 = -3J/4 and J/4', -0.75 < mean < 0.25, mean)
E8, V8 = np.linalg.eigh(heisenberg(8))
g = V8[:, 0]
nz = np.abs(g) > 1e-10
Elg = (heisenberg(8) @ g)[nz] / g[nz]
check('at the ground state of the open chain of 8 spins E_loc is the same number on every s with C(s) != 0',
      np.max(np.abs(Elg - E8[0])) < 1e-10, (E8[0], np.max(np.abs(Elg - E8[0]))))

# ------------------------------------------------------------------- tomography
up, dn = np.array([1.0, 0.0]), np.array([0.0, 1.0])
xp, xm = (up + dn) / np.sqrt(2), (up - dn) / np.sqrt(2)
for sign in (1, -1):
    psi = (up + sign * dn) / np.sqrt(2)
    pz = [abs(up @ psi) ** 2, abs(dn @ psi) ** 2]
    px = [abs(xp @ psi) ** 2, abs(xm @ psi) ** 2]
    check('the state with %s gives 50%% and 50%% along z, and %s along x' % ('+' if sign > 0 else '-', px),
          np.allclose(pz, [0.5, 0.5]) and np.allclose(px, [1, 0] if sign > 0 else [0, 1]), (pz, px))
psi3 = rng.normal(size=8) + 1j * rng.normal(size=8)
psi3 /= np.linalg.norm(psi3)
n = rng.multinomial(1000, np.abs(psi3) ** 2).astype(float)
freq = n / n.sum()
ll = lambda q: np.sum(n[n > 0] * np.log(q[n > 0]))
others = [rng.dirichlet(np.ones(8)) for _ in range(2000)] + [np.abs(psi3) ** 2]
check('the likelihood sum n(s) ln p(s) of 1000 shots on 3 spins is largest at p(s) = n(s)/sum n',
      all(ll(q) < ll(freq) for q in others), ll(freq))
phase = np.exp(1j * rng.uniform(0, 2 * np.pi, 8))
check('a phase on each configuration changes no count, |C|^2 is the same', np.allclose(np.abs(psi3 * phase) ** 2,
      np.abs(psi3) ** 2), 1)
check('the ratio of two probabilities is |C(s)|^2/|C(s\')|^2, so the relative weight is in the counts',
      abs((np.abs(psi3[0]) ** 2 / np.abs(psi3[1]) ** 2) - abs(psi3[0] / psi3[1]) ** 2) < 1e-12, 1)
# corrected on 2026-11-22, the tomography paragraph: with counts in more than one basis, a network of far fewer
# parameters than 2^L. Counts along z fix only |C(s)| (asserted above), and a restricted Boltzmann machine with M = L
# hidden spins has L + M + L M parameters
check('an RBM with M = L hidden spins has L + M + L M parameters, 1680 for L = 40 against 2^40 = 1.1e12, and fewer '
      'than 2^L for every L from 10 on', 40 + 40 + 40 * 40 == 1680 and all(2 * n + n * n < 2 ** n / 5 for n in range(10, 41)),
      (1680, 2.0 ** 40))
print('all checks of page 03b hold')
