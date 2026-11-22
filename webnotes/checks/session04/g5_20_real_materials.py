"""Session 4, the numbers that page 20 (Sections 4.20 and 4.21, real materials with Chern and fractional Chern physics, and the
closing summary) quotes. One check script per page is the rule: every number of a caption, a feedback, a fold, a solution or a
lab box is an assert, here or in the figure script that draws it. The figure scripts of the page, flat_chern_band.py and the
three g5_quiz_band_*.py, assert through _g5_bands.load the widths, the gaps, the ratio 14.0 and the Chern numbers that the
script g5_haldane_t3_bands.py gives. This script checks the same models by a second route: the pyqula model with
tij=[1, t2 cos(phi), t3] and h.add_haldane(2 t2 sin(phi)/sqrt(3)) has the spectrum of the numpy model _honeycomb.bloch with the
first-neighbor hopping -1, which the conventions sheet uses, and its Chern number from the link variables of physcheck is the
one of h.get_chern(). It also checks that the flat band with C=0 keeps time reversal, the arguments of add_haldane that the
caption names, and the resistance 3h/2e^2 of the lab box, which is our conversion. The numbers 0.1 % and 1 % of the lab box are
read from the stored source with labsource.py. It finds the repository from its own path and writes no file, since pyqula runs
in a temporary folder.

The blocks marked "corrected on 2026-11-22" back the sentences of the old text that were corrected on that day, after
the lecturer chose to fix the errors of the old text. The block marked "decided on 2026-11-22" backs the closing bullet on
the Landau levels, |C_n| = 1 and |sigma_xy| = N e^2/h, which the lecturer picked that day, on a magnetic cell of the square
lattice with the phase (4.4) for both signs of the field. The last block backs the charge e/m written as a magnitude in
the caption of the fractional figure and in the closing bullet, after an independent check."""
import os
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, '..', '..', 'figures')
sys.path.insert(0, FIG)
sys.path.insert(0, os.path.join(FIG, 'session03'))
import physcheck as pc  # noqa: E402
import _honeycomb as hc  # noqa: E402


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


os.chdir(tempfile.mkdtemp())
from pyqula import geometry  # noqa: E402


def pyqula_model(t2, phi, t3, M):
    """The model of g5_haldane_t3_bands.py, with the same calls."""
    g = geometry.honeycomb_lattice()
    h = g.get_hamiltonian(has_spin=False, tij=[1., t2 * np.cos(phi), t3])
    h.add_haldane(2 * t2 * np.sin(phi) / np.sqrt(3))
    h.add_sublattice_imbalance(M)
    return h


def spectrum(hk, B, nk=48):
    """Every energy on the mesh nk x nk of the reduced zone, sorted, the width of the lower band, the gap, and the top of the
    lower band and the bottom of the upper band."""
    E = np.array([np.linalg.eigvalsh(hk(k)) for k in pc.kmesh(B, nk)])
    return np.sort(E.ravel()), np.ptp(E[:, 0]), E[:, 1].min() - E[:, 0].max(), E[:, 0].max(), E[:, 1].min()


models = [(0.1, np.pi / 2, 0., 0.), (0.3, 0.4 * np.pi, -0.2, 0.), (0.2, 0., 0., 1.5)]
Bn = pc.reciprocal([hc.a1, hc.a2])
rows = []
for t2, phi, t3, M in models:
    h = pyqula_model(t2, phi, t3, M)
    hk, B = pc.from_pyqula(h)
    Ep, Wp, Dp, top, bottom = spectrum(hk, B)
    En, Wn, Dn, _, _ = spectrum(lambda k: hc.bloch(np.asarray(k), t2=t2, phi=phi, M=M, t3=t3), Bn)
    Cl = pc.chern_links(hk, B, bands=0, nk=24)
    Cn = pc.chern_links(lambda k: hc.bloch(np.asarray(k), t2=t2, phi=phi, M=M, t3=t3), Bn, bands=0, nk=24)
    Cq = h.get_chern(nk=40)
    rows.append((Wp, Dp, Cl, Cq))
    check('t2=%.1f phi=%.2f pi t3=%.1f M=%.1f, the pyqula spectrum on the 48 x 48 mesh is the numpy spectrum' % (t2, phi / np.pi, t3, M),
          np.allclose(Ep, En, atol=1e-9), 'largest difference %.1e' % np.abs(Ep - En).max())
    check('  the width and the gap, pyqula and numpy', abs(Wp - Wn) < 1e-9 and abs(Dp - Dn) < 1e-9, '%.4f %.4f' % (Wp, Dp))
    check('  C from the links of pyqula, of numpy and from h.get_chern() agree', abs(Cl - Cq) < 1e-6 and abs(Cn - Cq) < 1e-6,
          '%+.6f %+.6f %+.6f' % (Cl, Cn, Cq))
    check('  zero energy is in the gap, so h.get_chern() counts the lower band only', top < 0 < bottom, '%.4f < 0 < %.4f' % (top, bottom))

