"""Helper of the picture quiz of Section 8.2, a chain of six spin-1/2 sites with singlets drawn as capsules and free
spins drawn as arrows.

Each picture is a sketch with no axes. The helper also builds the state that it draws, on the 64 states of six
spins, with every singlet (up down - down up)/sqrt2 in the order of its two sites, and returns the expectation value
of S_tot^2, the total S^z and whether the state is an eigenstate of S_tot^2. The picture scripts assert these, so a
picture cannot show a state with another total spin than its feedback says. This file writes no figure."""
from functools import reduce
import numpy as np
import style
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch

N = 6
UP, DN = np.array([1., 0.]), np.array([0., 1.])
_s = (np.array([[0, 1], [1, 0]]) / 2, np.array([[0, -1j], [1j, 0]]) / 2, np.diag([.5, -.5]))


def _site_op(o, i):
    return reduce(np.kron, [o if j == i else np.eye(2) for j in range(N)])


STOT = [sum(_site_op(o, i) for i in range(N)) for o in _s]
S2 = sum(t @ t for t in STOT)


def state(singlets, spins):
    """singlets: pairs (i, i+1) of neighbors, spins: {site: +1 or -1}. Every site is in one of the two."""
    parts, i = [], 0
    pairs = dict(singlets)
    while i < N:
        if i in pairs:
            assert pairs[i] == i + 1
            parts.append((np.kron(UP, DN) - np.kron(DN, UP)) / np.sqrt(2))
            i += 2
        else:
            parts.append(UP if spins[i] > 0 else DN)
            i += 1
    return reduce(np.kron, parts)


def total_spin(psi):
    """<S_tot^2>, <S^z_tot> and True when psi is an eigenstate of S_tot^2."""
    s2 = np.vdot(psi, S2 @ psi).real
    sz = np.vdot(psi, STOT[2] @ psi).real
    return s2, sz, np.allclose(S2 @ psi, s2 * psi)


def draw(script, singlets=(), spins=None, width_cm=6.2):
    """Draws the chain and returns total_spin of the drawn state."""
    spins = spins or {}
    assert sorted([i for p in singlets for i in p] + list(spins)) == list(range(N))
    fig, ax = style.plt.subplots(figsize=(width_cm * style.CM, 1.75 * style.CM))
    ax.set_xlim(-0.55, N - 0.45); ax.set_ylim(-0.62, 0.62); ax.set_aspect('equal'); ax.axis('off')
    fig.subplots_adjust(0, 0, 1, 1)
    for a, b in singlets:
        ax.add_patch(FancyBboxPatch((a - 0.36, -0.3), b - a + 0.72, 0.6, boxstyle='round,pad=0,rounding_size=0.3',
                                    facecolor='#e6eef6', edgecolor=style.ACCENT, lw=1.1, zorder=1))
    for i in range(N):
        ax.add_patch(Circle((i, 0), 0.13, facecolor=style.ACCENT, edgecolor='none', zorder=3))
    for i, s in spins.items():
        ax.add_patch(FancyArrowPatch((i, -0.5 * s), (i, 0.55 * s), arrowstyle='-|>', mutation_scale=11,
                                     color=style.ACCENT, lw=1.8, shrinkA=0, shrinkB=0, zorder=4))
    style.save(fig, script, sketch=True)
    return total_spin(state(singlets, spins))
