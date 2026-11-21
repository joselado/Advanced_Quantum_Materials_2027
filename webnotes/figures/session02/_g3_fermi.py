"""Fermi surfaces of the square lattice, the picture options of the quiz on nesting in Section 2.9.

The calculation is the pyqula script webnotes/scripts/session02/g3_fermi_surface.py, h.get_fermi_surface of the square
lattice with the hopping -1, the sign of (2.14), t = 1, at the energies -3t, -t and 0, with the half width 0.15 on 201 by
201 points from -2 pi to 2 pi with both ends. The weight is sum_n delta/((E - E_n)^2 + delta^2), checked here against
the band, so a state exactly at the energy gives 1/delta. It is positive, so the maps take a sequential scale from 0 to
1/delta, the same in the three, in the extended zone with the first zone dashed and the axes of _g3_maps.py.
This file writes no figure, the scripts g3_quiz_fermi_*.py call draw."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style
import _g3_maps as maps

ENERGIES = {'low': -3.0, 'mid': -1.0, 'half': 0.0}


def load():
    """The weights on the periodic grid of 200 by 200 points, the last row and column of pyqula dropped, since the
    window from -2 pi to 2 pi holds both ends, which are the same momenta."""
    d = style.run_script('session02/g3_fermi_surface.py')
    n, delta = d['nk'], d['delta']
    kx, ky = d['kx'].reshape(n, n), d['ky'].reshape(n, n)
    assert np.allclose(kx[:, 0], kx[:, -1]) and np.isclose(kx[0, 0], -2 * np.pi) and np.isclose(kx[-1, 0], 2 * np.pi)
    xs = kx[:-1, 0]
    band = -2 * (np.cos(kx) + np.cos(ky))
    out = {}
    for name, E in ENERGIES.items():
        w = d['w_' + name].reshape(n, n)
        assert np.allclose(w, delta / ((E - band) ** 2 + delta ** 2), atol=1e-9)   # the weight, with the sign of (2.14)
        out[name] = w[:-1, :-1]
    return xs, out, delta


def overlap(w):
    """How much of the weight lands on itself after the shift by Q = (pi, pi), 1 when the shift maps it onto itself."""
    n = w.shape[0]
    s = np.roll(np.roll(w, n // 4, axis=0), n // 4, axis=1)           # n/4 points are pi
    return float((w * s).sum() / (w * w).sum())


def draw(script, name):
    xs, ws, delta = load()
    assert np.isclose(xs[len(xs) // 4] - xs[0], np.pi)
    ov = {k: overlap(w) for k, w in ws.items()}
    print(os.path.basename(script), 'overlap with the shift by Q', {k: round(v, 4) for k, v in ov.items()})
    assert ov['half'] > 0.999 and ov['mid'] < 0.05 and ov['low'] < 0.01
    fig, ax = style.plt.subplots(figsize=(4.6 * style.CM, 4.6 * style.CM))
    ax.pcolormesh(xs, xs, ws[name].T, cmap='Blues', vmin=0, vmax=1 / delta, shading='nearest', rasterized=True)
    ax.set_xlim(-maps.HALF, maps.HALF); ax.set_ylim(-maps.HALF, maps.HALF); ax.set_aspect('equal')
    style.draw_zone(ax, maps.B)
    maps.phi_axes(ax)
    style.save(fig, script)
