"""Session 6, the statements and numbers of page 17 (Section 6.17, the closing summary). One check script per page is the rule.

It checks the formulas that the list of tasks quotes and the numbers of the quiz and of the figure caption: the exchange
splitting Um of the Hartree decoupling, J = 4t^2/U as the limit of the singlet-triplet splitting of the exact Hubbard dimer, the
classical triangle at 120 degrees with -3/2 J S^2, the magnon energy 8|J|S at (pi, pi) of the square lattice, and the two
dispersions of the chain, zero at k = 0, quadratic and linear at small k. The feedback of the third option of the quiz was
corrected on 2026-11-22, and again after the independent check of that day, to "an easy-axis anisotropy A (S^z)^2 with A<0
... for S >= 1 opens a gap. This gap is |A|(2S-1) in the ferromagnet, and in linear spin waves a larger one, of order
S sqrt(zJ|A|) for |A| << zJ, in the antiferromagnet", which the last two blocks assert, on one site and on an exact ring for
the ferromagnet, and by linear spin waves for the antiferromagnet. It uses numpy and scipy only and writes no file.

Run it from anywhere:  python3 webnotes/checks/session06/g5_17_closing_summary.py"""
import itertools

import numpy as np
from scipy.optimize import minimize


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# the exchange splitting Um: the Hartree field of one spin is U times the density of the other spin
U, nup, ndn = 4.0, 0.2, 0.0
e_up, e_dn = U * ndn, U * nup                         # onsite energies U<n_dn> and U<n_up> of the decoupling
check('the splitting of the two spins is Um, 0.8 for U=4 and m=0.2', abs((e_dn - e_up) - U * (nup - ndn)) < 1e-15
      and abs(e_dn - e_up - 0.8) < 1e-15, e_dn - e_up)

# J = 4t^2/U from the exact Hubbard dimer at half filling, six states with two electrons on two sites
modes = [(0, 1), (0, -1), (1, 1), (1, -1)]           # (site, spin)


def dimer(U, t=1.0):
    states = [s for s in itertools.combinations(range(4), 2)]
    idx = {s: i for i, s in enumerate(states)}
    H = np.zeros((6, 6))
    for s in states:
        i = idx[s]
        occ = [modes[a] for a in s]
        H[i, i] += U * sum(1 for site in (0, 1) if (site, 1) in occ and (site, -1) in occ)
        for a in s:                                   # hop -t c^dag_b c_a between the sites, same spin
            site, spin = modes[a]
            b = modes.index((1 - site, spin))
            if b in s:
                continue
            new = tuple(sorted([x for x in s if x != a] + [b]))
            rest = [x for x in s if x != a]
            sign = (-1) ** sum(1 for x in rest if x < a) * (-1) ** sum(1 for x in rest if x < b)
            H[idx[new], i] += -t * sign
    return np.linalg.eigvalsh(H)


ratios = []
for Uv in (8.0, 16.0, 64.0):
    e = dimer(Uv)
    ratios.append((e[1] - e[0]) / (4 / Uv))           # triplet at 0 minus the singlet, against 4t^2/U
check('the singlet-triplet splitting of the dimer tends to 4t^2/U', abs(ratios[1] - 0.9848) < 5e-5 and abs(ratios[2] - 1) < 1e-3,
      np.round(ratios, 4))

# three classical spins on a triangle with J > 0: 120 degrees and -3/2 J S^2
J, S = 1.0, 1.0


def energy(x):
    th, ph = x[:3], x[3:]
    s = np.array([[np.sin(a) * np.cos(b), np.sin(a) * np.sin(b), np.cos(a)] for a, b in zip(th, ph)]) * S
    return J * (s[0] @ s[1] + s[1] @ s[2] + s[2] @ s[0])


best = min((minimize(energy, np.random.default_rng(seed).uniform(0, np.pi, 6)) for seed in range(8)), key=lambda r: r.fun)
th, ph = best.x[:3], best.x[3:]
s = np.array([[np.sin(a) * np.cos(b), np.sin(a) * np.sin(b), np.cos(a)] for a, b in zip(th, ph)])
ang = np.degrees(np.arccos(np.clip(s[0] @ s[1], -1, 1)))
check('the classical triangle has its minimum at 120 degrees, -3/2 J S^2', abs(best.fun + 1.5) < 1e-8 and abs(ang - 120) < 1e-3,
      'E = %.6f, angle %.4f' % (best.fun, ang))

# the quiz: 8|J|S at (pi, pi) for z = 4, and both magnons at zero at k = 0, quadratic and linear at small k
gamma = lambda kx, ky: (np.cos(kx) + np.cos(ky)) / 2
check('the ferromagnetic magnon of the square lattice is 8|J|S at (pi, pi)', abs(4 * (1 - gamma(np.pi, np.pi)) - 8) < 1e-12,
      4 * (1 - gamma(np.pi, np.pi)))
