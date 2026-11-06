"""Helper of the level diagrams of the two-spin problems of session 8, the energies come from the 4x4 matrices."""
import numpy as np
import style

sx = np.array([[0, 1], [1, 0]]) / 2; sy = np.array([[0, -1j], [1j, 0]]) / 2; sz = np.diag([.5, -.5])
HEIS = sum(np.kron(s, s) for s in (sx, sy, sz)).real
ISING = np.kron(sz, sz)

def levels(H):
    """The distinct energies of H with their degeneracy, lowest first."""
    e = np.round(np.linalg.eigvalsh(H), 10)
    vals = sorted(set(e))
    return [(v, int((e == v).sum())) for v in vals]

def column(ax, x, H, title, colors, labels, w=0.9):
    """A column of levels at x, a short bar for every state of a degenerate level, the ground level in red."""
    for k, (v, d) in enumerate(levels(H)):
        col = colors[k]
        for j in range(d):
            x0 = x - w / 2 + j * (w / d)
            ax.plot([x0 + 0.03, x0 + w / d - 0.03], [v, v], color=col, lw=2.6, solid_capstyle='butt')
        style.label(ax, x + w / 2 + 0.08, v, labels[k], fontsize=8.2, color=col, ha='left')
    style.label(ax, x, 1.22, title, fontsize=8.8, color=style.INK)
