"""Session 1, the numbers and the signs that page 11b (Section 1.11b, classifying states of matter by the symmetry that
they break) quotes and that no figure script asserts. One check script per page is the rule: every number of a
caption, a feedback, a fold, a solution or a lab box is an assert, here or in the figure script that draws it. The
figure scripts of the page assert their own numbers: gapless_gapped.py (the gaps 0.45 and 1.2 of the caption, the
zero of the phonon and of the magnon at k = 0) and _g3_disp.py (the value at k = 0 of the three pictures of the quiz,
the linear and the quadratic rise).

This script checks the solution of the problem, time reversal T = i sigma_y K on two spins, the singlet and the Neel
state, with the Hubbard dimer that the solution compares them with, solved in the Fock space on a grid of U and in mean
field, where the threshold U = 2t is the slope U/2t of one pass of the loop at m = 0. It checks the alt texts of the
picture quiz and the sentence of the caption of gapless_gapped.svg on the continuum form of the Higgs curve. It also
checks that the two sentences of the lab box are in the stored abstract, and that the zero applied field of the box is
our reading and not in the abstract. It finds the repository from its own path and
writes no file."""
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# time reversal of one spin, T = i sigma_y K, in the basis up = (1, 0), down = (0, 1) with sigma_z up = up
sy = np.array([[0, -1j], [1j, 0]])
isy = 1j * sy
check('i sigma_y is the real matrix [[0, 1], [-1, 0]]', np.allclose(isy, [[0, 1], [-1, 0]]), isy.real)
up, dn = np.array([1., 0.]), np.array([0., 1.])


def T1(psi):
    return isy @ np.conj(psi)


check('T up = -down', np.allclose(T1(up), -dn), T1(up).real)
check('T down = up', np.allclose(T1(dn), up), T1(dn).real)
for v in (np.array([1, 1j]) / np.sqrt(2), np.array([0.6, -0.8j])):   # T sends the spin sigma to -sigma
    for s in (np.array([[0, 1], [1, 0]]), sy, np.diag([1, -1])):
        a, b = np.conj(v) @ s @ v, np.conj(T1(v)) @ s @ T1(v)
        check('T reverses the expectation value of a Pauli matrix', np.isclose(b, -a), (a.real, b.real))


# two spins, T acts on each spin and K on all the coefficients
def T2(psi):
    return np.kron(isy, isy) @ np.conj(psi)


ud, du = np.kron(up, dn), np.kron(dn, up)
singlet = (ud - du) / np.sqrt(2)
check('T |up down> = -|down up>', np.allclose(T2(ud), -du), T2(ud).real)
check('T |down up> = -|up down>', np.allclose(T2(du), -ud), T2(du).real)
check('the singlet passes the test, T S = S', np.allclose(T2(singlet), singlet), T2(singlet).real)
check('the Neel state goes to a state orthogonal to it', np.isclose(np.vdot(ud, T2(ud)), 0), np.vdot(ud, T2(ud)))
check('T^2 = +1 on two spins', np.allclose(np.kron(isy, isy) @ np.conj(np.kron(isy, isy)), np.eye(4)), 1)
mz0 = np.kron(np.diag([1., -1.]), np.eye(2))                     # m = n_up - n_down on the first spin
check('the singlet has m = 0 on the first site', np.isclose(singlet @ mz0 @ singlet, 0), singlet @ mz0 @ singlet)
check('the Neel state has m = 1 on the first site, and T of it has m = -1',
      np.isclose(ud @ mz0 @ ud, 1) and np.isclose(T2(ud).conj() @ mz0 @ T2(ud), -1), (ud @ mz0 @ ud, (T2(ud).conj() @ mz0 @ T2(ud)).real))


# the Hubbard dimer in the Fock space of four modes, 0 up, 0 down, 1 up, 1 down, with Jordan-Wigner matrices
def annihilators(n):
    a = np.array([[0., 1.], [0., 0.]])
    z = np.diag([1., -1.])
    out = []
    for j in range(n):
        m = np.eye(1)
        for i in range(n):
            m = np.kron(m, z if i < j else (a if i == j else np.eye(2)))
        out.append(m)
    return out


