"""Figure s08f02, fig:s08:frustration: the degenerate Ising triangle and the kagome lattice.

Collinear (Ising) spins throughout. (a) The three inequivalent placements of the unsatisfied bond
on a triangle, each with the frustrated bond drawn in the broken color. (b) A kagome patch of
corner-sharing triangles with one Ising ground state on it, up on sublattices A and C and down on
B, so that every triangle has two spins one way and one the other and exactly one frustrated
bond, drawn in the broken color.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's08f02_frustration'
R = 0.62                               # circumradius of a small triangle


def triangle(x0, y0, spins, tag):
    pts = [(x0 + R * math.cos(math.radians(a)), y0 + R * math.sin(math.radians(a))) for a in (210, 330, 90)]
    for k in range(3):
        p, q = pts[k], pts[(k + 1) % 3]
        frus = spins[k] == spins[(k + 1) % 3]
        F.rod(f'{tag}_b{k}', (*p, 0.05), (*q, 0.05), r=0.05 if frus else 0.03, rgb=F.BROKEN if frus else F.BOND)
    for k, (x, y) in enumerate(pts):
        F.site(f'{tag}_s{k}', (x, y, 0), r=0.2, h=0.06)
        F.arrow(f'{tag}_a{k}', (x, y, 0.4), (0, 0, spins[k]), length=0.62)


def build():
    F.studio()
    for k, sp in enumerate(((1, -1, 1), (1, 1, -1), (-1, 1, 1))):
        triangle(-6.0 + 1.6 * k, 1.0, sp, f't{k}')
    F.anchor('pa', (-6.9, 2.0, 0.9))
    F.anchor('ta', (-6.0 + 1.6, 1.0 - R - 0.2, 0))
    # (b) kagome: three sublattices, up on A and C, down on B
    a1, a2 = (1.0, 0.0), (0.5, math.sqrt(3) / 2)
    sc, x0, y0 = 1.2, 2.5, 1.0
    basis = {'A': (0.0, 0.0), 'B': (0.5, 0.0), 'C': (0.25, math.sqrt(3) / 4)}
    spin = {'A': 1, 'B': -1, 'C': 1}
    sites = []
    for i in range(-3, 4):
        for j in range(-3, 4):
            for lab, (bx, by) in basis.items():
                x = i * a1[0] + j * a2[0] + bx - 0.5
                y = i * a1[1] + j * a2[1] + by - 0.3
                if x * x / 3.0 + y * y / 2.1 < 1.0:
                    sites.append((x0 + sc * x, y0 + sc * y, lab))
    for k, (x, y, lab) in enumerate(sites):
        F.site(f'k_s{k}', (x, y, 0), r=0.13, h=0.05)
        F.arrow(f'k_a{k}', (x, y, 0.33), (0, 0, spin[lab]), length=0.5)
    nb = 0
    for i in range(len(sites)):
        for j in range(i + 1, len(sites)):
            (x1, y1, l1), (x2, y2, l2) = sites[i], sites[j]
            if abs(math.dist((x1, y1), (x2, y2)) - 0.5 * sc) < 1e-6:
                frus = spin[l1] == spin[l2]
                F.rod(f'k_b{nb}', (x1, y1, 0.04), (x2, y2, 0.04), r=0.045 if frus else 0.022, rgb=F.BROKEN if frus else F.BOND)
                nb += 1
    F.anchor('pb', (x0 - 2.6, 2.0 + 0.3, 0.9))
    F.axes_anchors('r', (x0 - 2.5, -0.4, 0.0), {'x': (x0 - 1.85, -0.4, 0.0), 'y': (x0 - 2.5, 0.25, 0.0)})
    F.camera((-1.25, 1.0, 0.45), elev=48.0, ortho=12.6, aspect=12.5 / 4.3)


F.main(build, NAME)
