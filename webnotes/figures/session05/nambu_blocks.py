"""Session 5, the structure of the BdG matrix (5.7) in the Nambu basis (5.6), and the two blocks (5.8) it splits into.

The matrix is built with numbers standing for eps and Delta, the basis is reordered as
(c_k_up, c+_-k_down, c_k_down, -c+_-k_up), and the script checks that the reordered matrix is block diagonal with
two identical 2x2 blocks. The cells are tinted by the block they belong to, so the two interleaved blocks of the
left matrix become the two contiguous blocks of the right one.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
import style

e, d = 1.3, 0.7                                          # stand-ins for eps(k) and a real Delta
H = np.array([[e, 0, d, 0], [0, e, 0, d], [d, 0, -e, 0], [0, d, 0, -e]])
perm = [0, 2, 1, 3]
Hp = H[np.ix_(perm, perm)]
assert np.allclose(Hp[:2, 2:], 0) and np.allclose(Hp[2:, :2], 0) and np.allclose(Hp[:2, :2], Hp[2:, 2:])
assert np.allclose(Hp[:2, :2], [[e, d], [d, -e]])         # the reduced matrix (5.8)

sym = {e: r'$\varepsilon$', -e: r'$-\varepsilon$', d: r'$\Delta$'}
basis = [r'$c_{\mathbf{k}\uparrow}$', r'$c_{\mathbf{k}\downarrow}$', r'$c^\dagger_{-\mathbf{k}\downarrow}$',
         r'$-c^\dagger_{-\mathbf{k}\uparrow}$']
block = [0, 1, 0, 1]                                      # which 2x2 block each basis state belongs to
tint = ['#dbe5f0', '#f3e0da']                             # light ACCENT and light WARM

FS = 12.5
style.plt.rcParams['font.size'] = FS          # labels of the arrows too, for a phone
W, Hh = 13.0, 4.7
fig = plt.figure(figsize=(W * style.CM, Hh * style.CM))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, Hh); ax.axis('off')
c = 0.9                                                   # cell size in cm


def matrix(M, order, x0, y0, labels_left):
    for i in range(4):
        for j in range(4):
            x, y = x0 + j * c, y0 - (i + 1) * c
            bi, bj = block[order[i]], block[order[j]]
            fc = tint[bi] if bi == bj else 'white'
            ax.add_patch(Rectangle((x, y), c, c, fc=fc, ec='white', lw=1.5))
            val = M[i, j]
            if abs(val) < 1e-12:
                ax.text(x + c / 2, y + c / 2, r'$0$', ha='center', va='center', fontsize=FS - 1.5, color=style.GRID)
            else:
                key = min(sym, key=lambda s: abs(s - val))
                txt = sym[key] if (key != d or order[i] < 2) else r'$\Delta^*$'   # Delta^* in the hole rows
                ax.text(x + c / 2, y + c / 2, txt, ha='center', va='center', fontsize=FS,
                        color=style.ACCENT if bi == 0 else style.BROKEN)
        lab = basis[order[i]]
        if labels_left:
            ax.text(x0 - 0.15, y0 - (i + 0.5) * c, lab, ha='right', va='center', fontsize=FS - 0.5)
        else:
            ax.text(x0 + 4 * c + 0.15, y0 - (i + 0.5) * c, lab, ha='left', va='center', fontsize=FS - 0.5)
    ax.plot([x0 - 0.05, x0 - 0.05], [y0 - 4 * c, y0], color=style.INK, lw=0.9)
    ax.plot([x0 + 4 * c + 0.05] * 2, [y0 - 4 * c, y0], color=style.INK, lw=0.9)


y0 = 4.05
matrix(H, [0, 1, 2, 3], 1.95, y0, True)
matrix(Hp, perm, 7.35, y0, False)
for x0 in (7.35,):
    for k in (0, 2):
        ax.add_patch(Rectangle((x0 + k * c, y0 - (k + 2) * c), 2 * c, 2 * c, fill=False, ec=style.INK, lw=1.0))
ax.add_patch(FancyArrowPatch((5.75, y0 - 2 * c), (7.0, y0 - 2 * c), arrowstyle='-|>', mutation_scale=11,
                             color=style.INK, lw=1.0))
ax.text(6.37, y0 - 2 * c + 0.3, 'reorder', ha='center', va='bottom', fontsize=FS - 1)
ax.text(1.95 + 2 * c, y0 + 0.45, r'$H_{\mathrm{BdG}}$ in the order of (5.6)', ha='center', fontsize=FS - 0.5)
ax.text(7.35 + 2 * c, y0 + 0.45, r'two copies of $h_{\mathrm{BdG}}$', ha='center', fontsize=FS - 0.5)
style.save(fig, __file__)
