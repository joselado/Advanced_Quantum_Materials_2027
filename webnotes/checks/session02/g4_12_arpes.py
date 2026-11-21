"""Session 2, the numbers that page 12 (Section 2.12 on ARPES and Section 2.13, the closing summary) quotes and that no
figure script asserts. One check script per page is the rule: every number of a caption, a feedback, a fold, a
solution or a lab box is an assert, here or in the figure script that draws it. The figure arpes_geometry.py asserts
the 4.0 and 7.8 nm^-1 of its caption, and _g4_dos.py the numbers of the closing picture quiz. This script checks the
fold, the quiz with numbers as options, the problem, the feedback of the old quizzes and the widths of the closing list.
The constant hbar^2/2m is computed from the CODATA values, and each angle of the problem is checked twice, by the
formula and by inverting it. The two numbers of the lab box, 1.4 eV and 0.1 m_e, are quoted from the source and are not
computed here. It finds the repository from its own path and writes no file."""
import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


hbar, m_e, e_charge = 1.054571817e-34, 9.1093837015e-31, 1.602176634e-19
hb2_2m = hbar ** 2 / (2 * m_e) / e_charge * 1e20          # in eV Angstrom^2
check('hbar^2/2m = 3.81 eV A^2', abs(hb2_2m - 3.81) < 0.005, round(hb2_2m, 4))


def k_nm(E_kin):
    """The size of the momentum of a free electron of kinetic energy E_kin in eV, in nm^-1."""
    return np.sqrt(E_kin / hb2_2m) * 10


# the fold and the quiz with numbers: 20 eV gives 2.29 A^-1 = 22.9 nm^-1, and 10 degrees give 3.98 nm^-1
check('sqrt(20/3.81) in A^-1, the fold says 2.29', abs(np.sqrt(20 / 3.81) - 2.29) < 0.005 and abs(k_nm(20) / 10 - 2.29) < 0.005,
      round(np.sqrt(20 / 3.81), 4))
check('k at 20 eV, the fold says 22.9 nm^-1', abs(k_nm(20) - 22.9) < 0.05, round(k_nm(20), 3))
check('sin 10 deg = 0.174 and sin 20 deg = 0.342', abs(np.sin(np.radians(10)) - 0.174) < 5e-4 and abs(np.sin(np.radians(20)) - 0.342) < 5e-4,
      np.round(np.sin(np.radians([10, 20])), 4))
k10, k20 = k_nm(20) * np.sin(np.radians(10)), k_nm(20) * np.sin(np.radians(20))
check('k_par at 20 eV and 10 deg, 3.98 nm^-1 that rounds to 4.0', abs(k10 - 3.98) < 0.005 and round(k10, 1) == 4.0, round(k10, 4))
check('k_par at 20 eV and 20 deg, 7.84 nm^-1 that rounds to 7.8', abs(k20 - 7.84) < 0.005 and round(k20, 1) == 7.8, round(k20, 4))
check('22.9 x 0.174 = 3.98 and 22.9 x 0.342 = 7.83, the products the feedback writes', abs(22.9 * 0.174 - 3.98) < 0.005 and abs(22.9 * 0.342 - 7.84) < 0.01,
      (round(22.9 * 0.174, 4), round(22.9 * 0.342, 4)))
check('sin 10 deg is about half of sin 20 deg, the feedback of 7.8 nm^-1', abs(np.sin(np.radians(10)) / np.sin(np.radians(20)) - 0.5) < 0.01,
      round(np.sin(np.radians(10)) / np.sin(np.radians(20)), 4))
check('the wrong option 0.40 nm^-1 is the value in A^-1, 0.398', abs(k10 / 10 - 0.398) < 0.001 and round(k10 / 10, 2) == 0.40, round(k10 / 10, 4))

# the problem: a = 0.4 nm, the zone edge pi/a = 7.85 nm^-1, reached at 20.0 deg for 20 eV and at 9.9 deg for 80 eV
a = 0.4
edge = np.pi / a
check('pi/a for a = 0.4 nm, 7.85 nm^-1', abs(edge - 7.85) < 0.005, round(edge, 4))
th20 = np.degrees(np.arcsin(edge / k_nm(20)))
th80 = np.degrees(np.arcsin(edge / k_nm(80)))
check('angle of the zone edge at 20 eV, the solution says about 20 deg', abs(th20 - 20.0) < 0.1, round(th20, 3))
check('angle of the zone edge at 80 eV, the solution says 9.9 deg', abs(th80 - 9.9) < 0.05, round(th80, 3))
check('k at 80 eV is twice k at 20 eV, 45.8 nm^-1', abs(k_nm(80) - 2 * k_nm(20)) < 1e-9 and abs(k_nm(80) - 45.8) < 0.05, round(k_nm(80), 3))
check('sin of the two angles, 0.343 and 0.171', abs(edge / k_nm(20) - 0.343) < 5e-4 and abs(edge / k_nm(80) - 0.171) < 5e-4,
      (round(edge / k_nm(20), 4), round(edge / k_nm(80), 4)))
