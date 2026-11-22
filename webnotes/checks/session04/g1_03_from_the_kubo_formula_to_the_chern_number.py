"""Session 4, the numbers and statements that page 03 (Sections 4.3 and 4.4) gives in the caption of landau_chern,
the quizzes and the problem. The figure scripts landau_chern.py and _g1_staircase.py assert what they draw, and the
numbers that their captions and feedback quote are computed again here, by a second route where there is one, so
that build.py --verify sees them.

The model is the one of webnotes/scripts/session04/g1_landau_levels_square.py: the square lattice with tij=[-1.] in
the magnetic cell geometry.square_lattice().get_supercell((1, q)) and h.add_orbital_magnetic_field(1/q). The Chern
numbers come from h.get_chern() and from the link variables of webnotes/figures/physcheck.py, which has the Omega of
the notes. Both give +1 per band for this sign of the field of pyqula. The caption says that this positive flux is the
field along +z for an electron and along -z for the charge +e, from the plaquette phase computed below, and that the
flux -1/20 gives -1. The opener and the problem give magnitudes only, since the conventions sheet leaves the sign of
(4.2) to the lecturer. The first quiz counts the chiral modes at an edge of a ribbon, and the Streda form is a
second route to the Chern number of the third gap, by the count of the states at a fixed Fermi energy.

pyqula writes files when it computes a Chern number, so the script works in a temporary folder and leaves no file.
It needs numpy and pyqula, and takes about half a minute."""
import os, sys, tempfile
import numpy as np

WEBNOTES = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(WEBNOTES, 'figures'))
import physcheck as pc
from pyqula import geometry

H, E = 6.62607015e-34, 1.602176634e-19


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def cell(q):
    g = geometry.square_lattice().get_supercell((1, q))
    h = g.get_hamiltonian(has_spin=False, tij=[-1.])
    h.add_orbital_magnetic_field(1 / q)
    return h


TMP = tempfile.TemporaryDirectory(prefix='g1_03_')     # removed at the end, with what pyqula wrote in it
os.chdir(TMP.name)

# ---------------------------------------------------------------- the caption of landau_chern, flux 1/20
q = 20
h = cell(q)
intra = np.array(h.intra)
phases = {tuple(t.dir): np.array(t.m) for t in h.hopping}
along_y = [phases[(0, 1, 0)], phases[(0, -1, 0)]]
along_x = phases[(1, 0, 0)]
check('the vector potential of pyqula is along x: the bonds along y are real, those along x carry phases',
      np.abs(intra.imag).max() < 1e-12 and max(np.abs(m.imag).max() for m in along_y) < 1e-12
      and np.ptp(np.angle(along_x[np.abs(along_x) > 0.5])) > 1, round(float(np.ptp(np.angle(along_x[np.abs(along_x) > 0.5]))), 3))
check('the band of no field starts at -4t with tij=[-1.]',
      abs(np.linalg.eigvalsh(np.array(geometry.square_lattice().get_hamiltonian(has_spin=False, tij=[-1.]).get_hk_gen()([0., 0., 0.]))).min() + 4) < 1e-12,
      -4)
hk, B = pc.from_pyqula(h)
ens = np.array([np.linalg.eigvalsh(hk(k)) for k in pc.kmesh(B, 12)])
lev = ens.mean(axis=0)
wc = 4 * np.pi / q
cont = -4 + wc * (np.arange(4) + 0.5)
check('the four lowest bands are flat over the whole magnetic zone', np.ptp(ens[:, :4], axis=0).max() < 2e-5,
      np.ptp(ens[:, :4], axis=0).max())
check('hbar omega_c = 4 pi t / 20 = 0.63 t', round(wc, 2) == 0.63, round(wc, 4))
sh = cont - lev[:4]
check('the bands sit below the dashed lines, by 0.01 t for the lowest and 0.30 t, about half a spacing, for the fourth',
      np.all(sh > 0) and round(sh[0], 2) == 0.01 and round(sh[3], 2) == 0.30 and abs(sh[3] / wc - 0.47) < 0.005,
      np.round(sh, 3))
Cl = [pc.chern_links(hk, B, bands=n, nk=24) for n in range(4)]
check('each of the four bands has C = 1 with the link variables and the Omega of the notes', np.allclose(Cl, 1, atol=1e-9),
      np.round(Cl, 6))
sig = []
for n in range(4):
    hf = h.copy()
    hf.add_onsite(-(lev[n] + lev[n + 1]) / 2)
    sig.append(hf.get_chern(nk=20))
