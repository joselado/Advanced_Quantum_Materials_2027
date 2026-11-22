"""Session 10, the numbers and formulas that page 07 (Section 10.7) quotes, in the steps fold, the quizzes, the problem
and the captions of ham_learning and dos_sign.

The toy of ham_learning is imported from figures/session10/_g5_hlquiz.py, the module that the figure and the three
picture options draw from, and it is run here for the seeds 0 to 9, since the new quiz quotes ranges over ten random
draws of the rings. The seed 3 of the figure is asserted in its figure script too. The pyqula scripts run through
style.run_script, in a temporary folder, so this script writes no file. About 70 s on a free machine."""
import os
import sys
import time

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures', 'session10'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures'))
import _g5_hlquiz as toy  # noqa: E402
import style  # noqa: E402


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def band(k, t, t2):
    return -2 * t * np.cos(k) - 2 * t2 * np.cos(2 * k)


# --- the steps fold: the squared loss and the average of the labels ---------------------------------------------
rng = np.random.default_rng(7)
la, lb = rng.normal(size=2)
yy = np.linspace(-4, 4, 800001)
two = (yy - la) ** 2 + (yy - lb) ** 2
check('two labels, 2(y-la)+2(y-lb)=0 at the average, and the loss is not zero there',
      abs(yy[np.argmin(two)] - (la + lb) / 2) < 2e-5 and two.min() > 0, (round(yy[np.argmin(two)], 5), round((la + lb) / 2, 5)))
lam = rng.normal(size=6)
y0 = 0.37
lhs = np.sum((y0 - lam) ** 2)
C = lhs - len(lam) * (y0 - lam.mean()) ** 2
C2 = np.sum((0.9 - lam) ** 2) - len(lam) * (0.9 - lam.mean()) ** 2
check('M labels, sum (y - l_m)^2 = M (y - mean)^2 + C with C independent of y, the cross term vanishes',
      abs(C - C2) < 1e-12 and abs(np.sum(lam.mean() - lam)) < 1e-12, (C, C2))
# the linear network: least squares on repeated inputs is least squares on the averages of their labels, each average
# counted with its number M of pairs, the sum of M (y - mean)^2 over the inputs; with unequal M the unweighted fit to the
# averages is another fit, so the fold says "each average counts as many times as it has pairs"
K = 12
Ms = np.random.default_rng(11).integers(1, 9, K)
Xg = np.hstack([rng.normal(size=(K, 4)), np.ones((K, 1))])
X = np.repeat(Xg, Ms, axis=0)
labels = rng.normal(size=Ms.sum())
means = np.array([g.mean() for g in np.split(labels, np.cumsum(Ms)[:-1])])
th_all = np.linalg.lstsq(X, labels, rcond=None)[0]
th_w = np.linalg.lstsq(Xg * np.sqrt(Ms)[:, None], means * np.sqrt(Ms), rcond=None)[0]
th_un = np.linalg.lstsq(Xg, means, rcond=None)[0]
check('the linear network fitted to all the pairs is the fit to the averages weighted by M, and not the unweighted one',
      len(set(Ms)) > 1 and np.abs(th_all - th_w).max() < 1e-12 and np.abs(th_all - th_un).max() > 0.01,
      'M from %d to %d, weighted %.1e, unweighted %.3f' % (Ms.min(), Ms.max(), np.abs(th_all - th_w).max(),
                                                          np.abs(th_all - th_un).max()))

# --- the second quiz: the bandwidth 4t, and the two labels t and -t of one input -----------------------------------
kk = np.linspace(-np.pi, np.pi, 200001)
check('the chain with t=1 has the bandwidth 4t', abs(np.ptp(band(kk, 1.0, 0.0)) - 4) < 1e-9, np.ptp(band(kk, 1.0, 0.0)))
t = 1.0
lsum = (yy - t) ** 2 + (yy + t) ** 2
check('the pairs (O, t) and (O, -t): the best output is the mean 0 of the two labels, and there the sum (10.12) over the '
      'two pairs is 2t^2, t^2 per pair, corrected on 2026-11-22', abs(yy[np.argmin(lsum)]) < 1e-9
      and abs(lsum.min() - 2 * t ** 2) < 1e-12 and abs((0 - t) ** 2 + (0 + t) ** 2 - 2 * t ** 2) == 0,
      (yy[np.argmin(lsum)], lsum.min(), lsum.min() / 2))

