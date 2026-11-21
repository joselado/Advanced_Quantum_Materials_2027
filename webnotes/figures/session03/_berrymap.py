"""Small maps of the Berry curvature of the filled band of a gapped honeycomb lattice, the picture options of a quiz.

The calculation is the pyqula script webnotes/scripts/session03/berry_curvature_three_lattices.py. The maps are drawn
as berry_haldane.py draws them, b / 2 pi in the extended zone with the first Brillouin zone dashed and the axes k_x
and k_y, so red is a positive Omega = -2 Im <d_kx u | d_ky u> of Section 3.5. The color scale is the same in the three
maps, and it saturates at 5, well below the peaks, so that the weak spots of the third lattice can be seen.
This file writes no figure, the scripts quiz_berrymap_*.py call draw."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

VMAX = 5


def draw(script, name, expect):
    """Writes the map of one lattice. expect is its Chern number, with its sign, checked here."""
    d = style.run_script('session03/berry_curvature_three_lattices.py')
    m = d['omega_' + name] / (2 * np.pi)
    C = d['chern_' + name]
    print(os.path.basename(script), 'Chern number', round(float(C), 4), 'average', round(m.mean(), 4),
          'largest red', round(m.max(), 2), 'largest blue', round(m.min(), 2))
    assert abs(C - expect) < 1e-6 and abs(m.mean() - expect) < 1e-6, C
    fig, ax = style.plt.subplots(figsize=(4.6 * style.CM, 4.6 * style.CM))
    style.pyqula_kmap(ax, d['g'], d['kx'], d['ky'], m, half=3.3, cmap='RdBu_r', vmin=-VMAX, vmax=VMAX)
    style.kaxes(ax)
    style.save(fig, script)
    return m
