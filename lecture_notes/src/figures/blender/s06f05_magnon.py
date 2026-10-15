"""Figure s06f05, fig:s06:magnon: what a magnon is in real space.

Two renders. Left, seen from the side: (a) behind, the ferromagnetic chain with every arrow up;
(b) in front, one magnon, every arrow tilted by 35 degrees from z on its cone (a ghost cone), with
the precession phase advancing by k delta = 45 degrees from site to site, so that eight sites make
one wavelength. Right, seen from above: the same magnon chain, where the transverse component turns
at a constant rate. The tilt is much larger than in reality.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's06f05_magnon'
L, STEP = 9, 1.0
TILT = math.radians(35)
X0 = -(L - 1) * STEP / 2


def cone(name, loc, h, r):
    m = F.ghost('cone_ghost', F.BOND, 0.18)
    x, y, z = loc
    return F.obj(name, F.mesh_of(name, [m], lambda bm: F.bm_cylinder(bm, (0, 0, h), (0, 0, 0), r, 0.0, seg=40,
                                                                      caps=False)), loc=loc)


def magnon_chain(y, tag, top_view=False):
    for n in range(L):
        x = X0 + n * STEP
        F.site(f'{tag}_s{n}', (x, y, 0), r=0.26)
        if n < L - 1:
            F.bond(f'{tag}_b{n}', (x + 0.26, y, 0.05), (x + STEP - 0.26, y, 0.05))
        ph = math.radians(45 * n)
        d = (math.sin(TILT) * math.cos(ph), math.sin(TILT) * math.sin(ph), math.cos(TILT))
        Lr = 0.85
        if not top_view:
            cone(f'{tag}_cone{n}', (x, y, 0.1), Lr * math.cos(TILT), Lr * math.sin(TILT))
        F.sz_arrow(f'{tag}_a{n}', (x + d[0] * Lr / 2, y + d[1] * Lr / 2, 0.1 + d[2] * Lr / 2), d, length=Lr)


def build_side():
    F.studio()
    for n in range(L):
        x = X0 + n * STEP
        F.site(f'f_s{n}', (x, 4.6, 0), r=0.26)
        if n < L - 1:
            F.bond(f'f_b{n}', (x + 0.26, 4.6, 0.05), (x + STEP - 0.26, 4.6, 0.05))
        F.arrow(f'f_a{n}', (x, 4.6, 0.1 + 0.425), (0, 0, 1), length=0.85)
    magnon_chain(0.0, 'm')
    F.anchor('a', (X0 - 0.5, 4.6, 1.3))
    F.anchor('b', (X0 - 0.5, 0.0, 1.3))
    F.anchor('lam', (0, -0.5, 0))
    F.camera((0.0, 2.3, 0.75), elev=22.0, ortho=9.8, aspect=10.0 / 4.6)


def build_top():
    F.studio(shadows=False)
    magnon_chain(0.0, 't', top_view=True)
    F.anchor('top', (X0 - 0.4, 0.75, 0))
    F.camera((0.0, 0.0, 0.0), elev=89.9, ortho=9.6, aspect=5.4 / 1.6)


F.main_panels(NAME, [('side', build_side), ('top', build_top)])
