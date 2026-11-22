"""Session 10, Section 10.7, a toy version of (10.11) and (10.12), with a hidden variable.

The Hamiltonian is a ring of 200 sites with first-neighbor hopping t=1, a second-neighbor hopping lambda = t2, the
parameter we want, and a random onsite energy uniform in [-W, W], the hidden variable mu. The observable O is the
fraction of the 200 levels in each of 40 bins of energy on [-3.5, 3.5], a density of states.

Left, O for t2 = 0.05 and 0.35, each for W = 0, 0.7 and 1.4. This is the pyqula script
webnotes/scripts/session10/g5_ring_dos.py, which the student downloads under the figure, checked here against the
numpy ring with the same onsite energies. Right, the predicted t2 against the true one for 200 test rings with W in
[0, 1.5], for a linear network fitted by least squares on 600 clean rings and on 600 rings with W in [0, 1.5]. This
is the toy of _g5_hlquiz.py with the seed 3, numpy, since least squares is not a pyqula call.

The SVG is the same file at every run. The clean rings of the left panel have levels exactly on a bin edge, two at
0.7 for t2=0.35 and one at -2.1 for t2=0.05, and the last digit of a diagonalization used to decide their bin; the
levels are rounded to 8 digits before the histogram, and the bins of these three levels are asserted below."""
import os, sys
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'     # small matrices, threads only cost time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import style
import _g5_hlquiz as toy
style.plt.rcParams.update({'font.size': 11, 'axes.labelsize': 11, 'xtick.labelsize': 10.5, 'ytick.labelsize': 10.5,
                           'legend.fontsize': 10.5})     # larger than the default, so that the labels read on a phone

# the left panel, from the pyqula script
d = style.run_script('session10/g5_ring_dos.py')
obs, bins = d['observables'], d['bins']
assert np.array_equal(bins, toy.BINS) and sorted(obs) == [(t2, W) for t2 in (0.05, 0.35) for W in (0.0, 0.7, 1.4)]
rng = np.random.default_rng(3)     # the same draws as the script, in the same order
for t2 in (0.05, 0.35):
    for W in (0.0, 0.7, 1.4):
        levels = np.linalg.eigvalsh(toy.ring(t2, rng.uniform(-W, W, toy.N)))
        assert np.array_equal(obs[(t2, W)], toy.histogram(levels)), (t2, W)     # pyqula is the numpy ring
        assert abs(obs[(t2, W)].sum() - 1) < 1e-12                                # no level outside the window
# the levels on a bin edge, -2 - 2 t2 = -2.1 at k=0 and 2 t2 = 0.7 twice at k = +-pi/2, fall in a fixed bin
for t2, E, n in ((0.05, -2.1, 1), (0.35, 0.7, 2)):
    lv = np.linalg.eigvalsh(toy.ring(t2, np.zeros(toy.N)))
    on = lv[np.abs(lv - E) < 1e-12]
    assert len(on) == n and np.min(np.abs(bins - E)) < 1e-12
    assert set(np.searchsorted(bins, np.round(on, 8), side='right') - 1) == {int(np.argmin(np.abs(bins - E)))}

# the right panel, the toy with the seed of the figure, and the numbers of the caption: 0.06, 0.10 for W>1, 0.004
r = toy.toy(toy.SEED)
toy.check_seed3(r)
assert round(r['clean_rms'], 2) == 0.06 and round(r['clean_rms_W1'], 2) == 0.10 and round(r['disorder_rms'], 3) == 0.004
assert len(r['true']) == 200 and np.all((r['W'] >= 0) & (r['W'] <= 1.5)) and r['clean_below'] > 0.5

fig, axs = style.plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 5.6 * style.CM),
                              gridspec_kw=dict(wspace=0.36, width_ratios=[1.3, 1]))
ax = axs[0]
ec = 0.5 * (bins[1:] + bins[:-1])
for t2, col in ((0.05, style.ACCENT), (0.35, style.BROKEN)):
    for W in (0.0, 0.7, 1.4):
        ax.plot(ec, obs[(t2, W)], color=col, lw=1.0 + 0.6 * (W == 0.0), alpha=1.0 if W == 0 else 0.6)
style.arrows(ax, xlabel=r'$E/t$', ticks=True)
ax.set_ylabel(r'$\mathcal{O}$, fraction of levels per bin', fontsize=10.5, labelpad=3)
ax.set_xlim(-3.5, 3.5); ax.set_ylim(0, 0.34)
ax.set_xticks([-3, -2, -1, 0, 1, 2, 3]); ax.set_xticklabels(['$-3$', '$-2$', '$-1$', '0', '1', '2', '3'])
ax.set_yticks([0, 0.1, 0.2, 0.3]); ax.set_yticklabels(['0', '0.1', '0.2', '0.3'])
ax.tick_params(length=2.5, width=0.6, pad=2)
style.label(ax, -3.3, 0.315, r'$t_2=0.05$', color=style.ACCENT, fontsize=11.5, ha='left')
style.label(ax, 1.9, 0.315, r"$t_2=0.35$", color=style.BROKEN, fontsize=11.5, ha='left')

ax = axs[1]
ax.plot([0, 0.42], [0, 0.42], color=style.GRID, lw=1.2, zorder=0)
ax.scatter(r['true'], r['clean'], color=style.BROKEN, s=6, lw=0)
ax.scatter(r['true'], r['disorder'], color=style.ACCENT, s=6, lw=0)
style.arrows(ax, xlabel=r'true $t_2$', ylabel=r'predicted $t_2$', ticks=True)
ax.set_xlim(0, 0.42); ax.set_ylim(*toy.YLIM)
ax.set_xticks([0, 0.2, 0.4]); ax.set_xticklabels(['0', '0.2', '0.4'])
ax.set_yticks([0, 0.2, 0.4]); ax.set_yticklabels(['0', '0.2', '0.4'])
ax.tick_params(length=2.5, width=0.6, pad=2)
style.label(ax, 0.02, 0.43, 'trained with\ndisorder', color=style.ACCENT, fontsize=11, ha='left', va='top')
style.label(ax, 0.02, 0.30, 'trained on\nclean rings', color=style.BROKEN, fontsize=11, ha='left', va='top')
style.save(fig, __file__)
