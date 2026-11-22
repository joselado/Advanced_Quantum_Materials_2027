"""Shared code of the phase fields of Section 1.3, the figure vortex_phase and the three picture options of the quiz
"Which one holds a vortex?". This file writes no figure.

The arrow at a point r is Delta(r) = |Delta(r)| exp(i theta(r)) drawn in the complex plane, with the positions in units
of the coherence length xi. Three fields are drawn. The uniform one has theta = 0. The vortex has theta = arg(x + iy)
and the amplitude tanh(r/xi), so the amplitude vanishes at the core. The bend has theta = pi y/(4 xi), a smooth turn of
the phase with no core. A phase field is a formula and not a pyqula calculation, so it is numpy. The winding along the
red loop of radius 2.2 xi is computed from the field sampled on that loop, and check() asserts the numbers of the
feedback, the windings 0, 1 and 0 and the largest phase of the bend on the loop, 0.55 pi."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

LOOP = 2.2                    # radius of the red loop, in units of xi


def field(kind, x, y):
    """The amplitude and the phase theta of Delta at the points (x, y), in units of xi."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    if kind == 'uniform':
        return np.ones_like(x), np.zeros_like(x)
    if kind == 'vortex':
        return np.tanh(np.hypot(x, y)), np.arctan2(y, x)
    if kind == 'bend':
        return np.ones_like(x), np.pi * y / 4
    raise ValueError(kind)


def winding(kind, n=2000):
    """The number of turns of the phase along the loop, from the field sampled on the loop, counterclockwise."""
    phi = np.linspace(0, 2 * np.pi, n + 1)
    amp, th = field(kind, LOOP * np.cos(phi), LOOP * np.sin(phi))
    z = amp * np.exp(1j * th)
    return np.sum(np.angle(z[1:] / z[:-1])) / (2 * np.pi)


def check():
    w = {kind: winding(kind) for kind in ('uniform', 'vortex', 'bend')}
    assert abs(w['uniform']) < 1e-9 and abs(w['vortex'] - 1) < 1e-9 and abs(w['bend']) < 1e-9, w
    # the bend: on the loop the phase goes up to pi*2.2/4 = 0.55 pi at the top and down to -0.55 pi at the bottom
    phi = np.linspace(0, 2 * np.pi, 2001)
    th = field('bend', LOOP * np.cos(phi), LOOP * np.sin(phi))[1]
    assert abs(th.max() / np.pi - 0.55) < 1e-6 and abs(th.min() / np.pi + 0.55) < 1e-6
    # the vortex: the amplitude vanishes at the core, and it is above 0.97 on the loop and above 0.76 at r = xi
    amp = field('vortex', LOOP * np.cos(phi), LOOP * np.sin(phi))[0]
    assert field('vortex', 0., 0.)[0] == 0 and amp.min() > 0.97 and abs(np.tanh(1.0) - 0.76) < 0.01
    print('windings', {k: round(v, 9) for k, v in w.items()}, 'phase of the bend on the loop up to',
          round(th.max() / np.pi, 4), 'pi')
    return w


def draw(ax, kind, n=9, half=3.0, scale=1.9, loop=True):
    """The arrows of one field on an n by n grid from -half to half, and the red loop."""
    g = np.linspace(-half, half, n)
    X, Y = np.meshgrid(g, g)
    amp, th = field(kind, X, Y)
    kw = dict(angles='xy', scale_units='xy', scale=scale, width=0.012, headwidth=3.6, headlength=3.6,
              headaxislength=3.2)
    ax.quiver(X, Y, amp * np.cos(th), amp * np.sin(th), color=style.ACCENT, **kw)
    if loop:
        phi = np.linspace(0, 2 * np.pi, 400)
        ax.plot(LOOP * np.cos(phi), LOOP * np.sin(phi), color=style.BROKEN, lw=1.3, zorder=0)
    ax.set_aspect('equal')


def option(script, kind):
    """One picture option, a field with its axes x/xi and y/xi and no other text."""
    check()
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 3.9 * style.CM))
    draw(ax, kind, n=7, scale=1.45)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xlim(-3.7, 3.7); ax.set_ylim(-3.7, 3.7)
    ax.set_xticks([-3, 0, 3]); ax.set_xticklabels(['$-3$', '0', '3'], fontsize=11)
    ax.set_yticks([-3, 0, 3]); ax.set_yticklabels(['$-3$', '0', '3'], fontsize=11)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$x/\xi$', fontsize=12, labelpad=0); ax.set_ylabel(r'$y/\xi$', fontsize=12, labelpad=-4)
    style.save(fig, script)
