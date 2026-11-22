"""Session 10, the numbers and formulas that page 06b (Section 10.6b) quotes, in the key box, the steps fold, the
caption of igt_hist, the quizzes and the problem.

The plaquette of one square, the open lattices of 2 x 2 and 2 x 3 plaquettes and the torus of 3 x 3 vertices are summed
over all their configurations. The 16 x 16 torus of igt_hist is checked with random configurations and, for the fraction
of plaquettes at -1 at k_BT = 5J, with a vectorized Metropolis run on four sublattices of links, a second route to the
run of the figure script, which asserts its own numbers. The same run at 0.2 J with no vertex flips, from every link at
+1, is the statement of the caption that single flips alone leave the bonds at +1. The bond pictures of the quiz are asserted by
figures/session10/_g4_igtlattice.py, whose check() is called here. The links are those of igt_hist.py, h[x, y] from
(x, y) to (x+1, y) and v[x, y] from (x, y) to (x, y+1). It writes no file."""
import itertools
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures', 'session10'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures'))
import _g4_igtlattice  # noqa: E402


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def torus_plaquettes(h, v):
    """The plaquette products of an L x L torus, P[x, y] = h[x, y] v[x+1, y] h[x, y+1] v[x, y], as in igt_hist.py.
    h and v may carry a leading axis of configurations."""
    return h * np.roll(v, -1, -2) * np.roll(h, -1, -1) * v


def star_torus(h, v, X, Y):
    L = h.shape[-1]
    h[X, Y] *= -1; h[(X - 1) % L, Y] *= -1; v[X, Y] *= -1; v[X, (Y - 1) % L] *= -1


def all_configs(n):
    return 1 - 2 * ((np.arange(2 ** n)[:, None] >> np.arange(n)) & 1)


TEMPS = (0.2, 1.0, 5.0)

# --- the steps fold, one plaquette -----------------------------------------------------------------------------------
s = all_configs(4)
P = s.prod(axis=1)
flip = s * np.array([-1, -1, 1, 1])
check('one plaquette: the flip of the bonds 1 and 2 keeps every product and maps sigma_1 to -sigma_1',
      np.array_equal(flip.prod(axis=1), P) and np.array_equal(flip[:, 0], -s[:, 0]), 'all 16 configurations')
for T in TEMPS:
    w = np.exp(P / T)
    check('one plaquette at k_BT = %gJ: <sigma_1> = 0' % T, abs((s[:, 0] * w).sum() / w.sum()) < 1e-15,
          (s[:, 0] * w).sum() / w.sum())

# --- the problem: <P> = tanh(J/k_BT), its values, the open 2 x 2 lattice, the fraction at -1 -------------------------
check('one plaquette: 8 configurations with P = +1 and 8 with P = -1', (P == 1).sum() == 8 and (P == -1).sum() == 8,
      ((P == 1).sum(), (P == -1).sum()))
for T in (0.2, 0.7, 1.0, 5.0):
    w = np.exp(P / T)
    check('one plaquette at k_BT = %gJ: <P> = tanh(J/k_BT)' % T, abs((P * w).sum() / w.sum() - np.tanh(1 / T)) < 1e-14,
          round((P * w).sum() / w.sum(), 6))
check('tanh(J/k_BT) is 0.9999 at 0.2 J, 0.76 at J and 0.197 at 5 J',
      round(np.tanh(5), 4) == 0.9999 and round(np.tanh(1), 2) == 0.76 and round(np.tanh(0.2), 3) == 0.197,
      (np.tanh(5), np.tanh(1), np.tanh(0.2)))
