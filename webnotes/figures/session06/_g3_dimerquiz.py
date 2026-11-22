"""Shared code of the picture options of the quiz of Section 6.8 on the levels of the Hubbard dimer at U = 10t.

The Hubbard dimer, two sites with the hopping -t and the repulsion U n_up n_dn on each site, is built with
Jordan-Wigner fermions on four modes and diagonalized in the sector of two electrons, six states. This is a
diagonalization of many-body states, which pyqula does not do, so it stays in numpy and has no download button. The
check holds the numbers of the quiz: at U = 10t the lowest level is the singlet at U/2 - sqrt(U^2/4 + 4t^2) = -0.385t,
with total spin zero, the next three levels are the triplet at exactly 0, and the two others are at U and at
U/2 + sqrt(U^2/4 + 4t^2), far above the window of the pictures. Each picture draws the four lowest levels as short
bars on an energy axis E/t, one bar for a single level and three bars side by side for a level of degeneracy three.
This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from functools import reduce
import matplotlib.pyplot as plt
import style

U, T = 10.0, 1.0
ES = U / 2 - np.sqrt(U ** 2 / 4 + 4 * T ** 2)


def dimer(U, t=1.0):
    """The six levels of the half-filled Hubbard dimer and the total spin S(S+1) of each eigenstate."""
    I2, Z, a = np.eye(2), np.diag([1., -1.]), np.array([[0., 1.], [0., 0.]])
    c = [reduce(np.kron, [Z] * m + [a] + [I2] * (3 - m)) for m in range(4)]     # modes (0,up), (0,dn), (1,up), (1,dn)
    n = [x.T @ x for x in c]
    H = sum(-t * (c[s].T @ c[2 + s] + c[2 + s].T @ c[s]) for s in (0, 1)) + U * (n[0] @ n[1] + n[2] @ n[3])
    Sp = sum(c[2 * i].T @ c[2 * i + 1] for i in (0, 1))                         # total S^+
    Sz = sum(0.5 * (n[2 * i] - n[2 * i + 1]) for i in (0, 1))
    S2 = Sp @ Sp.T + Sz @ Sz - Sz                                                # S^2 = S^+ S^- + Sz^2 - Sz
    keep = np.where(abs(np.diag(sum(n)) - 2) < 1e-9)[0]
    assert len(keep) == 6
    e, v = np.linalg.eigh(H[np.ix_(keep, keep)])
    s2 = np.einsum('in,ij,jn->n', v, S2[np.ix_(keep, keep)], v)
    return e, s2


def check():
    e, s2 = dimer(U, T)
    assert abs(e[0] - ES) < 1e-12 and round(e[0], 3) == -0.385 and abs(s2[0]) < 1e-12   # the singlet
    assert np.allclose(e[1:4], 0, atol=1e-12) and np.allclose(s2[1:4], 2, atol=1e-12)    # the triplet, S(S+1) = 2
    assert abs(e[4] - U) < 1e-12 and abs(e[5] - (U / 2 + np.sqrt(U ** 2 / 4 + 4 * T ** 2))) < 1e-12
    assert abs(ES - (5 - np.sqrt(29))) < 1e-12


def option(script, singlet, triplet):
    """One picture, the singlet at the energy singlet and the triplet at the energy triplet, in units of t."""
    check()
    fs = 16
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 3.9 * style.CM))
    w, gap = 0.22, 0.08
    if abs(singlet - triplet) < 1e-12:
        xs = [-1.5 * w - 1.5 * gap + k * (w + gap) for k in range(4)]
        for x in xs:
            ax.plot([x, x + w], [singlet] * 2, color=style.ACCENT, lw=2.4, solid_capstyle='butt')
    else:
        ax.plot([-0.5 * w, 0.5 * w], [singlet] * 2, color=style.ACCENT, lw=2.4, solid_capstyle='butt')
        for k in (-1, 0, 1):
            x = k * (w + gap) - 0.5 * w
            ax.plot([x, x + w], [triplet] * 2, color=style.ACCENT, lw=2.4, solid_capstyle='butt')
    ax.set_xlim(-0.75, 0.75); ax.set_ylim(-0.55, 0.25)
    for s in ('top', 'right', 'bottom'):
        ax.spines[s].set_visible(False)
    ax.spines['left'].set_linewidth(0.6)
    ax.set_xticks([])
    ax.set_yticks([-0.385, 0]); ax.set_yticklabels(["$-0.385$", "$0$"], fontsize=fs - 1)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_ylabel('$E/t$', fontsize=fs, labelpad=1)
    style.save(fig, script)
