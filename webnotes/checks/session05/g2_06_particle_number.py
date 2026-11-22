"""Session 5, the numbers and the signs that page 06 (Sections 5.6 and 5.7) states and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold, a solution or a box is an assert, here
or in the figure script that draws it. The bars of the quiz figure, 0.5 and 0.5 at mu=0 and 0.15 and 0.85 at mu=0.5, are
asserted in figures/session05/particle_number_weights.py and again here. This script works with the matrices of the fermion
operators of a few modes, with numpy only, so it writes no file. From the repository, found from the path of this script, it
reads only the tracked source of the lab box, webnotes/sources/session05/tuominen1992_physrevlett.69.1997.txt.

Run it from anywhere:  python3 webnotes/checks/session05/g2_06_particle_number.py"""
import os

import numpy as np

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def fermions(n):
    """Annihilation operators of n fermion modes, with the Jordan-Wigner string, as 2^n x 2^n matrices. The basis state with
    the bits b_0 ... b_{n-1} has the index sum b_j 2^(n-1-j)."""
    a = np.array([[0., 1.], [0., 0.]])
    z = np.diag([1., -1.])
    out = []
    for j in range(n):
        m = np.array([[1.]])
        for i in range(n):
            m = np.kron(m, z if i < j else (a if i == j else np.eye(2)))
        out.append(m)
    return out


def dag(m):
    return m.conj().T


# ---- the key box of 5.6: on a chain of 3 sites with both spins, [H, (-1)^N] = 0 and [H, N] != 0 for Delta != 0
L = 3
c = fermions(2 * L)                                  # mode 2n is site n with spin up, mode 2n+1 is site n with spin down
up, dn = c[0::2], c[1::2]
Nop = sum(dag(x) @ x for x in c)
P = np.diag(np.exp(1j * np.pi * np.diag(Nop).real)).real
t, mu, D = 1.0, 0.3, 0.4 + 0.25j
Hhop = sum(-t * (dag(s[n]) @ s[n + 1] + dag(s[n + 1]) @ s[n]) for s in (up, dn) for n in range(L - 1)) - mu * Nop
Hpair = sum(D * dag(up[n]) @ dag(dn[n]) + np.conj(D) * dn[n] @ up[n] for n in range(L))
H = Hhop + Hpair
check('key 5.6: [H_MF, (-1)^N] = 0 on 3 sites', np.abs(H @ P - P @ H).max() < 1e-12, np.abs(H @ P - P @ H).max())
check('key 5.6: [H_MF, N] != 0 for Delta != 0', np.abs(H @ Nop - Nop @ H).max() > 0.1, round(np.abs(H @ Nop - Nop @ H).max(), 3))
check('text: the hopping and mu keep N', np.abs(Hhop @ Nop - Nop @ Hhop).max() < 1e-12, 0)
# every matrix element of H connects N and N' with N - N' in {0, 2, -2}
Nd = np.diag(Nop).real
i, j = np.nonzero(np.abs(H) > 1e-12)
check('opener and text: H changes N only by 0 or +-2', set(np.round(Nd[i] - Nd[j]).astype(int)) <= {0, 2, -2},
      sorted(set(np.round(Nd[i] - Nd[j]).astype(int))))
e, v = np.linalg.eigh(H)
g = v[:, 0]
w = {int(n): float(np.sum(np.abs(g[Nd == n])**2)) for n in range(2 * L + 1)}
check('text: the ground state has one parity and several N', (all(w[n] < 1e-12 for n in w if n % 2 == 1)
      or all(w[n] < 1e-12 for n in w if n % 2 == 0)) and sum(x > 1e-3 for x in w.values()) >= 2,
      {n: round(x, 3) for n, x in w.items() if x > 1e-6})

# ---- the steps fold: one site with both spins
c0 = fermions(2)
cu, cd = c0
n1 = dag(cu) @ cu + dag(cd) @ cd
vac = np.zeros(4); vac[0] = 1.                       # |0>, both bits zero
two = dag(cu) @ dag(cd) @ vac                        # |2> = c_up^dag c_dn^dag |0>
sup, sdn = dag(cu) @ vac, dag(cd) @ vac


def site(mu, D):
    return -mu * n1 + D * dag(cu) @ dag(cd) + np.conj(D) * cd @ cu


for mu, D in ((0.0, 0.5), (0.3, 0.2 + 0.4j), (-0.7, 0.6)):
    Hs = site(mu, D)
    pair = D * dag(cu) @ dag(cd) + np.conj(D) * cd @ cu
    ok = np.allclose(pair @ vac, D * two) and np.allclose(pair @ two, np.conj(D) * vac)
    ok = ok and np.allclose(pair @ sup, 0) and np.allclose(pair @ sdn, 0)
    ok = ok and np.allclose(Hs @ sup, -mu * sup) and np.allclose(Hs @ sdn, -mu * sdn)
    basis = np.c_[vac, two]
    Heven = dag(basis) @ Hs @ basis
    ok = ok and np.allclose(Heven, [[0, np.conj(D)], [D, -2 * mu]])
    R = np.sqrt(mu**2 + abs(D)**2)
    ok = ok and np.allclose(np.linalg.eigvalsh(Heven), [-mu - R, -mu + R]) and -mu - R < -mu
    ok = ok and np.isclose(np.linalg.eigvalsh(Hs)[0], -mu - R)
    check(f'fold: pairing on |0>, |2> and on N=1, H_even, E_pm = -mu +- sqrt(mu^2+|D|^2), even ground state, mu={mu} D={D}',
          ok, np.round(np.linalg.eigvalsh(Heven), 4))