c = annihilators(4)
n = [x.T @ x for x in c]
N = sum(n)
vac = np.zeros(16); vac[0] = 1.0
singlet_fock = (c[0].T @ c[3].T - c[1].T @ c[2].T) @ vac / np.sqrt(2)       # (c+_0up c+_1dn - c+_0dn c+_1up)|0>/sqrt2
Sp = c[0].T @ c[1] + c[2].T @ c[3]
Sz = 0.5 * (n[0] - n[1] + n[2] - n[3])
S2 = Sp.T @ Sp + Sz @ Sz + Sz                                     # S^2 = S- S+ + Sz^2 + Sz


def dimer(U, t=1.0):
    H = -t * sum(c[i].T @ c[i + 2] + c[i + 2].T @ c[i] for i in (0, 1)) + U * (n[0] @ n[1] + n[2] @ n[3])
    sec = np.where(np.isclose(np.diag(N), 2))[0]                  # two electrons
    E, V = np.linalg.eigh(H[np.ix_(sec, sec)])
    gs = np.zeros(16); gs[sec] = V[:, 0]
    return E[0], gs


for U in (0.5, 4.0, 40.0):
    E0, gs = dimer(U)
    check('exact dimer, E_0 = U/2 - sqrt(U^2/4 + 4t^2), U = %g t' % U, np.isclose(E0, U / 2 - np.sqrt(U ** 2 / 4 + 4)), E0)
    check('exact dimer, the ground state is a singlet, S^2 = 0, U = %g t' % U, np.isclose(gs @ S2 @ gs, 0), gs @ S2 @ gs)
    check('exact dimer, m = 0 on each site, U = %g t' % U, np.isclose(gs @ (n[0] - n[1]) @ gs, 0) and np.isclose(gs @ (n[2] - n[3]) @ gs, 0), 0)
ov = abs(singlet_fock @ dimer(40.0)[1]) ** 2
check('exact dimer at U = 40t, one electron per site with the spins in the singlet, weight above 0.99', ov > 0.99, ov)

# time reversal in the Fock space, with the signs of i sigma_y: T c+_up T^-1 = -c+_down, T c+_down T^-1 = c+_up,
# T|0> = |0>, and the complex conjugate of the coefficients of the states c+_a c+_b ... |0> in the order of the modes
TMAP = {0: (1, -1.0), 1: (0, 1.0), 2: (3, -1.0), 3: (2, 1.0)}


def T_fock(psi):
    out = np.zeros(16, complex)
    for idx in np.nonzero(np.abs(psi) > 1e-14)[0]:
        modes = [j for j in range(4) if (idx >> (3 - j)) & 1]       # mode 0 is the leftmost factor of the kron
        v = vac.astype(complex)
        for j in reversed(modes):
            k, s = TMAP[j]
            v = s * (c[k].T @ v)
        out += np.conj(psi[idx]) * v
    return out


one = c[0].T @ vac
check('Fock space, T c+_up|0> = -c+_down|0>, the same as T up = -down', np.allclose(T_fock(one), -(c[1].T @ vac)), 1)
check('Fock space, the singlet of two sites passes the test', np.allclose(T_fock(singlet_fock), singlet_fock), 1)
neel = c[0].T @ c[3].T @ vac
check('Fock space, T of the Neel state is orthogonal to it', np.isclose(np.vdot(neel, T_fock(neel)), 0), np.vdot(neel, T_fock(neel)))
for U in (0.5, 4.0, 40.0):
    gs = dimer(U)[1]
    check('exact dimer, T|GS> = |GS>, it does not break time reversal, U = %g t' % U, np.allclose(T_fock(gs), gs), np.vdot(gs, T_fock(gs)).real)
