"""Figure s02f06, fig:s02:archetypes: three two-dimensional dispersions and their densities of states.

A paraboloid E = k^2 with its constant density of states for E > 0, the step; a Dirac cone
E = +-|k| with g proportional to |E|; and a flat band E = 0 with a spike, drawn as a Lorentzian of
width 0.02 cut at the top of the axis. Each density stands on the same energy axis as its band.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's02f06_archetypes'
XS = (-5.0, 0.0, 5.0)                  # the three panels
Z0, SZ, R = 1.25, 0.95, 1.1            # height of E = 0, height per unit of E, radius of the k disc
GX = 1.0                               # x per unit of g
ES = [-1.1 + 2.2 * k / 400 for k in range(401)]


def panel(x0, kind, tag):
    xb = x0 - 0.75
    if kind == 'par':
        F.revolution(f'{tag}_E', lambda r: SZ * r * r / R, R, F.SURFACE, loc=(xb, 0.6, Z0)).visible_shadow = False
        gs = [0.0 if e < 0 else 0.8 for e in ES]
    elif kind == 'dirac':
        for sgn in (1, -1):
            F.revolution(f'{tag}_E{sgn}', lambda r, s=sgn: s * SZ * r, R, F.SURFACE, loc=(xb, 0.6, Z0)).visible_shadow = False
        gs = [0.85 * abs(e) for e in ES]
    else:
        F.revolution(f'{tag}_E', lambda r: 0.0, R, F.SURFACE, loc=(xb, 0.6, Z0)).visible_shadow = False
        gs = [min(1.3, 0.02 / math.pi / (e * e + 0.02 ** 2) * 0.05) for e in ES]
    xd = x0 + 0.95
    F.dos(f'{tag}_g', xd, 0, Z0, ES, gs, SZ, GX, depth=0.1)
    F.axis(f'{tag}_ay', (xd, 0, Z0 - 1.2 * SZ), (xd, 0, Z0 + 1.35 * SZ), r=0.018, head=0.14)
    F.axis(f'{tag}_ax', (xd, 0, Z0 - 1.2 * SZ), (xd + 1.55, 0, Z0 - 1.2 * SZ), r=0.018, head=0.14)
    F.tube(f'{tag}_zero', [(xb, 0.6, Z0), (xd + 1.4, 0, Z0)], 0.007, F.BOND).visible_shadow = False
    F.anchor('E', (xd, 0, Z0 + 1.35 * SZ))
    F.anchor('g', (xd + 1.55, 0, Z0 - 1.2 * SZ))
    F.anchor('band', (xb, -0.7, 0.0))
    F.anchor('zero', (xd, 0, Z0))


def build():
    F.studio()
    for k, (x, kind) in enumerate(zip(XS, ('par', 'dirac', 'flat'))):
        F.PREFIX[0] = 'abc'[k]
        panel(x, kind, 'abc'[k])
    F.PREFIX[0] = ''
    F.camera((0.0, 0.3, Z0), elev=26.0, ortho=15.4, aspect=3.0)


F.main(build, NAME)
