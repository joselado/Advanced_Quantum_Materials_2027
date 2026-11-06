"""Session 3, section 3.2 and 3.3, when the first-order admixture of (3.1) can be trusted.

Two levels at -D and +D, with a perturbation of strength lambda*V that couples them. The state |m> is
mixed into |n> with the amplitude of (3.1), alpha = lambda V / (eps_n - eps_m), here |alpha| = x/2 with
x = lambda V / D. The exact amplitude is sin(theta/2) with tan(theta) = x."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

x = np.linspace(0, 3, 400)
exact = np.sin(0.5 * np.arctan(x))      # amplitude of the excited level in the perturbed ground state
first = x / 2                            # first order of (3.1)

# the exact value is checked against a direct diagonalization
for xi in (0.3, 1.0, 2.5):
    w, v = np.linalg.eigh(np.array([[-1, xi], [xi, 1]]))
    assert abs(abs(v[1, 0]) - np.sin(0.5 * np.arctan(xi))) < 1e-12

fig, ax = style.figure(height_cm=5.6)
ax.set_xlim(0, 3)
ax.set_ylim(0, 1.45)
ax.axvspan(0, 0.4, color='#e6eef6', lw=0, zorder=0)
ax.plot(x, first, color=style.BROKEN, ls=(0, (4, 2.5)), lw=1.6)
ax.plot(x, exact, color=style.ACCENT)
style.guide(ax, y=1 / np.sqrt(2), ls=':')
style.guide(ax, x=1.0, ls=':')
style.arrows(ax, xlabel=r'$\lambda V/\Delta$', ylabel=r'$\lambda|\alpha_m|$, amplitude of the other level')
style.label(ax, 1.75, 1.25, r'first order of (3.1), $\lambda|\alpha_m|=\lambda V/2\Delta$', color=style.BROKEN, fontsize=8.5)
style.label(ax, 1.9, 0.27, r'exact, $\sin\left(\frac{1}{2}\arctan\frac{\lambda V}{\Delta}\right)$', color=style.ACCENT, fontsize=8.5)
style.label(ax, 0.2, 1.1, 'the expansion\nis good', fontsize=8, color=style.MUTED)
style.label(ax, 2.75, 0.72 + 0.07, r'$1/\sqrt{2}$', fontsize=8, color=style.MUTED)
ax.text(1.0, -0.07, '1', ha='center', va='top', fontsize=8.5, color=style.INK)
ax.text(0.0, -0.07, '0', ha='center', va='top', fontsize=8.5, color=style.INK)
style.save(fig, __file__)