# --- the caption of dos_sign: the same density of states for t and -t, 1/(pi sqrt(4t^2-E^2)) ------------------------
d = style.run_script('session10/g5_chain_sign_dos.py')
E = np.asarray(d['energies'])
D1, Dm = np.asarray(d['dos'][1.]), np.asarray(d['dos'][-1.])
inside = np.abs(E) < 1.9
closed = 1 / (np.pi * np.sqrt(4 - E[inside] ** 2))
check('pyqula, the density of states per site of t=1 and t=-1 is the same and is 1/(pi sqrt(4t^2-E^2)) inside the band',
      np.abs(D1 - Dm).max() < 1e-12 and np.abs(D1[inside] / closed - 1).max() < 1e-4
      and np.abs(np.asarray(d['bands'][1.]) + np.asarray(d['bands'][-1.])).max() < 1e-12,
      'largest relative deviation %.1e, D(0) = %.4f' % (np.abs(D1[inside] / closed - 1).max(), D1[np.argmin(np.abs(E))]))

# --- the problem: t and -t, t2 and -t2 -----------------------------------------------------------------------------
k = np.linspace(-np.pi, np.pi, 1001)
check('the shift k -> k + pi maps t to -t and keeps t2, eps_{k+pi}(t, t2) = eps_k(-t, t2)',
      np.abs(band(k + np.pi, 1.0, 0.3) - band(k, -1.0, 0.3)).max() < 1e-12, 'checked on 1001 momenta')
check('t2 -> -t2 turns every energy into minus itself, eps_k(t, -t2) = -eps_{k+pi}(t, t2)',
      np.abs(band(k, 1.0, -0.3) + band(k + np.pi, 1.0, 0.3)).max() < 1e-12, 'checked on 1001 momenta')
ext = {t2: (band(kk, 1.0, t2).min(), band(kk, 1.0, t2).max()) for t2 in (0.2, -0.2)}
check('the band goes from -2.4 to 1.6 for t2=0.2 and from -1.6 to 2.4 for t2=-0.2',
      np.allclose(ext[0.2], (-2.4, 1.6), atol=1e-9) and np.allclose(ext[-0.2], (-1.6, 2.4), atol=1e-9), ext)
w = np.random.default_rng(1).uniform(-1, 1, toy.N)
Hp, Hm = toy.ring(0.3, w), toy.ring(0.3, w)
i = np.arange(toy.N)
Hm[i, (i + 1) % toy.N] = Hm[(i + 1) % toy.N, i] = 1.0          # the ring with t=-1, the same t2 and onsite energies
G = np.diag((-1.0) ** i)
check('on the ring of 200 sites, c_j -> (-1)^j c_j maps t to -t and keeps t2 and the onsite energies',
      np.abs(G @ Hp @ G - Hm).max() < 1e-15 and toy.N % 2 == 0, np.abs(G @ Hp @ G - Hm).max())
lv_p, lv_m = np.linalg.eigvalsh(Hp), np.linalg.eigvalsh(Hm)
check('so the disordered rings with t and -t have the same levels', np.abs(lv_p - lv_m).max() < 1e-12,
      np.abs(lv_p - lv_m).max())


def ring_n(n, t, t2):
    """A clean ring of n sites with the matrix elements -t and -t2."""
    j = np.arange(n)
    H = np.zeros((n, n))
    H[j, (j + 1) % n] = H[(j + 1) % n, j] = -t
    H[j, (j + 2) % n] = H[(j + 2) % n, j] = -t2
    return np.linalg.eigvalsh(H)


