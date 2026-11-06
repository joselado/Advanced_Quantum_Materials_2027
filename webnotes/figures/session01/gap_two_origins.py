"""Session 1, two gaps that look alike. A band gap of the lattice and a pairing gap of the electrons."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle, Ellipse, FancyArrowPatch
import style

t, m, D = 1.0, 0.6, 0.6
fig, axs = style.figure(height_cm=5.6, ncols=2)
k = np.linspace(-np.pi / 2, np.pi / 2, 400)
# (a) chain with two sites per cell and an onsite energy +-m, the bands are +-sqrt(m^2+(2t cos k)^2)
ax = axs[0]
band = 2 * t * np.cos(k)
Ea = np.sqrt(m ** 2 + band ** 2)
assert abs(Ea.min() - m) < 1e-3                       # the gap is 2m, at the zone edge
H = lambda kk: np.array([[m, 2 * t * np.cos(kk)], [2 * t * np.cos(kk), -m]])
assert abs(np.linalg.eigvalsh(H(0.3))[1] - np.sqrt(m ** 2 + (2 * t * np.cos(0.3)) ** 2)) < 1e-12
ax.plot(k, band, color=style.GRID, lw=1.2, zorder=1)
ax.plot(k, -band, color=style.GRID, lw=1.2, zorder=1)
ax.plot(k, Ea, color=style.ACCENT)
ax.plot(k, -Ea, color=style.ACCENT)
style.guide(ax, y=0)
style.arrows(ax, xlabel=r'$k$', ylabel=r'$E$')
ax.set_xlim(-np.pi / 2, np.pi / 2); ax.set_ylim(-2.6, 2.6)
ax.set_title('semiconductor', fontsize=8.5, pad=10)
ax.annotate('', xy=(np.pi / 2 - 0.02, m), xytext=(np.pi / 2 - 0.02, -m), arrowprops=dict(arrowstyle='<->', color=style.BROKEN, lw=0.9, shrinkA=0, shrinkB=0))
style.label(ax, np.pi / 2 - 0.12, 0.0, r'$2m$', color=style.BROKEN, ha='right', fontsize=9)
# (b) quasiparticles of a superconductor, +-sqrt(xi^2+Delta^2), with xi = -2t cos k
ax = axs[1]
k = np.linspace(-np.pi, np.pi, 600)
xi = -2 * t * np.cos(k)
Eb = np.sqrt(xi ** 2 + D ** 2)
assert abs(Eb.min() - D) < 1e-3
ax.plot(k, xi, color=style.GRID, lw=1.2, zorder=1)
ax.plot(k, -xi, color=style.GRID, lw=1.2, zorder=1)
ax.plot(k, Eb, color=style.ACCENT)
ax.plot(k, -Eb, color=style.ACCENT)
style.guide(ax, y=0)
style.arrows(ax, xlabel=r'$k$', ylabel=r'$E$')
ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-2.6, 2.6)
ax.set_title('superconductor', fontsize=8.5, pad=10)
ax.annotate('', xy=(np.pi / 2, D), xytext=(np.pi / 2, -D), arrowprops=dict(arrowstyle='<->', color=style.BROKEN, lw=0.9, shrinkA=0, shrinkB=0))
style.label(ax, np.pi / 2 + 0.25, 0.0, r'$2\Delta$', color=style.BROKEN, ha='left', fontsize=9)
fig.subplots_adjust(wspace=0.35)
style.save(fig, __file__)
