"""Session 4, section 4.11, the Landau levels and the edge states of two lattice ribbons in a field.

Both ribbons are finite along x and periodic along y, with the Peierls phases (4.4) of the Landau gauge A = (0, Bx), so k_y is a
good quantum number and fixes the guiding center. Panel (a) is a square lattice ribbon of 30 sites, hopping t=1 and the
flux phi=1/60 per plaquette, so B = 2 pi phi and l_B = 3.1 sites. The dashed lines are the continuum levels -4t + hbar omega_c (n+1/2)
with hbar omega_c = 4 pi phi t of Section 4.9. Panel (b) is an armchair ribbon of the honeycomb lattice, 40 rectangular cells wide,
with t=1, second-neighbor distance 1, bond length 1/sqrt(3) and B = 1/16, so l_B = 4. The two valleys project on k_y = 0 modulo
2 pi/sqrt(3), so the guiding center is x0 = (2 pi/sqrt(3) - k_y)/B and the left edge is on the right of the panel. The dashed lines are the Dirac levels
sgn(n) sqrt(|n|) E_1 of (4.7), with E_1 = v sqrt(2B) and v = sqrt(3) t / 2. In both panels the states with more than half of their
weight within 3 l_B of the left edge are blue, those near the right edge are red, and all the bands are drawn in grey."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, so that they stay readable on a phone

# (a) the square lattice ribbon
Ws, phi = 30, 1 / 60
Bs = 2 * np.pi * phi
xs = np.arange(Ws)


def h_square(ky):
    return np.diag(-2 * np.cos(ky - Bs * xs)) - np.eye(Ws, k=1) - np.eye(Ws, k=-1)


# (b) the armchair ribbon of the honeycomb lattice, rectangular cells of width 1 along x and period sqrt(3) along y
Nx, Bh = 40, 1 / 16
Ly = np.sqrt(3)
cell = np.array([[0, 0], [0, 1 / np.sqrt(3)], [0.5, np.sqrt(3) / 2], [0.5, np.sqrt(3) / 2 + 1 / np.sqrt(3)]])
pos = np.array([c + [i, 0] for i in range(Nx) for c in cell])
bonds = []                                      # (i, j, dy) with dy = y_i - y_j including the periodic image
for n in (-1, 0, 1):
    d = np.linalg.norm(pos[:, None] - (pos[None] + [0, n * Ly]), axis=-1)
    for i, j in zip(*np.where(np.abs(d - 1 / np.sqrt(3)) < 1e-9)):
        bonds.append((i, j, pos[i, 1] - pos[j, 1] - n * Ly))
print('honeycomb sites', len(pos), 'bonds per site', 2 * len(bonds) / len(pos) / 2)


def h_honey(ky):
    H = np.zeros((len(pos), len(pos)), complex)
    for i, j, dy in bonds:
        xm = 0.5 * (pos[i, 0] + pos[j, 0])
        H[i, j] += -np.exp(1j * (ky + Bh * xm) * dy)
    return H


def spectrum(hf, ks, x, lB):
    E, side = [], []
    L = x.max()
    for k in ks:
        e, v = np.linalg.eigh(hf(k))
        p = np.abs(v) ** 2
        E.append(e); side.append(p[x < 3 * lB].sum(0) - p[x > L - 3 * lB].sum(0))
    return np.array(E), np.array(side)


assert np.allclose(h_honey(0.3), h_honey(0.3).conj().T)
ksa = np.linspace(-0.8, np.pi + 0.8, 241)
Ea, sa = spectrum(h_square, ksa, xs.astype(float), 1 / np.sqrt(Bs))
# the valleys sit at k_y = 0 modulo 2 pi / sqrt(3), and the guiding center is x0 = (2 pi / sqrt(3) - k_y) / B
Ky = 2 * np.pi / Ly
ksb = np.linspace(Ky - Bh * (Nx - 0.5) - 0.8, Ky + 0.8, 241)
Eb, sb = spectrum(h_honey, ksb, pos[:, 0], 1 / np.sqrt(Bh))
wc = 4 * np.pi * phi; E1 = np.sqrt(3) / 2 * np.sqrt(2 * Bh)
mid = np.argmin(np.abs(ksa - np.pi / 2))
print('square, bulk levels at the middle', np.round(np.sort(Ea[mid])[:4], 3), 'continuum', np.round(-4 + wc * (np.arange(4) + 0.5), 3))
midb = np.argmin(np.abs(ksb - (Ky - Bh * Nx / 2)))
eb = Eb[midb]
print('honeycomb, bulk levels at the middle', np.round(np.sort(eb[np.abs(eb) < 0.75]), 3), 'Dirac', np.round(E1 * np.sqrt([0, 1, 2, 3]), 3))


def panel(ax, ks, E, side, guides, ylim, yt, ytl, name):
    keep = [j for j in range(E.shape[1]) if E[:, j].min() < ylim[1] + 0.3 and E[:, j].max() > ylim[0] - 0.3]
    Ek = np.vstack([E[:, keep], np.full((1, len(keep)), np.nan)])
    Ek[(Ek < ylim[0] - 0.2) | (Ek > ylim[1] + 0.2)] = np.nan
    ax.plot(np.tile(np.append(ks, np.nan), len(keep)), Ek.T.ravel(), color=style.GRID, lw=0.9, zorder=1)
    for g in guides:
        style.guide(ax, y=g, ls='--', color=style.MUTED, lw=0.8, zorder=0)
    inw = (E > ylim[0]) & (E < ylim[1])
    for sgn, col in ((1, style.ACCENT), (-1, style.BROKEN)):
        sel = inw & (sgn * side > 0.5)
        Es = np.where(sel, E, np.nan)[:, keep]                  # the edge parts of every band, as one path per color
        Es = np.vstack([Es, np.full((1, len(keep)), np.nan)])
        ax.plot(np.tile(np.append(ks, np.nan), len(keep)), Es.T.ravel(), color=col, lw=1.5, zorder=2)
    ax.set_xlim(ks[0], ks[-1]); ax.set_ylim(*ylim)
    style.arrows(ax, xlabel=r'$k_y$', ylabel=r'$E/t$')
    ax.set_yticks(yt); ax.set_yticklabels(ytl, fontsize=11); ax.tick_params(length=2.5, width=0.6)
    ax.text(0.5, -0.1, name, transform=ax.transAxes, ha='center', va='top', fontsize=11)


fig, axs = plt.subplots(1, 2, figsize=(12 * style.CM, 5.8 * style.CM), gridspec_kw=dict(wspace=0.38))
panel(axs[0], ksa, Ea, sa, -4 + wc * (np.arange(4) + 0.5), (-4.0, -3.15), [-4, -3.75, -3.5, -3.25], ['$-4$', '', '$-3.5$', ''], '(a) square lattice')
panel(axs[1], ksb, Eb, sb, E1 * np.array([-np.sqrt(2), -1, 0, 1, np.sqrt(2)]), (-0.48, 0.48), [-0.4, 0, 0.4], ['$-0.4$', '0', '$0.4$'], '(b) honeycomb lattice')
style.save(fig, __file__)
