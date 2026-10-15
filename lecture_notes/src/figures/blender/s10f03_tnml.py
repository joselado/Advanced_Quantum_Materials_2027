"""Figure s10f03, fig:s10:tnml: tensor networks used in reverse, as function approximators.

Seen from the front. (a) The four geometries as small tensor diagrams: an MPS of six tensors, a
tree of four leaves, a MERA of two layers on four sites, and a 3 by 3 PEPS seen slightly from
above. (b) A tree tensor network reading an image: a 4 by 4 pixel tile, each pixel a two-component
vector (a short leg), joined pairwise by tensors up the tree to one output tensor with a two-valued
leg, the label.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s07 as G                                                    # noqa: E402
import figlib_s10 as N                                                    # noqa: E402

NAME = 's10f03_tnml'
S = 0.3                                # small tensor size


def mps(x0, z0):
    for k in range(6):
        x = x0 + 0.42 * k
        G.T(f'mps{k}', x, z0, s=S)
        G.leg(f'mpsp{k}', (x, z0 - 0.15), (x, z0 - 0.45))
        if k < 5:
            G.leg(f'mpsb{k}', (x + 0.15, z0), (x + 0.27, z0), r=0.03)


def tree(tag, xs, z0, dz=0.5, s=S):
    level = [(x, z0) for x in xs]
    for x in xs:
        G.leg(f'{tag}_p{x:.2f}', (x, z0 - 0.3), (x, z0))
    k = 0
    while len(level) > 1:
        nxt = []
        for a, b in zip(level[0::2], level[1::2]):
            x, z = (a[0] + b[0]) / 2, a[1] + dz
            G.T(f'{tag}_t{k}', x, z, s=s)
            G.leg(f'{tag}_la{k}', (a[0], a[1]), (x - s / 3, z - s / 2))
            G.leg(f'{tag}_lb{k}', (b[0], b[1]), (x + s / 3, z - s / 2))
            nxt.append((x, z))
            k += 1
        level = nxt
    return level[0]


def build():
    F.studio()
    mps(-7.0, 1.3)
    F.anchor('mps', (-7.0 + 1.05, 0, 0.6))
    top = tree('tree', [-4.3 + 0.45 * k for k in range(4)], 0.9)
    G.leg('tree_top', (top[0], top[1] + S / 2), (top[0], top[1] + 0.45))
    F.anchor('tree', (-4.3 + 0.67, 0, 0.45))
    xm = [-1.75 + 0.42 * k for k in range(4)]           # a two-layer MERA on four sites
    for x in xm:
        G.leg(f'm_p{x:.2f}', (x, 0.6), (x, 0.95))
    G.T('m_d', (xm[1] + xm[2]) / 2, 1.05, s=S).scale = (1.6, 1, 1)
    for k, (a, b) in enumerate(((0, 1), (2, 3))):
        xc = (xm[a] + xm[b]) / 2
        G.prism(f'm_i{k}', xc, 1.6, w=0.55, h=0.3, d=0.3)
        G.leg(f'm_ia{k}', (xm[a], 0.95 if a == 0 else 1.2), (xm[a], 1.45))
        G.leg(f'm_ib{k}', (xm[b], 0.95 if b == 3 else 1.2), (xm[b], 1.45))
    G.T('m_top', (xm[0] + xm[3]) / 2, 2.15, s=S)
    for k, x in enumerate(((xm[0] + xm[1]) / 2, (xm[2] + xm[3]) / 2)):
        G.leg(f'm_u{k}', (x, 1.75), ((xm[0] + xm[3]) / 2 + (x - (xm[0] + xm[3]) / 2) * 0.3, 2.0))
    F.anchor('mera', ((xm[0] + xm[3]) / 2, 0, 0.45))
    for i in range(3):                                   # a 3 by 3 PEPS lying under the camera
        for j in range(3):
            x, y = 0.55 + 0.45 * i, -0.3 + 0.45 * j
            G.T(f'p_{i}{j}', x, 1.1, s=S * 0.8, y=y)
            G.leg(f'p_ph{i}{j}', (x, y, 0.98), (x, y, 0.7))
            if i < 2:
                G.leg(f'p_h{i}{j}', (x + 0.12, y, 1.1), (x + 0.33, y, 1.1), r=0.025)
            if j < 2:
                G.leg(f'p_v{i}{j}', (x, y + 0.12, 1.1), (x, y + 0.33, 1.1), r=0.025)
    F.anchor('peps', (1.0, 0, 0.45))
    F.anchor('pa', (-7.4, 0, 2.55))
    # (b) the classifier
    img = [[0, 1, 1, 0], [1, 0, 0, 1], [1, 1, 1, 1], [1, 0, 0, 1]]
    N.tile('b_img', 3.0, 1.6, img, cell=0.28)
    xs = [4.05 + 0.31 * k for k in range(8)]
    top = tree('b_tree', xs, 0.75, dz=0.55)
    G.leg('b_out', (top[0], top[1] + S / 2), (top[0], top[1] + 0.4), rgb=F.BROKEN, r=0.05)
    F.anchor('label', (top[0], 0, top[1] + 0.45))
    F.anchor('pixels', ((xs[0] + xs[-1]) / 2, 0, 0.35))
    F.anchor('img', (3.0, 0, 0.95))
    F.anchor('arr0', (3.65, 0, 1.6))
    F.anchor('arr1', (4.05, 0, 1.6))
    F.anchor('pb', (2.3, 0, 2.55))
    F.camera((-0.7, 0.0, 1.45), elev=8.0, ortho=15.2, aspect=3.0)


F.main(build, NAME)
