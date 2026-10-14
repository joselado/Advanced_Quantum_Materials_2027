"""Figure s02f02, fig:s02:cosband: the band -2t cos(phi) of (2.8), for t = 1, and its density of states.

The band is the tube, with its minimum at phi = 0 as in (2.5) with t > 0. The three ghost tubes are
its local forms: the parabola -2 + phi^2 at the bottom, the inverted parabola 2 - (phi - pi)^2 at the
top, and the tangent 2 (phi - pi/2) at midband. To the right, the density of states (2.16),
g(E) = 1 / (pi sqrt(4 - E^2)), as a slab standing on the same energy axis, cut at g = 0.9.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's02f02_cosband'
X0, SX = -1.9, 1.1                     # x of phi = 0 and x per unit of phi
Z0, SZ = 2.0, 0.62                     # height of E = 0 and height per unit of t
XD, GX = 3.9, 2.2                      # x of the density-of-states axis and x per unit of g


def P(phi, e):
    return (X0 + SX * phi, 0, Z0 + SZ * e)


def Q(phi, e):
    return (X0 + SX * phi, -0.12, Z0 + SZ * e)


def build():
    F.studio()
    F.tube('band', [P(-math.pi + 2 * math.pi * k / 300, -2 * math.cos(-math.pi + 2 * math.pi * k / 300))
                    for k in range(301)], 0.045, F.ACCENT_AQM)
    ghost = (0.50, 0.51, 0.56)                     # the local forms, a little in front of the band
    F.tube('par', [Q(p, -2 + p * p) for p in [-1.5 + 3.0 * k / 60 for k in range(61)]], 0.022, ghost)
    for sgn in (1, -1):
        F.tube(f'hole{sgn}', [Q(sgn * (math.pi - u), 2 - u * u) for u in [1.5 * k / 40 for k in range(41)]],
               0.022, ghost)
    F.tube('lin', [Q(p, 2 * (p - math.pi / 2)) for p in (math.pi / 2 - 0.9, math.pi / 2 + 0.9)], 0.022, ghost)
    F.axis('ax_phi', (X0 - SX * math.pi - 0.3, 0, Z0 - 3.2 * SZ), (X0 + SX * math.pi + 0.5, 0, Z0 - 3.2 * SZ))
    F.axis('ax_E', (X0, 0, Z0 - 3.2 * SZ), (X0, 0, Z0 + 2.6 * SZ))
    for v, tag in ((-math.pi, 'mpi'), (0, 'zero'), (math.pi, 'pi')):
        F.rod(f'tick_{tag}', P(v, -3.2), P(v, -3.05), r=0.015)
        F.anchor(tag, P(v, -3.25))
    F.anchor('phi', (X0 + SX * math.pi + 0.5, 0, Z0 - 3.2 * SZ))
    F.anchor('E', (X0, 0, Z0 + 2.6 * SZ))
    F.anchor('bottom', P(0.0, -2.12))
    F.anchor('top', P(math.pi, 2.12))
    F.anchor('mid', P(1.75, -0.35))
    # the density of states, standing on its own energy axis
    es = [-1.995 + 3.99 * k / 400 for k in range(401)]
    gs = [min(0.9, 1 / (math.pi * math.sqrt(4 - e * e))) for e in es]
    F.dos('dos', XD, 0, Z0, es, gs, SZ, GX, depth=0.1, alpha=0.75)
    F.axis('ax_E2', (XD, 0, Z0 - 3.2 * SZ), (XD, 0, Z0 + 2.6 * SZ))
    F.axis('ax_g', (XD, 0, Z0 - 3.2 * SZ), (XD + 2.9, 0, Z0 - 3.2 * SZ))
    for e in (-2, 2):
        F.tube(f'edge{e}', [(X0 - SX * math.pi, 0, Z0 + SZ * e), (XD + 2.5, 0, Z0 + SZ * e)], 0.008, F.BOND)
    F.anchor('E2', (XD, 0, Z0 + 2.6 * SZ))
    F.anchor('g', (XD + 2.9, 0, Z0 - 3.2 * SZ))
    F.anchor('peak', (XD + GX * 0.9 + 0.05, 0, Z0 + SZ * 1.85))
    F.anchor('m2t', (XD, 0, Z0 - 2 * SZ))
    F.anchor('p2t', (XD, 0, Z0 + 2 * SZ))
    F.camera((0.5, 0.0, Z0 - 0.3), elev=6.0, ortho=13.4, aspect=2.8)


F.main(build, NAME)
