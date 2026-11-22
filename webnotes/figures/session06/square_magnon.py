"""Session 6, Section 6.15, the ferromagnetic magnon (6.8) of the square lattice along the path Gamma, X, M, Gamma.

The picture sits in the feedback of the quiz at (pi, pi). The calculation is the pyqula script
webnotes/scripts/session06/g4_magnon_square.py, which the student downloads under the figure: the magnon is a boson
that hops with -|J|S to the four neighbors (tij=[-1.]) and has the onsite energy z|J|S = 4 (h.add_onsite(4.)), with
|J|S = 1, so its band is E = 4|J|S (1 - gamma) with gamma = (cos kx + cos ky)/2. The path is given as reduced momenta,
so steps 0, 100, 200 and 300 are Gamma, X, M and Gamma. The asserts check the band against the closed form at every
step, and the values 0, 4 and 8 at Gamma, X and M that the feedback quotes."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

d = style.run_script('session06/g4_magnon_square.py')
kp, e = np.asarray(d['kpath'], float), np.asarray(d['e'], float)
gamma = 0.5 * (np.cos(2 * np.pi * kp[:, 0]) + np.cos(2 * np.pi * kp[:, 1]))
assert len(e) == 301 and np.allclose(e, 4 * (1 - gamma), atol=1e-12)      # (6.8) with z = 4 and |J|S = 1
assert np.allclose(e[[0, 100, 200, 300]], [0, 4, 8, 0], atol=1e-12)        # Gamma, X, M, Gamma
assert abs(e.min()) < 1e-12 and np.isclose(e.max(), 8) and np.argmax(e) == 200  # zero at Gamma, top at M
x = np.r_[0, np.cumsum(np.linalg.norm(np.diff(kp[:, :2], axis=0), axis=1))] * 2 * np.pi
marks = x[[0, 100, 200, 300]]
assert np.allclose(marks, [0, np.pi, 2 * np.pi, (2 + np.sqrt(2)) * np.pi])

FS = 11
style.plt.rcParams['font.size'] = FS          # the labels of the arrows too, for a phone
fig, ax = style.figure(height_cm=5.0, width_cm=9.0)
for xx in marks:
    style.guide(ax, x=xx)
for yy in (4, 8):
    style.guide(ax, y=yy)
ax.plot(x, e, color=style.ACCENT)
style.arrows(ax, ylabel=r'$E/|J|S$')
ax.set_xticks(marks); ax.set_xticklabels([r'$\Gamma$', r'$X$', r'$M$', r'$\Gamma$'], fontsize=FS)
ax.set_yticks([0, 4, 8]); ax.set_yticklabels(['$0$', '$4$', '$8$'], fontsize=FS)
ax.tick_params(length=2.5, width=0.6, pad=2)
ax.set_xlim(0, marks[-1]); ax.set_ylim(0, 9.2)
style.save(fig, __file__)