check('h.get_chern() in the four gaps gives 1, 2, 3, 4, one more at each band', np.allclose(sig, [1, 2, 3, 4], atol=1e-6),
      np.round(sig, 6))


# the sign of the field of pyqula, for the sentence of the caption: the product of the amplitudes <i_{n+1}|H|i_n>
# around a plaquette, counterclockwise, with H(k) = sum_R m(R) exp(2 pi i k.R) and m(R)[i, j] = <i, 0|H|j, R>.
# The phase (4.4) of the charge +e in the field along +z gives +2 pi phi (conventions sheet), pyqula gives -2 pi phi
g20 = geometry.square_lattice().get_supercell((1, q))
mats = {(0, 0): intra}
mats.update({tuple(int(x) for x in t.dir[:2]): np.array(t.m) for t in h.hopping})
kt = np.array([0.13, 0.27, 0.])
check('the Bloch form of pyqula is H(k) = sum_R m(R) exp(2 pi i k.R)',
      np.allclose(sum(m * np.exp(2j * np.pi * (kt[0] * d[0] + kt[1] * d[1])) for d, m in mats.items()), np.array(h.get_hk_gen()(kt))),
      'ok')
rr = np.array(g20.r)[:, :2]
A1, A2 = np.array(g20.a1)[:2], np.array(g20.a2)[:2]


def locate(p):
    for nx in range(-2, 3):
        for ny in range(-2, 3):
            d = np.linalg.norm(rr - (p - nx * A1 - ny * A2), axis=1)
            if d.min() < 1e-6:
                return (nx, ny), int(np.argmin(d))


def amp(pb, pa):
    (cb, ib), (ca, ia) = locate(pb), locate(pa)
    return mats.get((ca[0] - cb[0], ca[1] - cb[1]), np.zeros_like(intra))[ib, ia]


ploop = []
for y0 in rr[:, 1]:                                   # every plaquette of the cell, the last one across its boundary
    pts = [np.array([0., y0]), np.array([1., y0]), np.array([1., y0 + 1]), np.array([0., y0 + 1])]
    ploop.append(np.prod([amp(pts[(n + 1) % 4], pts[n]) for n in range(4)]))
ploop = np.angle(ploop) / (2 * np.pi)
check('every counterclockwise plaquette of pyqula has the phase -2 pi/20, the field along -z for the charge +e',
      len(ploop) == q and np.allclose(ploop, -1 / q, atol=1e-9), (round(ploop.min(), 6), round(ploop.max(), 6)))
hm = geometry.square_lattice().get_supercell((1, q)).get_hamiltonian(has_spin=False, tij=[-1.])
hm.add_orbital_magnetic_field(-1 / q)
hkm, Bm = pc.from_pyqula(hm)
Cm = [pc.chern_links(hkm, Bm, bands=n, nk=12) for n in range(4)]
check('the flux -1/20, the field along +z for the charge +e, gives C = -1 for each band', np.allclose(Cm, -1, atol=1e-9),
      np.round(Cm, 6))

# a second route, the count of the states (the Streda form sigma_xy = e dn/dB): at a fixed Fermi energy in the third
# gap of both fluxes 1/20 and 1/21, the number of states below it on a k-mesh, per site, changes with the flux as 3
EF = -2.35
dens = {}
for qq in (20, 21):
    hq, Bq = pc.from_pyqula(cell(qq))
    eq = np.array([np.linalg.eigvalsh(hq(k)) for k in pc.kmesh(Bq, 6)])
    lq = eq.mean(axis=0)
    assert lq[2] < EF < lq[3] and np.ptp(eq[:, :4], axis=0).max() < 1e-4   # E_F is in the third gap of both
    dens[qq] = np.sum(eq < EF) / eq.size
dndphi = (dens[20] - dens[21]) / (1 / 20 - 1 / 21)
check('the density below E_F = -2.35 t changes as dn/dphi = 3 per site, the Chern number of the third gap',
      abs(dndphi - sig[2]) < 1e-9, (dens[20], round(dens[21], 6), round(dndphi, 9)))
check('the second quiz: three filled levels give 3 in units of e^2/h', abs(sig[2] - 3) < 1e-6, round(sig[2], 6))

# the first quiz: the number of chiral modes at one edge is the |C| of all the filled bands, while each band has 1.
# A ribbon of 80 sites, periodic along x as the ribbons of pyqula are, with the Fermi energy in the gaps 1, 2 and 3
gr = geometry.square_ribbon(80)
hr = gr.get_hamiltonian(has_spin=False, tij=[-1.])
hr.add_orbital_magnetic_field(1 / q)
hkr, yr = hr.get_hk_gen(), np.array(gr.r)[:, 1]
Er, Pr = [], []
for kk in np.linspace(-0.5, 0.5, 401):
    e, v = np.linalg.eigh(np.array(hkr([kk, 0., 0.])))
    Er.append(e); Pr.append((np.abs(v) ** 2 * yr[:, None]).sum(axis=0))
