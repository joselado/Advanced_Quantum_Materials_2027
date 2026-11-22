"""Session 5, the numbers and the algebra that page 13 (Section 5.13) states and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here or
in the figure script that draws it. The map and the curves of dwave_nodes, with Delta_0 = 2 delta = 0.2 and the value
below 0.01 Delta_0 at the nodes, are asserted in figures/session05/dwave_nodes.py, and the BdG bands of the picture quiz,
0.4 for the s-wave on the Fermi surface, 0.91 between Gamma and K and zero at (1/3, 0) for the f-wave, in
figures/session05/_g3_tribands.py. This script holds the rest, in the order of the page: the fold from the pairing on
the bonds to (5.13), checked with the Fourier sum and with the BdG levels of a torus, the d-wave entry of pyqula, the
lab box (Phi_0/2, the condition L Ic >> Phi_0 of our reading from the energy of a ring with one junction, and its
sentences in the stored source), the 130 K of the old text, the cos 3 theta of the first quiz, the problem on the
extended s-wave with what STM sees in the density of states, and the try-it box. pyqula is called only through its
Bloch Hamiltonian, which writes no file. It finds the repository from its own path and writes no file.

Run it from anywhere:  python3 webnotes/checks/session05/g3_13_dwave.py"""
import os, sys
sys.dont_write_bytecode = True
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
assert os.path.exists(os.path.join(REPO, 'webnotes', 'pages', 'session05'))
sys.path.insert(0, os.path.join(REPO, 'webnotes'))

import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


rng = np.random.default_rng(3)

# ---------------------------------------------------------------------------------------------------------------
# the fold. With c_r^dag = N^-1/2 sum_k e^{-ik.r} c_k^dag the bond delta gives the phase e^{ik.delta}, for either sign
for s in (1, -1):
    k = rng.uniform(-np.pi, np.pi, size=(20, 2))
    chain = sum(np.exp(1j * s * k[:, 0] * d) for d in (1, -1))
    check(f'fold, sign {s:+d} of the transform: the two bonds of a chain give 2 cos k', np.allclose(chain, 2 * np.cos(k[:, 0]), atol=1e-14), True)
    bonds = {(1, 0): 1, (-1, 0): 1, (0, 1): -1, (0, -1): -1}
    dk = sum(a * np.exp(1j * s * (k[:, 0] * dx + k[:, 1] * dy)) for (dx, dy), a in bonds.items())
    ext = sum(np.exp(1j * s * (k[:, 0] * dx + k[:, 1] * dy)) for (dx, dy) in bonds)
    check(f'fold, sign {s:+d}: +1 on the bonds along x and -1 along y give 2 (cos kx - cos ky), the same sign on all four 2 (cos kx + cos ky)',
          np.allclose(dk, 2 * (np.cos(k[:, 0]) - np.cos(k[:, 1])), atol=1e-14) and np.allclose(ext, 2 * (np.cos(k[:, 0]) + np.cos(k[:, 1])), atol=1e-14), True)

# the same with the BdG levels of a torus of 6 x 6 sites in real space: hopping -t, mu, singlet pairing Delta_1 on the
# bonds, +Delta_1 along x and -Delta_1 along y. One block (e up, h down) of the basis (5.6) is [[h, P], [P^dag, -h]],
# with P_{r, r+delta} = Delta_1 eta_delta, and its levels are +-sqrt(eps(k)^2 + (2 Delta_1 (cos kx - cos ky))^2)
L, t, mu, D1 = 6, 1.0, -1.0, 0.1
idx = lambda x, y: (x % L) * L + (y % L)
h = np.zeros((L * L, L * L)); P = np.zeros((L * L, L * L))
for x in range(L):
    for y in range(L):
        r = idx(x, y)
        h[r, r] = -mu
        for (dx, dy), eta in {(1, 0): 1, (-1, 0): 1, (0, 1): -1, (0, -1): -1}.items():
            h[r, idx(x + dx, y + dy)] = -t
            P[r, idx(x + dx, y + dy)] = D1 * eta
