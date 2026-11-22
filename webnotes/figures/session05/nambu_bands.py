"""Session 5, section 5.8, the electron and the hole band of the Nambu doubling of a chain, and the gap that pairing opens at
their crossing.

The data come from the downloadable script webnotes/scripts/session05/g2_nambu_chain.py, which calls pyqula. The chain has the
band eps(k) = -2t cos k - mu of the notes with t=1 (tij=[-1.] in pyqula) and mu=-1 (add_onsite(1.0), since add_onsite(x) is
mu=-x), so the Fermi points are at k = +-pi/3. Panel (a) has Delta=0 and panel (b) the s-wave Delta=0.45 of add_swave. The color
is the electron weight of each state, which in (b) is u^2 = (1 + eps/E)/2 on the upper branch, 1/2 at the Fermi points."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import _g2_bdg as b
style = b.style

d = style.run_script('session05/g2_nambu_chain.py')
k = 2 * np.pi * np.array(d['kpath'])[:, 0]
t, mu, D = 1.0, -1.0, 0.45
eps = -2 * t * np.cos(k) - mu
E = np.sqrt(eps**2 + D**2)
kF = np.arccos(-mu / (2 * t))
assert abs(kF - np.pi / 3) < 1e-12
e0, w0 = d['energies'][0], d['weights'][0]
e1, w1 = d['energies'][1], d['weights'][1]
for e, w in ((e0, w0), (e1, w1)):
    b.check(e, w)
# (a) the electron band eps and the hole band -eps, which cross at the Fermi points
assert np.allclose(np.sort(np.c_[eps, eps, -eps, -eps], axis=1), e0, atol=1e-9)
up =np.abs(eps) > 1e-6
assert np.allclose(w0[up, 2], (eps[up] > 0).astype(float), atol=1e-9)          # the upper band is the electron where eps>0
# (b) the spectrum (5.9), the smallest |E| = Delta at the Fermi points, the gap 2 Delta = 0.9, the weight u^2 of the upper branch
assert np.allclose(e1[:, 2], E, atol=1e-9) and abs(d['smallest'][1] - D) < 1e-9 and abs(d['smallest'][0]) < 1e-9
assert np.allclose(w1[:, 2], 0.5 * (1 + eps / E), atol=1e-9)
iF = np.argmin(np.abs(k - kF))
assert abs(k[iF] - kF) < 1e-9 and abs(w1[iF, 2] - 0.5) < 1e-9 and abs(2 * e1[iF, 2] - 0.9) < 1e-9
assert abs(e0[:, 3].max() - 3) < 1e-9 and abs(e0[:, 0].min() + 3) < 1e-9        # the bands reach +-3
print('Fermi points', round(kF, 4), 'smallest |E|', np.round(d['smallest'], 4), 'gap', round(2 * e1[iF, 2], 4),
      'u^2 at kF', round(w1[iF, 2], 4))

plt.rcParams.update({'font.size': 11.5})
fig, axs = plt.subplots(1, 2, figsize=(12.6 * style.CM, 5.6 * style.CM), sharey=True,
                        gridspec_kw=dict(wspace=0.22))
kt = [(-np.pi, r'$-\pi$'), (-np.pi / 3, r'$-\frac{\pi}{3}$'), (0, '0'), (np.pi / 3, r'$\frac{\pi}{3}$'), (np.pi, r'$\pi$')]
et = [(-3, '$-3$'), (-D, '$-0.45$'), (D, '$0.45$'), (3, '$3$')]
for ax, e, w, tag in ((axs[0], e0, w0, r'(a) $\Delta=0$'), (axs[1], e1, w1, r'(b) $\Delta=0.45$')):
    style.guide(ax, y=0)
    b.bands(ax, k, e, w)
    ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-3.4, 3.4)
    b.frame(ax, kt, et, r'$k$', r'$E/t$' if ax is axs[0] else None)
    ax.text(0, 3.75, tag, ha='center', va='bottom', fontsize=11.5)
for s in (-1, 1):
    axs[0].plot([s * kF], [0], 'o', color=style.INK, ms=3.2, zorder=5)
    axs[1].annotate('', xy=(s * kF, D), xytext=(s * kF, -D),
                    arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.8, shrinkA=0, shrinkB=0))
axs[1].text(kF + 0.22, 0,r'$2|\Delta|$', ha='left', va='center', fontsize=11.5)
b.colorbar(fig, list(axs), fontsize=11)
style.save(fig, __file__)
