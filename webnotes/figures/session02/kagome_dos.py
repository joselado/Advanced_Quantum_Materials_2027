"""Session 2, the bands and the density of states of the kagome lattice, H = -t sum over first neighbors.

The Bloch Hamiltonian has three orbitals per cell. The bands are computed along Gamma-K-M-Gamma, and the density
of states (2.16) is a histogram of the three bands on a uniform k-mesh of 600 x 600 points, with bins of
0.05 t. The flat band at +2t holds one third of the states and fills a single bin, which is cut in the plot.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

FS = 10.5
t = 1.0
a1, a2 = np.array([2.0, 0.0]), np.array([1.0, np.sqrt(3)])      # first-neighbor distance 1


def hk(k):
    """Bloch Hamiltonians for an array of k, shape (n, 3, 3)."""
    c1 = np.cos(k @ a1 / 2); c2 = np.cos(k @ a2 / 2); c3 = np.cos(k @ (a2 - a1) / 2)
    H = np.zeros((len(k), 3, 3))
    H[:, 0, 1] = H[:, 1, 0] = -2 * t * c1
    H[:, 0, 2] = H[:, 2, 0] = -2 * t * c2
    H[:, 1, 2] = H[:, 2, 1] = -2 * t * c3
    return H


# reciprocal vectors, b_i . a_j = 2 pi delta_ij
B = 2 * np.pi * np.linalg.inv(np.array([a1, a2])).T
n = 600
u = (np.arange(n) + 0.5) / n
U1, U2 = np.meshgrid(u, u)
kmesh = U1.reshape(-1, 1) * B[0] + U2.reshape(-1, 1) * B[1]
E = np.linalg.eigvalsh(hk(kmesh))
assert np.allclose(E[:, 2], 2 * t)                                # exactly flat, at the top
assert E[:, :2].min() > -4 * t - 1e-9 and E[:, 1].max() < 2 * t + 1e-9
bins = np.arange(-4.2, 2.25, 0.05)
hist, edges = np.histogram(E.ravel(), bins=bins, density=True)
centers = (edges[1:] + edges[:-1]) / 2
iflat = np.argmax(hist)
assert abs(centers[iflat] - 2 * t) < 0.05
frac = np.mean(np.isclose(E.ravel(), 2 * t))
assert abs(frac - 1 / 3) < 1e-3

G, K, M = np.zeros(2), (B[0] + B[1]) / 3 * np.array([1, 1]), B[0] / 2
K = (2 * B[0] + B[1]) / 3
nodes = [G, K, M, G]
ks, x, xt = [], [], [0.0]
for P, Q in zip(nodes[:-1], nodes[1:]):
    s = np.linspace(0, 1, 250)
    ks.append(P + s[:, None] * (Q - P)); x.append(xt[-1] + s * np.linalg.norm(Q - P))
    xt.append(xt[-1] + np.linalg.norm(Q - P))
Ep = np.linalg.eigvalsh(hk(np.vstack(ks))); x = np.concatenate(x)

fig = plt.figure(figsize=(12.5 * style.CM, 6.6 * style.CM))
gs = fig.add_gridspec(1, 2, width_ratios=[1.35, 1.0], wspace=0.08)
axb, axd = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
for j in range(3):
    axb.plot(x, Ep[:, j], color=style.BROKEN if j == 2 else style.ACCENT, lw=2.2 if j == 2 else 1.8)
for xv in xt:
    style.guide(axb, x=xv)
style.arrows(axb, ylabel=r'$\epsilon/t$', ticks=True)
axb.set_xticks(xt); axb.set_xticklabels([r'$\Gamma$', r'$K$', r'$M$', r'$\Gamma$'])
axb.set_yticks([-4, -2, 0, 2]); axb.tick_params(labelsize=FS, length=2.5)
axb.spines['left'].set_visible(True)
axb.set_xlim(0, xt[-1]); axb.set_ylim(-4.4, 2.9)
cut = 0.55
shown = np.minimum(hist, cut)
axd.fill_betweenx(centers, 0, shown, step='mid', color=style.LIGHT, lw=0)
axd.plot(shown, centers, color=style.ACCENT, lw=1.0, drawstyle='steps-mid')
axd.plot([0, cut], [centers[iflat]] * 2, color=style.BROKEN, lw=2.2)
style.arrows(axd, xlabel=r'$D(\epsilon)$')
axd.set_ylim(axb.get_ylim()); axd.set_xlim(0, cut * 1.02)
axd.annotate('flat band,\none third\nof the states', xy=(cut * 0.8, 2.0), xytext=(cut * 0.64, -2.95),
             fontsize=FS, color=style.BROKEN, ha='center', va='center', linespacing=1.15,
             arrowprops=dict(arrowstyle='-', color=style.BROKEN, lw=0.8))
style.save(fig, __file__)
