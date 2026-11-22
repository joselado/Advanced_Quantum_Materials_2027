"""Session 1, the numbers that page 02 (Section 1.2) quotes, in the caption of filling_bands and in its quizzes.

The bands of the caption and of the picture quiz are asserted in figures/session01/_g1_fill.py, from the pyqula script
webnotes/scripts/session01/g1_chain_bands.py, and this script runs its check() too, so that --verify sees those
asserts. It adds a second route in numpy for the fillings, the electrons per site of the caption by three routes, the
count of the six families of the list, and the numbers of the quiz on the two chains with the hoppings 1 and 2, whose
figure ssh_pair.py asserts only a part of them, so its six sites and 20 sites are read from its text. The feedback of the
doping quiz quoted the gap of silicon and the density of the dopants with no source, and since 2026-11-22 it quotes no
number, which the last check reads on the page. It writes no file."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures', 'session01'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures'))
import _g1_fill


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# the fillings, from the pyqula script through the figure helper
_g1_fill.check()

# a second route: the same chains in numpy, with k per site and the cell of two sites of length 2
t, m = 1.0, 0.6
k = (np.arange(4000) + 0.5) / 4000 * 2 * np.pi - np.pi          # a mesh of the zone of the chain with one site
metal = -2 * t * np.cos(k)
check('the metal at E_F = 0 has half of its states filled', abs((metal < 0).mean() - 0.5) < 1e-12,
      (metal < 0).mean())
q = k / 2                                                       # the zone of the cell of two sites, -pi/2 to pi/2
H = lambda x: np.array([[m, -t * (1 + np.exp(-2j * x))], [-t * (1 + np.exp(2j * x)), -m]])
bands = np.array([np.linalg.eigvalsh(H(x)) for x in q])
check('the gap goes from -0.6t to 0.6t', abs(bands[:, 0].max() + 0.6) < 1e-5 and abs(bands[:, 1].min() - 0.6) < 1e-5,
      (bands[:, 0].max(), bands[:, 1].min()))
check('E_F = 0 lies in the gap, so the valence band is full and the conduction band empty',
      bands[:, 0].max() < 0 < bands[:, 1].min(), 0)
nel = (bands[:, 1] < 0.95).mean()
check('E_F = 0.95t lies above the bottom of the conduction band, which holds some electrons', 0.6 < 0.95 and 0 < nel < 0.5,
      round(nel, 3))
nh = (bands[:, 0] > -0.95).mean()
check('E_F = -0.95t leaves holes at the top of the valence band, as many as the electrons above', abs(nh - nel) < 1e-12,
      round(nh, 3))
check('m + 0.35 is 0.95, the Fermi level of the doped chains', abs(m + 0.35 - 0.95) < 1e-12, m + 0.35)

# the caption: at E_F = 0.95t the spinless chain has 0.12 electrons per site in the conduction band, 0.24 of that band.
# The conduction band holds one state per cell of two sites, so the electrons per site are half of the filled part.
# First route, the closed form: E < E_F for |cos k| < sqrt(E_F^2 - m^2)/(2t), with k per site from -pi to pi.
EFn = 0.95
part = 2 / np.pi * np.arcsin(np.sqrt(EFn ** 2 - m ** 2) / (2 * t))
check('closed form, 0.24 of the conduction band is filled at E_F = 0.95t', round(part, 2) == 0.24, part)
check('closed form, 0.12 electrons per site', round(part / 2, 2) == 0.12, part / 2)
kd = (np.arange(200000) + 0.5) / 200000 * 2 * np.pi - np.pi
dense = (np.sqrt(m ** 2 + 4 * t ** 2 * np.cos(kd) ** 2) < EFn).mean()
check('a midpoint mesh of 200000 points gives the same part', abs(dense - part) < 1e-4, dense)
check('the Bloch matrix on the mesh of 4000 points, the same 0.24 and 0.12', round(nel, 2) == 0.24 and round(nel / 2, 2) == 0.12,
      (nel, nel / 2))
d = _g1_fill.data()
check('the pyqula script is spinless, one band per site of the chain and two per cell of the bichain',
      np.array(d['metal']).ndim == 1 and np.array(d['bands']).shape[1] == 2, np.array(d['bands']).shape)
check('the metal band of the alt text goes from -2t to 2t', abs(np.max(d['metal']) - 2) < 1e-12 and abs(np.min(d['metal']) + 2) < 1e-12,
      (np.min(d['metal']), np.max(d['metal'])))

# the opener and the list: six families of materials, one bullet each
page = open(os.path.join(HERE, '..', '..', 'pages', 'session01', '02-a-tour-of-the-quantum-materials-we-will-meet.md'),
            encoding='utf-8').read()
families = [x for x in page.splitlines() if x.startswith('- **')]
check('the list has six families of materials', len(families) == 6 and 'six families' in page,
      [x[4:x.index('**', 4)] for x in families])


# the quiz on the two chains with the hoppings 1 and 2
def bulk(t1, t2, n=400):
    kk = np.linspace(-np.pi, np.pi, n)
    return np.sort(np.array([[-abs(t1 + t2 * np.exp(1j * x)), abs(t1 + t2 * np.exp(1j * x))] for x in kk]).ravel())


def open_chain(t1, t2, N=20):
    T = np.zeros((N, N))
    for i in range(N - 1):
        T[i, i + 1] = T[i + 1, i] = t1 if i % 2 == 0 else t2
    return np.sort(np.abs(np.linalg.eigvalsh(T)))


check('the two chains have the same bulk bands', np.allclose(bulk(1., 2.), bulk(2., 1.)), True)
gap = 2 * np.abs(1 + 2 * np.exp(1j * np.pi))
check('the bulk gap is 2|t1 - t2| = 2', abs(gap - 2) < 1e-12 and abs(bulk(1., 2.)[bulk(1., 2.) > 0].min() - 1) < 1e-4, gap)
lowA, lowB = open_chain(1., 2.), open_chain(2., 1.)
check('20 sites with the weak bond at the ends, two levels at |E| = 1.5e-3, inside the gap, and the next at 1.11',
      abs(lowA[0] - 1.5e-3) < 1e-4 and abs(lowA[1] - 1.5e-3) < 1e-4 and abs(lowA[2] - 1.11) < 0.01, lowA[:3])
check('20 sites with the strong bond at the ends, no level in the gap, the lowest |E| is 1.07',
      abs(lowB[0] - 1.07) < 0.01, lowB[:2])

# the caption and the alt of ssh_pair: the chains are drawn with six sites and bonds 1, 2, 1, 2, 1 and 2, 1, 2, 1, 2, and
# the spectra are for 20 sites. ssh_pair.py is read as text and not run, since running it writes its SVG.
src = open(os.path.join(HERE, '..', '..', 'figures', 'session01', 'ssh_pair.py'), encoding='utf-8').read()
check('ssh_pair draws six sites per chain', 'x = np.arange(6) * 1.0' in src and 'for i in range(5):' in src, 6)
check('ssh_pair computes the spectra of 20 sites', 'def levels(t1, t2, N=20):' in src
      and 'wA, vA = levels(1.0, 2.0)' in src and 'wB, vB = levels(2.0, 1.0)' in src, 20)
check('ssh_pair draws chain A with t1 = 1, t2 = 2 and chain B with t1 = 2, t2 = 1',
      "chain(1.0, 1.0, 2.0, 'A', True)" in src and "chain(-0.4, 2.0, 1.0, 'B', False)" in src
      and "tt = t1 if i % 2 == 0 else t2" in src, True)
bondsA = [1 if i % 2 == 0 else 2 for i in range(5)]
bondsB = [2 if i % 2 == 0 else 1 for i in range(5)]
check('so the drawn bonds are 1, 2, 1, 2, 1 and 2, 1, 2, 1, 2', bondsA == [1, 2, 1, 2, 1] and bondsB == [2, 1, 2, 1, 2],
      (bondsA, bondsB))

# the doping quiz, feedback corrected on 2026-11-22: the gap of silicon and the density of the dopants had no stored
# source, so the feedback of the second option quotes no number
page = open(os.path.join(HERE, '..', '..', 'pages', 'session01', '02-a-tour-of-the-quantum-materials-we-will-meet.md'),
            encoding='utf-8').read()
fb = next(l for l in page.split('\n') if 'Silicon doped with phosphorus' in l)
check('the doping quiz: the feedback on silicon quotes no number', not any(ch.isdigit() for ch in fb), fb.strip())
