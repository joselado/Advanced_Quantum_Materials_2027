"""Bond configurations of the Ising gauge theory (10.10) on an open lattice of 3 x 3 plaquettes, the picture options of
a quiz of Section 10.6b. Drawings and not plots, so sketch=True, and not a pyqula calculation.

The lattice has the vertices (x, y) with x, y = 0..3, the links h[x, y] from (x, y) to (x+1, y) and v[x, y] from (x, y)
to (x, y+1), 24 in all, and the plaquette (x, y) is h[x, y] v[x+1, y] h[x, y+1] v[x, y], as in igt_hist.py. The three
configurations are
  'ground', the uniform state after the gauge flips of the star at the vertices that a seeded draw picks, so that every
            plaquette product is +1 and the bonds look random,
  'oneflip', the uniform state with the interior link h[1, 1] flipped, which is a bond of two plaquettes,
  'hot', a seeded random configuration with as many bonds at -1 as the ground one.
A bond at +1 is a solid red line and a bond at -1 a dashed blue line, the colors of Figure 10.5 of the same page,
and nothing is written on the pictures. check()
asserts the products and the energies that the feedback quotes, and checks/session10/g4_06b_ising_gauge_theory.py calls
it too. This file writes no figure, the scripts g4_quiz_igt_*.py call draw."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

NP = 3          # plaquettes per side


def star(h, v, X, Y):
    """Flips the links that meet at the vertex (X, Y), two, three or four of them on the open lattice."""
    if X <= NP - 1:
        h[X, Y] *= -1
    if X >= 1:
        h[X - 1, Y] *= -1
    if Y <= NP - 1:
        v[X, Y] *= -1
    if Y >= 1:
        v[X, Y - 1] *= -1


def products(h, v):
    """The NP x NP plaquette products."""
    return np.array([[h[x, y] * v[x + 1, y] * h[x, y + 1] * v[x, y] for y in range(NP)] for x in range(NP)])


def energy(h, v, J=1.0):
    """H_IGT of (10.10), -J times the sum of the plaquette products."""
    return -J * products(h, v).sum()


def configuration(kind):
    h = np.ones((NP, NP + 1), dtype=int)
    v = np.ones((NP + 1, NP), dtype=int)
    if kind == 'ground':
        flips = np.random.default_rng(3).integers(0, 2, (NP + 1, NP + 1))
        for X in range(NP + 1):
            for Y in range(NP + 1):
                if flips[X, Y]:
                    star(h, v, X, Y)
    elif kind == 'oneflip':
        h[1, 1] = -1
    elif kind == 'hot':
        rng = np.random.default_rng(103)
        h = rng.choice([-1, 1], (NP, NP + 1))
        v = rng.choice([-1, 1], (NP + 1, NP))
    return h, v


def red(h, v):
    return int((h < 0).sum() + (v < 0).sum())


def check():
    """The statements of the feedback. Returns the number of plaquettes at -1 of the hot picture."""
    g, o, t = (configuration(k) for k in ('ground', 'oneflip', 'hot'))
    assert (products(*g) == 1).all() and energy(*g) == -9          # every product +1, the energy -9J, the lowest
    assert red(*g) == 11 and red(*t) == 11                          # 11 bonds at -1 of 24 in both random-looking pictures
    assert abs(g[0].sum() + g[1].sum()) / 24 == abs(t[0].sum() + t[1].sum()) / 24   # the same |m|
    po = products(*o)
    assert (po < 0).sum() == 2 and po[1, 0] == po[1, 1] == -1        # the flipped bond is in two plaquettes
    assert energy(*o) == -5 and energy(*o) - energy(*g) == 4         # -5J, 4J above the ground state
    pt = products(*t)
    nneg = int((pt < 0).sum())
    assert nneg == 5 and energy(*t) == -9 + 2 * nneg == 1            # five plaquettes at -1, the energy +J, 10J above
    for k, (h, v) in (('ground', g), ('hot', t)):                    # the even and odd numbers of bonds at -1 per plaquette
        for x in range(NP):
            for y in range(NP):
                nred = sum(b < 0 for b in (h[x, y], v[x + 1, y], h[x, y + 1], v[x, y]))
                assert (nred % 2 == 0) == (products(h, v)[x, y] == 1)
    # the alt texts: the blue bonds, at -1, of the ground picture lie mostly on the left, only two right of the middle,
    # those of the hot picture on both sides, and the one blue bond of the third picture is not on the edge
    xg, xt = red_x(*g), red_x(*t)
    assert (xg > 1.5).sum() == 2 and (xt > 1.5).sum() >= 4 and (xt < 1.5).sum() >= 4
    rows = [y for x in range(NP) for y in range(NP + 1) if o[0][x, y] < 0]
    assert rows == [1] and 0 < rows[0] < NP and (o[1] > 0).all()     # one horizontal bond at -1, on an inner row
    return nneg


def red_x(h, v):
    """The x coordinates of the middles of the bonds at -1."""
    return np.array([x + 0.5 for x in range(NP) for y in range(NP + 1) if h[x, y] < 0] +
                    [x for x in range(NP + 1) for y in range(NP) if v[x, y] < 0], dtype=float)


def draw(script, kind):
    """Writes the picture of one configuration, 'ground', 'oneflip' or 'hot'."""
    check()
    h, v = configuration(kind)
    fig, ax = style.plt.subplots(figsize=(4.4 * style.CM, 4.4 * style.CM))
    gap = 0.13

    def bond(p, q, s):
        (x0, y0), (x1, y1) = p, q
        dx, dy = (x1 - x0) * gap, (y1 - y0) * gap
        kw = dict(color=style.BROKEN, lw=2.6, solid_capstyle='butt') if s > 0 else \
            dict(color=style.ACCENT, lw=2.6, ls=(0, (1.6, 1.0)), dash_capstyle='butt')
        ax.plot([x0 + dx, x1 - dx], [y0 + dy, y1 - dy], **kw)

    for x in range(NP):
        for y in range(NP + 1):
            bond((x, y), (x + 1, y), h[x, y])
    for x in range(NP + 1):
        for y in range(NP):
            bond((x, y), (x, y + 1), v[x, y])
    X, Y = np.meshgrid(np.arange(NP + 1), np.arange(NP + 1))
    ax.plot(X.ravel(), Y.ravel(), 'o', color=style.MUTED, ms=3.2, ls='none')
    ax.set_xlim(-0.2, NP + 0.2); ax.set_ylim(-0.2, NP + 0.2)
    ax.set_aspect('equal'); ax.axis('off')
    style.save(fig, script, sketch=True)
