"""Figure s04f05, fig:s04:droplet: angular momentum fixes the radius.

(a) The lowest-Landau-level orbitals |psi_m|^2 = r^(2m) exp(-r^2/2) (l_B = 1), each normalized to the
same peak height, for m = 0, 2, 4, 6, 8, as surfaces of revolution cut open over half a turn so that
the rings can be seen one inside the other; the peak of ring m is at r_m = sqrt(2m). Computed.
(b) The nu = 1 droplet of N = 6 electrons, flat out to R = sqrt(2(N - 1)) and falling off at the edge,
and the nu = 1/3 droplet of the same N, a third of the height and sqrt(3) times wider. Schematic
flat-top profiles with a logistic edge, as in the old figure.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's04f05_droplet'
XA, XB1, XB2 = -4.6, 1.0, 5.4
SR, H = 0.36, 1.2                      # x per l_B, height of a normalized peak
SHADES = [F.srgb(118, 158, 198), F.srgb(160, 190, 222)] * 3


def half_revolution(name, fn, R, rgb, loc, nr=70, nth=48):
    m = F.mat('rev_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.4, emit=0.05, spec=0.4)

    def f(bm):
        rs = [R * i / nr for i in range(nr + 1)]
        rings = [[bm.verts.new((r * math.cos(math.pi * j / nth), r * math.sin(math.pi * j / nth), fn(r)))
                  for j in range(nth + 1)] for r in rs]
        for a, b in zip(rings[:-1], rings[1:]):
            for j in range(nth):
                fc = bm.faces.new((a[j], a[j + 1], b[j + 1], b[j]))
                fc.smooth = True
    return F.obj(name, F.mesh_of(name, [m], f), loc=loc)


def build():
    F.studio()
    for k, mm in enumerate((0, 2, 4, 6, 8)):
        peak = math.sqrt(2 * mm) if mm else 0.0
        norm = (peak ** (2 * mm) * math.exp(-peak * peak / 2)) if mm else 1.0
        fn = lambda r, mm=mm, norm=norm: SR * 0 + H * (((r / SR) ** (2 * mm)) * math.exp(-(r / SR) ** 2 / 2) / norm)
        ob = half_revolution(f'orb{mm}', fn, SR * 6.0, SHADES[k], (XA, 0.6, 0.02))
        ob.rotation_euler = (0, 0, math.pi)          # the open half faces the camera
        F.anchor(f'm{mm}', (XA - SR * peak, 0.6, H + 0.12) if mm else (XA, 0.6, H + 0.12))
    F.axis('a_r', (XA, 0.6, 0.02), (XA + SR * 6.4, 0.6, 0.02), r=0.016, head=0.12)
    F.anchor('ar', (XA + SR * 6.4, 0.6, 0.02))
    F.anchor('apanel', (XA - SR * 6.2, 0.6, H + 0.75))
    # (b) the two droplets, schematic flat tops
    R1 = math.sqrt(2 * 5)
    drop = lambda R, h: (lambda r: h / (1 + math.exp((r / SR - R) / 0.35)))
    F.revolution('nu1', drop(R1, H * 0.95), SR * (R1 + 1.6), F.SURFACE, loc=(XB1, 0.6, 0.02))
    F.revolution('nu3', drop(math.sqrt(3) * R1, H * 0.95 / 3), SR * (math.sqrt(3) * R1 + 1.6), F.SURFACE,
                 loc=(XB2, 0.6, 0.02))
    F.anchor('nu1', (XB1, 0.6, H * 0.95 + 0.12))
    F.anchor('nu3', (XB2, 0.6, H * 0.95 / 3 + 0.25))
    F.anchor('R1', (XB1 + SR * R1, -0.2, 0.0))
    F.anchor('R3', (XB2 + SR * math.sqrt(3) * R1, -0.2, 0.0))
    F.anchor('bpanel', (XB1 - SR * R1 - 0.7, 0.6, H + 0.75))
    F.camera((0.4, 0.6, 0.45), elev=24.0, ortho=15.4, aspect=2.9)


F.main(build, NAME)
