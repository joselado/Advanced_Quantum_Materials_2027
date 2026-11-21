"""Shared code of the picture options of the quiz of Section 3.9c, the curve d(k) = t + t' exp(ik) in the complex plane.

t is the intracell hopping and t' the intercell one, so the curve is a circle of radius t' with its center at (t, 0),
and it encloses the origin when t < t'. It is a formula and no calculation, so there is no pyqula script. The numbers
that the feedback quotes are the gap 2|t - t'|, the winding number, and the levels closest to zero of an open chain of
40 sites that starts and ends with the bond t, and they are checked here. A picture has its axes, the curve with an
arrow in the direction of increasing k and the origin as a dot, and no other text. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style


def numbers(t, tp, L=40):
    """The gap, the winding number of d(k) around the origin and the two smallest |E| of the open chain of L sites."""
    k = np.linspace(0, 2 * np.pi, 4001)
    d = t + tp * np.exp(1j * k)
    phase = np.unwrap(np.angle(d))
    H = np.zeros((L, L))
    for i in range(L - 1):
        H[i, i + 1] = H[i + 1, i] = t if i % 2 == 0 else tp
    low = np.sort(np.abs(np.linalg.eigvalsh(H)))
    return 2 * np.abs(d).min(), int(round((phase[-1] - phase[0]) / (2 * np.pi))), low[0], low[2]


def option(script, t, tp, winding, lowest):
    """One picture option. winding and lowest are the numbers of the feedback, checked here."""
    gap, w, e0, e2 = numbers(t, tp)
    print(os.path.basename(script), 't', t, "t'", tp, 'gap', round(gap, 4), 'winding', w, 'lowest |E|', e0, 'next', round(e2, 4))
    assert abs(gap - 1) < 1e-6 and abs(gap - 2 * abs(t - tp)) < 1e-6 and w == winding
    assert abs(e0 - lowest) < 0.06 * lowest, (e0, lowest)
    k = np.linspace(0, 2 * np.pi, 400)
    d = t + tp * np.exp(1j * k)
    fig, ax = plt.subplots(figsize=(3.7 * style.CM, 3.9 * style.CM))
    ax.axhline(0, color=style.GRID, lw=0.8, zorder=0); ax.axvline(0, color=style.GRID, lw=0.8, zorder=0)
    ax.plot(d.real, d.imag, color=style.ACCENT, lw=1.6)
    j = 100                                                         # the arrow at k = pi/2, at the top of the circle
    ax.annotate('', xy=(d.real[j + 4], d.imag[j + 4]), xytext=(d.real[j - 4], d.imag[j - 4]),
                arrowprops=dict(arrowstyle='-|>', color=style.ACCENT, lw=1.6, mutation_scale=9, shrinkA=0, shrinkB=0))
    ax.plot([0], [0], 'o', color=style.BROKEN, ms=4.5, mew=0, zorder=5)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-0.75, 3.75); ax.set_ylim(-2.25, 2.25)
    ax.set_xticks([0, 1, 2, 3]); ax.set_xticklabels(['0', '1', '2', '3'], fontsize=11)
    ax.set_yticks([-2, -1, 0, 1, 2]); ax.set_yticklabels(['$-2$', '$-1$', '0', '1', '2'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'Re $d$', fontsize=12, labelpad=0); ax.set_ylabel(r'Im $d$', fontsize=12, labelpad=-6)
    style.save(fig, script)
