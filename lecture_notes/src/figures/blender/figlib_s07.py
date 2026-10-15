"""figlib_s07.py: tensor-network shapes used by the Session 7 and 10 figures, on top of figlib.py.

Diagrams are drawn in the xz plane (y = 0) and seen from the front. A tensor is a teal rounded cube,
an operator (MPO) tensor a darker one, an isometry a triangular prism, and a leg a grey rod.
"""
import figlib as F
from mathutils import Vector

TEAL = F.ACCENT[4]
OPER = (0.03, 0.17, 0.30)
HOLE = F.BROKEN


def T(name, x, z, s=0.5, rgb=None, y=0.0):
    return F.tensor(name, (x, y, z), size=(s, s, s), rgb=TEAL if rgb is None else rgb, radius=0.1 * s / 0.5)


def leg(name, p0, p1, r=0.04, rgb=F.BOND):
    return F.leg(name, (p0[0], p0[1] if len(p0) == 3 else 0.0, p0[-1]), (p1[0], p1[1] if len(p1) == 3 else 0.0, p1[-1]),
                 r=r, rgb=rgb)


def prism(name, x, z, w=0.7, h=0.55, d=0.5, rgb=None, y=0.0):
    """An isometry as a triangular prism pointing up, two legs below and one above."""
    m = F.mat('prism_%d_%d_%d' % tuple(int(255 * c) for c in (rgb or TEAL)), rgb or TEAL, rough=0.35, emit=0.08)

    def f(bm):
        pts = [(-w / 2, -h / 2), (w / 2, -h / 2), (0, h / 2)]
        front = [bm.verts.new((px, -d / 2, pz)) for px, pz in pts]
        back = [bm.verts.new((px, d / 2, pz)) for px, pz in pts]
        bm.faces.new(front[::-1]), bm.faces.new(back)
        for k in range(3):
            bm.faces.new((front[k], front[(k + 1) % 3], back[(k + 1) % 3], back[k]))
    return F.obj(name, F.mesh_of(name, [m], f), loc=(x, y, z))
