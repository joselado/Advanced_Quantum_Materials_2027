"""Session 6, the statements and numbers of page 17 (Section 6.17, the closing summary). One check script per page is the rule.

It checks the formulas that the list of tasks quotes and the numbers of the quiz and of the figure caption: the exchange
splitting Um of the Hartree decoupling, J = 4t^2/U as the limit of the singlet-triplet splitting of the exact Hubbard dimer, the
classical triangle at 120 degrees with -3/2 J S^2, the magnon energy 8|J|S at (pi, pi) of the square lattice, and the two
dispersions of the chain, zero at k = 0, quadratic and linear at small k. Not asserted: the feedback of the third option of the
quiz, "an easy-axis anisotropy A (S^z)^2 opens a gap of order A", which the conventions sheet lists as not true for S = 1/2. It uses
numpy and scipy only and writes no file.

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
print('all checks of page 17 hold')
