"""Session 10, Section 10.7, a toy version of (10.11) and (10.12), with a hidden variable.

The Hamiltonian is a ring of 200 sites with first-neighbor hopping t=1, a second-neighbor hopping lambda = t2,
the parameter we want, and a random onsite energy uniform in [-W, W], the hidden variable mu. W is drawn uniform
in [0, 1.5] for each sample, with its own random realization. The observable O is the density of states,
a histogram of the eigenvalues in 40 bins on [-3.5, 3.5]. The network is the simplest one, a linear map from the
40 numbers of O to lambda with no hidden layer, fitted by least squares, which is (10.12). It is trained twice on
600 samples with t2 uniform in [0, 0.4], once on clean rings only (W=0) and once with W in [0, 1.5], and both are
tested on the same 200 disordered samples. The seed is fixed.
Left, O for two values of t2, each with three realizations of the hidden disorder. Right, the predicted t2
against the true one for the test set, for the two training sets."""
import os, sys
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'     # small matrices, threads only cost time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
style.plt.rcParams.update({'font.size': 11, 'axes.labelsize': 11, 'xtick.labelsize': 10.5, 'ytick.labelsize': 10.5,
                           'legend.fontsize': 10.5})     # larger than the default, so that the labels read on a phone

rng = np.random.default_rng(3)
N, NB = 200, 40
bins = np.linspace(-3.5, 3.5, NB + 1)
i = np.arange(N)


def observable(t2, W):
    H = np.diag(rng.uniform(-W, W, N))
    H[i, (i + 1) % N] = H[(i + 1) % N, i] = -1.0
    H[i, (i + 2) % N] = H[(i + 2) % N, i] = -t2
    c, _ = np.histogram(np.linalg.eigvalsh(H), bins=bins)
    return c / N


def sample(n, Wmax):
    lam = rng.uniform(0, 0.4, n)
    W = rng.uniform(0, Wmax, n)
    O = np.array([observable(a, b) for a, b in zip(lam, W)])
    return O, lam, W


Ote, lte, Wte = sample(200, 1.5)
pred, rms = {}, {}
for Wmax in (0.0, 1.5):
    Otr, ltr, _ = sample(600, Wmax)
    X = np.hstack([Otr, np.ones((len(Otr), 1))])
    theta, *_ = np.linalg.lstsq(X, ltr, rcond=None)
    pred[Wmax] = np.hstack([Ote, np.ones((len(Ote), 1))]) @ theta
    rms[Wmax] = np.sqrt(((pred[Wmax] - lte) ** 2).mean())
    print('trained with W up to %.1f: test RMS error of t2 %.4f, for test samples with W>1 %.4f' %
          (Wmax, rms[Wmax], np.sqrt(((pred[Wmax] - lte)[Wte > 1] ** 2).mean())))

fig, axs = style.plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 5.4 * style.CM),
                              gridspec_kw=dict(wspace=0.32, width_ratios=[1.3, 1]))
ax = axs[0]
ec = 0.5 * (bins[1:] + bins[:-1])
for t2, col in ((0.05, style.ACCENT), (0.35, style.BROKEN)):
    for W in (0.0, 0.7, 1.4):
        ax.plot(ec, observable(t2, W), color=col, lw=1.0 + 0.5 * (W == 0.0), alpha=1.0 if W == 0 else 0.6)
style.arrows(ax, xlabel=r'$E/t$', ylabel=r'$\mathcal{O}$, density of states')
ax.set_xlim(-3.5, 3.5); ax.set_ylim(0, None)
ax.set_xticks([-2, 0, 2]); ax.tick_params(axis='x', length=2.5, pad=2)
top = ax.get_ylim()[1]
style.label(ax, -3.3, top * 0.93, r'$t_2=0.05$', color=style.ACCENT, fontsize=11.5, ha='left')
style.label(ax, 2.0, top * 0.93, r'$t_2=0.35$', color=style.BROKEN, fontsize=11.5, ha='left')

ax = axs[1]
ax.plot([0, 0.4], [0, 0.4], color=style.GRID, lw=1.2, zorder=0)
ax.scatter(lte, pred[0.0], color=style.BROKEN, s=6, lw=0)
ax.scatter(lte, pred[1.5], color=style.ACCENT, s=6, lw=0)
style.arrows(ax, xlabel=r'true $t_2$', ylabel=r'predicted $t_2$')
ax.set_xlim(0, 0.42); ax.set_ylim(min(-0.02, pred[0.0].min() - 0.02), max(0.44, pred[0.0].max() + 0.02))
ax.set_xticks([0, 0.2, 0.4]); ax.set_yticks([0, 0.2, 0.4]); ax.tick_params(length=2.5, pad=2)
style.label(ax, 0.025, 0.43, 'trained with\ndisorder', color=style.ACCENT, fontsize=11, ha='left', va='top')
style.label(ax, 0.025, 0.31, 'trained on\nclean rings', color=style.BROKEN, fontsize=11, ha='left', va='top')
style.save(fig, __file__)
