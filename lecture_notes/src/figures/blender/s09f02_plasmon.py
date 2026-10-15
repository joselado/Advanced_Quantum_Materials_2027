"""Figure s09f02, fig:s09:plasmon: the particle-hole continuum and the plasmon, seen from the front.

The (q, omega) plane of the three-dimensional electron gas in units k_F = v_F = 1 and hbar^2 / 2m =
1/2, so omega_+ = q + q^2 / 2 and, beyond 2 k_F, omega_- = q^2 / 2 - q. The continuum is a translucent
slab between them (down to omega = 0 for q < 2). The plasmon omega = sqrt(omega_p^2 + (3/5) q^2), with
omega_p = 1.4, is a solid tube until it meets omega_+ and a dashed ghost after it, Landau damped.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's09f02_plasmon'
SX, SZ, X0, Z0 = 1.25, 0.78, -2.6, 0.35
WP = 1.4
QMAX, WMAX = 3.6, 4.2


def build():
    F.studio()
    P = lambda q, w: (X0 + SX * q, 0, Z0 + SZ * w)
    qs = [QMAX * j / 300 for j in range(301)]
    up = [min(q + q * q / 2, WMAX) for q in qs]
    lo = [max(0.0, q * q / 2 - q) for q in qs]
    keep = [i for i, (u, l) in enumerate(zip(up, lo)) if l < WMAX]
    F.profile('cont', [X0 + SX * qs[i] for i in keep], [Z0 + SZ * up[i] for i in keep], 0.12, F.ACCENT_AQM, alpha=0.18,
              lows=[Z0 + SZ * lo[i] for i in keep])
    F.tube('wplus', [P(q, q + q * q / 2) for q in qs if q + q * q / 2 <= WMAX], 0.02, F.ACCENT_AQM)
    F.tube('wminus', [P(q, q * q / 2 - q) for q in qs if q >= 2 and q * q / 2 - q <= WMAX], 0.02, F.ACCENT_AQM)
    pl = lambda q: math.sqrt(WP * WP + 0.6 * q * q)
    qc = next(q for q in qs if q + q * q / 2 >= pl(q))
    F.tube('plasmon', [P(q, pl(q)) for q in qs if q <= qc], 0.04, F.BROKEN)
    for k in range(6):                                  # the damped part, dashed
        a = qc + 0.12 * k * 2
        b = a + 0.12
        if pl(b) <= WMAX:
            F.tube(f'damped{k}', [P(a, pl(a)), P(b, pl(b))], 0.035, F.BROKEN, alpha=0.45)
    F.axis('ax', P(0, 0), P(QMAX + 0.3, 0), r=0.016, head=0.13)
    F.axis('ay', P(0, 0), P(0, WMAX + 0.3), r=0.016, head=0.13)
    F.anchor('q', P(QMAX + 0.3, 0))
    F.anchor('w', P(0, WMAX + 0.3))
    F.anchor('wp', P(0, WP))
    F.anchor('twokf', P(2, 0))
    F.anchor('plasmon', P(0.25, pl(0.25) + 0.05))
    F.anchor('cont', P(2.4, 1.6))
    F.anchor('window', P(0.08, 2.75))
    F.anchor('damped', P(qc + 1.25, pl(qc + 1.25) - 0.1))
    print('plasmon enters the continuum at q =', round(qc, 3))
    F.camera((X0 + SX * 1.85, 0, Z0 + SZ * 2.2), elev=3.0, ortho=6.4, aspect=1.6)


F.main(build, NAME)
