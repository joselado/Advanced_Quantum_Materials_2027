"""Session 5, braids of Majorana worldlines, the order of two exchanges that share a Majorana matters."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

def smooth(s):
    return 0.5 - 0.5 * np.cos(np.pi * s)

def draw_braid(ax, n, swaps, cols, names):
    """Worldlines for n strands, time going up. swaps is the list of i such that the strands at places i and i+1 are exchanged."""
    order = list(range(n))                      # order[place] = strand
    paths = {s: [] for s in range(n)}           # list of (x, y) segments per strand
    over = []                                   # (strand, segment) that runs over
    s_ = np.linspace(0, 1, 40)
    segs = []
    for step, i in enumerate(swaps):
        y = step + s_
        for place, strand in enumerate(order):
            if place == i:
                x = place + (1) * smooth(s_)
                segs.append((strand, x, y, True))       # moves to the right, runs over
            elif place == i + 1:
                x = place - (1) * smooth(s_)
                segs.append((strand, x, y, False))
            else:
                segs.append((strand, np.full_like(s_, place), y, False))
        order[i], order[i + 1] = order[i + 1], order[i]
    # the lines of the strands that do not run over, then the ones that do, with a white halo
    for strand, x, y, ov in segs:
        if not ov:
            ax.plot(x, y, color=cols[strand], lw=2.0, solid_capstyle='round', zorder=2)
    for strand, x, y, ov in segs:
        if ov:
            ax.plot(x, y, color='white', lw=5.0, solid_capstyle='butt', zorder=3)
            ax.plot(x, y, color=cols[strand], lw=2.0, solid_capstyle='round', zorder=4)
    for place in range(n):
        ax.plot([place], [0], 'o', color=cols[place], ms=4.5, zorder=5)
    # the final order
    for place, strand in enumerate(order):
        ax.plot([place], [len(swaps)], 'o', color=cols[strand], ms=4.5, zorder=5)
    return order

cols = [style.ACCENT, style.BROKEN, style.LIGHT, style.WARM]
fig, axs = plt.subplots(1, 3, figsize=(style.WIDTH_CM * style.CM, 5.6 * style.CM), gridspec_kw=dict(width_ratios=[3, 3, 4]))
panels = [(3, [0, 1], r'(a) $(1,2)$, then $(2,3)$'), (3, [1, 0], r'(b) $(2,3)$, then $(1,2)$'), (4, [0, 2], r'(c) $(1,2)$, then $(3,4)$')]
orders = []
for ax, (n, swaps, ttl) in zip(axs, panels):
    orders.append(draw_braid(ax, n, swaps, cols, None))
    ax.axis('off'); ax.set_xlim(-0.4, n - 0.6); ax.set_ylim(-0.45, len(swaps) + 0.75)
    style.label(ax, (n - 1) / 2, len(swaps) + 0.55, ttl, fontsize=8)
    for place in range(n):
        style.label(ax, place, -0.3, r'$\gamma_%d$' % (place + 1), fontsize=8, color=style.MUTED)
# the end result: (a) and (b) end in different arrangements, the disjoint exchanges of (c) give one arrangement in either order
assert orders[0] != orders[1]
# the algebra behind it, for the generators i gamma_a gamma_b of the exchanges, on four Majoranas built from two fermion modes
sx = np.array([[0, 1], [1, 0]], complex); sy = np.array([[0, -1j], [1j, 0]]); sz = np.diag([1.0, -1.0]).astype(complex); I2 = np.eye(2)
g = [np.kron(sx, I2), np.kron(sy, I2), np.kron(sz, sx), np.kron(sz, sy)]
for a in range(4):
    for b in range(4):
        assert np.allclose(g[a] @ g[b] + g[b] @ g[a], 2 * np.eye(4) * (a == b))
B = lambda a, b: 1j * g[a] @ g[b]
assert not np.allclose(B(0, 1) @ B(1, 2), B(1, 2) @ B(0, 1))      # (1,2) and (2,3) do not commute
assert np.allclose(B(0, 1) @ B(2, 3), B(2, 3) @ B(0, 1))          # (1,2) and (3,4) commute
style.save(fig, __file__)
