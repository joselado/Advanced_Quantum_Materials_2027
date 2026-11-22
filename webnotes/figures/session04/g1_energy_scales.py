"""Session 4, Section 4.1, the energy scale of the Landau levels of GaAs and of graphene against the field.

Two closed formulas with the constants of the two materials, so numpy and no pyqula: the level spacing
hbar omega_c = hbar e B / m* of GaAs with m* = 0.067 m_e, and the first Dirac level E_1 = v sqrt(2 hbar e B) of
graphene with v = 1e6 m/s, from 0 to 10 T, in meV. The dots are at 1, 4 and 10 T, the fields that the quiz, the
problem and the caption quote, and the asserts check every number that the page quotes about this figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

HBAR, E, ME, KB = 1.054571817e-34, 1.602176634e-19, 9.1093837015e-31, 1.380649e-23
MSTAR, V = 0.067 * ME, 1e6


def gaas(B):
    """hbar omega_c of GaAs in meV, B in T."""
    return HBAR * E * B / MSTAR / E * 1e3


def graphene(B):
    """E_1 = v sqrt(2 hbar e B) of graphene in meV, B in T."""
    return V * np.sqrt(2 * HBAR * E * B) / E * 1e3


# the numbers of the caption, the quiz and the problem of the page, and the conventions sheet
assert abs(gaas(1) - 1.73) < 0.005 and abs(gaas(4) - 6.91) < 0.005 and abs(gaas(10) - 17.28) < 0.005
assert abs(graphene(1) - 36.3) < 0.05 and abs(graphene(4) - 72.6) < 0.05 and abs(graphene(10) - 114.7) < 0.05
assert abs(graphene(10) / gaas(10) - 6.64) < 0.005 and abs(graphene(1) / gaas(1) - 21.0) < 0.05
assert np.isclose(gaas(4) / gaas(1), 4) and np.isclose(graphene(4) / graphene(1), 2)
assert abs(gaas(10) * 1e-3 * E / KB - 200.5) < 0.1 and abs(graphene(10) * 1e-3 * E / KB - 1331.5) < 0.1
# the two curves never cross above zero field, since their ratio grows as 1/sqrt(B) toward small fields
Bs = np.linspace(0, 10, 501)
assert np.all(graphene(Bs[1:]) > gaas(Bs[1:]))
print('GaAs at 1, 4, 10 T', np.round(gaas(np.array([1., 4., 10.])), 2), 'meV, graphene',
      np.round(graphene(np.array([1., 4., 10.])), 1), 'meV, ratio at 10 T', round(graphene(10) / gaas(10), 2))

fig, ax = style.figure(height_cm=5.6, width_cm=10.0)
ax.set_xlim(0, 10.6); ax.set_ylim(0, 130)
marks = np.array([1., 4., 10.])
for b in marks:
    style.guide(ax, x=b, ls=':', lw=0.8)
ax.plot(Bs, graphene(Bs), color=style.BROKEN)
ax.plot(Bs, gaas(Bs), color=style.ACCENT)
ax.scatter(marks, graphene(marks), s=14, color=style.BROKEN, zorder=5, clip_on=False)
ax.scatter(marks, gaas(marks), s=14, color=style.ACCENT, zorder=5, clip_on=False)
style.label(ax, 3.4, 100, r'graphene, $E_1$', color=style.BROKEN, fontsize=9.5)
style.label(ax, 7.0, 26, r'GaAs, $\hbar\omega_c$', color=style.ACCENT, fontsize=9.5)
style.arrows(ax, xlabel=r'$B$ (T)', ylabel=r'$E$ (meV)', ticks=True)
ax.set_xticks([0, 1, 4, 10]); ax.set_xticklabels(['0', '1', '4', '10'])
ax.set_yticks([0, 17.3, 36.3, 72.6, 114.7]); ax.set_yticklabels(['0', '17', '36', '73', '115'])
ax.tick_params(length=2.5, width=0.6)
style.save(fig, __file__)