# the range of "the sign of t only moves each level in momentum": the infinite chain and a ring with an even number of
# sites; on an odd ring k + pi is not a momentum of the ring, and t and -t give other levels
odd5 = np.abs(ring_n(5, 1.0, 0.0) - ring_n(5, -1.0, 0.0)).max()
odd199 = np.abs(ring_n(199, 1.0, 0.2) - ring_n(199, -1.0, 0.2)).max()
even = max(np.abs(ring_n(n, 1.0, 0.2) - ring_n(n, -1.0, 0.2)).max() for n in (6, 200))
check('t and -t give the same levels on rings of 6 and 200 sites, and other levels on rings of 5 and 199 sites',
      even < 1e-12 and odd5 > 1 and odd199 > 0.03, 'even %.1e, 5 sites %.3f, 199 sites %.3f' % (even, odd5, odd199))
fine = np.linspace(-np.pi, np.pi, 2000001)
hp = np.histogram(band(fine, 1.0, 0.2), bins=70, range=(-3.5, 3.5))[0]
hm = np.histogram(band(fine, 1.0, -0.2), bins=70, range=(-3.5, 3.5))[0]
hq = np.histogram(band(fine, -1.0, 0.2), bins=70, range=(-3.5, 3.5))[0]
check('on a fine k-mesh, t2=0.2 and t2=-0.2 give different densities of states, t and -t the same, and -t2 the mirror',
      np.abs(hp - hm).sum() > 0.5 * hp.sum() and np.abs(hp - hq).max() <= 2 and np.abs(hp - hm[::-1]).max() <= 2,
      'differences %d, %d and %d of %d momenta' % (np.abs(hp - hm).sum(), np.abs(hp - hq).max(),
                                                   np.abs(hp - hm[::-1]).max(), hp.sum()))
asym = []
for t, t2 in ((1.0, 0.05), (1.0, 0.2), (1.0, 0.3), (1.0, 0.6), (1.0, -0.4), (-1.0, 0.2), (0.0, 0.3)):
    hh = np.histogram(band(fine, t, t2), bins=70, range=(-3.5, 3.5))[0]
    asym.append(np.abs(hh - hh[::-1]).sum() / hh.sum())
check('D(E) and D(-E) differ for t != 0 and t2 != 0, and are the same for t = 0',
      min(asym[:-1]) > 0.05 and asym[-1] < 1e-5, ' '.join('%.3f' % x for x in asym))
kmin = {t: kk[np.argmin(band(kk, t, 0.0))] for t in (1.0, -1.0)}
check('the band minimum is at k=0 for t>0 and at k=pi for t<0', abs(kmin[1.0]) < 1e-4 and abs(abs(kmin[-1.0]) - np.pi) < 1e-4,
      kmin)
# the range of this statement, t2 >= -|t|/4: the curvature at the minimum, 2|t| + 8 t2, is positive above it, and at
# t=1, t2 = -1/4 the band is eps_k - eps_0 = (cos k - 1)^2, flat to fourth order, so k=0 is still the minimum (an argmin
# on a grid is not asserted there); below it the minimum moves away from k=0 and pi
km = {}
for t in (1.0, -1.0):
    for t2 in (0.3, 0.0, -0.24, -0.26, -0.3, -0.6):
        km[(t, t2)] = abs(kk[np.argmin(band(kk, t, t2))])
edge = np.abs(band(kk, 1.0, -0.25) - band(0.0, 1.0, -0.25) - (np.cos(kk) - 1) ** 2).max()
edge_m = np.abs(band(kk + np.pi, -1.0, -0.25) - band(np.pi, -1.0, -0.25) - (np.cos(kk) - 1) ** 2).max()
check('the band minimum is at k=0 (t>0) and k=pi (t<0) for t2 >= -|t|/4, and moves away below it',
      all(km[(1.0, x)] < 1e-4 and abs(km[(-1.0, x)] - np.pi) < 1e-4 for x in (0.3, 0.0, -0.24))
      and all(km[(1.0, x)] > 0.2 and abs(km[(-1.0, x)] - np.pi) > 0.2 for x in (-0.26, -0.3, -0.6))
      and edge < 1e-12 and edge_m < 1e-12 and 2 * 1.0 + 8 * (-0.24) > 0 > 2 * 1.0 + 8 * (-0.26),
      'k_min for t=1: ' + ', '.join('%g at t2=%g' % (round(km[(1.0, x)], 3), x) for x in (0.0, -0.24, -0.26, -0.3, -0.6)))
