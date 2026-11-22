"""Session 4, the numbers and the algebra that page 11 (Sections 4.11 and 4.12, the lattice ribbons in a field and the
ladder operators) quotes, checked by a second route. One check script per page is the rule: every number of a caption,
a feedback, a fold or a solution is an assert, here or in the figure script that draws it. The figure scripts assert
their own numbers: wall_squeeze.py (0.50, 0.73 and 1.50 by finite differences) and _g3_ribbons.check, which
lattice_ribbons.py and the three pictures of the quiz call (the levels -3.88, -3.63, -3.40, the spacing 0.24 and
hbar omega_c = 0.25, the levels 0, 0.37, 0.52 against E_1 = 0.38 and 0.53, the ratio 1.40, one branch per edge with
opposite slopes, the no-field band from 0.03 to 0.48). This script runs that check again on the pyqula script, checks the
width and the period of the two ribbons, the edge branches over the whole gap of (a) and from 0 to 0.34 in (b), the dip
of the level 0.37 to 0.35 near the armchair edges with three branches per edge above it, the names canonical and kinetic
momentum, the energies of the wall by the zero of the parabolic cylinder function, the commutator
of the problem in the two gauges and the fold from (pi_x^2 + pi_y^2)/2m to (4.8) with sympy, acting on a test function.
It finds the repository from its own path and writes no file, since style.run_script runs pyqula in a temporary
folder.

The blocks marked "corrected on 2026-11-22" back the sentences of the old text that were corrected on that day, after
the lecturer chose to fix the errors of the old text. The block marked "decided on 2026-11-22" backs the width N = 30
of the Core cells, which the text gives again after an independent check found it in the notebook."""
import os
import sys

import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.special import pbdv

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, '..', '..', 'figures')
sys.path.insert(0, FIG)
sys.path.insert(0, os.path.join(FIG, 'session04'))


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# the problem: [pi_x, pi_y] = i hbar B in the Landau and in the symmetric gauge, with pi = p - A (charge +e, e = 1),
# acting on a test function f(x, y)
x, y, hb, B, m = sp.symbols('x y hbar B m', positive=True)
f = sp.Function('f')(x, y)


def ops(A):
    px = lambda g: -sp.I * hb * sp.diff(g, x)
    py = lambda g: -sp.I * hb * sp.diff(g, y)
    pix = lambda g: px(g) - A[0] * g
    piy = lambda g: py(g) - A[1] * g
    return pix, piy


# the names of the opener, the key box and the problem: p = -i hbar grad is the canonical momentum, conjugate to x, and
# its components commute, so the commutator that gives the oscillator is the one of the kinetic momentum pi = p - A
canon = sp.simplify(x * (-sp.I * hb * sp.diff(f, x)) - (-sp.I * hb * sp.diff(x * f, x)))
pxpy = sp.simplify(-sp.I * hb * sp.diff(-sp.I * hb * sp.diff(f, y), x) + sp.I * hb * sp.diff(-sp.I * hb * sp.diff(f, x), y))
check('problem: p is the canonical momentum, [x, p_x] = i hbar, and [p_x, p_y] = 0',
      sp.simplify(canon - sp.I * hb * f) == 0 and pxpy == 0, (canon, pxpy))
gauges = {'Landau (0, Bx)': (0, B * x), 'symmetric B/2 (-y, x)': (-B * y / 2, B * x / 2)}
for name, A in gauges.items():
    pix, piy = ops(A)
    comm = sp.simplify(pix(piy(f)) - piy(pix(f)))
    check('problem: [pi_x, pi_y] = i hbar B in the gauge ' + name, sp.simplify(comm - sp.I * hb * B * f) == 0, comm)
    # the general form i hbar (d_x A_y - d_y A_x)
    curl = sp.diff(A[1], x) - sp.diff(sp.sympify(A[0]), y)
    check('problem: d_x A_y - d_y A_x = B in the gauge ' + name, sp.simplify(curl - B) == 0, curl)
    # the fold: with l_B^2 = hbar/B, a = l_B (pi_x + i pi_y)/(sqrt2 hbar), the operator identities
    lB = sp.sqrt(hb / B)
    a = lambda g: lB / (sp.sqrt(2) * hb) * (pix(g) + sp.I * piy(g))
    ad = lambda g: lB / (sp.sqrt(2) * hb) * (pix(g) - sp.I * piy(g))
    check('fold: [a, a^dagger] = 1 in the gauge ' + name, sp.simplify(a(ad(f)) - ad(a(f)) - f) == 0, 'on f(x, y)')
    H = (pix(pix(f)) + piy(piy(f))) / (2 * m)
    check('fold: (pi_x^2 + pi_y^2)/2m = hbar (B/m) (a^dagger a + 1/2) in the gauge ' + name,
          sp.simplify(sp.expand(H - hb * B / m * (ad(a(f)) + f / 2))) == 0, 'on f(x, y)')
    check('fold: a^dagger a = l_B^2/(2 hbar^2) (pi_x^2 + pi_y^2) - 1/2 in the gauge ' + name,
          sp.simplify(sp.expand(ad(a(f)) - (lB ** 2 / (2 * hb ** 2) * (pix(pix(f)) + piy(piy(f))) - f / 2))) == 0,
          'on f(x, y)')

