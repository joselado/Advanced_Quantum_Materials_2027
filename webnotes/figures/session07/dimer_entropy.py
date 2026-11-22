"""Session 7, the entanglement entropy of the dimer product state (7.8) for a block of sites, computed exactly.

Redrawn on 2026-11-22 under the same name with its axes and ticks, by the rule of 2026-11-21. The state is a spin
state, so it is numpy and has no pyqula script. The singlets sit on (0,1), (2,3), ..., and the block starts at site 1.
The values are the same on 12 and on 16 sites, since a product state does not feel the sites outside its cut dimers."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

singlet = np.array([[0, 1], [-1, 0]]) / np.sqrt(2)      # (|ud> - |du>)/sqrt(2)


def block_entropies(N, ells):
    psi = np.array([1.0])
    for n in range(N // 2):
        psi = np.kron(psi, singlet.reshape(4))                # site 0 is the first factor
    psi = psi.reshape((2,) * N)
    assert abs(np.linalg.norm(psi) - 1) < 1e-12
    out = []
    for l in ells:
        sites = list(range(1, l + 1))
        rest = [i for i in range(N) if i not in sites]
        m = np.transpose(psi, sites + rest).reshape(2 ** len(sites), -1)
        p = np.linalg.svd(m, compute_uv=False) ** 2
        p = p[p > 1e-14]
        out.append(-np.sum(p * np.log(p)))
    return np.array(out) / np.log(2)


ells = np.arange(1, 11)
S = block_entropies(12, ells)
assert np.allclose(S, np.where(ells % 2 == 1, 1, 2)), S      # one cut dimer for odd blocks, two for even ones
assert np.allclose(block_entropies(16, ells), S)              # the same in a longer chain

fig, ax = style.figure(height_cm=5.2)
ax.plot([0, 6.2], [0, 6.2], color=style.MUTED, lw=1.2, ls=(0, (3, 3)))
ax.plot(ells, S, color=style.ACCENT, marker='o', ms=4)
ax.set_xlim(0, 10.8); ax.set_ylim(0, 6.2)
style.arrows(ax, xlabel=r'$\ell$, sites in the block', ylabel=r'$S/\log 2$', ticks=True)
ax.set_xticks(list(ells)); ax.set_yticks([1, 2, 5])
ax.tick_params(length=2.5, pad=2); ax.minorticks_off()
style.label(ax, 5.1, 5.6, r'volume law, $S=\ell\log 2$', color=style.MUTED, fontsize=8.5, ha='right')
style.label(ax, 10.6, 3.2, 'dimer product state', color=style.ACCENT, fontsize=8.5, ha='right')
style.save(fig, __file__)
