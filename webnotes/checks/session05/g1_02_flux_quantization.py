"""Session 5, the numbers of page 02 (Sections 5.2 and 5.3), in the fold, the lab box, the quizzes and the problem.

The constants are the exact SI values of h and e. The lab box quotes 2e/h = 483.5912 +- 0.0030 MHz/muV from its source,
which labsource.py checks, and converts it to h/2e, which is asserted here to the four digits of the page, the same
digits that the SI value gives. The field lines of the picture quiz of Section 5.3 are asserted by
_g1_fieldlines.check, which this script calls, and the field at the equator of the Meissner sphere is asserted here.
The old text says "trillions of atoms" and "billions of atoms", which are asserted as lower bounds for samples of
10 and 1 micrometer. It writes no file."""
import os, sys
import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


h = 6.62607015e-34                                        # J s, exact
e = 1.602176634e-19                                       # C, exact
hbar = h / (2 * np.pi)
phi0 = h / (2 * e)

# the fold: on a circle of radius R with the flux Phi, j = 0 gives d theta / d phi = q Phi / h, and one turn winds the
# phase by 2 pi q Phi / h, which is 2 pi n exactly when Phi = n h / q; checked by integrating the phase numerically
R = 1e-6
for q in (2 * e, -2 * e):
    for n in (1, 2, -3):
        Phi = n * h / q
        A_phi = Phi / (2 * np.pi * R)                    # the vector potential along the circle
        phis = np.linspace(0, 2 * np.pi, 2001)
        grad = q * A_phi / hbar                           # the gradient of the phase along the circle, j = 0
        winding = np.trapezoid(np.full_like(phis, grad * R), phis)
        assert np.isclose(winding, 2 * np.pi * n) and np.isclose(grad * R, q * Phi / h)
check('a circle with j = 0 and Phi = n h/q winds the phase by 2 pi n, for q = +2e and -2e', True, 'n = 1, 2, -3')
check('q = -2e gives the same set of fluxes as q = 2e, n -> -n',
      np.allclose(sorted(n * h / (2 * e) for n in range(-3, 4)), sorted(n * h / (-2 * e) for n in range(-3, 4))), 'ok')

# the quiz on the step: h/e = 4.1e-15 Wb, twice h/2e = 2.07e-15 Wb, and the step h/q for q = 4e and e/2
check('h/e = 4.1e-15 Wb and h/2e = 2.07e-15 Wb', round(h / e * 1e15, 1) == 4.1 and round(phi0 * 1e15, 2) == 2.07,
      (h / e, phi0))
check('h/e is twice h/2e, h/4e needs q = 4e, q = e/2 gives 2h/e', np.isclose(h / e, 2 * phi0) and
      np.isclose(h / (4 * e), phi0 / 2) and np.isclose(h / (e / 2), 2 * h / e), 'ok')

# the lab box: 2e/h = 483.5912 MHz/muV of the source gives h/2e = 2.068e-15 Wb, and the SI value gives the same digits
measured = 483.5912e6 / 1e-6                              # Hz per V
conv = 1 / measured
check('1/(483.5912 MHz/muV) = 2.068e-15 Wb, the conversion of the lab box', round(conv * 1e15, 3) == 2.068, conv)
check('the SI value h/2e = 2.068e-15 Wb to the same four digits', round(phi0 * 1e15, 3) == 2.068, phi0)

# the Josephson quiz: 2eV/h, eV/h and eV/2h for V = 1 muV
V = 1e-6
f2, f1, fh = 2 * e * V / h / 1e6, e * V / h / 1e6, e * V / (2 * h) / 1e6
check('2eV/h = 483.6 MHz, eV/h = 241.8 MHz and eV/2h = 120.9 MHz at V = 1 muV',
      round(f2, 1) == 483.6 and round(f1, 1) == 241.8 and round(fh, 1) == 120.9, (f2, f1, fh))
