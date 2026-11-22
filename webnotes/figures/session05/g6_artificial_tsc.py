"""Session 5, section 5.18, the artificial topological superconductor of the notebook against the exchange field.

The data come from the downloadable script webnotes/scripts/session05/g6_artificial_tsc.py, the cell "Topological phase
transition as a function of the exchange field" of session5.ipynb. The lattice is triangular with the hopping +1 of
pyqula, which is t=-1 of the notes, so the bare band runs from -3 at K to 6 at Gamma and the energies are in units of
|t|. add_onsite(-5.7) puts the band at Gamma at eps_Gamma = 6 - 5.7 = 0.3, which is the top of the band before the
Rashba term, and then come add_rashba(1.0), add_zeeman([0,0,J]) and add_swave(0.3). With the Rashba term Gamma is the
Kramers crossing of the two Rashba bands, and the Fermi level cuts them on two closed lines around Gamma, one at |k| below
0.1 and one at |k| of about 1.75. At Gamma the Rashba coupling vanishes and the four BdG levels are +-J +- sqrt(eps_Gamma^2 + Delta^2),
so the level closest to zero is |J - 0.4243| and it closes at J = 0.4243. The curve is the smallest |E| on the line M,
Gamma, M, which the check of the page compares with a minimization over the whole zone at all 41 values of J. At J=0
it is Delta=0.3, on the Fermi lines, and from J=0.225 on it is the level at Gamma. The dots come down almost to zero at
J=0.42, the point of the grid next to the closing, while the dashed line touches zero at J=0.4243. The Chern number of
the BdG bands below zero, from h.get_chern(nk=40), is 0 at J=0.3 and 1 at J=0.6, as webnotes/conventions/session05.md
says, and the check of the page gets the same from the link variables of physcheck."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

d = style.run_script('session05/g6_artificial_tsc.py')
Js, emin = np.array(d['Js']), np.array(d['emin'])
D, epsG = 0.3, 0.3
Jc = np.sqrt(epsG**2 + D**2)
assert abs(Jc - 0.4243) < 5e-5 and abs(round(Jc, 2) - 0.42) < 1e-12
assert len(Js) == 41 and abs(Js[0]) < 1e-12 and abs(Js[-1] - 0.6) < 1e-12

# the levels at Gamma, +-J +- sqrt(eps_Gamma^2 + Delta^2), the band at Gamma at 0.3 and the Fermi lines are asserted on
# pyqula in webnotes/checks/session05/g6_18_engineered_tsc.py, with the minimization over the whole zone
gamma = np.abs(Js - Jc)                                   # the level at Gamma closest to zero
assert abs(emin[0] - D) < 1e-3                            # at J=0 the smallest energy is Delta, on the Fermi lines
assert abs(gamma[0] - 0.4243) < 1e-4                      # while the level at Gamma is 0.42
assert np.all(emin <= gamma + 1e-9)
on_gamma = np.abs(emin - gamma) < 1e-6
first = int(np.argmax(on_gamma))
assert np.all(on_gamma[first:]) and not np.any(on_gamma[:first]) and abs(Js[first] - 0.225) < 1e-9   # from J=0.225 on
i = int(np.argmin(emin))
assert abs(Js[i] - 0.42) < 1e-9 and 3e-3 < emin[i] < 5e-3  # the dip, almost zero, next to the closing at 0.4243
on = Js >= 0.225                                           # from J of about 0.2 on, the curve lies on the dashed line
assert np.all(np.abs(emin[on] - np.abs(Js[on] - Jc)) < 1e-3)
Jf = np.linspace(0, 0.6, 601)
jd = int(np.argmin(np.abs(Jf - Jc)))
assert abs(Jf[jd] - 0.424) < 1e-9 and np.abs(Jf - Jc).min() < 3e-4  # the dashed line touches zero at the closing
assert np.allclose(d['Jc'], [0.3, 0.6]) and np.allclose(d['cherns'], [0, 1], atol=1e-6)
print('closing at J =', round(Jc, 4), 'smallest |E| at J=0', round(emin[0], 4), 'on Gamma from J =', Js[first],
      'dip', round(emin[i], 5), 'at J =', Js[i], 'Chern numbers', np.round(d['cherns'], 6))

FS = 11
plt.rcParams.update({'font.size': FS})
fig, ax = plt.subplots(figsize=(10.5 * style.CM, 6.2 * style.CM))
style.guide(ax, x=Jc, color=style.MUTED, lw=0.8, ls=(0, (3, 2)))
ax.plot(Jf, np.abs(Jf - Jc), color=style.BROKEN, lw=1.2, ls=(0, (4, 2)), zorder=2)
ax.plot(Js, emin, color=style.ACCENT, lw=1.6, marker='o', ms=3.2, zorder=3)
style.label(ax, 0.12, 0.13, '$C=0$', fontsize=FS)
style.label(ax, 0.53, 0.30, '$C=1$', fontsize=FS)
ax.set_xlim(0, 0.6); ax.set_ylim(0, 0.46)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
for s in ('left', 'bottom'):
    ax.spines[s].set_linewidth(0.6)
ax.set_xticks([0, 0.2, Jc, 0.6]); ax.set_xticklabels(['0', '0.2', '0.42', '0.6'], fontsize=FS - 1)
ax.set_yticks([0, 0.1, 0.2, D, Jc]); ax.set_yticklabels(['0', '0.1', '0.2', '0.3', '0.42'], fontsize=FS - 1)
ax.tick_params(length=2.5, width=0.6, pad=2)
ax.set_xlabel(r'exchange field $J/|t|$', fontsize=FS, labelpad=1)
ax.set_ylabel(r'$E_\mathrm{min}/|t|$', fontsize=FS, labelpad=2)
style.save(fig, __file__)
