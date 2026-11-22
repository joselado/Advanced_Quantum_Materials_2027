"""Session 1, the phase of a superconducting order parameter, uniform and with one vortex.

The arrow at each point is Delta(r) = |Delta(r)| exp(i theta(r)) drawn in the complex plane. Uniform state,
theta = 0. Vortex, theta = arg(x + i y) and |Delta| = tanh(r / xi), so the amplitude vanishes at the core
and the phase winds by 2 pi along any loop around it. Redrawn on 2026-11-21 with the axes x/xi and y/xi, the positions
in units of the coherence length xi. The fields and the winding along the red loop are in _g1_phase.py, which the
picture quiz of the same page also uses.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style
import _g1_phase

w = _g1_phase.check()
assert abs(w['vortex'] - 1) < 1e-9 and abs(w['uniform']) < 1e-9

FS = 11.5
fig, axs = plt.subplots(1, 2, figsize=(12.5 * style.CM, 6.9 * style.CM))
fig.subplots_adjust(wspace=0.32, left=0.08, right=0.98, bottom=0.14, top=0.88)
_g1_phase.draw(axs[0], 'uniform', loop=False)
_g1_phase.draw(axs[1], 'vortex')
axs[1].scatter([0], [0], s=40, facecolor='white', edgecolor=style.BROKEN, lw=1.2, zorder=4)
axs[0].set_title(r'uniform phase, $\theta=0$', fontsize=FS)
axs[1].set_title(r'one vortex, $\theta$ winds by $2\pi$', fontsize=FS, color=style.INK)
for ax in axs:
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xlim(-3.6, 3.6); ax.set_ylim(-3.6, 3.6)
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3]); ax.set_yticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_xticklabels(['$-3$', '', '', '0', '', '', '3'], fontsize=FS - 0.5)
    ax.set_yticklabels(['$-3$', '', '', '0', '', '', '3'], fontsize=FS - 0.5)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$x/\xi$', fontsize=FS, labelpad=1); ax.set_ylabel(r'$y/\xi$', fontsize=FS, labelpad=-2)
style.save(fig, __file__)
