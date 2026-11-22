"""Session 4, the statements and numbers that page 19 (Section 4.19, the Haldane model and the quantum Hall effect without Landau
levels) gives. One check script per page is the rule. The page has no figure of its own, since the panel of s03f05_masses is a
figure of the PDF of Session 3. This script checks the Chern numbers of the text and of the second quiz, C = +1 and -1 for the
two signs of the Haldane coupling and C = 0 for a staggered potential, each from h.get_chern() and from the link variables of
physcheck; that a filled Landau level of the honeycomb lattice and the Haldane model have the same Chern number, which is the
claim of the opener; that the Haldane model has no flux through its unit cell; and that on the path of the notebook cell
"Topological equivalence between the Quantum Hall state and a Chern insulator" no bulk state comes to zero energy, so the bulk
gap stays open, for the signs of the notebook, as the conventions sheet says. On the path of the text, where the field is
switched on and then the Haldane coupling off, it checks that the gap stays open and that one edge branch stays on each
edge, and it checks that the straight line of the notebook depends on the gauge, which the try-it box says. It finds the
repository from its own path and writes no file, since pyqula runs in a temporary folder.

The blocks marked "corrected on 2026-11-22" back the sentences of the old text that were corrected on that day, after
the lecturer chose to fix the errors of the old text. The block marked "decided on 2026-11-22" checks the first sentence of
the notebook box against the code cell of the notebook, rewritten that day by the rule of the coordinator."""
import os
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures'))
import physcheck as pc  # noqa: E402


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


os.chdir(tempfile.mkdtemp())
from pyqula import geometry  # noqa: E402

# the Chern numbers of the two gapped honeycomb lattices, with the sign of the Berry curvature of the notes
for x, want in ((0.1, 1), (-0.1, -1)):
    h = geometry.honeycomb_lattice().get_hamiltonian(has_spin=False)
    h.add_haldane(x)
    hk, B = pc.from_pyqula(h)
    Cl, Cq = pc.chern_links(hk, B, bands=0, nk=24), h.get_chern(nk=40)
    check('h.add_haldane(%+.1f) gives C = %+d, links and get_chern' % (x, want), abs(Cl - want) < 1e-6 and abs(Cq - want) < 1e-6,
          '%+.6f %+.6f' % (Cl, Cq))
h = geometry.honeycomb_lattice().get_hamiltonian(has_spin=False)
h.add_sublattice_imbalance(0.5)
hk, B = pc.from_pyqula(h)
Cl, Cq = pc.chern_links(hk, B, bands=0, nk=24), h.get_chern(nk=40)
check('a staggered potential 0.5 gives C = 0, links and get_chern', abs(Cl) < 1e-6 and abs(Cq) < 1e-6, '%+.6f %+.6f' % (Cl, Cq))

# no flux through the unit cell of the Haldane model: its Bloch Hamiltonian is periodic on the cell of two sites, while a field
# needs a magnetic cell with a whole number of flux quanta, as in the next check
h = geometry.honeycomb_lattice().get_hamiltonian(has_spin=False)
h.add_haldane(0.1)
hk, B = pc.from_pyqula(h)
k = np.array([0.31, -0.17])
check('the Haldane model, H(k + b) = H(k) on the cell of two sites', np.allclose(hk(k + B[0]), hk(k)) and np.allclose(hk(k + B[1]), hk(k)), 'yes')

# a filled Landau level of the honeycomb lattice and the Haldane model have the same Chern number, in the magnetic cell of the
# recipe "The Chern number of a Landau gap of the honeycomb lattice"
n = 20
g = geometry.honeycomb_lattice_square_cell().rotate(90).get_supercell((n, 1))
h = g.get_hamiltonian(has_spin=False)
h.add_orbital_magnetic_field(1 / (3 * np.sqrt(3) * n))
h.add_onsite(-0.25)
C_field = h.get_chern(nk=8)
h = g.get_hamiltonian(has_spin=False)
h.add_haldane(0.07)
C_haldane = h.get_chern(nk=8)
check('the gap above the zero level in a field and add_haldane(0.07) in the same cell, both C = +1',
      abs(C_field - 1) < 1e-3 and abs(C_haldane - 1) < 1e-3, '%+.4f %+.4f' % (C_field, C_haldane))

