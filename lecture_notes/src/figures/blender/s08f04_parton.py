"""Figure s08f04, fig:s08:parton: the parton construction, its four local states and the spinon lattice.

(a) The four fermionic states of one site as four discs: empty, one up fermion, one down fermion,
and doubly occupied. The two singly occupied ones are the physical spin-1/2 doublet; the empty and
the doubly occupied ones are unphysical, drawn as ghosts with a cross. (b) A 4 by 3 lattice of
spinons at half filling, one per site, hopping on bonds whose radius is the self-consistent
|chi_ij|, taken here as a staggered pattern of two values for illustration.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's08f04_parton'


def fermion(name, loc, up, ghost=False):
    d = (0, 0, 1) if up else (0, 0, -1)
    if ghost:
        F.ghost_arrow(name, loc, d, length=0.55, alpha=0.25)
    else:
        F.arrow(name, loc, d, length=0.55)


def build():
    F.studio()
    states = [('empty', []), ('up', [True]), ('down', [False]), ('double', [True, False])]
    for k, (lab, content) in enumerate(states):
        x = -6.3 + 1.45 * k
        phys = len(content) == 1
        if phys:
            F.site(f'a_site{k}', (x, 0, 0), r=0.48, h=0.08)
        else:
            m = F.ghost('ghost_site', F.SITE, 0.25)
            F.obj(f'a_site{k}', F.mesh_of(f'a_site{k}', [m], lambda bm: F.bm_cylinder(bm, (0, 0, 0), (0, 0, 0.08), 0.48, seg=48)),
                  loc=(x, 0, 0))
        for j, up in enumerate(content):
            fermion(f'a_f{k}{j}', (x + (0.0 if len(content) == 1 else (-0.15 if j == 0 else 0.15)), 0, 0.45), up, ghost=not phys)
        if not phys:
            F.marker(f'a_x{k}', (x, -0.2, 0.9), kind='cross', r=0.28, rgb=F.BROKEN)
        F.anchor(f'st{k}', (x, -0.65, 0))
    F.anchor('pa', (-6.9, 0.9, 1.4))
    # (b) the spinon lattice
    nx, ny, sp = 4, 3, 1.15
    ox, oy = 0.6, -0.6
    for i in range(nx):
        for j in range(ny):
            x, y = ox + i * sp, oy + j * sp
            F.site(f'b_s{i}{j}', (x, y, 0), r=0.2, h=0.05)
            F.ball(f'b_e{i}{j}', (x, y, 0.22), 0.12)
            if i < nx - 1:
                strong = (i + j) % 2 == 0
                F.rod(f'b_h{i}{j}', (x + 0.2, y, 0.05), (x + sp - 0.2, y, 0.05), r=0.07 if strong else 0.03, rgb=F.ACCENT_AQM)
            if j < ny - 1:
                strong = (i + j) % 2 == 1
                F.rod(f'b_v{i}{j}', (x, y + 0.2, 0.05), (x, y + sp - 0.2, 0.05), r=0.07 if strong else 0.03, rgb=F.ACCENT_AQM)
    F.anchor('chi', (ox + 0.5 * sp, oy - 0.3, 0.05))
    F.axes_anchors('r', (ox - 1.0, oy, 0.0), {'x': (ox - 0.4, oy, 0.0), 'y': (ox - 1.0, oy + 0.6, 0.0)})
    F.anchor('pb', (ox - 0.6, oy + (ny - 1) * sp + 0.6, 0.9))
    F.camera((-1.0, 0.4, 0.45), elev=34.0, ortho=12.4, aspect=2.8)


F.main(build, NAME)
