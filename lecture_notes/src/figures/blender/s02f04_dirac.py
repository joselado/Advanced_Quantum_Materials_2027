"""Figure s02f04, fig:s02:dirac: three bond vectors, one cancellation, two cones.

(a) A honeycomb patch built as a triangular lattice a1 = (sqrt3, 0), a2 = (sqrt3/2, 3/2) with the
    basis A at 0 and B at delta_1, and the three vectors delta_j from one A site.
(b) The three phasors exp(i k.delta_j) placed one after the other in the complex plane: at
    K = (4 pi / 3 sqrt3, 0) they close a triangle, f(K) = 0; at the generic k = K + (-0.55, 0.45)
    they do not, and the gap between the end and the start is |f(k)|.
(c) The hexagonal Brillouin zone as a tile with the two cones E = +-v|q| standing at K and K'.
Two renders: (a) and (b) from straight above, (c) tilted.
"""
import cmath
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's02f04_dirac'
XA, XB1, XB2, XC = -5.0, -1.0, 1.9, 5.5
S3 = math.sqrt(3)
DELTA = [(0.0, 1.0), (S3 / 2, -0.5), (-S3 / 2, -0.5)]
A1, A2 = (S3, 0.0), (S3 / 2, 1.5)
SL = 0.9                                # scale of the lattice
B_GREY = (0.55, 0.57, 0.62)


def honeycomb():
    sites = {}
    for i in range(-3, 4):
        for j in range(-3, 4):
            ax, ay = i * A1[0] + j * A2[0], i * A1[1] + j * A2[1]
            for tag, (dx, dy) in (('A', (0, 0)), ('B', DELTA[0])):
                x, y = ax + dx, ay + dy
                if x * x / 7.0 + y * y / 4.2 < 1.0:
                    sites[(tag, i, j)] = (x, y)
    drawn = set()
    for (tag, i, j), (x, y) in sites.items():
        p = (XA + SL * x, 0.9 + SL * y, 0)
        if tag == 'A':
            F.site(f'A{i}{j}', p, r=0.13, h=0.05)
            for d in DELTA:
                q = (x + d[0], y + d[1])
                if any(abs(q[0] - v[0]) + abs(q[1] - v[1]) < 1e-6 for k, v in sites.items() if k[0] == 'B'):
                    F.bond(f'b{i}{j}{d}', (p[0] + SL * d[0] * 0.2, p[1] + SL * d[1] * 0.2, 0.03),
                           (p[0] + SL * d[0] * 0.8, p[1] + SL * d[1] * 0.8, 0.03), r=0.02)
        else:
            F.obj(f'B{i}{j}', F.mesh_of(f'B{i}{j}', [F.mat('siteB', B_GREY, rough=0.5, spec=0.3)],
                  lambda bm: F.bm_cylinder(bm, (0, 0, 0), (0, 0, 0.05), 0.13, seg=40)), loc=p)
    o = (XA, 0.9, 0.12)
    for k, d in enumerate(DELTA):
        F.vector_arrow(f'delta{k}', o, (o[0] + SL * d[0], o[1] + SL * d[1], 0.12), r=0.03)
        F.anchor(f'd{k + 1}', (o[0] + SL * 1.25 * d[0], o[1] + SL * 1.25 * d[1], 0.12))
    F.anchor('A', (o[0] - 0.18, o[1] - 0.12, 0.1))