(W0, D0, C0, _), (W1, D1, C1, _), (W2, D2, C2, _) = rows
check('(a), the Haldane model t2=0.1: C=1, width 2.48 (2.5 t), gap 1.04, more than twice the gap',
      abs(C0 - 1) < 1e-6 and abs(W0 - 2.48) < 0.005 and abs(D0 - 1.04) < 0.005 and W0 > 2 * D0, '%.4f %.4f' % (W0, D0))
check('(b), the flat Chern band: C=1, width 0.21, gap 2.97, width 14 times smaller than the gap',
      abs(C1 - 1) < 1e-6 and abs(W1 - 0.212) < 0.0005 and abs(D1 - 2.965) < 0.0005 and abs(D1 / W1 - 14.0) < 0.05,
      '%.4f %.4f %.2f' % (W1, D1, D1 / W1))
check('(a), the caption writes the width 2.48 as 2.5 t', abs(W0 - 2.5) < 0.05, '%.4f' % W0)
check('the flat trivial band: C=0, width 0.20, gap 3.00',
      abs(C2) < 1e-6 and abs(W2 - 0.2) < 0.0005 and abs(D2 - 3.0) < 0.0005, '%.4f %.4f' % (W2, D2))
check('the flat Chern band and the flat trivial band have about the same width and gap, they differ by C',
      abs(W1 - W2) < 0.02 and abs(D1 - D2) < 0.05, '%.3f %.3f against %.3f %.3f' % (W1, D1, W2, D2))
check('the dispersive band has no window between its width and its gap, the flat bands have one',
      W0 > D0 and D1 > 10 * W1 and D2 > 10 * W2, '%.2f > %.2f, %.2f > 10 x %.3f, %.2f > 10 x %.2f' % (W0, D0, D1, W1, D2, W2))

# the recall box of (4.1): C is the integral of Omega over the zone divided by 2 pi, so the integral itself is 2 pi C
hk, B = pc.from_pyqula(pyqula_model(*models[0]))
area = abs(np.linalg.det(np.asarray(B, float)))
I_om = area * np.mean([pc.berry_curvature(hk, k, bands=0) for k in pc.kmesh(B, 48)])
check('(a), the integral of Omega of the lower band over the zone is 2 pi C = 6.283, not the integer C',
      abs(I_om - 2 * np.pi * C0) < 1e-2 and abs(I_om - round(I_om)) > 0.2, '%.4f against 2 pi C = %.4f' % (I_om, 2 * np.pi * C0))

# the flat trivial band keeps time reversal: every hopping is real, so H(-k) is the complex conjugate of H(k)
hk, B = pc.from_pyqula(pyqula_model(*models[2]))
ks = [np.array([0.13, 0.41]), np.array([-0.7, 0.25]), np.array([1.1, -0.3])]
check('the flat trivial band, H(-k) = H(k)* at three momenta, time reversal', all(np.allclose(hk(-k), np.conj(hk(k))) for k in ks), 'yes')
hk, B = pc.from_pyqula(pyqula_model(*models[1]))
check('the flat Chern band breaks time reversal, H(-k) is not H(k)*', not np.allclose(hk(-ks[0]), np.conj(hk(ks[0]))), 'yes')
hk, B = pc.from_pyqula(pyqula_model(0.2, 0., 0., 0.))
check('with t2 = 0.2 real and no staggered potential the gap is closed, so the potential 1.5 opens it',
      pc.gap(hk, B, 1, nk=48) < 1e-9, pc.gap(hk, B, 1, nk=48))

# a Landau level has |C| = 1, the lowest level of the magnetic cell of the recipe "The Chern number of a Landau level"
q = 20
h = geometry.square_lattice().get_supercell((1, q)).get_hamiltonian(has_spin=False)
h.add_orbital_magnetic_field(1 / q)
lev = np.linalg.eigvalsh(h.get_hk_gen()([0., 0., 0.]))[:2]
h.add_onsite(-0.5 * (lev[0] + lev[1]))
C_LL = h.get_chern(nk=20)
check('the lowest Landau level of the square lattice with the flux 1/20 has |C| = 1', abs(abs(C_LL) - 1) < 1e-3, '%+.4f' % C_LL)

