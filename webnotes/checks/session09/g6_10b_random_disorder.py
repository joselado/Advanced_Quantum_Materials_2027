"""Session 9, the numbers of page 10b (Section 9.10b, random disorder and the special role of one dimension). One check
script per page is the rule: every number of a caption, a feedback or a solution is an assert, here or in the figure
script that draws it. The asserts of a figure script do not run in `build.py --verify`, so the numbers of the captions
are asserted here again.

The figure localization_length.py prints its numbers and asserts none, so this script runs the calculation of that
file itself, every statement before the plot, and asserts the slope -2.0, the 2x10^5 sites and the crossing of the
sample of 100 sites near W = 0.5t that its caption states. A change of the figure is then caught here. The figure
mobility.py asserts the band edges +-(6t + W), and they are asserted here again. The critical disorder W_c of about 8t
of its caption comes from the transfer matrix of MacKinnon and Kramer on bars of 4x4 and 6x6 sites, where the ratio
lambda_M/M grows with M on the extended side and falls on the localized side. A localization length of one
realization is not a number of the page, so the quizzes quote ranges over six realizations. The density of states of
the Anderson insulator at W = 20t comes from eight cubes of 10^3 sites. The conductance of the quiz is the transmission
of a chain between two clean leads, over 3000 realizations. The try-it box is the notebook cell on random disorder,
run with pyqula in a temporary folder. The disorder is w_n uniform in [-W, W], the hopping is -t with t = 1, and xi is
the length of the amplitude, |psi| ~ exp(-x/xi), as on the conventions sheet. The script finds the repository from its
own path and writes no file."""
import ast, os, sys, tempfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.abspath(os.path.join(HERE, '..', '..', 'figures'))


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# ---- the figure localization_length: every statement of figures/session09/localization_length.py before the plot
fsrc = open(os.path.join(FIGS, 'session09', 'localization_length.py')).read()
ftree = ast.parse(fsrc)
Lsamp = [ast.literal_eval(n_.value) for n_ in ftree.body
         if isinstance(n_, ast.Assign) and getattr(n_.targets[0], 'id', '') == 'Lsamp'][0]
body = []
for node in ftree.body:
    seg = ast.get_source_segment(fsrc, node)
    if isinstance(node, (ast.Import, ast.ImportFrom, ast.Expr)) and not seg.startswith('print'):
        continue                      # the imports, the docstring and sys.path
    if 'fig' in seg or 'plt' in seg or 'style' in seg:
        break                         # the plot starts here
    body.append(seg)
figvars = {'np': np, 'print': lambda *a: None}
exec('\n'.join(body), figvars)
check('caption: the transfer matrix of the figure has 2x10^5 sites, at E = 0, eight realizations',
      figvars['L'] == 200000 and figvars['E'] == 0.0 and figvars['ns'] == 8, (figvars['L'], figvars['E'], figvars['ns']))
xi_fig, Ws = figvars['xi'], figvars['Ws']
check('caption: the fitted slope at weak disorder is -2.0', round(figvars['slope'], 1) == -2.0, figvars['slope'])
check('law quiz: the fit of the figure runs from W = 0.25t to about t', abs(Ws[0] - 0.25) < 1e-12 and round(Ws[7], 1) == 1.1,
      Ws[:8])
cross = np.exp(np.interp(np.log(Lsamp), np.log(xi_fig[::-1]), np.log(Ws[::-1])))
check('caption: the red line is a sample of 100 sites, and xi passes it at W about 0.5t',
      Lsamp == 100 and abs(cross - 0.5) < 0.05 and xi_fig[3] > 100 > xi_fig[4], (Lsamp, round(cross, 3), np.round(xi_fig[3:5], 1)))


