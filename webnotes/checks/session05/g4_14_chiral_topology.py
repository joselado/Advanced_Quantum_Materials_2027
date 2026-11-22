"""Session 5, the numbers that page 14 (Section 5.14) quotes and that no figure script asserts.

One check script per page is the rule: every number of a caption, a feedback, a fold, a solution or a lab box is an
assert, here or in the figure script that draws it. The ribbon figure and the three pictures of the quiz assert their
statements in figures/session05/_g4_ribbon.py (the empty gap 0.40 of the s-wave ribbon, C = 0 and -2 from
h.get_chern(), two branches per edge going down at y > 0 and up at y < 0, no edge state in the f-wave ribbon). This
script holds the rest: the bulk numbers of the caption, the fold on the 2x2 block (5.8), the two quizzes with numbers,
the range of the key box and the problem. It also runs the downloadable script and _g4_ribbon.check on its data, so
the statements of the figure are asserted by build.py --verify too, and it asserts from the eigenvectors that no state
of the f-wave ribbon sits at an edge. It finds the repository from its own path and runs pyqula in a temporary folder,
so it writes no file.

Run it from anywhere:  python3 webnotes/checks/session05/g4_14_chiral_topology.py"""
import os
import sys
import tempfile
from functools import partial

import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures'))
import physcheck  # noqa: E402


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# ---------------------------------------------------------------------------------------------------------------
# The fold: one block (5.8) on the square lattice, eps = -2t(cos kx + cos ky) - mu with t = 1, written as d.tau with
# d = (Re Delta, -Im Delta, eps). The Chern number of the lower band, with the Berry curvature of Session 3.
# ---------------------------------------------------------------------------------------------------------------
BSQ = 2 * np.pi * np.eye(2)


def pairing(kind, D0, kx, ky):
    if kind == 's':
        return D0 + 0 * kx
    sign = {'p+ip': 1, 'p-ip': -1}[kind]
    return D0 * (np.sin(kx) + sign * 1j * np.sin(ky))


def block(mu, D0, kind, flip=1):
    """The block (5.8), with flip = -1 for the second spin block of the triplet, which carries -Delta."""
    def hk(k):
        eps = -2 * (np.cos(k[0]) + np.cos(k[1])) - mu
        D = flip * pairing(kind, D0, k[0], k[1])
        return np.array([[eps, D], [np.conj(D), -eps]])
    return hk


def degree(mu, D0, kind, n=240):
    """How many times d/|d| covers the unit sphere, (1/4 pi) int dhat.(d_x dhat x d_y dhat) on an n x n mesh."""
    s = np.arange(n) * 2 * np.pi / n
    kx, ky = np.meshgrid(s, s, indexing='ij')
    D = pairing(kind, D0, kx, ky)
    d = np.stack([D.real, -D.imag, -2 * (np.cos(kx) + np.cos(ky)) - mu])
    d = d / np.linalg.norm(d, axis=0)
    dx = (np.roll(d, -1, axis=1) - np.roll(d, 1, axis=1)) / 2
    dy = (np.roll(d, -1, axis=2) - np.roll(d, 1, axis=2)) / 2
    return np.sum(d * np.cross(dx, dy, axis=0)) / (4 * np.pi)


C = {}
for mu in (-3.5, -2.0, -1.0, 1.0, 3.0):
    for kind in ('p+ip', 'p-ip'):
        C[mu, kind] = physcheck.chern_links(block(mu, 0.5, kind), BSQ, bands=0, nk=48)
check('block of p+ip, filled pocket around Gamma (mu=-3.5,-2,-1), the fold says C=+1',
      all(abs(C[mu, 'p+ip'] - 1) < 1e-6 for mu in (-3.5, -2.0, -1.0)), [round(C[mu, 'p+ip'], 6) for mu in (-3.5, -2, -1)])
check('block of p-ip, the same pockets, the fold says C=-1',
      all(abs(C[mu, 'p-ip'] + 1) < 1e-6 for mu in (-3.5, -2.0, -1.0)), [round(C[mu, 'p-ip'], 6) for mu in (-3.5, -2, -1)])