check('eV/h is half and eV/2h a quarter of 2eV/h', np.isclose(f1, f2 / 2) and np.isclose(fh, f2 / 4), 'ok')
check('the energy 2eV of a pair gives the phase rate 2eV/hbar and the frequency 2eV/h',
      np.isclose((2 * e * V / hbar) / (2 * np.pi), 2 * e * V / h), 'ok')

# the problem: a hole of radius 1 muM, the area 3.14e-12 m^2 and the field 0.658 mT, and 6.58 muT for 10 muM
area = np.pi * (1e-6) ** 2
B = phi0 / area
check('pi r^2 = 3.142e-12 m^2 and B = 6.58e-4 T = 0.658 mT', round(area * 1e12, 3) == 3.142 and round(B * 1e4, 2) == 6.58
      and round(B * 1e3, 3) == 0.658, (area, B))
check('the rounded values of the solution give the same field, 2.068e-15 / 3.142e-12 = 6.58e-4 T',
      round(2.068e-15 / 3.142e-12 * 1e4, 2) == 6.58 and round(phi0 * 1e15, 3) == 2.068, 2.068e-15 / 3.142e-12)
B10 = phi0 / (np.pi * (10e-6) ** 2)
check('a radius of 10 muM gives a period 100 times smaller, 6.58 muT', np.isclose(B / B10, 100) and round(B10 * 1e6, 2) == 6.58,
      B10)

# the old text of Section 5.2: a superconductor of "trillions of atoms", and "billions of atoms" in a macroscopic
# measurement. With at least one atom in a cube of side 0.5 nm, larger than the distance between neighbor atoms of a
# metal, a cube of side 10 micrometer holds at least 8e12 atoms, trillions, and a cube of side 1 micrometer at least
# 8e9, billions, which is the radius of the hole of the problem
atoms = lambda side: (side / 0.5e-9) ** 3
check('a sample of 10 um holds more than a trillion atoms, and one of 1 um more than a billion',
      atoms(10e-6) >= 1e12 and atoms(1e-6) >= 1e9, (atoms(10e-6), atoms(1e-6)))

# the picture quiz of Section 5.3: the field lines of the three pictures, B_r continuous at the surface, div B = 0,
# four lines through the sphere in the picture of the vortices and none in the Meissner picture
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'figures', 'session05'))
import _g1_fieldlines
_g1_fieldlines.check()
check('the field lines of the quiz pictures: four lines enter the sphere with vortices, none the Meissner sphere', True,
      'beta = -1/4 and -1/2')
# the feedback of the Meissner picture: for the perfect diamagnet (beta = -1/2) the field at the equator is 1.5 times
# the applied field, so it reaches the lower critical field when the applied field is 2/3 of it
Bx, Bz = _g1_fieldlines.field(np.array([1.0]), np.array([0.0]), -0.5)
Bx2, Bz2 = _g1_fieldlines.field(np.array([-1.0]), np.array([0.0]), -0.5)
check('the Meissner sphere: the field at the equator is 1.5 times the applied field, so vortices enter at 2/3 of Hc1',
      np.isclose(np.hypot(Bx[0], Bz[0]), 1.5) and np.isclose(np.hypot(Bx2[0], Bz2[0]), 1.5) and np.isclose(1 / 1.5, 2 / 3),
      (float(Bz[0]), 1 / 1.5))
# the equator is the largest field on the surface, B_th = -1.5 B0 sin(th), so the field there is the first to reach Hc1
th = np.linspace(0.01, np.pi - 0.01, 300)
Bxs, Bzs = _g1_fieldlines.field(np.sin(th), np.cos(th), -0.5)
check('on the surface of the Meissner sphere the field is largest at the equator', np.isclose(np.hypot(Bxs, Bzs).max(), 1.5, atol=1e-4)
      and abs(th[np.argmax(np.hypot(Bxs, Bzs))] - np.pi / 2) < 0.02, round(float(np.hypot(Bxs, Bzs).max()), 4))
