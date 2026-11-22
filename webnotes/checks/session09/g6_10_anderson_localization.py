"""Session 9, the numbers and the statements of page 10 (Section 9.10a, disorder and Anderson localization). One check
script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here or in the
figure script that draws it. The asserts of a figure script do not run in `build.py --verify`, so the numbers of the
captions are asserted here again.

This script checks the fold on the self-dual point by the transformation itself, and that on a ring the two dual
spectra agree only up to a difference that falls with the size. It checks the caption of the mean IPR of the
Aubry-Andre rings (N*IPR about 2 at V0=t, the curves apart below 2t and on top of each other above it, pyqula equal
to numpy), the caption of Figure 9.6 by running the functions of its own Blender script, the feedback of the two
quizzes on the IPR, the picture quiz again from the pyqula script, the solution of the problem with its condition
on xi, and the try-it box of the notebook cell on quasicrystals with sqrt(2) and two other irrational numbers. It
needs numpy and pyqula, finds the repository from its own path and writes no file, since pyqula runs in a temporary
folder."""
import ast, os, runpy, tempfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, '..', '..', 'scripts')
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def run_script(rel):
    """The variables of a downloadable pyqula script, run in a temporary folder, as style.run_script does."""
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as d:
        os.chdir(d)
        try:
            return runpy.run_path(os.path.join(SCRIPTS, rel))
        finally:
            os.chdir(cwd)


def aah(N, q, V0, phi, t=1.0):
    """The Aubry-Andre ring of the page, hopping -t and the onsite energy V0 cos(2 pi q n + phi)."""
    H = np.diag(V0 * np.cos(2 * np.pi * q * np.arange(N) + phi)).astype(complex)
    i = np.arange(N)
    H[i, (i + 1) % N] = H[(i + 1) % N, i] = -t
    return H


ipr = lambda w: float((np.abs(w) ** 4).sum())

# ---- the fold: psi_n = sum_m exp(2 pi i q m n) a_m maps the chain (t, V0) onto the chain (V0/2, 2t)
N, p = 233, 144
q = p / N
n = np.arange(N)
U = np.exp(2j * np.pi * q * np.outer(n, n)) / np.sqrt(N)          # U[n, m] = exp(2 pi i q m n) / sqrt(N)
check('fold: U is unitary on the ring with q = 144/233', np.allclose(U.conj().T @ U, np.eye(N), atol=1e-10),
      np.abs(U.conj().T @ U - np.eye(N)).max())
t, V0 = 1.0, 3.0
for phi in (0.0, 0.3):
    D = np.diag(-2 * t * np.cos(2 * np.pi * q * n)).astype(complex)   # -2t cos(2 pi q m) on the diagonal
    D[(n + 1) % N, n] = V0 / 2 * np.exp(1j * phi)                    # (V0/2) e^{i phi} a_{m-1} in row m
    D[n, (n + 1) % N] = V0 / 2 * np.exp(-1j * phi)                   # (V0/2) e^{-i phi} a_{m+1} in row m
    err = np.abs(U.conj().T @ aah(N, q, V0, phi) @ U - D).max()
    check('fold: U^dag H U is (V0/2)(a_{m+1} + a_{m-1}) - 2t cos(2 pi q m) a_m, the hopping with the phase phi = %.1f'
          % phi, err < 1e-10, err)
# the two signs: (-1)^m changes the sign of the hopping on the infinite chain, and cos(x + pi) = -cos(x)
check('fold: cos(x + pi) = -cos(x), a phase pi in the potential', np.allclose(np.cos(n + np.pi), -np.cos(n)), 'ok')
# a state localized in n is extended in m, and the other way round. The lowest state is not degenerate, so its IPR
# does not depend on how the solver mixes the degenerate pairs of levels that the ring has below V0 = 2t.
for V0 in (1.0, 3.0):
    e, w = np.linalg.eigh(aah(N, q, V0, 0.3))
    g0 = w[:, np.argmin(e)]
    gap = np.sort(e)[1] - np.sort(e)[0]
    In, Im = ipr(g0), ipr(U.conj().T @ g0)
    if V0 == 3.0:
        ok = round(In, 2) == 0.83 and N * Im < 2.0
        what = 'localized in n (IPR 0.83) and extended in m (N*IPR below 2)'
    else:
        ok = N * In < 1.3 and Im > 0.85
        what = 'extended in n (N*IPR 1.2) and localized in m (IPR above 0.85)'
    check('fold: at V0 = %.0ft the lowest state, %.1e away from the next level, is %s' % (V0, gap, what),
          ok and gap > 1e-5, (round(In, 4), round(N * In, 2), round(Im, 4), round(N * Im, 2)))