# the path of the notebook, from the Chern insulator to the quantum Hall state, keeps the bulk gap open
g = geometry.honeycomb_armchair_ribbon(20)
H_hall = g.get_hamiltonian(has_spin=False)
H_hall.add_orbital_magnetic_field(0.01)
H_hall.add_onsite(-0.2)
H_chern = g.get_hamiltonian(has_spin=False)
H_chern.add_haldane(0.07)
central = np.abs(g.y) < 0.5 * np.max(g.y)
closest = []
for nu in np.linspace(0., 1., 11):
    hk = (H_hall * nu + H_chern * (1 - nu)).get_hk_gen()
    e_min = 10.
    for kk in np.linspace(-0.5, 0.5, 41):
        e, v = np.linalg.eigh(np.array(hk([kk, 0., 0.])))
        bulk = np.sum(np.abs(v[central]) ** 2, axis=0) > 0.5
        e_min = min(e_min, np.min(np.abs(e[bulk])))
    closest.append(e_min)
check('on the path of the notebook no bulk state comes closer to zero energy than 0.198',
      min(closest) > 0.19 and abs(min(closest) - 0.198) < 0.0015, np.round(closest, 3))

# the path of the text, which the corrected sentence of 2026-11-22 names: we start in the Haldane model at zero field, we
# switch on the field and then we switch off the Haldane coupling, with the parameters of the notebook, add_haldane(0.07),
# the field 0.01 and the onsite energy -0.2 all along. The Haldane coupling is added first, so that the field puts its
# Peierls phase on every bond, also on the second neighbors, and a gauge change is then a unitary change of the whole
# Hamiltonian. The edge branches are followed one edge at a time: at each k, among the states inside the gap, |E| < 0.1,
# the one closest to zero energy with its mean y on the upper (lower) half, and a crossing is a change of its sign between
# two neighboring k.
k_edge = np.linspace(-0.5, 0.5, 201)


def path_step(field, t2):
    hs = g.get_hamiltonian(has_spin=False)
    if t2 != 0:
        hs.add_haldane(t2)
    if field != 0:
        hs.add_orbital_magnetic_field(field)
    hs.add_onsite(-0.2)
    hk = hs.get_hk_gen()
    e_min, e_up, e_low = 10., [], []
    for kk in k_edge:
        e, v = np.linalg.eigh(np.array(hk([kk, 0., 0.])))
        w = np.abs(v) ** 2
        e_min = min(e_min, np.min(np.abs(e[np.sum(w[central], axis=0) > 0.5])))
        ybar = w.T @ g.y
        for on, store in (((ybar > 0) & (np.abs(e) < 0.1), e_up), ((ybar < 0) & (np.abs(e) < 0.1), e_low)):
            store.append(e[on][np.argmin(np.abs(e[on]))] if np.any(on) else np.nan)
    slopes = []
    for store in (e_up, e_low):
        s = np.array(store)
        cross = np.nonzero(s[:-1] * s[1:] < 0)[0]          # a comparison with nan is False, so only states in the gap
        slopes.append(tuple(int(np.sign(s[i + 1] - s[i])) for i in cross))
    return e_min, tuple(slopes)


steps = [(f, 0.07) for f in np.linspace(0., 0.01, 6)] + [(0.01, t2) for t2 in np.linspace(0.07, 0., 6)[1:]]
two_step = [path_step(f, t2) for f, t2 in steps]
gaps = [r[0] for r in two_step]
check('path of the text: no bulk state closer to zero energy than 0.135 at zero field, 0.404 at full field, 0.198 at the end, '
      'and at every step one edge branch on each edge, rising on the upper edge and falling on the lower one',
      min(gaps) > 0.13 and abs(gaps[0] - 0.135) < 0.001 and abs(gaps[5] - 0.404) < 0.001 and abs(gaps[-1] - 0.198) < 0.001
      and all(r[1] == ((1,), (-1,)) for r in two_step), (np.round(gaps, 3), sorted(set(r[1] for r in two_step))))