check('fold, the pairing on the bonds is even in the bond, P symmetric, so it is a singlet', np.allclose(P, P.T), True)
bdg = np.block([[h, P], [P.T, -h]])
kk = 2 * np.pi * np.arange(L) / L
KX, KY = np.meshgrid(kk, kk, indexing='ij')
eps = -2 * t * (np.cos(KX) + np.cos(KY)) - mu
Dd = 2 * D1 * (np.cos(KX) - np.cos(KY))
exact = np.sort(np.concatenate([np.sqrt(eps ** 2 + Dd ** 2).ravel(), -np.sqrt(eps ** 2 + Dd ** 2).ravel()]))
check('fold, torus of 6 x 6 sites, t=1, mu=-t, Delta_1=0.1: the BdG levels are +-sqrt(eps^2 + (2 Delta_1 (cos kx - cos ky))^2)',
      np.allclose(np.sort(np.linalg.eigvalsh(bdg)), exact, atol=1e-12), round(np.abs(exact).min(), 6))
bdg_flip = np.block([[h, -P], [-P.T, -h]])
check('fold, the overall sign of Delta_1 does not change the levels', np.allclose(np.linalg.eigvalsh(bdg_flip), np.linalg.eigvalsh(bdg), atol=1e-12), True)
# the zeros of cos kx - cos ky inside the zone are the two diagonals
g = np.linspace(-np.pi, np.pi, 801)
GX, GY = np.meshgrid(g, g, indexing='ij')
zero = np.abs(np.cos(GX) - np.cos(GY)) < 1e-12
check('fold, cos kx = cos ky inside the zone only on kx = +-ky', np.all(np.isclose(np.abs(GX[zero]), np.abs(GY[zero]), atol=1e-9)) and zero.sum() > 1000, int(zero.sum()))

# pyqula: add_pairing(mode="dx2y2", delta=x) gives 2x (cos kx - cos ky) at the entries (0,2) and (1,3), so Delta_0 = 2x
from pyqula import geometry
H = geometry.square_lattice().get_hamiltonian(tij=[-1.])
H.add_onsite(1.0)
H.add_pairing(mode="dx2y2", delta=0.1)
hk = H.get_hk_gen()
ok = True
for kx, ky in rng.uniform(-0.5, 0.5, size=(10, 2)):
    m = hk([kx, ky, 0.])
    target = 0.2 * (np.cos(2 * np.pi * kx) - np.cos(2 * np.pi * ky))
    ok = ok and abs(m[0, 2] - target) < 1e-12 and abs(m[1, 3] - target) < 1e-12
    ok = ok and abs(m[0, 0] - (-2 * (np.cos(2 * np.pi * kx) + np.cos(2 * np.pi * ky)) + 1.0)) < 1e-12
check('fold and caption, pyqula dx2y2 with delta=0.1 is Delta_0 = 0.2 of (5.13), and add_onsite(1.0) is mu = -t', ok, True)

# ---------------------------------------------------------------------------------------------------------------
# the lab box: Phi_0/2 = h/4e, and (n + 1/2) Phi_0 for a phase pi added to the winding 2 pi n
h_planck, e = 6.62607015e-34, 1.602176634e-19
check('lab box, Phi_0/2 = h/4e', abs((h_planck / (2 * e)) / 2 - h_planck / (4 * e)) < 1e-30, h_planck / (4 * e))
for n in range(-2, 3):
    phase = 2 * np.pi * n + np.pi                    # the winding with one sign change, 2 pi Phi / Phi_0
    check(f'lab box, our reading, n={n}: a winding 2 pi n + pi gives Phi = (n + 1/2) Phi_0', abs(phase / (2 * np.pi) - (n + 0.5)) < 1e-12, n + 0.5)
# the condition of our reading: a ring of inductance L with one junction of critical current Ic and no applied field.
# The fluxoid 2 pi f + phi = 2 pi n + pi s, with f = Phi/Phi_0, s = 1 for an odd number of sign changes, gives the
# energy E/E_J = (2 pi^2/beta) f^2 - cos(pi s - 2 pi f), with beta = 2 pi L Ic/Phi_0. The trapped flux of the ground
# state is Phi_0/2 only when L Ic is large compared with Phi_0, it is below Phi_0/2 for a smaller ring and zero for beta < 1
fr = np.linspace(-1.5, 1.5, 300001)
trapped = {}
for s in (0, 1):
    for LIc in (0.05, 0.3, 1.6, 16.0, 160.0):        # L Ic in units of Phi_0
        beta = 2 * np.pi * LIc
        E = (2 * np.pi ** 2 / beta) * fr ** 2 - np.cos(np.pi * s - 2 * np.pi * fr)
        trapped[(s, LIc)] = abs(fr[np.argmin(E)])
