"""Session 7, the entropy of one site of the two-spin state cos(t)|ud> + sin(t)|du>, computed from its reduced density matrix."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

def entropy(theta):
    psi = np.array([[0, np.cos(theta)], [np.sin(theta), 0]])      # psi[s0, s1], the state cos|ud> + sin|du>
    rho = psi @ psi.conj().T                                       # trace over the second spin
    p = np.linalg.eigvalsh(rho)
    p = p[p > 1e-14]
    return -np.sum(p * np.log(p))

theta = np.linspace(0, np.pi / 2, 400)
S = np.array([entropy(t) for t in theta]) / np.log(2)
assert abs(entropy(0)) < 1e-12 and abs(entropy(np.pi / 4) - np.log(2)) < 1e-12 and S.max() <= 1 + 1e-12

fig, ax = style.figure(height_cm=5.0)
ax.plot(theta / (np.pi / 4), S, color=style.ACCENT)
style.guide(ax, y=1)
ax.set_xlim(0, 2.0); ax.set_ylim(0, 1.25)
for x, s, txt, dx in [(0, 0, 'product state\n' + r'$|{\uparrow\downarrow}\rangle$', 0.05), (2, 0, 'product state\n' + r'$|{\downarrow\uparrow}\rangle$', -0.05)]:
    ax.plot([x], [s], 'o', color=style.BROKEN, ms=4.5, clip_on=False)
    style.label(ax, x + dx, 0.42, txt, color=style.BROKEN, fontsize=8, ha='left' if dx > 0 else 'right', linespacing=1.3)
ax.plot([1], [1], 'o', color=style.BROKEN, ms=4.5)
style.label(ax, 1, 1.13, r'$(|{\uparrow\downarrow}\rangle+|{\downarrow\uparrow}\rangle)/\sqrt{2}$, $S=\log 2$, as for the singlet', fontsize=8.2, color=style.BROKEN)
ax.set_xticks([0, 1, 2]); ax.set_xticklabels([r'$0$', r'$\pi/4$', r'$\pi/2$'])
ax.tick_params(axis='x', length=2.5, pad=2)
ax.set_yticks([0, 1]); ax.set_yticklabels([r'$0$', r'$\log2$']); ax.tick_params(axis='y', length=2.5, pad=2)
style.arrows(ax, xlabel=r'$\vartheta$', ylabel=r'$S$', ticks=True)
style.save(fig, __file__)
