"""Helper of the level diagrams of the two-spin problems of Section 8.3, the energies come from the 4x4 matrices.

The spins are S = sigma/2 with hbar = 1, as in webnotes/conventions/session08.md. The Ising dimer (8.1) is
Sz0 Sz1 and the Heisenberg dimer (8.2) is S0.S1, both with the coupling 1, so the energies are in units of J. Each
picture is one axes with the energy on the vertical axis and ticks at -3/4, -1/4, 1/4 and 3/4, and one column of
levels per Hamiltonian, with a short bar for every state of a degenerate level. These are many-body levels of two
spins, which pyqula does not diagonalize, so they stay in numpy and have no download button. This file writes no
figure."""
import numpy as np
import style

sx = np.array([[0, 1], [1, 0]]) / 2; sy = np.array([[0, -1j], [1j, 0]]) / 2; sz = np.diag([.5, -.5])
HEIS = sum(np.kron(s, s) for s in (sx, sy, sz)).real
ISING = np.kron(sz, sz)
TICKS = (-0.75, -0.25, 0.25, 0.75)
TICKLABELS = (r'$-3/4$', r'$-1/4$', r'$1/4$', r'$3/4$')


def levels(H):
    """The distinct energies of H with their degeneracy, lowest first."""
    e = np.round(np.linalg.eigvalsh(H), 10)
    vals = sorted(set(e))
    return [(v, int((e == v).sum())) for v in vals]


def plot(script, columns, ylabel, width_cm=9.5, height_cm=5.4, w=0.62, xlabel_gap=1.55, right=1.45):
    """columns: a list of (H, title, labels), one column of levels per Hamiltonian, with one label per level,
    lowest first. The ground level is red and the others blue. Returns the levels of every column."""
    fig, ax = style.plt.subplots(figsize=(width_cm * style.CM, height_cm * style.CM))
    out = []
    xs = [k * xlabel_gap for k in range(len(columns))]
    for x, (H, title, labels) in zip(xs, columns):
        lv = levels(H)
        assert len(lv) == len(labels), (title, lv)
        for k, (v, d) in enumerate(lv):
            col = style.BROKEN if k == 0 else style.ACCENT
            for j in range(d):
                x0 = x - w / 2 + j * (w / d)
                ax.plot([x0 + 0.03, x0 + w / d - 0.03], [v, v], color=col, lw=2.6, solid_capstyle='butt')
            style.label(ax, x + w / 2 + 0.06, v, labels[k], fontsize=8.5, color=col, ha='left')
        out.append(lv)
    ax.set_xlim(-0.55, xs[-1] + right); ax.set_ylim(-0.95, 0.95)
    ax.set_yticks(TICKS); ax.set_yticklabels(TICKLABELS)
    ax.set_xticks(xs); ax.set_xticklabels([c[1] for c in columns], fontsize=8.8)
    ax.tick_params(axis='x', length=0, pad=5)
    ax.tick_params(axis='y', length=2.5, pad=2)
    ax.set_ylabel(ylabel, fontsize=9)
    for sp in ('top', 'right', 'bottom'):
        ax.spines[sp].set_visible(False)
    style.save(fig, script)
    return out
