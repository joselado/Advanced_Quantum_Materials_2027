"""Figure s03f01, fig:s03:chiraledge: chiral edge states in real space, seen from above.

(a) A flat sample with B out of the page (+z). Electrons orbit counter-clockwise in the bulk, the
    closed rings with an arrowhead; at the edges the orbits cannot close and skip, to +x along the
    top edge and to -x along the bottom one, as the E x B drift of the confining potential gives.
(b) One edge with an impurity as a bump, and the edge mode going around it and on.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's03f01_chiraledge'
XA, XB = -2.6, 5.0                     # centers of the panels
LX, LY, H = 8.0, 3.4, 0.12             # sample size and thickness
RC = 0.32                              # cyclotron radius
FLOW = F.ACCENT_AQM


def orbit(name, cx, cy, z):
    pts = [(cx + RC * math.cos(a), cy + RC * math.sin(a), z) for a in
           [-math.pi / 2 + 2 * math.pi * 0.85 * k / 40 for k in range(41)]]
    return F.flow(name, pts, r=0.022, rgb=FLOW)


def skipping(name, x0, x1, yw, sgn, z):
    """Arcs of radius RC hanging from the wall at y = yw into the sample (sgn = -1 for the top wall),
    chained in the direction from x0 to x1."""
    n = int(abs(x1 - x0) / (2 * RC))
    d = 1 if x1 > x0 else -1
    pts = []
    for j in range(n):
        cx = x0 + d * (2 * j + 1) * RC
        for k in range(13):
            a = math.pi * k / 12
            pts.append((cx - d * RC * math.cos(a), yw + sgn * RC * math.sin(a) * 0.95, z))
    return F.flow(name, pts, r=0.024, rgb=FLOW)


def build():
    F.studio()
    z = H + 0.03
    F.slab('a_sample', (XA, 0, H / 2), (LX, LY, H), rgb=(0.84, 0.86, 0.90), radius=0.04)
    for k, (cx, cy) in enumerate([(XA - 2.4, 0.45), (XA - 0.8, -0.35), (XA + 0.8, 0.45), (XA + 2.4, -0.35)]):
        orbit(f'a_orb{k}', cx, cy, z)
    skipping('a_top', XA - LX / 2 + 0.35, XA + LX / 2 - 0.2, LY / 2, -1, z)
    skipping('a_bot', XA + LX / 2 - 0.35, XA - LX / 2 + 0.2, -LY / 2, 1, z)
    F.anchor('B', (XA - LX / 2 + 0.3, -LY / 2 + 0.75, z))
    F.anchor('top', (XA, LY / 2, z))
    F.anchor('bot', (XA, -LY / 2 - 0.15, 0))
    F.anchor('bulk', (XA, 0.05, z))
    F.anchor('a', (XA - LX / 2, LY / 2 + 0.6, 0))
    F.axes_anchors('r', (XA + LX / 2 + 0.3, -LY / 2, 0.0), {'x': (XA + LX / 2 + 1.1, -LY / 2, 0.0), 'y': (XA + LX / 2 + 0.3, -LY / 2 + 0.8, 0.0)})
    # (b) one edge, an impurity, and the mode going around it
    w = 4.2
    F.slab('b_sample', (XB, 0.6, H / 2), (w, 2.2, H), rgb=(0.84, 0.86, 0.90), radius=0.04)
    ye = -0.5 + 0.28
    bump = F.mat('impurity', (0.30, 0.31, 0.35), rough=0.5)
    F.obj('b_imp', F.mesh_of('b_imp', [bump], lambda bm: F.bm_sphere(bm, F.Vector((0, 0, 0)), 0.32)),
          loc=(XB, ye, H), scale=(1, 1, 0.8))
    pts = []
    for k in range(81):
        x = XB - w / 2 + 0.2 + (w - 0.4) * k / 80
        dx = (x - XB) / 0.55
        pts.append((x, ye + 0.62 * math.exp(-dx * dx), z))
    F.flow('b_mode', pts, r=0.03, rgb=FLOW)
    F.anchor('imp', (XB, ye - 0.35, H))
    F.anchor('edge', (XB + w / 2, -0.5, 0))
    F.anchor('b', (XB - w / 2, LY / 2 + 0.6, 0))
    F.camera((0.75, 0.25, 0.0), elev=89.9, ortho=16.0, aspect=3.2)


F.main(build, NAME)
