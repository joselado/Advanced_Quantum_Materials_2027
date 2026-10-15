"""Figure s06f02, fig:s06:dimer: superexchange in the two-site Hubbard model.

Two renders. (a) Two dimers. Behind, parallel spins: the hop that would put two up electrons on one
site is drawn as a ghost arrow and a ghost hop crossed out. In front, antiparallel spins: the hop
to the virtual doubly occupied state (a ghost pair under a glow of energy U) and the hop back.
(b) Seen from the front, the exact singlet energy E_S = U/2 - sqrt((U/2)^2 + 4t^2) against U/t,
with t = 1, the triplet E_T = 0, and the ghost -4t^2/U that E_S approaches at large U.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
from mathutils import Vector                                              # noqa: E402

NAME = 's06f02_dimer'
D = 1.6                                # distance between the two sites
TOP = 0.08


def pair(y, tag):
    xs = (-D / 2, D / 2)
    for k, x in enumerate(xs):
        F.site(f'{tag}_s{k}', (x, y, 0), r=0.32)
    F.bond(f'{tag}_b', (xs[0] + 0.32, y, 0.05), (xs[1] - 0.32, y, 0.05))
    return xs


def hop(name, p0, p1, height, rgb, alpha=1.0):
    p0, p1 = Vector(p0), Vector(p1)
    pts = [p0.lerp(p1, j / 30) + Vector((0, 0, height * math.sin(math.pi * j / 30))) for j in range(31)]
    if alpha < 1:
        return F.tube(name, pts, 0.025, rgb, alpha=alpha)
    return F.flow(name, pts, r=0.025, rgb=rgb)


def build_a():
    F.studio()
    yb, yf = 3.8, 0.0
    xs = pair(yb, 'p')
    for k, x in enumerate(xs):
        F.arrow(f'p_up{k}', (x, yb, TOP + 0.45), (0, 0, 1), length=0.8)
    F.ghost_arrow('p_ghost', (xs[1] - 0.2, yb, TOP + 0.45), (0, 0, 1), length=0.8, alpha=0.25)
    hop('p_hop', (xs[0] + 0.15, yb, 1.0), (xs[1] - 0.3, yb, 1.0), 0.5, F.BOND, alpha=0.45)
    F.marker('p_block', (0, yb, 1.5), kind='cross', r=0.22, rgb=F.BROKEN)
    xs = pair(yf, 'a')
    F.arrow('a_up', (xs[0], yf, TOP + 0.45), (0, 0, 1), length=0.8)
    F.arrow('a_dn', (xs[1], yf, TOP + 0.45), (0, 0, -1), length=0.8)
    F.ghost_arrow('a_vup', (xs[1] - 0.18, yf, TOP + 0.45), (0, 0, 1), length=0.8, alpha=0.25)
    g = F.glow('glowU', F.ACCENT[1], strength=1.0, alpha=0.25)
    F.obj('a_glow', F.mesh_of('a_glow', [g], lambda bm: F.bm_sphere(bm, Vector((0, 0, 0)), 1.0, seg=48, rings=24)),
          loc=(xs[1], yf, TOP + 0.45), scale=(0.6, 0.6, 0.6))
    hop('a_there', (xs[0] + 0.15, yf, 1.0), (xs[1] - 0.3, yf, 1.0), 0.55, F.ACCENT_AQM)
    hop('a_back', (xs[1] - 0.15, yf, 0.95), (xs[0] + 0.3, yf, 0.95), 0.95, F.ACCENT_AQM)
    F.anchor('blocked', (0, yb, 1.85))
    F.anchor('par', (-D / 2 - 0.5, yb, 0.0))
    F.anchor('anti', (-D / 2 - 0.5, yf, 0.0))
    F.anchor('U', (xs[1] + 0.55, yf, TOP + 0.9))
    F.anchor('t', (0, yf, 2.05))
    F.anchor('panel', (-D / 2 - 1.1, yb, 1.9))
    F.camera((0.0, 1.9, 0.9), elev=30.0, ortho=5.6, aspect=6.8 / 4.6)


def build_b():
    F.studio()
    W, HZ = 6.0, 0.9                                  # x per 10 units of U, height per unit of t
    us = [0.05 + 12.0 * j / 300 for j in range(301)]
    P = lambda u, e: (-W / 2 + W * u / 12.0, 0, 3.4 + HZ * e)
    F.tube('ES', [P(u, u / 2 - math.sqrt((u / 2) ** 2 + 4)) for u in us], 0.035, F.ACCENT_AQM)
    F.tube('ET', [P(0, 0), P(12, 0)], 0.035, F.SITE)
    F.tube('pert', [P(u, -4 / u) for u in us if -4 / u > -2.6], 0.03, F.BOND, alpha=0.45)
    F.axis('b_ax', P(0, 0), P(12.6, 0), r=0.016, head=0.13)
    F.axis('b_ay', P(0, -2.8), P(0, 0.6), r=0.016, head=0.13)
    F.anchor('U', P(12.6, 0))
    F.anchor('E', P(0, 0.6))
    F.anchor('ET', P(6.5, 0))
    F.anchor('ES', P(3.0, 1.5 - math.sqrt(1.5 ** 2 + 4)))
    F.anchor('pert', P(2.0, -2.0))
    F.anchor('panel', P(-0.6, 0.65))
    F.camera((0.2, 0.0, 3.4 + HZ * -1.05), elev=3.0, ortho=7.4, aspect=8.6 / 4.6)


F.main_panels(NAME, [('a', build_a), ('b', build_b)])