ok, nU = True, 0
for U in np.concatenate([np.linspace(-20.0, 100.0, 121), [1e3]]):     # "for every U", on a grid of U
    E0, gs = dimer(U)
    ok = ok and np.isclose(E0, U / 2 - np.sqrt(U ** 2 / 4 + 4)) and np.isclose(gs @ S2 @ gs, 0)
    ok = ok and np.isclose(gs @ (n[0] - n[1]) @ gs, 0) and np.isclose(gs @ (n[2] - n[3]) @ gs, 0)
    ok = ok and np.allclose(T_fock(gs), gs)
    nU += 1
check('exact dimer on %d values of U from -20t to 1000t, a singlet with m = 0 that T leaves the same' % nU, ok, nU)
check('the singlet of two spins has m = 0 on both sites', np.isclose(singlet @ np.kron(np.eye(2), np.diag([1., -1.])) @ singlet, 0)
      and np.isclose(singlet @ mz0 @ singlet, 0), 0)


def mean_field(U, seed, t=1.0, steps=4000):
    """Antiferromagnetic mean field of the dimer, the moment m on site 0 and -m on site 1, one electron per spin."""
    m = seed
    for _ in range(steps):
        new = 0.0
        for s in (+1, -1):                                       # spin s feels U <n_{-s}> = U (1 - s m_i)/2 on site i
            h = np.array([[U * (1 - s * m) / 2, -t], [-t, U * (1 + s * m) / 2]])
            v = np.linalg.eigh(h)[1][:, 0]
            new += s * v[0] ** 2                                  # n_{0 up} - n_{0 down}
        m = 0.5 * m + 0.5 * new
    return m


check('mean-field dimer, no moment below U = 2t, U = 1.5t', abs(mean_field(1.5, 0.3)) < 1e-6, mean_field(1.5, 0.3))
m4 = mean_field(4.0, 0.3)
check('mean-field dimer, a moment above U = 2t, m = sqrt(1 - (2t/U)^2) = 0.866 at U = 4t', np.isclose(m4, np.sqrt(1 - 0.25), atol=1e-6), m4)


def one_pass(m, U, t=1.0):
    """One pass of the antiferromagnetic loop of the dimer, with no mixing, the new m on site 0 from the old m."""
    new = 0.0
    for s in (+1, -1):
        h = np.array([[U * (1 - s * m) / 2, -t], [-t, U * (1 + s * m) / 2]])
        new += s * np.linalg.eigh(h)[1][:, 0][0] ** 2
    return new


# the threshold U = 2t on a grid of U, not only at two points: the map has the slope U/2t at m = 0, it has no fixed
# point m > 0 below 2t, and above 2t its fixed point is sqrt(1 - (2t/U)^2)
ms = np.linspace(0.01, 1.0, 100)
ok, worst = True, 0.0
for U in np.linspace(0.2, 20.0, 100):
    q = 1e-6
    slope = one_pass(q, U) / q
    ok = ok and np.isclose(slope, U / 2, rtol=1e-6)
    F = np.array([one_pass(m, U) for m in ms])
    ok = ok and np.allclose(F, U * ms / np.sqrt(U ** 2 * ms ** 2 + 4))     # the closed form m' = Um/sqrt(U^2m^2 + 4t^2)
    if U < 2:
        ok = ok and np.all(F < ms)                                    # below 2t only m = 0 is a fixed point
    elif U > 2:
        mstar = np.sqrt(1 - 4 / U ** 2)
        worst = max(worst, abs(one_pass(mstar, U) - mstar))
        ok = ok and np.isclose(one_pass(mstar, U), mstar) and np.all(F[ms < mstar - 1e-9] > ms[ms < mstar - 1e-9])
check('mean-field dimer on 100 values of U from 0.2t to 20t, slope U/2t at m = 0, a moment only for U > 2t', ok, worst)

