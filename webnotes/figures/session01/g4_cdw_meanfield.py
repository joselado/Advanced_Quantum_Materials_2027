"""Session 1, Section 1.13, the charge imbalance and the gap of the charge density wave of the chain (1.6) against the
repulsion V, a new figure of the web notes.

The calculation is the pyqula script webnotes/scripts/session01/g4_cdw_chain.py, which the student downloads under the
figure, and _g4_cdw.check asserts it against the gap equation and asserts the numbers of the caption: the imbalance
0.03 at V = 0.5t, 0.34 at V = t and 0.89 at V = 3t, the gap 2 V dn, which is 5.35t at V = 3t and stays below 2V."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import _g4_cdw
import style

FS = 10.5
d = style.run_script('session01/g4_cdw_chain.py')       # the variables of the script that the student downloads
_g4_cdw.check(d)
Vs, dn, gap = np.array(d['Vs']), np.array(d['imbalance']), np.array(d['gap'])
i3 = int(np.argmin(np.abs(Vs - 3.0)))

fig = plt.figure(figsize=(13.0 * style.CM, 5.6 * style.CM))
gs = fig.add_gridspec(1, 2, wspace=0.45)
axn, axg = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
for ax in (axn, axg):
    style.arrows(ax, ticks=True)
    ax.spines['bottom'].set_visible(True); ax.spines['left'].set_visible(True)
    ax.tick_params(labelsize=FS, length=2.5)
    ax.set_xticks([0, 1, 2, 3, 4, 5, 6]); ax.set_xlim(0, 6.3)
    style.guide(ax, x=3)
# (a) the charge imbalance dn = |<n_even> - <n_odd>|
axn.plot(Vs, dn, color=style.ACCENT, marker='o', ms=3.2)
style.guide(axn, y=1)
axn.set_ylim(0, 1.08); axn.set_yticks([0, 0.5, 1]); axn.set_yticklabels(['0', '0.5', '1'])
style.label(axn, 3.15, dn[i3] - 0.1, r'$0.89$', color=style.ACCENT, fontsize=FS, ha='left')
axn.annotate(r'$\delta n$', xy=(0, 1.06), xycoords='axes fraction', ha='center', va='bottom', fontsize=FS)
axn.annotate(r'$V/t$', xy=(1.03, 0), xycoords='axes fraction', ha='left', va='center', fontsize=FS)
# (b) the gap 2 V dn, and the line 2V of a full imbalance
axg.plot(Vs, 2 * Vs, color=style.MUTED, lw=1.1, ls=(0, (4, 3)))
axg.plot(Vs, gap, color=style.ACCENT, marker='o', ms=3.2)
axg.set_ylim(0, 12.6); axg.set_yticks([0, 4, 8, 12])
style.label(axg, 4.6, 10.9, r'$2V$', color=style.MUTED, fontsize=FS)
style.label(axg, 3.2, gap[i3] - 1.2, r'$5.35$', color=style.ACCENT, fontsize=FS, ha='left')
axg.annotate(r'gap$/t$', xy=(0, 1.06), xycoords='axes fraction', ha='center', va='bottom', fontsize=FS)
axg.annotate(r'$V/t$', xy=(1.03, 0), xycoords='axes fraction', ha='left', va='center', fontsize=FS)
for ax, tag in ((axn, '(a)'), (axg, '(b)')):
    ax.text(-0.3, 1.1, tag, transform=ax.transAxes, fontsize=FS, ha='left', va='bottom')
style.save(fig, __file__)
