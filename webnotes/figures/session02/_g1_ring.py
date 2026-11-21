"""Shared code of the picture options of the quiz of Section 2.3, which state on a ring of four sites is an eigenstate
of the rotation by 90 degrees.

The arrow on a site is the complex amplitude, with its real part to the right and its imaginary part up, as the small
key in the corner shows. The three states are e^{i pi j/2}, which turns by 90 degrees from site to site, the same
turn with the lengths 1 and 1/2, and e^{i pi j/3}, which turns by 60 degrees. The asserts check, for the rotation in
both senses, that only the first one is an eigenstate, and the numbers that the feedback of the quiz quotes. A
picture is a drawing with no data axes, so it is saved with sketch=True. This file writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

J = np.arange(4)
STATES = {
    'turn90': np.exp(1j * np.pi * J / 2),
    'lengths': np.exp(1j * np.pi * J / 2) * np.array([1, 0.5, 1, 0.5]),
    'turn60': np.exp(1j * np.pi * J / 3),
}
SITES = np.c_[np.cos(np.pi / 4 + np.pi / 2 * J), np.sin(np.pi / 4 + np.pi / 2 * J)]    # counterclockwise


def is_eigen(R, v):
    lam = (v.conj() @ R @ v) / (v.conj() @ v)
    return np.allclose(R @ v, lam * v), lam


def check():
    R = np.roll(np.eye(4), 1, axis=0)            # (R v)_j = v_{j-1}, every amplitude moves to the next site
    for name, v in STATES.items():
        for Rs in (R, R.T):                        # the rotation in the two senses
            ok, lam = is_eigen(Rs, v)
            assert ok == (name == 'turn90'), name
            if ok:
                assert np.isclose(abs(lam), 1) and np.isclose(lam ** 4, 1)
    v = STATES['lengths']
    assert np.allclose(sorted(set(np.round(np.abs(v), 9))), [0.5, 1.0])                 # the lengths 1 and 1/2
    assert np.allclose(np.angle(v[1:] / v[:-1]), np.pi / 2)                            # it turns by 90 degrees
    w = STATES['turn60']
    steps = np.degrees(np.angle(np.r_[w[1:], w[:1]] / w)) % 360
    assert np.allclose(steps, [60, 60, 60, 180])                                       # the step back to site 0
    assert np.isclose(np.degrees(np.angle(w[3])) % 360, 180)                           # 3 x 60 = 180 on the last site
    assert np.allclose(np.abs(w), 1)                                                   # the alt text: the same length
    assert 4 * 60 == 240 and 240 % 360 != 0                       # four equal steps of 60 degrees do not close the ring
    print('steps of the state turning by 60 degrees', steps)


def option(script, name):
    """One picture option, the state STATES[name] on the ring."""
    check()
    fig, ax = plt.subplots(figsize=(3.9 * style.CM, 3.9 * style.CM))
    ax.set_aspect('equal'); ax.axis('off')
    ring = np.r_[SITES, SITES[:1]]
    ax.plot(ring[:, 0], ring[:, 1], color=style.GRID, lw=2.0, zorder=1)
    for p, a in zip(SITES, STATES[name]):
        ax.scatter(*p, s=40, color=style.INK, zorder=3)
        d = 0.8 * np.array([a.real, a.imag])
        ax.annotate('', xy=tuple(p + d), xytext=tuple(p), zorder=4,
                    arrowprops=dict(arrowstyle='-|>', color=style.ACCENT, lw=1.6, mutation_scale=8, shrinkA=0, shrinkB=0))
    # the key of the complex plane, real part to the right and imaginary part up
    o = np.array([-2.0, -2.0])
    for dx, dy, lab, ha, va in ((0.6, 0, r'$\mathrm{Re}$', 'left', 'center'), (0, 0.6, r'$\mathrm{Im}$', 'center', 'bottom')):
        ax.annotate('', xy=(o[0] + dx, o[1] + dy), xytext=tuple(o),
                    arrowprops=dict(arrowstyle='-|>', color=style.INK, lw=0.9, mutation_scale=8, shrinkA=0, shrinkB=0))
        style.label(ax, o[0] + dx + (0.06 if dx else 0), o[1] + dy + (0.04 if dy else 0), lab, ha=ha, va=va, fontsize=11)
    ax.set_xlim(-2.1, 1.65); ax.set_ylim(-2.1, 1.65)
    ax.add_patch(plt.Rectangle((-2.1, -2.1), 3.75, 3.75, fill=False, lw=0, ec='none'))
    style.save(fig, script, sketch=True)