# the alt texts of the picture quiz: 1 - cos k and 1 - cos k + 0.45 rise as k^2/2 near zero and flatten at 2 and at
# 2.45 at the edges of the zone, and 2|sin(k/2)| rises to 2. The caption of gapless_gapped.svg: the phonon and the
# magnon are forms of a chain, periodic and flat at k = pi, while the Higgs curve sqrt(1.2^2 + k^2) is the continuum
# form, with a slope at k = pi.
mag = lambda k: 1 - np.cos(k)                                       # noqa: E731
gap = lambda k: 1 - np.cos(k) + 0.45                                # noqa: E731
pho = lambda k: 2 * np.abs(np.sin(k / 2))                           # noqa: E731
hig = lambda k: np.sqrt(1.2 ** 2 + k ** 2)                          # noqa: E731
d = lambda f, k, e=1e-6: (f(k + e) - f(k - e)) / (2 * e)            # noqa: E731
q = 1e-3
check('alt, 1 - cos k starts at 0 and rises as k^2/2 near zero', mag(0.0) == 0 and np.isclose(mag(q) / q ** 2, 0.5, rtol=1e-6), mag(q) / q ** 2)
check('alt, 1 - cos k + 0.45 starts at 0.45 and rises as k^2/2 near zero', np.isclose(gap(0.0), 0.45) and np.isclose((gap(q) - 0.45) / q ** 2, 0.5, rtol=1e-6), gap(0.0))
for f, top, name in ((mag, 2.0, '1 - cos k'), (gap, 2.45, '1 - cos k + 0.45')):
    check('alt, %s flattens at %g at the edges of the zone, slope 0 at k = +-pi' % (name, top),
          np.isclose(f(np.pi), top) and np.isclose(f(-np.pi), top) and abs(d(f, np.pi)) < 1e-6 and abs(d(f, -np.pi)) < 1e-6, f(np.pi))
check('alt, 2|sin(k/2)| starts at 0 and rises to 2 at the edges of the zone', pho(0.0) == 0 and np.isclose(pho(np.pi), 2) and np.isclose(pho(-np.pi), 2), pho(np.pi))
check('caption, the phonon and the magnon are periodic, f(k + 2 pi) = f(k)',
      all(np.allclose(f(np.linspace(-np.pi, np.pi, 50) + 2 * np.pi), f(np.linspace(-np.pi, np.pi, 50))) for f in (mag, gap, pho)), 1)
check('caption, the Higgs curve is the continuum form, slope pi/sqrt(1.44 + pi^2) = 0.93 at k = pi and not 0',
      np.isclose(d(hig, np.pi), np.pi / np.sqrt(1.44 + np.pi ** 2)) and d(hig, np.pi) > 0.9 and np.isclose(hig(0.0), 1.2), d(hig, np.pi))

# the lab box: the two sentences of the stored abstract, kept apart in the box
src = open(os.path.join(ROOT, 'webnotes', 'sources', 'session06', 'huang2017_nature22391.txt')).read()
s1 = 'we use magneto-optical Kerr effect (MOKE) microscopy to demonstrate that monolayer chromium triiodide (CrI3) is an Ising ferromagnet with out-of-plane spin orientation.'
s2 = 'Its Curie temperature of 45 K is only slightly lower than the 61 K of the bulk crystal'
check('lab, the stored abstract says that MOKE shows an Ising ferromagnet with out-of-plane spins', s1 in src, s1[:60])
check('lab, the stored abstract gives 45 K for the monolayer and 61 K for the bulk', s2 in src, s2)
low = src.lower()
check('lab, the zero applied field is our reading, the stored abstract says nothing on zero field or remanence',
      'zero' not in low and 'remanen' not in low and 'applied field' not in low, 'zero, remanen, applied field')

# the sentence on the Hall conductivity and the Kerr effect, old text corrected on 2026-11-22: in an applied field a
# metal with no magnetism has a Hall signal, odd in the field, so only a signal at zero applied field tells that the
# material breaks time reversal. Route 1 is the Drude tensor, route 2 the steady drift of the equation of motion
# dv/dt = -(E + v x B) - v, with e = m = tau = 1, so that omega_c tau = B
def drude_xy(b):
    return (np.array([[1, -b], [b, 1]]) / (1 + b ** 2))[0, 1]


def drift_xy(b, steps=40000, dt=1e-3):
    v = np.zeros(2)
    for _ in range(steps):
        v = v + dt * (-(np.array([1., 0.]) + np.array([v[1] * b, -v[0] * b])) - v)
    return v[1]


