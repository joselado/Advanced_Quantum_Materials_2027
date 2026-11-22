"""Shared code of the picture options of the quiz of Section 5.10, the quasiparticle energy on one Fermi surface against the angle.

The Fermi surface is the one of the problem of the page, the square lattice with eps(k) = -2t (cos kx + cos ky) - mu at mu=-t,
which is the closed curve cos kx + cos ky = 1/2 around Gamma. For each angle theta around Gamma the Fermi momentum k_F(theta) is
the root of this equation along the ray, and on the Fermi surface eps=0, so E = |Delta(k_F)| by (5.9). The three pairings are
Delta=0 (a metal), a uniform Delta_0 (a full gap) and the d-wave Delta_0 (cos kx - cos ky) of (5.13) (four nodes at theta = pi/4,
3pi/4, 5pi/4 and 7pi/4, and 1.5 Delta_0 on the axes). This draws a formula on a lattice, so it is numpy, and the pictures have
their axes and no other text. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
import style

THETA = np.linspace(0, 2 * np.pi, 721)


def fermi_surface(mu=-1.0, t=1.0):
    """kx, ky of the Fermi surface along the rays of the angles THETA."""
    out = []
    for th in THETA:
        c, s = np.cos(th), np.sin(th)
        rmax = np.pi / max(abs(c), abs(s))
        r = brentq(lambda r: -2 * t * (np.cos(r * c) + np.cos(r * s)) - mu, 0, rmax)
        out.append((r * c, r * s))
    kx, ky = np.array(out).T
    assert np.allclose(-2 * t * (np.cos(kx) + np.cos(ky)) - mu, 0, atol=1e-9)
    return kx, ky


def energy(kind):
    """E/Delta_0 on the Fermi surface for the pairing kind, 'metal', 'swave' or 'dwave'."""
    kx, ky = fermi_surface()
    if kind == 'metal':
        return np.zeros_like(kx)
    if kind == 'swave':
        return np.ones_like(kx)
    E = np.abs(np.cos(kx) - np.cos(ky))
    z = THETA[1:][np.diff(np.sign(np.cos(kx) - np.cos(ky))) != 0]
    assert np.allclose(z, np.pi / 4 * np.array([1, 3, 5, 7]), atol=1e-2)    # four nodes, on the diagonals
    assert abs(E.max() - 1.5) < 1e-9 and abs(E[0] - 1.5) < 1e-9              # 1.5 Delta_0 on the axes
    k0 = np.arccos(0.25)
    assert abs(kx[90] - k0) < 1e-9 and abs(ky[90] - k0) < 1e-9 and abs(k0 - 1.318) < 1e-3   # the node (k0, k0) of the problem
    return E


def option(script, kind):
    """One picture option with its axes and no other text, the same window in the three pictures."""
    E = energy(kind)
    print(kind, 'E/Delta_0 on the Fermi surface from', round(E.min(), 4), 'to', round(E.max(), 4))
    plt.rcParams.update({'font.size': 11})
    fig, ax = plt.subplots(figsize=(3.7 * style.CM, 3.9 * style.CM))
    ax.plot(THETA, E, color=style.ACCENT, lw=1.8, clip_on=False, zorder=4)
    ax.set_xlim(0, 2 * np.pi); ax.set_ylim(-0.06, 1.7)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_position(('data', -0.06))
    ax.set_xticks([0, np.pi, 2 * np.pi]); ax.set_xticklabels(['0', r'$\pi$', r'$2\pi$'], fontsize=11)
    ax.set_yticks([0, 1]); ax.set_yticklabels(['0', '1'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$\theta$', fontsize=12, labelpad=0); ax.set_ylabel(r'$E/\Delta_0$', fontsize=12, labelpad=0)
    style.save(fig, script)