# second route: the angles put back into the formula give the zone edge
check('the two angles give back pi/a', abs(k_nm(20) * np.sin(np.radians(th20)) - edge) < 1e-9 and abs(k_nm(80) * np.sin(np.radians(th80)) - edge) < 1e-9,
      round(edge, 4))
# the photon at 80 eV of kinetic energy: about 85 eV with a work function of about 4.5 eV, so h nu/hbar c is about
# 0.4 nm^-1, five percent of pi/a, and all of it along the surface moves the angle of the zone edge by about half a degree
kph80 = 84.5 / 197.327
check('photon for 80 eV, about 0.4 nm^-1', round(kph80, 1) == 0.4, round(kph80, 3))
check('five percent of pi/a', abs(kph80 / edge - 0.05) < 0.01, round(kph80 / edge, 4))
shift = max(abs(np.degrees(np.arcsin((edge + s_) / k_nm(80))) - th80) for s_ in (kph80, -kph80))
check('the angle moves by about half a degree', 0.4 < shift < 0.6, round(shift, 3))

# the first quiz: on the chain -2t cos(ka), the energy is -2t at k = 0 and 0 at ka = pi/2
check('chain band at k = 0 and ka = pi/2, -2t and 0', np.isclose(-2 * np.cos(0), -2) and abs(-2 * np.cos(np.pi / 2)) < 1e-12, (-2, 0))

# the closing quiz on four orbitals: the uniform chain with a cell of four sites has -2t, 0, 0, 2t at phi = 0
L = 4
H = np.zeros((L, L))
for i in range(L):
    H[i, (i + 1) % L] += -1; H[(i + 1) % L, i] += -1          # phi = 0, the hopping to the next cell closes the ring
check('chain with a cell of four sites at phi = 0, -2t, 0, 0, 2t', np.allclose(np.linalg.eigvalsh(H), [-2, 0, 0, 2]), np.linalg.eigvalsh(H))

# the closing list: the widths 4t, 8t and 12t of the chain, the square and the cubic lattices with -t
k = np.linspace(-np.pi, np.pi, 41)
w1 = np.ptp(-2 * np.cos(k))
KX, KY = np.meshgrid(k, k)
w2 = np.ptp(-2 * (np.cos(KX) + np.cos(KY)))
KX, KY, KZ = np.meshgrid(k, k, k)
w3 = np.ptp(-2 * (np.cos(KX) + np.cos(KY) + np.cos(KZ)))
check('widths of the chain, the square and the cubic lattices, 4t, 8t and 12t', np.allclose([w1, w2, w3], [4, 8, 12]), (w1, w2, w3))

# ---- added after the physics check of the group, findings c2 and c5 and the numbers with no assert ----
import os  # noqa: E402
import sys  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

# c2, the momentum of the photon: h nu/hbar c with hbar c from CODATA, 0.101 nm^-1 at 20 eV and 0.127 at 25 eV, about
# 0.1, and 0.13 for 25 eV in the fold, small next to the 3.98 nm^-1 at 10 degrees
c_light = 299792458.0
hbar_c = hbar * c_light / e_charge * 1e9                  # in eV nm
check('hbar c = 197.3 eV nm', abs(hbar_c - 197.3) < 0.05, round(hbar_c, 3))
kph = np.array([20.0, 25.0]) / hbar_c
check('photon of 20 to 25 eV, h nu/hbar c from 0.10 to 0.13 nm^-1, about 0.1', kph[0] > 0.1 and kph[1] < 0.13 and round(kph[1], 2) == 0.13,
      np.round(kph, 4))
check('the photon of 25 eV is about 3 percent of the 3.98 nm^-1, small', kph[1] / k10 < 0.035, round(kph[1] / k10, 4))

# c2, the sign of E - E_F = E_kin + phi - h nu, not on the conventions sheet, checked by two routes. The first is the
# balance of the energy: the photon brings h nu, an electron at the Fermi level needs phi to reach the vacuum, and one
# below it needs E_F - E more. The second is the Fermi edge: the fastest electrons, E_kin = h nu - phi, come from E_F.
hnu, phi, EF = 21.2, 4.5, 0.0
for E in (0.0, -0.4, -1.0, -2.5):
    Ekin = hnu - phi - (EF - E)                           # the fold, route one
    check('E - E_F = E_kin + phi - h nu for a state at %g eV, the box' % E, abs((Ekin + phi - hnu) - (E - EF)) < 1e-12,
          round(Ekin + phi - hnu, 6))
