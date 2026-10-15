"""Figure s09f04, fig:s09:vacancy: a vacancy is a boundary of zero size.

Two renders. Top, seen from above: a topological slab three times, with a large hole and the edge
mode running around it as a glowing tube, a small hole with its smaller loop, and a single missing
site with a glow where the bound mode sits. Bottom, seen from the front: three schematic level
ladders, the clean spectrum that a trivial and a topological insulator with the same gap share,
the trivial one with a vacancy, unchanged, and the topological one with a vacancy, with a level
in the gap in the broken color. Schematic, not computed.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's09f04_vacancy'


def build_top():
    F.studio(shadows=False)
    xs = (-4.4, 0.0, 4.4)
    for k, (x0, rh) in enumerate(zip(xs, (1.0, 0.45, 0.0))):
        m = F.mat('qsh_slab', (0.70, 0.73, 0.79), rough=0.6)

        def slab(bm, rh=rh):
            outer, nth = 1.75, 96
            rin = max(rh, 0.001)
            o = [bm.verts.new((outer * max(abs(math.cos(t)), abs(math.sin(t))) ** -1 * math.cos(t) * 0.8,
                               outer * max(abs(math.cos(t)), abs(math.sin(t))) ** -1 * math.sin(t) * 0.6, 0.0))
                 for t in [2 * math.pi * j / nth for j in range(nth)]]
            i = [bm.verts.new((rin * math.cos(2 * math.pi * j / nth), rin * math.sin(2 * math.pi * j / nth), 0.0)) for j in range(nth)]
            for j in range(nth):
                bm.faces.new((i[j], o[j], o[(j + 1) % nth], i[(j + 1) % nth]))
        F.obj(f'slab{k}', F.mesh_of(f'slab{k}', [m], slab), loc=(x0, 0, 0))
        g = F.glow('edge_glow', F.ACCENT_AQM, strength=1.0, alpha=0.35)
        if rh > 0:
            loop = [(x0 + (rh + 0.12) * math.cos(2 * math.pi * j / 80), (rh + 0.12) * math.sin(2 * math.pi * j / 80), 0.05)
                    for j in range(73)]
            F.flow(f'mode{k}', loop, r=0.035, rgb=F.ACCENT_AQM)
        else:
            gb = F.glow('vac_glow', F.BROKEN, strength=1.3, alpha=0.4)
            F.obj('vac', F.mesh_of('vac', [gb], lambda bm: F.bm_sphere(bm, F.Vector((0, 0, 0)), 1.0, seg=40, rings=20)),
                  loc=(x0, 0, 0.05), scale=(0.4, 0.4, 0.15))
            for j in range(-2, 3):
                for i in range(-3, 4):
                    if (i, j) != (0, 0):
                        F.site(f'site{i}{j}', (x0 + 0.38 * i, 0.38 * j, 0.0), r=0.06, h=0.03)
        F.anchor(f'h{k}', (x0, -1.15, 0))
    F.anchor('arr0', (-2.35, 0, 0))
    F.anchor('arr1', (-1.95, 0, 0))
    F.anchor('arr2', (2.05, 0, 0))
    F.anchor('arr3', (2.45, 0, 0))
    F.camera((0.0, -0.1, 0.0), elev=89.9, ortho=12.6, aspect=12.6 / 2.6)


def build_bottom():
    F.studio()
    xs = (-4.4, 0.0, 4.4)
    bands = [-1.5 + 0.12 * j for j in range(5)] + [0.98 + 0.12 * j for j in range(5)]
    for k, x0 in enumerate(xs):
        F.axis(f'ax{k}', (x0 - 0.75, 0, 0.2), (x0 - 0.75, 0, 2.35), r=0.016, head=0.12)
        for j, e in enumerate(bands):
            F.level(f'l{k}{j}', x0, 0, 1.25 + 0.6 * e, length=0.9, r=0.025)
        if k == 2:
            F.level('ingap', x0, 0, 1.25, length=0.9, r=0.04, rgb=F.BROKEN)
        F.anchor(f'top{k}', (x0, 0, 2.3))
        F.anchor(f'bot{k}', (x0, 0, 0.15))
    F.tube('gapline', [(-5.4, 0, 1.25), (5.3, 0, 1.25)], 0.006, F.BOND).visible_shadow = False
    F.camera((0.0, 0.0, 1.25), elev=3.0, ortho=12.6, aspect=12.6 / 2.6)


F.main_panels(NAME, [('top', build_top), ('bottom', build_bottom)])