check('block of p+ip, empty pocket around M (mu=1,3), the fold says the sign is reversed',
      all(abs(C[mu, 'p+ip'] + 1) < 1e-6 and abs(C[mu, 'p-ip'] - 1) < 1e-6 for mu in (1.0, 3.0)),
      [(round(C[mu, 'p+ip'], 6), round(C[mu, 'p-ip'], 6)) for mu in (1.0, 3.0)])
kubo = physcheck.chern_kubo(block(-2.0, 0.5, 'p+ip'), BSQ, bands=0, nk=96)
check('the Kubo form agrees with the links for p+ip at mu=-2', abs(kubo - 1) < 2e-2, round(kubo, 4))
cs = physcheck.chern_links(block(-2.0, 0.5, 's'), BSQ, bands=0, nk=48)
check('block of s-wave, the fold says C=0', abs(cs) < 1e-6, round(cs, 6))
cf = [physcheck.chern_links(block(mu, 0.5, 'p+ip', flip=-1), BSQ, bands=0, nk=48) for mu in (-2.0, 1.0)]
check('the block with -Delta has the same C, the fold says so', abs(cf[0] - 1) < 1e-6 and abs(cf[1] + 1) < 1e-6,
      [round(c, 6) for c in cf])
deg = [degree(mu, 0.5, kind) for mu, kind in ((-2.0, 'p+ip'), (-2.0, 'p-ip'), (1.0, 'p+ip'), (-2.0, 's'))]
check('d/|d| covers the sphere once for p+-ip and not at all for s-wave, |degree| = |C|',
      all(abs(abs(x) - 1) < 1e-2 for x in deg[:3]) and abs(deg[3]) < 1e-6
      and all(abs(abs(x) - abs(C[m, kd])) < 1e-2 for x, (m, kd) in zip(deg[:3], ((-2.0, 'p+ip'), (-2.0, 'p-ip'), (1.0, 'p+ip')))),
      [round(x, 4) for x in deg])
# the pictures of the fold: d points down at Gamma inside a filled pocket and up outside, and lies in the plane on
# the Fermi surface. At mu=-2 the Fermi surface is cos kx + cos ky = 1, so eps(Gamma) = -2 < 0 and eps(X), eps(M) > 0.
eps = lambda kx, ky, mu: -2 * (np.cos(kx) + np.cos(ky)) - mu  # noqa: E731
mus = np.linspace(-3.99, -0.01, 200)
check('the fold: for -4t<mu<0, Gamma is the only zero of Delta_p+ip with eps<0, so a pocket of filled states',
      all(eps(0, 0, m) < 0 and eps(np.pi, 0, m) > 0 and eps(0, np.pi, m) > 0 and eps(np.pi, np.pi, m) > 0 for m in mus), True)
mus = np.linspace(0.01, 3.99, 200)
check('the fold: for 0<mu<4t, (pi,pi) is the only zero with eps>0, a pocket of empty states around it',
      all(eps(np.pi, np.pi, m) > 0 and eps(np.pi, 0, m) < 0 and eps(0, np.pi, m) < 0 and eps(0, 0, m) < 0 for m in mus), True)
check('mu=-2: eps(Gamma) < 0, eps(X) > 0, eps(M) > 0', eps(0, 0, -2) < 0 and eps(np.pi, 0, -2) > 0
      and eps(np.pi, np.pi, -2) > 0, (eps(0, 0, -2), eps(np.pi, 0, -2), eps(np.pi, np.pi, -2)))
th = np.linspace(0, 2 * np.pi, 2001)
rays = []                                                      # the Fermi momentum along each direction theta
for t in th[:-1]:
    lo, hi = 0.0, np.pi / max(abs(np.cos(t)), abs(np.sin(t)))   # from Gamma to the boundary of the zone along the ray
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if eps(mid * np.cos(t), mid * np.sin(t), -2) < 0 else (lo, mid)
    rays.append(lo)
rays = np.array(rays)
ph = np.unwrap(np.angle(pairing('p+ip', 1, rays * np.cos(th[:-1]), rays * np.sin(th[:-1]))))
check('the phase of p+ip winds once around the Fermi surface at mu=-2', abs((ph[-1] - ph[0]) / (2 * np.pi) - 1) < 1e-2,
      round((ph[-1] - ph[0]) / (2 * np.pi), 3))
