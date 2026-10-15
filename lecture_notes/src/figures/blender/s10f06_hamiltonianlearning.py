"""Figure s10f06, fig:s10:hamlearning: Hamiltonian learning.

Seen from the front. Top: a Hamiltonian, a small matrix tile, and a spectrum, a tile of bars, with
the forward arrow between them and the inverse arrow as a ghost crossed out (both drawn in the
overlay, the cross in the scene). (a) Five known Hamiltonians, matrix tiles with their parameters,
each simulated into a spectrum, feeding a network. (b) The trained network applied to one measured
spectrum, giving its parameter.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s10 as N                                                    # noqa: E402

NAME = 's10f06_hamiltonianlearning'


def matrix(tag, x0, z0, lam, cell=0.14):
    vals = [[(1.0 if i == j else (lam if abs(i - j) == 1 else 0.0)) for j in range(5)] for i in range(5)]
    N.tile(tag, x0, z0, vals, cell=cell, rgb_on=F.ACCENT_AQM)


def spectrum(tag, x0, z0, lam, scale=1.0):
    hs = [scale * (0.12 + 0.5 * abs(math.sin(0.9 * k * (0.6 + lam)))) for k in range(1, 7)]
    N.bars(tag, x0, z0, hs, w=0.09, gap=0.04)


def build():
    F.studio()
    rnd = random.Random(5)
    # top row
    matrix('t_H', -1.6, 2.6, 0.6, cell=0.16)
    spectrum('t_O', 1.6, 2.2, 0.6)
    F.marker('t_x', (0.0, 0, 2.35), kind='cross', r=0.18, rgb=F.BROKEN)
    F.anchor('tH', (-1.6, 0, 3.15))
    F.anchor('tO', (1.6, 0, 3.15))
    F.anchor('f0', (-0.9, 0, 2.85))
    F.anchor('f1', (0.9, 0, 2.85))
    F.anchor('i0', (0.9, 0, 2.35))
    F.anchor('i1', (-0.9, 0, 2.35))
    # (a) training on synthetic data
    for k in range(5):
        lam = rnd.uniform(0.2, 1.0)
        z = 1.75 - 0.4 * k
        matrix(f'a_H{k}', -6.4, z, lam, cell=0.065)
        spectrum(f'a_O{k}', -5.4, z - 0.15, lam, scale=0.45)
        F.anchor(f'alam{k}', (-4.85, 0, z))
    N.net('a_net', -3.3, 0.85, [6, 5, 4, 1], w=1.6, h=1.4, r=0.06)
    F.anchor('apanel', (-6.9, 0, 1.95))
    F.anchor('a0', (-4.4, 0, 0.85))
    F.anchor('a1', (-4.15, 0, 0.85))
    F.anchor('anet', (-3.3, 0, 0.05))
    # (b) deployment on one measured spectrum
    spectrum('b_O', 2.2, 0.55, 0.45)
    N.net('b_net', 4.4, 0.85, [6, 5, 4, 1], w=1.6, h=1.4, r=0.06)
    F.ball('b_out', (5.8, 0, 0.85), 0.12, rgb=F.BROKEN)
    F.anchor('bO', (2.2, 0, 0.35))
    F.anchor('b0', (2.75, 0, 0.85))
    F.anchor('b1', (3.45, 0, 0.85))
    F.anchor('bout', (5.8, 0, 1.1))
    F.anchor('bpanel', (1.5, 0, 1.45))
    F.camera((-0.3, 0.0, 1.6), elev=6.0, ortho=14.4, aspect=3.0)


F.main(build, NAME)