Er, Pr = np.array(Er), np.array(Pr)
modes = []
for N in (1, 2, 3):
    s = np.sign(Er - (lev[N - 1] + lev[N]) / 2)
    cross = s[1:] != s[:-1]
    assert np.all(np.abs(Pr[:-1][cross]) > 25)                # each crossing state sits at an edge of the ribbon
    modes.append((int(np.sum(cross & (Pr[:-1] > 0))), int(np.sum(cross & (Pr[:-1] < 0)))))
check('quiz 1, 1, 2 and 3 chiral modes at each edge with 1, 2 and 3 filled levels, each of |C| = 1',
      modes == [(1, 1), (2, 2), (3, 3)] and np.allclose(sig[:3], [1, 2, 3], atol=1e-6), modes)

# ---------------------------------------------------------------- the picture quiz, fluxes 1/10, 1/20, 1/40
step = {}
for qq in (10, 20, 40):
    hh = cell(qq)
    hkq, Bq = pc.from_pyqula(hh)
    eq = np.array([np.linalg.eigvalsh(hkq(k)) for k in pc.kmesh(Bq, 8)]).mean(axis=0)
    step[qq] = eq[1] - eq[0]                          # the plateau at sigma_xy = e^2/h, between the first two levels
check('the plateaus at sigma_xy = e^2/h are 1.07, 0.58 and 0.30 t wide, the widest for the strongest field',
      [round(step[qq], 2) for qq in (10, 20, 40)] == [1.07, 0.58, 0.30] and step[10] > step[20] > step[40], step)
check('the continuum gives 4 pi t / 10 = 1.26 t, and the lattice plateau is narrower',
      round(4 * np.pi / 10, 2) == 1.26 and step[10] < 4 * np.pi / 10, round(4 * np.pi / 10, 4))
# the question: hbar e B / m with the band mass m = hbar^2 / 2 t a^2 of the band bottom -4t + t a^2 k^2 is 4 pi phi t,
# with the flux phi = e B a^2 / h per plaquette in flux quanta, for any lattice constant, field and hopping
HB = H / (2 * np.pi)
ok = True
for a, Bf, t in ((3e-10, 1.0, 0.1 * E), (5e-9, 7.0, 0.002 * E), (1e-8, 0.3, 0.01 * E)):
    k = 0.01 / a                                      # a momentum close to the band bottom, k a = 0.01
    m = HB ** 2 / (2 * t * a ** 2)
    above_bottom = -2 * t * (np.cos(k * a) + np.cos(0.)) + 4 * t       # the band along k_x, measured from -4t
    ok &= abs(above_bottom / (HB ** 2 * k ** 2 / (2 * m)) - 1) < 1e-4
    ok &= abs(HB * E * Bf / m / (4 * np.pi * (E * Bf * a ** 2 / H) * t) - 1) < 1e-12
check('the question: hbar e B / m with m = hbar^2/2ta^2 is 4 pi phi t, with phi = e B a^2/h', ok, 'three lattices')

# ---------------------------------------------------------------- the problem, a circle of radius R in a large sample,
# magnitudes only
N, R, dBdt, Bfield = 3, 1e-6, 0.7, 5.0
sxy = N * E ** 2 / H
Ephi = R / 2 * dBdt                                   # Faraday, 2 pi R E = pi R^2 dB/dt
rate_hall = 2 * np.pi * R * sxy * Ephi                # the Hall current across the circle
dn = (N * E * (Bfield + 1e-3) / H - N * E * Bfield / H) / 1e-3   # dn/dB by a difference, n = N e B / h
rate_count = E * dn * np.pi * R ** 2 * dBdt           # what the filled levels need
check('problem, the Hall current and the count of states give the same rate for |sigma_xy| = N e^2/h',
      abs(rate_hall / rate_count - 1) < 1e-9 and abs(E * dn / sxy - 1) < 1e-9, (rate_hall, rate_count))
check('problem, h/3e^2 = 8.60 kOhm', round(H / (3 * E ** 2) / 1e3, 2) == 8.60, round(H / (3 * E ** 2), 2))
os.chdir(WEBNOTES)
TMP.cleanup()
print('all checks of page 03 hold')
