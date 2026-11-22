"""Shared code of the picture options of the quiz of Section 9.4b, the Fermi surface of the square lattice at three fillings.

The calculation is the pyqula script webnotes/scripts/session09/g2_fermi_surface_square.py: eps(k) = -2t(cos kx + cos ky)
with t=1, and the spectral weight at the Fermi level from h.get_fermi_surface with delta=0.1, on a window from -2 pi to 2 pi
with both ends. The last row and column repeat the first ones, so they are dropped, and the window is then a period that
style.pyqula_kmap repeats. mu=0 gives the diamond |kx|+|ky|=pi (the right option), mu=-t the rounded square
cos kx + cos ky = 1/2, which reaches 2.09 along the axes and 1.86 along the diagonals, and mu=-3t the small circle of radius
k_F = 1.03. The checks below hold the numbers of the feedback. This file writes no figure, the scripts g2_quiz_fermi_*.py
call option."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from scipy.optimize import brentq
import style

VMAX = 6.0


def maps():
    d = style.run_script('session09/g2_fermi_surface_square.py')
    nk = d['nk']
    kx = d['kx'].reshape(nk, nk)[:-1, :-1]
    ky = d['ky'].reshape(nk, nk)[:-1, :-1]
    out = {}
    for mu, w in zip(d['mus'], d['maps']):
        out[mu] = w.reshape(nk, nk)[:-1, :-1]
    return d['g'], kx, ky, out


def checks(kx, ky, m):
    K1, K2 = 2 * np.pi * kx, 2 * np.pi * ky
    eps = -2 * (np.cos(K1) + np.cos(K2))
    for mu, W in m.items():
        top = W > 0.5 * W.max()
        assert np.abs(eps[top] - mu).max() < 0.1 + 1e-9, mu                  # the bright line is eps(k) = mu
    # mu = 0: the diamond, and the shift by Q = (pi, pi), 20 points of the mesh, maps it onto itself
    s = (kx.shape[0]) // 4
    assert np.isclose(kx[s, 0] - kx[0, 0], 0.5)
    W0, W1 = m[0.0], m[-1.0]
    assert np.allclose(np.roll(np.roll(W0, s, 0), s, 1), W0, rtol=1e-9)
    assert not np.allclose(np.roll(np.roll(W1, s, 0), s, 1), W1, rtol=0.1)
    inzone = (np.abs(K1) <= np.pi) & (np.abs(K2) <= np.pi)
    u = np.linspace(-np.pi, np.pi, 101)                                      # the diamond |kx| + |ky| = pi has eps = 0
    for sx, sy in ((1, 1), (1, -1)):
        assert np.abs(np.cos(u) + np.cos(sx * np.pi - sy * u)).max() < 1e-12
    top = (W0 > 0.5 * W0.max()) & inzone & (np.abs(np.abs(K1) - np.pi) > 0.6) & (np.abs(np.abs(K2) - np.pi) > 0.6)
    assert np.abs(np.abs(K1[top]) + np.abs(K2[top]) - np.pi).max() < 0.1      # away from the saddle points, on the mesh
    # mu = -t: the radii of the contour cos kx + cos ky = 1/2 along the axes and the diagonals
    ra, rd = np.arccos(-0.5), np.sqrt(2) * np.arccos(0.25)
    assert f'{ra:.2f}' == '2.09' and f'{rd:.2f}' == '1.86'
    # mu = -3t: the circle of radius k_F = 1.03 from the area, between 1.02 on the diagonal and 1.05 on the axes
    th = np.linspace(0, 2 * np.pi, 361)
    r = np.array([brentq(lambda r: -2 * (np.cos(r * np.cos(a)) + np.cos(r * np.sin(a))) + 3, 0, np.pi) for a in th])
    area = 0.5 * np.sum(r[:-1]**2 * np.diff(th))
    kF = np.sqrt(area / np.pi)
    assert f'{kF:.2f}' == '1.03' and abs(r.min() - 1.02) < 0.01 and abs(r.max() - 1.05) < 0.01, (kF, r.min(), r.max())
    top = (m[-3.0] > 0.5 * m[-3.0].max()) & inzone
    rr = np.hypot(K1[top], K2[top])
    assert rr.min() > 0.85 and rr.max() < 1.25, (rr.min(), rr.max())
    return kF


def option(script, mu):
    """One picture option with its axes and no other text, the same window and color scale in the three pictures."""
    g, kx, ky, m = maps()
    kF = checks(kx, ky, m)
    print(os.path.basename(script), 'mu =', mu, 'largest weight %.2f' % m[mu].max(), 'k_F at mu=-3t %.3f' % kF)
    style.plt.rcParams.update({'font.size': 11})
    cmap = LinearSegmentedColormap.from_list('aqm', ['white', style.LIGHT, style.ACCENT])
    fig, ax = style.plt.subplots(figsize=(4.4 * style.CM, 4.4 * style.CM))
    style.pyqula_kmap(ax, g, kx.ravel(), ky.ravel(), m[mu].ravel(), half=1.3 * np.pi, cmap=cmap, vmin=0, vmax=VMAX)
    style.kaxes(ax, fontsize=12)
    ax.set_xticks([-np.pi, 0, np.pi]); ax.set_yticks([-np.pi, 0, np.pi])
    ax.set_xticklabels([r'$-\pi$', '0', r'$\pi$'], fontsize=10.5); ax.set_yticklabels([r'$-\pi$', '0', r'$\pi$'], fontsize=10.5)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    style.save(fig, script)
