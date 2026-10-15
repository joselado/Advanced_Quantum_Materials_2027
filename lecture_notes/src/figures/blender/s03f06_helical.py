"""Figure s03f06, fig:s03:helical: schematic edge dispersions, chiral against helical.

In each panel the bulk bands are two grey slabs, below -1 and above +1, and the edge branches are
tubes across the gap, E against the momentum k along the edge. (a) One chiral branch E = v k.
(b) Two helical branches E = +v k (spin up, the warm color) and E = -v k (spin down, the cold
color) crossing at the time-reversal-invariant momentum k = 0. (c) The same two branches with a
term that breaks time reversal: E = +-sqrt((v k)^2 + Delta^2), Delta = 0.35. Schematic, not computed.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's03f06_helical'
XS = (-5.0, 0.0, 5.0)
KX, Z0, SZ = 1.6, 1.4, 0.75            # half width of the k axis, height of E = 0, height per unit
V, DELTA = 1.0, 0.35
BULK = (0.80, 0.81, 0.85)
UP, DOWN = F.UP_TAIL, F.DOWN_TAIL


def panel(x0, kind, tag):
    for sgn in (1, -1):
        F.slab(f'{tag}_bulk{sgn}', (x0, 0, Z0 + sgn * 1.45 * SZ), (2 * KX, 0.3, 0.9 * SZ), rgb=BULK, radius=0.04)
    ks = [-1.3 + 2.6 * j / 120 for j in range(121)]
    P = lambda k, e: (x0 + KX * k / 1.3, -0.2, Z0 + SZ * e)
    if kind == 'chiral':
        F.tube(f'{tag}_e', [P(k, V * k) for k in ks], 0.035, F.ACCENT_AQM)
    elif kind == 'helical':
        F.tube(f'{tag}_up', [P(k, V * k) for k in ks], 0.035, UP)
        F.tube(f'{tag}_dn', [P(k, -V * k) for k in ks], 0.035, DOWN)
    else:
        neg = [k for k in ks if k <= 0]
        pos = [k for k in ks if k >= 0]
        e = lambda k: math.sqrt((V * k) ** 2 + DELTA ** 2)
        F.tube(f'{tag}_un', [P(k, e(k)) for k in neg], 0.035, DOWN)
        F.tube(f'{tag}_up', [P(k, e(k)) for k in pos], 0.035, UP)
        F.tube(f'{tag}_ln', [P(k, -e(k)) for k in neg], 0.035, UP)
        F.tube(f'{tag}_lp', [P(k, -e(k)) for k in pos], 0.035, DOWN)
        F.anchor('Delta', P(0.05, 0.0))
    F.axis(f'{tag}_ay', (x0, -0.2, Z0 - 2.05 * SZ), (x0, -0.2, Z0 + 2.15 * SZ), r=0.016, head=0.13)
    F.axis(f'{tag}_ax', (x0 - KX - 0.1, -0.2, Z0 - 2.05 * SZ), (x0 + KX + 0.3, -0.2, Z0 - 2.05 * SZ), r=0.016, head=0.13)
    F.anchor('E', (x0, -0.2, Z0 + 2.15 * SZ))
    F.anchor('k', (x0 + KX + 0.3, -0.2, Z0 - 2.05 * SZ))
    F.anchor('title', (x0 - KX, -0.2, Z0 + 2.15 * SZ))
    F.anchor('below', (x0, -0.2, Z0 - 2.1 * SZ))
    F.anchor('bulk', (x0 + KX, -0.2, Z0 + 1.45 * SZ))


def build():
    F.studio()
    for c, (x, kind) in enumerate(zip(XS, ('chiral', 'helical', 'gapped'))):
        F.PREFIX[0] = 'abc'[c]
        panel(x, kind, 'abc'[c])
    F.PREFIX[0] = ''
    F.camera((0.0, 0.0, Z0), elev=5.0, ortho=15.6, aspect=3.0)


F.main(build, NAME)
