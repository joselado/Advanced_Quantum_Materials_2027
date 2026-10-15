"""Figure s07f03, fig:s07:ceiling: what an MPS of bond dimension M can represent.

Seen from the front, the entropy in bits, S / log 2, against the block length l from 0 to 40. A
gapped chain, S = 2 (1 - exp(-l / 3)), saturating; a critical chain with c = 1, (c/3) log2(l) + 0.7,
growing as a logarithm and crossing the lower ceiling near l = 15; a generic state, S = l, the
volume law; and two horizontal translucent slabs at S = log2 M for M = 4 and M = 16, the ceilings
of two bond dimensions. The gapped curve saturates at 1.5 bits. Schematic, not fits.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's07f03_entropyceiling'
SX, SZ = 0.16, 0.62                    # x per site, height per bit
LMAX = 40


def build():
    F.studio()
    ls = [0.05 + LMAX * j / 400 for j in range(401)]
    P = lambda l, s: (SX * l - 3.2, 0, 0.3 + SZ * s)
    F.tube('gapped', [P(l, 1.5 * (1 - math.exp(-l / 3))) for l in ls], 0.035, F.ACCENT_AQM)
    F.tube('critical', [P(l, max(0.0, math.log2(max(l, 1)) / 3 + 0.7 * min(l, 1))) for l in ls], 0.035, F.SURFACE)
    F.tube('volume', [P(l, l) for l in ls if l <= 5.6], 0.035, F.BROKEN)
    for k, (m, a) in enumerate(((4, 0.2), (16, 0.2))):
        s = math.log2(m)
        F.slab(f'ceil{k}', P(LMAX / 2, s), (SX * LMAX, 0.8, 0.02), rgb=F.SITE, alpha=a).visible_shadow = False
        F.anchor(f'M{k}', P(13, s))
    F.axis('ax', P(0, 0), P(LMAX + 3, 0), r=0.016, head=0.13)
    F.axis('ay', P(0, 0), P(0, 6.2), r=0.016, head=0.13)
    F.anchor('l', P(LMAX + 3, 0))
    F.anchor('S', P(0, 6.2))
    F.anchor('gapped', P(LMAX, 1.45))
    F.anchor('critical', P(LMAX, math.log2(LMAX) / 3 + 0.7 + 0.08))
    F.anchor('volume', P(5.6, 5.6))
    F.camera((0.1, 0.0, 2.25), elev=3.0, ortho=7.9, aspect=1.7)


F.main(build, NAME)
