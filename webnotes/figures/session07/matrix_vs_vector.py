"""Session 7, what we have to store for the Heisenberg chain of L sites, the dense matrix, its nonzero elements and
the vector of 2^L coefficients (7.4). The nonzero elements are counted on the bit strings of the basis."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style
plt.rcParams.update({'font.size': 11})          # labels a size up from style.py, so that they stay readable on a phone

def nonzeros(L):
    """Nonzero matrix elements of H = sum_i S_i.S_{i+1}, open chain, in the basis of S^z products."""
    s = np.arange(2 ** L, dtype=np.int64)
    diag = np.zeros(2 ** L)
    off = np.zeros(2 ** L, dtype=np.int64)
    for i in range(L - 1):
        a = (s >> i) & 1
        b = (s >> (i + 1)) & 1
        diag += np.where(a == b, 0.25, -0.25)
        off += (a != b)              # S^+_i S^-_{i+1} + h.c. flips an antiparallel pair, one element each
    return int(np.count_nonzero(np.abs(diag) > 1e-12) + off.sum())

Ls = np.arange(2, 23, 2)
nnz = np.array([nonzeros(L) for L in Ls], dtype=float)
# every basis state has (L-1)/2 antiparallel bonds on average, so the off-diagonal count is (L-1) 2^(L-1),
# and for even L the diagonal is never zero, which gives (L+1) 2^(L-1) in total
assert all(n == (L + 1) * 2 ** (L - 1) for n, L in zip(nnz, Ls))

fig, ax = style.figure(height_cm=6.6, width_cm=12.0)
x = np.arange(1, 25)
ax.plot(x, np.log10(4.0 ** x), color=style.MUTED, lw=1.4, ls=(0, (4, 2.5)))
ax.plot(x, np.log10(2.0 ** x), color=style.ACCENT)
ax.plot(Ls, np.log10(nnz), 'o', ms=4, color=style.BROKEN, zorder=3)
ax.set_xlim(0, 25); ax.set_ylim(0, 15)
gb = np.log10(1e9 / 16)
style.guide(ax, y=gb, linestyle=(0, (3, 3)))
style.label(ax, 0.6, gb + 0.5, '1 GB', ha='left', fontsize=11, color=style.MUTED)
style.arrows(ax, xlabel=r'$L$', ylabel=r'$\log_{10}$ of the numbers to store')
ax.set_xticks([10, 20]); ax.tick_params(axis='x', length=2.5, pad=2, labelsize=11)
ax.plot([1.0, 2.6], [14.0, 14.0], color=style.MUTED, lw=1.4, ls=(0, (4, 2.5)))
style.label(ax, 3.2, 14.0, r'dense matrix, $4^L$', ha='left', fontsize=11, color=style.MUTED)
ax.plot([1.8], [12.7], 'o', ms=4, color=style.BROKEN)
style.label(ax, 3.2, 12.7, r'nonzero elements, $(L+1)\,2^{L-1}$', ha='left', fontsize=11, color=style.BROKEN)
ax.plot([1.0, 2.6], [11.4, 11.4], color=style.ACCENT)
style.label(ax, 3.2, 11.4, r'vector of coefficients, $2^L$', ha='left', fontsize=11, color=style.ACCENT)
style.save(fig, __file__)