check('for t2=0 the band has the width 4|t| for both signs of t',
      abs(np.ptp(band(kk, 1.0, 0.0)) - 4) < 1e-9 and abs(np.ptp(band(kk, -1.0, 0.0)) - 4) < 1e-9, 4)

# --- the caption of ham_learning: the observable and the left panel from pyqula --------------------------------------
check('the observable has 40 bins of width 0.175 between -3.5 and 3.5',
      len(toy.BINS) == 41 and toy.BINS[0] == -3.5 and toy.BINS[-1] == 3.5 and np.allclose(np.diff(toy.BINS), 0.175),
      np.diff(toy.BINS)[0])
r = style.run_script('session10/g5_ring_dos.py')
rng = np.random.default_rng(3)
same = True
for t2 in (0.05, 0.35):
    for W in (0.0, 0.7, 1.4):
        same = same and np.array_equal(r['observables'][(t2, W)],
                                       toy.histogram(np.linalg.eigvalsh(toy.ring(t2, rng.uniform(-W, W, toy.N)))))
check('the left panel, the pyqula script gives the observable of the numpy ring for t2 = 0.05, 0.35 and W = 0, 0.7, 1.4',
      same and sorted(r['observables']) == [(a, b) for a in (0.05, 0.35) for b in (0.0, 0.7, 1.4)], same)

# --- the toy over ten seeds: the caption (seed 3) and the picture quiz (ranges) ------------------------------------
# the errors of the unrounded levels, conventions sheet of Session 10 and a copy of the old script, to 4 digits
OLD = {'clean_rms': [0.0711, 0.0577, 0.0717, 0.0635, 0.0739, 0.0653, 0.0681, 0.0650, 0.0594, 0.0684],
       'disorder_rms': [0.0046, 0.0045, 0.0044, 0.0043, 0.0046, 0.0049, 0.0050, 0.0054, 0.0040, 0.0044]}
start = time.perf_counter()
runs = [toy.toy(s) for s in range(10)]
per_pair = (time.perf_counter() - start) / (10 * (200 + 600 + 600))
toy.check_seed3(runs[3])
val = {key: np.array([x[key] for x in runs]) for key in ('clean_rms', 'clean_rms_W1', 'disorder_rms', 'clean_bias',
                                                          'clean_below', 'flat_rms', 'disorder_bias', 'clean_empty',
                                                          'disorder_empty', 'clean_orth', 'disorder_orth',
                                                          'clean_nullproj', 'clean_flipnorm')}
# the first quiz, "so we can make 10^5 pairs": one pair of the toy is one ring of 200 sites, diagonalized and binned,
# and the ten seeds above, with the fits, take per_pair seconds per ring on one thread; an hour for 10^5 pairs is
# 36 ms per pair, several times the cost here, so that a loaded machine passes too
check('the first quiz, 10^5 pairs of the toy take less than an hour on one thread', 1e5 * per_pair < 3600,
      '%.1f ms per pair, %.0f min for 10^5 pairs' % (1e3 * per_pair, 1e5 * per_pair / 60))
