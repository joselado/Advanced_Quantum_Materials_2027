"""Session 10, Section 10.7, the toy of Hamiltonian learning, shared by the right panel of ham_learning.py, the three
picture options of the quiz on the training set (g5_quiz_hl_*.py) and the check script of the page.

The Hamiltonian is a ring of 200 sites with the matrix elements -1 to the first and -t2 to the second neighbors, the
sign of the notes with t=1, and a random onsite energy uniform in [-W, W], the hidden variable. The observable O is
the fraction of the 200 levels in each of 40 bins of energy on [-3.5, 3.5]. The network is the simplest one, a linear
map from the 40 numbers of O and a constant to t2, fitted by least squares, which is (10.12). It is trained twice on
600 rings with t2 uniform in [0, 0.4], once on clean rings (W=0) and once with W uniform in [0, 1.5], and both are
tested on the same 200 rings with W uniform in [0, 1.5]. The random numbers are drawn in the order of the old script
ham_learning.py, so the seed 3 gives its errors, 0.0635, 0.1027 for W>1 and 0.0043. Some bins are empty in all the
training rings, 12 of the 40 for the clean ones, so the least-squares fit has many solutions, and lstsq gives the one
of smallest norm, which the caption says. The levels are rounded to 8
digits before the histogram, as in webnotes/scripts/session10/g5_ring_dos.py, so that a level on a bin edge falls in
the same bin at every run; this changes no error of the seeds 0 to 9 (the check script asserts it). Numpy, since
pyqula has no least-squares fit, so the options have no button. This file writes no figure."""
import os, sys
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')     # small matrices, threads only cost time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import style

N, NB = 200, 40
BINS = np.linspace(-3.5, 3.5, NB + 1)
I = np.arange(N)


def ring(t2, onsite):
    """The ring of 200 sites with the matrix elements -1 and -t2 and the given onsite energies."""
    H = np.diag(np.asarray(onsite, float))
    H[I, (I + 1) % N] = H[(I + 1) % N, I] = -1.0
    H[I, (I + 2) % N] = H[(I + 2) % N, I] = -t2
    return H


def histogram(levels, rounded=True):
    """The observable O, the fraction of the levels in each bin."""
    lv = np.round(levels, 8) if rounded else levels
    return np.histogram(lv, bins=BINS)[0] / N


def toy(seed, rounded=True):
    """The test set and the two trained networks of the toy, for one seed."""
    rng = np.random.default_rng(seed)

    def sample(n, wmax):
        lam = rng.uniform(0, 0.4, n)
        W = rng.uniform(0, wmax, n)
        O = np.array([histogram(np.linalg.eigvalsh(ring(a, rng.uniform(-b, b, N))), rounded) for a, b in zip(lam, W)])
        return O, lam, W

    Ote, lte, Wte = sample(200, 1.5)
    Xte = np.hstack([Ote, np.ones((len(Ote), 1))])
    out = dict(true=lte, W=Wte)
    for name, wmax in (('clean', 0.0), ('disorder', 1.5)):
        Otr, ltr, Wtr = sample(600, wmax)
        out[name + '_train'] = (len(ltr), ltr.min(), ltr.max(), Wtr.max())
        X = np.hstack([Otr, np.ones((len(Otr), 1))])
        theta = np.linalg.lstsq(X, ltr, rcond=None)[0]
        p = Xte @ theta
        out[name] = p
        out[name + '_rms'] = np.sqrt(np.mean((p - lte) ** 2))
        out[name + '_rms_W1'] = np.sqrt(np.mean((p - lte)[Wte > 1] ** 2))
        out[name + '_bias'] = np.mean(p - lte)
        out[name + '_below'] = np.mean(p < lte)
        out[name + '_rank'] = np.linalg.matrix_rank(X)
        # (10.12) has many solutions when bins are empty in all the training rings: the null space of X. lstsq gives
        # the solution of smallest norm, orthogonal to it, and a null vector moves the test predictions by Xte @ null
        s, Vt = np.linalg.svd(X)[1:]
        null = Vt[int(np.sum(s > s[0] * 1e-12)):].T
        g = (Xte @ null).mean(0)
        out[name + '_empty'] = int(np.sum(Otr.sum(0) == 0))
        out[name + '_orth'] = np.abs(null.T @ theta).max()
        out[name + '_nullproj'] = np.abs(Xte @ null).max()
        out[name + '_flipnorm'] = abs(out[name + '_bias']) / np.linalg.norm(g) if np.linalg.norm(g) > 1e-12 else np.inf
    out['flat'] = np.full(len(lte), 0.2)
    out['flat_rms'] = np.sqrt(np.mean((0.2 - lte) ** 2))
    return out


