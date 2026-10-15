"""Figure s05f04, fig:s05:topology: same gap, different topology, seen from above.

(a) s-wave and (b) chiral p-wave on the same circular Fermi pocket: at twelve points of the pocket a
dial, a small disc in the complex plane placed at the momentum where Delta is evaluated, with an
arrow at the phase of Delta. For s-wave the phase is the same everywhere; for p + ip,
sin kx + i sin ky ~ kF exp(i phi), it equals the angle of the momentum and turns once. (c) The
consequence in a finite sample: the trivial state has no edge states, and the chiral state with
C = 2 has two branches on each edge, all going around in the same sense.
"""
import cmath
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's05f04_topology'
XA, XB, XC = -4.0, 0.3, 4.6
RP = 1.35                              # drawn radius of the pocket
N = 12


def pocket(x0, chiral, tag):
    F.tube(f'{tag}_FS', [(x0 + RP * math.cos(2 * math.pi * j / 120), RP * math.sin(2 * math.pi * j / 120), 0.02)
                         for j in range(121)], 0.015, F.BOND)
    F.rod(f'{tag}_kx', (x0 - RP - 0.6, 0, 0.01), (x0 + RP + 0.6, 0, 0.01), r=0.008)
    F.rod(f'{tag}_ky', (x0, -RP - 0.6, 0.01), (x0, RP + 0.6, 0.01), r=0.008)
    disc = F.mat('dial', (0.80, 0.82, 0.86), rough=0.6, spec=0.2)
    for k in range(N):
        p = 2 * math.pi * k / N
        x, y = x0 + RP * math.cos(p), RP * math.sin(p)
        F.obj(f'{tag}_d{k}', F.mesh_of(f'{tag}_d{k}', [disc], lambda bm: F.bm_cylinder(bm, (0, 0, 0), (0, 0, 0.03), 0.27, seg=40)),
              loc=(x, y, 0.03))
        ph = cmath.phase(complex(math.cos(p), math.sin(p))) if chiral else 0.0
        F.vector_arrow(f'{tag}_a{k}', (x - 0.2 * math.cos(ph), y - 0.2 * math.sin(ph), 0.08),
                       (x + 0.2 * math.cos(ph), y + 0.2 * math.sin(ph), 0.08), r=0.022, head=0.09)
    F.anchor('panel', (x0 - RP - 0.35, RP + 0.75, 0))
    F.anchor('below', (x0, -RP - 0.65, 0))
    F.anchor('kx', (x0 + RP + 0.6, 0, 0.01))
    F.anchor('ky', (x0, RP + 0.6, 0.01))


def sample(x0, y0, chiral, tag):
    w, h = 2.0, 1.25
    F.slab(f'{tag}_s', (x0, y0, 0.02), (w, h, 0.04), rgb=(0.84, 0.86, 0.90), radius=0.03)
    if chiral:
        for k, inset in enumerate((0.14, 0.3)):
            a, b = w / 2 - inset, h / 2 - inset
            pts = [(x0 - a, y0 - b, 0.07), (x0 + a, y0 - b, 0.07), (x0 + a, y0 + b, 0.07), (x0 - a, y0 + b, 0.07),
                   (x0 - a, y0 - b + 0.15, 0.07)]
            F.flow(f'{tag}_edge{k}', pts, r=0.02, rgb=F.ACCENT_AQM)
    F.anchor(tag, (x0, y0 - h / 2 - 0.05, 0))


def build():
    F.studio(shadows=False)
    F.PREFIX[0] = 'a'
    pocket(XA, False, 'a')
    F.PREFIX[0] = 'b'
    pocket(XB, True, 'b')
    F.PREFIX[0] = 'c'
    sample(XC, 0.95, False, 'triv')
    sample(XC, -0.95, True, 'chir')
    F.anchor('panel', (XC - 1.2, RP + 0.75, 0))
    F.PREFIX[0] = ''
    F.camera((0.25, 0.05, 0.0), elev=89.9, ortho=12.3, aspect=12.5 / 5.4)


F.main(build, NAME)
