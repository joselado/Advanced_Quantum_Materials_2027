"""Figure s08f06, fig:s08:kondobands: the Kondo lattice bands, from (8.21) per spin in one dimension.

Seen from the front, with eps_k = -2t cos k (t = 1) and the f level at zero. Left, gamma_K = 0: the
conduction band crossing the flat f band at the Fermi level, a translucent plane at E = 0. Right,
gamma_K = 0.5: the two hybridized bands (eps_k +- sqrt(eps_k^2 + 4 gamma_K^2)) / 2 with the gap at the
crossing, the lower band full and the Fermi level inside the gap.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's08f06_kondo_bands'
SX, SZ, Z0 = 0.62, 0.72, 1.8


def panel(x0, g, tag):
    ks = [-math.pi + 2 * math.pi * j / 300 for j in range(301)]
    P = lambda k, e: (x0 + SX * k, 0, Z0 + SZ * e)
    if g == 0:
        F.tube(f'{tag}_c', [P(k, -2 * math.cos(k)) for k in ks], 0.035, F.ACCENT_AQM)
        F.tube(f'{tag}_f', [P(k, 0.0) for k in (ks[0], ks[-1])], 0.035, F.BROKEN)
    else:
        for sgn in (1, -1):
            F.tube(f'{tag}_h{sgn}', [P(k, (-2 * math.cos(k) + sgn * math.sqrt(4 * math.cos(k) ** 2 + 4 * g * g)) / 2) for k in ks],
                   0.035, F.ACCENT_AQM)
    F.slab(f'{tag}_EF', (x0, 0.1, Z0), (2 * SX * math.pi + 0.3, 1.0, 0.015), rgb=F.SITE, alpha=0.12).visible_shadow = False
    F.axis(f'{tag}_ax', P(-math.pi - 0.1, -2.3), P(math.pi + 0.45, -2.3), r=0.016, head=0.13)
    F.axis(f'{tag}_ay', P(-math.pi - 0.1, -2.3), P(-math.pi - 0.1, 2.4), r=0.016, head=0.13)
    F.anchor('k', P(math.pi + 0.45, -2.3))
    F.anchor('E', P(-math.pi - 0.1, 2.4))
    F.anchor('EF', P(math.pi + 0.1, 0.0))
    F.anchor('panel', P(-math.pi - 0.2, 2.6))
    F.anchor('gap', P(0.0, -0.08))


def build():
    F.studio()
    F.PREFIX[0] = 'a'
    panel(-2.75, 0.0, 'a')
    F.PREFIX[0] = 'b'
    panel(2.75, 0.5, 'b')
    F.PREFIX[0] = ''
    F.camera((0.15, 0.0, Z0 + 0.05), elev=3.0, ortho=11.6, aspect=12.5 / 5.2)


F.main(build, NAME)
