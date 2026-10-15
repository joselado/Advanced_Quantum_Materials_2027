"""figlib_s10.py: shapes used by the Session 10 figures, on top of figlib.py and figlib_s07.py.

Drawn in the xz plane (y = 0) and seen from the front: a network as columns of balls joined by thin
rods, a tile of pixels or spins, a small matrix, and a small bar spectrum.
"""
import figlib as F

NODE = F.ELECTRON


def net(tag, x0, z0, layers, w=2.0, h=1.4, r=0.09, y=0.0):
    """A fully connected network with the given widths, left to right, centered on (x0, z0)."""
    xs = [x0 - w / 2 + w * i / (len(layers) - 1) for i in range(len(layers))]
    pos = [[(x, y, z0 - h / 2 + h * (j + 0.5) / n) for j in range(n)] for x, n in zip(xs, layers)]
    for i in range(len(layers) - 1):
        for a in pos[i]:
            for b in pos[i + 1]:
                F.rod(f'{tag}_w{i}_{a[2]:.2f}_{b[2]:.2f}', a, b, r=0.008, rgb=F.BOND)
    for i, col in enumerate(pos):
        for j, p in enumerate(col):
            F.ball(f'{tag}_n{i}_{j}', p, r, rgb=F.ACCENT_AQM if i in (0, len(layers) - 1) else NODE)
    return pos


def tile(tag, x0, z0, vals, cell=0.18, rgb_on=None, rgb_off=(0.86, 0.87, 0.90), y=0.0, standing=True):
    """A grid of square cells, vals[row][col] in {0, 1} (or a gray level in [0, 1]), standing in the
    xz plane if `standing`, else lying in the xy plane."""
    rgb_on = F.ACCENT_AQM if rgb_on is None else rgb_on
    rows, cols = len(vals), len(vals[0])
    for i in range(rows):
        for j in range(cols):
            v = vals[i][j]
            rgb = tuple(o * v + f * (1 - v) for o, f in zip(rgb_on, rgb_off))
            x = x0 + (j - (cols - 1) / 2) * cell
            if standing:
                F.slab(f'{tag}_{i}_{j}', (x, y, z0 + ((rows - 1) / 2 - i) * cell), (cell * 0.92, 0.04, cell * 0.92), rgb=rgb,
                       radius=0.01)
            else:
                F.slab(f'{tag}_{i}_{j}', (x, y + ((rows - 1) / 2 - i) * cell, z0), (cell * 0.92, cell * 0.92, 0.04), rgb=rgb,
                       radius=0.01)


def bars(tag, x0, z0, heights, w=0.12, gap=0.05, rgb=None, y=0.0):
    rgb = F.ACCENT_AQM if rgb is None else rgb
    n = len(heights)
    for k, hgt in enumerate(heights):
        x = x0 + (k - (n - 1) / 2) * (w + gap)
        F.slab(f'{tag}_{k}', (x, y, z0 + hgt / 2), (w, 0.06, max(hgt, 0.02)), rgb=rgb, radius=0.008)
