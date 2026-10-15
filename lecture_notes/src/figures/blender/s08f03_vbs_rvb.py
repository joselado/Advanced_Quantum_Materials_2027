"""Figure s08f03, fig:s08:vbsrvb: valence bond solid against resonating valence bonds, on a chain.

Four rows of twelve sites at four depths, back to front (a1), (a2), (b1), (b2). Strong bonds are
the (2n, 2n+1) ones. (a1) The fixed covering: a singlet capsule on every strong bond. (a2) Two
spinons, open balls at sites 2 and 9; between them the singlets sit on the weak bonds, and the
strong bonds (2,3), (4,5), (6,7), (8,9) have lost theirs, glowing in the broken color: the confining
string. (b1) The RVB state as three coverings stacked as
translucent ghost layers: the dimer covering, the shifted covering and one with a longer bond.
(b2) The same two spinons in the RVB background, where re-pairing behind them costs nothing,
so no string forms.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's08f03_vbs_rvb'
L, STEP = 12, 0.9
X0 = -(L - 1) * STEP / 2
YS = {'a1': 6.3, 'a2': 4.2, 'b1': 2.1, 'b2': 0.0}


def chain(y, tag, z=0.0, alpha=1.0):
    xs = [X0 + i * STEP for i in range(L)]
    for i, x in enumerate(xs):
        F.site(f'{tag}_s{i}', (x, y, z), r=0.2, h=0.05)
        if i < L - 1:
            F.bond(f'{tag}_b{i}', (x + 0.2, y, z + 0.04), (xs[i + 1] - 0.2, y, z + 0.04), r=0.03 if i % 2 == 0 else 0.015)
    return xs


def capsule(name, xa, xb, y, z, alpha=0.25, arc=0.0):
    cap = F.ghost('singlet_%.2f' % alpha, F.ACCENT_AQM, alpha)
    if arc == 0.0:
        return F.obj(name, F.mesh_of(name, [cap], lambda bm: F.bm_sphere(bm, F.Vector((0, 0, 0)), 1.0, seg=40, rings=20)),
                     loc=((xa + xb) / 2, y, z + 0.22), scale=(abs(xb - xa) / 2 + 0.28, 0.28, 0.24))
    pts = [((xa + xb) / 2 - (xb - xa) / 2 * math.cos(math.pi * k / 30), y, z + 0.22 + arc * math.sin(math.pi * k / 30))
           for k in range(31)]
    return F.tube(name, pts, 0.09, F.ACCENT_AQM, alpha=alpha)


def open_ball(name, loc, r=0.17):
    shell = F.mat('open_ball', (0.97, 0.97, 0.98), rough=0.3, spec=0.5)
    F.obj(name, F.mesh_of(name, [shell], lambda bm: F.bm_sphere(bm, F.Vector((0, 0, 0)), r)), loc=loc)
    ring = F.mat('open_ring', F.SITE, rough=0.4)
    x, y, z = loc
    F.obj(name + '_rim', F.mesh_of(name + '_rim', [ring], lambda bm: F.bm_sweep(
        bm, [(r * math.cos(2 * math.pi * k / 48), r * math.sin(2 * math.pi * k / 48), 0) for k in range(49)], 0.022,
        end_caps=False)), loc=(x, y, z))


def build():
    F.studio()
    xs = chain(YS['a1'], 'a1')
    for i in range(0, L, 2):
        capsule(f'a1_c{i}', xs[i], xs[i + 1], YS['a1'], 0)
    F.anchor('a1', (X0 - 0.45, YS['a1'], 0.0))
    # (a2) and (b2): spinons at 2 and 9, the singlets between them on the weak bonds (3,4), (5,6), (7,8)
    for row in ('a2', 'b2'):
        xs = chain(YS[row], row)
        for i, j in ((0, 1), (3, 4), (5, 6), (7, 8), (10, 11)):
            capsule(f'{row}_c{i}', xs[i], xs[j], YS[row], 0)
        for i in (2, 9):
            open_ball(f'{row}_open{i}', (xs[i], YS[row], 0.25))
        F.anchor(row, (X0 - 0.45, YS[row], 0.0))
    xs = [X0 + i * STEP for i in range(L)]
    g = F.glow('string_glow', F.BROKEN, strength=1.0, alpha=0.3)
    for i in (2, 4, 6, 8):                              # the strong bonds that lost their singlet
        F.rod(f'a2_str{i}', (xs[i] + 0.2, YS['a2'], 0.05), (xs[i + 1] - 0.2, YS['a2'], 0.05), r=0.06, rgb=F.BROKEN)
        F.obj(f'a2_g{i}', F.mesh_of(f'a2_g{i}', [g], lambda bm: F.bm_sphere(bm, F.Vector((0, 0, 0)), 1.0, seg=40, rings=20)),
              loc=((xs[i] + xs[i + 1]) / 2, YS['a2'], 0.1), scale=(0.5, 0.22, 0.18))
    F.anchor('string', ((xs[2] + xs[9]) / 2, YS['a2'] + 0.45, 0.45))
    F.anchor('free', ((xs[2] + xs[9]) / 2, YS['b2'] - 0.35, 0))
    # (b1): three coverings stacked as translucent layers
    xs = chain(YS['b1'], 'b1')
    for i in range(0, L, 2):
        capsule(f'b1_c0_{i}', xs[i], xs[i + 1], YS['b1'], 0.0, alpha=0.22)
    for i in range(1, L - 1, 2):
        capsule(f'b1_c1_{i}', xs[i], xs[i + 1], YS['b1'], 0.45, alpha=0.16)
    capsule('b1_long', xs[3], xs[8], YS['b1'], 0.9, alpha=0.18, arc=0.35)
    F.anchor('b1', (X0 - 0.45, YS['b1'], 0.0))
    F.anchor('sum', (X0 + (L - 1) * STEP + 0.45, YS['b1'], 0.45))
    F.camera((0.0, 3.15, 0.5), elev=36.0, ortho=12.6, aspect=2.6)


F.main(build, NAME)
