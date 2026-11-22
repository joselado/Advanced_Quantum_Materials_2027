"""Session 9, the numbers and the algebra that page 05b (Section 9.5b, the Stoner instability) states.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here or
in the figure script that draws it. The figures stoner.py and rpa_factor.py assert their captions when they are drawn,
and this script asserts the same numbers again from the same arrays, the helper _g3_chi0path.py of
webnotes/figures/session09, together with the three pictures of the quiz on (9.8), which _g3_chi0path.option() draws
from those arrays. The steps fold is checked on the four states of one site and by a second route, a self-consistent
Hartree loop of the Hubbard ring (1.7) in a small field, uniform and modulated, which gives the spin response
2 chi_0/(1 - U chi_0) with chi_0 per spin, as the sheet webnotes/conventions/session09.md says. The problem is checked
with the Lindhard function of the chain and with pyqula h.get_chi, run in a temporary folder. The lab box is checked
against its stored source. Nothing here writes a file in the tree.

Run it from anywhere:  python3 webnotes/checks/session09/g3_05b_stoner_instability.py"""
import os, sys, tempfile
sys.dont_write_bytecode = True
os.environ.setdefault('OMP_NUM_THREADS', '1')      # small matrices, one thread is faster than many
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WEBNOTES = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(WEBNOTES, 'figures', 'session09'))
import _g3_chi0path as cp


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


fermi = cp.fermi

# ---- the identity of the problem and of the fold, on the four states of one site
a = np.array([[0., 1.], [0., 0.]])
z, one = np.diag([1., -1.]), np.eye(2)
cu, cd = np.kron(a, one), np.kron(z, a)                       # Jordan-Wigner, c_up and c_dn
nu, nd = cu.T @ cu, cd.T @ cd
n, m = nu + nd, nu - nd
U = 1.7
check('U n_up n_dn = U/4 (n^2 - m^2) as an operator on the four states', np.allclose(U * nu @ nd, U / 4 * (n @ n - m @ m)),
      np.diag(U / 4 * (n @ n - m @ m)).tolist())
check('n_sigma^2 = n_sigma, and both sides are 0, 0, 0 and U on |0>, |up>, |dn>, |up dn>',
      np.allclose(nu @ nu, nu) and np.allclose(nd @ nd, nd) and sorted(np.diag(U * nu @ nd).tolist()) == [0, 0, 0, U],
      np.diag(U * nu @ nd).tolist())
# the mean field of the fold: -(U/4) m^2 -> -(U/2)<m> m + (U/4)<m>^2, and the two channels together are the Hartree term
for au, ad in ((0.3, 0.6), (0.55, 0.45)):
    mm, nn = au - ad, au + ad
    hartree = U * (ad * nu + au * nd - au * ad * np.eye(4))
    split = U / 4 * (2 * nn * n - nn ** 2 * np.eye(4)) - U / 4 * (2 * mm * m - mm ** 2 * np.eye(4))
    check('the mean field of U/4 n^2 - U/4 m^2 is the Hartree term, <n_up>=%.2f <n_dn>=%.2f' % (au, ad),
          np.allclose(hartree, split), np.diag(split).round(3).tolist())


# ---- the fold by a second route, a Hartree loop of the Hubbard ring in a small field
def ring_density(N, mu, T, onsite):
    H = np.diag(onsite).astype(float)
    i = np.arange(N)
    H[i, (i + 1) % N] = H[(i + 1) % N, i] = -1.0
    e, w = np.linalg.eigh(H)
    return (np.abs(w) ** 2) @ fermi(e - mu, T)


def hartree(N, mu, T, U, vup, vdn, ite=150):
    """The self-consistent Hartree densities of (1.7) with onsite energies vup and vdn, relative to the ring without
    them, at the fixed chemical potential mu. Spin up feels U n_dn and spin down feels U n_up."""
    n0 = ring_density(N, mu, T, np.zeros(N))
    du, dd = np.zeros(N), np.zeros(N)
    for _ in range(ite):
        du_new = ring_density(N, mu, T, U * dd + vup) - n0
        dd_new = ring_density(N, mu, T, U * du + vdn) - n0
        du, dd = 0.5 * du + 0.5 * du_new, 0.5 * dd + 0.5 * dd_new
    return du, dd