# the levels of the chain at V0 = t are those of its dual, the chain in m with the hopping +1/2 and the potential -2t cos
eA = np.linalg.eigvalsh(aah(N, q, 1.0, 0.0))
Ddual = np.diag(-2 * np.cos(2 * np.pi * q * n)) + 0.5 * (np.eye(N, k=1) + np.eye(N, k=-1))
Ddual[0, -1] = Ddual[-1, 0] = 0.5
check('fold: the dual of V0 = t is a chain with the hopping 1/2 and the potential 2t, the same levels',
      np.allclose(eA, np.linalg.eigvalsh(Ddual), atol=1e-10), np.abs(eA - np.linalg.eigvalsh(Ddual)).max())
check('caption: 610/987 is close to (sqrt 5 - 1)/2', abs(610 / 987 - (np.sqrt(5) - 1) / 2) < 1e-5, 610 / 987)

# ---- the first quiz: equal weight on 10 sites
psi = np.zeros(10000); psi[:10] = 1 / np.sqrt(10)
check('quiz 1: ten equal sites give IPR 0.1', abs(ipr(psi) - 0.1) < 1e-12, ipr(psi))
check('quiz 1: the same on chains of 100 and 10^4 sites', abs(ipr(psi[:100]) - 0.1) < 1e-12, ipr(psi[:100]))
check('quiz 1: 1/N = 0.01 for N = 100, ten times less than 0.1', 1 / 100 == 0.01 and abs(0.1 / 0.01 - 10) < 1e-12, 0.01)
check('quiz 1: 10/N = 0.001 for N = 10^4', 10 / 1e4 == 0.001, 10 / 1e4)

# ---- the second quiz: a factor 0.7 when N doubles
tau = -np.log2(0.7)
check('quiz 2: 2^-tau = 0.7 gives tau about 0.5', round(tau, 1) == 0.5, tau)
check('quiz 2: tau = 1 gives 0.5 and tau = 0 gives 1', 2.0 ** -1 == 0.5 and 2.0 ** 0 == 1.0, 'ok')

# ---- the picture quiz: the lowest state of the rings of 55, 233 and 987 sites at V0 = t, 2t, 3t, from pyqula
d = run_script('session09/g6_aah_states.py')
I = d['ipr']
check('picture quiz: the lowest level is not degenerate', min(d['spacing'].values()) > 1e-6, min(d['spacing'].values()))
check('picture quiz: N*IPR = 1.20 at V0 = t on 55, 233, 987 sites',
      all(abs(N_ * I[(N_, 1.0)] - 1.20) < 0.01 for N_ in (55, 233, 987)), [round(N_ * I[(N_, 1.0)], 3) for N_ in (55, 233, 987)])
check('picture quiz: IPR 0.0052 on 233 and 0.0012 on 987 sites at V0 = t',
      round(I[(233, 1.0)], 4) == 0.0052 and round(I[(987, 1.0)], 4) == 0.0012, (I[(233, 1.0)], I[(987, 1.0)]))
check('picture quiz: IPR 0.83 on the three rings at V0 = 3t, 0.91 of the weight on one site',
      all(round(I[(N_, 3.0)], 2) == 0.83 for N_ in (55, 233, 987)) and round(float(d['weight'][(233, 3.0)].max()), 2) == 0.91,
      [round(I[(N_, 3.0)], 4) for N_ in (55, 233, 987)])
check('picture quiz: IPR 0.23, 0.099, 0.062 at V0 = 2t',
      (round(I[(55, 2.0)], 2), round(I[(233, 2.0)], 3), round(I[(987, 2.0)], 3)) == (0.23, 0.099, 0.062),
      [round(I[(N_, 2.0)], 4) for N_ in (55, 233, 987)])
check('picture quiz: from 233 to 987 sites 1/N falls to 0.24 and the IPR at 2t to 0.62',
      round(233 / 987, 2) == 0.24 and round(I[(987, 2.0)] / I[(233, 2.0)], 2) == 0.62, I[(987, 2.0)] / I[(233, 2.0)])