# the open lattice of 2 x 2 plaquettes: h[x, y] with x in 0..1, y in 0..2, v[x, y] with x in 0..2, y in 0..1, 12 links
c = all_configs(12)
h, v = c[:, :6].reshape(-1, 2, 3), c[:, 6:].reshape(-1, 3, 2)
Po = np.stack([h[:, x, y] * v[:, x + 1, y] * h[:, x, y + 1] * v[:, x, y] for x in range(2) for y in range(2)], axis=1)
codes = ((1 - Po) // 2) @ (2 ** np.arange(4))
check('open 2 x 2 plaquettes: the four products take all 16 sets of values, each in 256 configurations',
      np.array_equal(np.bincount(codes, minlength=16), np.full(16, 256)), np.unique(np.bincount(codes, minlength=16)))
for T in TEMPS:
    w = np.exp(Po.sum(axis=1) / T)
    avg = (Po * w[:, None]).sum(axis=0) / w.sum()
    check('open 2 x 2 plaquettes at k_BT = %gJ: every plaquette has <P> = tanh(J/k_BT)' % T,
          np.abs(avg - np.tanh(1 / T)).max() < 1e-14, np.round(avg, 6))
    mm = c.mean(axis=1)
    cc = (c.T * w) @ c / w.sum()
    check('open 2 x 2 plaquettes at k_BT = %gJ: <sigma_i sigma_j> = 0 for i != j and <m^2> = 1/12' % T,
          np.abs(cc - np.eye(12)).max() < 1e-14 and abs((mm ** 2 * w).sum() / w.sum() - 1 / 12) < 1e-14,
          round((mm ** 2 * w).sum() / w.sum(), 6))
# a second size, the open lattice of 2 x 3 plaquettes: h[x, y] with x in 0..1, y in 0..3, v[x, y] with x in 0..2,
# y in 0..2, 17 links, so that "on an open lattice it is the same for every size" holds on more than one lattice
c = all_configs(17)
h, v = c[:, :8].reshape(-1, 2, 4), c[:, 8:].reshape(-1, 3, 3)
Po = np.stack([h[:, x, y] * v[:, x + 1, y] * h[:, x, y + 1] * v[:, x, y] for x in range(2) for y in range(3)], axis=1)
codes = ((1 - Po) // 2) @ (2 ** np.arange(6))
check('open 2 x 3 plaquettes: the six products take all 64 sets of values, each in 2048 configurations',
      np.array_equal(np.bincount(codes, minlength=64), np.full(64, 2048)), np.unique(np.bincount(codes, minlength=64)))
for T in TEMPS:
    w = np.exp(Po.sum(axis=1) / T)
    avg = (Po * w[:, None]).sum(axis=0) / w.sum()
    check('open 2 x 3 plaquettes at k_BT = %gJ: every plaquette has <P> = tanh(J/k_BT), as for one plaquette and for '
          '2 x 2, to the round-off of 131072 weights' % T, np.abs(avg - np.tanh(1 / T)).max() < 1e-12, np.round(avg, 6))
t5 = np.tanh(0.2)
check('the fraction of plaquettes at -1 is (1 - tanh(J/k_BT))/2 = 0.40 at 5 J on an open lattice', round((1 - t5) / 2, 2)
      == 0.40, (1 - t5) / 2)
Np = 256
Ptor = (t5 + t5 ** (Np - 1)) / (1 + t5 ** Np)
check('on the 16 x 16 torus, (t + t^(N-1))/(1 + t^N) with N = 256 plaquettes gives the same 0.40', round((1 - Ptor) / 2, 2)
      == 0.40, (1 - Ptor) / 2)

# --- the 3 x 3 torus by enumeration: the gauge flips, <sigma_i> = 0, <sigma_i sigma_j> = 0, <m^2> = 1/18 ---------------
L = 3
c = all_configs(2 * L * L)
h, v = c[:, :L * L].reshape(-1, L, L), c[:, L * L:].reshape(-1, L, L)
Pt = torus_plaquettes(h, v).reshape(len(c), -1)
E = -Pt.sum(axis=1)
for T in TEMPS:
    w = np.exp(-E / T)
    mean = (c * w[:, None]).sum(axis=0) / w.sum()
    cc = (c.T * w) @ c / w.sum()
    m2 = (c.mean(axis=1) ** 2 * w).sum() / w.sum()
    check('3 x 3 torus at k_BT = %gJ: <sigma_i> = 0, <sigma_i sigma_j> = 0 for i != j, <m^2> = 1/18' % T,
          np.abs(mean).max() < 1e-14 and np.abs(cc - np.eye(2 * L * L)).max() < 1e-14 and abs(m2 - 1 / 18) < 1e-14,
          round(m2, 6))

# --- the key box, the fold and the caption on the 16 x 16 torus of igt_hist ------------------------------------------
L = 16
rng = np.random.default_rng(5)
h, v = rng.choice([-1, 1], (L, L)), rng.choice([-1, 1], (L, L))
ok = True
for X, Y in rng.integers(0, L, (50, 2)):
    h2, v2 = h.copy(), v.copy()
    star_torus(h2, v2, X, Y)
    ok &= np.array_equal(torus_plaquettes(h2, v2), torus_plaquettes(h, v)) and int((h2 != h).sum() + (v2 != v).sum()) == 4
check('16 x 16 torus: the flip of the four links at a vertex keeps every plaquette, at 50 random vertices', ok, '50 flips')
ok = True
for _ in range(50):
    h2 = h.copy(); X, Y = rng.integers(0, L, 2); h2[X, Y] *= -1
    ok &= int((torus_plaquettes(h2, v) != torus_plaquettes(h, v)).sum()) == 2
check('16 x 16 torus: one flipped link changes two plaquettes', ok, '50 flips')
check('512 links and 1/sqrt 512 = 0.044', 2 * L * L == 512 and round(1 / np.sqrt(512), 3) == 0.044, 1 / np.sqrt(512))
# configurations with every plaquette +1 in a random gauge: the uniform state after random star flips
gauge = rng.integers(0, 2, (4000, L, L))
hg = (-1) ** (gauge + np.roll(gauge, -1, 1))          # h[x, y] flips with the vertices (x, y) and (x+1, y)
vg = (-1) ** (gauge + np.roll(gauge, -1, 2))          # v[x, y] flips with the vertices (x, y) and (x, y+1)
check('random gauge copies of the uniform state have every plaquette +1', (torus_plaquettes(hg, vg) == 1).all(), '4000')
mg = np.abs(hg.sum(axis=(1, 2)) + vg.sum(axis=(1, 2))) / 512
mr = np.abs(rng.choice([-1, 1], (4000, 512)).mean(axis=1))
for name, a in (('every plaquette +1, random gauge', mg), ('random links, infinite temperature', mr)):
    check('16 x 16 torus, %s: <|m|> = sqrt(2/(512 pi)) = 0.035, which is 0.04 to one digit, and rms 0.044' % name,
          abs(a.mean() - np.sqrt(2 / (512 * np.pi))) < 0.002 and round(np.sqrt(2 / (512 * np.pi)), 2) == 0.04
          and abs(np.sqrt((a ** 2).mean()) - 1 / np.sqrt(512)) < 0.002, (round(a.mean(), 4), round(np.sqrt((a ** 2).mean()), 4)))

def bond_metropolis(T, sweeps, keep, rng):
    """Metropolis flips of single links on the L x L torus from every link at +1, with no vertex flips, on four
    sublattices of links that share no plaquette, h with y even, h with y odd, v with x even, v with x odd. Returns the
    fraction of plaquettes at -1 and |m| after each sweep from the sweep keep on, and the last links."""
    h, v = np.ones((L, L), int), np.ones((L, L), int)
    even = (np.arange(L) % 2 == 0)
    frac, absm = [], []
    for sweep in range(sweeps):
        for which, par in itertools.product('hv', (True, False)):
            Pl = torus_plaquettes(h, v)
            if which == 'h':      # h[x, y] is in the plaquettes (x, y) and (x, y-1)
                dE = 2 * (Pl + np.roll(Pl, 1, 1))
                mask = np.broadcast_to(even[None, :] == par, (L, L))
                acc = mask & (rng.random((L, L)) < np.exp(-dE / T))
                h[acc] *= -1
            else:                 # v[x, y] is in the plaquettes (x, y) and (x-1, y)
                dE = 2 * (Pl + np.roll(Pl, 1, 0))
                mask = np.broadcast_to(even[:, None] == par, (L, L))
                acc = mask & (rng.random((L, L)) < np.exp(-dE / T))
                v[acc] *= -1
        if sweep >= keep:
            frac.append((torus_plaquettes(h, v) < 0).mean())
            absm.append(abs(h.sum() + v.sum()) / (2 * L * L))
    return np.array(frac), np.array(absm), h, v


# a second route to the fraction of plaquettes at -1 of the run of igt_hist at 5 J
frac = bond_metropolis(5.0, 1500, 300, rng)[0]
check('a vectorized Metropolis run at 5 J gives the fraction 0.40 of plaquettes at -1, as the run of igt_hist',
      round(np.mean(frac), 2) == 0.40, round(np.mean(frac), 4))

# --- the caption of igt_hist: the run starts at +1, the vertex flips are moves of their own, and why ----------------
src = open(os.path.join(HERE, '..', '..', 'figures', 'session10', 'igt_hist.py')).read()
check('igt_hist.py starts the gauge theory with every bond at +1 and makes the flips at a vertex as moves',
      'h = np.ones((L, L), dtype=int)' in src and 'v = np.ones((L, L), dtype=int)' in src
      and 'h[x, y] *= -1; h[(x - 1) % L, y] *= -1; v[x, y] *= -1; v[x, (y - 1) % L] *= -1' in src
      and 'np.exp(-2 * P / T)' in src, 'the text of the script')
h, v = np.ones((L, L), int), np.ones((L, L), int)
h1 = h.copy(); h1[3, 5] = -1
cost = torus_plaquettes(h, v).sum() - torus_plaquettes(h1, v).sum()
check('from every bond at +1 one flip costs 4J, accepted at 0.2 J with e^-20 = 2e-9', cost == 4 and
      round(np.exp(-cost / 0.2) * 1e9) == 2, (int(cost), np.exp(-cost / 0.2)))
frac02, absm02, h02, v02 = bond_metropolis(0.2, 3500, 500, rng)
check('single flips alone at 0.2 J, over the 3500 sweeps of igt_hist: every bond stays at +1 and |m| = 1',
      (h02 == 1).all() and (v02 == 1).all() and (absm02 == 1).all() and (frac02 == 0).all(),
      (absm02.min(), 3500 * 512 * np.exp(-20)))

# --- the recall box and the quizzes ------------------------------------------------------------------------------------
Tc = 2 / np.log(1 + np.sqrt(2))
check('the recall box: T_c = 2.27 J', round(Tc, 2) == 2.27, round(Tc, 4))
Tg = np.linspace(0.05, 20, 4000)
check('the crossover quiz: tanh(J/T) is smooth, no jump on a fine grid of T', np.abs(np.diff(np.tanh(1 / Tg))).max() < 0.01,
      np.abs(np.diff(np.tanh(1 / Tg))).max())
nneg = _g4_igtlattice.check()
check('the bond pictures: ground state at -9J with 11 bonds at -1, one flip at -5J, the hot one with 5 plaquettes at -1 '
      'and the energy +J, 10J above', nneg == 5, nneg)

# --- corrected on 2026-11-22: the crossover quiz, the size-dependent crossover and the caption of igt_hist ------------
# A classifier that answers "low temperature" when no plaquette is at -1, on the L x L torus with N = L^2 plaquettes.
# The plaquette sets with an even number of -1 are the allowed ones, each with the same number of link configurations,
# so P(no plaquette at -1) = 2 / [(1+x)^N + (1-x)^N] with x = exp(-2J/k_BT). First route: this formula. Second route:
# all 2^18 link configurations of the 3 x 3 torus.
def p_clean(Lt, T):
    x = np.exp(-2.0 / T)
    return 2.0 / ((1 + x) ** (Lt * Lt) + (1 - x) ** (Lt * Lt))


s18 = all_configs(18)
Pl3 = torus_plaquettes(s18[:, :9].reshape(-1, 3, 3), s18[:, 9:].reshape(-1, 3, 3)).reshape(-1, 9)
clean3 = (Pl3 == 1).all(axis=1)
dev = max(abs(np.exp(Pl3.sum(1) / T)[clean3].sum() / np.exp(Pl3.sum(1) / T).sum() - p_clean(3, T))
          for T in (0.2, 0.5, 1.0, 2.0, 5.0))
check('the detector of plaquettes at -1 on the 3 x 3 torus, the formula and the sum over the 2^18 configurations agree',
      dev < 1e-12, dev)


def t_at(Lt, q):
    lo_, hi_ = 0.02, 20.0                      # p_clean falls with T, bisection on q
    for _ in range(200):
        mid_ = 0.5 * (lo_ + hi_)
        lo_, hi_ = (mid_, hi_) if p_clean(Lt, mid_) > q else (lo_, mid_)
    return 0.5 * (lo_ + hi_)


half = [t_at(Lt, 0.5) for Lt in (4, 8, 16, 28)]
width = [t_at(Lt, 0.25) - t_at(Lt, 0.75) for Lt in (4, 8, 16, 28)]
check('the crossover quiz and the text: the crossover of this classifier moves toward T=0 as L grows, its middle at '
      '0.82, 0.52, 0.38 and 0.31 J for L = 4, 8, 16 and 28, the sizes of the slides',
      np.allclose(half, [0.817, 0.517, 0.380, 0.313], atol=0.001) and all(np.diff(half) < 0)
      and all(np.diff(width) < 0), ([round(t, 3) for t in half], [round(w_, 3) for w_ in width]))
src_h = open(os.path.join(HERE, '..', '..', 'figures', 'session10', 'igt_hist.py')).read()
check('the caption of igt_hist: the run has 500 + 1500 x 2 = 3500 sweeps of 512 tries, read in igt_hist.py',
      'L, NTH, NS, EVERY = 16, 500, 1500, 2' in src_h and 500 + 1500 * 2 == 3500 and 2 * 16 * 16 == 512, 3500)
check('the caption of igt_hist: 3500 x 512 x e^-20 = 0.0037, about 0.004 accepted flips',
      round(3500 * 512 * np.exp(-20), 3) == 0.004, 3500 * 512 * np.exp(-20))
print('all checks of page 06b passed')
