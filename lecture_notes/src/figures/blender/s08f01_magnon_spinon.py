"""Figure s08f01, fig:s08:magnonspinon: magnon against spinon, Delta S = 1 against Delta S = 1/2.

(a) Behind, a Neel chain of ten sites with one arrow flipped, the flipped one in the broken color.
(b) In front, the same ten sites paired into singlets, drawn as translucent capsules, with one pair
broken: since the chain has an even number of sites, breaking the pattern leaves two unpaired
sites, drawn as open balls, each with S = 1/2.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's08f01_magnon_spinon'
L, STEP = 10, 1.15
X0 = -(L - 1) * STEP / 2
FLIP = 5


def chain(y, tag):
    xs = [X0 + i * STEP for i in range(L)]
    for i, x in enumerate(xs):
        F.site(f'{tag}_s{i}', (x, y, 0), r=0.28)
        if i < L - 1:
            F.bond(f'{tag}_b{i}', (x + 0.28, y, 0.05), (xs[i + 1] - 0.28, y, 0.05))
    return xs


def open_ball(name, loc, r=0.2):
    shell = F.mat('open_ball', (0.97, 0.97, 0.98), rough=0.3, spec=0.5)
    ring = F.mat('open_ring', F.SITE, rough=0.4)
    F.obj(name, F.mesh_of(name, [shell], lambda bm: F.bm_sphere(bm, F.Vector((0, 0, 0)), r)), loc=loc)
    x, y, z = loc
    import math
    F.obj(name + '_rim', F.mesh_of(name + '_rim', [ring], lambda bm: F.bm_sweep(
        bm, [(r * math.cos(2 * math.pi * k / 48), r * math.sin(2 * math.pi * k / 48), 0) for k in range(49)], 0.025,
        end_caps=False)), loc=(x, y, z))


def build():
    F.studio()
    yb = 2.6
    xs = chain(yb, 'a')
    for i, x in enumerate(xs):
        up = (i % 2 == 0) != (i == FLIP)
        if i == FLIP:
            F.ghost_arrow('a_was', (x - 0.2, yb, 0.53), (0, 0, 1 if i % 2 == 0 else -1), length=0.8, alpha=0.25)
            m = F.gradient_arrow_material('arrow_flip', F.srgb(230, 90, 80), F.BROKEN)
            F.obj('a_flip', F.arrow_mesh('arrow_flip_mesh', m), loc=(x + 0.12, yb, 0.53),
                  rot=F.Vector((0, 0, 1 if up else -1)).to_track_quat('Z', 'Y').to_euler(), scale=0.8)
        else:
            F.arrow(f'a_ar{i}', (x, yb, 0.53), (0, 0, 1 if up else -1), length=0.8)
    F.anchor('flip', (xs[FLIP], yb, 1.1))
    F.anchor('a', (X0 - 0.4, yb, 0.3))
    xs = chain(0.0, 'b')
    cap = F.ghost('singlet', F.ACCENT_AQM, 0.22)
    pairs = [(0, 1), (2, 3), (6, 7), (8, 9)]           # the pair (4, 5) is broken
    for k, (i, j) in enumerate(pairs):
        F.obj(f'b_cap{k}', F.mesh_of(f'b_cap{k}', [cap], lambda bm: F.bm_sphere(bm, F.Vector((0, 0, 0)), 1.0, seg=48, rings=24)),
              loc=((xs[i] + xs[j]) / 2, 0, 0.3), scale=(STEP / 2 + 0.35, 0.38, 0.32))
        for s in (i, j):
            F.ball(f'b_e{s}', (xs[s], 0, 0.3), 0.13, rgb=F.ACCENT_AQM)
    for s in (4, 5):
        open_ball(f'b_open{s}', (xs[s], 0, 0.32))
    F.anchor('spinon', ((xs[4] + xs[5]) / 2, -0.45, 0))
    F.anchor('b', (X0 - 0.4, 0, 0.3))
    F.camera((0.0, 1.3, 0.55), elev=26.0, ortho=12.6, aspect=2.8)


F.main(build, NAME)
