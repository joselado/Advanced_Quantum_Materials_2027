"""Session 1, the dispersion of the quasiparticle of each broken symmetry, with and without a gap.

Closed forms, so numpy and no script to download: the phonon of a chain of masses, omega = 2|sin(k/2)|, the magnon of
a ferromagnetic chain, omega = 1 - cos k, with the gap 0.45 of an easy-axis anisotropy added to it, and the amplitude
(Higgs) mode, omega = sqrt(1.2^2 + k^2). The momentum k is in units of the inverse lattice constant, omega in
arbitrary units, the same in the three panels. The ticks are at the values that the caption quotes, and the asserts
check them.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style

FS = 12
k = np.linspace(-np.pi, np.pi, 501)
J, Da, Dg = 1.0, 0.45, 1.2
phonon = 2 * np.abs(np.sin(k / 2))
magnon = J * (1 - np.cos(k))
higgs = np.sqrt(Dg ** 2 + k ** 2)
i0 = np.argmin(np.abs(k))
assert k[i0] == 0 and phonon[i0] == 0 and magnon[i0] == 0          # the phonon and the magnon reach zero at k = 0
assert np.isclose((magnon + Da).min(), 0.45) and np.isclose(higgs.min(), 1.2)   # the two gaps of the caption
assert np.isclose(phonon.max(), 2) and np.isclose(magnon.max(), 2)

fig, axs = style.figure(height_cm=5.6, ncols=3)
YL = (-0.1, 3.7)


def panel(a, title, yticks, ylabels):
    style.arrows(a, xlabel=r'$k$', ylabel=r'$\omega$', ticks=True)
    for t in a.texts:
        t.set_fontsize(FS + 1)                                   # the names of the axes, readable at 390 px
    a.set_xlim(-np.pi, np.pi); a.set_ylim(*YL)
    a.set_xticks([-np.pi, 0, np.pi]); a.set_xticklabels([r'$-\pi$', '0', r'$\pi$'])
    a.set_yticks(yticks); a.set_yticklabels(ylabels)
    a.tick_params(labelsize=FS, length=2.5, width=0.6, pad=2)
    a.minorticks_off()
    style.guide(a, y=0)
    a.set_title(title, fontsize=FS, pad=12)


# (a) phonon of a chain of masses, gapless
a = axs[0]
a.plot(k, phonon, color=style.ACCENT)
panel(a, 'phonon', [0, 2], ['0', '2'])
# (b) magnon of a ferromagnetic chain, and the same with the gap of an easy-axis anisotropy
a = axs[1]
a.plot(k, magnon, color=style.ACCENT)
a.plot(k, magnon + Da, color=style.BROKEN)
panel(a, 'magnon', [0, Da, 2], ['0', '0.45', '2'])
style.label(a, 0.0, 3.3, "with anisotropy", color=style.BROKEN, fontsize=FS - 1)
a.annotate('', xy=(0, Da), xytext=(0, 0), arrowprops=dict(arrowstyle='<->', color=style.BROKEN, lw=0.8, shrinkA=0, shrinkB=0))
# (c) amplitude (Higgs) mode of a superconductor, gapped
a = axs[2]
a.plot(k, higgs, color=style.ACCENT)
panel(a, 'Higgs mode', [0, Dg], ['0', '1.2'])
a.annotate('', xy=(0, Dg), xytext=(0, 0), arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.8, shrinkA=0, shrinkB=0))
style.label(a, 0.2, 0.55, "gap", color=style.INK, ha="left", fontsize=FS - 1)
fig.subplots_adjust(wspace=0.42)
style.save(fig, __file__)
