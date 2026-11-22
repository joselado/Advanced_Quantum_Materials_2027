"""Shared code of the picture options of the quiz of Section 10.2, the fits of the widget netfit for H=1, 3 and 12.

The curves come from compute() of webnotes/widgets/defs/netfit.py, so that the pictures are the curves of the widget,
one hidden layer of H tanh units fitted to y=sin(3 pi x) on 41 points of [-1, 1]. Numpy, since pyqula does not train
networks, so the options have no button. A picture is the fit against x with the target as a grey dashed line on top
of it, with its axes and no other text, and the three share the scale. This file writes no figure."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'widgets', 'defs'))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patheffects
import style
import netfit


def fit(H):
    """The fit of the widget for H hidden neurons, as (x, network output, mean squared error printed by the widget)."""
    d = netfit.compute(dict(H=H))
    s = d['panels'][0]['series']
    assert s[2]['label'] == 'network'
    return np.asarray(s[2]['x']), np.asarray(s[2]['y']), float(d['text'].split('error is ')[1].rstrip('.'))


def extrema(y):
    """The number of turning points of a curve sampled on a grid."""
    dy = np.diff(y)
    return int(np.sum(np.sign(dy[1:]) != np.sign(dy[:-1])))


def check():
    """The numbers that the feedback of the quiz quotes, checked on the curves that the pictures draw."""
    out = {H: fit(H) for H in (1, 3, 12)}
    x = np.linspace(-1, 1, 41)
    target = np.sin(3 * np.pi * x)
    # the target has six extrema on [-1, 1], and an output that is zero has the mean squared error 0.49
    assert extrema(np.sin(3 * np.pi * out[1][0])) == 6
    assert abs(np.mean(target ** 2) - 0.49) < 0.005
    # H=1 is monotonic, with no extremum, and its error is 0.46, H=3 has two extrema and 0.23, H=12 six and 2.3e-4
    (x1, y1, e1), (x3, y3, e3), (x12, y12, e12) = out[1], out[3], out[12]
    assert np.all(np.diff(y1) > 0) and extrema(y1) == 0 and abs(e1 - 0.46) < 0.005
    assert extrema(y3) == 2 and abs(e3 - 0.23) < 0.005
    assert extrema(y12) == 6 and abs(e12 - 2.3e-4) < 0.05e-4
    # the widget prints the error of the last recorded step; the drawn curve, after the last step, gives the same digits
    for H, (xf, yf, e) in out.items():
        on41 = np.interp(x, xf, yf)
        assert abs(np.mean((on41 - target) ** 2) - e) / e < 0.02, H
    # the shapes that the alt texts state, read on the drawn curves (101 points of [-1, 1])
    # H=1 rises slowly and almost straight: slope about 0.29, within 0.01 of a straight line
    p1 = np.polyfit(x1, y1, 1)
    assert 0 < p1[0] < 0.5 and np.abs(np.polyval(p1, x1) - y1).max() < 0.01
    # H=3 rises from x=-1, so it misses the first minimum of the target at -5/6; its maximum is near the first
    # maximum of the target at -1/2 and its minimum near the minimum after it at -1/6; then it rises, is near zero
    # on [0.3, 0.6] and is above 0.6 at the right end, from x=0.8 on
    i3, j3 = int(np.argmax(y3)), int(np.argmin(y3))
    assert y3[1] > y3[0] and abs(x3[i3] + 0.5) < 0.1 and abs(x3[j3] + 1 / 6) < 0.1 and x3[i3] < x3[j3]
    assert np.all(np.diff(y3[j3:]) > 0)
    assert np.abs(y3[(x3 >= 0.3) & (x3 <= 0.6)]).max() < 0.05 and y3[x3 >= 0.8].min() > 0.6
    # H=12 follows the target everywhere, within 0.05 on the drawn grid
    assert np.abs(y12 - np.sin(3 * np.pi * x12)).max() < 0.05
    # all three curves fit in the window of the pictures
    assert max(np.abs(y).max() for (_, y, _) in out.values()) < 1.25
    print('H=1 error %.3f, H=3 error %.3f with %d extrema, H=12 error %.2e with %d extrema'
          % (e1, e3, extrema(y3), e12, extrema(y12)))
    return out


def option(script, H):
    """One picture option, the fit of the widget for H hidden neurons."""
    out = check()
    xf, yf, _ = out[H]
    fig, ax = plt.subplots(figsize=(3.7 * style.CM, 3.9 * style.CM))
    ax.axhline(0, color=style.GRID, lw=0.8, zorder=0)
    # the dashed target is drawn on top of the fit, with a white edge, so that its dashes show where the fit covers
    # it (H=12), also at the 100 px of a picture option on a phone
    ax.plot(xf, yf, color=style.ACCENT, lw=1.8, zorder=1)
    ax.plot(xf, np.sin(3 * np.pi * xf), color=style.MUTED, lw=1.1, ls=(0, (3, 2)), zorder=2,
            path_effects=[patheffects.withStroke(linewidth=2.1, foreground='white')])
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xlim(-1.05, 1.05); ax.set_ylim(-1.3, 1.3)
    ax.set_xticks([-1, 0, 1]); ax.set_xticklabels(['$-1$', '0', '1'], fontsize=11)
    ax.set_yticks([-1, 0, 1]); ax.set_yticklabels(['$-1$', '0', '1'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$x$', fontsize=12, labelpad=0); ax.set_ylabel(r'$y$', fontsize=12, labelpad=-4)
    style.save(fig, script)