check('Hall, route 1, the Drude sigma_xy is 0 at zero field, nonzero and odd in a field, -0.099 sigma_0 at omega_c tau = 0.1',
      drude_xy(0.) == 0 and abs(drude_xy(0.1) + 0.099) < 1e-3 and np.isclose(drude_xy(-0.1), -drude_xy(0.1)), drude_xy(0.1))
check('Hall, route 2, the drift has no transverse part at zero field and the Drude one in a field',
      abs(drift_xy(0.)) < 1e-12 and abs(drift_xy(0.1) - drude_xy(0.1)) < 1e-4, (drift_xy(0.), drift_xy(0.1)))

# the table and the sentence after it, old text corrected on 2026-11-22: only the acoustic phonon is gapless in every
# material, since a crystal with two atoms per cell has an optical branch with a gap at k = 0. Route 1 diagonalizes the
# dynamical matrix of a chain with the masses 1 and 2 and the spring 1, route 2 is its closed form sqrt(2K(1/m1 + 1/m2))
def phonon_branches(k, m1=1., m2=2., K=1.):
    off = -K * (1 + np.exp(-1j * k)) / np.sqrt(m1 * m2)
    D = np.array([[2 * K / m1, off], [np.conj(off), 2 * K / m2]])
    return np.sqrt(np.abs(np.linalg.eigvalsh(D)))


w0 = phonon_branches(0.)
check('at k = 0 the acoustic branch is 0 and the optical branch is sqrt(3) = 1.732 for the masses 1 and 2',
      w0[0] < 1e-6 and abs(w0[1] - np.sqrt(2 * (1 + 0.5))) < 1e-12, w0)

# the caption of gapless_gapped.svg, 2026-11-22: its phonon 2|sin(k/2)| is the acoustic branch of a chain with one mass
# per cell, which has no other branch. Route 1, the dynamical matrix of one mass per cell is the number 2K(1 - cos k)/m.
# Route 2, the cell of two equal masses gives 2|sin(k/4)| and 2|cos(k/4)|, the one branch 2|sin(q/2)| folded, q = k/2
ks = np.linspace(-np.pi, np.pi, 201)
one = np.sqrt(2 * (1 - np.cos(ks)))
two = np.array([phonon_branches(k, 1., 1.) for k in ks])
check('caption, one mass per cell has the single branch 2|sin(k/2)|, 0 at k = 0',
      np.allclose(one, pho(ks)) and one[100] == 0, one[100])
check('caption, two equal masses per cell give only the folded branch, 2|sin(k/4)| and 2|cos(k/4)|, so no optical branch',
      np.allclose(two[:, 0], pho(ks / 2)) and np.allclose(two[:, 1], pho(ks / 2 + np.pi)), two[100])

# the definition "a transverse current generated by a longitudinal voltage", decided on 2026-11-22: at zero field
# a square lattice with the hopping t' = 0.4t on one diagonal keeps time reversal and has sigma_xy = sigma_yx = 0.095
# against sigma_xx = 0.466, Boltzmann with tau = 1 at mu = -0.5t and T = 0.2t on a midpoint mesh of 400^2 cells. The
# sum over v_a v_b is symmetric, so the antisymmetric part, the Hall conductivity, is 0. Route 2, along the diagonals,
# the principal axes, the tensor is diagonal
Lm = 400
km = (np.arange(Lm) + 0.5) * 2 * np.pi / Lm - np.pi
KX, KY = np.meshgrid(km, km, indexing='ij')
tq, muq, Tq = 0.4, -0.5, 0.2
Eq = -2 * (np.cos(KX) + np.cos(KY)) - 2 * tq * np.cos(KX + KY)
vq = (2 * np.sin(KX) + 2 * tq * np.sin(KX + KY), 2 * np.sin(KY) + 2 * tq * np.sin(KX + KY))
wq = 1 / (4 * Tq * np.cosh((Eq - muq) / (2 * Tq)) ** 2)
S = np.array([[np.mean(a * b * wq) for b in vq] for a in vq])
R = np.array([[1, 1], [-1, 1]]) / np.sqrt(2)
Sd = R @ S @ R.T
check('Hall definition, route 1, zero field and one diagonal hopping, sigma_xy = sigma_yx = 0.095 against sigma_xx = 0.466',
      abs(S[0, 1] - 0.095) < 1e-3 and abs(S[0, 0] - 0.466) < 1e-3 and abs(S[0, 1] - S[1, 0]) < 1e-14, S)
