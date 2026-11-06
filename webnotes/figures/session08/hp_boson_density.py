"""Session 8, the boson number of the Holstein-Primakoff map S^z = S - n for a ferromagnetic site and for a site of the singlet."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

up = np.array([1., 0]); dn = np.array([0, 1.])
singlet = (np.kron(up, dn) - np.kron(dn, up)) / np.sqrt(2)
def site_probs(psi2):
    """Probabilities n=0 (spin up, S^z=+1/2) and n=1 (spin down) of the first site, from the reduced density matrix."""
    rho = psi2.reshape(2, 2) @ psi2.reshape(2, 2).T
    return np.array([rho[0, 0], rho[1, 1]])
P_fm = site_probs(np.kron(up, up))
P_sl = site_probs(singlet)
assert np.allclose(P_fm, [1, 0]) and np.allclose(P_sl, [.5, .5])
S = 0.5
nbar = [P_fm @ [0, 1], P_sl @ [0, 1]]
assert np.allclose(nbar, [0, S])                                  # <S^z> = S - <n> = 0 needs <n> = S for the singlet

fig, axs = style.plt.subplots(1, 2, figsize=(10.5 * style.CM, 5.0 * style.CM), sharey=True)
for ax, P, title, nb, col in zip(axs, (P_fm, P_sl), ('ferromagnet', 'singlet, one site'), nbar, (style.ACCENT, style.BROKEN)):
    style.arrows(ax)
    ax.bar([0, 1], P, width=0.5, color=col)
    ax.set_xlim(-0.7, 1.9); ax.set_ylim(0, 1.2)
    style.label(ax, 0.5, 1.22, title, fontsize=8.8)
    ax.set_xticks([0, 1]); ax.tick_params(axis='x', length=2.5, pad=2)
    ax.set_xlabel(r'$n$', fontsize=8.8, labelpad=2)
    style.label(ax, 1.55, 0.95, r'$\langle n\rangle=%s$' % ('0' if nb == 0 else r'\frac{1}{2}=S'), fontsize=8.5, color=col, ha='right')
axs[0].set_yticks([0, 0.5, 1]); axs[0].set_yticklabels([r'$0$', r'$\frac{1}{2}$', r'$1$']); axs[0].tick_params(axis='y', length=2.5, pad=2)
axs[0].set_ylabel('probability', fontsize=8.8)
axs[1].tick_params(axis='y', left=False)
style.save(fig, __file__)
