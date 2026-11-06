"""Session 2, the Dirac cone E = +- sqrt(m^2 + (v q)^2) with and without a mass term."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import style

v, m = 1.0, 0.5
q = np.linspace(-1.6, 1.6, 400)
H = lambda qx, qy, mm: np.array([[mm, v * (qx - 1j * qy)], [v * (qx + 1j * qy), -mm]])
for qq in (0.0, 0.7):
    assert np.allclose(np.linalg.eigvalsh(H(qq, 0.0, m)), [-np.sqrt(m ** 2 + (v * qq) ** 2), np.sqrt(m ** 2 + (v * qq) ** 2)])
assert np.allclose(np.linalg.eigvalsh(H(0, 0, 0.0)), [0, 0])         # no mass, no gap at the tip
fig, ax = style.figure(height_cm=4.4, width_cm=9.6)
ax.plot(q, v * np.abs(q), color=style.ACCENT); ax.plot(q, -v * np.abs(q), color=style.ACCENT)
E = np.sqrt(m ** 2 + (v * q) ** 2)
ax.plot(q, E, color=style.BROKEN, lw=1.4, ls=(0, (4, 2))); ax.plot(q, -E, color=style.BROKEN, lw=1.4, ls=(0, (4, 2)))
style.guide(ax, y=0)
style.arrows(ax, xlabel=r'$q_x$', ylabel=r'$E$')
ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.8, 1.8)
style.label(ax, 0.0, 1.62, 'no mass term', color=style.ACCENT, fontsize=8.5)
style.label(ax, 0.0, 1.28, r'mass term $m\sigma_z$', color=style.BROKEN, fontsize=8.5)
ax.annotate('', xy=(0.0, m), xytext=(0.0, -m), arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.8, shrinkA=0, shrinkB=0))
style.label(ax, 0.0, 0.72, r'$2m$', fontsize=8.5)
style.save(fig, __file__)
