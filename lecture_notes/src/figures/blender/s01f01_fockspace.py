"""Figure s01f01, fig:s01:fockspace: one matrix against a Fock space, for three sites.

Left, the three-site chain with its 3 by 3 hopping matrix standing behind it, the four
first-neighbor entries raised and dark, the others flat. Right, the 2^3 = 8 Fock states, each a
plate with three sites and a ball on every occupied site, in columns of N = 0, 1, 2, 3 particles
holding 1, 3, 3 and 1 states.
"""
import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's01f01_fockspace'
XA, XB = -5.1, 2.1                     # centers of the two panels
STEP = 1.0
DARK, LIGHT = (0.30, 0.31, 0.35), (0.66, 0.68, 0.73)


def build():
    F.studio()
    # left: the chain and its L x L matrix
    xs = [XA + (i - 1) * STEP for i in range(3)]
    for i, x in enumerate(xs):
        F.site(f'a_s{i}', (x, 0, 0), r=0.26)
        if i < 2:
            F.bond(f'a_b{i}', (x + 0.26, 0, 0.05), (xs[i + 1] - 0.26, 0, 0.05))
    ts, zc, ym = 0.62, 1.55, 1.3
    for i in range(3):
        for j in range(3):
            nn = abs(i - j) == 1
            depth = 0.22 if nn else 0.05
            t = F.slab(f'a_m{i}{j}', (XA + (j - 1) * ts, ym - depth / 2, zc + (1 - i) * ts),
                       (0.54, depth, 0.54), rgb=DARK if nn else LIGHT)
            t.visible_shadow = False               # a matrix, not an object on the floor
    F.anchor('mat', (XA + 1.5 * ts + 0.05, ym, zc))
    F.anchor('titleA', (XA, ym, zc + 1.5 * ts + 0.15))
    F.anchor('chain', (XA, -0.45, 0))
    # right: the eight Fock states in columns of fixed particle number
    w, sp = 1.25, 0.36
    for N in range(4):
        xc = XB + (N - 1.5) * 2.0
        states = [c for c in itertools.product((1, 0), repeat=3) if sum(c) == N]
        ys = [0.95 * (k - (len(states) - 1) / 2) + 1.0 for k in range(len(states))]
        for k, (c, y) in enumerate(zip(states, ys)):
            F.slab(f'b_sl{N}{k}', (xc, y, 0.03), (w, 0.62, 0.06))
            for q in range(3):
                x = xc + (q - 1) * sp
                F.site(f'b_s{N}{k}{q}', (x, y, 0.06), r=0.12, h=0.03)
                if c[q]:
                    F.ball(f'b_e{N}{k}{q}', (x, y, 0.21), 0.11)
        F.anchor(f'N{N}', (xc, 2.45, 0.0))
        F.anchor(f'c{N}', (xc, -0.45, 0.0))
    F.anchor('titleB', (XB, 2.45, 0.75))
    F.camera((-1.35, 1.0, 0.85), elev=34.0, ortho=14.6, aspect=3.2)


F.main(build, NAME)
