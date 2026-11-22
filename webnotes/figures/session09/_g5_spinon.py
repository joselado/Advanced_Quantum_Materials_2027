"""Shared code of the picture options of the quiz of Section 9.9 on three gapped spinon chains.

The data come from the downloadable script webnotes/scripts/session09/g5_spinon_chain_field.py, the same calculation as the
figure spinon_impurity: an open chain of 2000 sites with chi alternating 1 and chi_2, half filling, a field h = 0.1 on the
central site, and the induced moment <S^z_n>. The chains have chi_2 = 0.6, 0.8 and 0.9, so the gaps 2(1 - chi_2) are 0.8, 0.4
and 0.2. Each picture shows |<S^z_n>| for n = 1 to 40 on a logarithmic axis, with the points above 1e-8 and their logarithm
rounded to 0.01 of a decade, as the figure does, so that the SVG is the same at every run. The three share the window, the
ticks and one color, and they have no other text. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style


def option(script, chi2):
    """Draws |<S^z_n>| of the chain with the weak hopping chi2, and returns the moment on every site and the central site."""
    d = style.run_script('session09/g5_spinon_chain_field.py')
    m, c = d['moments'][chi2], d['c']
    n = np.arange(1, 41)
    y = np.abs(m[c + n])
    keep = y >= 1e-8
    plt.rcParams.update({'font.size': 11})
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 3.9 * style.CM))
    ax.semilogy(n[keep], 10 ** np.round(np.log10(y[keep]), 2), 'o', color=style.ACCENT, ms=2.2)
    ax.set_xlim(0, 42); ax.set_ylim(1e-8, 0.05)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_linewidth(0.6)
    ax.set_xticks([0, 20, 40]); ax.set_yticks([1e-8, 1e-5, 1e-2])
    ax.minorticks_off()
    ax.tick_params(length=2.5, width=0.6, pad=2, labelsize=10.5)
    ax.set_xlabel(r'$n$', fontsize=11, labelpad=1)
    ax.set_ylabel(r'$|\langle S^z_n\rangle|$', fontsize=11, labelpad=1)
    style.save(fig, script)
    return m, c
