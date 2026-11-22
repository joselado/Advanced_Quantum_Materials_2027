"""Session 10, feedback of a quiz of Section 10.7, the chains with t=1 and t=-1 have bands that are upside down with
respect to each other and the same density of states.

The calculation is the pyqula script webnotes/scripts/session10/g5_chain_sign_dos.py, the band of h.get_bands on a
k-path and the density of states per site of h.get_dos(mode="Green", delta=1e-3), spinless, for tij=[-1.] (t=1) and
tij=[1.] (t=-1). The figure is a quiz feedback, so it has no button. Energies are in units of |t|, the momentum in
units of the inverse lattice constant. Left, the two bands against k on one zone, right, the two densities of states
against the same energy axis, with the closed form 1/(pi sqrt(4 t^2 - E^2)) checked inside the band."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

d = style.run_script('session10/g5_chain_sign_dos.py')
k, bands, dos, E = d['k'], d['bands'], d['dos'], np.asarray(d['energies'])
b1, bm = np.asarray(bands[1.]), np.asarray(bands[-1.])
D1, Dm = np.asarray(dos[1.]), np.asarray(dos[-1.])
# the sign of pyqula: tij=[-1.] is -2t cos k with t=1, tij=[1.] is +2 cos k, the band of t=-1, of width 4|t|
assert np.abs(b1 + 2 * np.cos(k)).max() < 1e-12 and np.abs(bm - 2 * np.cos(k)).max() < 1e-12
assert abs(b1.max() - b1.min() - 4) < 1e-9 and abs(k[0] + np.pi) < 1e-12 and abs(k[-1] - np.pi) < 1e-12
# the two densities of states are the same, and they are 1/(pi sqrt(4 - E^2)) per site inside the band
assert np.abs(D1 - Dm).max() < 1e-12
inside = np.abs(E) < 1.9
closed = 1 / (np.pi * np.sqrt(4 - E[inside] ** 2))
assert np.abs(D1[inside] / closed - 1).max() < 1e-4
i0 = np.argmin(np.abs(E))
assert abs(E[i0]) < 1e-12 and abs(D1[i0] - 0.159) < 5e-4
print('largest |band + 2 cos k| %.1e, density of states at E=0 %.4f, largest relative deviation inside %.1e'
      % (np.abs(b1 + 2 * np.cos(k)).max(), D1[i0], np.abs(D1[inside] / closed - 1).max()))

fig, axs = style.plt.subplots(1, 2, figsize=(9.6 * style.CM, 5.0 * style.CM), gridspec_kw=dict(wspace=0.42))
a, b = axs
a.plot(k, b1, color=style.ACCENT, lw=1.8)
a.plot(k, bm, color=style.BROKEN, lw=1.3, ls=(0, (4, 2)))
style.arrows(a, xlabel=r'$k$', ylabel=r'$E/|t|$', ticks=True)
a.set_xlim(-np.pi, np.pi); a.set_ylim(-2.6, 2.6)
a.set_xticks([-np.pi, 0, np.pi]); a.set_xticklabels([r'$-\pi$', '0', r'$\pi$'])
a.set_yticks([-2, 0, 2]); a.set_yticklabels(['$-2$', '0', '2'])
style.label(a, 0, -2.25, r'$t=1$', color=style.ACCENT, fontsize=9)
style.label(a, 0, 2.25, r'$t=-1$', color=style.BROKEN, fontsize=9)
band = np.abs(E) < 2     # the tails of the broadening outside the band are not drawn
assert D1[np.abs(E) > 2.05].max() < 0.01
b.plot(D1[band], E[band], color=style.ACCENT, lw=2.6)
b.plot(Dm[band], E[band], color=style.BROKEN, lw=1.1, ls=(0, (4, 2)))
style.arrows(b, xlabel=r'$D\,|t|$', ylabel=r'$E/|t|$', ticks=True)
b.set_xlim(0, 0.8); b.set_ylim(-2.6, 2.6)
b.set_xticks([0, 0.4, 0.8]); b.set_xticklabels(['0', '0.4', '0.8'])
b.set_yticks([-2, 0, 2]); b.set_yticklabels(['$-2$', '0', '2'])
for ax in axs:
    ax.tick_params(length=2.5, width=0.6, pad=2)
style.save(fig, __file__)