def chi0_ring(N, mu, T, iq):
    """chi_0 of (9.4) per spin on the k-mesh of the ring, for the band -2 cos k - mu, at q = 2 pi iq/N."""
    k = 2 * np.pi * np.arange(N) / N
    e1, e2 = -2 * np.cos(k) - mu, -2 * np.cos(k + 2 * np.pi * iq / N) - mu
    f1, f2 = fermi(e1, 1.0 * T), fermi(e2, T)
    d = e2 - e1
    s = np.abs(d) < 1e-12
    return float(np.mean(np.where(s, f1 * (1 - f1) / T, (f1 - f2) / np.where(s, 1.0, d))))


N, mu, T, h = 120, -1.0, 0.1, 1e-5
x = np.arange(N)
rows = []
for U_ in (0.0, 1.0, 3.0):
    for iq in (0, 20):
        c0 = chi0_ring(N, mu, T, iq)
        prof = np.cos(2 * np.pi * iq * x / N)
        du, dd = hartree(N, mu, T, U_, -h * prof, h * prof)          # the field -h (n_up - n_dn) cos(q r)
        mq = (2 if iq else 1) * np.mean((du - dd) * prof)
        heff = h + U_ * mq / 2
        rows.append((U_, iq, c0, mq / h, 2 * c0 / (1 - U_ * c0), mq / (2 * c0 * heff)))
ok = all(abs(r - f) < 1e-4 * f and abs(s - 1) < 1e-4 for U_, iq, c0, r, f, s in rows)
check('the fold: the Hartree ring gives <m> = 2 chi_0 (h + U<m>/2) = 2 chi_0 h/(1 - U chi_0), at q = 0 and q = 2pi/6', ok,
      ['U=%.0f q=2pi*%d/%d chi0=%.4f m/h=%.4f formula=%.4f' % (U_, iq, N, c0, r, f) for U_, iq, c0, r, f, s in rows])
check('the fold: without interaction a band moved down by h gains chi_0(0,0) h = D(E_F) h electrons per site',
      abs(rows[0][3] / 2 - rows[0][2]) < 1e-4 * rows[0][2], (rows[0][3] / 2, rows[0][2]))
du, dd = hartree(N, mu, T, 1.0, h * np.ones(N), h * np.ones(N))
c0 = chi0_ring(N, mu, T, 0)
dens = np.mean(du + dd) / h
check('the fold: the density channel gives the denominator 1 + U chi_0', abs(dens + 2 * c0 / (1 + c0)) < 1e-4 * c0,
      (dens, -2 * c0 / (1 + c0)))

# ---- the figure stoner and the first quiz, at T = 0.1t on the 240 x 240 mesh
pts, y, xt = cp.path(0.0, T=0.1, nk=240, step=8)
g0, gM = cp.elliptic(0.1)
check('stoner: chi_0 = 0.264/t at Gamma and 0.677/t at M, the same from the elliptic density of states',
      abs(y[0] - 0.264) < 1e-3 and abs(y[xt[2]] - 0.677) < 1e-3 and abs(y[0] - g0) < 1e-5 and abs(y[xt[2]] - gM) < 1e-5,
      (y[0], y[xt[2]], g0, gM))
check('stoner: the maximum of the path is at M = (pi, pi)', int(np.argmax(y)) == xt[2] and pts[xt[2]] == (120, 120),
      pts[int(np.argmax(y))])
check('stoner and quiz 1: 0.26/t and 0.68/t, the thresholds U = 1/chi_0 are 1.5t and 3.8t',
      round(y[0], 2) == 0.26 and round(y[xt[2]], 2) == 0.68 and round(1 / y[xt[2]], 1) == 1.5 and round(1 / y[0], 1) == 3.8
      and round(1 / 0.26, 1) == 3.8 and round(1 / 0.68, 1) == 1.5, (1 / y[xt[2]], 1 / y[0]))
check('quiz 1: at U = 1.5t the ferromagnetic channel gives 1.5 x 0.26 = 0.39', abs(1.5 * 0.26 - 0.39) < 1e-12, 1.5 * 0.26)
check('quiz 2: 1 + U chi_0 = 1.68 and 1 - U chi_0 = 0.32 at U = t and chi_0 = 0.68/t, and 1.5 x 0.68 > 1',
      abs(1 + 0.68 - 1.68) < 1e-12 and abs(1 - 0.68 - 0.32) < 1e-12 and 1.5 * y[xt[2]] > 1, 1.5 * y[xt[2]])
