"""Figure s05f05, fig:s05:kitaev: the Kitaev chain, which Majoranas pair with which, seen from above.

N = 5 sites as light discs, each carrying its two Majorana halves gamma_{2n-1} and gamma_{2n} as two
balls. At the top, the trivial phase: the two halves of each site bound together by a translucent
capsule. At the bottom, the topological phase: gamma_{2n} bound to gamma_{2n+1} across the bond
between sites, which leaves gamma_1 and gamma_10 alone at the two ends, in the broken color.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's05f05_kitaev'
N, STEP = 5, 2.4
X0 = -(N - 1) * STEP / 2
DX = 0.42                              # offset of the two halves inside a site
YT, YB = 1.2, -1.2                     # the two rows
SITE_RGB = (0.80, 0.82, 0.86)


def row(y, tag, inside):
    disc = F.mat('kit_site', SITE_RGB, rough=0.6, spec=0.2)
    cap = F.ghost('kit_pair', F.ACCENT_AQM, 0.22)
    for n in range(N):
        x = X0 + n * STEP
        F.obj(f'{tag}_site{n}', F.mesh_of(f'{tag}_site{n}', [disc], lambda bm: F.bm_cylinder(bm, (0, 0, 0), (0, 0, 0.03),
                                                                                               0.8, seg=48)), loc=(x, y, 0))
        for h, sgn in ((1, -1), (2, 1)):
            idx = 2 * n + h
            lone = (not inside) and idx in (1, 2 * N)
            F.ball(f'{tag}_g{idx}', (x + sgn * DX, y, 0.2), 0.2, rgb=F.BROKEN if lone else F.ELECTRON)
            F.anchor(f'g{idx}', (x + sgn * DX, y - 0.3, 0.2))
        if inside:
            F.obj(f'{tag}_cap{n}', F.mesh_of(f'{tag}_cap{n}', [cap], lambda bm: F.bm_sphere(bm, F.Vector((0, 0, 0)), 1.0, seg=48, rings=24)),
                  loc=(x, y, 0.2), scale=(0.78, 0.36, 0.3))
    if not inside:
        for n in range(N - 1):
            x = X0 + n * STEP + DX + (STEP - 2 * DX) / 2
            F.obj(f'{tag}_cap{n}', F.mesh_of(f'{tag}_cap{n}', [cap], lambda bm: F.bm_sphere(bm, F.Vector((0, 0, 0)), 1.0, seg=48, rings=24)),
                  loc=(x, y, 0.2), scale=(STEP / 2 - DX + 0.38, 0.36, 0.3))
    F.anchor('panel', (X0 - 1.05, y + 0.95, 0))


def build():
    F.studio(shadows=False)
    F.PREFIX[0] = 't'
    row(YT, 't', True)
    F.PREFIX[0] = 'b'
    row(YB, 'b', False)
    F.PREFIX[0] = ''
    F.camera((0.0, 0.0, 0.0), elev=89.9, ortho=12.6, aspect=3.0)


F.main(build, NAME)
