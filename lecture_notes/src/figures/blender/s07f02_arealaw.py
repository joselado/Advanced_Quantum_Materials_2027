"""Figure s07f02, fig:s07:arealaw: the entropy counts the boundary, seen from above.

(a) The dimerized chain of 14 sites, dimers (0,1), (2,3), ..., the strong bonds thick. Behind, the
block A = sites 1 to 6, with two interior dimers; in front, A = sites 1 to 12, with five. In both,
A cuts the two dimers (0,1) and (6,7) or (12,13), drawn in the broken color: 2 cut singlets each.
(b) A square lattice of tetramers, 2 by 2 clusters with strong bonds. Left, A is a 2 by 2 block of
sites shifted by one site from the cluster grid; right, a 4 by 4 block, twice the linear size. The
cut bonds, inside clusters and across the boundary of A, are in the broken color, and counted here.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's07f02_arealaw'
S = 0.55                               # lattice spacing in the scene


def rod(name, p, q, cut, strong):
    if cut:
        return F.rod(name, (*p, 0.04), (*q, 0.04), r=0.05, rgb=F.BROKEN)
    return F.rod(name, (*p, 0.04), (*q, 0.04), r=0.045 if strong else 0.015, rgb=F.SITE if strong else F.BOND)


def dimer_chain(y, a0, a1, tag):
    n = 14
    xs = [-7.1 + i * S for i in range(n)]
    cut = 0
    for i in range(n - 1):
        strong = i % 2 == 0
        is_cut = strong and ((a0 <= i <= a1) != (a0 <= i + 1 <= a1))
        cut += is_cut
        rod(f'{tag}_b{i}', (xs[i], y), (xs[i + 1], y), is_cut, strong)
    for i, x in enumerate(xs):
        F.site(f'{tag}_s{i}', (x, y, 0), r=0.11, h=0.04)
    xa, xb = xs[a0] - 0.3, xs[a1] + 0.3
    F.slab(f'{tag}_A', ((xa + xb) / 2, y, 0.01), (xb - xa, 0.6, 0.02), rgb=F.ACCENT_AQM, alpha=0.2)
    F.anchor('A', (xa, y + 0.32, 0))
    F.anchor('count', (xs[0] - 0.1, y - 0.3, 0))
    return cut


def tetramers(x0, y0, lo, hi, tag):
    n = 6
    pos = lambda i, j: (x0 + (i - (n - 1) / 2) * S, y0 + (j - (n - 1) / 2) * S)
    inA = lambda i, j: lo <= i <= hi and lo <= j <= hi
    cut = 0
    for i in range(n):
        for j in range(n):
            for di, dj in ((1, 0), (0, 1)):
                k, l = i + di, j + dj
                if k >= n or l >= n:
                    continue
                strong = (i // 2 == k // 2) and (j // 2 == l // 2)
                is_cut = strong and inA(i, j) != inA(k, l)
                cut += is_cut
                rod(f'{tag}_b{i}{j}{di}', pos(i, j), pos(k, l), is_cut, strong)
            F.site(f'{tag}_s{i}{j}', (*pos(i, j), 0), r=0.09, h=0.04)
    (xa, ya), (xb, yb) = pos(lo, lo), pos(hi, hi)
    F.slab(f'{tag}_A', ((xa + xb) / 2, (ya + yb) / 2, 0.01), (xb - xa + 0.4, yb - ya + 0.4, 0.02), rgb=F.ACCENT_AQM,
           alpha=0.2)
    F.anchor('A', (xa - 0.2, yb + 0.2, 0))
    F.anchor('count', (x0, y0 - (n / 2) * S - 0.15, 0))
    return cut


def build():
    F.studio(shadows=False)
    F.PREFIX[0] = 'as'
    c1 = dimer_chain(1.0, 1, 6, 'as')
    F.PREFIX[0] = 'al'
    c2 = dimer_chain(-0.4, 1, 12, 'al')
    F.PREFIX[0] = 'bs'
    c3 = tetramers(2.75, 0.3, 1, 2, 'bs')
    F.PREFIX[0] = 'bl'
    c4 = tetramers(6.35, 0.3, 1, 4, 'bl')
    F.PREFIX[0] = ''
    print('cut bonds', c1, c2, c3, c4)
    F.anchor('pa', (-7.1, 2.0, 0))
    F.anchor('pb', (1.1, 2.0, 0))
    F.axes_anchors('r', (0.55, -1.25, 0.0), {'x': (1.1, -1.25, 0.0), 'y': (0.55, -0.7, 0.0)})
    F.camera((0.6, 0.4, 0.0), elev=89.9, ortho=15.6, aspect=15.6 / 4.9)


F.main(build, NAME)