def phasors(x0, k, tag):
    o = complex(x0 - 0.35, 0.55)
    p = o
    for j, d in enumerate(DELTA):
        z = cmath.exp(1j * (k[0] * d[0] + k[1] * d[1])) * 1.2
        F.vector_arrow(f'{tag}_ph{j}', (p.real, p.imag, 0.06), ((p + z).real, (p + z).imag, 0.06), r=0.028)
        p += z
    F.rod(f'{tag}_re', (x0 - 1.0, 0.55, 0.02), (x0 + 1.25, 0.55, 0.02), r=0.01)
    F.rod(f'{tag}_im', (x0 - 0.35, -0.2, 0.02), (x0 - 0.35, 2.1, 0.02), r=0.01)
    F.ball(f'{tag}_start', (o.real, o.imag, 0.06), 0.06, rgb=F.SITE)
    if abs(p - o) > 0.05:
        F.marker(f'{tag}_end', (p.real, p.imag, 0.06), kind='ghost', r=0.08, rgb=F.BROKEN)
    F.anchor(tag, (x0, -0.55, 0))
    F.axes_anchors(tag + 'ax', (x0 - 0.35, 0.55, 0.02), {'re': (x0 + 1.25, 0.55, 0.02), 'im': (x0 - 0.35, 2.1, 0.02)})
    return abs(p - o) / 1.2


def build_ab():
    F.studio(shadows=False)
    F.PREFIX[0] = 'a'
    honeycomb()
    F.anchor('panel', (XA - 1.95, 2.75, 0.0))
    F.axes_anchors('r', (XA - 1.85, -0.75, 0.0), {'x': (XA - 1.15, -0.75, 0.0), 'y': (XA - 1.85, -0.05, 0.0)})
    F.PREFIX[0] = 'b'
    K = (4 * math.pi / (3 * S3), 0.0)
    print('|f(K)| =', phasors(XB1, K, 'K'))
    print('|f(k)| =', phasors(XB2, (K[0] - 0.55, 0.45), 'k'))
    F.anchor('panel', (XB1 - 1.2, 2.75, 0.0))
    F.PREFIX[0] = ''
    F.camera((-1.55, 0.75, 0.0), elev=89.9, ortho=10.9, aspect=10.9 / 4.55)


def build_c():
    F.studio()
    yc, zc, rz = 0.95, 0.75, 1.15
    hexagon = [(XC + rz * math.cos(math.pi * m / 3), yc + rz * math.sin(math.pi * m / 3)) for m in range(6)]
    tile = F.mat('bz', (0.80, 0.82, 0.87), rough=0.6, spec=0.3)

    def hexmesh(bm):
        top = [bm.verts.new((x - XC, y - yc, 0.0)) for x, y in hexagon]
        bm.faces.new(top)
        bot = [bm.verts.new((x - XC, y - yc, -0.04)) for x, y in hexagon]
        bm.faces.new(list(reversed(bot)))
        for m in range(6):
            bm.faces.new((top[m], bot[m], bot[(m + 1) % 6], top[(m + 1) % 6]))
    F.obj('bz', F.mesh_of('bz', [tile], hexmesh), loc=(XC, yc, zc))
    F.rod('bz_post', (XC, yc, 0), (XC, yc, zc - 0.04), r=0.025)
    for m, lab in ((0, 'K'), (1, 'Kp')):
        x, y = hexagon[m]
        for sgn in (1, -1):
            F.obj(f'cone{m}{sgn}', F.mesh_of(f'cone{m}{sgn}', [F.mat('cone', F.ACCENT_AQM, rough=0.4, emit=0.05)],
                  lambda bm: F.bm_cylinder(bm, (0, 0, sgn * 0.5), (0, 0, 0.0), 0.26, 0.0, seg=48)),
                  loc=(x, y, zc))
        F.anchor(lab, (x + 0.2 * math.cos(math.pi * m / 3), y + 0.2 * math.sin(math.pi * m / 3), zc + 0.52))
    F.anchor('Gamma', (XC, yc, zc + 0.02))
    F.axes_anchors('k', (XC, yc, zc + 0.01), {'x': (XC + rz + 0.55, yc, zc + 0.01), 'y': (XC, yc + rz + 0.45, zc + 0.01)})
    F.anchor('panel', (XC - 1.75, yc + 1.2, zc + 0.7))
    F.camera((XC + 0.1, yc, zc + 0.15), elev=35.0, ortho=4.1, aspect=4.9 / 4.55)


F.main_panels(NAME, [('ab', build_ab), ('c', build_c)])
