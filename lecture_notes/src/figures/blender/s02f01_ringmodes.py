"""Figure s02f01, fig:s02:ring: the eigenstates of the three-site ring are fixed by symmetry.

Left, the ring three times, for n = 0, 1, 2, with the coefficient alpha_j = exp(i 2 pi n j / 3)
of each site as an arrow in the plane, turning by 2 pi n / 3 from one site to the next.
Right, the allowed phases phi_n = 2 pi n / L as balls on a unit circle for L = 3 and L = 5, and
the full circle for L to infinity, which is the first Brillouin zone.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's02f01_ringmodes'
XR = (-6.2, -3.6, -1.0)                # the three rings
XC = (1.9, 4.3, 6.7)                   # the three circles of phases
RR, RC = 0.85, 0.9                     # radius of a ring of sites, of a circle of phases


def circle(name, x0, r, rad, rgb, alpha=1.0, n=96):
    pts = [(x0 + r * math.cos(2 * math.pi * k / n), r * math.sin(2 * math.pi * k / n), 0.06) for k in range(n + 1)]
    return F.tube(name, pts, rad, rgb, alpha=alpha)


def build():
    F.studio()
    for n, x0 in enumerate(XR):
        pos = [(x0 + RR * math.cos(math.pi / 2 + 2 * math.pi * j / 3), RR * math.sin(math.pi / 2 + 2 * math.pi * j / 3))
               for j in range(3)]
        for j, (x, y) in enumerate(pos):
            F.site(f'r{n}_s{j}', (x, y, 0), r=0.2, h=0.05)
            x1, y1 = pos[(j + 1) % 3]
            d = math.hypot(x1 - x, y1 - y)
            ux, uy = (x1 - x) / d, (y1 - y) / d
            F.bond(f'r{n}_b{j}', (x + 0.2 * ux, y + 0.2 * uy, 0.04), (x1 - 0.2 * ux, y1 - 0.2 * uy, 0.04))
            F.phasor(f'r{n}_a{j}', (x, y, 0.32), 2 * math.pi * n * j / 3, length=0.62)
        F.anchor(f'n{n}', (x0, -RR - 0.35, 0))
    for k, (x0, L) in enumerate(zip(XC, (3, 5, None))):
        if L is None:
            circle('c_inf', x0, RC, 0.05, F.ACCENT_AQM)
        else:
            circle(f'c{L}', x0, RC, 0.018, F.BOND)
            for m in range(L):
                a = 2 * math.pi * m / L
                F.ball(f'c{L}_{m}', (x0 + RC * math.cos(a), RC * math.sin(a), 0.1), 0.11, rgb=F.ACCENT_AQM)
        F.rod(f'c{k}_re', (x0 - RC - 0.25, 0, 0.02), (x0 + RC + 0.25, 0, 0.02), r=0.012)
        F.rod(f'c{k}_im', (x0, -RC - 0.25, 0.02), (x0, RC + 0.25, 0.02), r=0.012)
        F.anchor(f'L{k}', (x0, -RC - 0.35, 0))
    F.anchor('one', (XC[0] + RC + 0.12, 0, 0.1))
    F.anchor('BZ', (XC[2], RC + 0.35, 0.1))
    F.camera((0.2, 0.0, 0.0), elev=45.0, ortho=15.4, aspect=4.0)


F.main(build, NAME)
