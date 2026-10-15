"""Figure s10f05, fig:s10:phaseclass: an easy and a hard phase-classification problem.

Seen from above at an angle. (a, b) Two 6 by 6 Ising snapshots as tiles, up raised and in the warm
color, down sunk and in the cold one: (a) all up with 4 spins flipped, m = +0.78; (b) a random
configuration with 19 up and 17 down, m = +0.06, redrawn until no row or column is fully polarized.
(c, d) Two Ising gauge snapshots on a 5 by 5 grid of vertices, the 40 bond spins as short rods of
two heights and colors: (c) sigma_vw = eps_v eps_w with random eps on the vertices, so every one of
the 16 plaquette products is +1, with one star (the four bonds at one vertex) highlighted, the gauge
flip that keeps every product; (d) the 40 bonds drawn independently at random, with the plaquettes
whose product is -1 marked by a cross. All from a fixed seed, checked in the script.
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's10f05_phaseclassification'
UP, DN = F.srgb(224, 62, 40), F.srgb(40, 92, 200)
XS = (-6.0, -2.1, 2.0, 6.0)
C = 0.48


def ising_tiles(tag, x0, s):
    for i in range(6):
        for j in range(6):
            up = s[i][j] > 0
            F.slab(f'{tag}_{i}{j}', (x0 + (j - 2.5) * C, (2.5 - i) * C, 0.12 if up else 0.04), (C * 0.9, C * 0.9, 0.24 if up else 0.08),
                   rgb=UP if up else DN, radius=0.02)
    return sum(map(sum, s)) / 36


def gauge(tag, x0, bonds, mark_star=None):
    n, c = 5, 0.78
    P = lambda i, j: (x0 + (i - 2) * c, (j - 2) * c)
    for i in range(n):
        for j in range(n):
            F.site(f'{tag}_v{i}{j}', (*P(i, j), 0), r=0.06, h=0.03)
    for (kind, i, j), s in bonds.items():
        (x1, y1) = P(i, j)
        (x2, y2) = P(i + 1, j) if kind == 'h' else P(i, j + 1)
        star = mark_star is not None and ((kind == 'h' and (i, j) in (mark_star, (mark_star[0] - 1, mark_star[1])))
                                          or (kind == 'v' and (i, j) in (mark_star, (mark_star[0], mark_star[1] - 1))))
        h = 0.22 if s > 0 else 0.07
        F.slab(f'{tag}_{kind}{i}{j}', ((x1 + x2) / 2, (y1 + y2) / 2, h / 2), (abs(x2 - x1) * 0.62 + 0.1, abs(y2 - y1) * 0.62 + 0.1, h),
               rgb=UP if s > 0 else DN, radius=0.02)
        if star:
            F.slab(f'{tag}_st{kind}{i}{j}', ((x1 + x2) / 2, (y1 + y2) / 2, 0.005), (abs(x2 - x1) * 0.8 + 0.22, abs(y2 - y1) * 0.8 + 0.22, 0.01),
                   rgb=F.ACCENT_AQM, alpha=0.35)
    bad = 0
    for i in range(n - 1):
        for j in range(n - 1):
            p = bonds[('h', i, j)] * bonds[('h', i, j + 1)] * bonds[('v', i, j)] * bonds[('v', i + 1, j)]
            if p < 0:
                bad += 1
                F.marker(f'{tag}_x{i}{j}', (x0 + (i - 1.5) * c, (j - 1.5) * c, 0.35), kind='cross', r=0.16, rgb=F.SITE)
    m = sum(bonds.values()) / len(bonds)
    return bad, m


def build():
    F.studio()
    rnd = random.Random(3)
    a = [[1] * 6 for _ in range(6)]
    for i, j in ((1, 4), (2, 1), (4, 3), (5, 0)):
        a[i][j] = -1
    while True:
        cells = [1] * 19 + [-1] * 17
        rnd.shuffle(cells)
        b = [cells[6 * i:6 * i + 6] for i in range(6)]
        if all(abs(sum(r)) < 6 for r in b) and all(abs(sum(b[i][j] for i in range(6))) < 6 for j in range(6)):
            break
    print('m(a) =', round(ising_tiles('a', XS[0], a), 3), ' m(b) =', round(ising_tiles('b', XS[1], b), 3))
    keys = [('h', i, j) for i in range(4) for j in range(5)] + [('v', i, j) for i in range(5) for j in range(4)]
    eps = {(i, j): rnd.choice((1, -1)) for i in range(5) for j in range(5)}
    cb = {k: eps[(k[1], k[2])] * eps[(k[1] + 1, k[2]) if k[0] == 'h' else (k[1], k[2] + 1)] for k in keys}
    print('(c) bad plaquettes, m =', gauge('c', XS[2], cb, mark_star=(2, 2)))
    rnd2 = random.Random(11)
    db = {k: rnd2.choice((1, -1)) for k in keys}
    print('(d) bad plaquettes, m =', gauge('d', XS[3], db))
    for k, x in enumerate(XS):
        F.anchor('p' + 'abcd'[k], (x - 1.6, 1.85, 0))
        F.anchor('m' + 'abcd'[k], (x, -1.75, 0))
    F.camera((0.0, 0.0, 0.0), elev=55.0, ortho=15.6, aspect=3.4)


F.main(build, NAME)
