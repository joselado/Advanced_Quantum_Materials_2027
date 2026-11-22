"""Session 8, the numbers that page 13 (Section 8.13) states and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold, a solution or a lab box is an
assert, here or in the figure script that draws it. The figures of the page assert their own numbers: kondo_bdg.py the
gap 0.33 and 2 Delta = 1, hybrid_gap.py the direct gaps 1 and 2, g4_kondo_lattice_bands.py the gaps of the notebook
model, and _g4_kondo.py the bands of the chain and the Fermi level of the three quiz pictures. This script holds the
key box, the fold, the problem, the counts of the quizzes and the f occupation of the notebook model, and it computes
again with pyqula the numbers of the captions that otherwise only the figure scripts assert, since --verify runs only
this folder: the gaps 0.028 and 0.111 and the direct gaps 0.5 and 1.0 of the notebook model on its mesh of 90, the
sign t = -1 of pyqula's hopping and the sign of JK, the direct gaps 1 and 2 of hybrid_gap and 2 Delta = 1 of
kondo_bdg. It finds the repository from its own path, runs pyqula in a temporary folder and writes no file."""
import os
import sys
import tempfile

import numpy as np
from scipy.optimize import brentq

sys.dont_write_bytecode = True


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def Epm(eps, g):
    r = np.sqrt(eps ** 2 + 4 * g ** 2)
    return (eps - r) / 2, (eps + r) / 2


# the key box and the fold: the eigenvalues of [[eps, -gamma], [-gamma, 0]], trace eps and determinant -gamma^2
rng = np.random.default_rng(3)
err, sign_ok = 0.0, True
for eps, g in zip(rng.uniform(-6, 6, 200), rng.uniform(-2, 2, 200)):
    H = np.array([[eps, -g], [-g, 0.0]])
    lo, up = Epm(eps, g)
    err = max(err, np.abs(np.linalg.eigvalsh(H) - [lo, up]).max())
    sign_ok &= lo < 0 < up and abs(np.trace(H) - eps) < 1e-12 and abs(np.linalg.det(H) + g ** 2) < 1e-9
check('E_+- = (eps +- sqrt(eps^2 + 4 gamma^2))/2 are the levels, and E_- < 0 < E_+', err < 1e-12 and sign_ok, err)
check('the sign of gamma_K does not change the levels', np.allclose(np.linalg.eigvalsh([[1.3, 0.6], [0.6, 0]]),
      np.linalg.eigvalsh([[1.3, -0.6], [-0.6, 0]])), 0)
for g in (0.25, 0.5, 0.6, 1.0):
    lo, up = Epm(0.0, g)
    check('at eps = 0 the levels are -+gamma_K and the direct gap is 2 gamma_K, gamma_K = %g' % g,
          abs(lo + g) < 1e-12 and abs(up - g) < 1e-12, (lo, up))
e_grid = np.linspace(-6, 6, 2001)
lo, up = Epm(e_grid, 0.6)
check('E_- and E_+ both grow with eps', np.all(np.diff(lo) > 0) and np.all(np.diff(up) > 0), 0)
check('the direct gap at fixed eps is smallest at eps = 0', abs(e_grid[np.argmin(up - lo)]) < 1e-12, 0)

# the chain eps = -2t cos k: top of the lower band at k = pi, bottom of the upper band at k = 0
t = 1.0
k = np.linspace(-np.pi, np.pi, 40001)
eps = -2 * t * np.cos(k)
for g in (0.1, 0.5, 0.6):
    lo, up = Epm(eps, g)
    ind = up.min() - lo.max()
    exact = 2 * (np.sqrt(t ** 2 + g ** 2) - t)
    check('chain, gamma_K = %g: the indirect gap is 2(sqrt(t^2+gamma^2)-t) = %.4f, top at k = pi and bottom at k = 0'
          % (g, exact), abs(ind - exact) < 1e-12 and abs(abs(k[np.argmax(lo)]) - np.pi) < 1e-12 and abs(k[np.argmin(up)]) < 1e-12, round(ind, 5))
exact = 2 * (np.sqrt(1.36) - 1)
check('the problem: 2(sqrt(1.36)-1) = 0.33, against gamma^2/t = 0.36', abs(round(exact, 2) - 0.33) < 1e-12
      and abs(0.6 ** 2 - 0.36) < 1e-12, round(exact, 4))
check('gamma^2/t is within 10 percent of the gap up to gamma_K = 0.6 t',
      all(abs(g ** 2 / (2 * (np.sqrt(1 + g ** 2) - 1)) - 1) < 0.1 for g in np.linspace(0.01, 0.6, 60)),
      round(0.36 / exact - 1, 4))
