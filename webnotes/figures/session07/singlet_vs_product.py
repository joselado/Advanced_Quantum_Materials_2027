"""Session 7, quiz of 7.1, the energy of two spins 1/2 in a product state against the singlet, computed with 2x2 matrices."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

sx = np.array([[0, 1], [1, 0]]) / 2; sy = np.array([[0, -1j], [1j, 0]]) / 2; sz = np.diag([.5, -.5])
SS = sum(np.kron(s, s) for s in (sx, sy, sz))
def spinor(th):                      # spin pointing at the angle th from the z axis, in the xz plane
    return np.array([np.cos(th / 2), np.sin(th / 2)])
th = np.linspace(0, np.pi, 300)
E = np.array([np.real(np.kron(spinor(0), spinor(t)) @ SS @ np.kron(spinor(0), spinor(t))) for t in th])
assert np.allclose(E, np.cos(th) / 4) and abs(E.min() + 0.25) < 1e-12
sing = np.array([0, 1, -1, 0]) / np.sqrt(2)
Es = np.real(sing @ SS @ sing)
assert abs(Es + 0.75) < 1e-12

fig, ax = style.figure(height_cm=5.0, width_cm=9.5)
ax.plot(th / np.pi, E, color=style.ACCENT)
ax.axhline(Es, color=style.BROKEN, lw=1.5, ls=(0, (4, 2)))
style.guide(ax, y=0)
ax.set_xlim(0, 1.0); ax.set_ylim(-0.95, 0.42)
ax.plot([1], [-0.25], 'o', color=style.ACCENT, ms=4.5, clip_on=False)
style.label(ax, 0.97, -0.46, r'best product state, $-\frac{1}{4}$', fontsize=8.3, color=style.ACCENT, ha='right')
style.label(ax, 0.5, -0.82, r'singlet, $-\frac{3}{4}$', fontsize=8.3, color=style.BROKEN)
ax.set_xticks([0, 1]); ax.set_xticklabels([r'$0$', r'$\pi$']); ax.tick_params(axis='x', length=2.5, pad=2)
ax.set_yticks([-0.75, -0.25, 0, 0.25]); ax.set_yticklabels([r'$-\frac{3}{4}$', r'$-\frac{1}{4}$', r'$0$', r'$\frac{1}{4}$']); ax.tick_params(axis='y', length=2.5, pad=2)
style.arrows(ax, xlabel=r'angle between the spins', ylabel=r'$\langle\mathbf{S}_1\cdot\mathbf{S}_2\rangle$', ticks=True)
style.save(fig, __file__)
