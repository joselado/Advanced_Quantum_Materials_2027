"""Session 8, the energy of a superposition of the two singlet coverings of a four-site Heisenberg plaquette,
cos(theta)|a> + sin(theta)|b>, computed exactly, with the exact ground state as a reference."""
import os, sys, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
from matplotlib.patches import Circle

up, dn = np.array([1., 0]), np.array([0, 1.])
def kron(vs):
    out = np.ones(1)
    for v in vs:
        out = np.kron(out, v)
    return out
def covering(pairs):
    """Product of the singlets (|up dn> - |dn up>)/sqrt 2 on the given pairs of the four sites."""
    psi = np.zeros(16)
    for flips in itertools.product((0, 1), repeat=len(pairs)):
        spins, sign = [None] * 4, 1
        for (i, j), f in zip(pairs, flips):
            spins[i], spins[j] = (dn, up) if f else (up, dn)
            sign *= -1 if f else 1
        psi += sign * kron(spins) / 2
    return psi
S = [np.array([[0, .5], [.5, 0]]), np.array([[0, -.5j], [.5j, 0]]), np.diag([.5, -.5])]
def op(o, i):
    return np.kron(np.kron(np.eye(2 ** i), o), np.eye(2 ** (3 - i)))
H = sum(op(s, i) @ op(s, (i + 1) % 4) for i in range(4) for s in S).real      # J = 1 on the four bonds of the ring
a = covering([(0, 1), (2, 3)])
b = covering([(1, 2), (3, 0)])
E0 = np.linalg.eigvalsh(H)[0]
th = np.linspace(-np.pi / 2, np.pi / 2, 401)
E = np.array([(p @ H @ p) / (p @ p) for p in (np.cos(t) * a + np.sin(t) * b for t in th)])
assert np.isclose(E0, -2) and np.isclose(a @ H @ a, -1.5) and np.isclose(a @ b, 0.5)
assert np.isclose(E.min(), E0) and np.isclose(th[E.argmin()], np.pi / 4)

fig, ax = style.figure(height_cm=6.6, width_cm=12.0)
style.guide(ax, y=E0, linestyle=(0, (3, 3)))
style.guide(ax, y=-1.5, linestyle=(0, (3, 3)))
ax.plot(th, E, color=style.ACCENT)
ax.set_xlim(-np.pi / 2 - 0.08, np.pi / 2 + 0.12); ax.set_ylim(-2.25, 0.75)
style.arrows(ax, xlabel=r'$\theta$', ylabel=r'$E/J$')
ax.set_xticks([-np.pi / 2, 0, np.pi / 4, np.pi / 2]); ax.set_xticklabels([r'$-\pi/2$', r'$0$', r'$\pi/4$', r'$\pi/2$'])
ax.set_yticks([-2, -1.5, 0]); ax.set_yticklabels([r'$-2$', r'$-\frac{3}{2}$', r'$0$'])
ax.tick_params(length=2.5, pad=2, labelsize=9.5)
style.label(ax, -0.45, -1.95, 'exact ground state', fontsize=9.5, color=style.MUTED, va='bottom')

def plaquette(x, y, pairs_list, w=0.5, h=0.8):
    """A small square of four sites in data coordinates, with the singlets of one or two coverings."""
    ins = ax.inset_axes([x - w / 2, y - h / 2, w, h], transform=ax.transData)
    ins.set_xlim(-0.3, 1.3); ins.set_ylim(-0.3, 1.3); ins.set_aspect('equal'); ins.axis('off')
    pos = [(0, 0), (1, 0), (1, 1), (0, 1)]
    for pairs in pairs_list:
        for i, j in pairs:
            ins.plot(*zip(pos[i], pos[j]), color=style.BROKEN, lw=4.0, solid_capstyle='round', alpha=0.8)
    for p in pos:
        ins.add_patch(Circle(p, 0.17, facecolor='white', edgecolor=style.INK, lw=0.9, zorder=3))
A, B = [(0, 1), (2, 3)], [(1, 2), (3, 0)]
plaquette(0.0, -0.75, [A])
plaquette(1.35, -0.75, [B])
plaquette(np.pi / 4, -1.15, [A, B])
style.label(ax, 0.0, -0.22, r'$|a\rangle$', fontsize=9.5)
style.label(ax, 1.35, -0.22, r'$|b\rangle$', fontsize=9.5)
style.label(ax, np.pi / 4, -0.6, r'$|a\rangle+|b\rangle$', fontsize=9.5)
style.label(ax, -1.45, -1.78, r'$-|b\rangle$', fontsize=9.5, ha='left')
style.label(ax, -np.pi / 4, 0.22, 'the other singlet, $|a\\rangle-|b\\rangle$', fontsize=9.5, color=style.ACCENT, va='bottom')
style.save(fig, __file__)