SEED = 3          # the seed of the figure ham_learning and of the pictures of the quiz
YLIM = (-0.1, 0.44)


def check_seed3(d):
    """The numbers of the caption of ham_learning and of the pictures, for the seed of the figure."""
    assert abs(d['clean_rms'] - 0.0635) < 5e-5 and abs(d['clean_rms_W1'] - 0.1027) < 5e-5, d['clean_rms']
    assert abs(d['disorder_rms'] - 0.0043) < 5e-5, d['disorder_rms']
    assert d['clean_rank'] == 27 and d['disorder_rank'] == 38
    # the caption: some bins are empty in all the training rings, 12 of the 40 for the clean ones, so (10.12) has many
    # solutions, and the numbers are those of the solution of smallest norm; with disorder the test rings of the seed 3
    # have no part in the null space, so there every solution gives the same predictions
    assert d['clean_empty'] == 12 and d['disorder_empty'] >= 1
    assert d['clean_orth'] < 1e-9 and d['disorder_orth'] < 1e-9
    assert d['clean_nullproj'] > 0.05 and d['disorder_nullproj'] < 1e-12
    # 200 test rings with W in [0, 1.5], 600 training rings, t2 in [0, 0.4], W = 0 for the clean ones
    assert len(d['true']) == 200 and 0 <= d['W'].min() and d['W'].max() <= 1.5 and 0 <= d['true'].min()
    assert d['true'].max() <= 0.4 and d['clean_train'][0] == d['disorder_train'][0] == 600
    assert d['clean_train'][3] == 0 and 1.4 < d['disorder_train'][3] <= 1.5
    assert all(0 <= d[k][1] and d[k][2] <= 0.4 for k in ('clean_train', 'disorder_train'))
    assert 0.8 < d['clean_below'] < 0.85 and abs(d['flat_rms'] - 0.1076) < 5e-4
    # every point of the three pictures is inside the common window
    for k in ('clean', 'disorder', 'flat'):
        assert YLIM[0] < d[k].min() and d[k].max() < YLIM[1], (k, d[k].min(), d[k].max())
    print('seed 3: clean %.4f (W>1 %.4f, bias %.4f, %.0f%% below), disorder %.4f, flat %.4f, empty bins %d and %d'
          % (d['clean_rms'], d['clean_rms_W1'], d['clean_bias'], 100 * d['clean_below'], d['disorder_rms'],
             d['flat_rms'], d['clean_empty'], d['disorder_empty']))


def option(script, which):
    """One picture option of the quiz, the predicted t2 against the true one for the 200 test rings of the seed 3."""
    d = toy(SEED)
    check_seed3(d)
    fig, ax = style.plt.subplots(figsize=(3.7 * style.CM, 3.9 * style.CM))
    ax.plot([0, 0.42], [0, 0.42], color=style.GRID, lw=1.0, zorder=0)
    ax.scatter(d['true'], d[which], color=style.ACCENT, s=5, lw=0, zorder=2)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xlim(0, 0.42); ax.set_ylim(*YLIM)
    ax.set_xticks([0, 0.2, 0.4]); ax.set_xticklabels(['0', '0.2', '0.4'], fontsize=11)
    ax.set_yticks([0, 0.2, 0.4]); ax.set_yticklabels(['0', '0.2', '0.4'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'true $t_2$', fontsize=12, labelpad=1); ax.set_ylabel(r'predicted $t_2$', fontsize=12, labelpad=1)
    style.save(fig, script)