check('the problem: 0.36 is 8 percent above 0.33', abs(round(100 * (0.36 / exact - 1)) - 8) < 1e-12, round(100 * (0.36 / exact - 1), 2))
check('the problem: the direct gap 2 gamma_K = 1.2 is about 3.6 times the indirect gap',
      abs(2 * 0.6 - 1.2) < 1e-12 and abs(round(1.2 / exact, 1) - 3.6) < 1e-12, round(1.2 / exact, 3))
check('and not at gamma_K = t, where the gap is 0.83', abs(1 / (2 * (np.sqrt(2) - 1)) - 1) > 0.1 and abs(2 * (np.sqrt(2) - 1) - 0.83) < 5e-3,
      round(2 * (np.sqrt(2) - 1), 4))

# the count of the particles, on the chain with 4000 momenta: a half-filled c band gives one half per k and spin, and
# the full lower band at gamma_K = 0.6 holds one half of a c electron and one half of an f fermion per k and spin
kc = 2 * np.pi * (np.arange(4000) + 0.5) / 4000
ec = -2 * np.cos(kc)
cw, fw, cboth, fboth = [], [], [], []
for e_ in ec:
    w, v = np.linalg.eigh(np.array([[e_, -0.6], [-0.6, 0.0]]))
    cw.append(abs(v[0, 0]) ** 2)
    fw.append(abs(v[1, 0]) ** 2)
    cboth.append(np.sum(abs(v[0, :]) ** 2))                     # c weight of the two bands together
    fboth.append(np.sum(abs(v[1, :]) ** 2))
check('a half-filled c band, gamma_K = 0, holds one half per k and spin', abs(np.mean(ec < 0) - 0.5) < 1e-12, np.mean(ec < 0))
check('chain, gamma_K = 0.6: the lower band holds 0.500 f fermions per spin', abs(np.mean(fw) - 0.5) < 1e-9, round(np.mean(fw), 6))
check('the lower band holds one half of c and one half of f, one particle per k and spin',
      abs(np.mean(cw) - 0.5) < 1e-9 and abs(np.mean(cw) + np.mean(fw) - 1) < 1e-12, round(np.mean(cw) + np.mean(fw), 12))
check('both bands full give 2 per k and spin, a full c band (2 per site) and 2 f fermions per site',
      np.allclose(cboth, 1) and np.allclose(fboth, 1) and abs(2 * np.mean(cboth) - 2) < 1e-12 and abs(2 * np.mean(fboth) - 2) < 1e-12,
      (2 * np.mean(cboth), 2 * np.mean(fboth)))
# the first picture of the quiz: gamma_K = 0 with one particle per k and spin, so the c band holds one half and the flat
# f level at the Fermi level holds the other half, which is half filled
check('gamma_K = 0, one particle per k and spin: c holds 0.5 and the f level 1 - 0.5 = 0.5', abs(1 - np.mean(ec < 0) - 0.5) < 1e-12,
      1 - np.mean(ec < 0))

# the quiz pictures: with 0.6 particles per k and spin the Fermi level is E_-(-2 cos 0.6 pi), inside the lower band
ef = Epm(-2 * np.cos(0.6 * np.pi), 0.6)[0]
lo, up = Epm(eps, 0.6)
check('0.6 particles per k and spin: the Fermi level %.3f is below the top %.3f of the lower band' % (ef, lo.max()),
      lo.min() < ef < lo.max() and abs(np.mean(lo < ef) - 0.6) < 1e-3, round(np.mean(lo < ef), 4))
check('the quiz says that the Fermi level cuts the lower band at -0.37 t', abs(round(ef, 2) + 0.37) < 1e-12, round(ef, 4))
check('the quiz says that the gap of the insulator picture is 0.33 t', abs(round(lo.max() * -2, 2) - 0.33) < 1e-12, round(-2 * lo.max(), 4))
check('with gamma_K = 0 the c band crosses zero at k = +-pi/2', np.allclose(-2 * np.cos([np.pi / 2, -np.pi / 2]), 0), 0)

# the caption of g4_kondo_lattice_bands: pyqula's triangular hopping +1 is t = -1 in the sign of (8.18), since -t times
# 2[cos 2pi k1 + cos 2pi k2 + cos 2pi(k1+k2)] is +6 at Gamma and -3 at K only for t = -1
os.chdir(tempfile.mkdtemp())
from pyqula import geometry  # noqa: E402
from pyqula.specialhamiltonian import H2HFH  # noqa: E402
h0k = geometry.triangular_lattice().get_hamiltonian().get_hk_gen()
tsign = -1.0
rng = np.random.default_rng(5)
bad = 0.0
for q1, q2 in [(0, 0), (1 / 3, 1 / 3), (0.5, 0)] + [tuple(x) for x in rng.uniform(0, 1, (20, 2))]:
    form = -tsign * 2 * (np.cos(2 * np.pi * q1) + np.cos(2 * np.pi * q2) + np.cos(2 * np.pi * (q1 + q2)))
    bad = max(bad, np.abs(np.linalg.eigvalsh(h0k([q1, q2, 0.])) - form).max())
