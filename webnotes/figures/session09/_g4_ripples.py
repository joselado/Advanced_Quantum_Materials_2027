"""Shared code of the figures of the Friedel ripples in a square lattice, Section 9.6a, which are friedel2d.py and the
three picture options of its quiz, g4_quiz_ripples_e38.py, g4_quiz_ripples_e34.py and g4_quiz_ripples_e30.py.

The calculation is the pyqula script webnotes/scripts/session09/g4_friedel_square.py. One impurity of onsite energy
3 sits in the infinite square lattice with the hopping -1, and pyqula's embedding gives the LDOS of 25 x 25 sites
around it at the energies -3.8, -3.4 and -3.0, with the broadening 0.05 on a 150 x 150 k-mesh. The map is that LDOS
minus the LDOS of the clean lattice from the same k-mesh, in units of 1/t. check() asserts what the captions and the
quiz quote: the band -2 (cos kx + cos ky) of the pyqula Hamiltonian, k_F = 0.45, 0.80 and 1.05 along the axes, the
periods pi/k_F = 6.97, 3.95 and 3.00 sites, the wavevector of the ripples along the axes fitted on the map within 5
percent of 2 k_F, the four axes equal by symmetry, the largest change on the impurity site, and the color scale. The
mesh was checked against nk = 250, which changes the maps by less than 1.5 percent of their largest ripple. This file
writes no figure."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
import physcheck

VMAX = 6.0                     # the color scale, in units of 10^-3 / t, the same in every map
TICKS = (-8, -4, 0, 4, 8)      # the sites of the axes, every 4 sites, close to the period 3.95 of E = -3.4


def axis_values(d, i, nmax=12):
    """The change of the LDOS at energy number i on the four half axes, sites 3 to nmax, one row per direction."""
    x, y, m = d['x'], d['y'], d['maps'][i]
    rows = []
    for sx, sy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        rows.append([m[np.where((np.abs(x - sx * n) < 1e-6) & (np.abs(y - sy * n) < 1e-6))[0][0]]
                     for n in range(3, nmax + 1)])
    return np.arange(3, nmax + 1), np.array(rows)


def fit_q(n, v, gamma):
    """The wavevector q of the ripples along an axis, from a least-squares fit by exp(-gamma n)/n (A cos qn + B sin qn),
    the envelope of the LDOS at one energy in two dimensions with the damping of the broadening."""
    qs = np.linspace(0.3, 3.0, 2701)
    res = []
    for q in qs:
        A = (np.exp(-gamma * n) / n)[:, None] * np.array([np.cos(q * n), np.sin(q * n)]).T
        c = np.linalg.lstsq(A, v, rcond=None)[0]
        res.append(np.sum((A @ c - v) ** 2))
    return qs[int(np.argmin(res))]


def check(d):
    """Asserts the numbers of the captions and of the quiz on the variables d of the pyqula script, which the figure
    script gets with style.run_script('session09/g4_friedel_square.py'). Returns d."""
    hk, B = physcheck.from_pyqula(d['h'])
    for k in ((0.3, -1.1), (2.0, 0.4), (np.pi, np.pi)):
        assert abs(hk(k)[0, 0].real + 2 * (np.cos(k[0]) + np.cos(k[1]))) < 1e-12, k
    assert np.allclose(B, 2 * np.pi * np.eye(2))
    assert list(d['energies']) == [-3.8, -3.4, -3.0] and d['delta'] == 0.05 and d['nk'] == 150 and d['nsuper'] == 25
    kF = d['kF']
    assert np.allclose(np.round(kF, 2), [0.45, 0.80, 1.05]), kF
    assert np.allclose(np.round(np.pi / kF, 2), [6.97, 3.95, 3.00]), np.pi / kF
    r = np.hypot(d['x'], d['y'])
    for i, e in enumerate(d['energies']):
        m = d['maps'][i] * 1e3
        assert r[np.argmax(np.abs(m))] < 1e-9                       # the largest change is on the impurity site
        n, rows = axis_values(d, i)
        assert np.abs(rows - rows[0]).max() < 1e-12                  # the four half axes are the same
        q = fit_q(n, rows[0] * 1e3, 2 * d['delta'] / (2 * np.sin(kF[i])))
        print(f'E = {e}: k_F = {kF[i]:.3f}, pi/k_F = {np.pi / kF[i]:.2f}, fitted q/2 = {q / 2:.3f}, '
              f'largest ripple beyond 3 sites {np.abs(m[r >= 3]).max():.2f}e-3', flush=True)
        assert abs(q / (2 * kF[i]) - 1) < 0.05, (e, q, 2 * kF[i])
        assert 0.75 * VMAX < np.abs(m[r >= 3]).max() < 1.05 * VMAX      # the scale shows the ripples, saturates near 0
    return d


def grid(d, i):
    """The map of energy number i as a square array [y, x] with the impurity site left out, and its half width."""
    x, y = np.round(d['x']).astype(int), np.round(d['y']).astype(int)
    c = int(x.max())
    M = np.full((2 * c + 1, 2 * c + 1), np.nan)
    M[y + c, x + c] = d['maps'][i] * 1e3
    M[c, c] = np.nan
    return M, c


def draw_map(ax, d, i, ticks=TICKS, fontsize=8.5):
    """The map of energy number i in real space, with the axes x and y in sites. Returns the image, for a colorbar."""
    M, c = grid(d, i)
    s = np.arange(-c, c + 1)
    im = ax.pcolormesh(s, s, M, cmap='RdBu_r', vmin=-VMAX, vmax=VMAX, shading='nearest', rasterized=True)
    ax.set_aspect('equal')
    ax.set_xlim(-c - 0.5, c + 0.5); ax.set_ylim(-c - 0.5, c + 0.5)
    for s_ in ('top', 'right', 'left', 'bottom'):
        ax.spines[s_].set_visible(True); ax.spines[s_].set_linewidth(0.6)
    ax.set_xticks(ticks); ax.set_yticks(ticks)
    ax.tick_params(length=2.5, width=0.6, labelsize=fontsize - 0.5)
    ax.set_xlabel(r'$x$', fontsize=fontsize, labelpad=1); ax.set_ylabel(r'$y$', fontsize=fontsize, labelpad=1)
    return im


def colorbar(fig, ax, im, label=None, fontsize=8):
    cb = fig.colorbar(im, ax=ax, fraction=0.06, pad=0.04, extend='both', ticks=[-VMAX, -VMAX / 2, 0, VMAX / 2, VMAX])
    cb.ax.tick_params(labelsize=fontsize, length=2, width=0.5)
    cb.outline.set_linewidth(0.5)
    if label:
        cb.set_label(label, fontsize=fontsize)
    return cb


def quiz(script, energy):
    """Writes the picture of one energy, the same map as friedel2d.py with the same color scale, no other text."""
    d = check(style.run_script('session09/g4_friedel_square.py'))
    i = list(d['energies']).index(energy)
    fig, ax = style.plt.subplots(figsize=(4.9 * style.CM, 4.2 * style.CM))
    im = draw_map(ax, d, i, ticks=(-10, 0, 10), fontsize=8)
    colorbar(fig, ax, im, fontsize=7.5)
    style.save(fig, script)
