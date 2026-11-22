"""Shared code of the helical edge of Section 5.18, used by helical_edge_gap.py and by the picture options of the quiz.

The edge of a quantum spin Hall insulator with a magnet and a pairing is, in the Nambu basis (5.6) and with the rule of
webnotes/conventions/session05.md (a term that keeps time reversal enters as tau_z h(k), an exchange field as
tau_0 B.sigma, an s-wave pairing as Delta tau_x),

    H(k) = tau_z (v k sigma_z - mu) + h sigma_x + Delta tau_x,

with sigma for the spin and tau for electron and hole, tau first in the Kronecker product. This is a continuum model that
pyqula does not have, so it is numpy, and the pictures have no download. The quiz pictures take v=1 and mu=0.2, with no
term, with the magnet h=0.5 alone or with the pairing Delta=0.3 alone. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

S0 = np.eye(2)
SX = np.array([[0., 1.], [1., 0.]])
SZ = np.diag([1., -1.])
V, MU_QUIZ = 1.0, 0.2
CASES = {'bare': (0.0, 0.0), 'magnet': (0.5, 0.0), 'pairing': (0.0, 0.3)}     # (h, Delta) of the three pictures


def bdg(k, h, D, mu, v=V):
    """The 4x4 BdG matrix of the edge at the momentum k."""
    return np.kron(SZ, v * k * SZ - mu * S0) + h * np.kron(S0, SX) + D * np.kron(SX, S0)


def levels(ks, h, D, mu, v=V):
    """The four BdG levels at each momentum of ks, sorted."""
    return np.array([np.linalg.eigvalsh(bdg(k, h, D, mu, v)) for k in ks])


def frame(ax, xticks, yticks, xlabel, ylabel, fs):
    """Left and bottom axes with ticks and names, as in the other redrawn figures of the session."""
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_linewidth(0.6)
    ax.set_xticks([t for t, _ in xticks]); ax.set_xticklabels([l for _, l in xticks], fontsize=fs - 1)
    ax.set_yticks([t for t, _ in yticks]); ax.set_yticklabels([l for _, l in yticks], fontsize=fs - 1)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(xlabel, fontsize=fs, labelpad=0); ax.set_ylabel(ylabel, fontsize=fs, labelpad=1)


def check_quiz(ks, e, kind):
    """The numbers that the feedback of the quiz states, asserted on the drawn levels."""
    h, D = CASES[kind]
    mu = MU_QUIZ
    i0 = int(np.argmin(abs(ks)))
    assert abs(ks[i0]) < 1e-12
    if kind == 'bare':
        assert np.allclose(np.sort(e[i0]), [-mu, -mu, mu, mu])                 # the branches cross each other at k=0
        for kF in (-mu / V, mu / V):                                           # and they cross zero at k = +-mu/v = +-0.2
            assert np.min(np.abs(levels([kF], h, D, mu))) < 1e-12
        assert np.min(np.abs(e)) < 1e-2
    if kind == 'magnet':
        # electron levels -mu +- sqrt(v^2 k^2 + h^2), hole levels mu +- sqrt(...), so the smallest |E| is h - mu at k=0
        ref = np.sort(np.c_[-mu + np.sqrt((V * ks)**2 + h**2), -mu - np.sqrt((V * ks)**2 + h**2),
                            mu + np.sqrt((V * ks)**2 + h**2), mu - np.sqrt((V * ks)**2 + h**2)], axis=1)
        assert np.allclose(e, ref)
        emin = np.min(np.abs(e), axis=1)
        assert abs(emin.min() - (h - mu)) < 1e-12 and abs(h - mu - 0.3) < 1e-12 and int(np.argmin(emin)) == i0
    if kind == 'pairing':
        # +-sqrt((v k -+ mu)^2 + Delta^2), smallest |E| = Delta = 0.3 at k = +-mu/v, and +-sqrt(mu^2 + Delta^2) at k=0
        emin = np.min(np.abs(e), axis=1)
        assert abs(emin.min() - D) < 1e-6 and abs(D - 0.3) < 1e-12
        kmin = abs(ks[emin < D + 1e-6])
        assert np.allclose(kmin, mu / V, atol=2e-3)
        assert np.allclose(np.sort(e[i0]), [-np.sqrt(mu**2 + D**2)] * 2 + [np.sqrt(mu**2 + D**2)] * 2)
        assert abs(np.sqrt(mu**2 + D**2) - 0.36) < 1e-2
    print(kind, 'h =', h, 'Delta =', D, 'mu =', mu, 'smallest |E| =', round(float(np.min(np.abs(e))), 4))


def option(script, kind):
    """One picture option, the BdG levels of the edge against k, with its axes and no other text."""
    ks = np.linspace(-0.65, 0.65, 651)
    h, D = CASES[kind]
    e = levels(ks, h, D, MU_QUIZ)
    check_quiz(ks, e, kind)
    plt.rcParams.update({'font.size': 11})
    fig, ax = plt.subplots(figsize=(3.7 * style.CM, 3.9 * style.CM))
    style.guide(ax, y=0)
    for j in range(4):
        ax.plot(ks, e[:, j], color=style.ACCENT, lw=1.6)
    ax.set_xlim(-0.65, 0.65); ax.set_ylim(-0.9, 0.9)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xticks([-0.2, 0.2]); ax.set_xticklabels(['$-0.2$', '$0.2$'], fontsize=10)
    ax.set_yticks([-0.3, 0, 0.3]); ax.set_yticklabels(['$-0.3$', '0', '$0.3$'], fontsize=10)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$k$', fontsize=12, labelpad=0); ax.set_ylabel(r'$E$', fontsize=12, labelpad=-2)
    style.save(fig, script)
