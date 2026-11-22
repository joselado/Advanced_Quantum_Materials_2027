"""Session 9, Section 9.10a, the shared code of the three pictures of the quiz on the eigenstates of the Aubry-Andre chain.

Each picture is the weight |psi_n|^2 of the lowest eigenstate of a ring of 233 sites, with q = 144/233 and phi = 0.3, for
V0 = t, 2t and 3t, on a logarithmic axis. The three pictures have the same axes and the same ticks and no other text,
since they are the options of a quiz. The calculation is the pyqula script webnotes/scripts/session09/g6_aah_states.py,
which also gives the same state on rings of 55 and 987 sites for the feedback. The lowest level is not degenerate, since
its distance to the next level is checked, so the picture does not depend on how the solver mixes degenerate states.
This file writes no figure."""
import os, sys
os.environ['OMP_NUM_THREADS'] = '1'          # one thread and the reproducible mode of MKL, so that the SVG is the same at
os.environ['OPENBLAS_NUM_THREADS'] = '1'     # every run
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['MKL_CBWR'] = 'COMPATIBLE'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

N = 233
YMIN = 1e-10


def option(script, V0):
    """One picture option, |psi_n|^2 of the lowest state against the site n, with its axes and no other text.
    Returns the variables of the pyqula script, for the asserts of the option script."""
    d = style.run_script('session09/g6_aah_states.py')
    w = d['weight'][(N, V0)]
    assert abs(w.sum() - 1) < 1e-10 and len(w) == N
    assert min(d['spacing'][(n, V0)] for n in (55, 233, 987)) > 1e-6       # the lowest level is not degenerate
    print(os.path.basename(script), 'V0 =', V0, ' IPR on 55, 233, 987 sites:',
          [round(float(d['ipr'][(n, V0)]), 4) for n in (55, 233, 987)], ' largest weight', round(float(w.max()), 3),
          ' smallest', '%.1e' % w.min())
    plt.rcParams.update({'savefig.dpi': 220})
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 3.4 * style.CM))
    ax.semilogy(np.arange(N), np.maximum(w, YMIN * 1e-3), color=style.ACCENT, lw=0.9)
    ax.set_xlim(0, N - 1); ax.set_ylim(YMIN, 2)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    for sp in ('left', 'bottom'):
        ax.spines[sp].set_linewidth(0.6); ax.spines[sp].set_color(style.INK)
    ax.set_xticks([0, 100, 200]); ax.set_xticklabels(['0', '100', '200'], fontsize=10.5)
    ax.set_yticks([1e-10, 1e-5, 1]); ax.set_yticklabels([r'$10^{-10}$', r'$10^{-5}$', r'$1$'], fontsize=10.5)
    ax.minorticks_off()
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'site $n$', fontsize=11.5, labelpad=0); ax.set_ylabel(r'$|\psi_n|^2$', fontsize=11.5, labelpad=1)
    style.save(fig, script)
    return d
