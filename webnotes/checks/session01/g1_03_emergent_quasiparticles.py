"""Session 1, the numbers that page 03 (Section 1.3) quotes, in the caption of vortex_phase, in the quizzes and in the
lab box.

The windings of the picture quiz and of vortex_phase are asserted in figures/session01/_g1_phase.py, and this script
runs its check() too. It adds a second route for the winding, with np.unwrap on other loops, the spins of the quiz
on the spinons, and the numbers of the lab box, which must stand in the tracked source file
webnotes/sources/session01/cornelissen2015_nphys3465.txt. It writes no file."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures', 'session01'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures'))
import _g1_phase


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


w = _g1_phase.check()
check('the windings along the red loop are 0, 1 and 0', [round(w[x], 9) for x in ('uniform', 'vortex', 'bend')] == [0, 1, 0], w)
check('the red loop has the radius 2.2 xi', _g1_phase.LOOP == 2.2, _g1_phase.LOOP)


def unwrap_winding(kind, center, radius, n=4000):
    phi = np.linspace(0, 2 * np.pi, n + 1)
    amp, th = _g1_phase.field(kind, center[0] + radius * np.cos(phi), center[1] + radius * np.sin(phi))
    ph = np.unwrap(np.angle(amp * np.exp(1j * th)))
    return (ph[-1] - ph[0]) / (2 * np.pi)


check('the vortex winds once along any loop around the core', all(abs(unwrap_winding('vortex', (0, 0), r) - 1) < 1e-9
                                                                   for r in (0.3, 1.0, 2.2, 3.0)), True)
check('a loop that does not hold the core has the winding 0', abs(unwrap_winding('vortex', (2., 1.5), 0.8)) < 1e-9, True)
check('the bend has the winding 0 on every loop', all(abs(unwrap_winding('bend', c, r)) < 1e-9
                                                      for c, r in (((0, 0), 2.2), ((0, 0), 3.0), ((1, -1), 1.5))), True)
amp0 = _g1_phase.field('vortex', 0., 0.)[0]
check('the amplitude of the vortex vanishes at the core', amp0 == 0, amp0)
# a smooth change of the arrows makes the bend uniform: theta = s pi y / 4 with s from 1 to 0 keeps the amplitude 1,
# and the winding along the red loop stays 0 at every step
phi = np.linspace(0, 2 * np.pi, 4001)
steps = []
for s_ in np.linspace(1, 0, 11):
    ph = np.unwrap(s_ * np.pi * _g1_phase.LOOP * np.sin(phi) / 4)
    steps.append((ph[-1] - ph[0]) / (2 * np.pi))
check('the bend goes smoothly to the uniform field, with the winding 0 at every step', np.allclose(steps, 0, atol=1e-9),
      max(abs(x) for x in steps))

# the quiz on the spinons: two spins 1/2 give the total spin 0 or 1, two spins 1 give up to 2
sx = np.array([[0, 1], [1, 0]]) / 2; sy = np.array([[0, -1j], [1j, 0]]) / 2; sz = np.diag([0.5, -0.5])
S2 = sum(np.kron(s, np.eye(2)) @ np.kron(s, np.eye(2)) + 2 * np.kron(s, s) + np.kron(np.eye(2), s) @ np.kron(np.eye(2), s)
         for s in (sx, sy, sz))
ev = np.round(np.linalg.eigvalsh(S2), 9)
check('two spins 1/2 have S(S+1) = 0 once and 2 three times, so S = 0 or 1', list(ev) == [0, 2, 2, 2], ev)
l1 = [np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]) / np.sqrt(2), np.array([[0, -1j, 0], [1j, 0, -1j], [0, 1j, 0]]) / np.sqrt(2),
      np.diag([1., 0., -1.])]
S2 = sum((np.kron(s, np.eye(3)) + np.kron(np.eye(3), s)) @ (np.kron(s, np.eye(3)) + np.kron(np.eye(3), s)) for s in l1)
ev1 = np.linalg.eigvalsh(S2)
check('two spins 1 give the total spin up to 2, S(S+1) = 6', abs(ev1.max() - 6) < 1e-9, round(ev1.max(), 9))
# the quiz on the Mott insulator: with U n_up n_dn a second electron on a site costs U, 10t for U = 10t
U = 10.0
check('a doubly occupied site has the energy U n_up n_dn = U, 10t for U = 10t', U * 1 * 1 == 10.0, U)
check('a site holds one electron, with S_z = +-1/2', set(np.diag(sz)) == {0.5, -0.5}, np.diag(sz))

# the lab box: every number of the box is in the tracked source, in the sentence that the box uses
src = open(os.path.join(HERE, '..', '..', 'sources', 'session01', 'cornelissen2015_nphys3465.txt'), encoding='utf-8').read()
check('the source states 40 μm for the distance of the spin transport through YIG',
      'over distances as large as 40 μm' in src, True)
check('the source states the magnon spin diffusion length 9.4 ± 0.6 μm in a 200 nm YIG film at room temperature',
      'magnon spin diffusion length λ = 9.4 ± 0.6 μm in a thin 200 nm YIG film at room temperature' in src, True)
check('the source calls YIG a magnetic insulator where the large band gap prohibits the motion of electrons',
      'magnetic insulator, where the large bandgap prohibits the motion of electrons' in src
      and 'excited and detected fully electrically' in src, True)
page = open(os.path.join(HERE, '..', '..', 'pages', 'session01',
                         '03-emergent-quasiparticles-and-what-the-lattice-gives-us.md'), encoding='utf-8').read()
import re
four = re.search(r'the same four ingredients, which are ([^.]*?), and a single isolated atom', page)
names = re.split(r', | and ', four.group(1)) if four else []
check('the four ingredients are four, electrons, protons, neutrons and photons',
      names == ['electrons', 'protons', 'neutrons', 'photons'], names)
box = page.split('::: lab', 1)[1].split(':::', 1)[0]
check('the box quotes 40 μm, 200 nm and 9.4 ± 0.6 μm and links the article',
      '$40$ μm' in box and '$200$ nm' in box and '$9.4\\pm0.6$ μm' in box and 'nature.com/articles/nphys3465' in box, True)
