"""Session 5, the pair function of a chain in real space, for three pairings that differ in their parity in k.

The real-space amplitude Delta(r), with r the distance between the two paired electrons, is the Fourier transform
Delta(r) = (1/N) sum_k Delta(k) e^{ikr}, computed with an FFT on a ring of N=64 sites, for
Delta(k) = Delta0 (onsite s-wave), 2 Delta0 cos k (extended s-wave) and 2i Delta0 sin k (p-wave, as in (5.20)).
An even Delta(k) gives an even Delta(r), and an odd one gives an odd Delta(r) that vanishes at r=0. The amplitudes
and their checks are in _g3_pairfun.py, which the picture options of the quiz of Section 5.11 also use. Redrawn on
2026-11-21 with the axis Delta(r)/Delta0 and its ticks, which the old figure did not have.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g3_pairfun as pf
from _g3_pairfun import style, plt

assert pf.N == 64                                        # the ring of the caption
FS = 12
fig, axs = plt.subplots(1, 3, figsize=(13.0 * style.CM, 4.9 * style.CM), gridspec_kw=dict(wspace=0.32))
for i, (ax, name) in enumerate(zip(axs, ('onsite', 'extended', 'pwave'))):
    vals = pf.amplitude(name)
    _, form, title, par = pf.CASES[name]
    pf.stems(ax, vals, FS)
    pf.frame(ax, FS, yname=(i == 0))
    ax.set_xticks([-2, 0, 2]); ax.set_xticklabels(['$-2$', '0', '2'], fontsize=FS - 1)
    ax.set_title(title + ', ' + form, fontsize=FS - 0.5, pad=4)
    style.label(ax, -2.2, -0.95, par, fontsize=FS - 1, color=style.MUTED)
style.save(fig, __file__)
