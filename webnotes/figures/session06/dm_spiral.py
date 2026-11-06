"""Session 6, classical spins on a chain, the angle between neighbours with a Dzyaloshinskii-Moriya term."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow
import style

# bond energy for spins in the plane, with D along z: E(theta) = J cos(theta) + D sin(theta), theta = angle from site to site
# minimum at cos(theta) = -J/sqrt(J^2+D^2)
def angle(J, D):
    th = np.linspace(0, 2 * np.pi, 200001)
    th0 = th[np.argmin(J * np.cos(th) + D * np.sin(th))]
    assert abs(abs(np.cos(th0)) - J / np.hypot(J, D)) < 1e-3
    return np.arccos(-J / np.hypot(J, D))      # the magnitude of the rotation from site to site

cases = [(1.0, 0.0), (1.0, 1.0), (1.0, 5.0)]
fig, ax = plt.subplots(figsize=(style.WIDTH_CM * style.CM, 5.6 * style.CM))
ax.axis('off'); ax.set_aspect('equal')
N = 9
for row, (J, D) in enumerate(cases):
    y = -row * 1.6
    th = angle(J, D)
    for i in range(N):
        a = np.pi / 2 + i * th
        ax.add_patch(FancyArrow(i * 1.0 - 0.31 * np.cos(a), y - 0.31 * np.sin(a), 0.62 * np.cos(a), 0.62 * np.sin(a), width=0.05, head_width=0.2, head_length=0.18,
                                length_includes_head=True, fc=style.ACCENT, ec='none'))
        ax.plot([i], [y], 'o', color=style.INK, ms=2.0, zorder=5)
    
    lab = r'$D=0$' if D == 0 else (r'$D=J$' if D == J else r'$D=5J$')
    style.label(ax, -1.1, y, lab, fontsize=8.5, ha='right')
    style.label(ax, N + 0.2, y, r'$%.0f^\circ$' % np.degrees(th), fontsize=8.5, color=style.BROKEN, ha='left')
style.label(ax, N + 0.2, 0.9, 'angle per bond', fontsize=8, color=style.BROKEN, ha='left')
style.label(ax, 4, 0.95, r'view along $\mathbf{D}$, the spins stay in the plane', fontsize=8.5)
ax.set_xlim(-2.6, N + 3.2); ax.set_ylim(-3.9, 1.3)
style.save(fig, __file__)
print([round(np.degrees(angle(*c)), 1) for c in cases])