check('quiz 2, the feedback figure: the charge ratio 1/1.68 = 0.60 and the spin ratio 1/0.32 = 3.1',
      round(1 / 1.68, 2) == 0.60 and round(1 / 0.32, 1) == 3.1, (1 / 1.68, 1 / 0.32))

# ---- the picture quiz, from the arrays that the three pictures draw (step 4 on the 240 x 240 mesh, T = 0.1t)
P = {w: cp.path(cp.MU_QUIZ[w], step=4) for w in cp.MU_QUIZ}
ph, yh, th = P['half']
check('picture quiz, half filling: the maximum is at M with 0.68/t, against 0.26/t at Gamma, so U = 1.5t',
      cp.MU_QUIZ['half'] == 0.0 and int(np.argmax(yh)) == th[2] and round(yh[th[2]], 2) == 0.68 and round(yh[0], 2) == 0.26
      and round(1 / yh.max(), 1) == 1.5, (yh[th[2]], yh[0]))
pi_, yi, ti = P['incomm']
k = int(np.argmax(yi))
qy = pi_[k][1] / 120
check('picture quiz, mu = -t: the maximum is on the line from X to M at about (pi, 0.6 pi), with 0.25/t',
      cp.MU_QUIZ['incomm'] == -1.0 and ti[1] < k < ti[2] and pi_[k][0] == 120 and abs(qy - 0.6) < 0.05
      and round(yi[k], 2) == 0.25, (pi_[k], qy, yi[k]))
check('picture quiz, mu = -t: 0.16/t at M, and the threshold 1/0.25 is about 3.9t',
      round(yi[ti[2]], 2) == 0.16 and round(1 / yi[k], 1) == 3.9 and yi[ti[2]] < yi[k], (yi[ti[2]], 1 / yi[k]))
pl, yl, tl = P['low']
half_gx = [j for j, p in enumerate(pl) if p[1] == 0 and p[0] <= 60]        # Gamma to (pi/2, 0)
vals = yl[half_gx]
check('picture quiz, mu = -3t: between 0.09/t and 0.10/t on the first half from Gamma to X, 0.025/t at M',
      cp.MU_QUIZ['low'] == -3.0 and vals.min() > 0.09 and vals.max() < 0.10 and round(yl[tl[2]], 3) == 0.025,
      (vals.min(), vals.max(), yl[tl[2]]))
check('picture quiz, mu = -3t: the threshold 1/max is about 10t', 9.5 < 1 / yl.max() < 10.5, 1 / yl.max())
mg_near = [j for j in range(tl[2], tl[3] + 1) if pl[j][0] <= 36]            # the part of M-Gamma close to Gamma
check('picture quiz, mu = -3t, the alt text: flat near Gamma, lower at X and lowest at M',
      yl[tl[1]] < 0.6 * vals.min() and int(np.argmin(yl)) == tl[2] and yl[tl[2]] < yl[tl[1]]
      and yl[mg_near].min() > 0.09 and abs(yl[0] - yl[-1]) < 1e-12,
      (round(vals.min(), 4), round(yl[tl[1]], 4), round(yl[tl[2]], 4), round(yl[mg_near].min(), 4)))
kk = 2 * np.pi * np.arange(240) / 240
KX, KY = np.meshgrid(kk, kk, indexing='ij')
fill = float(np.mean(fermi(-2 * (np.cos(KX) + np.cos(KY)) + 3.0, 0.1)))
check('picture quiz, mu = -3t: a small Fermi surface around Gamma, above the band bottom -4t', fill < 0.1 and -3.0 > -4.0,
      fill)
check('picture quiz: the three curves fit the shared scale 0 to 0.75', all(P[w][1].max() < 0.75 for w in P),
      [round(P[w][1].max(), 3) for w in P])