# the quiz on the wall: the lowest level with a hard wall at x = 0 and the center x0, in units of hbar omega_c and l_B,
# is the energy E where the parabolic cylinder function D_{E - 1/2}(-sqrt2 x0) vanishes, a route without a grid
def wall_level(x0):
    D = lambda E: pbdv(E - 0.5, -np.sqrt(2) * x0)[0]
    Es = np.linspace(0.4999, 1.6, 2202)                # the first zero above 1/2 is the lowest level
    vals = np.array([D(v) for v in Es])
    i = np.where(np.sign(vals[1:]) != np.sign(vals[:-1]))[0][0]
    return brentq(D, Es[i], Es[i + 1])


E = [wall_level(x0) for x0 in (3.0, 1.0, 0.0)]
check('quiz: the wall levels for x0 = 3, 1, 0 l_B are 0.50, 0.73 and 1.50 hbar omega_c',
      [round(v, 2) for v in E] == [0.5, 0.73, 1.5], np.round(E, 4))

# the ribbons: the check of the figures, again on the downloadable pyqula script
import style                      # noqa: E402
import _g3_ribbons                # noqa: E402
d = style.run_script('session04/g3_ribbons_in_field.py')
num = _g3_ribbons.check(d)
check('ribbons: the numbers of the caption and of the quiz, _g3_ribbons.check', True, num)
check('ribbons: the square ribbon is 40 sites wide', d['square_energies'].shape[1] == 40 and d['square_edge'] == 19.5,
      d['square_edge'])
check('ribbons: the armchair ribbon is 51 bond lengths wide', round(2 * d['honeycomb_edge']) == 51, 2 * d['honeycomb_edge'])
check('ribbons: hbar omega_c = 4 pi 0.02 t = 0.25 t and E_1 = 3 sqrt(pi 0.005) t = 0.38 t',
      round(4 * np.pi * 0.02, 2) == 0.25 and round(3 * np.sqrt(np.pi * 0.005), 2) == 0.38, num['E1'])

# the caption of lattice_ribbons: the period a of the two ribbons, one lattice constant and three bond lengths
import tempfile                   # noqa: E402
cwd = os.getcwd()
with tempfile.TemporaryDirectory() as tmp:
    os.chdir(tmp)
    try:
        from pyqula import geometry
        periods = [float(np.linalg.norm(geometry.square_ribbon(40).a1)),
                   float(np.linalg.norm(geometry.honeycomb_armchair_ribbon(30).a1))]
    finally:
        os.chdir(cwd)
check('ribbons: the period a is 1 for the square ribbon and 3 bond lengths for the armchair ribbon',
      np.allclose(periods, [1, 3]), periods)

# the caption of lattice_ribbons: one branch per edge with opposite slopes in the whole gap above -3.88 in (a) and from
# zero energy to 0.34 in (b); near each edge of (b) the level 0.37 dips to 0.35, so just below it three branches cross
# at each edge, with the net count one
ks = d['ks']
Es, Ys, Eh, Yh = d['square_energies'], d['square_positions'], d['honeycomb_energies'], d['honeycomb_positions']
lev, pos = num['square'], num['honeycomb']


def per_edge(E, Y, mu, edge):
    top, bot = _g3_ribbons.edge_modes(E, Y, ks, mu, edge)
    return len(top), len(bot), int(sum(top)), int(sum(bot))


scan = [per_edge(Es, Ys, mu, d['square_edge']) for mu in np.linspace(lev[0] + 0.005, lev[1] - 0.005, 60)]
check('ribbons (a): one branch per edge, opposite slopes, in the whole gap from -3.88 to -3.63',
      all(s[:2] == (1, 1) and s[2] == -s[3] for s in scan), set(scan))
scan = [per_edge(Eh, Yh, mu, d['honeycomb_edge']) for mu in np.linspace(0.005, 0.34, 68)]
check('ribbons (b): one branch per edge, opposite slopes, from zero energy to 0.34',
      all(s[:2] == (1, 1) and s[2] == -s[3] for s in scan), set(scan))
Esort = np.sort(Eh, axis=1)
dips = []
for n in range(Esort.shape[1]):
    e = Esort[:, n]
    for j in range(1, len(ks) - 1):
        if e[j] < e[j - 1] and e[j] < e[j + 1] and 0.2 < e[j] < pos[1] - 0.01:
            dips.append((e[j], Yh[j, np.argsort(Eh[j])[n]] / d['honeycomb_edge']))
dip = min(v for v, _ in dips)
check('ribbons (b): the level 0.37 dips to 0.35 near each edge, and nowhere below 0.34',
      round(dip, 2) == 0.35 and dip > 0.34 and len(dips) == 2 and all(abs(yy) > 0.4 for _, yy in dips),
      [(round(v, 4), round(yy, 2)) for v, yy in dips])