check('the triangular band of pyqula is -t 2[cos + cos + cos] with t = -1, +6 at Gamma and -3 at K', bad < 1e-12
      and np.allclose(np.linalg.eigvalsh(h0k([0, 0, 0])), 6) and np.allclose(np.linalg.eigvalsh(h0k([1 / 3, 1 / 3, 0])), -3), bad)
# H2HFH puts +JK between c and f, while (8.21) has -gamma_K, so JK = -gamma_K, and the bands are the same (f -> -f)
hc = H2HFH(geometry.chain().get_hamiltonian(tij=[-1.]), JK=0.6).get_hk_gen()([0.25, 0., 0.])
check('H2HFH on the chain, JK = 0.6, k = pi/2: the c-f entry is +0.6 = -gamma_K, and the levels are those of -gamma_K',
      np.allclose(hc[0, 2], 0.6) and np.allclose(hc[1, 3], 0.6) and np.allclose(np.linalg.eigvalsh(hc), [-0.6, -0.6, 0.6, 0.6]),
      np.real(hc[0, 2]))
# the direct gaps 1 and 2 of hybrid_gap, at the crossing k = pi/2 of the chain for JK = 0.5 and 1
for JK in (0.5, 1.0):
    lv = np.linalg.eigvalsh(H2HFH(geometry.chain().get_hamiltonian(tij=[-1.]), JK=JK).get_hk_gen()([0.25, 0., 0.]))
    check('hybrid_gap: the direct gap at the crossing is %g for JK = %g' % (2 * JK, JK), abs(lv[2] - lv[1] - 2 * JK) < 1e-12, lv[2] - lv[1])
# the gap 2 Delta = 1 of kondo_bdg, with add_swave(0.5) on the chain and 400 momenta
hs = geometry.chain().get_hamiltonian(tij=[-1.])
hs.add_swave(0.5)
hsk = hs.get_hk_gen()
es = np.array([np.linalg.eigvalsh(hsk([q, 0., 0.])) for q in np.arange(400) / 400])
nb = es.shape[1] // 2
check('kondo_bdg: add_swave(0.5) on the chain gives the gap 2 Delta = 1', abs(es[:, nb].min() - es[:, nb - 1].max() - 1) < 1e-9,
      round(es[:, nb].min() - es[:, nb - 1].max(), 6))

# the notebook model, triangular lattice, add_onsite(-2.0), on a mesh of 90 per side that holds Gamma and K: the f
# occupation with the states below zero filled, the indirect gaps 0.028 and 0.111, and the direct gaps 2 JK
ks = np.arange(90) / 90
check('the mesh of 90 per side holds Gamma and K', np.any(np.isclose(ks, 0)) and np.any(np.isclose(ks, 1 / 3)), 90 % 3)
for JK, want, gap_want in ((0.25, 0.46, 0.028), (0.5, 0.48, 0.111)):
    h = geometry.triangular_lattice().get_hamiltonian()
    h.add_onsite(-2.0)
    h = H2HFH(h, JK=JK)
    hk = h.get_hk_gen()
    nf_site, below, top, bottom = 0.0, 0, -np.inf, np.inf
    for k1 in ks:
        for k2 in ks:
            w, v = np.linalg.eigh(hk([k1, k2, 0.]))
            occ = v[:, w < 0]
            below += occ.shape[1]
            nf_site += np.sum(np.abs(occ[2:]) ** 2)
            top, bottom = max(top, w[1]), min(bottom, w[2])
    nf_site /= len(ks) ** 2
    check('notebook model, JK = %g: two of the four bands below zero, and %.2f f fermions per site there' % (JK, want),
          below == 2 * len(ks) ** 2 and abs(nf_site - want) < 5e-3, round(nf_site, 4))
    check('notebook model, JK = %g: the indirect gap on the mesh is %.3f, with zero inside it' % (JK, gap_want),
          abs(bottom - top - gap_want) < 5e-4 and top < 0 < bottom, round(bottom - top, 5))
    # the direct gap at the crossing, on the line from Gamma to K where the conduction band is zero
    s0 = brentq(lambda s: 2 * (2 * np.cos(2 * np.pi * s / 3) + np.cos(4 * np.pi * s / 3)) - 2, 0, 1)
    lv = np.linalg.eigvalsh(hk([s0 / 3, s0 / 3, 0.]))
    check('notebook model, JK = %g: the direct gap at the crossing is %.1f' % (JK, 2 * JK), abs(lv[2] - lv[1] - 2 * JK) < 1e-9,
          round(lv[2] - lv[1], 9))
