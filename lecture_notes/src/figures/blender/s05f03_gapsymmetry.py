"""Figure s05f03, fig:s05:gapsymmetry: the sign of Delta(k) over the Brillouin zone, by angular momentum.

Five zone tiles, each a height field z = c Delta(k), positive regions raised and blue, negative ones
sunk and warm, so that the nodal lines are where the surface crosses its own base. Square zone
[-pi, pi]^2 for (a) s: 1, (b) extended s: cos kx + cos ky, (c) p: sin kx, (d) d: cos kx - cos ky; and the
hexagonal zone of the triangular lattice (a = 1, corners at K = 4 pi / 3) for (e) f:
sin kx - 2 sin(kx / 2) cos(sqrt3 ky / 2), which changes sign six times around Gamma.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's05f03_gapsymmetry'
XS = (-6.4, -3.2, 0.0, 3.2, 6.4)
HALF = 1.25                            # half side of a square tile in the scene
HZ = 0.32                              # height of |Delta| = 1
POS, NEG = F.srgb(118, 158, 198), F.srgb(214, 150, 132)


def tile(name, x0, delta, rmax, nr=70, nth=240):
    """A polar mesh over the zone, r up to rmax(theta), with each face colored by the sign of Delta."""
    mpos = F.mat('gap_pos', POS, rough=0.45, spec=0.35)
    mneg = F.mat('gap_neg', NEG, rough=0.45, spec=0.35)

    def f(bm):
        center = bm.verts.new((0, 0, HZ * delta(0.0, 0.0)))
        rings = []
        for i in range(1, nr + 1):
            ring = []
            for j in range(nth):
                th = 2 * math.pi * j / nth
                r = rmax(th) * i / nr
                kx, ky = r * math.cos(th), r * math.sin(th)
                ring.append(bm.verts.new((kx * HALF / math.pi, ky * HALF / math.pi, HZ * delta(kx, ky))))
            rings.append(ring)

        def face(vs):
            fc = bm.faces.new(vs)
            fc.smooth = True
            fc.material_index = 0 if sum(v.co.z for v in vs) >= 0 else 1
        for j in range(nth):
            face((center, rings[0][j], rings[0][(j + 1) % nth]))
        for a, b in zip(rings[:-1], rings[1:]):
            for j in range(nth):
                face((a[j], b[j], b[(j + 1) % nth], a[(j + 1) % nth]))
    ob = F.obj(name, F.mesh_of(name, [mpos, mneg], f), loc=(x0, 0, 0.85))
    return ob


def square(th):
    return math.pi / max(abs(math.cos(th)), abs(math.sin(th)))


def hexagon(th):
    K = 4 * math.pi / 3
    return K * math.cos(math.pi / 6) / math.cos(((th % (math.pi / 3)) - math.pi / 6))


DELTAS = [
    ('s', lambda kx, ky: 1.0, square),
    ('ext', lambda kx, ky: math.cos(kx) + math.cos(ky), square),
    ('p', lambda kx, ky: math.sin(kx), square),
    ('d', lambda kx, ky: math.cos(kx) - math.cos(ky), square),
    ('f', lambda kx, ky: (math.sin(kx) - 2 * math.sin(kx / 2) * math.cos(math.sqrt(3) * ky / 2)) / 1.3, hexagon),
]


def build():
    F.studio()
    for k, (x0, (tag, delta, rmax)) in enumerate(zip(XS, DELTAS)):
        tile(f't_{tag}', x0, delta, rmax)
        F.rod(f'post_{tag}', (x0, 0, 0), (x0, 0, 0.85 - HZ * 2.0), r=0.02)
        F.anchor(f'p{"abcde"[k]}', (x0 - HALF - 0.1, HALF + 0.4, 0.85 + HZ))
        F.anchor(f'G{"abcde"[k]}', (x0, 0, 0.85 + HZ * delta(0.0, 0.0) + 0.05))
        if k == 1:
            F.axes_anchors('k', (x0 - HALF, -HALF - 0.35, 0.0), {'x': (x0 - HALF + 0.9, -HALF - 0.35, 0.0), 'y': (x0 - HALF, -HALF + 0.55, 0.0)})
    F.camera((0.0, 0.25, 0.85), elev=40.0, ortho=16.0, aspect=3.4)


F.main(build, NAME)