# ---- the problem: psi_n ~ exp(-|n|/xi) on an infinite chain
xi = 10.0
coth = lambda x: 1 / np.tanh(x)
m = np.arange(-2000, 2001)
s2 = np.exp(-2 * np.abs(m) / xi).sum()
s4 = np.exp(-4 * np.abs(m) / xi).sum()
check('problem: the sum of exp(-2|n|/xi) is coth(1/xi)', abs(s2 - coth(1 / xi)) < 1e-10, (s2, coth(1 / xi)))
check('problem: the sum of exp(-4|n|/xi) is coth(2/xi)', abs(s4 - coth(2 / xi)) < 1e-10, (s4, coth(2 / xi)))
check('problem: coth(0.2) = 5.066 and coth(0.1) = 10.033', round(coth(0.2), 3) == 5.066 and round(coth(0.1), 3) == 10.033,
      (coth(0.2), coth(0.1)))
val = coth(2 / xi) / coth(1 / xi) ** 2
check('problem: 5.066/10.033^2 = 0.0503', round(5.066 / 10.033 ** 2, 4) == 0.0503, 5.066 / 10.033 ** 2)
check('problem: the IPR is 0.0503 for xi = 10', round(val, 4) == 0.0503 and round(s4 / s2 ** 2, 4) == 0.0503, val)
check('problem: 1/(2 xi) = 0.05 for xi = 10, and the ratio to it tends to 1 for large xi',
      1 / (2 * xi) == 0.05 and abs(coth(2 / 1000.) / coth(1 / 1000.) ** 2 * 2000 - 1) < 1e-5, 'ok')
for Nc in (101, 1001):
    k = np.arange(Nc) - Nc // 2
    w2 = np.exp(-2 * np.abs(k) / xi); w2 /= w2.sum()
    check('problem: on a chain of %d sites the IPR is the same 0.0503' % Nc, round(float((w2 ** 2).sum()), 4) == 0.0503,
          (w2 ** 2).sum())

# ---- the fold, last sentence: on a ring the sign change (-1)^m and the removal of the phase phi leave a mismatch on the
# bond that closes the ring, so the levels at V0 are V0/2t times those at 4t^2/V0 only up to a small difference
diff = {}
for N_, p_ in ((233, 144), (987, 610)):
    eV = np.linalg.eigvalsh(aah(N_, p_ / N_, 3.0, 0.3))
    eD = 1.5 * np.linalg.eigvalsh(aah(N_, p_ / N_, 4 / 3., 0.3))
    diff[N_] = np.abs(eV - eD).max()
check('fold: at V0 = 3t and phi = 0.3 the levels are 3/2 times those at 4t/3 up to 0.015t on 233 and 0.0035t on 987 sites',
      round(diff[233], 3) == 0.015 and round(diff[987], 4) == 0.0035 and eV[-1] - eV[0] > 6.7, diff)
check('fold: the difference falls as the ring grows, and it is not zero', diff[987] < diff[233] / 3 and diff[987] > 1e-4, diff)

# ---- the caption of the mean IPR, the figure aah_ipr: the rings and the phase of the pyqula script g6_aah_ipr.py
src = open(os.path.join(SCRIPTS, 'session09', 'g6_aah_ipr.py')).read()
par = {}
for node in ast.parse(src).body:
    if isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', '') in ('sizes', 'qs', 'phi'):
        par[node.targets[0].id] = eval(compile(ast.Expression(node.value), 'g6_aah_ipr.py', 'eval'), {'__builtins__': {}})
check('caption: rings of 55, 233 and 987 sites, q = 610/987 for the largest, phi = 0.3, as in the pyqula script',
      par['sizes'] == [55, 233, 987] and par['qs'][2] == 610 / 987 and par['phi'] == 0.3, par)


def mean_ipr(N_, q_, V0):
    return float((np.abs(np.linalg.eigh(aah(N_, q_, V0, 0.3))[1]) ** 4).sum(axis=0).mean())


M = {V0: np.array([mean_ipr(N_, q_, V0) for N_, q_ in zip(par['sizes'], par['qs'])]) for V0 in (1.0, 1.9, 2.2, 2.5, 3.0, 4.0)}
NI = M[1.0] * np.array(par['sizes'])
check('caption: at V0 = t the product N*IPR is about 2 on the three rings', np.all((NI > 1.9) & (NI < 2.2)), np.round(NI, 3))
check('caption: below 2t the three curves are apart, the IPR falls with N at t and 1.9t',
      np.all(np.diff(M[1.0]) < 0) and np.all(np.diff(M[1.9]) < 0) and M[1.9][0] / M[1.9][2] > 10, (M[1.0], M[1.9]))
