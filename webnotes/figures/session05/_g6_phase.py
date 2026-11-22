"""Shared code of the picture options of the quiz of Section 5.20, the pairing function on a Fermi pocket around Gamma.

The pocket is the Fermi surface of the square lattice with eps(k) = -2t (cos kx + cos ky) - mu at mu=-t, the closed curve
cos kx + cos ky = 1/2 around Gamma, which encloses filled states. At 16 points of it, every 22.5 degrees around Gamma, the
complex number Delta(k) is drawn as an arrow, centered on the point and scaled by the largest |Delta| on the pocket. The
three pairings are the s-wave Delta_0, the chiral p-wave Delta_0 (sin kx + i sin ky) of (5.15) and the d-wave
Delta_0 (cos kx - cos ky) of (5.13). The s-wave arrows do not turn, the p-wave arrows turn once around the pocket, and the
d-wave arrows are real, change sign four times and vanish on the diagonals, where the dots are. The pictures draw a formula,
so they are numpy, and they have their axes and no other text. The Chern numbers that the feedback states are asserted
in webnotes/checks/session05/g6_20_closing_summary.py. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
import style

MU = -1.0


def pocket(thetas, mu=MU, t=1.0):
    """kx, ky of the Fermi surface along the rays of the angles thetas around Gamma."""
    out = []
    for th in thetas:
        c, s = np.cos(th), np.sin(th)
        r = brentq(lambda r: -2 * t * (np.cos(r * c) + np.cos(r * s)) - mu, 0, np.pi / max(abs(c), abs(s)))
        out.append((r * c, r * s))
    kx, ky = np.array(out).T
    assert np.allclose(-2 * t * (np.cos(kx) + np.cos(ky)) - mu, 0, atol=1e-9)
    return kx, ky


def pairing(kind, kx, ky):
    """Delta(k)/Delta_0 for the pairing kind, 'swave', 'pwave' or 'dwave'."""
    if kind == 'swave':
        return np.ones_like(kx) + 0j
    if kind == 'pwave':
        return np.sin(kx) + 1j * np.sin(ky)
    return np.cos(kx) - np.cos(ky) + 0j


def winding(kind):
    """The winding number of the phase of Delta(k) once around the pocket, and the number of sign changes of a real one."""
    th = np.linspace(0, 2 * np.pi, 3601)
    d = pairing(kind, *pocket(th))
    if kind == 'dwave':
        assert np.abs(d.imag).max() == 0
        changes = int(np.sum(np.diff(np.sign(d.real)) != 0))
        return 0, changes
    w = np.sum(np.angle(d[1:] / d[:-1])) / (2 * np.pi)
    return int(round(w)), 0


def check(kind):
    w, changes = winding(kind)
    if kind == 'swave':
        assert w == 0
    if kind == 'pwave':
        assert w == 1                                               # p+ip winds once, counterclockwise
    if kind == 'dwave':
        assert changes == 4
        kd = np.arccos(0.25)                                        # the pocket crosses the diagonal at cos k = 1/4
        kx, ky = pocket([np.pi / 4])
        assert abs(kx[0] - kd) < 1e-9 and abs(ky[0] - kd) < 1e-9 and abs(pairing(kind, kx, ky)[0]) < 1e-9
    print(kind, 'winding', w, 'sign changes', changes)


def marks(kind):
    """The 16 points of the pocket, every 22.5 degrees from the kx axis, and the arrow of Delta(k) at each, scaled by the
    largest |Delta| on the pocket. A point where Delta vanishes is drawn as a dot and not as an arrow. The check of the
    page counts these, sixteen arrows for s and p, and twelve arrows and four dots on the diagonals for d."""
    th = np.linspace(0, 2 * np.pi, 400)
    fx, fy = pocket(th)
    th16 = 2 * np.pi * np.arange(16) / 16
    px, py = pocket(th16)
    a = 0.78 * pairing(kind, px, py) / np.abs(pairing(kind, fx, fy)).max()
    return th16, px, py, a


def option(script, kind):
    """One picture option, the arrows of Delta(k) on the pocket in the plane kx, ky, with the first zone dashed."""
    check(kind)
    th = np.linspace(0, 2 * np.pi, 400)
    fx, fy = pocket(th)
    _, px, py, a = marks(kind)
    plt.rcParams.update({'font.size': 11})
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 3.9 * style.CM))
    ax.set_aspect('equal')
    z = np.pi
    ax.plot([-z, z, z, -z, -z], [-z, -z, z, z, -z], color=style.MUTED, lw=0.8, ls=(0, (3, 2)))
    ax.plot(fx, fy, color=style.GRID, lw=1.4, zorder=1)
    for x, y, c in zip(px, py, a):
        if abs(c) < 1e-9:
            ax.plot(x, y, 'o', color=style.BROKEN, ms=3.6, zorder=4)
            continue
        ax.annotate('', xy=(x + c.real / 2, y + c.imag / 2), xytext=(x - c.real / 2, y - c.imag / 2),
                    arrowprops=dict(arrowstyle='-|>', color=style.ACCENT, lw=1.6, mutation_scale=8.5, shrinkA=0, shrinkB=0),
                    zorder=3)
    ax.set_xlim(-3.6, 3.6); ax.set_ylim(-3.6, 3.6)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_linewidth(0.6)
    ax.set_xticks([-z, 0, z]); ax.set_xticklabels([r'$-\pi$', '0', r'$\pi$'], fontsize=10)
    ax.set_yticks([-z, 0, z]); ax.set_yticklabels([r'$-\pi$', '0', r'$\pi$'], fontsize=10)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$k_x$', fontsize=12, labelpad=0); ax.set_ylabel(r'$k_y$', fontsize=12, labelpad=-3)
    style.save(fig, script)
