"""Figure s09f05, fig:s09:decay: power law against exponential, the induced moments near an impurity.

Two renders. Left, two chains of sixteen sites, an impurity (a dark ball) at the left end, and the
induced moment on site n as an arrow of length proportional to (-1)^n times the envelope, with the
envelope as a ghost tube: (a) behind, the S = 1/2 chain, 1/n; (b) in front, the S = 1 chain,
exp(-n / xi) with xi = 2.5. Right, seen from the front: (c) the two envelopes on a logarithmic
vertical scale, log10 of 1/n and of exp(-n/xi) against n, the exponential a straight line.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's09f05_decay'
N, STEP, XI = 16, 0.62, 2.5


def build_chains():
    F.studio()
    for row, (y, env, tag) in enumerate(((3.6, lambda n: 1 / n, 'a'), (0.0, lambda n: math.exp(-(n - 1) / XI), 'b'))):
        xs = [-5.0 + i * STEP for i in range(N + 1)]
        F.ball(f'{tag}_imp', (xs[0], y, 0.25), 0.25, rgb=F.SITE)
        for n in range(1, N + 1):
            x = xs[n]
            F.site(f'{tag}_s{n}', (x, y, 0), r=0.17, h=0.05)
            if n < N:
                F.bond(f'{tag}_b{n}', (x + 0.17, y, 0.04), (xs[n + 1] - 0.17, y, 0.04), r=0.02)
            m = env(n) * (1 if n % 2 else -1)
            L = max(0.08, 1.0 * abs(m))
            F.sz_arrow(f'{tag}_a{n}', (x, y, 0.1 + L / 2 if m > 0 else 0.1 + L / 2), (0, 0, 1 if m > 0 else -1), length=L)
        F.tube(f'{tag}_env', [(xs[1] + (xs[N] - xs[1]) * j / 200, y + 0.25, 0.1 + 1.0 * env(1 + (N - 1) * j / 200)) for j in range(201)],
               0.02, F.BOND, alpha=0.5)
        F.anchor(f'{tag}panel', (xs[0] - 0.45, y, 1.5))
        F.anchor(f'{tag}env', (xs[4], y + 0.25, 0.75))
    F.camera((0.0, 1.8, 0.6), elev=24.0, ortho=11.2, aspect=10.0 / 4.6)


def build_log():
    F.studio()
    sx, sz, z0 = 0.27, 1.25, 3.9                # the n axis at 10^-3 sits just above the floor
    P = lambda n, v: (-2.2 + sx * n, 0, z0 + sz * v)
    ns = [1 + (N - 1) * j / 200 for j in range(201)]
    F.tube('pl', [P(n, math.log10(1 / n)) for n in ns], 0.035, F.ACCENT_AQM)
    F.tube('ex', [P(n, math.log10(math.exp(-(n - 1) / XI))) for n in ns], 0.035, F.BROKEN)
    F.axis('ax', P(0, -3.0), P(N + 1.5, -3.0), r=0.016, head=0.13)
    F.axis('ay', P(0, -3.0), P(0, 0.4), r=0.016, head=0.13)
    for d in (0, -1, -2, -3):
        F.rod(f't{d}', P(0, d), P(-0.3, d), r=0.01)
        F.anchor(f'd{-d}', P(-0.3, d))
    F.anchor('n', P(N + 1.5, -3.0))
    F.anchor('y', P(0, 0.4))
    F.anchor('pl', P(N, math.log10(1 / N)))
    F.anchor('ex', P(7.5, math.log10(math.exp(-6.5 / XI))))
    F.anchor('panel', P(-1.0, 0.55))
    F.camera((-0.0, 0.0, 2.5), elev=3.0, ortho=5.3, aspect=5.4 / 4.6)


F.main_panels(NAME, [('chains', build_chains), ('log', build_log)])