check('lab box, condition: a ring with no sign change traps no flux for any L Ic', all(trapped[(0, x)] < 1e-9 for x in (0.05, 0.3, 1.6, 16.0, 160.0)),
      [trapped[(0, x)] for x in (0.05, 16.0)])
check('lab box, condition: with an odd number of sign changes the trapped flux grows to Phi_0/2 only for L Ic >> Phi_0',
      trapped[(1, 0.05)] < 1e-9 and 0.25 < trapped[(1, 0.3)] < 0.35 and 0.44 < trapped[(1, 1.6)] < 0.46
      and 0.49 < trapped[(1, 16.0)] < 0.5 and 0.499 < trapped[(1, 160.0)] <= 0.5,
      [round(trapped[(1, x)], 4) for x in (0.05, 0.3, 1.6, 16.0, 160.0)])
# the sentences of the box in the source. The tracked file keeps the quotation with 4.2 K, and the full copy, which git
# ignores, holds the whole abstract pasted from the APS page, with the 0, 2 and 3 junctions, the half flux quantum in
# the ring with 3 junctions and the words "consistent with d-wave pairing symmetry"
srcdir = os.path.join(REPO, 'webnotes', 'sources')
tracked = ' '.join(open(os.path.join(srcdir, 'session05', 'tsuei1994_physrevlett.73.593.txt'), encoding='utf-8').read().split())
check('lab box, the tracked source states the flux through the rings at 4.2 K, measured with a scanning SQUID microscope',
      'The magnetic flux threading these rings at 4.2 K is measured by employing a scanning superconducting quantum interference '
      'device microscope' in tracked, 'found')
full = os.path.join(srcdir, '.full', 'session05', 'tsuei1994_physrevlett.73.593.txt')
if os.path.exists(full):
    text = ' '.join(open(full, encoding='utf-8').read().split())
    for phrase in ('rings with 0, 2, and 3 grain-boundary Josephson junctions to test the pairing symmetry',
                   'Spontaneous magnetization of a half magnetic flux quantum, Φ0/2 = h/4e has been observed in the 3-junction ring, '
                   'but not in the 2-junction rings',
                   'These results are consistent with d-wave pairing symmetry'):
        check('lab box, the full copy of the source says "%s"' % phrase, phrase in text, 'found')
else:
    print('NOT CHECKED the 0, 2 and 3 junctions, the half flux quantum and "consistent with d-wave" of tsuei1994, no full copy '
          'of the source on this machine', flush=True)
# the old text: "up to about 130 K at ambient pressure" for the cuprates, against the tracked abstract of the sulfur hydride
hydride = ' '.join(open(os.path.join(srcdir, 'session05', 'drozdov2015_nature14964.txt'), encoding='utf-8').read().split())
check('old text, about 130 K: the stored abstract of the sulfur hydride gives 133 K at ambient pressure for the cuprates, 2% away',
      'The highest Tc that has been achieved in cuprates1 is 133 K at ambient pressure' in hydride and abs(130 - 133) / 133 < 0.03,
      round(abs(130 - 133) / 133, 3))

# the first quiz: cos 3 theta has six lobes of alternating sign and is odd under theta -> theta + pi
th = np.linspace(0, 2 * np.pi, 3601)
f = np.cos(3 * th)
changes = np.sum(np.diff(np.sign(f[np.abs(f) > 1e-9])) != 0)
check('first quiz, cos 3 theta changes sign 6 times around the circle, six lobes', changes == 6, int(changes))
check('first quiz, cos(3 theta + 3 pi) = -cos 3 theta', np.allclose(np.cos(3 * (th + np.pi)), -f, atol=1e-12), True)