k = 1e-3
fm, afm = 1 - np.cos(k), np.sqrt(1 - np.cos(k) ** 2)
check('the chain: both are zero at k=0, the ferromagnet is k^2/2 and the antiferromagnet |k| at small k',
      1 - np.cos(0) == 0 and abs(fm / (k * k / 2) - 1) < 1e-6 and abs(afm / k - 1) < 1e-6, '%.3e %.3e' % (fm, afm))

# corrected on 2026-11-22, the third option of the quiz: A (S^z)^2 with A < 0 is an easy axis, and one magnon costs
# |A|(2S - 1), 0 for S = 1/2, |A| for S = 1 and 2|A| for S = 3/2. Two routes: one site, where the cost is
# A(S-1)^2 - A S^2, and the exact ferromagnetic ring of 4 spins with J = -1, where the lowest one-magnon level above the
# polarized state is the k = 0 magnon at |A|(2S - 1), since a uniform turn costs no exchange energy.


def spin_ops(S):
    m = np.arange(S, -S - 1, -1)
    sp = np.diag(np.sqrt(S * (S + 1) - m[1:] * (m[1:] + 1)), 1)
    return np.diag(m), sp


A = -1.0
site_cost, ring_cost = [], []
for S in (0.5, 1.0, 1.5):
    sz, sp = spin_ops(S)
    e = np.diag(A * sz @ sz)
    site_cost.append(e[1] - e[0])
    d = sz.shape[0]
    op = lambda o, i: np.kron(np.kron(np.eye(d ** i), o), np.eye(d ** (3 - i)))
    Hr = sum(-1.0 * (op(sz, i) @ op(sz, (i + 1) % 4) + 0.5 * (op(sp, i) @ op(sp.T, (i + 1) % 4) + op(sp.T, i) @ op(sp, (i + 1) % 4)))
             for i in range(4)) + sum(A * op(sz @ sz, i) for i in range(4))
    Sz = sum(op(sz, i) for i in range(4))
    w, v = np.linalg.eigh(Hr)
    szv = np.real(np.einsum('ij,jk,ki->i', v.T, Sz, v))
    e_top = w[np.isclose(szv, 4 * S)].min()
    e_one = w[np.isclose(szv, 4 * S - 1)].min()
    ring_cost.append(e_one - e_top)
check('quiz, third option: A (S^z)^2 with A<0 costs |A|(2S - 1) for one magnon, 0, 1 and 2 for S = 1/2, 1 and 3/2, on one site '
      'and on the exact ring of 4 spins', np.allclose(site_cost, [0, 1, 2]) and np.allclose(ring_cost, [0, 1, 2]),
      (np.round(site_cost, 12).tolist(), np.round(ring_cost, 10).tolist()))
# corrected after the independent check of 2026-11-22 (k5): the stem names both dispersions. In linear spin waves the
# antiferromagnet (6.9) with the easy axis has, at k = 0, the Bogoliubov block [[zJS + a, zJS], [zJS, zJS + a]] with a the
# onsite cost of one magnon, so its gap is sqrt((zJS + a)^2 - (zJS)^2), which is larger than a. Two routes: the closed form
# and the eigenvalues of eta M. For |A| small against zJ it is close to 2S sqrt(zJ|A|) with a = 2|A|S, the linear spin-wave
# cost, and close to sqrt(2(2S - 1)S) sqrt(zJ|A|) with a = |A|(2S - 1), so of order S sqrt(zJ|A|) for both. No number of a
# chain goes on the page, since linear spin waves are not reliable on a chain of spins 1.
rows = []
for z in (2, 4, 6):
    for S in (1.0, 1.5, 2.0):
        for Aa in (0.001, 0.01, 0.05):
            for a in (2 * Aa * S, Aa * (2 * S - 1)):
                Mb = np.array([[z * S + a, z * S], [z * S, z * S + a]])
                wb = np.max(np.real(np.linalg.eigvals(np.diag([1, -1]) @ Mb)))
                closed = np.sqrt((z * S + a) ** 2 - (z * S) ** 2)
                rows.append((abs(wb - closed), wb / a, wb / (S * np.sqrt(z * Aa))))
check('quiz, third option: in linear spin waves the antiferromagnetic gap sqrt((zJS + a)^2 - (zJS)^2) is larger than the cost a '
      'of one magnon, |A|(2S - 1) or 2|A|S, and of order S sqrt(zJ|A|) for |A| << zJ, between 1 and 2.1 times it',
      all(d < 1e-9 and r > 1 and 1 < q < 2.1 for d, r, q in rows),
      (round(min(r for d, r, q in rows), 2), round(min(q for d, r, q in rows), 3), round(max(q for d, r, q in rows), 3)))
print('all checks of page 17 hold')
