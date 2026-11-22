"""Session 4, section 4.16, two electrons in the Laughlin state, the probability of their distance.

For two electrons Psi = (z1 - z2)^m exp(-(|z1|^2 + |z2|^2)/4 l_B^2). With z1 = Z + r/2 and z2 = Z - r/2 this is
|Psi|^2 = |r|^(2m) exp(-|r|^2/4 l_B^2) exp(-|Z|^2/l_B^2), so the distance r = |z1 - z2| has the probability
P(r) dr proportional to r^(2m+1) exp(-r^2/4) dr, normalized to one, with a maximum at r = sqrt(2(2m+1)) l_B, which is
2.45, 3.74 and 4.69 l_B for m = 1, 3, 5. P is a probability per unit length, in units of 1/l_B.
The formula is checked below against a direct integral of |Psi|^2 over the plane of the center Z.
Redrawn on 2026-11-21 with the ticks of both axes and the unit of P, under the same name."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from math import factorial
import matplotlib.pyplot as plt
import style
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, so that they stay readable on a phone


def P(r, m):
    return r ** (2 * m + 1) * np.exp(-r ** 2 / 4) / (2 * 4 ** m * factorial(m))


# direct check: the weight of |Psi|^2 at the distance r, summed over the center Z on a grid
def weight(r, m):
    g = np.linspace(-8, 8, 801)
    X, Y = np.meshgrid(g, g)
    z1 = X + 1j * Y + r / 2; z2 = X + 1j * Y - r / 2
    return (np.abs(z1 - z2) ** (2 * m) * np.exp(-(np.abs(z1) ** 2 + np.abs(z2) ** 2) / 2)).sum() * (g[1] - g[0]) ** 2


rr = np.linspace(0, 40, 40001)
for m, peak in ((1, 2.45), (3, 3.74), (5, 4.69)):
    ratio = weight(3.0, m) / weight(2.0, m)
    assert abs(ratio - (3.0 ** (2 * m) * np.exp(-9 / 4)) / (2.0 ** (2 * m) * np.exp(-1))) < 1e-6 * ratio
    assert abs(np.trapezoid(P(rr, m), rr) - 1) < 1e-6                        # normalized to one
    assert abs(rr[np.argmax(P(rr, m))] - np.sqrt(2 * (2 * m + 1))) < 1e-3      # the maximum at sqrt(2(2m+1))
    assert round(np.sqrt(2 * (2 * m + 1)), 2) == peak                         # the ticks 2.45, 3.74, 4.69
    assert 0.40 < P(np.sqrt(2 * (2 * m + 1)), m) < 0.41                       # the peak height, under the tick 0.4

r = np.linspace(0, 10, 800)
fig, ax = style.figure(height_cm=5.0, width_cm=12)
ax.set_xlim(0, 10); ax.set_ylim(0, 0.5)
for m, col in ((1, style.WARM), (3, style.ACCENT), (5, style.BROKEN)):
    ax.plot(r, P(r, m), color=col)
    ax.vlines(np.sqrt(2 * (2 * m + 1)), 0, P(np.sqrt(2 * (2 * m + 1)), m), color=col, lw=0.8, ls=':')
style.label(ax, 1.6, 0.46, r'$m=1$', color=style.WARM, fontsize=11)
style.label(ax, 3.75, 0.46, r'$m=3$', color=style.ACCENT, fontsize=11)
style.label(ax, 5.9, 0.46, r'$m=5$', color=style.BROKEN, fontsize=11)
style.arrows(ax, xlabel=r'$|z_1-z_2|/\ell_B$', ylabel=r'probability of the distance, in units of $1/\ell_B$')
ax.set_xticks([0, 2.45, 3.74, 4.69, 10]); ax.set_xticklabels(['0', '2.45', '3.74', '4.69', '10'], fontsize=11)
ax.set_yticks([0, 0.2, 0.4]); ax.set_yticklabels(['0', '0.2', '0.4'], fontsize=11)
ax.tick_params(length=2.5, width=0.6, pad=2)
style.save(fig, __file__)
