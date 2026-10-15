"""Figure s10f02, fig:s10:nnqs: neural network quantum states.

Seen from the front. (a) A configuration s of eight spins as a row of up and down tiles entering
a network, and one coefficient C_theta(s) coming out as a single ball. (b) Six sampled
configurations as a stack of rows, each with its local energy as a bar, and the average of the
bars as a line, the estimate of (10.3). (c) The variational families as nested translucent
ellipses lying in a plane: MPS inside PEPS inside NNQS.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s10 as N                                                    # noqa: E402

NAME = 's10f02_nnqs'
UP, DN = F.srgb(224, 62, 40), F.srgb(40, 92, 200)


def spins(tag, x0, z0, s, cell=0.2):
    for j, v in enumerate(s):
        F.slab(f'{tag}_{j}', (x0 + (j - (len(s) - 1) / 2) * cell, 0, z0), (cell * 0.9, 0.05, cell * 0.9), rgb=UP if v > 0 else DN,
               radius=0.01)


def build():
    F.studio()
    rnd = random.Random(7)
    s0 = [1, -1, -1, 1, -1, 1, 1, -1]
    spins('a_s', -6.0, 1.4, s0)
    N.net('a_net', -3.6, 1.4, [8, 6, 4, 1], w=2.2, h=1.8, r=0.07)
    F.ball('a_C', (-2.1, 0, 1.4), 0.14, rgb=F.BROKEN)
    F.anchor('as', (-6.0, 0, 1.1))
    F.anchor('aC', (-2.1, 0, 1.65))
    F.anchor('ap', (-6.9, 0, 2.6))
    # (b) sampled configurations and local energies
    eloc = []
    for r in range(6):
        s = [rnd.choice((1, -1)) for _ in range(8)]
        z = 2.3 - 0.36 * r
        spins(f'b_s{r}', -0.5, z, s, cell=0.16)
        e = 0.3 + 0.5 * rnd.random()
        eloc.append(e)
        F.slab(f'b_e{r}', (0.5 + e / 2, 0, z), (e, 0.05, 0.14), rgb=F.ACCENT_AQM, radius=0.01)
    m = sum(eloc) / len(eloc)
    F.tube('b_mean', [(0.5 + m, 0, 2.5), (0.5 + m, 0, 0.3)], 0.015, F.BROKEN)
    F.anchor('bs', (-0.5, 0, 0.25))
    F.anchor('be', (0.5 + m, 0, 2.55))
    F.anchor('bp', (-1.3, 0, 2.6))
    # (c) the nested families
    for k, (tag, a, b, alpha) in enumerate((('nnqs', 1.65, 1.0, 0.12), ('peps', 1.15, 0.68, 0.18), ('mps', 0.62, 0.38, 0.28))):
        F.obj(f'c_{tag}', F.mesh_of(f'c_{tag}', [F.ghost(f'fam{k}', F.ACCENT_AQM, alpha)], lambda bm, k=k: F.bm_cylinder(
            bm, (0, 0, 0), (0, -0.04 - 0.03 * k, 0), 1.0, seg=64)), loc=(4.6 + (1.65 - a) * 0.55, -0.05 * k, 1.35),
            scale=(a, 1, b))
        F.anchor(tag, (4.6 + (1.65 - a) * 0.55 + 0.55 * a, 0, 1.35 + b - 0.08))
    F.anchor('cp', (2.8, 0, 2.6))
    F.camera((-0.9, 0.0, 1.35), elev=14.0, ortho=15.0, aspect=2.8)


F.main(build, NAME)