# ---- six realizations at W = 0.25t, 0.5t and t, a transfer matrix of 10^5 sites at the band center
def xi_seeds(Wlist, seeds, L=100000, E=0.0):
    """The localization length of the amplitude, one row per W and one column per seed."""
    Wr = np.repeat(np.asarray(Wlist, float), len(seeds))
    R = np.tile(np.array([np.random.default_rng(s).random(L) for s in seeds]), (len(Wlist), 1))
    p0 = np.ones_like(Wr); p1 = np.zeros_like(Wr); acc = np.zeros_like(Wr)
    for n in range(L):
        p0, p1 = (Wr * (2 * R[:, n] - 1) - E) * p0 - p1, p0
        if n % 50 == 49:
            s = np.hypot(p0, p1); acc += np.log(s); p0 /= s; p1 /= s
    return (L / acc).reshape(len(Wlist), len(seeds))


Wl = np.array([0.25, 0.5, 1.0])
xi = xi_seeds(Wl, range(1, 7))
xw = xi * Wl[:, None] ** 2
check('law quiz: xi W^2 between about 24 and 29 over six seeds and the three W', xw.min() > 23.5 and xw.max() < 29.0,
      (xw.min(), xw.max()))
check('law quiz: xi between about 24 and 26 sites at W = t', 23.5 < xi[2].min() < 24.5 and 25.5 < xi[2].max() < 26.5,
      np.round(xi[2], 1))
check('law quiz: xi between about 98 and 108 sites at W = 0.5t', 97.0 < xi[1].min() < 99.0 and 107.0 < xi[1].max() < 109.0,
      np.round(xi[1], 1))
check('law quiz: xi between about 380 and 460 sites at W = 0.25t', 375 < xi[0].min() < 385 and 455 < xi[0].max() < 465,
      np.round(xi[0], 1))
ratio = xi.mean(axis=1)
check('law quiz and halving quiz: the factor is about 4 for each halving of W',
      abs(ratio[1] / ratio[2] - 4) < 0.4 and abs(ratio[0] / ratio[1] - 4) < 0.4, (ratio[1] / ratio[2], ratio[0] / ratio[1]))
check('law quiz: e^2 = 7.4, the factor of the exponential law', round(np.exp(2), 1) == 7.4, np.exp(2))
check('law quiz: xi W^2 about 26, near 105/4 of perturbation theory at the band center', abs(xw.mean() - 26) < 0.5,
      (xw.mean(), 105 / 4))

# ---- the condition of the key box, close to the band center: at the band edge E = 2t the law is not (t/W)^2
check('key box: the clean chain has its band between -2t and 2t',
      np.allclose(np.linalg.eigvalsh(-(np.eye(400, k=1) + np.eye(400, k=-1)))[[0, -1]], [-2, 2], atol=1e-3), 'ok')
xe = xi_seeds([0.125, 0.25, 0.5], range(11, 15), L=50000, E=2.0).mean(axis=1)
sl_edge = np.polyfit(np.log([0.125, 0.25, 0.5]), np.log(xe), 1)[0]
check('key box: at the band edge E = 2t the slope of ln xi against ln W is about -2/3 and not -2', -0.8 < sl_edge < -0.5,
      (np.round(xe, 1), sl_edge))

# ---- the halving quiz now says close to the band center: at the band edge E = 2t halving W from 0.5t to 0.25t
# multiplies xi by about 1.6 and not by 4
check('halving quiz: at the band edge E = 2t halving W multiplies xi by about 1.6, so the factor 4 needs the band center',
      1.45 < xe[1] / xe[2] < 1.75 and 1.45 < xe[0] / xe[1] < 1.75, (round(xe[0] / xe[1], 3), round(xe[1] / xe[2], 3)))

# ---- the halving quiz
check('halving quiz: halving W multiplies (t/W)^2 by 4, 100 sites become 400', (1 / 0.25) ** 2 / (1 / 0.5) ** 2 == 4 and 100 * 4 == 400,
      'ok')
check('halving quiz: a chain of 20 sites is shorter than xi = 100 sites', 20 < 100, 'ok')

