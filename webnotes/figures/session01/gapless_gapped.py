"""Session 1, the dispersion of the quasiparticle of each broken symmetry, with and without a gap."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style

fig, axs = style.figure(height_cm=4.8, ncols=3)
k = np.linspace(-np.pi, np.pi, 500)
# (a) phonon of a chain of masses, omega = 2 c |sin(k/2)|, gapless
a = axs[0]
a.plot(k, 2 * np.abs(np.sin(k / 2)), color=style.ACCENT)
style.arrows(a, xlabel=r'$k$', ylabel=r'$\omega$'); a.set_ylim(-0.1, 3.5); a.set_xlim(-np.pi, np.pi)
style.guide(a, y=0)
a.set_title('phonon', fontsize=8.5, pad=9)
# (b) magnon of a ferromagnetic chain, omega = J(1-cos k) + Delta, Delta from the anisotropy
a = axs[1]
J, Da = 1.0, 0.45
a.plot(k, J * (1 - np.cos(k)), color=style.ACCENT)
a.plot(k, J * (1 - np.cos(k)) + Da, color=style.BROKEN)
style.arrows(a, xlabel=r'$k$', ylabel=r'$\omega$'); a.set_ylim(-0.1, 3.5); a.set_xlim(-np.pi, np.pi)
style.guide(a, y=0)
a.set_title('magnon', fontsize=8.5, pad=9)
style.label(a, 2.3, 0.5, 'with\nanisotropy', color=style.BROKEN, fontsize=7.5)
a.annotate('', xy=(0, Da), xytext=(0, 0), arrowprops=dict(arrowstyle='<->', color=style.BROKEN, lw=0.8, shrinkA=0, shrinkB=0))
# (c) amplitude (Higgs) mode of a superconductor, omega = sqrt(Delta^2 + c^2 k^2), gapped
a = axs[2]
Dg = 1.2
a.plot(k, np.sqrt(Dg ** 2 + k ** 2), color=style.ACCENT)
style.arrows(a, xlabel=r'$k$', ylabel=r'$\omega$'); a.set_ylim(-0.1, 3.5); a.set_xlim(-np.pi, np.pi)
style.guide(a, y=0)
a.set_title('Higgs mode', fontsize=8.5, pad=9)
style.label(a, 0.0, 0.55, 'gap', color=style.INK, fontsize=8)
fig.subplots_adjust(wspace=0.3)
style.save(fig, __file__)
