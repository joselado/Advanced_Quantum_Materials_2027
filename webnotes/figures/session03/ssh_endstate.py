"""Session 3, section 3.9, the end states of the open SSH chain of L sites, intracell hopping t and intercell hopping 1.

The bonds along the chain are t, 1, t, 1, ..., t, so the first and the last site are attached by the weak bond t, which is the topological
phase for t<1. Panel (a) is the amplitude of the end state of the left end, on its sublattice, for L=40, and it decays as t per cell. Panel (b)
is the smallest |E| of the open chain against L. The line is the guide t^(L/2)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style


def chain(L, t):
    H = np.zeros((L, L))
    for i in range(L - 1):
        H[i, i + 1] = H[i + 1, i] = t if i % 2 == 0 else 1.0
    return H


def lowest(L, t):
    w, v = np.linalg.eigh(chain(L, t))
    i = np.argmin(np.abs(w))
    return abs(w[i]), v[:, i]


# the numbers of the quiz of Section 3.9
print([float('%.2g' % lowest(L, 0.25)[0]) for L in (4, 8, 12)])

Ls = np.arange(4, 41, 4)
fig, axs = style.figure(ncols=2, height_cm=5.4, gridspec_kw=dict(wspace=0.42))
ax = axs[0]
j = np.arange(0, 20, 2)
ax.set_yscale('log'); ax.set_xlim(-1, 21); ax.set_ylim(3e-9, 2.5)
for t, col in ((0.25, style.ACCENT), (0.5, style.LIGHT)):
    E, v = lowest(40, t)
    # the states at +-E are mixed, so the weight on the left half is the sum of the two by symmetry
    w, V = np.linalg.eigh(chain(40, t))
    idx = np.argsort(np.abs(w))[:2]
    left = (V[:, idx[0]] + V[:, idx[1]]) / np.sqrt(2)
    left *= np.sign(left[0])
    amp = np.abs(left[:20])
    ax.plot(np.arange(20)[::2], amp[::2], 'o-', color=col, ms=3.2, lw=1.2)
    assert np.allclose(amp[::2][:6], t ** np.arange(6) * amp[0] / 1, rtol=1e-2)
style.arrows(ax, xlabel=r'site', ylabel=r'$|\psi|$ of the left end state')
ax.set_xticks([0, 10, 20]); ax.tick_params(length=2.5, width=0.6); ax.minorticks_off()
ax.set_yticks([1e-8, 1e-4, 1]); ax.set_yticklabels([r'$10^{-8}$', r'$10^{-4}$', '1'])
style.label(ax, 11.5, 0.12, r'$t=1/2$', color=style.LIGHT, fontsize=8.5)
style.label(ax, 6.5, 2e-5, r'$t=1/4$', color=style.ACCENT, fontsize=8.5)
ax.text(0.5, -0.2, '(a)', transform=ax.transAxes, ha='center', va='top', fontsize=8.5)
ax = axs[1]
ax.set_yscale('log'); ax.set_xlim(0, 44); ax.set_ylim(1e-13, 2)
for t, col in ((0.25, style.ACCENT), (0.5, style.LIGHT)):
    E = np.array([lowest(L, t)[0] for L in Ls])
    ax.plot(Ls, E, 'o-', color=col, ms=3.2, lw=1.2)
    ax.plot(Ls, t ** (Ls / 2), color=col, lw=0.8, ls=':')
style.arrows(ax, xlabel=r'$L$', ylabel=r'$|E|$ of the end states')
ax.set_xticks([0, 20, 40]); ax.tick_params(length=2.5, width=0.6); ax.minorticks_off()
ax.set_yticks([1e-12, 1e-8, 1e-4, 1]); ax.set_yticklabels([r'$10^{-12}$', r'$10^{-8}$', r'$10^{-4}$', '1'])
ax.text(0.5, -0.2, '(b)', transform=ax.transAxes, ha='center', va='top', fontsize=8.5)
style.label(ax, 32, 1e-3, r'$t=1/2$', color=style.LIGHT, fontsize=8.5)
style.label(ax, 34, 1e-7, r'$t=1/4$', color=style.ACCENT, fontsize=8.5)
style.save(fig, __file__)
