"""Shared code of the three picture options of the quiz of Section 5.13 on the nodal superconductor, the BdG bands
of the triangular lattice along Gamma, K, M, Gamma with no pairing, with s-wave and with nodal f-wave pairing.

The data come from the downloadable script webnotes/scripts/session05/g3_triangular_pairing_bands.py, the notebook cell
"Gapped and nodal superconducting orders": the triangular lattice with the hopping +1 of pyqula and the Fermi level at
zero, and add_pairing with mode="swave", delta=0 (no pairing), mode="swave", delta=0.4 and mode="nodal_fwave",
delta=0.2, where delta is the parameter of pyqula. The path has 300 steps on each segment, so the point (1/3, 0), two
thirds of the way from Gamma to M, where the Fermi surface crosses the line Gamma-M, is a step of the path. The checks
hold what the feedback of the quiz says. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

NODE = 700                         # the step (1/3, 0) of the segment M-Gamma


def check(d):
    """What the feedback says: the metal crosses zero on Gamma-K and on M-Gamma, the s-wave has 0.4 at the crossing
    of the Fermi surface, the f-wave a gap of about 0.9 on Gamma-K and zero at the crossing on M-Gamma."""
    kp = np.array(d['kpath'])
    assert len(kp) == 901 and np.allclose(kp[NODE], [1 / 3, 0, 0], atol=1e-12)
    assert [tuple(m) for m in d['modes']] == [('swave', 0.), ('swave', 0.4), ('nodal_fwave', 0.2)]
    metal, swave, fwave = (np.abs(np.array(e)) for e in d['energies'])
    gk, mg = slice(0, 300), slice(600, 901)
    # the metal: the bands eps and -eps cross zero where the Fermi surface crosses the path, on Gamma-K and on M-Gamma
    assert metal[gk].min() < 0.02 and metal[NODE].min() < 1e-12
    # the s-wave: 0.4 at the crossing on M-Gamma, which is on the Fermi surface, and at least 0.4 everywhere
    assert abs(swave[NODE].min() - 0.4) < 1e-12 and swave.min() > 0.4 - 1e-12
    # the f-wave: zero at the crossing on M-Gamma, where the pairing vanishes, and a gap above 0.9 on Gamma-K
    assert fwave[NODE].min() < 1e-12 and fwave[gk].min() > 0.9 and round(fwave[gk].min(), 2) == 0.91
    assert np.allclose(np.sort(np.array(d['energies'][2])[NODE]), np.sort(np.array(d['energies'][0])[NODE]), atol=1e-12)
    # the segment K-M stays far from zero in the three cases
    assert min(a[300:600].min() for a in (metal, swave, fwave)) > 1.9
    return kp


def option(script, d, i):
    """One picture option, the four BdG bands of one pairing, with the axes and no other text."""
    kp = check(d)
    B = 2 * np.pi * np.linalg.inv(np.array([[1., 0.], [-0.5, np.sqrt(3) / 2]])).T      # rows b1, b2 of the lattice of pyqula
    kc = kp[:, :2] @ B
    x = np.r_[0, np.cumsum(np.linalg.norm(np.diff(kc, axis=0), axis=1))]
    e = np.array(d['energies'][i])
    fs = 12
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 3.9 * style.CM))
    style.guide(ax, y=0)
    for xs in (x[300], x[600]):
        style.guide(ax, x=xs)
    for n in range(e.shape[1]):
        ax.plot(x, e[:, n], color=style.ACCENT, lw=1.6)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_linewidth(0.6)
    ax.set_xlim(0, x[-1]); ax.set_ylim(-1.6, 1.6)
    ax.set_xticks([0, x[300], x[600], x[-1]]); ax.set_xticklabels([r'$\Gamma$', '$K$', '$M$', r'$\Gamma$'], fontsize=fs - 1)
    ax.set_yticks([-1, 0, 1]); ax.set_yticklabels(['$-1$', '0', '1'], fontsize=fs - 1)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_ylabel(r'$E/t$', fontsize=fs, labelpad=1)
    ax.set_xlabel(r'$\mathbf{k}$', fontsize=fs, labelpad=0)
    style.save(fig, script)
