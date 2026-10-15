"""Figure s06f03, fig:s06:frustration: bipartite order against geometric frustration.

(a) A square plaquette with Neel arrows, the two sublattices as dark large discs and light small
discs. (b) A triangle with two antiparallel spins and, on the third site, the two choices as ghost
arrows; the bond that stays frustrated is drawn in the broken color. (c) The 120 degree state: three
spins in the plane, in one neutral color, at 120 degrees from each other.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's06f03_frustration'
XA, XB, XC = -4.2, 0.0, 4.2
TOP = 0.08
LIGHT = (0.62, 0.64, 0.70)


def light_site(name, loc, r=0.24):
    m = F.mat('site_light', LIGHT, rough=0.5, spec=0.3)
    return F.obj(name, F.mesh_of(name, [m], lambda bm: F.bm_cylinder(bm, (0, 0, 0), (0, 0, 0.08), r, seg=48)), loc=loc)


def bond(name, p, q, rgb=None, r=0.035):
    if rgb is None:
        return F.bond(name, (*p, 0.05), (*q, 0.05), r=r)
    return F.rod(name, (*p, 0.05), (*q, 0.05), r=0.06, rgb=rgb)


def build():
    F.studio()
    # (a) square plaquette, Neel order, two sublattices
    s = 0.95
    sq = [(XA - s, -s + 0.9), (XA + s, -s + 0.9), (XA + s, s + 0.9), (XA - s, s + 0.9)]
    for k, p in enumerate(sq):
        bond(f'a_b{k}', p, sq[(k + 1) % 4])
    for k, (x, y) in enumerate(sq):
        if k % 2 == 0:
            F.site(f'a_s{k}', (x, y, 0), r=0.32)
        else:
            light_site(f'a_s{k}', (x, y, 0))
        F.arrow(f'a_ar{k}', (x, y, TOP + 0.5), (0, 0, 1 if k % 2 == 0 else -1), length=0.85)
    F.anchor('apanel', (XA - 1.55, 2.2, 1.45))
    F.anchor('abelow', (XA, -0.45, 0))
    # (b) frustrated triangle
    r = 1.15
    tri = [(XB + r * math.cos(math.radians(a)), 0.75 + r * math.sin(math.radians(a))) for a in (210, 330, 90)]
    bond('b_b01', tri[0], tri[1])
    bond('b_b12', tri[1], tri[2], rgb=F.BROKEN)
    bond('b_b20', tri[2], tri[0])
    for k, (x, y) in enumerate(tri):
        F.site(f'b_s{k}', (x, y, 0), r=0.3)
    F.arrow('b_ar0', (*tri[0], TOP + 0.5), (0, 0, 1), length=0.85)
    F.arrow('b_ar1', (*tri[1], TOP + 0.5), (0, 0, -1), length=0.85)
    F.ghost_arrow('b_g_up', (tri[2][0] - 0.18, tri[2][1], TOP + 0.5), (0, 0, 1), length=0.85, alpha=0.3)
    F.ghost_arrow('b_g_dn', (tri[2][0] + 0.18, tri[2][1], TOP + 0.5), (0, 0, -1), length=0.85, alpha=0.3)
    F.anchor('q', (tri[2][0] + 0.35, tri[2][1], TOP + 1.0))
    F.anchor('bpanel', (XB - 1.55, 2.2, 1.45))
    F.anchor('bbelow', (XB, -0.45, 0))
    F.anchor('frus', ((tri[1][0] + tri[2][0]) / 2 + 0.25, (tri[1][1] + tri[2][1]) / 2, 0.1))
    # (c) the 120 degree state, spins in the plane
    tri = [(XC + r * math.cos(math.radians(a)), 0.75 + r * math.sin(math.radians(a))) for a in (210, 330, 90)]
    for k in range(3):
        bond(f'c_b{k}', tri[k], tri[(k + 1) % 3])
    for k, (x, y) in enumerate(tri):
        F.site(f'c_s{k}', (x, y, 0), r=0.3)
        a = math.radians(90 + 120 * k)
        F.sz_arrow(f'c_ar{k}', (x, y, TOP + 0.3), (math.cos(a), math.sin(a), 0), length=0.85, neutral=True)
    F.anchor('cpanel', (XC - 1.55, 2.2, 1.45))
    F.anchor('cbelow', (XC, -0.45, 0))
    F.camera((0.0, 0.8, 0.7), elev=30.0, ortho=12.2, aspect=3.0)


F.main(build, NAME)
