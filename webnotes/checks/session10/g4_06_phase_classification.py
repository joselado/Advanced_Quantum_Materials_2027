"""Session 10, the numbers and formulas that page 06 (Section 10.6a) quotes, in the key box, the captions, the quizzes
and the problem.

The pictures of the quiz of histograms are the pyqula script scripts/session10/g4_ising_snapshots.py, run here as the
figure helper figures/session10/_g4_isinghist.py runs it, and its check() and check_pictures() are called on that run.
The same calls are made again with the seeds 2 to 5, in parallel, and at k_BT = 3.5 J alone with the seeds 6 to 20,
since the feedback of that picture gives the range of the mean over 20 runs. The five runs also give the numbers of the
Ising side of igt_hist on page 06b, for the conventions sheet. The caption of onsager is asserted in its figure script,
and its numbers again here without drawing. The caption of ising_sizes is asserted here, with the function, the seed and
the parameters of its script, which is not run, so that its SVG is not written. It writes no file, and pyqula runs in a
temporary folder."""
import os
import runpy
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
SCRIPT = os.path.join(ROOT, 'scripts', 'session10', 'g4_ising_snapshots.py')
sys.path.insert(0, os.path.join(ROOT, 'figures', 'session10'))
sys.path.insert(0, os.path.join(ROOT, 'figures'))
import _g4_isinghist  # noqa: E402


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def run(seed, temps=None):
    """The variables of the downloadable script, with its seed 1 replaced by seed, run in a temporary folder. With
    temps, only these temperatures are run. The script sets the seed again before each temperature, so the snapshots
    at one temperature do not depend on the others, which the check asserts for the seed 1."""
    src = open(SCRIPT).read()
    assert src.count('np.random.seed(1)') == 1
    src = src.replace('np.random.seed(1)', 'np.random.seed(%d)' % seed)
    if temps is not None:
        assert src.count('temps = [1.5, 2.27, 3.5]') == 1
        src = src.replace('temps = [1.5, 2.27, 3.5]', 'temps = %r' % list(temps))
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as d:
        os.chdir(d)
        try:
            env = {'__name__': '__main__'}
            exec(compile(src, SCRIPT, 'exec'), env)
        finally:
            os.chdir(cwd)
    return {T: np.asarray(env['absm'][T]) for T in (temps or _g4_isinghist.TEMPS)}


def run_hot(seed):
    """The snapshots at k_BT = 3.5 J alone, for the range of the mean over 20 runs."""
    return run(seed, temps=(3.5,))[3.5]


def figure_ising_sizes():
    """The Monte Carlo of figures/session10/ising_sizes.py with its own function mean_absm, its seed and its order of the
    random numbers, without the drawing. The part of the script before the figure is run as it is, and the loop over the
    sizes and the temperatures is the loop of the script, which is checked in its text."""
    path = os.path.join(ROOT, 'figures', 'session10', 'ising_sizes.py')
    src = open(path).read()
    head, tail = src.split('fig, ax = style.figure(', 1)
    assert 'rng = np.random.default_rng(7)' in head and 'Ts = np.linspace(1.5, 3.5, 21)' in head
    assert 'def mean_absm(L, T, s, nth=1500, nme=3000):' in head       # 1500 sweeps to thermalize, 3000 to average
    assert 'rng' not in tail.split('for L in (8, 16, 32):', 1)[0]      # nothing draws a random number before the loop
    assert 'for L in (8, 16, 32):' in tail and 's = np.ones((L, L), dtype=int)' in tail
    assert 'for T in Ts:' in tail and 'v, s = mean_absm(L, T, s)' in tail
    env = {'__name__': 'ising_sizes_head', '__file__': path}
    exec(compile(head, path, 'exec'), env)
    out = {}
    for L in (8, 16, 32):
        s = np.ones((L, L), dtype=int)
        m = []
        for T in env['Ts']:
            v, s = env['mean_absm'](L, T, s)
            m.append(v)
        out[L] = dict(zip(np.round(env['Ts'], 2), m))
    return out


def exact_m(T):
    return (1 - np.sinh(2 / T) ** -4) ** 0.125