spread = {V0: float(np.ptp(M[V0]) / M[V0][2]) for V0 in (2.2, 2.5, 3.0, 4.0)}
check('caption: above 2t the three curves fall on top of each other, within 6% at 2.2t and 3% from 2.5t',
      spread[2.2] < 0.06 and all(spread[V0] < 0.03 for V0 in (2.5, 3.0, 4.0)), spread)
cwd = os.getcwd()
with tempfile.TemporaryDirectory() as dtmp:
    os.chdir(dtmp)
    try:
        from pyqula import geometry
        ring = geometry.chain().get_hamiltonian(has_spin=False, tij=[-1.]).set_finite_system(n=987, periodic=True)
        pq = {}
        for V0 in (1.0, 3.0):
            h = ring.copy()
            h.add_onsite(V0 * np.cos(2 * np.pi * (610 / 987) * np.arange(987) + 0.3))
            pq[V0] = float(np.mean(h.get_ipr()[1]))
    finally:
        os.chdir(cwd)
check('caption: computed with pyqula, h.get_ipr() gives the numpy mean IPR of the ring of 987 sites at t and 3t',
      abs(pq[1.0] / M[1.0][2] - 1) < 0.01 and abs(pq[3.0] / M[3.0][2] - 1) < 1e-8, (pq, M[1.0][2], M[3.0][2]))

# ---- the caption of Figure 9.6, from the functions of its Blender script, run without Blender
bsrc = open(os.path.join(REPO, 'lecture_notes', 'src', 'figures', 'blender', 's09f06_localization.py')).read()
btree = ast.parse(bsrc)
code = ['import math', 'import numpy as np']
nstates = None
for node in btree.body:
    if isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', '') in ('NS', 'Q'):
        code.append(ast.get_source_segment(bsrc, node))
    if isinstance(node, ast.FunctionDef) and node.name in ('chain', 'center_states', 'ipr'):
        code.append(ast.get_source_segment(bsrc, node))
    if isinstance(node, ast.FunctionDef) and node.name == 'build_states':
        seg = ast.get_source_segment(bsrc, node)
        for sub in ast.walk(node):
            if isinstance(sub, ast.Assign) and isinstance(sub.targets[0], ast.Tuple) and \
                    [getattr(e, 'id', '') for e in sub.targets[0].elts] == ['n', 'sp']:
                nstates = ast.literal_eval(sub.value)[0]
        bloch_flat = 'np.full(n, 1.0 / n)' in seg
fns = {}
exec('\n'.join(code), fns)
check('Figure 9.6: the three states are drawn on a chain of N = 89 sites', nstates == 89, nstates)
check('Figure 9.6: the IPR panel is computed for N = 34 to 610', fns['NS'][0] == 34 and fns['NS'][-1] == 610, fns['NS'])
pw = np.exp(2j * np.pi * 5 * np.arange(89) / 89) / np.sqrt(89)
check('Figure 9.6: the Bloch wave has weight exactly 1/N on every site, as the figure draws it',
      bloch_flat and np.allclose(np.abs(pw) ** 2, 1 / 89, atol=1e-15), 'np.full(n, 1/n)')
slopes = {}
for kind in ('bloch', 'aah', 'rand'):
    v = np.array([fns['ipr'](n_, kind) for n_ in fns['NS']])
    slopes[kind] = float(np.polyfit(np.log(fns['NS']), np.log(v), 1)[0])