# the caption, "with the solution of smallest norm": some bins are empty in all the training rings, 12 of the 40 for the
# clean ones, so (10.12) has many solutions; lstsq gives the one orthogonal to the null space, the smallest norm, and a
# null vector moves the predictions on the disordered test rings, so the numbers of the clean fit hold for this solution;
# a null vector of norm flipnorm turns the mean error of the clean fit to zero
check('the caption, bins empty in all the training rings, 12 of the 40 for the clean ones, so (10.12) has many solutions',
      np.all(val['clean_empty'] == 12) and np.all(val['disorder_empty'] >= 1) and np.all(val['clean_nullproj'] > 0.05),
      'empty bins %s and %s, a null vector moves a clean prediction by up to %.3f to %.3f'
      % (sorted(set(val['clean_empty'])), sorted(set(val['disorder_empty'])), val['clean_nullproj'].min(),
         val['clean_nullproj'].max()))
check('the caption, lstsq gives the solution of smallest norm, orthogonal to the null space, in both fits and all seeds',
      val['clean_orth'].max() < 1e-9 and val['disorder_orth'].max() < 1e-9,
      max(val['clean_orth'].max(), val['disorder_orth'].max()))
check('another solution changes the clean numbers, a null vector of norm 1 to 3 brings the mean error of the clean fit to 0',
      1 < val['clean_flipnorm'].min() and val['clean_flipnorm'].max() < 3,
      '%.2f to %.2f' % (val['clean_flipnorm'].min(), val['clean_flipnorm'].max()))
check('rounding the levels to 8 digits changes no error of the seeds 0 to 9, to 4 digits',
      all(np.abs(val[key] - np.array(OLD[key])).max() < 5.1e-5 for key in OLD),
      max(np.abs(val[key] - np.array(OLD[key])).max() for key in OLD))
check('the caption, the seed 3 misses t2 by 0.06 trained on clean rings, 0.10 for W>1, and 0.004 trained with disorder',
      round(runs[3]['clean_rms'], 2) == 0.06 and round(runs[3]['clean_rms_W1'], 2) == 0.10
      and round(runs[3]['disorder_rms'], 3) == 0.004,
      (round(runs[3]['clean_rms'], 4), round(runs[3]['clean_rms_W1'], 4), round(runs[3]['disorder_rms'], 4)))
dr = val['disorder_rms']
check('the quiz, trained with disorder the error is 0.004 to 0.005 over ten draws', 0.0039 < dr.min() and dr.max() < 0.0055
      and round(dr.min(), 3) == 0.004 and round(dr.max(), 3) == 0.005, (dr.min().round(4), dr.max().round(4)))
cb, cbl = val['clean_bias'], val['clean_below']
check('the quiz, trained on clean rings most points are below the diagonal and the mean error is -0.03 to -0.05',
      cbl.min() > 0.75 and round(-cb.max(), 2) == 0.03 and round(-cb.min(), 2) == 0.05 and cb.max() < 0,
      'fraction below %.2f to %.2f, mean error %.4f to %.4f' % (cbl.min(), cbl.max(), cb.min(), cb.max()))
cw = val['clean_rms_W1']
check('the caption, decided on 2026-11-22: over ten draws the clean fit misses t2 by about 0.1 for W>1, 0.093 to 0.121',
      round(cw.min(), 1) == 0.1 and round(cw.max(), 1) == 0.1, (cw.min().round(4), cw.max().round(4)))
cr = val['clean_rms']
check('the quiz, trained on clean rings the error is 0.06 to 0.07 over ten draws',
      round(cr.min(), 2) == 0.06 and round(cr.max(), 2) == 0.07, (cr.min().round(4), cr.max().round(4)))
fr = val['flat_rms']
check('the quiz, an output 0.2 for every ring has the error 0.11 to 0.12, near 0.4/sqrt(12) = 0.12 of t2 uniform in [0, 0.4]',
      round(fr.min(), 2) == 0.11 and round(fr.max(), 2) == 0.12 and round(0.4 / np.sqrt(12), 2) == 0.12,
      (fr.min().round(4), fr.max().round(4), round(0.4 / np.sqrt(12), 4)))
check('the network trained with disorder has no systematic error, the mean error is below 0.001',
      np.abs(val['disorder_bias']).max() < 0.001, np.abs(val['disorder_bias']).max().round(5))
print('all checks of page 07 hold')