if __name__ == '__main__':
    # --- the key box, the opener and the captions: T_c and the exact |m| ------------------------------------------
    Tc = 2 / np.log(1 + np.sqrt(2))
    check('T_c = 2J/ln(1+sqrt 2) = 2.27 J, where sinh(2J/T_c) = 1', round(Tc, 2) == 2.27 and abs(np.sinh(2 / Tc) - 1) < 1e-12,
          round(Tc, 4))
    check('the exact |m| at k_BT = 1.5 J is 0.9865, the 0.99 of the problem and of the quiz',
          round(exact_m(1.5), 4) == 0.9865 and round(exact_m(1.5), 2) == 0.99, round(exact_m(1.5), 4))
    check('the exact |m| goes to zero at T_c, as (T_c - T)^(1/8), and is 0.78 at 2.2', exact_m(Tc - 1e-12) < 0.05
          and round(exact_m(2.2), 2) == 0.78, (round(exact_m(Tc - 1e-12), 3), round(exact_m(2.2), 3)))

    # --- the quiz on |m| = 0.93 ------------------------------------------------------------------------------------
    N = 64 ** 2
    check('N = 64^2 = 4096 independent spins give 1/sqrt N = 0.016', N == 4096 and round(1 / np.sqrt(N), 3) == 0.016,
          1 / np.sqrt(N))
    check('|m| = 0.93 is more than 50 standard deviations of independent spins', 0.93 * np.sqrt(N) > 50,
          round(0.93 * np.sqrt(N), 1))

    # --- the problem: <m> = 0 and <m^2> = 1/N, by enumeration and by sampling -------------------------------------
    n = 10
    s = 1 - 2 * ((np.arange(2 ** n)[:, None] >> np.arange(n)) & 1)          # all 2^10 configurations
    m = s.mean(axis=1)
    check('N = 10 independent spins, all configurations: <m> = 0 and <m^2> = 1/N', abs(m.mean()) < 1e-15
          and abs((m ** 2).mean() - 1 / n) < 1e-15, ((m ** 2).mean(), 1 / n))
    spreads = []
    for seed in range(5):      # 20000 snapshots, so that the spread has a statistical error of 0.5 percent
        rng = np.random.default_rng(seed)
        sample = np.concatenate([rng.choice(np.array([-1, 1], dtype=np.int8), size=(2000, N)).mean(axis=1)
                                 for _ in range(10)])
        spreads.append(sample.std())
    check('20000 snapshots of 4096 random spins give a spread of m of 0.016, in five samples',
          all(round(x, 3) == 0.016 for x in spreads), [round(x, 5) for x in spreads])
    check('0.99 at k_BT = 1.5 J is more than 60 times 1/sqrt N', exact_m(1.5) * np.sqrt(N) > 60 and 0.99 * 64 > 60,
          round(exact_m(1.5) * np.sqrt(N), 1))

    # --- the quiz of histograms: the seed of the pictures, five runs, and 20 runs at 3.5 J; the caption of ising_sizes -
    hot_seeds = [1] + list(range(6, 21))       # the seeds 2 to 5 at 3.5 J come from the five full runs
    with ProcessPoolExecutor(max_workers=6) as ex:
        sizes_job = ex.submit(figure_ising_sizes)
        runs = dict(zip(range(1, 6), ex.map(run, range(1, 6))))
        hot = dict(zip(hot_seeds, ex.map(run_hot, hot_seeds)))
        sizes = sizes_job.result()
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as d:
        os.chdir(d)
        try:
            pictures = runpy.run_path(SCRIPT)['absm']
        finally:
            os.chdir(cwd)
    check('the run with the seed 1 is the run of the pictures', all(np.array_equal(pictures[T], runs[1][T])
          for T in _g4_isinghist.TEMPS), 'seed 1')
    lo, tcmin, tcmax, hi = _g4_isinghist.check(pictures)
    _g4_isinghist.check_pictures(pictures)
    check('pictures: mean 0.99 at 1.5 J, from below 0.5 to above 0.9 at 2.27 J, a mean of 0.115 to 0.135 at 3.5 J, and '
          'the alt texts', True, (round(lo, 3), round(tcmin, 3), round(tcmax, 3), round(hi, 3)))
    for seed, r in runs.items():
        out = _g4_isinghist.check(r)
        check('seed %d, the statements of the feedback at 1.5 J and 2.27 J, and a mean at 3.5 J of 0.115 to 0.135'
              % seed, True, tuple(round(x, 3) for x in out))
    check('the run at 3.5 J alone gives the same snapshots as the full run, for the seed 1',
          np.array_equal(hot[1], runs[1][3.5]), 'seed 1')
    hot.update({s_: runs[s_][3.5] for s_ in range(2, 6)})
    means = np.array([hot[s_].mean() for s_ in sorted(hot)])
    check('the feedback at 3.5 J: the mean |m| is about 0.12, from 0.11 to 0.13 over 20 runs', len(means) == 20
          and round(means.mean(), 2) == 0.12 and round(means.min(), 2) == 0.11 and round(means.max(), 2) == 0.13,
          (round(means.min(), 4), round(means.max(), 4), round(means.mean(), 4)))
    check('at 3.5 J the mean |m| is of the order of 1/sqrt N = 1/16 of 256 spins, between one and three times it',
          all(1 < x * 16 < 3 for x in means), (round(means.min() * 16, 2), round(means.max() * 16, 2)))

    # --- the Ising side of igt_hist on page 06b is this run, for the line of the conventions sheet --------------------
    m15 = [runs[s_][1.5].mean() for s_ in runs]
    m35 = [runs[s_][3.5].mean() for s_ in runs]
    check('the seed 1 of igt_hist: the largest |m| at 3.5 J is 0.508, below the smallest 0.922 at 1.5 J',
          round(pictures[3.5].max(), 3) == 0.508 and round(pictures[1.5].min(), 3) == 0.922,
          (round(pictures[3.5].max(), 4), round(pictures[1.5].min(), 4)))
    check('the seeds 1 to 5: the mean |m| is 0.987 to 0.988 at 1.5 J and 0.119 to 0.134 at 3.5 J',
          round(min(m15), 3) == 0.987 and round(max(m15), 3) == 0.988 and round(min(m35), 3) == 0.119
          and round(max(m35), 3) == 0.134, ([round(x, 4) for x in m15], [round(x, 4) for x in m35]))

    # --- the caption of ising_sizes, with the seed and the parameters of its script ------------------------------------
    low = (1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1)
    dev = {L: {T: sizes[L][T] - exact_m(T) for T in low + (2.2,)} for L in sizes}
    check('ising_sizes: L = 8, 16 and 32, 1500 sweeps to thermalize and 3000 to average, read in its script',
          sorted(sizes) == [8, 16, 32], 'the text of ising_sizes.py')
    check('ising_sizes below T_c: the three sizes agree with the exact |m| to 0.0066 at the seven temperatures from 1.5 J '
          'to 2.1 J', all(abs(dev[L][T]) < 0.0066 for L in sizes for T in low),
          round(max(abs(dev[L][T]) for L in sizes for T in low), 4))
    check('ising_sizes at 2.2 J, close to T_c, the caption corrected on 2026-11-22: L = 8 is 0.03 above the exact '
          'curve, and up to 2.1 J the three sizes are within 0.007', dev[8][2.2] > 0.025 and round(dev[8][2.2], 2) == 0.03
          and round(max(abs(dev[L][T]) for L in sizes for T in low), 3) <= 0.007,
          tuple(round(dev[L][2.2], 3) for L in (8, 16, 32)))
    check('the text, ferromagnetic order with |m| > 0 below T_c, which reaches 1 only as T goes to 0',
          all(0 < exact_m(T) < 1 for T in np.linspace(0.5, Tc - 1e-6, 200)) and exact_m(0.5) > 0.9999,
          (round(exact_m(2.2), 4), exact_m(0.5)))
    m30 = [sizes[L][3.0] for L in (8, 16, 32)]
    check('ising_sizes above T_c: L <|m|> at 3.0 J is 2.6 to 2.9 for the three sizes, the order 1/L',
          all(2.6 < L * m < 2.9 for L, m in zip((8, 16, 32), m30)), [round(L * m, 2) for L, m in zip((8, 16, 32), m30)])
    above = [T for T in sizes[8] if T >= 2.4]
    check('ising_sizes: the drop becomes sharper as L grows, <|m|> falls with L at every temperature from 2.4 J',
          all(sizes[8][T] > sizes[16][T] > sizes[32][T] for T in above), '%d temperatures' % len(above))
    print('all checks of page 06 passed')