# ---- the Anderson insulator quiz: the 3D Anderson model at W = 20t, eight cubes of 10^3 sites
def cube(Lc):
    idx = np.arange(Lc ** 3).reshape(Lc, Lc, Lc)
    H = np.zeros((Lc ** 3, Lc ** 3))
    for axis in range(3):
        j = np.roll(idx, -1, axis=axis).ravel()
        H[idx.ravel(), j] = H[j, idx.ravel()] = -1.0
    return H


Lc, Wa, window, ncubes = 10, 20.0, 5.0, 8
H0 = cube(Lc)
dos, edges = [], []
for s in range(1, ncubes + 1):
    e = np.linalg.eigvalsh(H0 + np.diag(Wa * (2 * np.random.default_rng(s).random(Lc ** 3) - 1)))
    dos.append(np.sum(np.abs(e) < window) / (Lc ** 3 * 2 * window))
    edges.append(np.abs(e).max())
dos = np.array(dos)
check('Anderson quiz: 1/(2W) = 0.025 at W = 20t', 1 / (2 * Wa) == 0.025, 1 / (2 * Wa))
check('Anderson quiz: eight cubes of 10^3 sites and the window |E| < 5t', ncubes == 8 and Lc ** 3 == 1000 and window == 5.0, 'ok')
check('Anderson quiz: the density of states in |E| < 5t is between about 0.022 and 0.027 per site and per t',
      dos.min() >= 0.0215 and dos.max() < 0.0275, np.round(dos, 4))
check('Anderson quiz: its mean over the cubes is 0.025 to 2 percent', abs(dos.mean() / 0.025 - 1) < 0.02, dos.mean())
check('Anderson quiz: every level lies inside +-(6t + W)', max(edges) < 6 + Wa, max(edges))


# the typical conductance of a chain of L sites between clean leads at E = 0, T = 4|G_1L|^2 with the self-energy -i
# of each lead. It falls as e^{-L/xi} for the xi of |psi|^2, and as e^{-2L/xi} for the xi of the amplitude.
def lnT(L, W, nr, rng):
    a = -W * (2 * rng.random((nr, L)) - 1) + 0j
    a[:, 0] += 1j; a[:, -1] += 1j
    th2 = np.ones(nr, complex); th1 = a[:, 0].copy(); lg = np.zeros(nr)
    for k in range(1, L):
        th = a[:, k] * th1 - th2
        s = np.abs(th); th2 = th1 / s; th1 = th / s; lg += np.log(s)
    return np.log(4) - 2 * (lg + np.log(np.abs(th1)))


rngT = np.random.default_rng(5)
check('Anderson quiz: a clean chain between the leads has T = 1', np.allclose(np.exp(lnT(50, 0.0, 2, rngT)), 1), 'ok')
lT = {L: lnT(L, 1.0, 3000, rngT).mean() for L in (200, 400)}
rate = -(lT[400] - lT[200]) / 200
check('Anderson quiz: at W = t the typical conductance falls at the rate 2/xi per site for the xi of the amplitude',
      abs(rate * ratio[2] / 2 - 1) < 0.1, (lT, rate, 2 / ratio[2]))

# ---- the caption of mobility: the band edges +-(6t + W), and W_c about 8t
check('mobility: the clean cubic band is between -6t and 6t', np.allclose(np.linalg.eigvalsh(cube(8))[[0, -1]], [-6, 6]), 'ok')
H8, rng8 = cube(8), np.random.default_rng(3)
for Wt in (2.0, 6.0, 12.0):
    e = np.linalg.eigvalsh(H8 + np.diag(Wt * (2 * rng8.random(8 ** 3) - 1)))
    check('mobility: every level of a cube of 8^3 sites at W = %.0ft lies inside +-(6t + W)' % Wt, np.all(np.abs(e) < 6 + Wt),
          (e[0], e[-1]))