check('Hall definition, route 1, along the diagonals the tensor is diagonal, so the transverse part is not a Hall response',
      abs(Sd[0, 1]) < 1e-12 and abs(Sd[1, 0]) < 1e-12, np.diag(Sd))
# the sentence after the key box, added on 2026-11-22: "In (1.4) equal means equal up to a phase, and the test is for an
# even number of electrons, since for an odd number T^2 = -1 and no state passes". T acts as i sigma_y K on each spin.
# On one and on three spins T^2 = -1, and then <psi|T psi> = 0 for every state, checked on random states, so no state
# has T psi = e^(i a) psi, also with no moment: the three spins (up up up + down down down)/sqrt2 have m = 0 on every
# site. On two spins T^2 = +1, the singlet passes with the phase +1, and the triplet (ud + du)/sqrt2, with m = 0 on
# both sites, passes only up to the phase -1.
def Tn(psi, n):
    return reduce_kron([isy] * n) @ np.conj(psi)


def reduce_kron(ms):
    out = np.eye(1)
    for m_ in ms:
        out = np.kron(out, m_)
    return out


rng = np.random.default_rng(7)
for n in (1, 2, 3):
    U_T = reduce_kron([isy] * n)
    T2n = U_T @ np.conj(U_T)
    check(f'after (1.4): T^2 = {(-1) ** n:+d} on {n} spin' + ('s' if n > 1 else ''), np.allclose(T2n, (-1) ** n * np.eye(2 ** n)),
          np.real(T2n[0, 0]))
    if n % 2:
        worst = max(abs(np.vdot(v, Tn(v, n))) for v in (rng.normal(size=2 ** n) + 1j * rng.normal(size=2 ** n)
                                                         for _ in range(200)))
        check(f'after (1.4): on {n} spin' + ('s' if n > 1 else '') + ' every state is orthogonal to T of it, so none passes',
              worst < 1e-12, worst)
ghz = (np.kron(np.kron(up, up), up) + np.kron(np.kron(dn, dn), dn)) / np.sqrt(2)
sz3 = [reduce_kron([np.diag([1., -1.]) if j == i else np.eye(2) for j in range(3)]) for i in range(3)]
sx3 = [reduce_kron([np.array([[0., 1.], [1., 0.]]) if j == i else np.eye(2) for j in range(3)]) for i in range(3)]
sy3 = [reduce_kron([sy if j == i else np.eye(2) for j in range(3)]) for i in range(3)]
mom = max(abs(np.vdot(ghz, o @ ghz)) for o in sz3 + sx3 + sy3)
check('after (1.4): three spins with no moment on any site still fail, <ghz|T ghz> = 0', mom < 1e-12 and
      abs(np.vdot(ghz, Tn(ghz, 3))) < 1e-12, (mom, abs(np.vdot(ghz, Tn(ghz, 3)))))
trip = (ud + du) / np.sqrt(2)
mz1 = np.kron(np.eye(2), np.diag([1., -1.]))
check('after (1.4): the triplet (ud + du)/sqrt2 has m = 0 on both sites and T of it is -1 times it, equal up to a phase',
      np.allclose(T2(trip), -trip) and np.isclose(trip @ mz0 @ trip, 0) and np.isclose(trip @ mz1 @ trip, 0), T2(trip).real)
check('after (1.4): the singlet passes with the phase +1', np.allclose(T2(singlet), singlet), 1)

