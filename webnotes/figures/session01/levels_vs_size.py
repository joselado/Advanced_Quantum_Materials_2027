"""Session 1, the levels of an open chain of N sites, -2 t cos(n pi/(N+1)), for N=10 and N=100."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style

t = 1.0
lev = lambda N: np.sort(-2 * t * np.cos(np.arange(1, N + 1) * np.pi / (N + 1)))
for N in (10, 100):
    H = -t * (np.eye(N, k=1) + np.eye(N, k=-1))
    assert np.allclose(np.linalg.eigvalsh(H), lev(N))
mid = lambda N: np.diff(lev(N))[N // 2 - 1]
assert abs(mid(10) - 0.57) < 0.01 and abs(mid(100) - 0.062) < 0.002
fig, ax = style.figure(height_cm=3.4, width_cm=9.6)
for j, N in enumerate((100, 10)):
    for e in lev(N):
        ax.plot([e, e], [j + 0.15, j + 0.85], color=style.ACCENT, lw=1.2 if N == 10 else 0.5)
    style.label(ax, -2.45, j + 0.5, rf'$N={N}$', ha='right', fontsize=9)
ax.set_xlim(-2.5, 2.5); ax.set_ylim(0, 2.0)
ax.set_xticks([-2, 0, 2]); ax.set_xticklabels([r'$-2t$', r'$0$', r'$2t$'])
ax.spines['bottom'].set_visible(True)
ax.tick_params(axis='x', length=2.5)
style.label(ax, 0.0, -0.55, r'$E$', fontsize=9)
ax.annotate('', xy=(lev(10)[5], 1.95), xytext=(lev(10)[4], 1.95), arrowprops=dict(arrowstyle='<->', color=style.BROKEN, lw=0.9, shrinkA=0, shrinkB=0))
style.label(ax, 0.38, 1.95, r'$0.57t$', color=style.BROKEN, fontsize=8, ha='left')
ax.annotate('', xy=(lev(100)[50], 1.0), xytext=(lev(100)[49], 1.0), arrowprops=dict(arrowstyle='<->', color=style.BROKEN, lw=0.9, shrinkA=0, shrinkB=0))
style.label(ax, 0.12, 1.0, r'$0.062t$', color=style.BROKEN, fontsize=8, ha='left')
style.save(fig, __file__)
