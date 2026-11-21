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


# the artists of a map over a plane, by the name of their class: pcolormesh, pcolor, contourf, tripcolor
MAPS = ('QuadMesh', 'PolyQuadMesh', 'QuadContourSet', 'TriContourSet', 'TriMesh')


def _all_axes(fig):
    """The axes of the figure and their insets, without the colorbars, which carry a QuadMesh and no names."""
    out, todo = [], list(fig.axes)
    while todo:
        ax = todo.pop(0)
        if ax in out:
            continue
        todo.extend(getattr(ax, 'child_axes', []))
        if ax.get_label() == '<colorbar>' or hasattr(ax, '_colorbar') or not ax.get_visible():
            continue
        out.append(ax)
    return out


def _has_names(ax):
    """True when the axes names a quantity on an axis: an xlabel or a ylabel, or a text at the tip of an arrow
    written in axes-fraction coordinates, as arrows(ax, xlabel=..., ylabel=...) does. The tags (a) and (b) under a
    panel are not names."""
    if ax.get_xlabel().strip() or ax.get_ylabel().strip():
        return True
    for t in ax.texts:
        if not t.get_text().strip() or getattr(t, 'xycoords', None) != 'axes fraction':
            continue
        x, y = t.xy
        if (x >= 1 and y <= 0.05) or (x <= 0.05 and y >= 1):
            return True
    return False


def axes_warnings(fig, script):
    """The lines AXES-WARNING of the rule "every plot has its axes" for this figure. An axes that holds data
    (lines, collections, images, bars) warns when its axis is on and it names no quantity, and a map (pcolormesh
    or image) also warns when its axis is switched off. It only reads the figure, so the SVG does not change."""
    path = os.path.abspath(script)
    name = os.path.basename(os.path.dirname(path)) + '/' + os.path.basename(path)
    axes = _all_axes(fig)
    out = []
    for i, ax in enumerate(axes, start=1):
        maps = [type(c).__name__ for c in ax.collections if type(c).__name__ in MAPS] + ['image'] * len(ax.images)
        if not (ax.lines or ax.collections or ax.images or ax.containers):
            continue
        what = f'axes {i} of {len(axes)}'
        if ax.axison and not _has_names(ax):
            held = ', '.join(f'{n} {k}' for n, k in ((len(ax.lines), 'lines'), (len(ax.collections), 'collections'),
                                                    (len(ax.images), 'images'), (len(ax.containers), 'bar sets')) if n)
            out.append(f'AXES-WARNING {name}: {what} ({held}) has no axis names, neither xlabel nor ylabel '
                       'nor style.arrows(xlabel=..., ylabel=...)')
        elif maps and not ax.axison:
            out.append(f'AXES-WARNING {name}: {what} is a map ({maps[0]}) with its axis switched off')
    return out


def save(fig, script, sketch=False):
    """Writes NAME.svg next to the script NAME.py, atomically and reproducibly.

    Before that it prints the lines AXES-WARNING of axes_warnings, which build.py lists among the warnings of the
    build. A drawing that is not a plot, such as a lattice sketch or a concept map, says so with sketch=True and
    gets no warning. The check only reads the figure, so what is written does not depend on it."""
    if not sketch:
        try:
            lines = axes_warnings(fig, script)
        except Exception as e:                  # the check must never stop a figure from being written
            lines = [f'AXES-WARNING {os.path.basename(script)}: the axes could not be checked, {e!r}']
        for line in lines:
            print(line, flush=True)
    svg = os.path.splitext(os.path.abspath(script))[0] + '.svg'
    tmp = svg + '.%d.tmp' % os.getpid()      # one name per process, since two builds may redraw the same figure
    fig.savefig(tmp, format='svg', metadata={'Date': None, 'Creator': 'webnotes/figures/style.py'},
                bbox_inches='tight', pad_inches=0.06)
    os.replace(tmp, svg)
    plt.close(fig)
    return svg


# ---------------------------------------------------------------------------------------------------------------
# Plots in reciprocal space, and the downloadable pyqula scripts. Rules of 2026-11-21: every plot has its axes, a
# map over the Brillouin zone shows k_x and k_y and the first Brillouin zone, and a calculation that pyqula can do
# is done by a small script of webnotes/scripts/ that the student downloads next to the figure.
# ---------------------------------------------------------------------------------------------------------------

def run_script(name):
    """Runs the downloadable script webnotes/scripts/NAME, for instance 'session03/haldane_berry.py', and returns
    its variables as a dictionary. The figure is drawn from these variables, so that the figure and the script that
    the student downloads are the same calculation. It runs in a temporary folder, since pyqula writes files."""
    import runpy, tempfile
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts', name)
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as d:
        os.chdir(d)
        try:
            return runpy.run_path(path)
        finally:
            os.chdir(cwd)


def first_zone(B):
    """The corners of the first Brillouin zone, in order, for the reciprocal vectors B (rows b1, b2)."""
    from scipy.spatial import Voronoi
    B = np.asarray(B, float)
    pts = np.array([i * B[0] + j * B[1] for i in range(-2, 3) for j in range(-2, 3)])
    vor = Voronoi(pts)
    origin = int(np.argmin(np.linalg.norm(pts, axis=1)))
    c = vor.vertices[vor.regions[vor.point_region[origin]]]
    return c[np.argsort(np.arctan2(c[:, 1], c[:, 0]))]


