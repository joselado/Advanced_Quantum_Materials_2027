"""Figure s01f03, fig:s01:channels: one Hamiltonian and three ordered states.

Left, a four-site chain with two electrons on neighboring sites and the glow of the interaction
between them, the generic Hamiltonian (1.5). Right, the three ordered states that its three
mean-field decouplings give: the charge as columns of alternating height, the spin as alternating
arrows, and the electrons bound in pairs by a translucent capsule.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
from mathutils import Vector                                              # noqa: E402

NAME = 's01f03_threechannels'
X0, XS = -5.9, (-1.75, 2.2, 6.1)      # the Hamiltonian, and the three ordered states
STEP, R = 0.78, 0.22
TOP = 0.08


def chain(xc, tag):
    xs = [xc + (i - 1.5) * STEP for i in range(4)]
    for i, x in enumerate(xs):
        F.site(f'{tag}_s{i}', (x, 0, 0), r=R)
        if i < 3:
            F.bond(f'{tag}_b{i}', (x + R, 0, 0.05), (xs[i + 1] - R, 0, 0.05))
    return xs


def build():
    F.studio()
    xs = chain(X0, 'h')
    for i in (1, 2):
        F.ball(f'h_e{i}', (xs[i], 0, TOP + 0.24), 0.2)
    g = F.glow('glowV', F.ACCENT[1], strength=1.2, alpha=0.30)
    F.obj('h_glow', F.mesh_of('h_glow', [g], lambda bm: F.bm_sphere(bm, Vector((0, 0, 0)), 1.0, seg=48, rings=24)),
          loc=((xs[1] + xs[2]) / 2, 0, TOP + 0.24), scale=(0.7, 0.32, 0.32))
    F.anchor('H', (X0, 0, 1.05))
    F.anchor('Hb', (X0, -0.4, 0))
    F.anchor('out', (X0 + 1.75, 0, 0.35))
    # charge density wave
    xs = chain(XS[0], 'c')
    for i, x in enumerate(xs):
        F.column(f'c_col{i}', (x, 0, TOP), 0.95 if i % 2 == 0 else 0.15, r=0.17)
    # magnet
    xs = chain(XS[1], 'm')
    for i, x in enumerate(xs):
        F.arrow(f'm_a{i}', (x, 0, TOP + 0.42), (0, 0, 1 if i % 2 == 0 else -1), length=0.78)
    # superconductor: two pairs, each bound by a capsule
    xs = chain(XS[2], 's')
    cap = F.ghost('pair', F.ELECTRON, 0.18)
    for p in (0, 2):
        for i in (p, p + 1):
            F.ball(f's_e{i}', (xs[i], 0, TOP + 0.24), 0.17)
        F.obj(f's_cap{p}', F.mesh_of(f's_cap{p}', [cap], lambda bm: F.bm_sphere(
            bm, Vector((0, 0, 0)), 1.0, seg=48, rings=24)), loc=((xs[p] + xs[p + 1]) / 2, 0, TOP + 0.24),
            scale=(0.66, 0.27, 0.27))
    for k, x in enumerate(XS):
        F.anchor(f'in{k}', (x - 1.5, 0, 0.35))
        F.anchor(f'top{k}', (x, 0, 1.15))
        F.anchor(f'bot{k}', (x, -0.4, 0))
    F.camera((0.1, 0.0, 0.3), elev=22.0, ortho=15.6, aspect=3.0)


F.main(build, NAME)
