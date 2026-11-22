"""Session 9, Section 9.8, a vacancy in a Chern insulator and in a trivial insulator with the same gap.

The data come from the downloadable script webnotes/scripts/session09/g5_vacancy_honeycomb.py, a pyqula honeycomb torus
of 18x18 unit cells (648 sites, no edges), first-neighbor hopping 1. The Chern insulator is the Haldane model with
add_haldane(0.3/sqrt(3)), which is t2 = 0.15 with the phase pi/2 (the sheet of Session 3, and RECIPES.md), and the gap
6 sqrt(3) t2 = 1.559 at K and K'. The trivial insulator has t2 = 0 and add_sublattice_imbalance(0.78), the gap 2M = 1.56.
The site closest to the center is removed with h.remove_sites, and it is a site with the onsite energy +M. We plot the
local density of states summed on the three neighbors of the vacancy, with a Lorentzian broadening 0.03, next to the same
sum in the clean torus, in states per unit of t. The bulk gap is shaded. The first-neighbor hopping of pyqula is +1, and on
the bipartite honeycomb lattice its sign changes no density, so this is the numpy figure of before, which had -1. The
third model of the script, t2 = 0.15 with M = 1.0, is the picture quiz of the page (g5_quiz_vacancy_*.py)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
style.plt.rcParams.update({'font.size': 11, 'axes.labelsize': 11, 'xtick.labelsize': 10.5, 'ytick.labelsize': 10.5,
                           'legend.fontsize': 10.5})     # larger than the default, so that the labels read on a phone

d = style.run_script('session09/g5_vacancy_honeycomb.py')
E, ldos, clean, levels, weights, gaps = (d[k] for k in ('energies', 'ldos', 'ldos_clean', 'levels', 'weights', 'gaps'))
assert abs(d['eta'] - 0.03) < 1e-12 and len(d['g'].r) == 648
H = d['H']                                                          # the last model of the loop, t2=0.15 and M=1.0
assert abs(H[d['v'], d['v']].real - 1.0) < 1e-12                    # the vacancy sits on the sublattice with +M
nbr = d['nbr']                                                      # three first neighbors at the distance 1, not the vacancy
assert len(nbr) == 3 and d['v'] not in nbr and np.allclose(np.linalg.norm(d['g'].r[nbr] - d['g'].r[d['v']], axis=1), 1.0)
assert abs(gaps['chern'] - 6 * np.sqrt(3) * 0.15) < 1e-4 and abs(round(gaps['chern'], 2) - 1.56) < 1e-12
assert abs(gaps['trivial'] - 1.56) < 1e-9
edges = {}
for name in ('chern', 'trivial'):
    inside = [(x, w) for x, w in zip(levels[name], weights[name]) if abs(x) < gaps[name] / 2 - 1e-3]
    edges[name] = gaps[name] / 2
    if name == 'chern':
        assert len(inside) == 1 and abs(inside[0][0]) < 1e-9 and abs(inside[0][1] - 0.45) < 0.005   # one level at E=0, 45%
    else:
        assert len(inside) == 0                                                                   # nothing enters the gap
# in the trivial insulator the weight that the vacancy adds sits at the lower gap edge, and the gap stays empty
lo = -gaps['trivial'] / 2
win = (E > lo - 0.15) & (E < lo)
assert (ldos['trivial'][win] - clean['trivial'][win]).max() > 1.0
below = [(x, w) for x, w in zip(levels['trivial'], weights['trivial']) if lo - 0.01 < x < lo]
big = max(below, key=lambda p: p[1])
assert abs(big[0] + 0.784) < 1e-3 and big[1] > 0.3 and sum(w for x, w in below) < big[1] + 0.05   # one level at the edge
print('gaps', {k: round(v, 4) for k, v in gaps.items()}, 'peak of the Chern insulator',
      round(ldos['chern'][np.argmin(np.abs(E))], 3))

fig, axs = style.plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 5.6 * style.CM), sharey=True,
                              gridspec_kw=dict(wspace=0.18))
top = 5.6
for ax, (name, title, col) in zip(axs, (('trivial', 'trivial insulator', style.ACCENT),
                                        ('chern', 'Chern insulator', style.BROKEN))):
    ax.axvspan(-edges[name], edges[name], color=style.GRID, alpha=0.6, lw=0, zorder=0)
    ax.plot(E, clean[name], color=style.MUTED, lw=1.0)
    ax.plot(E, ldos[name], color=col, lw=1.5)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_linewidth(0.6)
    ax.set_xlim(E[0], E[-1]); ax.set_ylim(0, top)
    ax.set_xticks([-1, 0, 1]); ax.set_yticks([0, 2, 4])
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$E/t$', labelpad=1)
    ax.set_title(title, fontsize=11.5, pad=6)
    style.label(ax, -0.42 if name == 'trivial' else -0.45, top * 0.9, 'gap', color=style.MUTED, fontsize=11)
assert ldos['chern'].max() < top and ldos['trivial'].max() < top
axs[0].set_ylabel(r'LDOS, states per $t$', labelpad=2)
style.label(axs[0], 0.05, top * 0.45, 'no bound\nstate', color=style.ACCENT, fontsize=11)
style.label(axs[1], 0.1, top * 0.62, 'bound\nstate', color=style.BROKEN, fontsize=11, ha='left')
style.save(fig, __file__)
