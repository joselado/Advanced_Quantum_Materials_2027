"""Shared code of the figures of Section 1.13 on the charge density wave of the chain (1.6), the plot
g4_cdw_meanfield.py and the three picture options g4_quiz_cdw_*.py of the quiz that asks which charges belong to
V = 3t. This file writes no figure.

The data come from the downloadable script webnotes/scripts/session01/g4_cdw_chain.py: the spinless chain with two
sites per cell and the first-neighbor hopping +1 of pyqula, at half filling, in the Hartree mean field alone
(compute_cross=False), which is the decoupling of the text of Section 1.13, on a mesh of 400 cells for the loop and
for the charges. The sign of the hopping changes no charge and no gap on this bipartite chain.

check(d) asserts the script against a second route, the gap equation of the Hartree charge density wave,
1 = V (1/pi) int_{-pi/2}^{pi/2} dk / sqrt(D^2 + 4 t^2 cos^2 k) with the staggered potential D = V dn, solved with
numpy, and it asserts every number that the caption of the plot and the feedback of the quiz state."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
import style

KK = np.linspace(-np.pi / 2, np.pi / 2, 200001)          # the reduced zone of the cell of two sites


def imbalance_of_V(V, t=1.0):
    """The Hartree imbalance dn of the infinite chain from the gap equation, 0 at V = 0."""
    if V == 0:
        return 0.0
    f = lambda D: V * np.trapezoid(1 / np.sqrt(D ** 2 + 4 * t ** 2 * np.cos(KK) ** 2), KK) / np.pi - 1
    return brentq(f, 1e-9, 2 * V) / V


def data():
    """The variables of the pyqula script, checked."""
    d = style.run_script('session01/g4_cdw_chain.py')
    check(d)
    return d


def check(d):
    Vs, dn, gap = np.array(d['Vs']), np.array(d['imbalance']), np.array(d['gap'])
    n = np.array(d['charges'])
    assert d['nk'] == 400                                                     # the mesh of 400 cells of the caption
    ref = np.array([imbalance_of_V(V) for V in Vs])
    assert np.all(np.abs(dn - ref) < 1e-3), np.c_[Vs, dn, ref]                 # pyqula and the gap equation
    assert np.allclose(n.sum(axis=1), 1, atol=1e-6)                           # one electron per cell
    assert np.allclose(np.abs(n[:, 0] - n[:, 1]), dn)
    assert np.all(np.abs(gap - 2 * Vs * dn) < 1e-3), np.c_[Vs, gap, 2 * Vs * dn]   # the gap is 2 V dn
    assert np.all(gap <= 2 * Vs + 1e-9) and np.all(np.diff(dn) > 0)           # below the line 2V, and growing
    i = {V: int(np.argmin(np.abs(Vs - V))) for V in (0.5, 1.0, 3.0)}
    # the numbers of the caption and of the quiz, two digits as quoted
    assert abs(dn[i[3.0]] - 0.892) < 1e-3 and abs(gap[i[3.0]] - 5.35) < 0.005
    assert abs(max(n[i[3.0]]) - 0.946) < 1e-3 and abs(min(n[i[3.0]]) - 0.054) < 1e-3
    assert abs(dn[i[1.0]] - 0.340) < 1e-3 and abs(gap[i[1.0]] - 0.68) < 0.005
    assert abs(max(n[i[1.0]]) - 0.67) < 0.005 and abs(min(n[i[1.0]]) - 0.33) < 0.005
    assert abs(dn[i[0.5]] - 0.030) < 1e-3 and abs(gap[i[0.5]] - 0.030) < 1e-3
    assert abs(max(n[i[0.5]]) - 0.515) < 1e-3 and abs(min(n[i[0.5]]) - 0.485) < 1e-3
    assert dn[0] < 1e-9 and gap[0] < 1e-9 and dn[-1] > 0.97                   # no order at V = 0, close to 1 at 6t
    # the alt text: the gap stays far below the line 2V at small V and approaches it at large V
    small, large = (Vs > 0) & (Vs <= 1.0), Vs >= 3.0
    assert np.all(gap[small] / (2 * Vs[small]) < 0.35) and np.all(gap[large] / (2 * Vs[large]) > 0.89)
    # the Hartree charge density wave is the antiferromagnet of (1.7) with U = 2V, 0.340, 0.769 and 0.892
    for V, m in ((1.0, 0.340), (2.0, 0.769), (3.0, 0.892)):
        assert abs(imbalance_of_V(V) - m) < 1e-3


def option(script, V):
    """One picture option, the charges <n_i> of six sites at the repulsion V, with the axes and no other text."""
    d = data()
    Vs, n = np.array(d['Vs']), np.array(d['charges'])
    cell = n[int(np.argmin(np.abs(Vs - V)))]
    assert abs(Vs[int(np.argmin(np.abs(Vs - V)))] - V) < 1e-12
    big, small = max(cell), min(cell)
    sites = np.arange(1, 7)
    q = np.array([big, small] * 3)                    # the larger charge drawn on the odd sites in every picture
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 3.6 * style.CM))
    ax.bar(sites, q, width=0.62, color=style.ACCENT, lw=0)
    ax.axhline(0.5, color=style.GRID, lw=0.9, zorder=0)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xlim(0.3, 6.7); ax.set_ylim(0, 1.05)
    ax.set_xticks([1, 3, 5]); ax.set_xticklabels(['1', '3', '5'], fontsize=11)
    ax.set_yticks([0, 0.5, 1]); ax.set_yticklabels(['0', '0.5', '1'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'site $i$', fontsize=12, labelpad=0); ax.set_ylabel(r'$\langle n_i\rangle$', fontsize=12, labelpad=1)
    style.save(fig, script)