# the notebook takes instead the straight line nu H_QH + (1 - nu) H_C, where only H_QH carries the Peierls phases, so the
# Hamiltonians in between are not a uniform field, and the line depends on the gauge of H_QH. Moving the ribbon of H_QH
# by 40 in y before the field is added changes the vector potential by a constant, a pure gauge change: the spectrum of
# H_QH alone is the same up to a shift of k by -0.01 * 3 * 40 = -1.2, so -0.2 of the zone, and its gap stays at 0.198.
# The straight line then closes the gap near nu = 0.5. This backs the sentence of the try-it box.
g_moved = geometry.honeycomb_armchair_ribbon(20)
g_moved.y = g_moved.y + 40.
g_moved.xyz2r()
H_moved = g_moved.get_hamiltonian(has_spin=False)
H_moved.add_orbital_magnetic_field(0.01)
H_moved.add_onsite(-0.2)
hk_a, hk_b = H_hall.get_hk_gen(), H_moved.get_hk_gen()
same = max(np.max(np.abs(np.linalg.eigvalsh(np.array(hk_b([kk, 0., 0.]))) - np.linalg.eigvalsh(np.array(hk_a([kk - 0.2, 0., 0.])))))
           for kk in (-0.37, 0.05, 0.31))
moved = []
for nu in (0.5, 1.0):
    hk = (H_moved * nu + H_chern * (1 - nu)).get_hk_gen()
    e_min = 10.
    for kk in np.linspace(-0.5, 0.5, 41):
        e, v = np.linalg.eigh(np.array(hk([kk, 0., 0.])))
        e_min = min(e_min, np.min(np.abs(e[np.sum(np.abs(v[central]) ** 2, axis=0) > 0.5])))
    moved.append(e_min)
check('the straight line depends on the gauge: with H_QH moved by 40 in y, the same spectrum shifted by -0.2 in k, a bulk '
      'state comes within 0.01 of zero energy at nu = 0.5, while nu = 1 keeps 0.198',
      same < 1e-9 and moved[0] < 0.01 and abs(moved[1] - closest[-1]) < 1e-6, (same, np.round(moved, 4)))

# the sentence of the path, corrected on 2026-11-22: the gap stays open "for the parameters of the notebook, where the
# field and the Haldane coupling give the same Chern number". With add_haldane(-0.07), which has C = -1 while the field
# with the zero of energy above the zero level has C = +1, a bulk state comes to zero energy on the way, so the condition
# is needed. The same path, with the same criterion of a bulk state.
H_minus = g.get_hamiltonian(has_spin=False)
H_minus.add_haldane(-0.07)
closest_minus = []
for nu in np.linspace(0., 1., 11):
    hk = (H_hall * nu + H_minus * (1 - nu)).get_hk_gen()
    e_min = 10.
    for kk in np.linspace(-0.5, 0.5, 41):
        e, v = np.linalg.eigh(np.array(hk([kk, 0., 0.])))
        bulk = np.sum(np.abs(v[central]) ** 2, axis=0) > 0.5
        e_min = min(e_min, np.min(np.abs(e[bulk])))
    closest_minus.append(e_min)
check('with add_haldane(-0.07), of the other Chern number, a bulk state comes within 0.03 of zero energy on the path',
      min(closest_minus) < 0.03, np.round(closest_minus, 3))

# the notebook box, corrected on 2026-11-22: the cell "Topological domains in the quantum Hall state" has no Haldane coupling.
# It is a square ribbon of 80 with the field 0.02 and the onsite energy +3.5 for y > 0 and -3.5 for the others. As two bulks,
# in the magnetic cell (1, 50) with the flux 1/50, the two halves have C = +2 and -2 by get_chern and by the link variables
# of physcheck, and the ribbon has |2 - (-2)| = 4 branches across zero energy at the wall and 2 at each outer edge.
chern_halves = {}
for c0 in (3.5, -3.5):
    hb = geometry.square_lattice().get_supercell((1, 50)).get_hamiltonian(has_spin=False)
    hb.add_orbital_magnetic_field(1 / 50)
    hb.add_onsite(c0)
    hkb, Bb = pc.from_pyqula(hb)
    nfill = int(np.sum(np.linalg.eigvalsh(hkb(np.zeros(2))) < 0))
    chern_halves[c0] = (round(hb.get_chern(nk=10), 6), round(pc.chern_links(hkb, Bb, bands=list(range(nfill)), nk=10), 6))