scan = [per_edge(Eh, Yh, mu, d['honeycomb_edge']) for mu in np.linspace(dip + 0.001, pos[1] - 0.001, 20)]
check('ribbons (b): just below the level 0.37, three branches per edge with the net count one',
      all(s[:2] == (3, 3) and abs(s[2]) == 1 and s[2] == -s[3] for s in scan), set(scan))

# the text of the widget landaufan, corrected on 2026-11-22: its dashed lines are -4t + (n + 1/2) hbar omega_c, measured
# from the bottom of the band at -4t, and not (n + 1/2) hbar omega_c. First route, the code of the widget, which draws
# the dashed lines and the bands; second route, a Harper matrix of q sites written here, whose lowest level sits near
# -4t + hbar omega_c/2 for a small flux, and at zero flux the bottom of the band is -4t.
import importlib.util  # noqa: E402
spec = importlib.util.spec_from_file_location('landaufan', os.path.join(HERE, '..', '..', 'widgets', 'defs', 'landaufan.py'))
lf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lf)
widget = {}
for q in (16, 40):
    series = lf.compute(dict(q=q))['panels'][0]['series']
    dashed = [s['y'][0] for s in series if s['kind'] == 'dash']
    bands = [float(np.mean(s['y'])) for s in series if s['kind'] == 'line']
    wq = 4 * np.pi / q
    hq = np.diag(-2 * np.cos(2 * np.pi * np.arange(q) / q + 0.3)) - np.eye(q, k=1) - np.eye(q, k=-1)
    hq[0, -1] = hq[-1, 0] = -1.0
    widget[q] = (np.allclose(dashed, [-4 + wq * (n + 0.5) for n in range(len(dashed))], atol=1e-12),
                 abs(bands[0] - (-4 + wq / 2)) / wq, abs(np.linalg.eigvalsh(hq)[0] - (-4 + wq / 2)) / wq)
bottom =min(-2 * np.cos(kx) - 2 * np.cos(ky) for kx in np.linspace(-np.pi, np.pi, 41) for ky in np.linspace(-np.pi, np.pi, 41))
check('widget: the dashed lines are -4t + (n + 1/2) hbar omega_c, the lowest band is within 5 percent of a spacing of the '
      'first line for q = 16 and 40 by the widget and by a Harper matrix, and the band bottom at zero flux is -4t',
      all(v[0] and v[1] < 0.05 and v[2] < 0.05 for v in widget.values()) and abs(bottom + 4) < 1e-12,
      {q: (v[0], round(v[1], 4), round(v[2], 4)) for q, v in widget.items()})

# ---------------------------------------------------------------- the width of the notebook, decided on 2026-11-22
# "for example with the width N = 30 of its Core cells": the two Core cells of the notebook box of Section 4.10 that
# build the ribbons in a field, "Landau levels of conventional electrons" and "Landau levels of the Dirac equation", set
# N = 30 and pass it to square_ribbon and to honeycomb_armchair_ribbon. The square ribbon of 30 is 30 sites across and
# the armchair ribbon of 30 has 60 rows of sites, so the page gives the width parameter and not a number of sites.
import json  # noqa: E402
import re    # noqa: E402
nb = json.load(open(os.path.join(HERE, '..', '..', '..', 'jupyter-notebooks', 'session4.ipynb'), encoding='utf-8'))
cells, title = {}, None
for c in nb['cells']:
    src = ''.join(c['source'])
    if c['cell_type'] == 'markdown':
        m = re.search(r'^#+\s*(.*)', src, re.M)
        title = m.group(1) if m else title
    elif title is not None:
        cells.setdefault(title, src)
core = {name: next(v for k, v in cells.items() if k.startswith(name)) for name in
        ('Landau levels of conventional electrons', 'Landau levels of the Dirac equation')}
page11 = open(os.path.join(HERE, '..', '..', 'pages', 'session04',
                           '11-numerical-check-of-the-landau-levels-and-edge-states-on-the-lattice.md'), encoding='utf-8').read()
box10 = open(os.path.join(HERE, '..', '..', 'pages', 'session04', '10-landau-levels-of-dirac-electrons.md'),
             encoding='utf-8').read().split('::: notebookbox', 1)[1].split('\n:::', 1)[0]
rows = {name: len(set(np.round(g.r[:, 1], 6))) for name, g in         # the geometry of pyqula writes no file
        (('square', geometry.square_ribbon(30)), ('armchair', geometry.honeycomb_armchair_ribbon(30)))}
check('decided on 2026-11-22, the width: the Core cells "Landau levels of conventional electrons" and "Landau levels of the '
      'Dirac equation", named in the notebook box of Section 4.10, set N = 30 for square_ribbon and '
      'honeycomb_armchair_ribbon, which are 30 and 60 rows of sites across',
      all(re.search(r'^N = 30\b', v, re.M) for v in core.values())
      and 'square_ribbon(N)' in core['Landau levels of conventional electrons']
      and 'honeycomb_armchair_ribbon(N)' in core['Landau levels of the Dirac equation']
      and all(f'"{k}" (Core)' in box10 for k in core) and rows == {'square': 30, 'armchair': 60}
      and 'for example with the width `N = 30` of its Core cells' in page11, rows)
print('all checks of page 11 hold')
