"""Figure s03f03, fig:s03:ssh: the SSH chain with eight sites in its two dimerizations.

(a) In front, the intracell hopping t is the strong one, t = 4 against the intercell hopping 1:
    every site is paired inside its cell and the spectrum has a gap with nothing in it.
(b) Behind, t = 1/4: the strong bonds are between the cells, the two end sites are left over,
    and the spectrum has two levels at zero, split by 0.007 through the chain.
Both ladders are the eigenvalues of the open eight-site chain, in units of the strong hopping,
so that the two bulk spectra can be compared directly.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
from mathutils import Vector                                              # noqa: E402

NAME = 's03f03_ssh'
L, STEP = 8, 1.0                       # sites and spacing
X0 = -5.2                              # x of the first site
XL = 4.3                               # x of the level ladder
Y_BACK = 4.6                           # depth of the row of (b)
Z0, ES = 1.0, 0.62                     # height of E = 0 and height per unit of the strong hopping
R_SITE = 0.26
STRONG, WEAK = 0.11, 0.024            # bond radii


def spectrum(intra, inter):
    h = np.zeros((L, L))
    for i in range(L - 1):
        h[i, i + 1] = h[i + 1, i] = intra if i % 2 == 0 else inter
    return np.linalg.eigvalsh(h) / max(intra, inter)


def chain(y, tag, intra_strong):
    xs = [X0 + i * STEP for i in range(L)]
    cell = F.ghost('cell', F.ACCENT_AQM, 0.16)
    for c in range(0, L, 2):                       # the same cells (0,1), (2,3), ... in both rows
        xc = (xs[c] + xs[c + 1]) / 2
        F.obj(f'{tag}_cell{c}', F.mesh_of(f'{tag}_cell{c}', [cell], lambda bm: F.bm_rounded_box(
            bm, Vector((0, 0, 0)), (STEP + 0.72, 0.95, 0.03), 0.012)), loc=(xc, y, 0.015))
    for i, x in enumerate(xs):
        F.site(f'{tag}_s{i}', (x, y, 0), r=R_SITE)
        if i < L - 1:
            strong = (i % 2 == 0) == intra_strong
            F.bond(f'{tag}_b{i}', (x + R_SITE, y, 0.05), (xs[i + 1] - R_SITE, y, 0.05),
                   r=STRONG if strong else WEAK)
    return xs


def ladder(y, tag, energies):
    F.axis(f'{tag}_axis', (XL - 0.75, y, 0.02), (XL - 0.75, y, Z0 + 1.45 * ES), r=0.02, head=0.16)
    F.tube(f'{tag}_zero', [(XL - 0.95, y, Z0), (XL + 0.55, y, Z0)], 0.008, F.BOND).visible_shadow = False
    zero = [e for e in energies if abs(e) < 0.1]
    for k, e in enumerate(e for e in energies if abs(e) >= 0.1):
        F.level(f'{tag}_lev{k}', XL, y, Z0 + ES * e, length=0.8, r=0.026)
    for k, e in enumerate(sorted(zero)):           # the two end states side by side, they overlap in E
        F.level(f'{tag}_zero{k}', XL - 0.21 + 0.42 * k, y, Z0 + ES * e, length=0.36, r=0.05, rgb=F.BROKEN)
    F.anchor('E', (XL - 0.75, y, Z0 + 1.45 * ES + 0.05))
    F.anchor('zero', (XL - 0.85, y, Z0))
    F.anchor('top', (XL + 0.45, y, Z0 + ES))
    F.anchor('bot', (XL + 0.45, y, Z0 - ES))


def build():
    F.studio()
    # (a) in front: the intracell bond t is strong
    xs = chain(0.0, 'a', True)
    F.PREFIX[0] = 'a'
    ladder(0.0, 'a', spectrum(4.0, 1.0))
    F.anchor('panel', (X0 - 0.45, 0.0, 0.95))
    F.anchor('t', ((xs[2] + xs[3]) / 2, 0.3, 0.1))
    F.anchor('one', ((xs[3] + xs[4]) / 2, 0.3, 0.1))
    # (b) behind: the intercell bond is strong and the two end sites are left over
    xs = chain(Y_BACK, 'b', False)
    F.PREFIX[0] = 'b'
    ladder(Y_BACK, 'b', spectrum(0.25, 1.0))
    g = F.glow('glow_end', F.BROKEN, strength=1.2, alpha=0.32)
    for k, x in enumerate((xs[0], xs[-1])):
        F.obj(f'b_glow{k}', F.mesh_of(f'b_glow{k}', [g], lambda bm: F.bm_sphere(
            bm, Vector((0, 0, 0)), 1.0, seg=48, rings=24)), loc=(x, Y_BACK, 0.1), scale=(0.5, 0.5, 0.32))
    F.anchor('panel', (X0 - 0.45, Y_BACK, 0.95))
    F.anchor('endL', (xs[0], Y_BACK, 0.42))
    F.anchor('endR', (xs[-1], Y_BACK, 0.42))
    F.anchor('t', ((xs[2] + xs[3]) / 2, Y_BACK + 0.3, 0.1))
    F.anchor('one', ((xs[3] + xs[4]) / 2, Y_BACK + 0.3, 0.1))
    F.PREFIX[0] = ''
    F.camera((0.1, Y_BACK / 2, 0.95), elev=28.0, ortho=12.6, aspect=2.6)


F.main(build, NAME)