gd = geometry.square_ribbon(80)
gd.center()
hd = gd.get_hamiltonian(has_spin=False)
hd.add_orbital_magnetic_field(0.02)
hd.add_onsite(lambda r: 3.5 if r[1] > 0. else -3.5)
hkd, yd = hd.get_hk_gen(), gd.r[:, 1]
kd = np.linspace(-0.5, 0.5, 801)
Ed, Yd = [], []
for kk in kd:
    e, v = np.linalg.eigh(np.array(hkd([kk, 0., 0.])))
    Ed.append(e)
    Yd.append((np.abs(v) ** 2).T @ yd)
Ed, Yd = np.array(Ed), np.array(Yd)
where = []
for b in range(Ed.shape[1]):
    s = np.sign(Ed[:, b])
    where += [Yd[i, b] for i in np.nonzero(s[:-1] * s[1:] < 0)[0]]
where = np.array(where)
counts = (int(np.sum(np.abs(where) < 10)), int(np.sum(where > 30)), int(np.sum(where < -30)), len(where))
check('topological domains: the halves have C = +2 and -2, with 4 branches across zero energy at the wall and 2 at each edge',
      chern_halves[3.5] == (2.0, 2.0) and chern_halves[-3.5] == (-2.0, -2.0) and counts == (4, 2, 2, 8), (chern_halves, counts))
# ---------------------------------------------------------------- the notebook box, decided on 2026-11-22
# "Build the Haldane model and a quantum Hall ribbon, follow the straight line between the two Hamiltonians, and watch
# the bulk gap and the edge branches of the ribbon", rewritten to match the cell "Topological equivalence between the
# Quantum Hall state and a Chern insulator" by the rule of the coordinator. The code cell under that heading builds the
# two Hamiltonians on one armchair ribbon, takes H_hall*nu + H_chern*(1-nu), and plots the bands colored by the position,
# with no Chern number. The bulk gap along this line is the check above, no bulk state closer than 0.198.
import json  # noqa: E402
nb = json.load(open(os.path.join(HERE, '..', '..', '..', 'jupyter-notebooks', 'session4.ipynb'), encoding='utf-8'))
cells = nb['cells']
head = [i for i, c in enumerate(cells) if c['cell_type'] == 'markdown'
        and ''.join(c['source']).startswith('## Topological equivalence between the Quantum Hall state and a Chern insulator')]
code = ''.join(cells[head[0] + 1]['source']) if len(head) == 1 else ''
page = open(os.path.join(HERE, '..', '..', 'pages', 'session04',
                         '19-the-haldane-model-and-the-quantum-hall-effect-without-landau-levels.md'), encoding='utf-8').read()
box = page.split('::: notebookbox', 1)[1].split('\n:::', 1)[0]
check('decided on 2026-11-22, the notebook box: the cell builds a ribbon in a field and the Haldane model on the same ribbon, '
      'follows the straight line and plots the bands with the position, and computes no Chern number',
      cells[head[0] + 1]['cell_type'] == 'code' and 'honeycomb_armchair_ribbon' in code and 'H_hall.add_orbital_magnetic_field' in code
      and 'H_chern.add_haldane' in code and 'H = H_hall*nu + H_chern*(1-nu)' in code and 'operator="yposition"' in code
      and 'get_chern' not in code and 'Chern number' not in box.split('"topological domains"')[0]
      and 'follow the straight line between the two Hamiltonians' in box, 'cell %d' % (head[0] + 1))
print('all checks of page 19 hold')