# the definition of the Hall conductivity, sentence corrected on 2026-11-22: "a transverse current generated by a
# longitudinal voltage, in its antisymmetric part sigma_xy = -sigma_yx". Route 2 to the check above, the drift of
# carriers with an inverse mass tensor M that has its axes at 30 degrees, dv/dt = M (-E - v x B) - v, with e = n = tau = 1.
# At zero field sigma = M is symmetric, with sigma_xy = sigma_yx = 0.217, a transverse current that keeps time
# reversal. In a field the antisymmetric part appears, odd in B, and sigma_xy(B) = sigma_yx(-B), the Onsager relation.
th = np.pi / 6
Rm = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
Mm = Rm @ np.diag([1.0, 0.5]) @ Rm.T


def sigma_drift(B):
    cross = np.array([[0., B], [-B, 0.]])          # v x B with B along z, (v_y B, -v_x B)
    return np.linalg.solve(np.eye(2) + Mm @ cross, Mm)


s0, sp, sm = sigma_drift(0.), sigma_drift(0.1), sigma_drift(-0.1)
anti = lambda s_: (s_[0, 1] - s_[1, 0]) / 2
check('Hall definition: at zero field the anisotropic tensor has sigma_xy = sigma_yx = 0.217 and no antisymmetric part',
      abs(s0[0, 1] - s0[1, 0]) < 1e-15 and abs(s0[0, 1] - 0.2165) < 1e-3, s0[0, 1])
check('Hall definition: in a field the antisymmetric part is nonzero and odd in B',
      abs(anti(sp)) > 1e-3 and np.isclose(anti(sm), -anti(sp)), (anti(sp), anti(sm)))
check('Hall definition: sigma_xy(B) = sigma_yx(-B), the Onsager relation', np.isclose(sp[0, 1], sm[1, 0]), (sp[0, 1], sm[1, 0]))

# the try-it box, rewritten on 2026-11-22 to match the cell "Magnetic order driven by interactions in a chain": its
# arrows are extract("mz") of the mean-field Hamiltonian, normalized, which is the exchange field -U m/2 and points
# against the moment m = get_vev("mz") of the site. Route 1 reads the cell, route 2 runs it with pyqula at its U = 6t.
import contextlib, io, json, tempfile
nb = json.load(open(os.path.join(ROOT, 'jupyter-notebooks', 'session1.ipynb'), encoding='utf-8'))
heads = [''.join(c['source']).strip() for c in nb['cells']]
ic = [j for j, h in enumerate(heads) if h.startswith('## Magnetic order driven by interactions in a chain')][0]
src = ''.join(nb['cells'][ic + 1]['source'])
check('try-it box: the cell has the panel "Antiferromagnetic guess", with mf="antiferro" and U = 6.0, and draws extract("mz")',
      'plt.title("Antiferromagnetic guess")' in src and 'mf="antiferro"' in src and 'U = 6.0' in src
      and src.count('mz = hs.extract("mz")') == 2, 'U = 6.0')
from pyqula import geometry
with tempfile.TemporaryDirectory() as tmp:
    cwd = os.getcwd(); os.chdir(tmp)
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            haf = geometry.bichain().get_hamiltonian().get_mean_field_hamiltonian(U=6.0, mf="antiferro")
            arrows = np.real(np.array(haf.get_supercell(4).extract("mz")))
            mom6 = np.real(np.array(haf.get_vev("mz", nk=200)))
        left = os.listdir(tmp)
    finally:
        os.chdir(cwd)
check('try-it box: the arrows are the exchange field -U m/2, so each one points against the moment of its site',
      np.allclose(arrows[:2], -6.0 * mom6 / 2, atol=2e-3) and np.all(np.sign(arrows[:2]) == -np.sign(mom6)),
      (np.round(arrows[:2], 4), np.round(mom6, 4)))
check('try-it box: the arrows alternate in sign from one site to the next',
      np.all(np.sign(arrows[1:]) == -np.sign(arrows[:-1])), np.sign(arrows))
check('try-it box: pyqula left no file', left == [], left)

print('all checks of page 11b hold')
