"""Figure s04f03, fig:s04:guidingcenter: why the Landau levels are flat.

Seen from the front, in units of hbar omega_c and l_B. (a) Three wells V = (x - x0)^2 / 2 for
x0 = k_y = -2, 0, 2, the middle one in the accent color and the two others as ghosts; inside each
the same levels E_n = n + 1/2, n = 0..3, as rods across the well, and on the lowest level the ground
state |psi_0|^2 = exp(-(x - x0)^2) / sqrt(pi) as a bump. (b) The same levels as bands over k_y, with
the three values of k_y of (a) marked.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's04f03_guidingcenter'
XA, XB = -2.9, 4.3                     # centers of the two panels
SX, SZ, Z0 = 0.62, 0.62, 0.35          # x per l_B, height per hbar omega_c, height of E = 0
EMAX = 4.2
KS = (-2.0, 0.0, 2.0)


def build():
    F.studio()
    for k, x0 in enumerate(KS):
        main = x0 == 0.0
        rgb = F.ACCENT_AQM
        alpha = 1.0 if main else 0.45
        y = 0.0 if main else 0.15
        h = math.sqrt(2 * EMAX)
        F.tube(f'well{k}', [(XA + SX * (x0 + u), y, Z0 + SZ * u * u / 2) for u in [-h + 2 * h * j / 120 for j in range(121)]],
               0.03, rgb, alpha=alpha)
        F.tube(f'psi{k}', [(XA + SX * (x0 + u), y - 0.05, Z0 + SZ * (0.5 + 1.1 * math.exp(-u * u) / math.sqrt(math.pi) * 1.6))
                           for u in [-2.2 + 4.4 * j / 80 for j in range(81)]], 0.025, F.BROKEN, alpha=1.0 if main else 0.4)
        F.anchor(f'x{k}', (XA + SX * x0, 0, Z0 - 0.2))
    for n in range(4):                             # the shared ladder, the same for every well
        F.tube(f'lev{n}', [(XA - SX * 4.8, 0.3, Z0 + SZ * (n + 0.5)), (XA + SX * 4.8, 0.3, Z0 + SZ * (n + 0.5))], 0.014,
               F.SITE).visible_shadow = False
    F.axis('a_ax', (XA - SX * 5.0, 0, Z0 - 0.12), (XA + SX * 5.2, 0, Z0 - 0.12), r=0.018, head=0.14)
    F.axis('a_ay', (XA - SX * 5.0, 0, Z0 - 0.12), (XA - SX * 5.0, 0, Z0 + SZ * 4.6), r=0.018, head=0.14)
    F.anchor('ax', (XA + SX * 5.2, 0, Z0 - 0.12))
    F.anchor('aE', (XA - SX * 5.0, 0, Z0 + SZ * 4.6))
    F.anchor('apanel', (XA - SX * 5.0 - 0.1, 0, Z0 + SZ * 5.0))
    for n in range(4):
        F.anchor(f'E{n}', (XA - SX * 5.0, 0, Z0 + SZ * (n + 0.5)))
    # (b) flat bands over k_y
    W = 2.2
    for n in range(4):
        F.tube(f'band{n}', [(XB - W, 0, Z0 + SZ * (n + 0.5)), (XB + W, 0, Z0 + SZ * (n + 0.5))], 0.03, F.ACCENT_AQM)
    for k, x0 in enumerate(KS):
        F.marker(f'mk{k}', (XB + W * x0 / 3.0, -0.05, Z0 + SZ * 0.5), kind='ball' if x0 == 0 else 'ghost', r=0.08,
                 rgb=F.BROKEN)
        F.anchor(f'k{k}', (XB + W * x0 / 3.0, 0, Z0 - 0.2))
    F.axis('b_ax', (XB - W - 0.2, 0, Z0 - 0.12), (XB + W + 0.35, 0, Z0 - 0.12), r=0.018, head=0.14)
    F.axis('b_ay', (XB - W - 0.2, 0, Z0 - 0.12), (XB - W - 0.2, 0, Z0 + SZ * 4.6), r=0.018, head=0.14)
    F.anchor('bx', (XB + W + 0.35, 0, Z0 - 0.12))
    F.anchor('bE', (XB - W - 0.2, 0, Z0 + SZ * 4.6))
    F.anchor('bpanel', (XB - W - 0.3, 0, Z0 + SZ * 5.0))
    F.camera((0.65, 0.0, Z0 + SZ * 2.35), elev=3.0, ortho=15.0, aspect=3.0)


F.main(build, NAME)
