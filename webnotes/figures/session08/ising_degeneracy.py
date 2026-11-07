"""Session 8, the number of classical ground states of the antiferromagnetic Ising model on small periodic clusters
of the square, triangular and kagome lattices, counted by enumerating all 2^N configurations."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
import style
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, so that they stay readable on a phone

def count(N, bonds):
    """Number of configurations with the lowest energy sum_<ij> s_i s_j."""
    emin, cnt = None, 0
    chunk = 1 << min(N, 22)
    for start in range(0, 1 << N, chunk):
        c = np.arange(start, start + chunk, dtype=np.int64)
        E = np.zeros(chunk, dtype=np.int16)
        for i, j in bonds:
            E += (1 - 2 * (((c >> i) ^ (c >> j)) & 1)).astype(np.int16)
        m = E.min()
        if emin is None or m < emin:
            emin, cnt = m, int((E == m).sum())
        elif m == emin:
            cnt += int((E == m).sum())
    return cnt

def torus(L1, L2, steps):
    idx = lambda x, y: (x % L1) + L1 * (y % L2)
    return L1 * L2, [(idx(x, y), idx(x + dx, y + dy)) for x in range(L1) for y in range(L2) for dx, dy in steps]

def kagome(n1, n2):
    """Three sites per cell, A at 0, B at a1/2, C at a2/2, the up triangle in the cell and the down one across cells."""
    idx = lambda x, y, s: 3 * ((x % n1) + n1 * (y % n2)) + s
    b = []
    for x in range(n1):
        for y in range(n2):
            A, B, C = idx(x, y, 0), idx(x, y, 1), idx(x, y, 2)
            b += [(A, B), (B, C), (C, A), (B, idx(x + 1, y, 0)), (C, idx(x, y + 1, 0)), (B, idx(x + 1, y - 1, 2))]
    return 3 * n1 * n2, b

square = [count(*torus(a, b, ((1, 0), (0, 1)))) for a, b in ((4, 2), (4, 4), (4, 6))]
tri = [count(*torus(a, b, ((1, 0), (0, 1), (1, -1)))) for a, b in ((3, 3), (3, 4), (4, 4), (3, 6), (4, 5), (6, 4))]
kag = [count(*kagome(a, b)) for a, b in ((2, 2), (2, 3), (2, 4))]
Nsq, Ntri, Nkag = [8, 16, 24], [9, 12, 16, 18, 20, 24], [12, 18, 24]
assert square == [2, 2, 2]                      # bipartite, only the two Neel states
s_tri = 2 / np.pi * quad(lambda w: np.log(2 * np.cos(w)), 0, np.pi / 3)[0]     # 0.323 per site, the infinite lattice
assert abs(np.log(tri[-1]) / 24 - s_tri) < 0.02 and abs(np.log(kag[-1]) / 24 - 0.502) < 0.01

fig, ax = style.figure(height_cm=6.4, width_cm=12.0)
n = np.linspace(0, 26, 50)
ax.plot(n, s_tri * n, color=style.GRID, lw=1.2, ls=(0, (3, 3)), zorder=0)
ax.plot(n, 0.502 * n, color=style.GRID, lw=1.2, ls=(0, (3, 3)), zorder=0)
ax.plot(Nkag, np.log(kag), 'o', ms=4.5, color=style.BROKEN, zorder=3)
ax.plot(Ntri, np.log(tri), 's', ms=4, color=style.ACCENT, zorder=3)
ax.plot(Nsq, np.log(square), 'D', ms=4, color=style.MUTED, zorder=3)
ax.set_xlim(0, 26.5); ax.set_ylim(0, 13.5)
style.arrows(ax, xlabel=r'$N$', ylabel=r'$\ln$ of the number of ground states')
ax.set_xticks([8, 16, 24]); ax.set_yticks([np.log(2), 5, 10]); ax.set_yticklabels([r'$\ln 2$', '5', '10'])
ax.tick_params(length=2.5, pad=2, labelsize=11)
style.label(ax, 22.8, 13.0, 'kagome', ha='right', fontsize=11, color=style.BROKEN)
style.label(ax, 25.8, 6.0, 'triangular', ha='right', fontsize=11, color=style.ACCENT)
style.label(ax, 25.8, 1.55, 'square', ha='right', fontsize=11, color=style.MUTED)
style.label(ax, 11.0, 6.9, r'$0.50\,N$', ha='right', fontsize=11, color=style.MUTED)
style.label(ax, 13.5, 3.0, r'$0.32\,N$', ha='left', fontsize=11, color=style.MUTED)
style.save(fig, __file__)