Hs = site(0.0, 0.5)
e, v = np.linalg.eigh(Hs)
g = v[:, 0] * np.sign(v[0, 0])
check('fold and quiz: at mu=0, Delta=0.5 the ground state is (|0> - |2>)/sqrt2 at -0.5', np.isclose(e[0], -0.5)
      and np.allclose(g, (vac - two) / np.sqrt(2)), round(e[0], 4))
check('fold and quiz: P(N=0) = P(N=2) = 1/2 and P(N=1) = 0 at mu=0', np.isclose(abs(g @ vac)**2, 0.5)
      and np.isclose(abs(g @ two)**2, 0.5) and abs(g @ sup) + abs(g @ sdn) < 1e-12, 0.5)

# ---- the quiz figure and the problem: Delta=0.5, mu=0.5
Hs = site(0.5, 0.5)
basis = np.c_[vac, two]
Heven = dag(basis) @ Hs @ basis
ev = np.linalg.eigvalsh(Heven)
check('problem: H_even = [[0, 0.5], [0.5, -1]], eigenvalues -0.5 +- sqrt(0.5) = 0.207 and -1.207',
      np.allclose(Heven, [[0, 0.5], [0.5, -1]]) and np.allclose(ev, [-1.2071, 0.2071], atol=1e-4)
      and np.allclose(ev, -0.5 + np.array([-1, 1]) * np.sqrt(0.5)), np.round(ev, 4))
check('problem: the ground state -1.207 is below the odd states at -0.5', ev[0] < -0.5
      and np.isclose(np.linalg.eigvalsh(Hs)[0], ev[0]), round(ev[0], 4))
e, v = np.linalg.eigh(Heven)
a, b = v[:, 0] * np.sign(v[0, 0])
check('problem: b = 2 E a = -2.414 a', np.isclose(b / a, 2 * e[0]) and abs(b / a + 2.414) < 1e-3, round(b / a, 4))
check('problem and quiz figure: P(N=0) = 0.146 and P(N=2) = 0.854, the bars 0.15 and 0.85', abs(a**2 - 0.146) < 5e-4
      and abs(b**2 - 0.854) < 5e-4 and round(a**2, 2) == 0.15 and round(b**2, 2) == 0.85, (round(a**2, 4), round(b**2, 4)))
check('problem: the average number of electrons 2 x 0.854 = 1.707', abs(2 * b**2 - 1.707) < 5e-4, round(2 * b**2, 4))
check('problem: <N> = 2 P(N=2) = 2 x 0.8536 = 1.707, with the four digits of P(2) as printed', round(b**2, 4) == 0.8536
      and round(2 * 0.8536, 3) == 1.707 and np.isclose(2 * b**2, 1 + 1 / np.sqrt(2)), (round(b**2, 4), round(2 * 0.8536, 4)))
# <N> straight from the ground state of the 4x4 Fock matrix of the site, as a second route
e4, v4 = np.linalg.eigh(Hs)
check('problem: <G|N|G> of the 4x4 Fock matrix is 1.707', abs(np.real(v4[:, 0].conj() @ n1 @ v4[:, 0]) - 1.707) < 5e-4,
      round(np.real(v4[:, 0].conj() @ n1 @ v4[:, 0]), 4))
# the BCS pair of k and -k: weight of the pair v^2 = (1 - eps/E)/2, the same form as P(2) with eps = -mu
check('problem: P(2) = (1 + mu/sqrt(mu^2+Delta^2))/2, the v^2 of BCS with eps=-mu', np.isclose(b**2, 0.5 * (1 + 0.5 / np.hypot(0.5, 0.5))),
      round(0.5 * (1 + 0.5 / np.hypot(0.5, 0.5)), 4))

# ---- Section 5.7: the gauge transformation U c U^dag = c e^{i phi} with U = exp(-i phi N)
for phi in (0.3, np.pi / 4, np.pi / 2, np.pi):
    U = np.diag(np.exp(-1j * phi * np.diag(Nop).real))
    tr = lambda X: U @ X @ dag(U)                                   # noqa: E731
    ok = all(np.allclose(tr(x), x * np.exp(1j * phi)) for x in c)
    hop = dag(up[0]) @ up[1]
    dens = dag(up[0]) @ up[0] @ dag(dn[1]) @ dn[1]
    pr = dag(up[0]) @ dag(dn[0])
    ok = ok and np.allclose(tr(hop), hop) and np.allclose(tr(dens), dens) and np.allclose(tr(pr), np.exp(-2j * phi) * pr)
    check(f'(5.5) and the new quiz: c -> c e^(i phi), hopping and density-density keep, pairing gets e^(-2i phi), phi={phi:.4f}',
          ok, np.round(np.exp(-2j * phi), 4))