# the parameters of pyqula that the caption names
check('t2 = 0.1 with phi = pi/2 is h.add_haldane(0.1155)', abs(2 * 0.1 / np.sqrt(3) - 0.1155) < 5e-5, 2 * 0.1 / np.sqrt(3))
check('t2 = 0.3 with phi = 0.4 pi is tij=[1, 0.0927, -0.2] and h.add_haldane(0.3295)',
      abs(0.3 * np.cos(0.4 * np.pi) - 0.0927) < 5e-5 and abs(2 * 0.3 * np.sin(0.4 * np.pi) / np.sqrt(3) - 0.3295) < 5e-5,
      (0.3 * np.cos(0.4 * np.pi), 2 * 0.3 * np.sin(0.4 * np.pi) / np.sqrt(3)))
h = geometry.honeycomb_lattice().get_hamiltonian(has_spin=False)
h.add_haldane(0.1)
hk, B = pc.from_pyqula(h)
check('h.add_haldane(0.1) of other pages is t2 = 0.087 with the gap 0.90, not the model of the figure',
      abs(pc.gap(hk, B, 1, nk=60) - 0.9) < 1e-6, pc.gap(hk, B, 1, nk=60))

# the factor 2/sqrt(3) of the caption, on the bare call: h.add_haldane(x) is the numpy model with t2 sin(phi) = x sqrt(3)/2,
# and not the one with t2 sin(phi) = x
for x in (0.05, 0.1, 0.1155, 0.2):
    h = geometry.honeycomb_lattice().get_hamiltonian(has_spin=False)
    h.add_haldane(x)
    hk, B = pc.from_pyqula(h)
    Ep = spectrum(hk, B, nk=24)[0]
    Es = spectrum(lambda k: hc.bloch(np.asarray(k), t2=x * np.sqrt(3) / 2, phi=np.pi / 2), Bn, nk=24)[0]
    E1 = spectrum(lambda k: hc.bloch(np.asarray(k), t2=x, phi=np.pi / 2), Bn, nk=24)[0]
    check('h.add_haldane(%.4f) has the spectrum of t2 sin(phi) = %.4f, so t2 sin(phi) enters times 2/sqrt(3)' % (x, x * np.sqrt(3) / 2),
          np.allclose(Ep, Es, atol=1e-9) and not np.allclose(Ep, E1, atol=1e-3),
          'difference %.1e with the factor, %.1e without' % (np.abs(Ep - Es).max(), np.abs(Ep - E1).max()))

# the lab box: 3h/2e^2 in kilo-ohm, our conversion, and the Hall conductance that it means, our reading
RK = 25812.807
check('3h/2e^2 = 38.7 kOhm, with h/e^2 = 25812.807 Ohm', abs(1.5 * RK / 1000 - 38.7) < 0.05, 1.5 * RK / 1000)
check('R_xy = 3h/2e^2 is the Hall conductance (2/3) e^2/h, two thirds of e^2/h', abs(1 / 1.5 - 2 / 3) < 1e-12, 1 / 1.5)
# "since R_xx is small there, its inverse is close to the Hall conductance": sigma_xy = rho_xy/(rho_xx^2 + rho_xy^2), so
# sigma_xy rho_xy = 1/(1 + r^2) with r = rho_xx/rho_xy, which is 1 only at r = 0 and 0.990 at r = 0.1
r = np.array([0., 0.1])
rho_xy = 1.5
rho = np.array([[[ri * rho_xy, rho_xy], [-rho_xy, ri * rho_xy]] for ri in r])
s_xy = np.array([np.linalg.inv(m)[1, 0] for m in rho])
check('sigma_xy rho_xy from the inverse of the resistivity tensor is 1/(1 + r^2), 1 at r = 0 and 0.990 at r = 0.1',
      np.allclose(s_xy * rho_xy, 1 / (1 + r**2)) and abs(s_xy[0] - 2 / 3) < 1e-12 and abs(s_xy[1] * rho_xy - 0.990) < 0.0005,
      s_xy * rho_xy)