def mk_lambda(M, W, L, seed, E=0.0, k=8):
    """MacKinnon-Kramer localization length lambda_M of a bar of M x M sites, periodic in the two transverse
    directions, from the smallest positive Lyapunov exponent of the transfer matrix."""
    n = M * M
    idx = np.arange(n).reshape(M, M)
    Ht = np.zeros((n, n))
    for ax in range(2):
        j = np.roll(idx, -1, axis=ax).ravel()
        Ht[idx.ravel(), j] -= 1.0; Ht[j, idx.ravel()] -= 1.0
    rng = np.random.default_rng(seed)
    A, B, acc = np.eye(n), np.zeros((n, n)), np.zeros(n)
    for s in range(L):
        Hn = Ht.copy(); Hn[np.diag_indices(n)] += W * (2 * rng.random(n) - 1) - E
        A, B = Hn @ A - B, A
        if s % k == k - 1:
            Q, R = np.linalg.qr(np.vstack([A, B]))
            d = np.diag(R); acc += np.log(np.abs(d))
            Q = Q * np.sign(d); A, B = Q[:n], Q[n:]
    return L / np.min(acc)


# the caption of mobility: the height of the guide at W = 5t. The ratio r of neighboring level spacings of cubes of
# 10^3 sites (8 seeds) and 12^3 sites (4 seeds), periodic, is that of extended states, close to the 0.53 of the GOE and
# far from the 0.386 of localized states, for 5t < |E| < 6t and 6t < |E| < 7t at W = 5t. So extended states reach E = 7t
# there, below the guide of webnotes/figures/session09/mobility.py. The window 7t < |E| < 8t gives 0.51 to 0.53 with about
# 200 levels, close to the edge, and it is not asserted.
def r_ratio(L, W, win, seeds):
    rs = []
    for sd in seeds:
        n = L ** 3
        idx = np.arange(n).reshape(L, L, L)
        H = np.zeros((n, n))
        for ax in range(3):
            j = np.roll(idx, -1, axis=ax).ravel()
            H[idx.ravel(), j] = H[j, idx.ravel()] = -1.0
        H[np.diag_indices(n)] = W * (2 * np.random.default_rng(sd).random(n) - 1)
        e = np.linalg.eigvalsh(H)
        dd = np.diff(e); r = np.minimum(dd[1:], dd[:-1]) / np.maximum(dd[1:], dd[:-1])
        em = np.abs(e[1:-1])
        rs.append(r[(em > win[0]) & (em < win[1])])
    return float(np.concatenate(rs).mean())


rr = {(L, win): r_ratio(L, 5.0, win, seeds) for L, seeds in ((10, range(100, 108)), (12, range(200, 204))) for win in ((5, 6), (6, 7))}
check('mobility caption: at W = 5t the level statistics of cubes of 10^3 and 12^3 sites are those of extended states up to E = 7t',
      all(v_ > 0.50 for v_ in rr.values()), {k_: round(v_, 3) for k_, v_ in rr.items()})

Lam = {(M, W): mk_lambda(M, W, 30000, 1) / M for M in (4, 6) for W in (7.0, 9.5)}
check('mobility: at W = 7t the ratio lambda_M/M grows from bars of 4x4 to 6x6 sites, extended', Lam[(6, 7.0)] > Lam[(4, 7.0)] * 1.02,
      (Lam[(4, 7.0)], Lam[(6, 7.0)]))
check('mobility: at W = 9.5t it falls, localized', Lam[(6, 9.5)] < Lam[(4, 9.5)] / 1.02, (Lam[(4, 9.5)], Lam[(6, 9.5)]))
d7, d95 = np.log(Lam[(6, 7.0)] / Lam[(4, 7.0)]), np.log(Lam[(6, 9.5)] / Lam[(4, 9.5)])
Wc = 7.0 + 2.5 * d7 / (d7 - d95)
check('mobility: the two sizes cross at W_c about 8t, so a box of full width 2W_c of about 16t', 7.5 < Wc < 9.0, Wc)

