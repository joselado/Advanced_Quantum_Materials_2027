"""Figure s05f01, fig:s05:flux: flux quantization as a macroscopic readout of h/2e.

Two renders. (a) A superconducting ring as a translucent torus, the contour deep in the bulk as a
dashed tube inside it, and the flux through the hole as vertical arrows. (b) Seen from above, the
condensate phase theta along the same contour as an arrow at each of twelve points, turning once
(n = 1) as we go once around, so that it comes back to itself.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's05f01_flux'
RT, RM = 1.6, 0.42                     # torus radius and tube radius
N = 12                                 # points around the contour in (b)


def build_a():
    F.studio()
    ring = F.ghost('ring_glass', F.SURFACE, 0.35)
    loop = [(RT * math.cos(2 * math.pi * k / 96), RT * math.sin(2 * math.pi * k / 96), 1.0) for k in range(97)]
    F.obj('torus', F.mesh_of('torus', [ring], lambda bm: F.bm_sweep(bm, loop, RM, seg=40, end_caps=False)))
    for k in range(24):                                 # the dashed contour deep inside the ring
        a0, a1 = 2 * math.pi * k / 24, 2 * math.pi * (k + 0.55) / 24
        F.tube(f'contour{k}', [(RT * math.cos(a), RT * math.sin(a), 1.0) for a in [a0 + (a1 - a0) * j / 6 for j in range(7)]],
               0.03, F.ACCENT_AQM)
    for k, (x, y) in enumerate([(0, 0), (0.5, 0.2), (-0.45, 0.3), (0.1, -0.5), (-0.3, -0.35)]):
        F.vector_arrow(f'B{k}', (x, y, 0.15), (x, y, 2.0), r=0.025, rgb=F.SITE, head=0.18)
    F.anchor('Phi', (0.1, 0.0, 2.1))
    F.anchor('contour', (RT * math.cos(-0.9), RT * math.sin(-0.9), 1.0 - RM - 0.05))
    F.anchor('panel', (-RT - RM - 0.2, 0, 2.3))
    F.camera((0.0, 0.0, 1.05), elev=28.0, ortho=4.9, aspect=5.3 / 4.5)


def build_b():
    F.studio(shadows=False)
    loop = [(RT * math.cos(2 * math.pi * k / 96), RT * math.sin(2 * math.pi * k / 96), 0.02) for k in range(97)]
    F.tube('path', loop, 0.015, F.BOND)
    for k in range(N):
        a = 2 * math.pi * k / N
        x, y = RT * math.cos(a), RT * math.sin(a)
        disc = F.mat('dial', (0.80, 0.82, 0.86), rough=0.6, spec=0.2)
        F.obj(f'dial{k}', F.mesh_of(f'dial{k}', [disc], lambda bm: F.bm_cylinder(bm, (0, 0, 0), (0, 0, 0.03), 0.3, seg=40)),
              loc=(x, y, 0.03))
        th = a                                          # theta advances by 2 pi once around, n = 1
        F.vector_arrow(f'th{k}', (x - 0.22 * math.cos(th), y - 0.22 * math.sin(th), 0.08),
                       (x + 0.22 * math.cos(th), y + 0.22 * math.sin(th), 0.08), r=0.025, head=0.1)
    F.anchor('start', (RT + 0.35, 0, 0.05))
    F.anchor('center', (0, 0, 0.05))
    F.anchor('panel', (-RT - 0.75, RT + 0.45, 0))
    F.camera((0.0, 0.05, 0.0), elev=89.9, ortho=4.7, aspect=5.4 / 4.5)


F.main_panels(NAME, [('a', build_a), ('b', build_b)])
