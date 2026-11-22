"""Session 7, what we have to store for the Heisenberg chain of L sites, the dense matrix, its nonzero elements and
the vector of 2^L coefficients (7.4). The nonzero elements are counted on the bit strings of the basis.

Redrawn on 2026-11-22 under the same name, with a logarithmic axis that has its powers of ten, ticks at the sizes
L=13 and L=26 that the caption quotes, and the lines drawn past L=26, where the vector crosses the line of one
gigabyte."""
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
assert all(abs(n / 2.0 ** L - (L + 1) / 2) < 1e-12 for n, L in zip(nnz, Ls))      # (L+1)/2 times the vector
per_gb = 1e9 / 16                    # 16 bytes per complex number, so 1 GB (1e9 bytes) is 6.25e7 numbers
x = np.arange(1, 29)
# the caption: the dense matrix crosses the line at L=13 and the vector at L=26, the first sizes above it
assert int(x[np.argmax(4.0 ** x > per_gb)]) == 13 and int(x[np.argmax(2.0 ** x > per_gb)]) == 26
assert all(nnz < per_gb)             # the dots that we count stay below the line

fig, ax = style.figure(height_cm=6.6, width_cm=12.0)
ax.set_yscale('log')
ax.plot(x, 4.0 ** x, color=style.MUTED, lw=1.4, ls=(0, (4, 2.5)))
ax.plot(x, 2.0 ** x, color=style.ACCENT)
ax.plot(Ls, nnz, 'o', ms=4, color=style.BROKEN, zorder=3)
ax.set_xlim(0, 29); ax.set_ylim(1, 1e15)
style.guide(ax, y=per_gb, linestyle=(0, (3, 3)))
style.label(ax, 0.6, per_gb * 3.5, '1 GB', ha='left', fontsize=11, color=style.MUTED)
ax.plot([1.0, 2.6], [1e14, 1e14], color=style.MUTED, lw=1.4, ls=(0, (4, 2.5)))
style.label(ax, 3.2, 1e14, r'dense matrix, $4^L$', ha='left', fontsize=11, color=style.MUTED)
ax.plot([1.8], [10 ** 12.6], 'o', ms=4, color=style.BROKEN)
style.label(ax, 3.2, 10 ** 12.6, r'nonzero elements, $(L+1)\,2^{L-1}$', ha='left', fontsize=11, color=style.BROKEN)
ax.plot([1.0, 2.6], [10 ** 11.2, 10 ** 11.2], color=style.ACCENT)
style.label(ax, 3.2, 10 ** 11.2, r'vector of coefficients, $2^L$', ha='left', fontsize=11, color=style.ACCENT)
ax.set_xticks([10, 13, 20, 26])
ax.set_yticks([1.0, 1e5, 1e10, 1e15])
ax.set_yticklabels([r'$1$', r'$10^{5}$', r'$10^{10}$', r'$10^{15}$'])
ax.yaxis.set_minor_locator(plt.NullLocator())
ax.tick_params(axis='both', length=2.5, pad=2, labelsize=11)
style.arrows(ax, xlabel=r'$L$', ylabel=r'numbers to store', ticks=True)
style.save(fig, __file__)
