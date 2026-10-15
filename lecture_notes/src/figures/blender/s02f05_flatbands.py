"""Figure s02f05, fig:s02:flatbands: flat bands from geometry, the Lieb and the kagome lattice.

(a) The Lieb lattice, a square lattice with one site in four removed, and (b) its three bands from
the Bloch Hamiltonian with H = -t sum c^dag c, t = 1, along Gamma-X-M-Gamma: flat at 0, all three
touching at M. (c) The kagome lattice and (d) its bands along Gamma-K-M-Gamma: a Dirac-like
crossing at K at -t and the flat band at +2t. (e) One kagome hexagon carrying the localized state,
amplitudes +1 and -1 alternating around it as balls above and below a raised plate; the two hops
onto an outside site arrive with opposite sign and cancel, marked by the cross.
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's02f05_flatbands'
XS = (-6.9, -3.75, -0.35, 2.85, 6.4)   # the five panels
S3 = math.sqrt(3)
W, SZ = 2.4, 0.36                      # width of a band panel, height per unit of t
Z0 = 1.75                              # height of E = 0 in the band panels
FLAT = F.BROKEN


def lieb_h(k):
    a, b = -2 * math.cos(k[0] / 2), -2 * math.cos(k[1] / 2)
    return np.array([[0, a, b], [a, 0, 0], [b, 0, 0]])


def kagome_h(k):
    a1, a2 = np.array([1.0, 0.0]), np.array([0.5, S3 / 2])
    c = lambda v: -2 * math.cos(k @ v / 2)
    return np.array([[0, c(a1), c(a2)], [c(a1), 0, c(a2 - a1)], [c(a2), c(a2 - a1), 0]])


def path(points, n=120):
    ks, xs, total = [], [], 0.0
    lens = [np.linalg.norm(np.array(b) - np.array(a)) for a, b in zip(points[:-1], points[1:])]
    for (a, b), L in zip(zip(points[:-1], points[1:]), lens):
        m = max(2, int(n * L / sum(lens)))
        for j in range(m):
            ks.append(np.array(a) + (np.array(b) - np.array(a)) * j / m)
            xs.append((total + L * j / m) / sum(lens))
        total += L
    ks.append(np.array(points[-1])), xs.append(1.0)
    return ks, xs, [sum(lens[:i]) / sum(lens) for i in range(len(points))]


def bands(x0, hfun, points, labels, flat, tag):
    ks, xs, ticks = path(points)
    es = np.array([np.linalg.eigvalsh(hfun(k)) for k in ks])
    for b in range(3):
        isflat = np.ptp(es[:, b]) < 1e-9
        F.tube(f'{tag}_b{b}', [(x0 - W / 2 + W * x, 0, Z0 + SZ * e) for x, e in zip(xs, es[:, b])],
               0.035, FLAT if isflat else F.ACCENT_AQM)
    F.axis(f'{tag}_ay', (x0 - W / 2, 0, Z0 - 4.3 * SZ), (x0 - W / 2, 0, Z0 + 3.2 * SZ), r=0.018, head=0.14)
    F.rod(f'{tag}_ax', (x0 - W / 2, 0, Z0 - 4.3 * SZ), (x0 + W / 2, 0, Z0 - 4.3 * SZ), r=0.018)
    for t, lab in zip(ticks, labels):
        F.rod(f'{tag}_t{lab}', (x0 - W / 2 + W * t, 0, Z0 - 4.3 * SZ), (x0 - W / 2 + W * t, 0, Z0 + 3.0 * SZ), r=0.006)
        F.anchor(lab, (x0 - W / 2 + W * t, 0, Z0 - 4.35 * SZ))
    F.anchor('E', (x0 - W / 2, 0, Z0 + 3.2 * SZ))
    F.anchor('flat', (x0 + W / 2 + 0.05, 0, Z0 + SZ * flat))
    print(tag, 'band ranges', np.round(es.min(0), 3), np.round(es.max(0), 3))


def lattice(x0, sites, bonds, tag, sl):
    for k, (x, y) in enumerate(sites):
        F.site(f'{tag}_s{k}', (x0 + sl * x, 1.0 + sl * y, 0), r=0.11, h=0.04)
    for k, (i, j) in enumerate(bonds):
        (x1, y1), (x2, y2) = sites[i], sites[j]
        F.bond(f'{tag}_b{k}', (x0 + sl * (x1 + 0.22 * (x2 - x1)), 1.0 + sl * (y1 + 0.22 * (y2 - y1)), 0.03),
               (x0 + sl * (x2 - 0.22 * (x2 - x1)), 1.0 + sl * (y2 - 0.22 * (y2 - y1)), 0.03), r=0.02)


def neighbors(sites, d):
    return [(i, j) for i in range(len(sites)) for j in range(i + 1, len(sites))
            if abs(math.dist(sites[i], sites[j]) - d) < 1e-6]


def lieb_sites():
    s = []
    for i in range(-2, 3):
        for j in range(-2, 3):
            if i % 2 == 0 or j % 2 == 0:
                s.append((0.5 * i, 0.5 * j))
    return s


def kagome_sites(rmax=1.55):
    a1, a2 = np.array([1.0, 0.0]), np.array([0.5, S3 / 2])
    s = []
    for i in range(-3, 4):
        for j in range(-3, 4):
            for b in (np.zeros(2), a1 / 2, a2 / 2):
                p = i * a1 + j * a2 + b - (a1 + a2) / 2 + np.array([0.0, 0.0])
                if np.linalg.norm(p) < rmax:
                    s.append(tuple(np.round(p, 9)))
    return s


def hexagon(x0):
    """The localized kagome state seen from above: amplitude +1 as a filled ball and -1 as a ghost
    ball on alternating hexagon sites, the six outside sites, and the two hops onto the top outside
    site, which cancel at the cross."""
    rh = 0.7
    hexp = [(x0 + rh * math.cos(math.pi / 6 + math.pi * m / 3), 1.0 + rh * math.sin(math.pi / 6 + math.pi * m / 3))
            for m in range(6)]
    outer = [(x0 + 2 * rh * math.cos(math.pi * m / 3) * S3 / 2,      # beyond the middle of an edge,
              1.0 + 2 * rh * math.sin(math.pi * m / 3) * S3 / 2) for m in range(6)]   # closing its triangle
    for m, (x, y) in enumerate(hexp):
        F.site(f'e_s{m}', (x, y, 0), r=0.1, h=0.03)
        x1, y1 = hexp[(m + 1) % 6]
        F.bond(f'e_b{m}', (x, y, 0.03), (x1, y1, 0.03), r=0.018)
        if m % 2 == 0:
            F.ball(f'e_amp{m}', (x, y, 0.2), 0.14)
        else:
            F.ghost_ball(f'e_amp{m}', (x, y, 0.2), 0.14, alpha=0.3)
        F.anchor(f'amp{m}', (x + 0.24 * (x - x0) / rh, y + 0.24 * (y - 1.0) / rh, 0.2))
    for m, (x, y) in enumerate(outer):
        F.site(f'e_o{m}', (x, y, 0), r=0.08, h=0.03)
        for q in (m, (m + 5) % 6):
            hx, hy = hexp[q]
            F.bond(f'e_ob{m}{q}', (x, y, 0.03), (hx, hy, 0.03), r=0.012)
    ox, oy = outer[0]
    for q in (0, 5):                           # the + and the - site of the edge under outer[0]
        hx, hy = hexp[q]
        F.flow(f'e_hop{q}', [(hx + 0.25 * (ox - hx), hy + 0.25 * (oy - hy), 0.25),
                             (hx + 0.8 * (ox - hx), hy + 0.8 * (oy - hy), 0.25)], r=0.02, rgb=(0.16, 0.20, 0.30))
    F.marker('e_zero', (ox, oy, 0.3), kind='cross', r=0.17, rgb=F.BROKEN)
    F.anchor('zero', (ox + 0.2, oy, 0.3))


H_CM = 4.0                             # height of every panel on the page
WIDTHS = {'a': 2.9, 'b': 3.3, 'c': 2.9, 'd': 3.3, 'e': 2.8}   # widths in cm, with four gaps of 0.1 cm


def cam_flat(ortho, panel, y=1.0):
    F.camera((0.0, y, 0.0), elev=89.9, ortho=ortho, aspect=WIDTHS[panel] / H_CM)


def cam_front(ortho, panel):
    F.camera((0.0, 0.0, Z0 - 0.55 * SZ), elev=3.0, ortho=ortho, aspect=WIDTHS[panel] / H_CM)


def build_a():
    F.studio(shadows=False)
    s = lieb_sites()
    lattice(0.0, s, neighbors(s, 0.5), 'a', 1.15)
    F.anchor('panel', (-1.15, 1.0 + 2.05, 0))
    cam_flat(3.4, 'a')


def build_b():
    F.studio()
    bands(0.0, lieb_h, [(0, 0), (math.pi, 0), (math.pi, math.pi), (0, 0)], ['G1', 'X', 'M', 'G2'], 0.0, 'b')
    F.anchor('panel', (-1.6, 0, Z0 + 4.1 * SZ))
    cam_front(3.55, 'b')


def build_c():
    F.studio(shadows=False)
    s = kagome_sites()
    lattice(0.0, s, neighbors(s, 0.5), 'c', 1.0)
    F.anchor('panel', (-1.15, 1.0 + 2.05, 0))
    cam_flat(3.4, 'c')


def build_d():
    F.studio()
    bands(0.0, kagome_h, [(0, 0), (4 * math.pi / 3, 0), (math.pi, math.pi / S3), (0, 0)],
          ['G1', 'K', 'M', 'G2'], 2.0, 'd')
    F.anchor('panel', (-1.6, 0, Z0 + 4.1 * SZ))
    cam_front(3.55, 'd')


def build_e():
    F.studio(shadows=False)
    hexagon(0.0)
    F.anchor('panel', (-1.55, 1.0 + 2.15, 1.0))
    cam_flat(4.7, 'e')                          # a portrait camera: the ortho scale spans the height


F.main_panels(NAME, [('a', build_a), ('b', build_b), ('c', build_c), ('d', build_d), ('e', build_e)])
