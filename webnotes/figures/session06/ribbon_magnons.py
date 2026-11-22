"""Session 6, the edge states of a magnon ribbon with the Dzyaloshinskii-Moriya term of one sign and of the opposite sign.

Redrawn on 2026-11-22 from the pyqula script webnotes/scripts/session06/g5_magnon_ribbon.py, which the student downloads, in
place of the numpy ribbon of _haldane.py. The ribbon has zigzag edges and 48 sites across, the magnon hops with -|J|S, |J|S = 1,
every site has the onsite energy 3|J|S of the bulk, and the second-neighbor hopping is DS = 0.1 in (a) and -0.1 in (b). The
sign of DS is the one of the conventions sheet of Session 6, where add_haldane(x) is DS = -sqrt(3) x/2. The caption says only
that the branches reverse with the sign, which is asserted here: one branch per edge inside the gap of the bulk, opposite slopes
on the two edges, and the slope of each edge reversed between (a) and (b)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import style
import _g5_ribbonquiz as r

models = r.load(style.run_script('session06/g5_magnon_ribbon.py'))
pos, neg = models[0], models[1]
assert pos['DS'] == 0.1 and neg['DS'] == -0.1
assert abs((pos['hi'] - pos['lo']) - 1.0392) < 5e-5                     # the gap of the bulk at K, 6 sqrt(3) DS
slopes = {}
for name, m in (('+', pos), ('-', neg)):
    for edge in ('lower', 'upper'):
        s = [r.branch_slopes(m, edge, level) for level in (2.75, 3.25)]
        assert all(len(x) == 1 for x in s), (name, edge, s)             # one branch of each edge crosses each energy of the gap
        assert s[0][0][1] * s[1][0][1] > 0                               # the same branch, with one sign of the slope
        slopes[name, edge] = np.sign(s[0][0][1])
assert slopes['+', 'lower'] == -slopes['+', 'upper'] and slopes['-', 'lower'] == -slopes['-', 'upper']
assert slopes['+', 'lower'] == -slopes['-', 'lower']                       # reversing D reverses the branches
print('slopes of the edge branches', slopes)

fig, axs = plt.subplots(1, 2, figsize=(11.0 * style.CM, 5.4 * style.CM), sharey=True)
for ax, m, ttl in zip(axs, (pos, neg), (r'(a) $DS=0.1$', r'(b) $DS=-0.1$')):
    r.draw(ax, m, ms=1.8)
    style.arrows(ax, xlabel=r'$k$', ylabel=r'$E/|J|S$' if m is pos else '', ticks=True)
    ax.set_xticks([0, np.pi, 2 * np.pi]); ax.set_xticklabels(['0', r'$\pi$', r'$2\pi$'])
    ax.set_yticks([2, 3, 4]); ax.set_yticklabels(['2', '3', '4'])
    ax.tick_params(length=2.5, width=0.6, pad=2)
    style.label(ax, np.pi, 4.72, ttl, fontsize=8.5)
style.label(axs[0], 1.25, 1.75, 'lower edge', color=r.LOWER, fontsize=8)
style.label(axs[0], 5.0, 1.75, 'upper edge', color=r.UPPER, fontsize=8)
fig.subplots_adjust(wspace=0.14)
style.save(fig, __file__)