def draw_zone(ax, B, **kw):
    """Draws the first Brillouin zone as a dashed polygon."""
    c = first_zone(B)
    c = np.vstack([c, c[:1]])
    kw = dict(dict(color=INK, lw=0.8, ls=(0, (4, 3)), zorder=5), **kw)
    return ax.plot(c[:, 0], c[:, 1], **kw)


def kmap(ax, B, values, half=None, zone=True, **kw):
    """A map of a quantity over reciprocal space, in the extended zone. values[i, j] is the quantity at the point
    (i/N) b1 + (j/N) b2 of the reduced zone. The map is repeated over the neighboring cells and cut to the square
    |k_x|, |k_y| < half (by default a bit more than the first zone), and the first Brillouin zone is drawn dashed.
    kw goes to pcolormesh (cmap, vmin, vmax). Returns the image, for a colorbar."""
    B = np.asarray(B, float)
    values = np.asarray(values)
    N = values.shape[0]
    if half is None:
        half = 1.18 * np.abs(first_zone(B)).max()
    u = np.arange(N + 1) / N
    U, V = np.meshgrid(u, u, indexing='ij')
    v = np.pad(values, ((0, 1), (0, 1)), mode='wrap')
    kw = dict(dict(shading='nearest', rasterized=True), **kw)
    im = None
    for i in range(-3, 3):
        for j in range(-3, 3):
            X = (U + i) * B[0, 0] + (V + j) * B[1, 0]; Y = (U + i) * B[0, 1] + (V + j) * B[1, 1]
            if X.max() < -half or X.min() > half or Y.max() < -half or Y.min() > half:
                continue
            im = ax.pcolormesh(X, Y, v, **kw)
    ax.set_xlim(-half, half); ax.set_ylim(-half, half)
    ax.set_aspect('equal')
    if zone:
        draw_zone(ax, B)
    return im


def kaxes(ax, ticks=None, fontsize=8.5):
    """The axes of a map in reciprocal space: a thin box, the labels k_x and k_y, and ticks at -ticks, 0, ticks
    (a number, or None for no numbers). Use it after kmap."""
    for s in ('top', 'right', 'left', 'bottom'):
        ax.spines[s].set_visible(True); ax.spines[s].set_linewidth(0.6)
    ax.set_xlabel(r'$k_x$', fontsize=fontsize, labelpad=1); ax.set_ylabel(r'$k_y$', fontsize=fontsize, labelpad=1)
    if ticks is None:
        ax.set_xticks([]); ax.set_yticks([])
    else:
        ax.set_xticks([-ticks, 0, ticks]); ax.set_yticks([-ticks, 0, ticks])
        ax.tick_params(length=2.5, width=0.6, labelsize=fontsize - 0.5)
    return ax


def pyqula_kmap(ax, g, kx, ky, values, half=None, zone=True, scale=None, **kw):
    """A map that pyqula computed on its window of reciprocal space, such as (kx, ky, b) = h.get_berry_curvature(),
    drawn in the extended zone with the first Brillouin zone dashed. g is the geometry of the Hamiltonian. pyqula
    gives kx and ky in units of 2 pi over the lattice constant, and here they become true momenta, in units of the
    inverse of the length unit of g (the bond length for geometry.honeycomb_lattice). The window of pyqula is a
    rectangle that is a period of the map, which is checked here, so it is repeated to fill the square
    |k_x|, |k_y| < half. kw goes to pcolormesh. Returns the image and the reciprocal vectors B (rows b1, b2)."""
    A = np.array([np.asarray(g.a1, float)[:2], np.asarray(g.a2, float)[:2]])
    B = 2 * np.pi * np.linalg.inv(A).T
    if scale is None:
        scale = 2 * np.pi / np.linalg.norm(A[0])
    xs = np.unique(np.round(np.asarray(kx, float), 9)); ys = np.unique(np.round(np.asarray(ky, float), 9))
    nx, ny = len(xs), len(ys)
    V = np.asarray(values, float).reshape(nx, ny)             # the first index of pyqula runs along kx
    X = xs * scale; Y = ys * scale
    Wx = (X[1] - X[0]) * nx; Wy = (Y[1] - Y[0]) * ny
    for W in ((Wx, 0.0), (0.0, Wy)):
        c = np.linalg.solve(B.T, np.array(W))
        assert np.allclose(c, np.round(c), atol=1e-6), 'the window of pyqula is not a period of the reciprocal lattice'
    if half is None:
        half = 1.35 * np.abs(first_zone(B)).max()
    kw = dict(dict(shading='nearest', rasterized=True), **kw)
    im = None
    for i in range(-3, 4):
        for j in range(-3, 4):
            x, y = X + i * Wx, Y + j * Wy
            if x.max() < -half or x.min() > half or y.max() < -half or y.min() > half:
                continue
            im = ax.pcolormesh(x, y, V.T, **kw)
    ax.set_xlim(-half, half); ax.set_ylim(-half, half)
    ax.set_aspect('equal')
    if zone:
        draw_zone(ax, B)
    return im, B