def wedge_max(mu, step=4, T=0.1, nk=240):
    """The largest chi_0(q,0) over the wedge 0 <= qy <= qx <= pi of the same mesh, which the symmetry of the square
    makes the whole zone, so that a threshold read on the path is the threshold of the whole zone."""
    k = 2 * np.pi * np.arange(nk) / nk
    KX, KY = np.meshgrid(k, k, indexing='ij')
    e1 = -2 * (np.cos(KX) + np.cos(KY)) - mu
    f1 = fermi(e1, T)
    best = (0.0, None)
    for ix in range(0, nk // 2 + 1, step):
        for iy in range(0, ix + 1, step):
            e2 = np.roll(np.roll(e1, -ix, 0), -iy, 1)
            f2 = np.roll(np.roll(f1, -ix, 0), -iy, 1)
            d = e2 - e1
            s = np.abs(d) < 1e-9
            v = float(np.mean(np.where(s, f1 * (1 - f1) / T, (f1 - f2) / np.where(s, 1.0, d))))
            best = max(best, (v, (ix, iy)))
    return best


W = {w: wedge_max(cp.MU_QUIZ[w]) for w in cp.MU_QUIZ}
check('picture quiz: the maximum over the whole zone of q is the maximum of the path, for the three fillings',
      all(abs(W[w][0] - P[w][1].max()) < 1e-12 for w in W), {w: (round(W[w][0], 4), W[w][1]) for w in W})
g05 = cp.elliptic(0.05)[0]
check('stoner: chi_0(0,0) is the density of states averaged over the thermal window, 0.264/t at T=0.1t, 0.299/t at 0.05t',
      abs(g0 - 0.264) < 1e-3 and abs(g05 - 0.299) < 1e-3, (g0, g05))
# the condition after "logarithmically enhanced": chi_0(pi,pi) grows as ln^2(1/T), chi_0(0,0) as ln(1/T)
TL = (0.2, 0.1, 0.05, 0.025, 0.0125)
EL = [cp.elliptic(T_) for T_ in TL]
G0, GM = np.array([e[0] for e in EL]), np.array([e[1] for e in EL])
d2M, d1G, d2G = np.diff(GM, 2), np.diff(G0), np.diff(G0, 2)
check('the text: at half filling chi_0(pi,pi) grows as ln^2(1/T), second differences ln^2(2)/(2 pi^2) for each halving',
      np.all(np.abs(d2M - np.log(2) ** 2 / (2 * np.pi ** 2)) < 1e-4) and np.all(np.diff(GM) > 0),
      (np.round(GM, 4).tolist(), np.round(d2M, 5).tolist(), round(np.log(2) ** 2 / (2 * np.pi ** 2), 5)))
check('the text: chi_0(0,0) grows only as ln(1/T), by ln(2)/(2 pi^2) for each halving, with no second difference',
      np.all(np.abs(d1G - np.log(2) / (2 * np.pi ** 2)) < 3e-4) and np.all(np.abs(d2G) < 2e-4),
      (np.round(G0, 4).tolist(), np.round(d1G, 4).tolist(), round(np.log(2) / (2 * np.pi ** 2), 4)))


# ---- the problem: the half-filled chain
def lindhard_chain(Q, mu, T, nk=200000):
    k = 2 * np.pi * (np.arange(nk) + 0.5) / nk
    e1, e2 = -2 * np.cos(k) - mu, -2 * np.cos(k + Q) - mu
    d = e2 - e1
    s = np.abs(d) < 1e-10
    f1, f2 = fermi(e1, T), fermi(e2, T)
    return float(np.mean(np.where(s, f1 * (1 - f1) / T, (f1 - f2) / np.where(s, 1.0, d))))


D = lindhard_chain(1e-7, 0.0, 0.005)
check('problem: chi_0(0,0) = D(E_F) = 1/(2 pi t) = 0.159/t, so U = 2 pi t = 6.28t at q = 0',
      abs(D - 1 / (2 * np.pi)) < 1e-4 and round(2 * np.pi, 2) == 6.28, (D, 1 / D))
Ts = (0.02, 0.01, 0.005, 0.0025)
cpi = [lindhard_chain(np.pi, 0.0, T_) for T_ in Ts]
check('problem: chi_0 at q = pi is 0.86/t, 0.97/t and 1.08/t at T = 0.02t, 0.01t and 0.005t',
      [round(c, 2) for c in cpi[:3]] == [0.86, 0.97, 1.08], np.round(cpi, 4).tolist())
check('problem: the thresholds 1/chi_0(pi) are 1.16t, 1.03t and 0.92t',
      [round(1 / c, 2) for c in cpi[:3]] == [1.16, 1.03, 0.92], np.round([1 / c for c in cpi], 4).tolist())
slopes = np.diff(cpi) / np.log(2)
check('problem: chi_0 at q = pi grows as D(E_F) ln(1/T), the same step D(E_F) ln 2 for each halving of T',
      np.all(np.abs(slopes - 1 / (2 * np.pi)) < 2e-3), np.round(slopes, 4).tolist())
cwd = os.getcwd()
with tempfile.TemporaryDirectory() as d:
    os.chdir(d)
    try:
        from pyqula import geometry
        hc = geometry.chain().get_hamiltonian(has_spin=False)
        pq = -float(hc.get_chi(energies=[0.], q=[0.5, 0., 0.], nk=400, delta=1e-3, T=0.02)[1][0].real)
    finally:
        os.chdir(cwd)
check('problem: pyqula h.get_chi gives the same chi_0 at q = pi, 0.86/t at T = 0.02t, with the sign of dn/dv',
      abs(pq - cpi[0]) < 2e-3, (pq, cpi[0]))

# ---- the lab box against its stored source
src = open(os.path.join(WEBNOTES, 'sources', 'session09', 'sokolov2008_arxiv0807.3586.txt'), encoding='utf-8').read()
quotes = ['Neutron diffraction measurements on single crystals of Cr1-xVx (x=0, 0.02, 0.037) show that the ordering moment',
          'the ordering moment and the Neel temperature are continuously suppressed as x approaches 0.037, a proposed '
          'Quantum Critical Point (QCP)',
          'The wave vector Q of the spin density wave (SDW) becomes more incommensurate as x increases',
          'At xc=0.037 we have found temperature dependent, resolution limited elastic scattering at 4 incommensurate wave '
          'vectors Q=(1+/-delta_1,2, 0, 0)*2pi/a, which correspond to 2 SDWs with Neel temperatures of 19 K and 300 K.',
          'tuning Cr to its QCP results not in the suppression of antiferromagnetism, but instead enables new spin '
          'ordering due to novel nesting of the Fermi surface of Cr.', 'Neutron diffraction']
check('the lab box: the sentences are in the stored abstract', all(s in src for s in quotes), '0.037, 19 K, 300 K')
# ---- the try-it box and the notebook box: the second cell of "The charge-charge response function" of session9.ipynb,
# run as it is for U = 2.0 and U = 0.5, at the q of the cell closest to 0 and at 1/2, in units of the reciprocal vector of
# the cell of two sites. geometry.bichain() has equal hoppings, add_antiferromagnetism(0.5) is the starting guess of the
# mean-field loop, and the loop ends in an antiferromagnet. With RPA the low-energy peak near q = 0 is many times the
# one without RPA at U = 2.0, and the enhancement is much weaker at U = 0.5.
nb = os.path.join(os.path.dirname(WEBNOTES), 'jupyter-notebooks', 'session9.ipynb')
cell = ''.join(next(c['source'] for c in __import__('json').load(open(nb, encoding='utf-8'))['cells']
                    if c['cell_type'] == 'code' and 'get_spinchi_ladder' in ''.join(c['source'])))
check('try-it: the cell uses bichain, the starting guess add_antiferromagnetism(0.5), U = 2.0 and nk = 100',
      'geometry.bichain()' in cell and 'hmf.add_antiferromagnetism(0.5)' in cell and 'mf=hmf' in cell
      and 'U = 2.0 ; nk = 100' in cell, 'read from the cell')
res = {}
cwd = os.getcwd()
with tempfile.TemporaryDirectory() as d:
    os.chdir(d)
    try:
        from pyqula import geometry
        hops = geometry.bichain().get_hamiltonian(has_spin=False)
        hopping = [abs(hops.intra[0, 1])] + [abs(x.m[1, 0]) for x in hops.get_multicell().hopping if tuple(x.dir) == (1, 0, 0)]
        energies = np.linspace(0.0, 4.5, 100)
        for U in (2.0, 0.5):
            h = geometry.bichain().get_hamiltonian()
            hmf = h.copy(); hmf.add_antiferromagnetism(0.5)
            h = h.get_mean_field_hamiltonian(U=U, nk=100, mf=hmf, filling=0.5)
            k_, e_ = h.get_bands(nk=2001)                    # the default path of 1600 points misses the gap at small U
            row = {}
            for q in (1 / 59, 0.5):
                for rpa in (False, True):
                    e, c = h.get_spinchi_ladder(energies=energies, q=[q, 0., 0.], nk=100, imode="mesh", RPA=rpa)
                    im = np.array([np.trace(ci) for ci in c]).imag
                    row[(q, rpa)] = im[energies < 1.0].max()
            res[U] = (np.min(e_[e_ > 0]) - np.max(e_[e_ < 0]), row)
    finally:
        os.chdir(cwd)
check('try-it: geometry.bichain() has two sites in its cell and equal hoppings', np.allclose(hopping, 1.0), hopping)
g2, r2 = res[2.0]
g05, r05 = res[0.5]
check('try-it: at U = 2.0 the loop ends in an antiferromagnet with the gap 0.68t, and at U = 0.5 the gap is 0.008t',
      abs(g2 - 0.681) < 0.005 and abs(g05 - 0.0081) < 0.0005, (round(g2, 4), round(g05, 4)))
check('try-it: at U = 2.0 the low-energy weight near q = 0 is small without RPA and a strong peak with RPA',
      r2[(1 / 59, True)] > 10 * r2[(1 / 59, False)] and r2[(1 / 59, False)] < 1.0, (round(r2[(1 / 59, False)], 3), round(r2[(1 / 59, True)], 3)))
check('try-it: at U = 0.5 the enhancement near q = 0 is much weaker', r05[(1 / 59, True)] < 2 * r05[(1 / 59, False)],
      (round(r05[(1 / 59, False)], 3), round(r05[(1 / 59, True)], 3)))

# ---- the notebook box: at half filling the chain orders in mean field at any U > 0, since chi_0 at q = pi diverges as
# T -> 0 (the problem above), and at small U the gap is set by the k-mesh of the cell, nk = 100. Route 1, the loop of the
# cell at U = 0.5 with nk = 100, 200 and 400, and at U = 0.1 with nk = 100, the gap read on 2001 points of the bands.
# Route 2, the gap equation of the infinite chain, 1/U = K(1 - p)/(pi sqrt(4 + D^2)) with p = D^2/(4 + D^2) and the gap
# 2D, which is 16t exp(-2 pi t/U) at small U.
from scipy.special import ellipkm1
from scipy.optimize import brentq


def gap_infinite(U):
    f = lambda D: ellipkm1(D ** 2 / (4 + D ** 2)) / (np.pi * np.sqrt(4 + D ** 2)) - 1 / U
    return 2 * brentq(f, 1e-200, 5.0, xtol=1e-300, rtol=1e-13)


def gap_cell(U, nk):
    h = geometry.bichain().get_hamiltonian()
    hmf = h.copy(); hmf.add_antiferromagnetism(0.5)
    h = h.get_mean_field_hamiltonian(U=U, nk=nk, mf=hmf, filling=0.5)
    k_, e_ = h.get_bands(nk=2001)
    return np.min(e_[e_ > 0]) - np.max(e_[e_ < 0])


cwd = os.getcwd()
with tempfile.TemporaryDirectory() as d:
    os.chdir(d)
    try:
        from pyqula import geometry
        mesh = [gap_cell(0.5, nk) for nk in (100, 200, 400)]
        small = gap_cell(0.1, 100)
    finally:
        os.chdir(cwd)
inf = {U: gap_infinite(U) for U in (2.0, 0.5, 0.1)}
check('notebook box: the gap equation of the infinite chain gives 0.681t at U = 2t, and 16t exp(-2 pi t/U) at small U',
      abs(inf[2.0] - 0.6809) < 1e-3 and abs(inf[0.5] / (16 * np.exp(-4 * np.pi)) - 1) < 1e-3
      and abs(inf[0.1] / (16 * np.exp(-20 * np.pi)) - 1) < 1e-3, {U: '%.4e' % g_ for U, g_ in inf.items()})
check('notebook box: in mean field the half-filled chain orders at any U > 0, with a gap at U = 0.1t in the infinite chain '
      'and in the cell', inf[0.1] > 0 and small > 5e-4, ('%.2e' % inf[0.1], round(small, 5)))
check('notebook box: at U = 0.5t the gap of the cell is set by the mesh, it falls with nk = 100, 200 and 400 and stays far '
      'above the gap of the infinite chain', mesh[0] > mesh[1] > mesh[2] > 10 * inf[0.5] and abs(mesh[0] - g05) < 1e-4,
      (np.round(mesh, 5).tolist(), '%.2e' % inf[0.5]))
check('notebook box: at U = 2t the gap does not depend on the mesh, the cell and the infinite chain agree',
      abs(g2 - inf[2.0]) < 2e-3, (round(g2, 4), round(inf[2.0], 4)))
print('all checks of page 05b of Session 9 hold')
