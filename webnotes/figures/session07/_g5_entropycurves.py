"""Shared code of the three picture options of the quiz of Section 7.11, the entropy of a block of l sites against l.

The critical and the dimerized curves are free fermions at half filling from pyqula, on an open chain of N=402 sites
with the block in the middle, the same two models as the pyqula script entropy_critical_chain.py of the main figure
(geometry.chain() with hopping 1, and geometry.bichain() with h.inter times 0.6, blocks of whole cells, so both ends cut
a bond 0.6). The chain is shorter than the 3002 sites of the main figure, so that each option takes about a second. The
volume law is S = l log 2, the largest entropy of l spins one-half. The entropy is in nats. The three pictures share
the axes, l from 2 to 100 on a logarithmic axis and S from 0 to 2.5. pyqula is called in a temporary folder, so no file
is written next to the figures. This file writes no figure."""
import os, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

N = 402
ELLS = np.array([2, 4, 6, 8, 10, 14, 20, 28, 40, 56, 80, 100])
SMAX = 2.5


def _blocks(hf):
    starts = [2 * ((N // 2 - l // 2) // 2) for l in ELLS]
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as d:
        os.chdir(d)
        try:
            S = [hf.get_entanglement_entropy(region=list(range(s, s + l))) for (s, l) in zip(starts, ELLS)]
        finally:
            os.chdir(cwd)
    return ELLS.astype(float), np.array(S)


def critical():
    """The uniform chain of free fermions, the XX chain, on N sites."""
    from pyqula import geometry
    hf = geometry.chain().get_hamiltonian(has_spin=False).set_finite_system(n=N)
    return _blocks(hf)


def dimerized():
    """The chain of free fermions with the hoppings 1 inside the cell and 0.6 between the cells, on N sites."""
    from pyqula import geometry
    h = geometry.bichain().get_hamiltonian(has_spin=False)
    h.inter = 0.6 * h.inter
    return _blocks(h.set_finite_system(n=N // 2))


def volume():
    """The volume law S = l log 2, drawn until it leaves the frame at S = 2.5."""
    l = np.linspace(2, SMAX / np.log(2), 50)
    return l, l * np.log(2)


def option(script, ell, S, color):
    """One picture, with its axes and no other text, the same frame in the three pictures."""
    plt.rcParams.update({'font.size': 11})
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 3.9 * style.CM))
    ax.semilogx(ell, S, color=color, lw=1.5, marker='o' if len(ell) < 20 else None, ms=2.6, clip_on=True)
    ax.set_xlim(2, 100); ax.set_ylim(0, SMAX)
    ax.set_xticks([2, 10, 100]); ax.set_xticklabels([r'$2$', r'$10$', r'$100$']); ax.minorticks_off()
    ax.set_yticks([0, 0.5, 1, 2]); ax.set_yticklabels([r'$0$', r'$0.5$', r'$1$', r'$2$'])
    ax.tick_params(length=2.5, width=0.6, pad=2)
    style.arrows(ax, xlabel=r'$\ell$', ylabel=r'$S$', ticks=True)
    style.save(fig, script)
