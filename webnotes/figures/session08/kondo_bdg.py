"""Session 8, one mechanism for two gaps. The Kondo lattice (8.21) in one dimension, per spin, mixes the conduction
band with the flat f level, and the Bogoliubov-de Gennes Hamiltonian of Section 5.8 mixes the electron band with
its hole copy. Both are 2x2 Bloch Hamiltonians, diagonalized here with numpy."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

t, g, D = 1.0, 0.6, 0.5              # hopping, Kondo hybridization gamma_K, pairing Delta
k = np.linspace(-np.pi, np.pi, 401)
eps = -2 * t * np.cos(k)             # half filling, the Fermi level is at zero energy
kondo = np.array([np.linalg.eigvalsh([[e, g], [g, 0.0]]) for e in eps])
bdg = np.array([np.linalg.eigvalsh([[e, D], [D, -e]]) for e in eps])
gap_k = (kondo[:, 0].max(), kondo[:, 1].min())
gap_b = (bdg[:, 0].max(), bdg[:, 1].min())
assert np.isclose(gap_k[1] - gap_k[0], 2 * (np.sqrt(t ** 2 + g ** 2) - t), atol=1e-6)   # indirect gap, about g^2/t
assert np.isclose(gap_b[1] - gap_b[0], 2 * D, atol=1e-4)

fig, axs = style.plt.subplots(1, 2, figsize=(12.6 * style.CM, 5.8 * style.CM), sharey=True)
fig.subplots_adjust(wspace=0.32)
for ax, bands, bare, gap, title in (
        (axs[0], kondo, (eps, 0 * eps), gap_k, 'Kondo lattice'),
        (axs[1], bdg, (eps, -eps), gap_b, 'superconductor')):
    style.arrows(ax, xlabel=r'$k$', ylabel=r'$E$' if ax is axs[0] else None)
    ax.axhspan(*gap, color='#f6e7e4', lw=0, zorder=0)
    for y, col in zip(bare, (style.MUTED, style.BROKEN)):
        ax.plot(k, y, color=col, lw=1.1, ls=(0, (3, 2.5)))
    for n in range(2):
        ax.plot(k, bands[:, n], color=style.ACCENT, lw=1.8)
    ax.set_xlim(-np.pi, np.pi * 1.05); ax.set_ylim(-2.3, 2.6)
    style.label(ax, 0, 2.75, title, fontsize=9.5)
    ax.set_xticks([-np.pi, 0, np.pi]); ax.set_xticklabels([r'$-\pi$', r'$0$', r'$\pi$'])
    ax.tick_params(length=2.5, pad=2, labelsize=9.5)
style.label(axs[0], 0, -1.5, r'$c$', fontsize=9.5, color=style.MUTED)
style.label(axs[0], -2.75, 0.32, r'$f$', fontsize=9.5, color=style.BROKEN)
style.label(axs[1], 0, -1.5, r'$e$', fontsize=9.5, color=style.MUTED)
style.label(axs[1], 0, 1.5, r'$h$', fontsize=9.5, color=style.BROKEN)
style.label(axs[0], np.pi * 1.08, 0.0, 'gap', fontsize=9.5, color=style.BROKEN, ha='left')
style.label(axs[1], np.pi * 1.08, 0.0, r'$2\Delta$', fontsize=9.5, color=style.BROKEN, ha='left')
style.save(fig, __file__)
