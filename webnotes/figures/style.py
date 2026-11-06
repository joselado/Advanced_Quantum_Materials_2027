"""Common look of the web-only schematics, so that they sit next to the converted figures of the notes.

A web schematic is a script webnotes/figures/sessionNN/NAME.py that ends with

    import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    import style
    fig, ax = style.figure()          # 14.6 cm wide, white background
    ...
    style.save(fig, __file__)         # writes NAME.svg next to the script

The look is taken from the converted figures of docs/notes/figures/. The text is in Computer Modern, the
same face as the labels of the PDF figures, drawn as outlines so that the SVG needs no font. The main curve is
the dark blue `accent` (31,78,121) of the labels, the secondary one the `broken` red, the guide lines are the
light grey `muted`, the axes are thin dark-grey lines with a small arrow head and no box. The background is
white, as the figures of the page are shown on a white card.
"""
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# the three colors of figures_preamble.tex, plus the two tints of the renders (aqmstyles.tex)
ACCENT = '#1f4e79'
BROKEN = '#a82a22'
MUTED = '#7d7d7d'
LIGHT = '#769ec6'      # keypos, a lighter blue for a second curve of the same family
WARM = '#d69684'       # keyneg
GRID = '#d9d9d9'
INK = '#333333'        # axes and arrows

WIDTH_CM = 14.6        # the width of a converted figure in the page is 421 pt, i.e. 14.9 cm
CM = 1 / 2.54


def setup():
    plt.rcParams.update({
        'svg.fonttype': 'path',            # text as outlines, no font dependency in the browser
        'svg.hashsalt': 'aqm',             # same ids at every run, so that the SVG is reproducible
        'font.family': 'serif',
        'font.serif': ['cmr10', 'DejaVu Serif'],
        'mathtext.fontset': 'cm',
        'axes.formatter.use_mathtext': True,
        'axes.unicode_minus': False,
        'font.size': 9,
        'axes.labelsize': 9,
        'xtick.labelsize': 8.5,
        'ytick.labelsize': 8.5,
        'axes.linewidth': 0.7,
        'axes.edgecolor': INK,
        'axes.labelcolor': INK,
        'text.color': INK,
        'xtick.color': INK,
        'ytick.color': INK,
        'lines.linewidth': 1.8,            # the blue curves of the converted figures are about 1.7 pt in the page
        'lines.solid_capstyle': 'round',
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'savefig.facecolor': 'white',
        'legend.frameon': False,
        'legend.fontsize': 8.5,
    })


setup()


def figure(height_cm=5.6, width_cm=WIDTH_CM, **kw):
    """A figure of the width of the converted ones, with one axes with the arrow style (see arrows)."""
    fig, ax = plt.subplots(figsize=(width_cm * CM, height_cm * CM), **kw)
    if isinstance(ax, np.ndarray):
        for a in ax.flat:
            arrows(a)
    else:
        arrows(ax)
    return fig, ax


def arrows(ax, xlabel=None, ylabel=None, ticks=False):
    """Axes as two thin arrows from the lower left corner, no box, no ticks unless ticks=True.
    The labels sit at the tips, as in the figures of the notes."""
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    if not ticks:
        ax.set_xticks([])
        ax.set_yticks([])
    kw = dict(arrowstyle='-|>', color=INK, lw=0.7, mutation_scale=7, shrinkA=0, shrinkB=0, clip_on=False)
    ax.annotate('', xy=(1.02, 0), xytext=(0, 0), xycoords='axes fraction', textcoords='axes fraction',
                arrowprops=kw)
    ax.annotate('', xy=(0, 1.04), xytext=(0, 0), xycoords='axes fraction', textcoords='axes fraction',
                arrowprops=kw)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    if xlabel:
        ax.annotate(xlabel, xy=(1.03, 0), xycoords='axes fraction', ha='left', va='center')
    if ylabel:
        ax.annotate(ylabel, xy=(0, 1.06), xycoords='axes fraction', ha='center', va='bottom')
    return ax


def guide(ax, y=None, x=None, **kw):
    """A light grey guide line, as the dotted levels of the band plots."""
    kw = dict(dict(color=GRID, lw=1.0, zorder=0), **kw)
    if y is not None:
        ax.axhline(y, **kw)
    if x is not None:
        ax.axvline(x, **kw)


def label(ax, x, y, s, color=INK, **kw):
    """A text label in data coordinates, no box."""
    return ax.text(x, y, s, color=color, **dict(dict(ha='center', va='center'), **kw))


def save(fig, script):
    """Writes NAME.svg next to the script NAME.py, atomically and reproducibly."""
    svg = os.path.splitext(os.path.abspath(script))[0] + '.svg'
    tmp = svg + '.tmp'
    fig.savefig(tmp, format='svg', metadata={'Date': None, 'Creator': 'webnotes/figures/style.py'},
                bbox_inches='tight', pad_inches=0.06)
    os.replace(tmp, svg)
    plt.close(fig)
    return svg
