"""Figure s10f01, fig:s10:template: the network as a parametric function, and its training loop.

Seen from the front. Left, a network with layers 6, 5, 5, 2, the input a 6 by 6 pixel tile (a
schematic picture) and the output two tiles, a one-hot label. Right, the training loop as four
stations on a ring, evaluate (the network again, small), loss (a bar against a target), gradient
(an arrow) and step (a ball moved down a slope), whose loop arrows are drawn in the overlay.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s10 as N                                                    # noqa: E402

NAME = 's10f01_networktemplate'
PIC = [[0, 0, 1, 1, 0, 0], [0, 1, 1, 1, 1, 0], [1, 1, 0, 0, 1, 1], [1, 1, 1, 1, 1, 1], [0, 1, 0, 0, 1, 0], [0, 1, 0, 0, 1, 0]]


def build():
    F.studio()
    N.tile('in', -6.2, 1.35, PIC, cell=0.2)
    N.net('net', -3.6, 1.35, [6, 5, 5, 2], w=2.6, h=1.8)
    N.tile('out', -1.7, 1.35, [[1], [0]], cell=0.3, rgb_on=F.BROKEN, rgb_off=(0.62, 0.64, 0.70))
    F.anchor('in', (-6.2, 0, 0.55))
    F.anchor('net', (-3.6, 0, 0.3))
    F.anchor('out', (-1.7, 0, 0.85))
    F.anchor('theta', (-3.6, 0, 2.4))
    F.anchor('a0', (-5.45, 0, 1.35))
    F.anchor('a1', (-4.95, 0, 1.35))
    F.anchor('a2', (-2.25, 0, 1.35))
    F.anchor('a3', (-1.95, 0, 1.35))
    # the training loop: four stations on a ring
    cx, cz, R = 3.4, 1.35, 1.25
    st = [(cx + R * math.cos(a), cz + R * math.sin(a)) for a in (math.pi * 0.75, math.pi * 0.25, -math.pi * 0.25, -math.pi * 0.75)]
    N.net('ev', st[0][0], st[0][1], [3, 3, 2], w=0.7, h=0.5, r=0.05)
    N.bars('loss', st[1][0], st[1][1] - 0.25, [0.55, 0.25], w=0.16, rgb=F.BROKEN)
    F.vector_arrow('grad', (st[2][0] - 0.3, 0, st[2][1] + 0.2), (st[2][0] + 0.25, 0, st[2][1] - 0.2), r=0.03, rgb=F.SITE)
    F.tube('slope', [(st[3][0] - 0.45 + 0.9 * j / 30, 0, st[3][1] - 0.15 + 0.5 * ((j / 30) - 0.5) ** 2 * 2) for j in range(31)],
           0.02, F.BOND)
    F.ball('stepball', (st[3][0] - 0.05, 0, st[3][1] - 0.08), 0.08, rgb=F.ACCENT_AQM)
    for k, (x, z) in enumerate(st):
        F.anchor(f'st{k}', (x, 0, z))
    F.anchor('loopc', (cx, 0, cz))
    F.camera((-1.35, 0.0, 1.35), elev=6.0, ortho=15.0, aspect=2.8)


F.main(build, NAME)
