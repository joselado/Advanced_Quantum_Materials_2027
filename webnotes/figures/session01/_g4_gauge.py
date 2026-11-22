"""Shared code of the picture options of the quiz of Section 1.15 that asks which picture shows the pairing amplitude
Delta of (1.9) after the gauge transformation (1.10) with phi = pi/4. This file writes no figure.

A picture is the complex plane with the axes Re and Im in units of |Delta|, the unit circle, Delta before the
transformation as a dashed grey arrow along the positive real axis, and the arrow after it. Under (1.10) each
annihilation operator gets e^{i phi}, so <c_i c_j> gets e^{2 i phi}, which for phi = pi/4 is a turn by pi/2 to the
positive imaginary axis. The check builds the gauge transformation as the operator exp(-i phi N) on the Fock space of
two fermionic modes with numpy, and asserts the turn of c_i c_j and that c^dagger c does not turn."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style


def check():
    # two fermionic modes with the Jordan-Wigner signs, |n0 n1> with c_0 the last Kronecker factor
    a, Z, I = np.array([[0., 1.], [0., 0.]]), np.diag([1., -1.]), np.eye(2)
    c0, c1 = np.kron(I, a), np.kron(a, Z)
    assert np.allclose(c0 @ c1 + c1 @ c0, 0) and np.allclose(c0 @ c0.T + c0.T @ c0, np.eye(4))
    N = c0.T @ c0 + c1.T @ c1
    phi = np.pi / 4
    G = np.diag(np.exp(1j * phi * np.diag(N)))                 # exp(i phi N), N is diagonal in this basis
    gauge = lambda op: G.conj().T @ op @ G                      # the operator identity e^{-i phi N} op e^{i phi N}
    assert np.allclose(gauge(c0), np.exp(1j * phi) * c0)       # c -> c e^{i phi}, as (1.10) writes it
    assert np.allclose(gauge(c0.T), np.exp(-1j * phi) * c0.T)  # c^dagger -> c^dagger e^{-i phi}
    assert np.allclose(gauge(c0.T @ c1), c0.T @ c1)            # a term c^dagger c does not turn
    assert np.allclose(gauge(c0 @ c1), 1j * (c0 @ c1))         # the pair gets e^{2 i phi} = i, a turn by pi/2
    assert np.isclose(np.exp(2j * phi), 1j) and not np.isclose(np.exp(1j * phi), 1j)


def option(script, angle):
    """One picture, Delta before (dashed) and after the transformation (solid), turned by the angle."""
    check()
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 3.9 * style.CM))
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(th), np.sin(th), color=style.GRID, lw=1.0)
    ax.axhline(0, color=style.GRID, lw=0.8, zorder=0); ax.axvline(0, color=style.GRID, lw=0.8, zorder=0)
    kw = dict(arrowstyle='-|>', lw=1.8, mutation_scale=11, shrinkA=0, shrinkB=0)
    ax.annotate('', xy=(1, 0), xytext=(0, 0), arrowprops=dict(kw, color=style.MUTED, ls=(0, (3, 2)), lw=1.3))
    ax.annotate('', xy=(np.cos(angle), np.sin(angle)), xytext=(0, 0), arrowprops=dict(kw, color=style.ACCENT))
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xlim(-1.25, 1.25); ax.set_ylim(-1.25, 1.25); ax.set_aspect('equal')
    ax.set_xticks([-1, 0, 1]); ax.set_xticklabels([r'$-1$', '0', '1'], fontsize=11)
    ax.set_yticks([-1, 0, 1]); ax.set_yticklabels([r'$-1$', '0', '1'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'Re $\Delta$', fontsize=12, labelpad=0); ax.set_ylabel(r'Im $\Delta$', fontsize=12, labelpad=0)
    style.save(fig, script)