# the fold: (5.15) vanishes only at Gamma, (pi,0), (0,pi) and (pi,pi). Since |sin x| >= (2/pi)|x| for |x| <= pi/2,
# |Delta|/Delta_0 is at least 2/pi times the distance to the nearest of the four points, checked on a mesh
s = np.linspace(-np.pi, np.pi, 1201)
ZX, ZY = np.meshgrid(s, s, indexing='ij')
near4 = lambda x: np.min(np.abs(x[..., None] - np.array([-np.pi, 0., np.pi])), axis=-1)  # noqa: E731
dk = np.hypot(near4(ZX), near4(ZY))
aD = np.abs(pairing('p+ip', 1, ZX, ZY))
check('the fold: (5.15) vanishes only at Gamma, (pi,0), (0,pi), (pi,pi), |Delta|/Delta_0 >= (2/pi) x distance to them',
      np.all(aD >= 2 / np.pi * dk - 1e-12) and aD[dk < 1e-12].max() < 1e-12, round(float(aD[dk > 0.05].min()), 4))

# ---------------------------------------------------------------------------------------------------------------
# The first quiz: the square lattice at mu = -2t with Delta_0 = 0.2t. The smallest energy is 0.2t for both, one
# pocket around Gamma, and C = +2 for the chiral pairing with both spins in pyqula.
# ---------------------------------------------------------------------------------------------------------------
def smallest(mu, D0, kind):
    f = lambda k: np.sqrt(eps(k[0], k[1], mu) ** 2 + abs(pairing(kind, D0, k[0], k[1])) ** 2)  # noqa: E731
    ks = np.linspace(-np.pi, np.pi, 121)
    grid = sorted((f([a, b]), a, b) for a in ks for b in ks)[:12]
    return min(minimize(f, [a, b], method='Nelder-Mead', options=dict(xatol=1e-10, fatol=1e-13)).fun for _, a, b in grid)


e_s, e_p = smallest(-2.0, 0.2, 's'), smallest(-2.0, 0.2, 'p+ip')
check('quiz 1, smallest energy at mu=-2t, Delta_0=0.2t, the page says 0.2t for both', abs(e_s - 0.2) < 1e-6
      and abs(e_p - 0.2) < 1e-6, (round(e_s, 6), round(e_p, 6)))
from scipy import ndimage  # noqa: E402
ks = np.linspace(-np.pi, np.pi, 201)
KX, KY = np.meshgrid(ks, ks, indexing='ij')
filled = eps(KX, KY, -2.0) < 0
lab, n = ndimage.label(filled)
check('quiz 1, one pocket around Gamma at mu=-2t, away from the boundary of the zone', n == 1 and filled[100, 100]
      and not filled[0, :].any() and not filled[:, 0].any(), n)
# the key box: for 0<|mu|<4t the Fermi surface of the square lattice is a single pocket, of filled states around
# Gamma for mu<0 and of empty states around (pi,pi) for mu>0, and for |mu|>4t the band has no Fermi surface
sg = np.linspace(-np.pi, np.pi, 240, endpoint=False)
G1, G2 = np.meshgrid(sg, sg, indexing='ij')


def one_pocket(region):
    """One connected region that holds the center of the grid and does not touch its border."""
    lab_, n_ = ndimage.label(region)
    return n_ == 1 and region[120, 120] and not (region[0, :].any() or region[-1, :].any() or region[:, 0].any()
                                                   or region[:, -1].any())


pockets = [one_pocket(eps(G1, G2, mu) < 0) for mu in (-3.9, -3.0, -2.0, -1.0, -0.3)]
pockets += [one_pocket(eps(G1 + np.pi, G2 + np.pi, mu) > 0) for mu in (0.3, 1.0, 3.0, 3.9)]
check('the key box: for 0<|mu|<4t a single pocket, filled around Gamma (mu<0) or empty around (pi,pi) (mu>0)',
      all(pockets), pockets)
check('the key box: for |mu|>4t the Fermi level is outside the band, eps has one sign', all(
      np.all(np.sign(eps(G1, G2, mu)) == np.sign(-mu)) for mu in (-4.5, 4.5)), True)
e_p35 = smallest(-3.5, 0.2, 'p+ip')
check('the sheet: at mu=-3.5t the two smallest energies differ, so the quiz names mu=-2t', abs(e_p35 - 0.1314) < 1e-3,
      round(e_p35, 4))

