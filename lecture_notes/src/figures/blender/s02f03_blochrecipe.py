"""Figure s02f03, fig:s02:recipe: band folding, the two-band chain (2.13) seen from the one-band one.

Two renders: (a) the chains seen from above, (b) the two band panels seen from the front.
Left, the chain twice. Behind, with one site per cell and all hoppings equal. In front, with two
sites A, B per cell, the intracell bond 1 thick and the intercell bond eta thin.
Middle, eta = 1: the band -2 cos(k) of the one-site cell over its zone (ghost) and the same band
folded into the zone of the two-site cell, phi = 2k in [-pi, pi], as the two branches
+-|1 + exp(-i phi)| of (2.13), which touch at the zone edge.
Right, eta = 0.6: the branches +-|1 + eta exp(-i phi)| with the gap 2(1 - eta) open at the edge.
"""
import cmath
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's02f03_blochrecipe'
XA, XB, XC = 0.0, -2.0, 5.15           # the chains, and the centers of the two band panels
STEP, R = 0.68, 0.17
SX, Z0, SZ = 0.62, 1.55, 0.55          # x per unit of phi, height of E = 0, height per unit of hopping
EDGE = (0.30, 0.31, 0.35)


def chain(y, tag, cell):
    xs = [XA + (i - 3.5) * STEP for i in range(8)]
    for i, x in enumerate(xs):
        F.site(f'{tag}_s{i}', (x, y, 0), r=R, h=0.05)
        if i < 7:
            strong = cell == 1 or i % 2 == 0
            F.bond(f'{tag}_b{i}', (x + R, y, 0.04), (xs[i + 1] - R, y, 0.04), r=0.06 if strong else 0.022)
    for c in range(0, 8, cell):
        xc = (xs[c] + xs[c + cell - 1]) / 2
        F.slab(f'{tag}_cell{c}', (xc, y, 0.0), (cell * STEP - 0.1, 0.62, 0.02), rgb=F.ACCENT_AQM, alpha=0.18)
    return xs


def bands(x0, eta, tag, ghost):
    P = lambda phi, e: (x0 + SX * phi, 0, Z0 + SZ * e)
    if ghost:
        F.tube(f'{tag}_full', [P(2 * k, -2 * math.cos(k)) for k in
                               [-math.pi + 2 * math.pi * j / 300 for j in range(301)]], 0.03, F.BOND, alpha=0.4)
    for sgn in (1, -1):
        F.tube(f'{tag}_band{sgn}', [P(p, sgn * abs(1 + eta * cmath.exp(-1j * p))) for p in
                                    [-math.pi + 2 * math.pi * j / 200 for j in range(201)]], 0.04, F.ACCENT_AQM)
    half = SX * (2 * math.pi if ghost else math.pi) + 0.2
    F.axis(f'{tag}_ax', (x0 - half - 0.15, 0, Z0 - 2.3 * SZ), (x0 + half + 0.35, 0, Z0 - 2.3 * SZ), r=0.02, head=0.15)
    F.axis(f'{tag}_ay', (x0, 0, Z0 - 2.3 * SZ), (x0, 0, Z0 + 2.45 * SZ), r=0.02, head=0.15)
    for sgn in (1, -1):
        F.slab(f'{tag}_edge{sgn}', (x0 + sgn * SX * math.pi, 0, Z0), (0.02, 0.5, 4.4 * SZ), rgb=EDGE, alpha=0.14)
        F.anchor(f'pi{"p" if sgn > 0 else "m"}', (x0 + sgn * SX * math.pi, 0, Z0 - 2.35 * SZ))
        if ghost:
            F.anchor(f'twopi{"p" if sgn > 0 else "m"}', (x0 + sgn * SX * 2 * math.pi, 0, Z0 - 2.35 * SZ))
    F.anchor('phi', (x0 + half + 0.35, 0, Z0 - 2.3 * SZ))
    F.anchor('E', (x0, 0, Z0 + 2.45 * SZ))
    F.anchor('gap', (x0 + SX * math.pi + 0.1, 0, Z0))
    F.anchor('title', (x0, 0, Z0 + 2.75 * SZ))


def build_a():
    F.studio()
    xs = chain(2.1, 'one', 1)
    F.anchor('one', (xs[0] - 0.3, 2.1 + 0.42, 0))
    xs = chain(0.0, 'two', 2)
    F.anchor('two', (xs[0] - 0.3, 0.42, 0))
    F.anchor('A', (xs[6], 0.3, 0))
    F.anchor('B', (xs[7], 0.3, 0))
    F.anchor('t1', ((xs[6] + xs[7]) / 2, -0.33, 0.0))
    F.anchor('teta', ((xs[5] + xs[6]) / 2, -0.33, 0.0))
    F.camera((XA, 1.1, 0.0), elev=55.0, ortho=5.9, aspect=1.32)


def build_b():
    F.studio()
    F.PREFIX[0] = 'b'
    bands(XB, 1.0, 'b', True)
    F.PREFIX[0] = 'c'
    bands(XC, 0.6, 'c', False)
    F.PREFIX[0] = ''
    F.camera((1.15, 0.0, Z0 - 0.05), elev=6.0, ortho=13.8, aspect=13.8 / 4.15)


F.main_panels(NAME, [('a', build_a), ('b', build_b)])