# the closing summary, corrected on 2026-11-22: the Haldane model "is adiabatically connected to the quantum Hall state
# driven by the field with the same Chern number". In the rotated honeycomb cell of 80 sites with one flux quantum, the
# field with the zero of energy above the zero level has C = +1, add_haldane(+0.07) has +1 and add_haldane(-0.07) has -1,
# so only the first Haldane model has the Chern number of this quantum Hall state. The path between them is the check of
# page 19, where the gap stays open for +0.07 and closes for -0.07.
gm = geometry.honeycomb_lattice_square_cell().rotate(90).get_supercell((20, 1))
hm = gm.get_hamiltonian(has_spin=False)
hm.add_orbital_magnetic_field(1 / (3 * np.sqrt(3) * 20))
hm.add_onsite(-0.25)
c_qh = hm.get_chern(nk=8)
c_h = {}
for xh in (0.07, -0.07):
    hh = gm.get_hamiltonian(has_spin=False)
    hh.add_haldane(xh)
    c_h[xh] = hh.get_chern(nk=8)
check('closing summary: the quantum Hall state above the zero level has C = +1, add_haldane(+0.07) +1 and add_haldane(-0.07) -1',
      abs(c_qh - 1) < 1e-3 and abs(c_h[0.07] - 1) < 1e-3 and abs(c_h[-0.07] + 1) < 1e-3, (round(c_qh, 4), c_h))
pcl = pc

# ---------------------------------------------------------------- the closing bullet of Section 4.21, decided on 2026-11-22 by the lecturer
# The bullet says that each Landau level has |C_n| = 1, so |sigma_xy| = N e^2/h for N filled levels, (4.2).
# A magnetic cell of the square lattice with the phase (4.4) of the charge +e, A = (0, s B x) and the flux 1/10: the
# hop from (x, y) to (x, y+1) is -exp(i s 2 pi x/10), s = +1 for the field along +z, and s = -1 is an electron there.
def landau_cell_q10(s, q=10):
    def hk_(k):
        m = np.diag(-2 * np.cos(k[1] - s * 2 * np.pi * np.arange(q) / q)).astype(complex)
        m += -np.eye(q, k=1) - np.eye(q, k=-1)
        m[q - 1, 0] += -np.exp(1j * k[0] * q)
        m[0, q - 1] += -np.exp(-1j * k[0] * q)
        return m
    return hk_, pcl.reciprocal([[q, 0], [0, 1]])


Cq10 = {s: [pcl.chern_links(*landau_cell_q10(s), bands=n, nk=10) for n in range(3)] for s in (1, -1)}
check('decided on 2026-11-22: closing bullet, each Landau level has |C_n| = 1 and N filled levels give |C_tot| = N, so |sigma_xy| = N e^2/h, for both charges', all(np.allclose(np.abs(Cq10[s]), 1, atol=1e-9)
      and np.allclose(np.abs(np.cumsum(Cq10[s])), [1, 2, 3], atol=1e-9) for s in Cq10)
      and np.allclose(Cq10[1], -1, atol=1e-9) and np.allclose(Cq10[-1], 1, atol=1e-9), {s: np.round(Cq10[s], 6) for s in Cq10})

# ---------------------------------------------------------------- the charge e/m as a magnitude, decided on 2026-11-22
# After an independent check the caption of the fractional figure and the closing bullet give e/m as the magnitude of
# the charge of a quasihole, as the key box of (4.15) does. The sign is -e/m for the charge +e: for m = 1 the quasihole
# at the origin moves the orbitals 0 to N - 1 to 1 to N, and the disc of radius R holds gammainc(1, R^2/2) -
# gammainc(N + 1, R^2/2) electrons fewer, 1 in the bulk for N = 40.
from scipy.special import gammainc  # noqa: E402
fewer = [gammainc(1, R ** 2 / 2) - gammainc(41, R ** 2 / 2) for R in (4.0, 5.0, 6.0)]
page20 = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'pages', 'session04',
                           '20-real-materials-realizing-chern-and-fractional-chern-physics.md'), encoding='utf-8').read()
check('decided on 2026-11-22: the caption and the closing bullet write the charge e/m as a magnitude, and for m = 1 the '
      'quasihole leaves 1 electron fewer, so its charge is -e for the charge +e',
      'In (a) the quasihole has a charge of magnitude $e/m$.' in page20
      and 'have a fractional charge of magnitude $e/m$, equation [(4.15)]' in page20
      and 'have fractional charge $e/m$' not in page20 and np.allclose(fewer, 1, atol=1e-3), np.round(fewer, 5))

print('all checks of page 20 hold')
