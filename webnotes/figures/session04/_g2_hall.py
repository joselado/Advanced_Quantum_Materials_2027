"""Session 4, Section 4.6, the Hall resistance of a two-dimensional electron gas at fixed density against the field,
shared by plateaus.py and the picture options g2_quiz_rxy_*.py of the quiz on the plateaus.

The field is x = B/B_1, with B_1 the field where the density fills one Landau level, so the filling is nu = 1/x. N_eff
is the number of Landau levels below the chemical potential, with each level filled in a window of width w in the
filling around its center, the model of plateaus.py since 2026-11-06. The Hall resistance is R_xy = h/(N_eff e^2), and
the classical one is R_xy = B/(n e) = (h/e^2) x. Both are in units of h/e^2. The third curve, a staircase with the
plateaus 1, 2, 3, 4 that rises with B, is a wrong picture for the quiz. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

WIDTH = 0.05                               # the broadening of the steps in the filling, chosen by hand
XMAX = 1.55                                # the largest field of the plots, in units of B_1


def quantum(x, w=WIDTH):
    """R_xy e^2/h of the model with the plateaus h/(N e^2)."""
    nu = 1 / np.asarray(x, float)
    return 1 / sum(0.5 * (1 + np.tanh((nu - (n - 0.5)) / w)) for n in range(1, 40))


def classical(x):
    """R_xy e^2/h = B/B_1, the classical Hall resistance B/(n e)."""
    return np.asarray(x, float)


def wrong_staircase(x, w=0.02):
    """A staircase that rises by one in units of h/e^2 every quarter of B_1, up to 4, the wrong option of the quiz."""
    x = np.asarray(x, float)
    return sum(0.5 * (1 + np.tanh((x - 0.25 * n) / w)) for n in range(1, 5))


def check():
    """The numbers that the caption and the quiz quote, on a dense grid of the model."""
    x = np.linspace(0.1, XMAX, 145001)
    R = quantum(x)
    out = {}
    for N in (1, 2, 3, 4):
        cross = 1 / N
        on = np.abs(R - 1 / N) < 1e-3
        out[N] = (x[on].min(), x[on].max())
        # the classical line meets the plateau N at B/B_1 = 1/N, inside its flat part
        assert abs(quantum(cross) - 1 / N) < 1e-3 and out[N][0] < cross < out[N][1], (N, out[N])
    # the plateaus become narrow at low field
    widths = [out[N][1] - out[N][0] for N in (1, 2, 3, 4)]
    assert all(a > b for a, b in zip(widths, widths[1:])), widths
    # the curve rises with B, so N falls as the field grows at fixed density
    assert np.all(np.diff(R) >= -1e-12)
    # the broadening lifts the end of the plateau N = 1 at B/B_1 = 1.55 by less than one percent
    assert 1 - 1e-3 < R.max() < 1.01, R.max()
    xs = np.linspace(0.1, XMAX, 3001)
    Rw = wrong_staircase(xs)
    for N in (1, 2, 3, 4):
        assert np.any(np.abs(Rw - N) < 1e-3)
    assert Rw.max() < 4 + 1e-9 and np.all(np.diff(Rw) >= 0)
    return out, widths


def option(script, curve):
    """One picture option, R_xy against B on the shared scale of the three options, with its axes and no other text."""
    check()
    x = np.linspace(0.1 if curve == 'quantum' else 0.0, XMAX, 3000)
    R = dict(quantum=quantum, classical=classical, wrong=wrong_staircase)[curve](x)
    print(os.path.basename(script), curve, 'largest R_xy e^2/h', round(float(R.max()), 3))
    fig, ax = style.plt.subplots(figsize=(3.7 * style.CM, 3.9 * style.CM))
    ax.plot(x, R, color=style.ACCENT, lw=1.5)
    ax.set_xlim(0, 1.6); ax.set_ylim(0, 4.4)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xticks([0, 1]); ax.set_xticklabels(['0', '1'], fontsize=11)
    ax.set_yticks([0, 1, 2, 3, 4]); ax.set_yticklabels(['0', '1', '2', '3', '4'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$B/B_1$', fontsize=12, labelpad=-2)
    ax.set_ylabel(r'$R_{xy}\,e^2/h$', fontsize=12, labelpad=1)
    style.save(fig, script)
