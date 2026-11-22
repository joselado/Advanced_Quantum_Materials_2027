"""Shared code of the picture options of the quiz of Section 6.12 on the chain of classical spins with a
Dzyaloshinskii-Moriya term.

The chain is H = sum_i [J S_i.S_{i+1} + D z.(S_i x S_{i+1})] with J > 0 and D along z. Two spins in the plane normal to z,
at the angle theta from S_i to S_{i+1} counted counterclockwise seen from +z, have the bond energy
S^2 (J cos theta + D sin theta). The check minimizes it over the full circle. The minimum is at
cos theta = -J/sqrt(J^2 + D^2) with sin theta < 0 for D > 0, so seen from +z the spins turn clockwise, as the sheet
webnotes/conventions/session06.md says, and the energy is -S^2 sqrt(J^2 + D^2) per bond. The angle between neighbors
is 180 degrees for D = 0, 135.0 for D = J and 101.3 for D = 5J.

Each picture is one row of four spins, and the page is the plane normal to z seen from +z, with x to the right and y up.
The question of the quiz says so. The rows turn clockwise in the page, which is the sense of the ground state for D > 0.
The check runs on the drawn vectors themselves: z.(S_i x S_{i+1}) < 0 on every bond of the two turning rows, and for
D = J the bond energies -J S^2 for the row at 180 degrees, -sqrt2 J S^2 = -1.414 J S^2 for the row at 135 degrees and
-1.177 J S^2 for the row at 101.3 degrees, the numbers of the feedback, so the row at 135 degrees is the lowest of the
three. The row at 101.3 degrees has -sqrt26 J S^2 for D = 5J, the ground state there. A picture is a drawing of real
space with no axes, so it is saved with sketch=True. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow
import style

TH = np.linspace(-np.pi, np.pi, 720001)          # the angle from S_i to S_{i+1}, counterclockwise seen from +z
ROWS = (180.0, 135.0, 101.3)                      # the angles between neighbors of the three pictures


def ground(J, D):
    """The angle that minimizes J cos theta + D sin theta, and the energy per bond for S = 1."""
    e = J * np.cos(TH) + D * np.sin(TH)
    k = np.argmin(e)
    return TH[k], e[k]


def row(degrees, n=4):
    """The unit spins of a drawn row, in the page seen from +z: the first one up, each next one turned clockwise."""
    a = np.pi / 2 - np.arange(n) * np.radians(degrees)
    return np.array([np.cos(a), np.sin(a), 0 * a]).T


def bonds(degrees, J, D):
    """The energies J S_i.S_{i+1} + D z.(S_i x S_{i+1}) of the bonds of a drawn row, for S = 1."""
    s = row(degrees)
    return np.array([J * s[i] @ s[i + 1] + D * np.cross(s[i], s[i + 1])[2] for i in range(len(s) - 1)])


def check():
    for D, deg in ((0.0, 180.0), (1.0, 135.0), (5.0, 101.3)):
        th, e = ground(1.0, D)
        assert abs(np.cos(th) + 1 / np.hypot(1, D)) < 1e-5            # the grid step is 9e-6
        assert round(np.degrees(abs(th)), 1) == deg, (D, np.degrees(th))
        assert abs(e + np.hypot(1, D)) < 1e-9                     # -S^2 sqrt(J^2 + D^2)
        if D > 0:
            assert np.sin(th) < 0                                 # clockwise seen from +z
    for deg in ROWS[1:]:                                          # the drawn rows turn clockwise seen from +z
        s = row(deg)
        assert all(np.cross(s[i], s[i + 1])[2] < 0 for i in range(len(s) - 1)), deg
    e = {deg: bonds(deg, 1.0, 1.0) for deg in ROWS}               # D = J
    assert np.allclose(e[180.0], -1.0, atol=1e-12)
    assert np.allclose(e[135.0], -np.sqrt(2), atol=1e-12) and round(e[135.0][0], 3) == -1.414
    assert np.allclose(e[101.3], e[101.3][0], atol=1e-12) and round(e[101.3][0], 3) == -1.177
    assert e[135.0][0] < e[101.3][0] < e[180.0][0]                # the row at 135 degrees is the lowest for D = J
    assert abs(bonds(101.3, 1.0, 5.0)[0] + np.sqrt(26)) < 1e-3    # the row at 101.3 degrees is the ground state of D = 5J
    assert round(np.degrees(np.arccos(-1 / np.sqrt(26))), 1) == 101.3


def option(script, degrees):
    """One picture, a row of four spins that turns clockwise by the given angle from site to site."""
    check()
    assert degrees in ROWS
    s = row(degrees)
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 1.9 * style.CM))
    ax.axis('off'); ax.set_aspect('equal')
    L = 0.86
    ax.plot([-0.3, 3.3], [0, 0], color=style.GRID, lw=1.0, zorder=0)
    for i, (ux, uy, _) in enumerate(s):
        ax.add_patch(FancyArrow(i - 0.5 * L * ux, -0.5 * L * uy, L * ux, L * uy, width=0.09, head_width=0.3,
                                head_length=0.25, length_includes_head=True, fc=style.ACCENT, ec="none", zorder=2))
        ax.plot([i], [0], 'o', color=style.INK, ms=2.6, zorder=3)
    ax.set_xlim(-0.55, 3.55); ax.set_ylim(-0.55, 0.55)
    style.save(fig, script, sketch=True)
