"""Figure s08f05, fig:s08:gauge: link phases are gauge, plaquette fluxes are physical; a vison.

Seen from above. (a) One plaquette twice, with a dial on every link at the phase theta_ij of
chi_ij (zero along +x), before and after the phase rotation (8.16) on the top-right site by
theta = pi/3, which shifts its two links by -+pi/3 and leaves the flux, the sum around the plaquette,
unchanged. (b) A 6 by 4 lattice of plaquettes with Z2 links, each a short rod, + light and - in the
broken color: a string of - links from the left edge ends at one plaquette, which has Phi = -1
and glows; every other plaquette has Phi = +1. Moving the string is a gauge choice; the plaquette
at its end is not.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's08f05_gauge_vison'


def dial(name, loc, phase, rgb=None):
    disc = F.mat('dial', (0.74, 0.76, 0.80), rough=0.6, spec=0.2)
    F.obj(name, F.mesh_of(name, [disc], lambda bm: F.bm_cylinder(bm, (0, 0, 0), (0, 0, 0.03), 0.24, seg=40)), loc=loc)
    x, y, z = loc
    F.vector_arrow(name + '_n', (x, y, z + 0.05), (x + 0.21 * math.cos(phase), y + 0.21 * math.sin(phase), z + 0.05),
                   r=0.02, head=0.08, rgb=rgb)


def plaquette(x0, y0, th, rot, tag):
    s = 1.3
    P = [(x0, y0), (x0 + s, y0), (x0 + s, y0 + s), (x0, y0 + s)]
    links = [(0, 1), (1, 2), (3, 2), (0, 3)]           # each traversed along +x or +y
    for k, (i, j) in enumerate(links):
        (x1, y1), (x2, y2) = P[i], P[j]
        F.bond(f'{tag}_b{k}', (x1, y1, 0.03), (x2, y2, 0.03), r=0.02)
        ph = th[k] + (rot if j == 2 else 0) - (rot if i == 2 else 0)
        dial(f'{tag}_d{k}', ((x1 + x2) / 2, (y1 + y2) / 2, 0.04), ph, rgb=F.BROKEN if rot and 2 in (i, j) else None)
    for k, (x, y) in enumerate(P):
        F.site(f'{tag}_s{k}', (x, y, 0), r=0.13, h=0.04)
    F.anchor('rot', (P[2][0] + 0.2, P[2][1] + 0.2, 0))
    F.anchor('flux', (x0 + s / 2, y0 + s / 2, 0))
    F.anchor('below', (x0 + s / 2, y0 - 0.35, 0))


def build():
    F.studio(shadows=False)
    th = [0.4, 1.2, -0.5, 0.9]
    F.PREFIX[0] = 'a0'
    plaquette(-7.0, -0.2, th, 0.0, 'a0')
    F.PREFIX[0] = 'a1'
    plaquette(-4.6, -0.2, th, math.pi / 3, 'a1')
    F.PREFIX[0] = ''
    F.anchor('pa', (-7.4, 1.95, 0))
    F.anchor('arrow0', (-5.55, 0.45, 0))
    F.anchor('arrow1', (-4.75, 0.45, 0))
    # (b) the Z2 lattice and the vison
    nx, ny, s = 6, 4, 0.75
    ox, oy = -1.6, -0.9
    vx, vy = 3, 1                                       # the flipped plaquette
    minus = {('v', i, vy) for i in range(0, vx + 1)}    # the vertical links crossed by a string from the left edge
    flux = {(i, j): (-1) ** sum(((('h', i, j) in minus), (('h', i, j + 1) in minus), (('v', i, j) in minus),
                                 (('v', i + 1, j) in minus))) for i in range(nx) for j in range(ny)}
    print('plaquettes with flux -1:', [p for p, f in flux.items() if f < 0])
    for i in range(nx + 1):
        for j in range(ny + 1):
            x, y = ox + i * s, oy + j * s
            F.site(f'b_s{i}{j}', (x, y, 0), r=0.07, h=0.03)
            for kind, di, dj in (('h', 1, 0), ('v', 0, 1)):
                if i + di > nx or j + dj > ny:
                    continue
                neg = (kind, i, j) in minus
                F.rod(f'b_{kind}{i}{j}', (x + 0.08 * di, y + 0.08 * dj, 0.03), (x + (s - 0.08) * di, y + (s - 0.08) * dj, 0.03),
                      r=0.04 if neg else 0.018, rgb=F.BROKEN if neg else F.BOND)
    for i in range(nx):
        for j in range(ny):
            vis = (i, j) == (vx, vy)
            F.slab(f'b_p{i}{j}', (ox + (i + 0.5) * s, oy + (j + 0.5) * s, 0.005), (s - 0.16, s - 0.16, 0.01),
                   rgb=F.BROKEN if vis else F.ACCENT_AQM, alpha=0.45 if vis else 0.1)
    g = F.glow('vison_glow', F.BROKEN, strength=1.2, alpha=0.35)
    F.obj('vison', F.mesh_of('vison', [g], lambda bm: F.bm_sphere(bm, F.Vector((0, 0, 0)), 1.0, seg=40, rings=20)),
          loc=(ox + (vx + 0.5) * s, oy + (vy + 0.5) * s, 0.05), scale=(0.42, 0.42, 0.15))
    F.anchor('vison', (ox + (vx + 0.5) * s, oy + (vy + 1) * s + 0.05, 0))
    F.anchor('string', (ox + 0.2, oy + (vy + 0.5) * s, 0))
    F.anchor('pb', (ox - 0.35, oy + ny * s + 0.5, 0))
    F.camera((-1.9, 0.6, 0.0), elev=89.9, ortho=11.6, aspect=2.6)


F.main(build, NAME)