check('the Fermi edge, E_kin = h nu - phi, gives E = E_F, route two', abs((hnu - phi) + phi - hnu) < 1e-12, hnu - phi)
check('a deeper state gives a slower electron, so only E < E_F is seen', hnu - phi - (EF - (-1.0)) < hnu - phi, 'True')

# c5 and the closing quiz on three densities of states, run in --verify from the pyqula script of the pictures
sys.dont_write_bytecode = True                                     # the check writes no file
os.environ.setdefault('MPLBACKEND', 'Agg')
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures', 'session02'))
import style  # noqa: E402
import _g4_dos  # noqa: E402
d = style.run_script('session02/g4_dos_three.py')
_g4_dos.check(d)
e = np.array(d['e'])
c, hc, kg = np.array(d['dos_chain']), np.array(d['dos_honeycomb']), np.array(d['dos_kagome'])
i0 = np.argmin(np.abs(e))
check('chain at zero energy, 1/(2 pi t) = 0.159, about 0.16/t', abs(c[i0] - 1 / (2 * np.pi)) < 0.001 and round(1 / (2 * np.pi), 2) == 0.16,
      round(c[i0], 4))
pk = [e[np.abs(e - s) < 0.1][np.argmax(c[np.abs(e - s) < 0.1])] for s in (-1.98, 1.98)]
pv = [c[np.abs(e - s) < 0.1].max() for s in (-1.98, 1.98)]
check('chain peaks at the band edges, at +-1.98 on the grid, cut by the broadening to about 0.64',
      np.allclose(pk, [-1.98, 1.98], atol=0.011) and np.allclose(pv, 0.644, atol=0.002) and round(pv[0], 2) == 0.64, np.round(pv, 4))
# second and third routes for the 0.64: a numpy Lorentzian sum on 2000 momenta, and the broadened formula
ks = np.arange(2000) / 2000 * 2 * np.pi
lor = np.mean(0.04 / np.pi / ((1.98 + 2 * np.cos(ks)) ** 2 + 0.04 ** 2))
z = 1.98 + 0.04j
formula = (-1 / np.pi / (np.sqrt(z - 2) * np.sqrt(z + 2))).imag
check('the chain peak by numpy and by -Im 1/(pi sqrt(z^2 - 4)) at z = 1.98 + 0.04i', abs(lor - pv[1]) < 1e-6 and abs(formula - pv[1]) < 1e-6,
      (round(lor, 4), round(formula, 4)))
check('the 0.64 is below the top 0.9 of the picture, so the peaks are drawn whole', max(pv) < 0.9, round(max(pv), 3))
check('graphene at zero energy, about 0.04, the V rounded by the broadening', abs(hc[i0] - 0.04) < 0.002, round(hc[i0], 4))
w = np.abs(e + 1) < 0.4
check('kagome V at -t, 0.042, at the same height as the tip of graphene', abs(kg[w].min() - 0.042) < 0.002 and abs(kg[w].min() - hc[i0]) < 0.003,
      round(kg[w].min(), 4))
check('kagome flat band at 2t far above the top 0.9 of the picture', abs(e[np.argmax(kg)] - 2) < 1e-9 and kg.max() > 7, round(kg.max(), 2))

# the lab box: the words of the box against the stored texts of talirz2017. The tracked file keeps a quotation with the
# 1.4 eV and the 0.1 m_e. The full copy, which git ignores, holds the whole abstract with the width and the substrate.
src = os.path.join(HERE, '..', '..', 'sources')
tracked = ' '.join(open(os.path.join(src, 'session02', 'talirz2017_acsnano.6b06405.txt'), encoding='utf-8').read().split())
for phrase in ('band gap of 1.4 eV', 'effective masses of ≈0.1 m', 'Fourier-transformed scanning tunneling spectroscopy reveal',
               '9-Atom Wide Armchair Graphene Nanoribbons'):
    check('lab box talirz2017, the tracked file says "%s"' % phrase, phrase in tracked, 'found')
full = os.path.join(src, '.full', 'session02', 'talirz2017_acsnano.6b06405.txt')
if os.path.exists(full):
    text = ' '.join(open(full, encoding='utf-8').read().split())
    for phrase in ('with a width of nine carbon atoms on Au(111)', 'effective masses of ≈0.1 m e for both electrons and holes',
                   'Angle-resolved photoemission spectroscopy and Fourier-transformed scanning tunneling spectroscopy reveal'):
        check('lab box talirz2017, the full copy says "%s"' % phrase, phrase in text, 'found')
else:
    print('NOT CHECKED nine carbon atoms and Au(111) of talirz2017, no full copy of the source on this machine', flush=True)
