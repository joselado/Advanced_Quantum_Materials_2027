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
    zc, rh = 0.75, 0.7                       # height of the plate, radius of the hexagon
    plate = F.slab('e_plate', (x0, 1.0, zc), (2.5, 2.3, 0.03), alpha=0.25)
    plate.visible_shadow = False
    F.rod('e_post', (x0, 1.0, 0), (x0, 1.0, zc - 0.02), r=0.025)
    hexp = [(x0 + rh * math.cos(math.pi / 6 + math.pi * m / 3), 1.0 + rh * math.sin(math.pi / 6 + math.pi * m / 3))
            for m in range(6)]
    outer = [(x0 + 2 * rh * math.cos(math.pi / 2 + math.pi * m / 3) * S3 / 2,
              1.0 + 2 * rh * math.sin(math.pi / 2 + math.pi * m / 3) * S3 / 2) for m in range(6)]
    for m, (x, y) in enumerate(hexp):
        F.site(f'e_s{m}', (x, y, zc + 0.02), r=0.1, h=0.03)
        x1, y1 = hexp[(m + 1) % 6]
        F.bond(f'e_b{m}', (x, y, zc + 0.04), (x1, y1, zc + 0.04), r=0.018)
        sgn = 1 if m % 2 == 0 else -1
        F.rod(f'e_p{m}', (x, y, zc), (x, y, zc + sgn * 0.42), r=0.012)
        F.ball(f'e_amp{m}', (x, y, zc + sgn * 0.5), 0.09)
    for m, (x, y) in enumerate(outer):         # the outside sites, each shared by two hexagon sites
        F.site(f'e_o{m}', (x, y, zc + 0.02), r=0.08, h=0.03)
        for q in (m, (m + 5) % 6):
            hx, hy = hexp[q]
            F.bond(f'e_ob{m}{q}', (x, y, zc + 0.04), (hx, hy, zc + 0.04), r=0.012)
    ox, oy = outer[0]                           # the two hops onto the top outside site, and the cancellation
    for q in (0, 5):
        hx, hy = hexp[q]
        sgn = 1 if q % 2 == 0 else -1
        F.flow(f'e_hop{q}', [(hx, hy, zc + sgn * 0.5), ((hx + ox) / 2, (hy + oy) / 2, zc + sgn * 0.45 + 0.15),
                             (ox, oy, zc + 0.12)], r=0.018, rgb=(0.16, 0.20, 0.30))
    F.marker('e_zero', (ox, oy, zc + 0.3), kind='cross', r=0.16, rgb=F.BROKEN)
    F.anchor('plus', (hexp[0][0] + 0.12, hexp[0][1], zc + 0.55))
    F.anchor('minus', (hexp[1][0] - 0.1, hexp[1][1], zc - 0.5))
    F.anchor('zero', (ox, oy + 0.15, zc + 0.45))


def build():
    F.studio()
    s = lieb_sites()
    lattice(XS[0], s, neighbors(s, 0.5), 'a', 1.15)
    s = kagome_sites()
    lattice(XS[2], s, neighbors(s, 0.5), 'c', 1.0)
    F.PREFIX[0] = 'b'
    bands(XS[1], lieb_h, [(0, 0), (math.pi, 0), (math.pi, math.pi), (0, 0)], ['G1', 'X', 'M', 'G2'], 0.0, 'b')
    F.PREFIX[0] = 'd'
    bands(XS[3], kagome_h, [(0, 0), (4 * math.pi / 3, 0), (math.pi, math.pi / S3), (0, 0)],
          ['G1', 'K', 'M', 'G2'], 2.0, 'd')
    F.PREFIX[0] = 'e'
    hexagon(XS[4])
    F.PREFIX[0] = ''
    for k, x in enumerate(XS):
        F.anchor('p' + 'abcde'[k], (x - (1.45 if k in (0, 2, 4) else 2.0), 0, Z0 + 3.0 * SZ))
    F.camera((-0.25, 0.9, 1.1), elev=26.0, ortho=16.4, aspect=3.0)


F.main(build, NAME)