# ---- the problem
C = 100 * 0.5 ** 2
check('problem: xi W^2 = 25 t^2 for xi = 100 at W = 0.5t', C == 25, C)
check('problem: xi = 400 sites at W = 0.25t', C / 0.25 ** 2 == 400, C / 0.25 ** 2)
Wn = np.sqrt(C / 1000)
check('problem: xi = 1000 sites at W = 0.158t, about 0.16t, which is 0.5t/sqrt(10)',
      round(Wn, 3) == 0.158 and round(Wn, 2) == 0.16 and abs(Wn - 0.5 / np.sqrt(10)) < 1e-12, Wn)
check('problem: the transfer matrix gives xi W^2 about 26, close to 25', round(xw.mean()) == 26, xw.mean())

# ---- the recall box: an extended state has an IPR that falls as 1/N, a plane wave exactly 1/N
Nr = 400
pw = np.exp(1j * 2 * np.pi * 7 * np.arange(Nr) / Nr) / np.sqrt(Nr)
check('recall: a plane wave on N sites has IPR 1/N', abs((np.abs(pw) ** 4).sum() * Nr - 1) < 1e-12, (np.abs(pw) ** 4).sum() * Nr)

# ---- the try-it box, the notebook cell "Localization due to random disorder": a chain of 400 sites with
# v*(random - 0.5) and h.get_tails(), against the quasiperiodic cell with v cos(sqrt(2) pi x)
cwd = os.getcwd()
with tempfile.TemporaryDirectory() as dtmp:
    os.chdir(dtmp)
    try:
        from pyqula import geometry
        g = geometry.chain(400); g.dimensionality = 0

        def tails(f):
            h = g.get_hamiltonian(has_spin=False)
            h.add_onsite(f)
            return float(np.mean(h.get_tails()[1]))

        rnd = {}
        for v in (0.25, 0.5, 1.0, 2.0, 4.0):
            row = []
            for s in (range(1, 7) if v == 0.5 else (1,)):
                np.random.seed(s)
                row.append(tails(lambda r, v=v: v * (np.random.random() - 0.5)))
            rnd[v] = row
        qp = {v: tails(lambda r, v=v: v * np.cos(np.sqrt(2) * np.pi * r[0])) for v in (0.5, 1.8, 3.0)}
    finally:
        os.chdir(cwd)
check('try-it: the random cell gives a mean 1/lambda of 0.04 to 0.06 at v = 0.5 over six seeds, already finite',
      min(rnd[0.5]) > 0.04 and max(rnd[0.5]) < 0.06 and min(rnd[0.5]) > 20 * qp[0.5], (np.round(rnd[0.5], 4), qp[0.5]))
mono = [rnd[0.25][0], rnd[0.5][0], rnd[1.0][0], rnd[2.0][0], rnd[4.0][0]]
check('try-it: it grows smoothly with v, with no threshold', mono[0] > 0.01 and np.all(np.diff(mono) > 0), np.round(mono, 4))
check('try-it: the quasiperiodic cell stays near zero up to v = 2', qp[0.5] < 0.005 and qp[1.8] < 0.02 and qp[3.0] > 0.5, qp)
# ---- the notebook box: the cells draw the random potential as v*(np.random.random()-0.5) and w*(np.random.random()-0.5),
# uniform in [-v/2, v/2], so their full width v is 2W of the page, with w_n uniform in [-W, W]
import json as _json
_cells = _json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
                                      'jupyter-notebooks', 'session9.ipynb'), encoding='utf-8'))['cells']
_src = [''.join(c['source']) for c in _cells if c['cell_type'] == 'code']
_v = np.random.default_rng(9).random(200000) - 0.5
check('notebook box: the cells write the random potential with the full width v or w, which is 2W of the page',
      any('v*(np.random.random()-0.5)' in x for x in _src) and any('w*(np.random.random()-0.5)' in x for x in _src)
      and abs(_v.min() + 0.5) < 1e-3 and abs(_v.max() - 0.5) < 1e-3, 'uniform in [-v/2, v/2]')

