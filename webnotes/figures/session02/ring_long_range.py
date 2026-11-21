"""Session 2, the five-site ring with first-neighbor hopping only and with a second-neighbor hopping added.

H1 = -t sum (c_j^+ c_{j+1} + h.c.), H2 = H1 - t2 sum (c_j^+ c_{j+2} + h.c.), t2 = 0.8 t. The matrices come from the
downloadable script webnotes/scripts/session02/g1_ring_five_sites.py, where pyqula builds the ring as a chain with a
cell of five sites at k=0. Both matrices commute with the rotation of the ring, so the five Fourier modes are
eigenstates of both, and each mode has the weight 1/5 on every site. Only the energies change. The energy of a mode
is read from the pyqula matrix, and it is checked against the formulas of the caption and the levels of pyqula.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

FS = 10.5
d = style.run_script('session02/g1_ring_five_sites.py')
L, t, t2 = 5, 1.0, d['t2']
assert t2 == 0.8
phis = 2 * np.pi * np.arange(L) / L
modes = np.array([np.exp(1j * p * np.arange(L)) / np.sqrt(L) for p in phis])
S = np.roll(np.eye(L), 1, axis=0)                           # the rotation of the ring, in either sense
E = {}
for name in ('first', 'second'):
    Hm = np.asarray(d['ring_' + name])
    assert np.allclose(Hm, Hm.conj().T) and np.allclose(Hm @ S, S @ Hm) and np.allclose(Hm @ S.T, S.T @ Hm)
    e = []
    for v in modes:
        w = Hm @ v
        en = (v.conj() @ w).real
        assert np.allclose(w, en * v)                       # each Fourier mode is an eigenstate of the pyqula matrix
        assert np.allclose(np.abs(v) ** 2, 1 / L)           # with the weight 1/5 on every site
        e.append(en)
    E[name] = np.array(e)
    assert np.allclose(np.sort(E[name]), d['levels_' + name])   # the five modes give the five levels of pyqula
    w0, V0 = np.linalg.eigh(Hm)
    assert w0[1] - w0[0] > 1.0                              # the ground state is single, so it is the mode phi = 0
    assert np.allclose(np.abs(V0[:, 0]) ** 2, 1 / L)
assert np.allclose(E['first'], -2 * t * np.cos(phis))
assert np.allclose(E['second'], -2 * t * np.cos(phis) - 2 * t2 * np.cos(2 * phis))
assert np.allclose(d['levels_second'], [-3.6, 0.6764, 0.6764, 1.1236, 1.1236], atol=1e-4)

fig = plt.figure(figsize=(12.5 * style.CM, 6.4 * style.CM))
gs = fig.add_gridspec(2, 2, width_ratios=[0.8, 1.25], wspace=0.25, hspace=0.12)
axr1, axr2 = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[1, 0])
axE = fig.add_subplot(gs[:, 1])
ang = np.pi / 2 + 2 * np.pi * np.arange(L) / L
xy = np.c_[np.cos(ang), np.sin(ang)]
for ax, second, col in ((axr1, False, style.ACCENT), (axr2, True, style.BROKEN)):
    ax.set_aspect('equal'); ax.axis('off')
    for j in range(L):
        ax.plot(*xy[[j, (j + 1) % L]].T, color=style.INK, lw=1.6, zorder=1)
        if second:
            ax.plot(*xy[[j, (j + 2) % L]].T, color=style.BROKEN, lw=1.1, zorder=1)
    ax.scatter(xy[:, 0], xy[:, 1], s=46, color=col, zorder=3)
    ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.2, 1.25)
style.label(axr1, -1.75, 0, r'$t$', fontsize=FS)
style.label(axr2, -1.75, 0.25, r'$t$', fontsize=FS)
style.label(axr2, -1.75, -0.3, r'$t_2$', fontsize=FS, color=style.BROKEN)
axr1.set_xlim(-2.2, 1.3); axr2.set_xlim(-2.2, 1.3)
p = np.linspace(-np.pi, np.pi, 300)
axE.plot(p, -2 * t * np.cos(p), color=style.GRID, lw=1.2, zorder=0)
axE.plot(p, -2 * t * np.cos(p) - 2 * t2 * np.cos(2 * p), color=style.GRID, lw=1.2, zorder=0)
pw = np.angle(np.exp(1j * phis))                          # the phases in (-pi, pi]
axE.scatter(pw, E['first'], s=34, color=style.ACCENT, zorder=3)
axE.scatter(pw, E['second'], s=34, color=style.BROKEN, zorder=3, marker='s')
style.arrows(axE, xlabel=r'$\varphi$', ylabel=r'$\epsilon/t$')
axE.set_xticks([-np.pi, 0, np.pi]); axE.set_xticklabels([r'$-\pi$', r'$0$', r'$\pi$'])
axE.set_yticks([-2, 0, 2]); axE.tick_params(labelsize=FS, length=2.5)
axE.spines['bottom'].set_visible(True); axE.spines['left'].set_visible(True)
axE.set_xlim(-np.pi - 0.2, np.pi + 0.2); axE.set_ylim(-3.9, 3.2)
for a in (axE,):
    for lab in a.get_xticklabels() + a.get_yticklabels():
        lab.set_fontsize(FS)
style.label(axE, 2.05, -2.85, 'weight $1/5$ on\nevery site', fontsize=FS, linespacing=1.2)
style.save(fig, __file__)