os.chdir(tempfile.mkdtemp())
from pyqula import geometry, ribbon  # noqa: E402,F401
from pyqula.sctk.pairing import get_triplet  # noqa: E402
from pyqula.utilities import get_callable  # noqa: E402

gs = geometry.square_lattice()
hs = gs.get_hamiltonian(tij=[-1.])
hs.add_onsite(2.0)                                     # mu = -2 of the notes
hs.add_pairing(mode="chiral_pwave", delta=0.1)          # Delta_0 = 2 delta = 0.2
entry = np.asarray(hs.get_hk_gen()([0.1, 0.2, 0.])[0, 2])
kx, ky = 2 * np.pi * 0.1, 2 * np.pi * 0.2
check('chiral_pwave 0.1 on the square lattice has |Delta| = 0.2 |sin kx + i sin ky|',
      abs(abs(entry) - 0.2 * abs(np.sin(kx) + 1j * np.sin(ky))) < 1e-12, round(abs(entry), 6))
c_full = hs.get_chern()
check('quiz 1, the chiral pairing with both spins at mu=-2t, C=+2, which the page writes as +-2', abs(c_full - 2) < 1e-6,
      round(c_full, 6))
hm = gs.get_hamiltonian(tij=[-1.])
hm.add_onsite(2.0)
hm.add_pairing(mode=partial(get_triplet, df=get_callable([0., 0., 1.]), L=-1), delta=0.1)
c_minus = hm.get_chern()
check('the kept quiz on p_x-ip_y: with this pocket of filled states C goes from +2 to -2', abs(c_minus + 2) < 1e-6,
      round(c_minus, 6))
# the key box: C = +-2 with both spins for 0<|mu|<4t and C = 0 outside the band. h.get_chern() with its default mesh
# gives 1.0 at mu=-3.9, close to the bottom of the band, so the mesh is given here, and the links agree
scan = {}
for mu in (-3.9, -3.0, -1.0, -0.3, 0.3, 1.0, 3.0, 3.9, -4.5, 4.5):
    hq = gs.get_hamiltonian(tij=[-1.])
    hq.add_onsite(-mu)                                  # mu of the notes
    hq.add_pairing(mode="chiral_pwave", delta=0.25)      # Delta_0 = 0.5
    hkq, Bq = physcheck.from_pyqula(hq)
    scan[mu] = (round(hq.get_chern(nk=60), 6), round(physcheck.chern_links(hkq, Bq, bands=range(2), nk=60), 6))
want = {mu: (2 if -4 < mu < 0 else -2 if 0 < mu < 4 else 0) for mu in scan}
check('the key box: chiral p-wave with both spins on the square lattice, C=+2 for -4t<mu<0, -2 for 0<mu<4t, 0 outside',
      all(abs(a - want[mu]) < 1e-6 and abs(b - want[mu]) < 1e-6 for mu, (a, b) in scan.items()), scan)

# ---------------------------------------------------------------------------------------------------------------
# The caption of the ribbon figure: the bulk of the notebook model, triangular lattice with add_onsite(-3.0)
# ---------------------------------------------------------------------------------------------------------------
g = geometry.triangular_lattice()
h0 = g.get_hamiltonian(has_spin=False)
h0.add_onsite(-3.0)
hk0, BT = physcheck.from_pyqula(h0)
K = (BT[0] + BT[1]) / 3
check('the band with add_onsite(-3.0) is +3 at Gamma and -6 at K, so the empty states form a pocket around Gamma',
      abs(hk0([0, 0])[0, 0].real - 3) < 1e-12 and abs(hk0(K)[0, 0].real + 6) < 1e-9, (hk0([0, 0])[0, 0].real, round(hk0(K)[0, 0].real, 9)))
# the caption: the band of pyqula with no onsite energy runs from -3 to 6, on a mesh that holds Gamma, K and M
band = np.array([hk0(p)[0, 0].real + 3.0 for p in physcheck.kmesh(BT, 120)])
check('the caption: the band of pyqula runs from -3 to 6, so add_onsite(-3.0) is mu=3 inside the band',
      abs(band.min() + 3) < 1e-9 and abs(band.max() - 6) < 1e-9, (round(band.min(), 9), round(band.max(), 9)))
