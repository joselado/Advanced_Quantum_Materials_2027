"""Session 5, section 5.9, the minimum of the quasiparticle energy is |Delta| at the Fermi momentum, for any chemical potential.

The data come from the downloadable script webnotes/scripts/session05/g2_swave_chain_mu.py, which calls pyqula. The chain has the
band eps(k) = -2t cos k - mu of the notes with t=1 (tij=[-1.]), the chemical potential mu (add_onsite(-mu)) and the s-wave
Delta=0.3. E(k) is the positive branch of (5.9), the smallest |E| at each k, for mu = -1.2, 0 and 1.2. The Fermi momenta are
arccos(-mu/2t) = 0.927, 1.571 and 2.214."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

d = style.run_script('session05/g2_swave_chain_mu.py')
k = 2 * np.pi * np.array(d['kpath'])[:, 0]
t, D = 1.0, 0.3
cols = [style.ACCENT, style.BROKEN, style.LIGHT]
kFs = []
for mu, E in zip(d['mus'], d['energies']):
    eps = -2 * t * np.cos(k) - mu
    assert np.allclose(E, np.sqrt(eps**2 + D**2), atol=1e-9)              # (5.9) with the band of the notes
    kF = np.arccos(-mu / (2 * t))
    i = np.argmin(E)
    assert abs(E[i] - D) < 1e-4 and abs(k[i] - kF) < 0.01                   # the minimum is |Delta|, at k_F
    kFs.append(kF)
assert np.allclose(kFs, [0.927, 1.571, 2.214], atol=5e-4) and np.allclose(d['gaps'], D, atol=1e-4)
print('k_F', np.round(kFs, 3), 'minimum of E', np.round(d['gaps'], 4))

plt.rcParams.update({'font.size': 11})
fig, ax = plt.subplots(figsize=(10.4 * style.CM, 5.8 * style.CM))
for mu, E, kF, col in zip(d['mus'], d['energies'], kFs, cols):
    style.guide(ax, x=kF, color=col, lw=0.7, ls=(0, (3, 2)))
    ax.plot(k, E, color=col, lw=1.9)
    ax.plot([kF], [D], 'o', color=col, ms=4, zorder=5)
style.guide(ax, y=D, color=style.MUTED, lw=0.8, ls=(0, (3, 2)))
for kF, s, col in zip(kFs, (r'$\mu=-1.2t$', r'$\mu=0$', r'$\mu=1.2t$'), cols):
    ax.text(kF, 0.14, s, color=col, fontsize=10.5, ha='center', va='center', zorder=6,
            bbox=dict(boxstyle='square,pad=0.08', fc='white', ec='none'))
ax.set_xlim(0, np.pi); ax.set_ylim(0, 1.75)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
ax.set_xticks([0] + kFs + [np.pi]); ax.set_xticklabels(['0', '0.93', '1.57', '2.21', r'$\pi$'], fontsize=11)
for lab, col in zip(ax.get_xticklabels()[1:4], cols):
    lab.set_color(col)
ax.set_yticks([0, D, 1]); ax.set_yticklabels(['0', '0.3', '1'], fontsize=11)
ax.tick_params(length=2.5, width=0.6, pad=2)
ax.set_xlabel(r'$k$', fontsize=11.5, labelpad=1); ax.set_ylabel(r'$E/t$', fontsize=11.5, labelpad=2)
style.save(fig, __file__)
