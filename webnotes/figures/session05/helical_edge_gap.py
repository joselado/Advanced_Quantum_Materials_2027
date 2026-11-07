"""Session 5, the helical edge of a quantum spin Hall insulator with a magnet and with pairing.

(a) The edge bands H0(k) = v k sigma_z, spin up moving right and spin down moving left, and the same edge under a
magnet, H0 + h sigma_x, where a gap 2h opens at k=0.
(b) The BdG Hamiltonian of the edge in the Nambu basis (5.6), H = tau_z (v k sigma_z - mu) + h sigma_x + Delta tau_x,
diagonalized at k=0 as a function of h, for mu=0. The four levels are +-h +- Delta, and the gap closes at h=Delta.
A region gapped by pairing (h<Delta) and a region gapped by the magnet (h>Delta) cannot be joined without closing
the gap, which is why a Majorana zero mode sits at the interface between a magnet and a superconductor.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

s0 = np.eye(2); sx = np.array([[0, 1], [1, 0]]); sz = np.diag([1., -1.])
v, mu, D = 1.0, 0.0, 1.0

def bdg(k, h):
    return np.kron(sz, v * k * sz - mu * s0) + h * np.kron(s0, sx) + D * np.kron(sx, s0)

k = np.linspace(-2.2, 2.2, 401)
h_a = 0.7
up, dn = v * k, -v * k                                   # the two helical branches, sigma_z = +1 and -1
mag = np.array([np.linalg.eigvalsh(v * kk * sz + h_a * sx) for kk in k])
assert abs((mag[200, 1] - mag[200, 0]) - 2 * h_a) < 1e-12        # the gap 2h at k=0

hs = np.linspace(0, 2.2, 441)
lev = np.array([np.linalg.eigvalsh(bdg(0.0, h)) for h in hs])
# the full gap over k, not only at k=0, closes at h=Delta and nowhere else
kk = np.linspace(-3, 3, 1201)
gap = np.array([min(abs(np.linalg.eigvalsh(bdg(q, h))).min() for q in kk) for h in hs[::10]])
assert gap[np.argmin(abs(hs[::10] - D))] < 1e-9 and np.all(gap[abs(hs[::10] - D) > 0.05] > 0.04)
assert np.allclose(np.sort(lev, axis=1), np.sort(np.c_[hs + D, hs - D, -hs + D, -hs - D], axis=1))

FS = 12
style.plt.rcParams['font.size'] = FS          # labels of the arrows too, for a phone
fig, axs = style.figure(height_cm=6.0, width_cm=13.0, ncols=2, gridspec_kw=dict(wspace=0.38))
ax = axs[0]
ax.plot(k, up, color=style.BROKEN, lw=1.6, ls=(0, (4, 2)))
ax.plot(k, dn, color=style.ACCENT, lw=1.6, ls=(0, (4, 2)))
ax.plot(k, mag[:, 0], color=style.INK, lw=2.0)
ax.plot(k, mag[:, 1], color=style.INK, lw=2.0)
style.guide(ax, y=0)
ax.annotate('', xy=(0, h_a), xytext=(0, -h_a), arrowprops=dict(arrowstyle='<->', color=style.INK, lw=0.9, shrinkA=0, shrinkB=0))
style.label(ax, 0.42, 0.0, '$2h$', ha='left', fontsize=FS)
style.label(ax, 1.65, 2.2, r'$\uparrow$', color=style.BROKEN, fontsize=FS + 2)
style.label(ax, -1.65, 2.2, r'$\downarrow$', color=style.ACCENT, fontsize=FS + 2)
style.label(ax, 0, -2.35, 'with a magnet', fontsize=FS)
style.arrows(ax, xlabel='$k$', ylabel='$E$')
ax.text(-0.2, 1.07, '(a)', transform=ax.transAxes, fontsize=FS, ha='left', va='bottom')
ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.6, 2.6)

ax = axs[1]
for j in range(4):
    ax.plot(hs, lev[:, j], color=style.ACCENT)
style.guide(ax, y=0)
style.guide(ax, x=D, color=style.MUTED, lw=0.8, ls=(0, (3, 2)))
ax.plot(D, 0, 'o', color=style.BROKEN, ms=5, zorder=5)
style.arrows(ax, xlabel=r'$h/\Delta$', ylabel=r'$E$')
style.label(ax, D, -3.55, '$1$', fontsize=FS - 0.5, va='top')
style.label(ax, 0.45, -2.6, 'pairing', fontsize=FS - 0.5)
style.label(ax, 1.7, -1.72, 'magnet', fontsize=FS - 0.5)
ax.text(-0.2, 1.07, '(b)', transform=ax.transAxes, fontsize=FS, ha='left', va='bottom')
ax.set_xlim(0, 2.2); ax.set_ylim(-3.3, 3.5)
style.save(fig, __file__)
