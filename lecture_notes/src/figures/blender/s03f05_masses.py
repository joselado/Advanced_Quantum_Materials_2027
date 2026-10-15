"""Figure s03f05, fig:s03:masses: two masses for the honeycomb Dirac cones, on the lattice and on a ribbon.

Two renders. (a) Top, seen from above: the honeycomb patch with a staggered potential, the A sites
(+m) as large dark discs and the B sites (-m) as small light ones; bottom-left in the spectra render, its zigzag ribbon spectrum, m = 0.5, with a
gap and nothing in it (the zigzag edge bands sit at the gap edges +-m). (b) Top: the honeycomb patch
with the Haldane second-neighbor hoppings t2 exp(+-i pi/2) as arrows circulating around one hexagon,
on both sublattices in the same sense; its ribbon spectrum, t2 = 0.1, with one branch per edge
crossing the gap. The ribbons are 16 unit cells wide, with first-neighbor hopping -1, and the
states with more than 60 percent of their weight in the outer 4 cells of an edge, inside the gap,
are drawn in the accent color, the top edge dark and the bottom edge light.
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's03f05_masses'
S3 = math.sqrt(3)
XA, XB = -3.9, 3.9                     # the two columns of spectra
LA, LB = -3.2, 4.6                     # the two lattice patches, shifted right to leave room for the labels
NB = 8                                 # bands drawn on each side of zero


def ribbon(W, m=0.0, t2=0.0, phi=math.pi / 2, nk=181):
    a2, basis = np.array([0.5, S3 / 2]), [np.zeros(2), np.array([0.0, 1 / S3])]
    pos = np.array([n * a2 + b for n in range(W) for b in basis])
    sub = np.array([s for n in range(W) for s in (0, 1)])
    N = len(pos)
    img = lambda i, sh: pos[i] + np.array([sh, 0.0])
    hops = []
    for i in range(N):
        for j in range(N):
            for sh in range(-2, 3):
                d = np.linalg.norm(img(j, sh) - pos[i])
                if abs(d - 1 / S3) < 1e-6:
                    hops.append((i, j, sh, -1.0))
                elif abs(d - 1) < 1e-6 and t2:
                    # nu = +1 when the hop turns left at the shared neighbor: along 0, 120 and 240
                    # degrees from an A site, and the opposite from a B site
                    v = img(j, sh) - pos[i]
                    a = math.atan2(v[1], v[0]) / (2 * math.pi / 3)
                    nu = (1 if abs(a - round(a)) < 1e-6 else -1) * (1 if sub[i] == 0 else -1)
                    hops.append((i, j, sh, t2 * np.exp(1j * nu * phi)))
    ks = np.linspace(0, 2 * np.pi, nk)
    E, top, bot = [], [], []
    for k in ks:
        h = np.zeros((N, N), complex)
        for i, j, sh, a in hops:
            h[i, j] += a * np.exp(1j * k * sh)
        h += np.diag(m * np.where(sub == 0, 1.0, -1.0))
        e, v = np.linalg.eigh(h)
        w = np.abs(v) ** 2
        E.append(e), bot.append(w[:8].sum(0)), top.append(w[-8:].sum(0))
    return ks, np.array(E), np.array(top), np.array(bot)


def patch(x0, tag):
    fits = lambda x, y: (x * x) / 2.9 + (y - 0.3) ** 2 / 1.0 < 1.0
    A, B, bonds = F.honeycomb(fits, bond=0.5)
    return [(x0 + x, 1.0 + y) for x, y in A], [(x0 + x, 1.0 + y) for x, y in B], \
        [((x0 + a[0], 1.0 + a[1]), (x0 + b[0], 1.0 + b[1])) for a, b in bonds]


def build_lattices():
    F.studio()
    # (a) staggered potential: +m on A, the large dark discs, -m on B, the small light ones
    A, B, bonds = patch(LA, 'a')
    light = F.mat('siteB', (0.62, 0.64, 0.70), rough=0.5, spec=0.3)
    for k, (x, y) in enumerate(A):
        F.site(f'a_A{k}', (x, y, 0), r=0.13, h=0.04)
    for k, (x, y) in enumerate(B):
        F.obj(f'a_B{k}', F.mesh_of(f'a_B{k}', [light], lambda bm: F.bm_cylinder(bm, (0, 0, 0), (0, 0, 0.04), 0.075,
                                                                                   seg=40)), loc=(x, y, 0))
    for k, ((x1, y1), (x2, y2)) in enumerate(bonds):
        F.bond(f'a_b{k}', (x1, y1, 0.03), (x2, y2, 0.03), r=0.014)
    F.anchor('a', (LA - 1.8, 1.3, 0))
    # (b) the Haldane coupling: arrows circulating around one hexagon on both sublattices
    A, B, bonds = patch(LB, 'b')
    for k, (x, y) in enumerate(A + B):
        F.site(f'b_s{k}', (x, y, 0), r=0.1, h=0.04)
    for k, ((x1, y1), (x2, y2)) in enumerate(bonds):
        F.bond(f'b_b{k}', (x1, y1, 0.03), (x2, y2, 0.03), r=0.014)
    cx, cy = LB + S3 * 0.25, 1.0 + 0.25            # the center of a hexagon next to the A site at the origin
    hexa = sorted([p for p in A + B if abs(math.dist(p, (cx, cy)) - 0.5) < 1e-6],
                  key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
    for sub in (0, 1):
        tri = [p for p in hexa if (p in A) == (sub == 0)]
        tri.sort(key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
        for j in range(3):
            p, q = tri[j], tri[(j + 1) % 3]
            sh = 0.12
            u = ((q[0] - p[0]), (q[1] - p[1]))
            L = math.hypot(*u)
            pts = [(p[0] + u[0] * s, p[1] + u[1] * s, 0.12 + 0.18 * math.sin(math.pi * s) + 0.06 * sub)
                   for s in [0.12 + 0.76 * k / 20 for k in range(21)]]
            F.flow(f'b_t2_{sub}{j}', pts, r=0.018, rgb=F.ACCENT_AQM)
    F.anchor('t2', (cx + 0.75, cy + 0.2, 0.3))
    F.anchor('b', (LB - 1.8, 1.3, 0))
    F.axes_anchors('r', (LA + 1.9, 0.0, 0.0), {'x': (LA + 2.6, 0.0, 0.0), 'y': (LA + 1.9, 0.7, 0.0)})
    F.camera((0.0, 1.3, 0.0), elev=89.9, ortho=15.6, aspect=15.6 / 2.4)


def spectrum(x0, tag, **kw):
    ks, E, top, bot = ribbon(16, **kw)
    n = E.shape[1]
    sx, sz, z0 = 0.55, 0.7, 1.35
    P = lambda k, e: (x0 + sx * (k - math.pi), 0, z0 + sz * e)
    for b in range(n // 2 - NB, n // 2 + NB):
        F.tube(f'{tag}_band{b}', [P(k, e) for k, e in zip(ks, E[:, b])], 0.015, (0.42, 0.43, 0.48))
    gap = 0.42
    for wts, rgb, side in ((top, F.ACCENT_AQM, 't'), (bot, F.SURFACE, 'b')):
        for b in range(n // 2 - 2, n // 2 + 2):
            seg = []
            for k, e, w in zip(ks, E[:, b], wts[:, b]):
                if w > 0.6 and abs(e) < gap:
                    seg.append(P(k, e))
                elif seg:
                    if len(seg) > 2:
                        F.tube(f'{tag}_{side}{b}_{len(seg)}_{seg[0][0]:.2f}', seg, 0.03, rgb)
                    seg = []
            if len(seg) > 2:
                F.tube(f'{tag}_{side}{b}_{len(seg)}_end', seg, 0.03, rgb)
    F.axis(f'{tag}_ay', (x0 - sx * math.pi, 0, z0 - 1.45 * sz), (x0 - sx * math.pi, 0, z0 + 1.55 * sz), r=0.016, head=0.13)
    F.rod(f'{tag}_ax', (x0 - sx * math.pi, 0, z0 - 1.45 * sz), (x0 + sx * math.pi, 0, z0 - 1.45 * sz), r=0.016)
    F.anchor('E', (x0 - sx * math.pi, 0, z0 + 1.55 * sz))
    F.anchor('k0', (x0 - sx * math.pi, 0, z0 - 1.5 * sz))
    F.anchor('k2pi', (x0 + sx * math.pi, 0, z0 - 1.5 * sz))
    F.anchor('kx', (x0, 0, z0 - 1.5 * sz))
    print(tag, 'min |E| =', np.abs(E).min().round(4))


def build_spectra():
    F.studio()
    F.PREFIX[0] = 'a'
    spectrum(XA, 'a', m=0.5)
    F.PREFIX[0] = 'b'
    spectrum(XB, 'b', t2=0.1)
    F.PREFIX[0] = ''
    F.camera((0.0, 0.0, 1.32), elev=5.0, ortho=15.6, aspect=15.6 / 2.5)


F.main_panels(NAME, [('lat', build_lattices), ('spec', build_spectra)])
