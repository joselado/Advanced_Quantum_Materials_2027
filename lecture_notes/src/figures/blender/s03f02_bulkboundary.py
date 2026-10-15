"""Figure s03f02, fig:s03:bulkboundary: the bulk-boundary correspondence as an argument about an integer.

Seen from the front, three rows over the same x, on a backdrop whose color goes from H1 on the
left to H2 on the right. Top, the Chern number, a step from 1 to 0 at the interface. Middle, the
local gap in the local-gap approximation, Delta(x) = Delta0 |tanh(x / w)|, which goes to zero there,
with a cross at the zero. Bottom, the bound state |psi|^2 = sech^2(x / w) as a slab with a glow.
Schematic, not computed from a model.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's03f02_bulkboundary'
LX, W = 7.0, 0.7                       # length of the rows, width of the interface
ZS = (3.1, 1.75, 0.4)                  # base heights of the three rows, top to bottom
SZ = 0.95                              # height per unit of each curve


def row_axis(tag, z):
    F.axis(f'{tag}_ax', (-LX / 2, 0, z), (LX / 2 + 0.3, 0, z), r=0.018, head=0.14)
    F.axis(f'{tag}_ay', (-LX / 2, 0, z), (-LX / 2, 0, z + 1.15 * SZ), r=0.018, head=0.14)


def build():
    F.studio()
    m = F.gradient_x_material('backdrop', F.srgb(196, 212, 232), F.srgb(238, 239, 242), -LX / 2, LX / 2)
    wall = F.obj('backdrop', F.mesh_of('backdrop', [m], lambda bm: F.bm_rounded_box(
        bm, F.Vector((0, 0, 0)), (LX + 0.2, 0.05, 4.35), 0.02)), loc=(0, 0.45, 2.3))
    wall.visible_shadow = False
    xs = [-LX / 2 + LX * k / 300 for k in range(301)]
    z = ZS[0]
    row_axis('c', z)
    F.tube('C', [(-LX / 2, 0, z + SZ), (0, 0, z + SZ), (0, 0, z + 0.02), (LX / 2, 0, z + 0.02)], 0.04, F.ACCENT_AQM)
    F.anchor('C1', (-LX / 4, 0, z + SZ + 0.05))
    F.anchor('C2', (LX / 4, 0, z + 0.1))
    F.anchor('Clab', (-LX / 2 - 0.1, 0, z + 0.5 * SZ))
    z = ZS[1]
    row_axis('g', z)
    F.tube('gap', [(x, 0, z + 0.9 * SZ * abs(math.tanh(x / W))) for x in xs], 0.04, F.ACCENT_AQM)
    F.marker('gap0', (0, -0.05, z + 0.02), kind='cross', r=0.16, rgb=F.BROKEN)
    F.anchor('glab', (-LX / 2 - 0.1, 0, z + 0.5 * SZ))
    z = ZS[2]
    row_axis('p', z)
    F.profile('psi', xs, [0.9 * SZ / math.cosh(x / W) ** 2 for x in xs], 0.1, F.BROKEN).location = (0, 0, z)
    g = F.glow('glow_bound', F.BROKEN, strength=1.2, alpha=0.3)
    F.obj('bound_glow', F.mesh_of('bound_glow', [g], lambda bm: F.bm_sphere(bm, F.Vector((0, 0, 0)), 1.0, seg=48, rings=24)),
          loc=(0, -0.1, z + 0.35), scale=(0.75, 0.3, 0.55))
    F.anchor('plab', (-LX / 2 - 0.1, 0, z + 0.5 * SZ))
    F.anchor('H1', (-LX / 2 + 0.15, 0, 4.4))
    F.anchor('H2', (LX / 2 - 0.15, 0, 4.4))
    F.anchor('x', (LX / 2 + 0.3, 0, ZS[2]))
    F.camera((-0.25, 0.0, 2.3), elev=4.0, ortho=9.6, aspect=2.0)


F.main(build, NAME)
