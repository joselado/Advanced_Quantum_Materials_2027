"""Session 8, Section 8.13, one mechanism for two gaps. The Kondo lattice (8.21) on a chain, per spin, mixes the
conduction band with the flat f level, and the Bogoliubov-de Gennes Hamiltonian of Section 5.8 mixes the electron band
with its hole copy. Both are 2x2 Bloch Hamiltonians.

The data come from the downloadable script webnotes/scripts/session08/g4_kondo_and_swave_chain.py, which calls pyqula on
a chain with tij=[-1.], so the band is -2t cos k with t=1 and its minimum at k=0, half filled at zero energy. The Kondo
half is H2HFH(h, JK=0.6), with JK the hybridization gamma_K of (8.21), and the superconducting half is add_swave(0.5),
whose gap 2 Delta = 1 the conventions sheet of the session confirms. The asserts are the numbers of the caption."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import _g4_kondo as kd
style = kd.style

d = style.run_script('session08/g4_kondo_and_swave_chain.py')
t, g, D = 1.0, d['gamma'], d['delta']
assert (g, D) == (0.6, 0.5)
k = 2 * np.pi * np.array(d['kpath'])[:, 0]
eps = -2 * t * np.cos(k)
k0, k1 = d['kondo']
s0, s1 = d['swave']
c = k0[:, 0] + k0[:, 3]                                    # with no mixing: the c band, and the f level at zero
assert np.allclose(c, eps, atol=1e-12) and np.argmin(c) == 100 and abs(c[100] + 2) < 1e-12
assert np.allclose(np.sort(np.c_[c, c, 0 * c, 0 * c], axis=1), k0, atol=1e-12)
assert np.allclose(np.sort(np.c_[eps, eps, -eps, -eps], axis=1), s0, atol=1e-12)      # the electron band and its hole copy
lo, up = kd.bands_formula(eps, g)
assert np.allclose(k1[:, 1], lo, atol=1e-9) and np.allclose(k1[:, 2], up, atol=1e-9)
E = np.sqrt(eps ** 2 + D ** 2)
assert np.allclose(s1[:, 1], -E, atol=1e-9) and np.allclose(s1[:, 2], E, atol=1e-9)
gap_k = (k1[:, 1].max(), k1[:, 2].min())
gap_b = (s1[:, 1].max(), s1[:, 2].min())
assert abs(d['gap_kondo'] - 2 * (np.sqrt(t ** 2 + g ** 2) - t)) < 1e-9 and abs(round(d['gap_kondo'], 2) - 0.33) < 1e-9
assert abs(g ** 2 / t - 0.36) < 1e-12 and abs(g ** 2 / t / d['gap_kondo'] - 1) < 0.1    # gamma^2/t within 10 percent
assert abs(d['gap_swave'] - 2 * D) < 1e-9 and abs(2 * D - 1) < 1e-12
assert np.argmax(k1[:, 1]) in (0, 200) and np.argmin(k1[:, 2]) == 100                  # top at k=pi, bottom at k=0
print('Kondo indirect gap %.4f, gamma^2/t %.2f, superconducting gap %.4f' % (d['gap_kondo'], g ** 2 / t, d['gap_swave']))

plt.rcParams.update({'font.size': 11})
fig, axs = plt.subplots(1, 2, figsize=(12.6 * style.CM, 5.8 * style.CM), sharey=True, gridspec_kw=dict(wspace=0.32))
for ax, bands, bare, gap, title in (
        (axs[0], k1, (eps, 0 * eps), gap_k, 'Kondo lattice'),
        (axs[1], s1, (eps, -eps), gap_b, 'superconductor')):
    style.arrows(ax, xlabel=r'$k$', ylabel=r'$E/t$' if ax is axs[0] else None)
    ax.axhspan(*gap, color='#f6e7e4', lw=0, zorder=0)
    for y, col in zip(bare, (style.MUTED, style.BROKEN)):
        ax.plot(k, y, color=col, lw=1.1, ls=(0, (3, 2.5)))
    for n in (1, 2):
        ax.plot(k, bands[:, n], color=style.ACCENT, lw=1.8)
    ax.set_xlim(-np.pi, np.pi * 1.05); ax.set_ylim(-2.3, 2.6)
    style.label(ax, 0, 2.75, title, fontsize=10.5)
    kd.ticks(ax, kd.KTICKS, [(-2, r'$-2$'), (-1, r'$-1$'), (0, r'$0$'), (1, r'$1$'), (2, r'$2$')], fontsize=10)
    if ax is not axs[0]:
        ax.tick_params(axis='y', left=False, labelleft=False)
style.label(axs[0], 0, -1.5, r'$c$', fontsize=10.5, color=style.MUTED)
style.label(axs[0], -2.75, 0.32, r'$f$', fontsize=10.5, color=style.BROKEN)
style.label(axs[1], 0, -1.5, r'$e$', fontsize=10.5, color=style.MUTED)
style.label(axs[1], 0, 1.5, r'$h$', fontsize=10.5, color=style.BROKEN)
style.label(axs[0], np.pi * 1.08, 0.0, r'$0.33$', fontsize=10.5, color=style.BROKEN, ha='left')
style.label(axs[1], np.pi * 1.08, 0.0, r'$2\Delta$', fontsize=10.5, color=style.BROKEN, ha='left')
style.save(fig, __file__)
