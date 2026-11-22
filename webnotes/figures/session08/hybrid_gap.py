"""Session 8, quiz of Section 8.13, the two bands of (8.21) per spin on a chain for gamma_K = 0.5 t and gamma_K = t,
with the direct gap 2 gamma_K at the crossing.

The data come from the downloadable script webnotes/scripts/session08/g4_kondo_chain_bands.py, which calls pyqula with
tij=[-1.], so the conduction band is -2t cos k with t=1, and H2HFH(h, JK=gamma_K). The asserts of _g4_kondo.check_chain
give the bands, the crossing at k = +-pi/2 and the direct gaps 1 and 2, which are drawn as the arrows."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import _g4_kondo as kd
style = kd.style

d = style.run_script('session08/g4_kondo_chain_bands.py')
k = kd.check_chain(d)
res = {}
for g in (0.5, 1.0):
    i = d['gammas'].index(g)
    e = d['energies'][i]
    res[g] = e[50, 2] - e[50, 1]
    assert abs(res[g] - 2 * g) < 1e-9 and abs(d['direct'][i] - 2 * g) < 1e-9            # direct gap 2 gamma at k=-pi/2
assert abs(res[1.0] / res[0.5] - 2) < 1e-9
print('direct gaps at the crossing', res)

plt.rcParams.update({'font.size': 11})
fig, axs = plt.subplots(1, 2, figsize=(9.5 * style.CM, 5.0 * style.CM), sharey=True, gridspec_kw=dict(wspace=0.25))
for ax, g, col in zip(axs, (0.5, 1.0), (style.ACCENT, style.BROKEN)):
    style.arrows(ax, xlabel=r'$k$', ylabel=r'$E/t$' if ax is axs[0] else None)
    e = d['energies'][d['gammas'].index(g)]
    style.guide(ax, y=0)
    for b in (1, 2):
        ax.plot(k, e[:, b], color=col, lw=1.6)
    ax.annotate('', xy=(k[50], e[50, 2]), xytext=(k[50], e[50, 1]),
                arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.9, shrinkA=0, shrinkB=0))
    ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-2.6, 2.6)
    kd.ticks(ax, kd.KTICKS, [(-2, r'$-2$'), (-1, r'$-1$'), (0, r'$0$'), (1, r'$1$'), (2, r'$2$')], fontsize=10)
    if ax is not axs[0]:
        ax.tick_params(axis='y', left=False, labelleft=False)
    ax.text(0, 2.75, r'$\gamma_K=%g\,t$' % g if g != 1 else r'$\gamma_K=t$', ha='center', va='bottom', fontsize=10.5)
    for t in ax.texts:
        t.set_fontsize(10.5)
style.save(fig, __file__)
