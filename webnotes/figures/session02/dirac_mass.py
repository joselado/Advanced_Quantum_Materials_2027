"""Session 2, Section 2.11a, the Dirac cone of (2.20) with and without a mass term, in the feedback of a quiz.

H = hbar v_F (q_x sigma_x + q_y sigma_y) + m sigma_z on the line q_y = 0. The energy is in units of m and the momentum
in units of m / hbar v_F, so the massless cone is E/m = +-|x| with x = hbar v_F q_x / m, and the massive one is
E/m = +-sqrt(1 + x^2), with the gap 2 at x = 0, which is 2m. This is the continuum Hamiltonian and not a lattice, so
it stays in numpy. The asserts check the two pairs of bands on the eigenvalues of the matrix."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

sx = np.array([[0, 1], [1, 0]], complex); sy = np.array([[0, -1j], [1j, 0]]); sz = np.diag([1., -1.]).astype(complex)
H = lambda x, y, mass: x * sx + y * sy + mass * sz          # hbar v_F q in units of m, and the mass 0 or 1
for x in (0.0, 0.7, -2.3):
    assert np.allclose(np.linalg.eigvalsh(H(x, 0.0, 1.0)), [-np.sqrt(1 + x ** 2), np.sqrt(1 + x ** 2)])
    assert np.allclose(np.linalg.eigvalsh(H(x, 0.0, 0.0)), [-abs(x), abs(x)])
assert np.allclose(np.diff(np.linalg.eigvalsh(H(0, 0, 1.0))), 2.0)    # the gap 2m at the tip
assert np.allclose(np.linalg.eigvalsh(H(0, 0, 0.0)), [0, 0])         # no mass, no gap at the tip

x = np.linspace(-3.2, 3.2, 401)
fig, ax = style.figure(height_cm=5.0, width_cm=9.6)
ax.plot(x, np.abs(x), color=style.ACCENT); ax.plot(x, -np.abs(x), color=style.ACCENT)
E = np.sqrt(1 + x ** 2)
ax.plot(x, E, color=style.BROKEN, lw=1.4, ls=(0, (4, 2))); ax.plot(x, -E, color=style.BROKEN, lw=1.4, ls=(0, (4, 2)))
style.guide(ax, y=0)
style.arrows(ax, xlabel=r'$\hbar v_F q_x/m$', ylabel=r'$E/m$', ticks=True)
ax.set_xlim(-3.2, 3.2); ax.set_ylim(-3.6, 3.6)
ax.set_xticks([-3, 0, 3]); ax.set_xticklabels([r'$-3$', '0', '3'])
ax.set_yticks([-3, -1, 0, 1, 3]); ax.set_yticklabels([r'$-3$', r'$-1$', '0', '1', '3'])
ax.tick_params(labelsize=9, length=2.5)
ax.spines['left'].set_visible(True); ax.spines['bottom'].set_visible(True)
style.label(ax, -1.9, 3.15, 'no mass term', color=style.ACCENT, fontsize=8.5)
style.label(ax, 1.75, 3.15, r'mass term $m\sigma_z$', color=style.BROKEN, fontsize=8.5)
ax.annotate('', xy=(0.0, 1.0), xytext=(0.0, -1.0), arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.8, shrinkA=0, shrinkB=0))
style.label(ax, 0.42, 0.0, r'$2m$', fontsize=9)
style.save(fig, __file__)