check('Figure 9.6: IPR ~ 1/N for the extended states, slope -1.0', round(slopes['bloch'], 1) == -1.0, slopes['bloch'])
check('Figure 9.6: N^-tau with 0 < tau < 1 for the critical state', 0.3 < -slopes['aah'] < 0.9, -slopes['aah'])
check('Figure 9.6: IPR ~ O(1) for the localized states, a slope near 0', abs(slopes['rand']) < 0.15, slopes['rand'])
# the list of the three regimes: critical means neither extended nor localized, with an IPR that falls as a power of N
# slower than 1/N. The mean IPR over all states of the rings of 55, 233 and 987 sites at V0 = 2t, phi = 0.3, gives an
# exponent tau between 0 and 1, while V0 = t gives about 1 and V0 = 3t about 0. Second route, the lowest state alone.
fib = ((55, 34), (233, 144), (987, 610))
mean_ipr = {V0: [np.mean([ipr(w_) for w_ in np.linalg.eigh(aah(N_, p_ / N_, V0, 0.3))[1].T]) for N_, p_ in fib] for V0 in (1.0, 2.0, 3.0)}
low_ipr = [ipr(np.linalg.eigh(aah(N_, p_ / N_, 2.0, 0.3))[1][:, 0]) for N_, p_ in fib]
taus = {V0: -np.polyfit(np.log([f[0] for f in fib]), np.log(v_), 1)[0] for V0, v_ in mean_ipr.items()}
tau_low = -np.polyfit(np.log([f[0] for f in fib]), np.log(low_ipr), 1)[0]
check('list: at V0 = 2t the IPR falls as N^-tau with 0 < tau < 1, for the mean over the states and for the lowest state, '
      'while V0 = t gives tau near 1 and V0 = 3t near 0', 0.3 < taus[2.0] < 0.8 and 0.2 < tau_low < 0.8 and taus[1.0] > 0.9
      and taus[3.0] < 0.05, ({k_: round(v_, 3) for k_, v_ in taus.items()}, round(tau_low, 3)))

# ---- the solution of the problem, its condition: xi ~ 1/(2 IPR) holds for a pure exponential with xi much longer than
# one site, and a real localized state has more weight on its center than its tail suggests
for xi_, ref in ((10.0, 9.93), (2.5, 2.30), (1.0, 0.83)):
    ipr_ = coth(2 / xi_) / coth(1 / xi_) ** 2
    check('problem: 1/(2 IPR) of the pure exponential is %.2f for xi = %.1f' % (ref, xi_), round(1 / (2 * ipr_), 2) == ref,
          1 / (2 * ipr_))
e3, w3 = np.linalg.eigh(aah(233, 144 / 233, 3.0, 0.3))
g3 = w3[:, 0]
c3 = int(np.argmax(np.abs(g3)))
dist = np.minimum(np.abs(np.arange(233) - c3), 233 - np.abs(np.arange(233) - c3))
fits = []
windows = ((4, 30), (10, 40), (10, 60), (20, 60))
windows_reach = (min(w_[1] for w_ in windows), max(w_[1] for w_ in windows))
for lo, hi in windows:
    s_ = (dist >= lo) & (dist <= hi)
    fits.append(-1 / np.polyfit(dist[s_], np.log(np.abs(g3[s_])), 1)[0])
check('problem: the lowest state of the ring of 233 sites at V0 = 3t and phi = 0.3 has 1/(2 IPR) = 0.6 sites', round(1 / (2 * ipr(g3)), 1) == 0.6,
      1 / (2 * ipr(g3)))
check('problem: fits of its tail that reach 30 to 60 sites from the center give xi between 2.1 and 2.4 sites',
      round(min(fits), 1) == 2.1 and round(max(fits), 1) == 2.4 and windows_reach == (30, 60),
      np.round(fits, 3))
w0 = float(np.abs(g3[c3]) ** 2)
check('problem: its center has more weight than an exponential with that xi, 0.91 against tanh(1/xi), less than half of it',
      round(w0, 2) == 0.91 and np.tanh(1 / max(fits)) < w0 / 2, (w0, np.tanh(1 / max(fits))))

# ---- the try-it box, the notebook cell "Extended and localized states in quasicrystals": a chain of 400 sites with
# v cos(a pi x) and h.get_tails(), for a = sqrt(2) of the cell and two other irrational numbers
with tempfile.TemporaryDirectory() as dtmp:
    os.chdir(dtmp)
    try:
        gq = geometry.chain(400); gq.dimensionality = 0
        tails = {}
        for name, a in (('sqrt2', np.sqrt(2)), ('sqrt3', np.sqrt(3)), ('golden', np.sqrt(5) - 1)):
            row = []
            for v in (1.0, 1.8, 2.2, 3.0):
                h = gq.get_hamiltonian(has_spin=False)
                h.add_onsite(lambda r, v=v, a=a: v * np.cos(a * np.pi * r[0]))
                row.append(float(np.mean(h.get_tails()[1])))
            tails[name] = row
    finally:
        os.chdir(cwd)
for name, row in tails.items():
    check('try-it: with %s the mean 1/lambda stays close to zero up to v = 1.8 and grows fast above v = 2' % name,
          row[0] < 0.01 and row[1] < 0.02 and row[2] > 5 * row[1] and row[3] > 0.5, np.round(row, 4))
