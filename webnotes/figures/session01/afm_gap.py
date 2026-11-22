"""Session 1, the local moment and the Mott gap of the antiferromagnetic mean-field solution of the Hubbard chain (1.7)
at half filling, redrawn on 2026-11-21 with ticks and from pyqula.

The calculation is the pyqula script webnotes/scripts/session01/g4_hubbard_chain.py, which the student downloads under
the figure: the chain with two sites per cell, the two spins and the first-neighbor hopping +1 of pyqula, the term
U n_up n_dn, an antiferromagnetic guess and a mesh of 400 cells for the loop and for get_vev("mz"), which is the m of
(1.8). The sign of the hopping changes no moment and no gap on this bipartite chain. The asserts check the script
against two routes with numpy, the gap equation 1 = (U/2) (1/pi) int dk / sqrt(D^2 + 4 t^2 cos^2 k) with D = U m / 2 on
a dense mesh, and a self-consistent ring of 120 sites in real space at U = 3t, and they check the numbers of the
caption: m = 0.03 at U = t, 0.62 at U = 3t and 0.94 at U = 8t, the gap U m, 1.86t at U = 3t, which stays below U."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
import style

t = 1.0
FS = 10.5
kk = np.linspace(-np.pi / 2, np.pi / 2, 20001)           # reduced zone of the doubled cell
eps = lambda k: 2 * t * np.cos(k)


def gap_of_U(U):
    # staggered mean field Delta = U m / 2, self-consistency 1 = (U/2) <1/sqrt(Delta^2 + eps^2)>_k
    f = lambda D: (U / 2) * np.trapezoid(1 / np.sqrt(D ** 2 + eps(kk) ** 2), kk) / np.pi - 1
    return brentq(f, 1e-9, U)


# check against the real-space solution of a ring, self-consistent loop with N=120 sites at U=3
def ring(U, N=120, it=300):
    n = np.zeros(N); n[::2] = 0.9; n[1::2] = 0.1; ndn = 1 - n; nup = n.copy()
    T = np.zeros((N, N))
    for i in range(N):
        T[i, (i + 1) % N] = T[(i + 1) % N, i] = -t
    for _ in range(it):
        out = []
        for ns in (ndn, nup):                                   # up feels U n_down and down feels U n_up
            w, v = np.linalg.eigh(T + np.diag(U * ns))
            out.append((np.abs(v[:, : N // 2]) ** 2).sum(axis=1))
        new_up, new_dn = out
        nup, ndn = 0.5 * nup + 0.5 * new_up, 0.5 * ndn + 0.5 * new_dn
    return nup - ndn


U0 = 3.0
r = ring(U0); m_ring = np.abs(r[0]); D0 = gap_of_U(U0)
assert abs(U0 * m_ring / 2 - D0) < 0.02, (U0 * m_ring / 2, D0)

d = style.run_script('session01/g4_hubbard_chain.py')
Us, ms, gaps = np.array(d['Us']), np.array(d['moment']), np.array(d['gap'])
assert d['nk'] == 400 and len(r) == 120                   # the mesh of 400 cells and the ring of 120 sites
ref = np.array([0.0 if U == 0 else 2 * gap_of_U(U) / U for U in Us])
assert np.all(np.abs(ms - ref) < 1e-3), np.c_[Us, ms, ref]       # pyqula against the gap equation
assert np.all(np.abs(gaps - Us * ms) < 1e-3)                     # the gap is U m
assert np.all(gaps <= Us + 1e-9) and np.all(np.diff(ms) > 0)     # below the line U, a moment that grows
assert abs(m_ring - ms[Us == U0][0]) < 2e-3                      # the ring of 120 sites, 0.62
i = {U: int(np.argmin(np.abs(Us - U))) for U in (1.0, 3.0, 8.0)}
assert abs(ref[i[1.0]] - 0.0299) < 2e-4 and abs(ms[i[1.0]] - 0.03) < 1e-3          # 0.03 at U = t
assert abs(ms[i[3.0]] - 0.621) < 1e-3 and abs(gaps[i[3.0]] - 1.862) < 1e-3          # 0.62 and 1.86t at U = 3t
assert abs(ms[i[8.0]] - 0.939) < 1e-3 and ms[0] < 1e-9 and gaps[0] < 1e-9           # 0.94 at U = 8t, none at U = 0
print('m at U=1, 3, 8:', ms[i[1.0]], ms[i[3.0]], ms[i[8.0]], ' gap at U=3:', gaps[i[3.0]], ' ring:', m_ring)

fig = plt.figure(figsize=(13.0 * style.CM, 5.6 * style.CM))
gs = fig.add_gridspec(1, 2, wspace=0.45)
a, b = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
for ax in (a, b):
    style.arrows(ax, ticks=True)
    ax.spines['bottom'].set_visible(True); ax.spines['left'].set_visible(True)
    ax.tick_params(labelsize=FS, length=2.5)
    ax.set_xticks([0, 2, 4, 6, 8]); ax.set_xlim(0, 8.4)
    ax.annotate(r'$U/t$', xy=(1.03, 0), xycoords='axes fraction', ha='left', va='center', fontsize=FS)
# (a) the local moment m of (1.8) on a site
a.plot(Us, ms, color=style.ACCENT, marker='o', ms=3.2)
style.guide(a, y=1.0)
a.set_ylim(0, 1.1); a.set_yticks([0, 0.5, 1]); a.set_yticklabels(['0', '0.5', '1'])
a.annotate(r'$m$', xy=(0, 1.06), xycoords='axes fraction', ha='center', va='bottom', fontsize=FS)
a.text(0.5, 1.12, 'local moment', transform=a.transAxes, fontsize=FS, ha='center', va='bottom', color=style.MUTED)
# (b) the gap 2 Delta = U m, and the line U
b.plot(Us, Us, color=style.MUTED, lw=1.1, ls=(0, (4, 3)))
b.plot(Us, gaps, color=style.ACCENT, marker='o', ms=3.2)
b.set_ylim(0, 8.4); b.set_yticks([0, 2, 4, 6, 8])
style.label(b, 6.3, 7.4, r'$U$', color=style.MUTED, fontsize=FS)
style.label(b, 4.9, 2.4, r'gap $=Um$', color=style.ACCENT, fontsize=FS, ha='left')
b.annotate(r'gap$/t$', xy=(0, 1.06), xycoords='axes fraction', ha='center', va='bottom', fontsize=FS)
b.text(0.5, 1.12, 'Mott gap', transform=b.transAxes, fontsize=FS, ha='center', va='bottom', color=style.MUTED)
style.save(fig, __file__)
