"""Session 5, the pair function of a chain in real space, for three pairings that differ in their parity in k.

The real-space amplitude Delta(r), with r the distance between the two paired electrons, is the Fourier transform
Delta(r) = (1/N) sum_k Delta(k) e^{ikr}, computed with an FFT on a ring of N sites, for
Delta(k) = Delta0 (onsite s-wave), 2 Delta0 cos k (extended s-wave) and 2i Delta0 sin k (p-wave, as in (5.20)).
An even Delta(k) gives an even Delta(r), and an odd one gives an odd Delta(r) that vanishes at r=0.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

N = 64
k = 2 * np.pi * np.fft.fftfreq(N)
cases = [(np.ones(N, complex), r'$\Delta_0$', 'onsite $s$', 'even'),
         (2 * np.cos(k) + 0j, r'$2\Delta_0\cos k$', 'extended $s$', 'even'),
         (2j * np.sin(k), r'$2i\Delta_0\sin k$', '$p$-wave', 'odd')]
R = np.arange(-3, 4)

FS = 12
style.plt.rcParams['font.size'] = FS          # labels of the arrows too, for a phone
fig, axs = plt.subplots(1, 3, figsize=(13.0 * style.CM, 4.8 * style.CM), gridspec_kw=dict(wspace=0.18))
for ax, (dk, form, name, par) in zip(axs, cases):
    dr = np.fft.ifft(dk)                              # (1/N) sum_k Delta(k) e^{ikr}
    vals = np.array([dr[r % N] for r in R])
    assert np.allclose(vals.imag, 0, atol=1e-12)
    vals = vals.real
    sgn = 1 if par == 'even' else -1
    assert np.allclose(vals, sgn * vals[::-1], atol=1e-12)     # Delta(-r) = +-Delta(r), as Delta(-k) = +-Delta(k)
    if par == 'odd':
        assert abs(vals[3]) < 1e-12                           # no amplitude at r=0
    ax.axis('off')
    ax.annotate('', xy=(3.75, 0), xytext=(-3.5, 0), arrowprops=dict(arrowstyle='-|>', color=style.INK, lw=0.7, mutation_scale=7, shrinkA=0, shrinkB=0))
    style.label(ax, 3.85, 0, '$r$', ha='left', fontsize=FS)
    for r, val in zip(R, vals):
        if abs(val) > 1e-9:
            c = style.ACCENT if val > 0 else style.BROKEN
            ax.plot([r, r], [0, val], color=c, lw=2.2)
            ax.plot(r, val, 'o', color=c, ms=5.5)
        else:
            ax.plot(r, 0, 'o', color=style.MUTED, ms=3, mfc='white', mew=0.9)
    ax.set_xlim(-3.6, 4.1); ax.set_ylim(-1.35, 1.5)
    for r in (-2, 0, 2):
        style.label(ax, r, -0.2, '$%d$' % r, fontsize=FS - 1, va='top')
    style.label(ax, 0, 1.95, name, fontsize=FS)
    style.label(ax, 0, 1.62, form, fontsize=FS - 0.5, color=style.MUTED)
    style.label(ax, -2.2, -1.0, par, fontsize=FS, color=style.INK)
style.save(fig, __file__)