band = np.array([2 * (np.cos(2 * np.pi * a) + np.cos(2 * np.pi * b) + np.cos(2 * np.pi * (a + b))) - 2.0
                 for a in ks for b in ks])
check('the conduction band of the notebook runs from -5 to 4', abs(band.min() + 5) < 1e-9 and abs(band.max() - 4) < 1e-9,
      (band.min(), band.max()))

# corrected and decided on 2026-11-22, old text of the page
# the first quiz picture: with gamma_K = 0 the flat f level is at the Fermi level zero, drawn behind the dashed line and
# not under it, and it holds the other half of the one particle per k and spin (asserted above and in _g4_kondo.py)
lv0 = np.linalg.eigvalsh(np.array([[-2 * np.cos(0.3), 0.0], [0.0, 0.0]]))
check('corrected, alt text of the metal picture: with gamma_K = 0 the f level sits at the Fermi level E = 0', 0.0 in lv0, lv0)
# the try-it box of the cell "Spinon dispersion in the Kondo lattice", add_onsite(-4.0) and J = 0, 0.025, 0.05: with
# JK = 0.5 the gap between the second and the third band is open at J = 0 and gone at J = 0.025, and with JK = 1.0 it
# stays open at the three values of J. At J = 0 the gap is also computed from E_- and E_+ of the 2x2 matrix per spin.
exch = {}
for JK, J in ((0.5, 0.0), (0.5, 0.025), (1.0, 0.0), (1.0, 0.025), (1.0, 0.05)):
    h = geometry.triangular_lattice().get_hamiltonian()
    h.add_onsite(-4.0)
    h = H2HFH(h, JK=JK, J=J)
    hk = h.get_hk_gen()
    Ex = np.array([np.linalg.eigvalsh(hk([a, b, 0.])) for a in ks for b in ks])
    exch[(JK, J)] = Ex[:, 2].min() - Ex[:, 1].max()
eps4 = np.array([2 * (np.cos(2 * np.pi * a) + np.cos(2 * np.pi * b) + np.cos(2 * np.pi * (a + b))) - 4.0 for a in ks for b in ks])
closed = {JK: (0.5 * (eps4 + np.sqrt(eps4 ** 2 + 4 * JK ** 2))).min() - (0.5 * (eps4 - np.sqrt(eps4 ** 2 + 4 * JK ** 2))).max()
          for JK in (0.5, 1.0)}
check('decided, try-it of 8.13: with JK = 0.5 the gap is open at J = 0 and the bands overlap at J = 0.025, and with '
      'JK = 1.0 the gap stays open at J = 0, 0.025 and 0.05',
      exch[(0.5, 0.0)] > 0.1 and exch[(0.5, 0.025)] < -0.05 and all(exch[(1.0, J)] > 0.1 for J in (0.0, 0.025, 0.05))
      and abs(closed[0.5] - exch[(0.5, 0.0)]) < 1e-9 and abs(closed[1.0] - exch[(1.0, 0.0)]) < 1e-9,
      {k_: round(v_, 4) for k_, v_ in exch.items()})
# the text of 8.13 and the try-it boxes of 8.12 and 8.13 quote the values of the notebook cells, read here from the
# notebook: JK = 0, 0.25 and 0.5 with add_onsite(-2.0), which is gamma_K of (8.21), and J = 0, 0.025 and 0.05 with
# add_onsite(-4.0) and JK = 0.5
import json  # noqa: E402
nbk = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
                                  'jupyter-notebooks', 'session8.ipynb')))
code = [''.join(c_['source']) for c_ in nbk['cells'] if c_['cell_type'] == 'code']
cell_jk = [c_ for c_ in code if 'JKs = np.linspace(0.,.5,3)' in c_]
cell_j = [c_ for c_ in code if 'Js = np.linspace(0.,.05,3)' in c_]
check('decided, the notebook cells: JK = 0, 0.25, 0.5 with add_onsite(-2.0), and J = 0, 0.025, 0.05 with add_onsite(-4.0) '
      'and JK=0.5', len(cell_jk) == 1 and 'h.add_onsite(-2.0)' in cell_jk[0] and np.allclose(np.linspace(0., .5, 3), [0, 0.25, 0.5])
      and len(cell_j) == 1 and 'h.add_onsite(-4.0)' in cell_j[0] and 'JK=0.5,J=J' in cell_j[0]
      and np.allclose(np.linspace(0., .05, 3), [0, 0.025, 0.05]), 'ok')
print('all checks of page 13 hold')
