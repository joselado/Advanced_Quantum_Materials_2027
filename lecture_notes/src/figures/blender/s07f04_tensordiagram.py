"""Figure s07f04, fig:s07:tensors: tensor diagrams, the MPS, and the MPO applied to it.

Seen from the front. (a) A scalar (a tensor with no legs), a vector (one leg), a matrix (two legs),
and a contraction, two tensors joined along a shared leg. (b) The exact coefficient tensor, one big
block with L = 6 physical legs, and next to it the MPS, a chain of six small tensors with one physical
leg down each and virtual bonds between them. (c) The MPO, a row of darker tensors with two physical
legs each, placed on top of the MPS so that the shared legs are contracted; the bonds of the result
are thicker, M times D, before the truncation brings them back to M.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s07 as G                                                    # noqa: E402

NAME = 's07f04_tensordiagram'


def build():
    F.studio()
    # (a) notation
    xa = -6.6
    z = 1.6
    G.T('a_sc', xa, z, s=0.45)
    G.T('a_vec', xa + 1.1, z, s=0.45)
    G.leg('a_vl', (xa + 1.1, z - 0.22), (xa + 1.1, z - 0.8))
    G.T('a_mat', xa + 2.2, z, s=0.45)
    G.leg('a_ml', (xa + 1.75, z), (xa + 1.98, z))
    G.leg('a_mr', (xa + 2.42, z), (xa + 2.65, z))
    G.T('a_c1', xa + 0.6, z - 1.6, s=0.45)
    G.T('a_c2', xa + 1.7, z - 1.6, s=0.45)
    G.leg('a_cl', (xa + 0.82, z - 1.6), (xa + 1.48, z - 1.6), rgb=F.ACCENT_AQM, r=0.05)
    G.leg('a_c1d', (xa + 0.6, z - 1.82), (xa + 0.6, z - 2.3))
    G.leg('a_c2d', (xa + 1.7, z - 1.82), (xa + 1.7, z - 2.3))
    for k, (lab, x) in enumerate((('sc', xa), ('vec', xa + 1.1), ('mat', xa + 2.2))):
        F.anchor(lab, (x, 0, z + 0.35))
    F.anchor('con', (xa + 1.15, 0, z - 1.25))
    F.anchor('pa', (xa - 0.4, 0, 2.55))
    # (b) the coefficient tensor and the MPS
    xb = -2.3
    big = G.T('b_big', xb, 1.65, s=0.5)
    big.scale = (3.4, 1.0, 1.1)
    for k in range(6):
        x = xb - 0.7 + 0.28 * k
        G.leg(f'b_bl{k}', (x, 1.38), (x, 0.95))
    F.anchor('big', (xb, 0, 2.05))
    for k in range(6):
        x = xb - 1.05 + 0.42 * k
        G.T(f'b_m{k}', x, 0.2, s=0.3)
        G.leg(f'b_ml{k}', (x, 0.05), (x, -0.3))
        if k < 5:
            G.leg(f'b_mb{k}', (x + 0.15, 0.2), (x + 0.27, 0.2), r=0.035)
    F.anchor('mps', (xb, 0, -0.35))
    F.anchor('arrow0', (xb, 0, 0.85))
    F.anchor('arrow1', (xb, 0, 0.5))
    F.anchor('pb', (xb - 1.6, 0, 2.55))
    # (c) the MPO on the MPS
    xc = 2.1
    for k in range(6):
        x = xc + 0.8 * k
        G.T(f'c_m{k}', x, 0.4, s=0.42)
        G.T(f'c_o{k}', x, 1.4, s=0.42, rgb=G.OPER)
        G.leg(f'c_pl{k}', (x, 0.62), (x, 1.18), rgb=F.ACCENT_AQM, r=0.045)
        G.leg(f'c_up{k}', (x, 1.62), (x, 2.05))
        if k < 5:
            G.leg(f'c_mb{k}', (x + 0.21, 0.4), (x + 0.59, 0.4), r=0.035)
            G.leg(f'c_ob{k}', (x + 0.21, 1.4), (x + 0.59, 1.4), r=0.035)
    F.anchor('mpo', (xc - 0.35, 0, 1.4))
    F.anchor('state', (xc - 0.35, 0, 0.4))
    F.anchor('trunc', (xc + 2.0, 0, -0.15))
    F.anchor('pc', (xc - 0.5, 0, 2.55))
    F.camera((0.0, 0.0, 1.05), elev=8.0, ortho=14.4, aspect=3.1)


F.main(build, NAME)
