"""Session 3, section 3.3, the overlap of the ground state before and after a local impurity.

A ring of N sites at half filling, hopping t=1, with an impurity of strength V on one site. The overlap is
|det(U0^dagger U1)| of the occupied orbitals of the two Hamiltonians. In a metal it keeps falling as a power
law of N, which is the orthogonality catastrophe. With a staggered potential +-1 on the sites, which opens a
gap of 2, the overlap saturates at a value close to one already at N=10."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style


def ring(N, V=0.0, stag=0.0):
    H = np.zeros((N, N))
    for i in range(N):
        H[i, (i + 1) % N] = H[(i + 1) % N, i] = -1.0
        H[i, i] = stag * (-1) ** i
    H[0, 0] += V
    return H


def overlap(N, V, stag):
    w0, v0 = np.linalg.eigh(ring(N, 0, stag))
    w1, v1 = np.linalg.eigh(ring(N, V, stag))
    return abs(np.linalg.det(v0[:, :N // 2].T @ v1[:, :N // 2]))


Ns = np.array([10, 18, 34, 66, 130, 258, 514, 1026, 1602])      # N = 4m+2, a closed shell in the metal
cases = {('metal', 3): (3.0, 0.0), ('metal', 1): (1.0, 0.0), ('gap', 3): (3.0, 1.0), ('gap', 1): (1.0, 1.0)}
data = {k: np.array([overlap(N, *p) for N in Ns]) for k, p in cases.items()}
for k in (('metal', 3), ('metal', 1)):
    sl = np.polyfit(np.log(Ns[-5:]), np.log(data[k][-5:]), 1)[0]
    print(k, 'exponent', -sl)
print({k: v[-1] for k, v in data.items()})

fig, ax = style.figure(height_cm=5.6)
ax.set_xscale('log')
ax.set_xlim(8, 1.5e3)
ax.set_ylim(0.62, 1.03)
ax.plot(Ns, data[('metal', 3)], color=style.ACCENT)
ax.plot(Ns, data[('metal', 1)], color=style.LIGHT)
ax.plot(Ns, data[('gap', 3)], color=style.BROKEN, ls=(0, (4, 2.5)), lw=1.6)
ax.plot(Ns, data[('gap', 1)], color=style.WARM, ls=(0, (4, 2.5)), lw=1.6)
style.guide(ax, y=1.0, ls=':')
style.arrows(ax, xlabel=r'$N$', ylabel=r'overlap $|\langle\Psi_0|\Psi_V\rangle|$')
ax.minorticks_off()
ax.set_xticks([10, 100, 1000]); ax.set_xticklabels(['10', '100', '1000'])
ax.set_yticks([0.7, 0.8, 0.9, 1.0]); ax.set_yticklabels(['0.7', '0.8', '0.9', '1'])
ax.tick_params(length=2.5, width=0.6)
style.label(ax, 300, 0.675, r'metal, $V=3$', color=style.ACCENT, fontsize=8.5)
style.label(ax, 300, 0.915, r'metal, $V=1$', color=style.LIGHT, fontsize=8.5)
style.label(ax, 250, 1.017, r'gapped, $V=1$ and $V=3$', color=style.BROKEN, fontsize=8.5)
style.save(fig, __file__)
