"""Figure s06f01, fig:s06:stoner: a graphical reading of the Stoner criterion (6.3).

Seen from the front. (a) The line y = m and the right-hand side of the self-consistency condition
drawn as f(m) = ms tanh(s m / ms) with ms = 1, an odd function that saturates, for two slopes at the
origin s = U D(E_F) = 0.6 (the ghost, one crossing at m = 0) and s = 1.8 (two more crossings at
+-m0, the balls). (b) m0 as a function of s from the same model, zero up to s = 1 and growing
continuously after it. Schematic in the shape of f, exact for this f.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's06f01_stoner'
XA, XB = -3.6, 4.0
SA, SB = 1.7, 1.25                     # scene units per unit of m in (a), and per unit of s in (b)
Z0 = 2.1


def m0(s):
    if s <= 1:
        return 0.0
    m = 1.0
    for _ in range(200):
        m = math.tanh(s * m)
    return m


def build():
    F.studio()
    ms = [-1.6 + 3.2 * j / 160 for j in range(161)]
    P = lambda m, y: (XA + SA * m, 0, Z0 + SA * y)
    F.tube('ym', [P(-1.45, -1.45), P(1.45, 1.45)], 0.02, F.SITE)
    F.tube('f_sub', [P(m, math.tanh(0.6 * m)) for m in ms], 0.035, F.ACCENT_AQM, alpha=0.4)
    F.tube('f_sup', [P(m, math.tanh(1.8 * m)) for m in ms], 0.035, F.ACCENT_AQM)
    x0 = m0(1.8)
    for k, x in enumerate((-x0, 0.0, x0)):
        F.ball(f'cross{k}', P(x, x), 0.08, rgb=F.BROKEN if x else F.SITE)
    F.axis('a_ax', P(-1.7, 0), P(1.8, 0), r=0.016, head=0.13)
    F.axis('a_ay', P(0, -1.2), P(0, 1.25), r=0.016, head=0.13)
    F.anchor('am', P(1.8, 0))
    F.anchor('ay', P(0, 1.25))
    F.anchor('m0p', P(x0, x0))
    F.anchor('m0m', P(-x0, -x0))
    F.anchor('sup', P(1.55, math.tanh(1.8 * 1.55)))
    F.anchor('sub', P(1.55, math.tanh(0.6 * 1.55)))
    F.anchor('line', P(1.42, 1.42))
    F.anchor('apanel', P(-1.7, 1.3))
    ss = [3.0 * j / 300 for j in range(301)]
    Q = lambda s, m: (XB - 1.9 + SB * s, 0, Z0 - 1.2 + 1.9 * m)
    F.tube('m0', [Q(s, m0(s)) for s in ss], 0.035, F.ACCENT_AQM)
    F.axis('b_ax', Q(0, 0), Q(3.25, 0), r=0.016, head=0.13)
    F.axis('b_ay', Q(0, 0), Q(0, 1.25), r=0.016, head=0.13)
    F.rod('b_one', Q(1, -0.03), Q(1, 0.03), r=0.012)
    F.anchor('bs', Q(3.25, 0))
    F.anchor('bm', Q(0, 1.25))
    F.anchor('bone', Q(1, -0.04))
    F.anchor('bpanel', Q(-0.1, 1.3))
    F.camera((0.2, 0.0, Z0 + 0.05), elev=3.0, ortho=15.0, aspect=2.8)


F.main(build, NAME)
