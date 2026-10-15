"""Figure s07f05, fig:s07:dmrg: DMRG erases one tensor and leaves a small eigenvalue problem.

Seen from the front. (a) The closed network of the Rayleigh quotient, three layers of six tensors:
the bra MPS on top, the Hamiltonian as an MPO in the middle, the ket MPS at the bottom, all legs
contracted. (b) The same network with the bra tensor of site k = 3 removed: a ghost outline where it
was, and its three legs, the two virtual bonds and the physical index, left open in the broken
color. The sweep of (c) is drawn in the overlay.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s07 as G                                                    # noqa: E402

NAME = 's07f05_dmrg'
N, DX = 6, 0.85
K = 3


def network(x0, hole, tag):
    zs = {'bra': 2.0, 'mpo': 1.1, 'ket': 0.2}
    for k in range(N):
        x = x0 + DX * k
        for layer, z in zs.items():
            if hole and layer == 'bra' and k == K:
                m = F.ghost('hole_ghost', F.BROKEN, 0.18)
                F.obj(f'{tag}_hole', F.mesh_of(f'{tag}_hole', [m], lambda bm: F.bm_rounded_box(
                    bm, F.Vector((0, 0, 0)), (0.42, 0.42, 0.42), 0.08)), loc=(x, 0, z))
                continue
            G.T(f'{tag}_{layer}{k}', x, z, s=0.42, rgb=G.OPER if layer == 'mpo' else None)
        for z0, z1 in ((zs['ket'] + 0.21, zs['mpo'] - 0.21), (zs['mpo'] + 0.21, zs['bra'] - 0.21)):
            open_leg = hole and k == K and z1 == zs['bra'] - 0.21
            G.leg(f'{tag}_v{k}_{z0:.1f}', (x, z0), (x, z1 - (0.12 if open_leg else 0)), rgb=F.BROKEN if open_leg else F.BOND,
                  r=0.045 if open_leg else 0.04)
        if k < N - 1:
            for layer, z in zs.items():
                open_l = hole and layer == 'bra' and k in (K - 1, K)
                a = x + 0.21 + (0.0 if not (open_l and k == K) else 0.12)
                b = x + DX - 0.21 - (0.12 if (open_l and k == K - 1) else 0.0)
                G.leg(f'{tag}_h{layer}{k}', (a, z), (b, z), r=0.045 if open_l else 0.035,
                      rgb=F.BROKEN if open_l else F.BOND)
    F.anchor('bra', (x0 + DX * (N - 1) + 0.35, 0, zs['bra']))
    F.anchor('mpo', (x0 + DX * (N - 1) + 0.35, 0, zs['mpo']))
    F.anchor('ket', (x0 + DX * (N - 1) + 0.35, 0, zs['ket']))
    F.anchor('hole', (x0 + DX * K, 0, zs['bra'] + 0.35))
    F.anchor('below', (x0 + DX * (N - 1) / 2, 0, -0.2))
    F.anchor('panel', (x0 - 0.4, 0, 2.55))
    F.anchor('sweep0', (x0 + DX * (K - 1), 0, -0.05))
    F.anchor('sweep1', (x0 + DX * (K + 1), 0, -0.05))


def build():
    F.studio()
    F.PREFIX[0] = 'a'
    network(-6.6, False, 'a')
    F.PREFIX[0] = 'b'
    network(1.1, True, 'b')
    F.PREFIX[0] = ''
    F.anchor('d0', (-1.55, 0, 1.1))
    F.anchor('d1', (0.65, 0, 1.1))
    F.camera((-0.2, 0.0, 1.15), elev=8.0, ortho=15.2, aspect=3.4)


F.main(build, NAME)
