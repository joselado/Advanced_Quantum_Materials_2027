"""Session 4, the numbers that page 09 (Section 4.9, the Landau levels of Schrodinger electrons) quotes and that no figure
script asserts. One check script per page is the rule: every number of a caption, a feedback, a fold, a solution or a
lab box is an assert, here or in the figure script that draws it. The figure script g3_landau_fan.py asserts the numbers
of its caption (the levels -3.70 and -3.12 against -3.69 and -3.06 at the flux 0.05, the cells q = 10 to 60). This script
checks the fold from (4.5) to (4.6) by finite differences, the degeneracy of one state per flux quantum by an explicit
count of k_y and on a torus of the square lattice, the feedback of the three quizzes and the solution of the problem. It
needs numpy and scipy, finds the repository from its own path and writes no file."""
import numpy as np
from scipy.linalg import eigh_tridiagonal

h = 6.62607015e-34          # J s
hbar = h / (2 * np.pi)
e = 1.602176634e-19         # C
me = 9.1093837015e-31       # kg


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# the fold: p^2/2m + B^2 (x - x0)^2 / 2m, in units hbar = m = 1, with B = 1.7, has the levels B (n + 1/2) for every x0
B = 1.7
L, N = 24.0, 4000
x = np.linspace(-L / 2, L / 2, N)
dx = x[1] - x[0]
for x0 in (0.0, 2.5, -3.0):
    w = eigh_tridiagonal(1 / dx ** 2 + 0.5 * B ** 2 * (x - x0) ** 2, -0.5 / dx ** 2 * np.ones(N - 1),
                         select='i', select_range=(0, 3))[0]
    check('fold: the levels at x0 = %.1f are hbar omega_c (n + 1/2) with omega_c = B/m' % x0,
          np.allclose(w, B * (np.arange(4) + 0.5), atol=2e-3), np.round(w / B, 4))
# B^2/2m = (1/2) m omega_c^2 with omega_c = B/m, for any m
for m in (0.3, 1.0, 2.2):
    check('fold: B^2/2m = m omega_c^2 / 2 for m = %.1f' % m, abs(B ** 2 / (2 * m) - 0.5 * m * (B / m) ** 2) < 1e-12, m)
# the ground state is the Gaussian exp(-(x - x0)^2 / 2 l_B^2) with l_B^2 = hbar/B: H psi = (hbar omega_c / 2) psi
x0 = 1.3
lB2 = 1 / B
psi = np.exp(-(x - x0) ** 2 / (2 * lB2))
Hpsi = -0.5 * np.gradient(np.gradient(psi, dx), dx) + 0.5 * B ** 2 * (x - x0) ** 2 * psi
inner = np.abs(x - x0) < 4
check('fold: H exp(-(x-x0)^2/2 l_B^2) = (B/2) exp(...)', np.allclose(Hpsi[inner], 0.5 * B * psi[inner], atol=1e-4),
      np.max(np.abs(Hpsi[inner] - 0.5 * B * psi[inner])))

# the flux quantum and the density of states of one level, with the units back
phi0 = h / e
check('the flux quantum h/e = 4.14e-15 T m^2', round(phi0 * 1e15, 2) == 4.14, phi0)
area = 1e-12                # 1 micrometre squared
for Bt, n_exp in ((1, 242), (2, 484)):
    check('quiz: %d T through 1 um^2 is about %d flux quanta' % (Bt, n_exp), round(Bt * area / phi0) == n_exp,
          Bt * area / phi0)
check('quiz: the law A/B gives about 121 at 2 T', round(242 / 2) == 121, 242 / 2)
check('new quiz: eB/h = 241.8 per um^2 at 1 T', round(e * 1 / h * 1e-12, 1) == 241.8, e / h * 1e-12)
check('new quiz: h/eB = 4136 nm^2 at 1 T', round(h / e * 1e18) == 4136, h / e * 1e18)
fc = e * 1 / (2 * np.pi * 0.067 * me)
check('new quiz: eB/2 pi m = 418 GHz for m = 0.067 m_e at 1 T', round(fc / 1e9) == 418, fc / 1e9)

# the problem: count the k_y = 2 pi j / L_y with 0 <= x0 = hbar k_y / eB < L_x, for L_x = L_y = 1 um at 1 T
Lx = Ly = 1e-6
Bt = 1.0
j = np.arange(-10, 1000)
x0s = hbar * 2 * np.pi * j / Ly / (e * Bt)
count = int(np.sum((x0s >= 0) & (x0s < Lx)))
check('problem: the flux BA/(h/e) = 241.8', round(Bt * Lx * Ly / phi0, 1) == 241.8, Bt * Lx * Ly / phi0)
check('problem: the count of the integers j is 242', count == 242, count)

# second route to one state per flux quantum: a 24 x 24 torus of the square lattice with the flux 1/12 per plaquette,
# Landau gauge with the phase 2 pi phi x on the bonds along y, so the torus holds 576/12 = 48 flux quanta
Lt, phi = 24, 1 / 12
n = Lt * Lt
H = np.zeros((n, n), complex)
idx = lambda a, b: (a % Lt) * Lt + (b % Lt)
for a in range(Lt):
    for b in range(Lt):
        H[idx(a + 1, b), idx(a, b)] += -1
        H[idx(a, b + 1), idx(a, b)] += -np.exp(2j * np.pi * phi * a)
H = H + H.conj().T
ev = np.linalg.eigvalsh(H)
gap = np.diff(ev)
first = int(np.argmax(gap[:100] > 0.1)) + 1
check('torus 24 x 24 with the flux 1/12: the lowest level holds 48 states, one per flux quantum',
      first == 48 and np.ptp(ev[:48]) < 1e-4, (first, np.ptp(ev[:48]), round(gap[first - 1], 3)))
