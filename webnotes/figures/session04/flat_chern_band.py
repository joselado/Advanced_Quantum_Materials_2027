"""Session 4, section 4.20, a flat band with Chern number one at zero field, on the honeycomb lattice, computed with pyqula.

Redrawn on 2026-11-21 from the downloadable script webnotes/scripts/session04/g5_haldane_t3_bands.py, in place of the numpy model
_honeycomb.bloch, under the same name. Both panels have the first-neighbor hopping t=1 of pyqula and a second-neighbor hopping
t2 exp(i phi), along the path Gamma, K, M, Gamma. Panel (a) is the Haldane model of Section 3.10b, t2=0.1 and phi=pi/2, which is
h.add_haldane(0.1155) since pyqula takes the imaginary part times 2/sqrt(3). Panel (b) has t2=0.3, phi=0.4 pi and a third-neighbor
hopping t3=-0.2, which is tij=[1, 0.0927, -0.2] and h.add_haldane(0.3295). The lower band has C=+1 in both, from h.get_chern(),
which is the sign of the Berry curvature of the notes. Its width is 2.48 in (a), more than twice the gap 1.04, and 0.212 in (b),
14.0 times smaller than the gap 2.965. The grey strip is the gap, and the energies are shifted so that the middle of the lower
band is at zero. _g5_bands.load asserts these numbers."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import _g5_bands as gb
style = gb.style
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, so that they stay readable on a phone

d = gb.load(style.run_script('session04/g5_haldane_t3_bands.py'))
fig, axs = plt.subplots(1, 2, figsize=(12 * style.CM, 5.6 * style.CM), gridspec_kw=dict(wspace=0.3))
for i, (ax, name) in enumerate(zip(axs, (r'(a) the Haldane model, $t_2=0.1$', '(b) a flat Chern band'))):
    b = d['bands'][i]
    assert abs(d['chern'][i] - 1) < 1e-6
    gb.draw(ax, b, style.ACCENT)
    ax.set_ylim(-2.2, 6.2)
    assert -2.2 < b.min() and b.max() < 6.2
    style.arrows(ax, ylabel=r'$E/t$', ticks=True)
    ax.set_xticks([0, 100, 200, 300]); ax.set_xticklabels(gb.NAMES, fontsize=11)
    ax.set_yticks([0, 2, 4, 6]); ax.set_yticklabels(['0', '2', '4', '6'], fontsize=11); ax.tick_params(length=2.5, width=0.6)
    j = 150                                        # the label in the middle of the gap, between K and M
    style.label(ax, j, 0.5 * (b[:, 0].max() + b[:, 1].min()), r'$C=1$', color=style.ACCENT, fontsize=11)
    ax.text(0.5, -0.15, name, transform=ax.transAxes, ha='center', va='top', fontsize=11)
style.save(fig, __file__)