U4 = lambda X: np.diag(np.exp(-1j * np.pi / 4 * Nd)) @ X @ np.diag(np.exp(1j * np.pi / 4 * Nd))   # noqa: E731
check('new quiz: at phi=pi/4 the pairing gets -i', np.allclose(U4(dag(up[0]) @ dag(dn[0])), -1j * dag(up[0]) @ dag(dn[0])), -1j)
# the interacting chain (5.2) keeps N, so it does not change under the transformation
Hint = Hhop + sum(-1.5 * dag(up[n]) @ dag(dn[n]) @ dn[n] @ up[n] for n in range(L))
check('key 5.7: the interacting Hamiltonian (5.2) commutes with N, so it is gauge invariant', np.abs(Hint @ Nop - Nop @ Hint).max() < 1e-12, 0)
check('quiz on phi: e^(-i pi) = -1, e^(-2 pi i) = 1, e^(-i pi/2) = -i', np.isclose(np.exp(-1j * np.pi), -1)
      and np.isclose(np.exp(-2j * np.pi), 1) and np.isclose(np.exp(-1j * np.pi / 2), -1j), 'ok')

# ---- the quiz on phi, option pi/4: the two readings of the phase, on one site with mu=0 and Delta=0.5
phi = np.pi / 4
U1 = np.diag(np.exp(-1j * phi * np.diag(n1).real))                 # U c U^dag = c e^{i phi} on the site
check('quiz pi/4: U c U^dag = c e^(i phi) on one site', np.allclose(U1 @ cu @ dag(U1), cu * np.exp(1j * phi))
      and np.allclose(U1 @ cd @ dag(U1), cd * np.exp(1j * phi)), 'ok')
check('quiz pi/4: the coefficient of c+_up c+_dn becomes -i Delta, U H(Delta) U^dag = H(-i Delta)',
      np.allclose(U1 @ site(0.0, 0.5) @ dag(U1), site(0.0, -0.5j)), -0.5j)
e1, v1 = np.linalg.eigh(site(0.0, 0.5))
G1 = v1[:, 0]
amp = G1.conj() @ cd @ cu @ G1
amp_kept = G1.conj() @ (cd * np.exp(1j * phi)) @ (cu * np.exp(1j * phi)) @ G1    # c -> c e^{i phi} put into <c_dn c_up>, state kept
UG = U1 @ G1
amp_moved = UG.conj() @ cd @ cu @ UG                                               # the amplitude of the transformed state
check('quiz pi/4: <c_dn c_up> = -0.5 in the ground state, and with c -> c e^(i phi) put in and the state kept it gets e^(i pi/2) = i',
      np.isclose(amp, -0.5) and np.isclose(amp_kept, 1j * amp) and np.isclose(np.exp(2j * phi), 1j), np.round(amp_kept, 4))
check('quiz pi/4: the transformed state U|G> is the ground state of H(-i Delta) and has the amplitude -i <c_dn c_up>, as the coefficient',
      np.isclose(abs(np.linalg.eigh(site(0.0, -0.5j))[1][:, 0].conj() @ UG), 1) and np.isclose(amp_moved, -1j * amp),
      np.round(amp_moved, 4))

# ---- the lab box: the 2e of the tracked source, and "2e instead of e" of our reading in the simplest charging model
src = open(os.path.join(REPO, 'webnotes', 'sources', 'session05', 'tuominen1992_physrevlett.69.1997.txt')).read()
title = [ln for ln in src.splitlines() if ln.startswith('title:')][0]
check('lab: the tracked source of the box names a 2e periodicity of the superconducting transistor, and 300 mK',
      '2e' in title and 'periodicity' in title and 'superconducting single-electron' in title and '300 mK' in src, title[7:])
# island with the charging energy E_C (n - n_g)^2 and an extra energy D_odd for an odd n, the ground-state energy against n_g
ng = np.linspace(0, 4, 4001)
ns = np.arange(-4, 9)


def ground(D_odd, EC=1.0):
    return np.min(EC * (ns[None, :] - ng[:, None])**2 + D_odd * (ns[None, :] % 2), axis=1)


def period(f, step=1000):
    """The smallest shift of n_g, 1 or 2 (in units of 1000 grid steps), under which f repeats."""
    for p in (1, 2):
        if np.allclose(f[:-p * step], f[p * step:], atol=1e-12):
            return p
    return None


check('lab, our reading: no odd energy gives the period e in the gate charge, an odd energy 0.5 E_C gives 2e',
      period(ground(0.0)) == 1 and period(ground(0.5)) == 2, (period(ground(0.0)), period(ground(0.5))))
nbest = ns[np.argmin(1.0 * (ns[None, :] - ng[:, None])**2 + 1.5 * (ns[None, :] % 2), axis=1)]
check('lab, our reading: an odd energy above E_C leaves only even numbers of electrons on the island', np.all(nbest % 2 == 0),
      sorted(set(nbest.tolist())))
print('all checks of page 06 hold')
