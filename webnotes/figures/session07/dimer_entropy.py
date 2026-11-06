"""Session 7, the entanglement entropy of the dimer product state (7.8) for a block of sites, computed exactly."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

N = 12
singlet = np.array([[0, 1], [-1, 0]]) / np.sqrt(2)      # (|ud> - |du>)/sqrt(2)
psi = np.array([1.0])
for n in range(N // 2):
    psi = np.kron(psi, singlet.reshape(4))
psi = psi.reshape((2,) * N)
assert abs(np.linalg.norm(psi) - 1) < 1e-12

def entropy(sites):
    rest = [i for i in range(N) if i not in sites]
    m = np.transpose(psi, list(sites) + rest).reshape(2 ** len(sites), -1)
    p = np.linalg.svd(m, compute_uv=False) ** 2
    p = p[p > 1e-14]
    return -np.sum(p * np.log(p))

ells = np.arange(1, 11)
S = np.array([entropy(list(range(1, l + 1))) for l in ells]) / np.log(2)
assert np.allclose(S, np.where(ells % 2 == 1, 1, 2)), S      # one cut dimer for odd blocks, two for even ones

fig, ax = style.figure(height_cm=5.2)
ax.plot(ells, ells, color=style.GRID, lw=1.4, ls=(0, (3, 3)))
ax.plot(ells, S, color=style.ACCENT, marker='o', ms=4)
ax.set_xlim(0, 10.8); ax.set_ylim(0, 10.8)
style.arrows(ax, xlabel=r'$\ell$', ylabel=r'$S/\log 2$')
style.label(ax, 4.2, 6.5, r'volume law, $S=\ell\log 2$', color=style.MUTED, fontsize=8.5, ha='right')
style.label(ax, 10.5, 4.4, 'dimer product state', color=style.ACCENT, fontsize=8.5, ha='right')
style.label(ax, 10.5, 3.6, 'one or two cut singlets', color=style.ACCENT, fontsize=8.5, ha='right')
style.save(fig, __file__)
