"""Figure s09f01, fig:s09:nesting: nesting is what makes a response function diverge.

Two renders. Seen from the front: (a) the band -2t cos k, t = 1, at filling k_F = 0.35 pi, the
occupied part thick and the empty part a thin ghost, and the nesting vector q* = 2 k_F as an arrow
between the two Fermi points; (b) the static Lindhard function of the one-dimensional electron gas,
chi_0(q) / D(E_F) = (k_F / q) ln|(q + 2k_F) / (q - 2k_F)| / 2, equal to 1 as q -> 0 and diverging at
q = 2 k_F (cut at the top). Seen from above: (c) the square-lattice zone with the half-filled Fermi
surface, the diamond |kx| + |ky| = pi, as a slab, and Q = (pi, pi) mapping one edge onto the opposite.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's09f01_nesting'
KF = 0.35 * math.pi


def build_ab():
    F.studio()
    xa, sx, sz, z0 = -2.6, 0.62, 0.62, 1.6
    P = lambda k, e: (xa + sx * k, 0, z0 + sz * e)
    ks = [-math.pi + 2 * math.pi * j / 300 for j in range(301)]
    F.tube('a_empty', [P(k, -2 * math.cos(k)) for k in ks], 0.02, F.BOND, alpha=0.6)
    F.tube('a_occ', [P(k, -2 * math.cos(k)) for k in ks if abs(k) <= KF], 0.05, F.ACCENT_AQM)
    ef = -2 * math.cos(KF)
    F.tube('a_EF', [P(-math.pi, ef), P(math.pi, ef)], 0.008, F.BOND).visible_shadow = False
    F.vector_arrow('a_q', P(-KF, ef + 0.18), P(KF, ef + 0.18), r=0.025, rgb=F.BROKEN, head=0.16)
    for s in (1, -1):
        F.ball(f'a_kf{s}', P(s * KF, ef), 0.07, rgb=F.SITE)
    F.axis('a_ax', P(-math.pi - 0.1, -2.3), P(math.pi + 0.45, -2.3), r=0.016, head=0.13)
    F.axis('a_ay', P(-math.pi - 0.1, -2.3), P(-math.pi - 0.1, 2.4), r=0.016, head=0.13)
    F.anchor('ak', P(math.pi + 0.45, -2.3))
    F.anchor('aE', P(-math.pi - 0.1, 2.4))
    F.anchor('aq', P(0, ef + 0.25))
    F.anchor('akfm', P(-KF, -2.35))
    F.anchor('akfp', P(KF, -2.35))
    F.anchor('aEF', P(math.pi, ef))
    F.anchor('apanel', P(-math.pi - 0.2, 2.6))
    xb, cz = 2.6, 0.9
    Q = lambda q, c: (xb - 1.8 + 3.4 * q / (4.3 * KF), 0, z0 - 1.45 + cz * c)
    qs = [0.002 + 4.0 * KF * j / 600 for j in range(601)]
    chi = lambda q: (KF / q) * math.log(abs((q + 2 * KF) / (q - 2 * KF))) / 2 if abs(q - 2 * KF) > 1e-6 else 99
    pts = [Q(q, min(chi(q), 3.3)) for q in qs]
    left = [p for p, q in zip(pts, qs) if q < 2 * KF]
    right = [p for p, q in zip(pts, qs) if q > 2 * KF]
    F.tube('b_chi_l', left, 0.035, F.ACCENT_AQM)
    F.tube('b_chi_r', right, 0.035, F.ACCENT_AQM)
    F.tube('b_div', [Q(2 * KF, 0), Q(2 * KF, 3.4)], 0.008, F.BROKEN).visible_shadow = False
    F.axis('b_ax', Q(0, 0), Q(4.3 * KF, 0), r=0.016, head=0.13)
    F.axis('b_ay', Q(0, 0), Q(0, 3.6), r=0.016, head=0.13)
    F.anchor('bq', Q(4.3 * KF, 0))
    F.anchor('bchi', Q(0, 3.6))
    F.anchor('b2kf', Q(2 * KF, -0.05))
    F.anchor('bone', Q(0, 1.0))
    F.anchor('bpanel', Q(-0.3, 3.75))
    F.camera((0.0, 0.0, z0 + 0.0), elev=3.0, ortho=10.6, aspect=10.4 / 3.9)


def build_c():
    F.studio(shadows=False)
    h = 1.6
    F.slab('c_bz', (0, 0, 0.01), (2 * h, 2 * h, 0.02), rgb=(0.86, 0.87, 0.90))
    m = F.mat('fs_fill', F.ACCENT_AQM, rough=0.5)
    sea = F.ghost('fs_sea', F.ACCENT_AQM, 0.25)

    def diamond(bm):
        vs = [bm.verts.new((h * c, h * s, 0.0)) for c, s in ((1, 0), (0, 1), (-1, 0), (0, -1))]
        bm.faces.new(vs)
    F.obj('c_sea', F.mesh_of('c_sea', [sea], diamond), loc=(0, 0, 0.025))
    edge = [(h, 0, 0.04), (0, h, 0.04), (-h, 0, 0.04), (0, -h, 0.04), (h, 0, 0.04)]
    F.tube('c_fs', edge, 0.03, F.ACCENT_AQM)
    for k, t in enumerate((0.3, 0.55, 0.8)):
        p0 = (-h * t, -h * (1 - t), 0.08)
        F.vector_arrow(f'c_Q{k}', p0, (p0[0] + h, p0[1] + h, 0.08), r=0.022, rgb=F.BROKEN, head=0.12)
    F.axes_anchors('k', (0, 0, 0.03), {'x': (h + 0.35, 0, 0.03), 'y': (0, h + 0.35, 0.03)})
    F.anchor('Q', (-h * 0.97, -h * 0.97, 0.1))
    F.anchor('panel', (-h - 0.1, h + 0.25, 0))
    F.camera((0.05, 0.12, 0.0), elev=89.9, ortho=4.8, aspect=4.9 / 3.9)


F.main_panels(NAME, [('ab', build_ab), ('c', build_c)])
