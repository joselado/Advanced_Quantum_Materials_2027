"""Figure s05f06, fig:s05:qsh: building a Kitaev chain out of a quantum spin Hall edge.

A quantum spin Hall slab with its front edge carrying the two helical channels, spin up to the
right and spin down to the left, as tubes in the warm and cold colors. Two ferromagnet blocks
(dark, with a magnetization arrow) sit on the edge and gap it below them, so the channels are
drawn faded there; a superconductor block (light) sits on the segment between them, and the two
Majorana zero modes are glowing balls at the two ferromagnet-superconductor interfaces.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's05f06_qsh'
LX, LY, H = 12.0, 3.2, 0.35            # the slab
YE = -LY / 2 + 0.25                    # depth of the edge channels
FM = ((-3.9, 2.6), (3.9, 2.6))         # centers and lengths of the ferromagnets
SC = (0.0, 4.6)                        # center and length of the superconductor


def channel(name, x0, x1, y, z, rgb, alpha):
    d = 1 if x1 > x0 else -1
    pts = [(x0 + (x1 - x0) * j / 40, y, z) for j in range(41)]
    if alpha < 1:
        return F.tube(name, pts, 0.035, rgb, alpha=alpha)
    return F.flow(name, pts, r=0.035, rgb=rgb)


def build():
    F.studio()
    F.slab('qsh', (0, 0, H / 2), (LX, LY, H), rgb=(0.84, 0.86, 0.90), radius=0.05)
    z = H + 0.06
    gapped = [(c - l / 2, c + l / 2) for c, l in FM]
    edges = [-LX / 2 + 0.2, gapped[0][0], gapped[0][1], gapped[1][0], gapped[1][1], LX / 2 - 0.2]
    for k in range(5):
        a, b = edges[k], edges[k + 1]
        alpha = 0.25 if k in (1, 3) else 1.0
        channel(f'up{k}', a, b, YE - 0.12, z, F.UP_TAIL, alpha)
        channel(f'dn{k}', b, a, YE + 0.12, z, F.DOWN_TAIL, alpha)
    fm = F.mat('ferromagnet', (0.30, 0.31, 0.36), rough=0.5)
    for k, (c, l) in enumerate(FM):
        F.obj(f'fm{k}', F.mesh_of(f'fm{k}', [fm], lambda bm: F.bm_rounded_box(bm, F.Vector((0, 0, 0)), (l, 1.1, 0.7), 0.05)),
              loc=(c, YE + 0.85, H + 0.35))
        F.vector_arrow(f'M{k}', (c - 0.5, YE + 0.85, H + 0.75), (c + 0.5, YE + 0.85, H + 0.75), r=0.04, rgb=F.UP_TIP, head=0.2)
        F.anchor(f'fm{k}', (c, YE + 0.85, H + 0.95))
    sc = F.mat('superconductor', (0.72, 0.80, 0.88), rough=0.4)
    F.obj('sc', F.mesh_of('sc', [sc], lambda bm: F.bm_rounded_box(bm, F.Vector((0, 0, 0)), (SC[1], 1.1, 0.7), 0.05)),
          loc=(SC[0], YE + 0.85, H + 0.35))
    F.anchor('sc', (SC[0], YE + 0.85, H + 0.75))
    g = F.glow('glow_majorana', F.BROKEN, strength=1.4, alpha=0.4)
    for k, x in enumerate((SC[0] - SC[1] / 2, SC[0] + SC[1] / 2)):
        F.ball(f'maj{k}', (x, YE - 0.45, z), 0.13, rgb=F.BROKEN)
        F.obj(f'majg{k}', F.mesh_of(f'majg{k}', [g], lambda bm: F.bm_sphere(bm, F.Vector((0, 0, 0)), 1.0, seg=48, rings=24)),
              loc=(x, YE - 0.45, z), scale=0.35)
        F.anchor(f'maj{k}', (x, YE - 0.65, z - 0.1))
    F.anchor('up', (LX / 2 - 0.2, YE - 0.12, z))
    F.anchor('dn', (-LX / 2 + 0.2, YE + 0.12, z))
    F.anchor('qsh', (LX / 2 - 0.3, LY / 2 - 0.25, H))
    F.camera((0.0, 0.2, 0.6), elev=34.0, ortho=13.4, aspect=2.8)


F.main(build, NAME)