# ---------------------------------------------------------------------------------------------------------------
# the problem: Delta_ext = Delta_0 (cos kx + cos ky) on the Fermi surface of -2t (cos kx + cos ky) - mu = 0
t, D0 = 1.0, 1.0
for mu, want in ((-1.0, 0.5), (0.0, 0.0)):
    kx = np.linspace(-np.pi, np.pi, 4001)
    cy = -mu / (2 * t) - np.cos(kx)
    sel = np.abs(cy) <= 1
    ky = np.arccos(cy[sel])
    pts = np.c_[kx[sel], ky]
    epsv = -2 * t * (np.cos(pts[:, 0]) + np.cos(pts[:, 1])) - mu
    gap = D0 * (np.cos(pts[:, 0]) + np.cos(pts[:, 1]))
    check(f'problem, mu={mu}: on {len(pts)} points of the Fermi surface the gap is {want} Delta_0 everywhere',
          np.allclose(epsv, 0, atol=1e-12) and np.allclose(gap, want * D0, atol=1e-12), (round(gap.min(), 12), round(gap.max(), 12)))
kx = np.linspace(-np.pi, np.pi, 1001)
check('problem, mu=0: the Fermi surface is the square |kx| + |ky| = pi', np.allclose(np.cos(kx) + np.cos(np.pi - np.abs(kx)), 0, atol=1e-12), True)
# what STM sees, the density of states, which sums over the whole zone: the smallest energy over all k. At mu=-t the
# spectrum has a full gap, of the order of Delta_0/2, for any Delta_0. At mu=0 the gap is -Delta_0 eps/2t, so
# E = |eps| sqrt(1 + Delta_0^2/4t^2), which goes to zero on the whole Fermi surface, as a metal with a faster band
Lz = 400                                              # a multiple of 4, so (pi/2, pi/2) is on the mesh
kz = 2 * np.pi * np.arange(Lz) / Lz - np.pi
ZX, ZY = np.meshgrid(kz, kz, indexing='ij')
for D0z in (0.2, 0.5):
    E = {}
    for mu in (-1.0, 0.0):
        epsz = -2 * t * (np.cos(ZX) + np.cos(ZY)) - mu
        E[mu] = np.sqrt(epsz ** 2 + (D0z * (np.cos(ZX) + np.cos(ZY))) ** 2)
    check(f'problem, Delta_0={D0z}: at mu=-t the smallest energy over the whole zone is a full gap, close to and not above Delta_0/2',
          0.9 * D0z / 2 < E[-1.0].min() <= D0z / 2 + 1e-12, round(E[-1.0].min() / D0z, 4))
    epsz = -2 * t * (np.cos(ZX) + np.cos(ZY))
    check(f'problem, Delta_0={D0z}: at mu=0 the energy is |eps| sqrt(1 + Delta_0^2/4t^2), so states reach zero energy on the Fermi surface',
          np.allclose(E[0.0], np.abs(epsz) * np.sqrt(1 + D0z ** 2 / (4 * t ** 2)), atol=1e-12) and E[0.0].min() < 1e-12
          and np.mean(E[0.0] < 0.05) > 0.005, round(np.mean(E[0.0] < 0.05), 4))

# ---------------------------------------------------------------------------------------------------------------
# the try-it box: the notebook cell, add_pairing swave 0.4 and nodal_fwave 0.2 on the triangular lattice at the Fermi
# level 0. The s-wave keeps 0.4 at the Fermi surface, and the f-wave vanishes at (1/3, 0) on Gamma-M, which is on it
G = geometry.triangular_lattice()
Hs = G.get_hamiltonian(); Hs.add_pairing(mode="swave", delta=0.4)
Hf = G.get_hamiltonian(); Hf.add_pairing(mode="nodal_fwave", delta=0.2)
H0 = G.get_hamiltonian()
node = [1 / 3, 0., 0.]
check('try-it, eps = 0 at (1/3, 0), two thirds of the way from Gamma to M, so it is on the Fermi surface',
      np.abs(np.linalg.eigvalsh(H0.get_hk_gen()(node))).max() < 1e-12, True)
es = np.abs(np.linalg.eigvalsh(Hs.get_hk_gen()(node))).min()
ef = np.abs(np.linalg.eigvalsh(Hf.get_hk_gen()(node))).min()
check('try-it, the s-wave smallest quasiparticle energy at that point of the Fermi surface is 0.4', abs(es - 0.4) < 1e-12, es)
check('try-it, the f-wave energy at that point is zero, a node', ef < 1e-12, ef)
