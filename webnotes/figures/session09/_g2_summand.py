"""Shared code of the picture options of the quiz of Section 9.4a on the summand of (9.4) for a chain.

The chain eps(k) = -2t cos k with t=1 at q=0.3 and T=0.01t. The question has k_F = pi/4, the Fermi level -sqrt2 t. The
three options are the summand S(k) = (n_F(eps(k)) - n_F(eps(k+q)))/(eps(k+q) - eps(k)) at k_F = pi/4 ('quarter', the right one),
the same summand at half filling, k_F = pi/2 ('half'), and the occupation n_F(eps(k)) at k_F = pi/4 ('occupation'), which is
one for |k| < pi/4. The axis is S(k) in units of 1/t. The windows of the summand, (k_F - q, k_F) and (-k_F - q, -k_F), and the numbers of the feedback are
asserted here. A summand is not an output of pyqula, so this is numpy, and the pictures have their axes and no other text.
This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

T, Q = 0.01, 0.3
assert Q == 0.3                                   # the q=0.3 of the question
K = np.linspace(-np.pi, np.pi, 1601)


def nF(e, mu):
    return 0.5 * (1 - np.tanh((e - mu) / (2 * T)))


def eps(k):
    return -2 * np.cos(k)


def summand(kF):
    mu = eps(kF)
    num, den = nF(eps(K), mu) - nF(eps(K + Q), mu), eps(K + Q) - eps(K)
    return np.where(np.abs(den) > 1e-12, num / np.where(np.abs(den) > 1e-12, den, 1), 0.0)


def windows(y, kF):
    """Checks that y is nonzero only in (kF - Q, kF) and (-kF - Q, -kF), up to the thermal rounding."""
    near = ((K > kF - Q - 0.08) & (K < kF + 0.08)) | ((K > -kF - Q - 0.08) & (K < -kF + 0.08))
    inside = ((K > kF - Q + 0.05) & (K < kF - 0.05)) | ((K > -kF - Q + 0.05) & (K < -kF - 0.05))
    assert np.all(y >= -1e-12) and y[~near].max() < 1e-3 and y[inside].min() > 1.0, (y[~near].max(), y[inside].min())


def curve(kind):
    kF = np.pi / 4
    if kind == 'quarter':
        y = summand(kF)
        windows(y, kF)
        mid = np.argmin(np.abs(K - (kF - Q / 2)))
        vF = 2 * np.sin(kF)
        assert abs(eps(kF) + np.sqrt(2)) < 1e-12 and abs(vF - np.sqrt(2)) < 1e-12
        assert abs(y[mid] - 1 / (vF * Q)) < 0.03 and f'{1 / (vF * Q):.1f}' == '2.4'     # about 2.4/t in the middle
        inner = ((K > kF - Q + 0.05) & (K < kF - 0.05)) | ((K > -kF - Q + 0.05) & (K < -kF - 0.05))
        assert y[inner].min() > 2.0 and f'{y.max():.1f}' == '2.7'                    # the alt text, 2 to 2.7
    elif kind == 'half':
        y = summand(np.pi / 2)
        windows(y, np.pi / 2)
        e1, e2 = eps(np.pi / 2 - Q / 2), eps(np.pi / 2 + Q / 2)                          # both above -sqrt2 t, so empty
        assert f'{e1:.2f}' == '-0.30' and f'{e2:.2f}' == '0.30' and min(e1, e2) > eps(kF)
        assert f'{y.max():.1f}' == '1.7'                                                 # the alt text
    else:
        y = nF(eps(K), eps(kF))
        assert abs(y[np.argmin(np.abs(K))] - 1) < 1e-12 and y[np.abs(K) > kF + 0.08].max() < 1e-3
        assert f'{eps(0):.2f}' == '-2.00' and f'{eps(Q):.2f}' == '-1.91' and eps(Q) < eps(kF)   # k=0 and k+q both filled
    return y


def option(script, kind):
    """One picture option with its axes and no other text, the same window and scale in the three pictures."""
    y = curve(kind)
    print(kind, 'largest value %.3f' % y.max())
    plt.rcParams.update({'font.size': 11})
    fig, ax = plt.subplots(figsize=(4.0 * style.CM, 3.9 * style.CM))
    kp, yp = K[::4], y[::4]                       # a coarser grid for the drawing, the checks use K
    ax.plot(kp, yp, color=style.BROKEN, lw=1.5, clip_on=False, zorder=4)
    ax.fill_between(kp, 0, yp, color=style.BROKEN, alpha=0.15, lw=0)
    ax.set_xlim(-np.pi, np.pi); ax.set_ylim(0, 3.0)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.spines['left'].set_linewidth(0.7); ax.spines['bottom'].set_linewidth(0.7)
    ax.set_xticks([-np.pi / 2, 0, np.pi / 2]); ax.set_xticklabels([r'$-\pi/2$', r'$0$', r'$\pi/2$'], fontsize=10.5)
    ax.set_yticks([0, 1, 2]); ax.set_yticklabels([r'$0$', r'$1$', r'$2$'], fontsize=10.5)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$k$', fontsize=12, labelpad=0); ax.set_ylabel(r'$S(k)$', fontsize=12, labelpad=1)
    style.save(fig, script)
