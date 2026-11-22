"""Session 9, the numbers and the statements of the quiz of page 11 (Section 9.11, the closing summary).

One check script per page is the rule: every number of a feedback is an assert. The quiz asks what a 1/|x| envelope of
the density around a vacancy in a clean chain says about the ground state. This script checks the two numbers of the
feedback, e^{-10/2.5} = 0.02 against 1/10 = 0.1, which are also the numbers of the quizzes of Sections 9.6b and 9.9,
and the physics of the quiz on two chains with one end, which is what a vacancy leaves. A spinless chain at mu = -t,
a metal, has a density that oscillates with the period pi/k_F = 3 sites and an envelope that falls as 1/x. The same
chain with the onsite energies +-0.3t on its two sublattices at half filling, an insulator with the gap 0.6t, has a
density that falls as exp(-x/xi), with xi about 3 sites. The script needs numpy only and writes no file."""
import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# ---- the two numbers of the first feedback
check('feedback: e^{-x/xi} at x = 10 for xi = 2.5 is e^{-4} = 0.02 of its value at x = 0',
      round(np.exp(-10 / 2.5), 2) == 0.02 and np.exp(-10 / 2.5) == np.exp(-4), np.exp(-10 / 2.5))
check('feedback: 1/x at x = 10 is 0.1 of its value at x = 1', 1 / 10 == 0.1, 0.1)

# ---- a metal: a spinless chain with one end, hopping -t, filled up to mu = -t, so k_F = pi/3
N = 1500
H = -(np.eye(N, k=1) + np.eye(N, k=-1))
e, v = np.linalg.eigh(H)
dens = (np.abs(v[:, e < -1.0]) ** 2).sum(axis=1)
kF = np.arccos(0.5)
dn = dens[:N // 2] - kF / np.pi                       # the bulk density is k_F / pi
x = np.arange(1, N // 2 + 1)
check('metal: k_F = pi/3 and the period pi/k_F = 3 sites', abs(np.pi / kF - 3) < 1e-12, np.pi / kF)
# the envelope: the amplitude of the oscillation in each period of 3 sites, (2/3)|sum dn e^{-2 i k_F x}|, which does
# not depend on the phase of the cosine and removes a constant offset of the finite chain, fitted by a power of x
sel = (x >= 30) & (x < 300)
z = (dn * np.exp(-2j * kF * x))[sel].reshape(-1, 3)
peak = 2 / 3 * np.abs(z.sum(axis=1))
xpk = x[sel].reshape(-1, 3).mean(axis=1)
p = -np.polyfit(np.log(xpk), np.log(peak), 1)[0]
check('metal: the envelope of the density falls as 1/x, a power 1.0', round(p, 1) == 1.0, p)
# a power law bends on a logarithmic axis: the logarithm of the envelope is not a straight line in x
a = np.polyfit(xpk, np.log(peak), 1)
check('metal: an exponential does not fit the envelope', np.max(np.abs(np.polyval(a, xpk) - np.log(peak))) > 0.3,
      np.max(np.abs(np.polyval(a, xpk) - np.log(peak))))

# ---- an insulator: the same chain with +-m on the two sublattices at half filling
m = 0.3
H2 = H + np.diag(m * (-1.0) ** np.arange(N))
e2, v2 = np.linalg.eigh(H2)
dens2 = (np.abs(v2[:, :N // 2]) ** 2).sum(axis=1)
bulk = dens2[N // 2 - 2:N // 2]                       # the bulk density of the two sublattices
dn2 = dens2[:200] - np.where(np.arange(200) % 2 == (N // 2 - 2) % 2, bulk[0], bulk[1])
check('insulator: the gap is 2m = 0.6t', abs((e2[N // 2] - e2[N // 2 - 1]) - 2 * m) < 1e-3, e2[N // 2] - e2[N // 2 - 1])
for par in (0, 1):                                      # each sublattice alone, from x = 4 to 39
    x2 = np.arange(par, 40, 2)
    d2 = np.abs(dn2[x2])
    sel2 = x2 >= 4
    a = np.polyfit(x2[sel2], np.log(d2[sel2]), 1)
    res_exp = np.max(np.abs(np.polyval(a, x2[sel2]) - np.log(d2[sel2])))
    b = np.polyfit(np.log(x2[sel2]), np.log(d2[sel2]), 1)
    res_pow = np.max(np.abs(np.polyval(b, np.log(x2[sel2])) - np.log(d2[sel2])))
    check('insulator, sublattice %d: the density falls as exp(-x/xi) with xi about 3 sites, and a power of x does not fit'
          % par, 0.25 < -a[0] < 0.40 and res_exp < 0.25 and res_pow > 1.0, (round(-a[0], 3), round(res_exp, 2), round(res_pow, 2)))
check('insulator: at x = 60 the change of the density is below 1e-6', np.abs(dn2[60:70]).max() < 1e-6, np.abs(dn2[60:70]).max())