# the key box and the caption: on this model the empty states form a single pocket around Gamma, which is the only
# zero of the chiral pairing inside it. The grid is the reduced zone centered at Gamma.
N = 240
u = np.arange(N) / N - 0.5
cell = [(a * BT[0] + b * BT[1]) for a in u for b in u]
eps_c = np.array([hk0(p)[0, 0].real for p in cell]).reshape(N, N)
lab_t, n_t = ndimage.label(eps_c > 0)
check('the caption: the empty states of the figure model are one pocket around Gamma, away from the border of the cell',
      n_t == 1 and eps_c[N // 2, N // 2] > 0 and not (eps_c[0, :] > 0).any() and not (eps_c[:, 0] > 0).any(), n_t)


def bulk(mode):
    hb = g.get_hamiltonian()
    hb.add_onsite(-3.0)
    hb.add_pairing(mode=mode, delta=0.4)
    return hb


def bulk_min(hb):
    hk, B = physcheck.from_pyqula(hb)
    f = lambda k: np.abs(np.linalg.eigvalsh(hk(k))).min()  # noqa: E731
    pts = physcheck.kmesh(B, 60)
    best = sorted(pts, key=f)[:6]
    return min(minimize(f, p, method='Nelder-Mead', options=dict(xatol=1e-10, fatol=1e-13)).fun for p in best)


hp, hsw = bulk("chiral_pwave"), bulk("swave")
hk, B = physcheck.from_pyqula(hp)
q = 1e-3
ratio = [hk(np.array([0., q]))[i, j] / hk(np.array([q, 0.]))[i, j] for i, j in ((0, 2), (1, 3))]
check('chiral_pwave on the triangular lattice is p_x+ip_y close to Gamma, Delta(0,q)/Delta(q,0) = +i in both blocks',
      all(abs(r - 1j) < 1e-9 for r in ratio), [complex(np.round(r, 9)) for r in ratio])
inpocket = [(np.linalg.norm(p), abs(hk(p)[0, 2])) for p, e_ in zip(cell, eps_c.ravel()) if e_ > 0]
far_ = [a for r_, a in inpocket if r_ > 0.05]
check('the key box: Gamma is the only zero of the chiral pairing inside the pocket of the figure model',
      abs(hk(np.zeros(2))[0, 2]) < 1e-12 and min(far_) > 0.02, round(min(far_), 4))
# a second route to the chirality: the winding of the entry (0,2) on a small circle around Gamma, +1 for chiral_pwave,
# and -1 for the pairing of the other chirality of the sheet, which gives C=+2 on the same model
hm3 = g.get_hamiltonian()
hm3.add_onsite(-3.0)
hm3.add_pairing(mode=partial(get_triplet, df=get_callable([0., 0., 1.]), L=-1), delta=0.4)
hkm, _ = physcheck.from_pyqula(hm3)
circ = np.linspace(0, 2 * np.pi, 721)
wind = []
for f_ in (hk, hkm):
    ph = np.unwrap(np.angle([f_(0.05 * np.array([np.cos(a_), np.sin(a_)]))[0, 2] for a_ in circ]))
    wind.append((ph[-1] - ph[0]) / (2 * np.pi))
check('chirality by a second route: the entry (0,2) winds +1 around Gamma for chiral_pwave and -1 for L=-1',
      abs(wind[0] - 1) < 1e-6 and abs(wind[1] + 1) < 1e-6, [round(w, 6) for w in wind])
c_m3 = hm3.get_chern()
check('the other chirality gives C=+2 on the notebook model', abs(c_m3 - 2) < 1e-6, round(c_m3, 6))
kq = np.array([0.31, 0.47])
check('chiral_pwave pairs one spin up with one spin down: the entries (0,3) and (1,2) of equal spins are zero',
      abs(hk(kq)[0, 3]) < 1e-14 and abs(hk(kq)[1, 2]) < 1e-14 and abs(hk(kq)[0, 2]) > 0.1,
      (abs(hk(kq)[0, 3]), abs(hk(kq)[1, 2]), round(abs(hk(kq)[0, 2]), 4)))
check('its two spin blocks carry Delta and -Delta', abs(hk(np.array([q, 0.3]))[0, 2] + hk(np.array([q, 0.3]))[1, 3]) < 1e-12,
      True)
m_p, m_s = bulk_min(hp), bulk_min(hsw)
check('the caption: smallest bulk energy of the chiral p-wave, the page says 1.34', abs(m_p - 1.34) < 5e-3, round(m_p, 4))
check('the caption: smallest bulk energy of the s-wave, the page says 0.40', abs(m_s - 0.40) < 1e-6, round(m_s, 6))
hk, B = physcheck.from_pyqula(hp)
cl = physcheck.chern_links(hk, B, bands=range(2), nk=30)
check('the caption: C=-2 for the chiral p-wave by the links too, with the sign of h.get_chern()',
      abs(cl + 2) < 1e-6 and abs(hp.get_chern() + 2) < 1e-6, round(cl, 6))
hk, B = physcheck.from_pyqula(hsw)
cl = physcheck.chern_links(hk, B, bands=range(2), nk=30)
check('the caption: C=0 for the s-wave', abs(cl) < 1e-6 and abs(hsw.get_chern()) < 1e-6, round(cl, 6))

# the f-wave picture: the gap vanishes on the lines Gamma-M, which cross the Fermi surface of this model, so the bulk
# has nodes, and their momenta along the ribbon (along x) are 0 and +-arccos(1/4) = +-1.318
hf = bulk("nodal_fwave")
hkf, B = physcheck.from_pyqula(hf)
nodes = []
for M in (B[0] / 2, B[1] / 2, (B[1] - B[0]) / 2):
    s = np.linspace(0, 1, 4001)
    e = np.array([hk0(x * M)[0, 0].real for x in s])
    j = np.where(np.diff(np.sign(e)) != 0)[0]
    assert len(j) == 1
    x = s[j[0]] - e[j[0]] * (s[j[0] + 1] - s[j[0]]) / (e[j[0] + 1] - e[j[0]])
    for _ in range(40):                                  # Newton steps on eps along the line
        de = (hk0((x + 1e-6) * M)[0, 0].real - hk0((x - 1e-6) * M)[0, 0].real) / 2e-6
        x -= hk0(x * M)[0, 0].real / de
    nodes.append((x * M, np.abs(np.linalg.eigvalsh(hkf(x * M))).min()))
check('the f-wave bulk has E=0 where Gamma-M crosses the Fermi surface', max(v for _, v in nodes) < 1e-8,
      [float('%.1e' % v) for _, v in nodes])
kxs = sorted(abs(p[0]) for p, _ in nodes)
check('the nodes sit at k_x = 0 and +-1.32 along the ribbon', abs(kxs[0]) < 1e-9 and abs(kxs[1] - 1.318) < 1e-3
      and abs(kxs[2] - 1.318) < 1e-3 and abs(np.arccos(0.25) - 1.318) < 1e-3, [round(x, 4) for x in kxs])

# ---------------------------------------------------------------------------------------------------------------
# The problem: Delta_0 (sin kx + i sin ky) on the circle of radius 0.3 around Gamma
# ---------------------------------------------------------------------------------------------------------------
th = np.linspace(0, 2 * np.pi, 20001)
r = 0.3
Dp = np.sin(r * np.cos(th)) + 1j * np.sin(r * np.sin(th))
Dm = np.sin(r * np.cos(th)) - 1j * np.sin(r * np.sin(th))
wp = (np.unwrap(np.angle(Dp))[-1] - np.angle(Dp)[0]) / (2 * np.pi)
wm = (np.unwrap(np.angle(Dm))[-1] - np.angle(Dm)[0]) / (2 * np.pi)
check('the problem, winding of p+ip and of p-ip on the circle, the page says +1 and -1', abs(wp - 1) < 1e-9
      and abs(wm + 1) < 1e-9, (round(wp, 6), round(wm, 6)))
c_, s_ = np.abs(np.cos(th)) > 1e-6, np.abs(np.sin(th)) > 1e-6
check('the problem, same quadrant: Re has the sign of cos(theta) and Im of sin(theta)',
      np.all(np.sign(Dp.real[c_]) == np.sign(np.cos(th[c_]))) and np.all(np.sign(Dp.imag[s_]) == np.sign(np.sin(th[s_]))),
      True)
amin, amax = np.abs(Dp).min(), np.abs(Dp).max()
check('the problem, |Delta|/Delta_0 from 0.2955 at theta=0 to 0.2978 at theta=pi/4', abs(amin - 0.2955) < 5e-5
      and abs(amax - 0.2978) < 5e-5 and abs(np.abs(Dp)[0] - amin) < 1e-12
      and abs(abs(np.sin(r / np.sqrt(2))) * np.sqrt(2) - amax) < 1e-9, (round(amin, 5), round(amax, 5)))
check('the problem, sin(0.3)^2 = 0.0873 and 2 sin(0.3/sqrt2)^2 = 0.0887', abs(np.sin(0.3) ** 2 - 0.0873) < 5e-5
      and abs(2 * np.sin(0.3 / np.sqrt(2)) ** 2 - 0.0887) < 5e-5, (round(np.sin(0.3) ** 2, 5), round(2 * np.sin(0.3 / np.sqrt(2)) ** 2, 5)))
approx = 0.09 - 0.3 ** 4 / 3 * (np.cos(th) ** 4 + np.sin(th) ** 4)
check('the problem, |Delta|^2 is 0.09 - (0.3^4/3)(cos^4 + sin^4) to 4e-5, much less than its variation 0.0013, and the '
      'factor is 1 on the axes and 1/2 on the diagonals',
      np.abs(np.abs(Dp) ** 2 - approx).max() < 4e-5 and np.ptp(np.abs(Dp) ** 2) > 30 * np.abs(np.abs(Dp) ** 2 - approx).max() and abs(np.cos(np.pi / 4) ** 4 + np.sin(np.pi / 4) ** 4 - 0.5) < 1e-12,
      float('%.1e' % np.abs(np.abs(Dp) ** 2 - approx).max()))
check('the problem, within 2 percent of 0.3 Delta_0', abs(amin - 0.3) / 0.3 < 0.02 and abs(amax - 0.3) / 0.3 < 0.02,
      round(abs(amin - 0.3) / 0.3, 4))
# the end of the solution: the square lattice with mu = -2t(1 + cos 0.3) = -3.91t has a pocket of radius 0.3, and
# the smallest quasiparticle energy on it is close to the smallest |Delta| of the circle only for a weak pairing
mu_p = -2 * (1 + np.cos(0.3))
radii = []
for t_ in np.linspace(0, np.pi / 2, 91):                  # the pocket has the symmetry of the square
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if eps(mid * np.cos(t_), mid * np.sin(t_), mu_p) < 0 else (lo, mid)
    radii.append(lo)
check('the solution, mu=-2t(1+cos 0.3), about -3.911t, gives the pocket of radius 0.3, 0.3 along k_x and within 0.001 of it in every direction',
      abs(mu_p + 3.91) < 5e-3 and abs(radii[0] - 0.3) < 1e-9 and max(abs(np.array(radii) - 0.3)) < 1e-3,
      (round(mu_p, 4), round(min(radii), 4), round(max(radii), 4)))


def smallest_local(mu, D0):
    """The smallest energy of p+ip near Gamma, (value, |k| where it sits), from a local grid and Nelder-Mead."""
    f = lambda k: np.sqrt(eps(k[0], k[1], mu) ** 2 + abs(pairing('p+ip', D0, k[0], k[1])) ** 2)  # noqa: E731
    kk = np.linspace(-0.6, 0.6, 121)
    best = sorted((f([a, b]), a, b) for a in kk for b in kk)[:10]
    res = min((minimize(f, [a, b], method='Nelder-Mead', options=dict(xatol=1e-12, fatol=1e-14)) for _, a, b in best),
              key=lambda r: r.fun)
    return res.fun, np.linalg.norm(res.x)


(e05, k05), (e20, k20) = smallest_local(mu_p, 0.05), smallest_local(mu_p, 0.2)
check('the solution, Delta_0=0.05t gives the smallest energy 0.295 Delta_0, close to the smallest |Delta| 0.2955 Delta_0',
      round(e05 / 0.05, 3) == 0.295 and abs(e05 / 0.05 - amin) < 2e-3, (round(e05 / 0.05, 5), round(k05, 4)))
check('the solution, Delta_0=0.2t gives 0.28 Delta_0, with the minimum inside the pocket where |Delta| is smaller',
      abs(e20 / 0.2 - 0.28) < 1e-3 and k20 < 0.29 and k20 < k05 - 0.02, (round(e20 / 0.2, 5), round(k20, 4)))

# ---------------------------------------------------------------------------------------------------------------
# The caption and the lead-in of the ribbon figure: the notebook takes delta=1.0 for the s-wave and 0.4 for the chiral
# p-wave, on the triangular lattice with add_onsite(-3.0), and the downloadable script takes 0.4 for both
# ---------------------------------------------------------------------------------------------------------------
import json  # noqa: E402
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
nb = json.load(open(os.path.join(REPO, 'jupyter-notebooks', 'session5.ipynb')))
srcs = [''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'code']
both = [s for s in srcs if 'plot_case("swave",1.0)' in s and 'plot_case("chiral_pwave",0.4)' in s
        and 'triangular_lattice()' in s and 'h.add_onsite(-3.0)' in s]
check('the caption: the bulk cell and the edge cell of the notebook take swave 1.0 and chiral_pwave 0.4',
      len(both) == 2 and sum('bulk2ribbon(g,n=20)' in s for s in both) == 1, len(both))
script = open(os.path.join(REPO, 'webnotes', 'scripts', 'session05', 'g4_pwave_ribbon.py')).read()
check('the caption: the downloadable script takes delta=0.4 for every pairing and add_onsite(-3.0)',
      script.count('add_pairing(mode=mode, delta=0.4)') == 2 and script.count('add_onsite(-3.0)') == 2
      and 'delta=1.0' not in script, True)

# ---------------------------------------------------------------------------------------------------------------
# The ribbon figure and the picture quiz: the asserts of _g4_ribbon.check on the data of the downloadable script, so
# that build.py --verify runs them too, and the edge weight of the states from the eigenvectors
# ---------------------------------------------------------------------------------------------------------------
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures', 'session05'))
import _g4_ribbon  # noqa: E402

d = _g4_ribbon.load(_g4_ribbon.style.run_script('session05/g4_pwave_ribbon.py'))
_g4_ribbon.check(d)
check('the ribbon figure: _g4_ribbon.check holds on the data of the downloadable script', True, d['modes'])
inwin = np.abs(d['energies'][2]) < _g4_ribbon.ELIM
check('quiz 3, f-wave: every state drawn in the window |E|<3 has its mean position y in the middle, so it is grey',
      inwin.sum() > 0 and np.abs(d['positions'][2][inwin]).max() < 1e-6, float('%.1e' % np.abs(d['positions'][2][inwin]).max()))
# <y> = 0 also holds for a state shared by the two edges, so we take the weight on the two outer rows of one edge,
# maximized over each degenerate subspace, which does not depend on the eigenvectors that the solver returns
gr = ribbon.bulk2ribbon(g, n=20)
yr = np.array(gr.r)[:, 1]
rows = [np.repeat(yr > yr.max() - 1.5, 4).astype(float), np.repeat(yr < yr.min() + 1.5, 4).astype(float)]


def edge_weight(mode, elim):
    hr = gr.get_hamiltonian()
    hr.add_onsite(-3.0)
    hr.add_pairing(mode=mode, delta=0.4)
    f = hr.get_hk_gen()
    worst = 0.0
    for ks in np.asarray(d['ks']):
        w, v = np.linalg.eigh(f([ks, 0., 0.]))
        idx = np.where(np.abs(w) < elim)[0]
        i = 0
        while i < len(idx):
            j = i
            while j + 1 < len(idx) and abs(w[idx[j + 1]] - w[idx[i]]) < 1e-8:
                j += 1
            V = v[:, idx[i:j + 1]]
            worst = max(worst, max(np.linalg.eigvalsh(V.conj().T @ (P[:, None] * V)).max() for P in rows))
            i = j + 1
    return worst


wf, ws, wc = edge_weight("nodal_fwave", 3.0), edge_weight("swave", 3.0), edge_weight("chiral_pwave", 1.0)
check('quiz 3, f-wave: no state in the window sits at an edge, the weight on the two outer rows of one edge is at most '
      'that of the s-wave bulk, against the chiral edge states', wf < 0.16 and abs(wf - ws) < 0.01 and wc > 0.8,
      (round(wf, 4), round(ws, 4), round(wc, 4)))
print('all checks of page 14 hold')

check('the solution writes mu as about -3.911t', round(-2 * (1 + np.cos(0.3)), 3) == -3.911, round(-2 * (1 + np.cos(0.3)), 5))
