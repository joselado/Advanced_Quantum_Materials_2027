"""Shared code of the Kitaev chain figures of Sections 5.16 and 5.17, the exact chain (5.19) in numpy.

The plan of the session keeps these figures in numpy until the lecturer picks between numpy and a pyqula script with a
download (webnotes/plans/session05.md, "Open for the lecturer"). The BdG matrix is the one of the conventions sheet, in the
basis (c_1..c_N, c_1^dag..c_N^dag), with the pairing matrix d_{n+1,n} = Delta = -d_{n,n+1}, so that the Hamiltonian (5.19) is
(1/2) Psi^dag H_BdG Psi plus a constant. Energies are in units of t. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style


def bdg(N, t, mu, D):
    """BdG matrix of (5.19) on an open chain of N sites, in the basis (c_1..c_N, c_1^dag..c_N^dag)."""
    h = -mu * np.eye(N) - t * (np.eye(N, k=1) + np.eye(N, k=-1))
    d = D * (np.eye(N, k=-1) - np.eye(N, k=1))       # antisymmetric pairing matrix of D(c_n c_{n+1} + h.c.)
    return np.block([[h, d], [d.conj().T, -h.T]])


def levels(N, t, mu, D):
    """The 2N BdG levels of the open chain, sorted, which come in pairs +E and -E."""
    e = np.linalg.eigvalsh(bdg(N, t, mu, D))
    assert np.allclose(e, -e[::-1], atol=1e-10)
    return e


def lowest_state(N, t, mu, D):
    """Weight |u_n|^2+|v_n|^2 on each site of the lowest state with E>0, and its energy."""
    e, v = np.linalg.eigh(bdg(N, t, mu, D))
    i = np.where(e > 0)[0][np.argmin(e[e > 0])]
    psi = v[:, i]
    w = abs(psi[:N])**2 + abs(psi[N:])**2
    assert abs(w.sum() - 1) < 1e-9
    return w, e[i]


def zero_weight(N, t, mu, D, tol=1e-9):
    """Weight on each site of the levels with |E| < tol, averaged over them, which does not depend on how the solver mixes
    the degenerate levels. Also returns the number of these levels."""
    e, v = np.linalg.eigh(bdg(N, t, mu, D))
    z = np.abs(e) < tol
    w = (abs(v[:N, z])**2 + abs(v[N:, z])**2).sum(axis=1) / z.sum()
    return w, int(z.sum())


def frame(ax, xticks, yticks, xlabel, ylabel, fontsize=10.5):
    """Left and bottom axes with ticks and names, no box on the top and the right."""
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_linewidth(0.6)
        ax.spines[s].set_color(style.INK)
    ax.set_xticks([x for x, _ in xticks]); ax.set_xticklabels([l for _, l in xticks], fontsize=fontsize)
    ax.set_yticks([y for y, _ in yticks]); ax.set_yticklabels([l for _, l in yticks], fontsize=fontsize)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.minorticks_off()
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=fontsize + 0.5, labelpad=1)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=fontsize + 0.5, labelpad=1)


def draw_levels(ax, e, ylim, yticks, fontsize=10.5, ms=3.2):
    """The BdG levels E_n against their index n, as dots, with a grey line at zero."""
    n = np.arange(1, len(e) + 1)
    style.guide(ax, y=0, lw=0.7)
    ax.plot(n, e, 'o', color=style.ACCENT, ms=ms, mec='none')
    ax.set_xlim(0, len(e) + 1); ax.set_ylim(*ylim)
    frame(ax, [(1, '1'), (len(e), str(len(e)))], yticks, r'$n$', r'$E_n/t$', fontsize=fontsize)


def draw_weight(ax, w, ylim, yticks, color=style.ACCENT, fontsize=10.5, lw=2.0, ylabel='weight'):
    """The weight of a state on each site n of the chain, as bars."""
    N = len(w)
    n = np.arange(1, N + 1)
    ax.vlines(n, 0, w, color=color, lw=lw)
    ax.set_xlim(0, N + 1); ax.set_ylim(*ylim)
    frame(ax, [(1, '1'), (N, str(N))], yticks, 'site', ylabel, fontsize=fontsize)


def levels_option(script, mu, D, N=10):
    """A picture option of the quiz of Section 5.16, the 2N BdG levels of an open chain of N=10 sites with t=1, with its axes
    and no other text. The window and the ticks are the same in the three pictures."""
    e = levels(N, 1.0, mu, D)
    print('mu', mu, 'Delta', D, 'smallest |E|', round(np.sort(np.abs(e))[0], 4), 'largest', round(e.max(), 4))
    plt.rcParams.update({'font.size': 11})
    fig, ax = plt.subplots(figsize=(3.7 * style.CM, 3.9 * style.CM))
    draw_levels(ax, e, (-4.8, 4.8), [(-4, '$-4$'), (-2, '$-2$'), (0, '$0$'), (2, '$2$'), (4, '$4$')], fontsize=11, ms=3.0)
    ax.yaxis.labelpad = 0
    style.save(fig, script)
    return e


def profile_option(script, mu, D=0.5, N=40):
    """A picture option of the quiz of Section 5.17, the weight of the lowest state of an open chain of N=40 sites with
    Delta=0.5t, with its axes and no other text. The weight axis is the same in the three pictures."""
    w, E = lowest_state(N, 1.0, mu, D)
    assert np.allclose(w, w[::-1], atol=1e-5)          # the two ends are mirror images, also when a pair at 1e-10 mixes
    print('mu', mu, 'E', E, 'weight on the four sites at each end', round(w[:4].sum() + w[-4:].sum(), 4),
          'largest', round(w.max(), 4))
    plt.rcParams.update({'font.size': 11})
    fig, ax = plt.subplots(figsize=(3.7 * style.CM, 3.9 * style.CM))
    draw_weight(ax, w, (0, 0.47), [(0, '$0$'), (0.2, '$0.2$'), (0.4, '$0.4$')], fontsize=11, lw=1.3)
    style.save(fig, script)
    return w, E
