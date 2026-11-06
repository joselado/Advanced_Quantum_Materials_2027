"""Session 3, section 3.4 and 3.5, the Berry curvature of the lower band of two gapped honeycomb lattices.

Panel (a) is the Haldane model, a purely imaginary second-neighbor hopping, panel (b) a staggered sublattice
potential. The curvature is Omega = -2 Im <d_kx u | d_ky u> of (3.5), computed on a grid with the gauge-invariant
link variables, and its integral over the Brillouin zone is 2 pi C."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

a1 = np.array([1.0, 0.0]); a2 = np.array([0.5, np.sqrt(3) / 2])
A = np.array([a1, a2])
B = 2 * np.pi * np.linalg.inv(A).T          # rows are b1, b2
deltas = [(a1 + a2) / 3 * 1.0, (a2 - 2 * a1) / 3, (a1 - 2 * a2) / 3]   # nearest neighbors A -> B
nnn = [a1, a2 - a1, -a2]                    # second neighbors, they sum to zero


def hamiltonian(k, t2=0.0, phi=np.pi / 2, M=0.0):
    f = 1 + np.exp(-1j * (k @ a1)) + np.exp(-1j * (k @ a2))     # periodic gauge, lattice vectors only
    dz = M - 2 * t2 * np.sin(phi) * sum(np.sin(k @ b) for b in nnn)
    return np.array([[dz, f], [np.conj(f), -dz]])


def curvature(N, **kw):
    """Returns the cartesian grid and Omega of the lower band, on a grid of N x N points in the reduced zone."""
    u = np.arange(N) / N
    ks = np.array([[ (ui * B[0] + vi * B[1]) for vi in u] for ui in u])
    vec = np.zeros((N, N, 2), complex)
    for i in range(N):
        for j in range(N):
            w, v = np.linalg.eigh(hamiltonian(ks[i, j], **kw))
            vec[i, j] = v[:, 0]
    def link(v1, v2):
        z = np.sum(np.conj(v1) * v2, axis=-1)
        return z / np.abs(z)
    U1 = link(vec, np.roll(vec, -1, axis=0))
    U2 = link(vec, np.roll(vec, -1, axis=1))
    F = np.angle(U1 * np.roll(U2, -1, axis=0) / np.roll(U1, -1, axis=1) / U2)
    area = abs(np.linalg.det(B)) / N ** 2
    return ks, F / area, F.sum() / (2 * np.pi)

N = 90
cases = (dict(t2=0.1), dict(M=0.5))
res = [curvature(N, **kw) for kw in cases]
vmax = max(np.abs(r[1]).max() for r in res)
fig, axs = style.plt.subplots(1, 2, figsize=(style.WIDTH_CM * style.CM, 5.4 * style.CM))
shift = -(B[0] + B[1]) / 2
u = np.arange(N + 1) / N
for ax, (ks, om, C) in zip(axs, res):
    P = np.array([[ui * B[0] + vi * B[1] + shift for vi in u] for ui in u])
    om_p = np.pad(om, ((0, 1), (0, 1)), mode='wrap')
    im = ax.pcolormesh(P[..., 0], P[..., 1], om_p, cmap='RdBu_r', vmin=-vmax, vmax=vmax, shading='nearest', rasterized=True)
    ax.set_aspect('equal')
    ax.axis('off')
    print('C =', C, 'max|Omega| =', abs(om).max())
cs = [r[2] for r in res]
axs[0].text(0.5, -0.03, r'(a) Haldane coupling, $|C|=%d$' % abs(round(cs[0])), transform=axs[0].transAxes, ha='center', va='top', fontsize=9)
axs[1].text(0.5, -0.03, r'(b) staggered potential, $|C|=%d$' % abs(round(cs[1])), transform=axs[1].transAxes, ha='center', va='top', fontsize=9)
cb = fig.colorbar(im, ax=list(axs), orientation='vertical', fraction=0.03, pad=0.06)
cb.set_ticks([-vmax, 0, vmax]); cb.set_ticklabels([r'$-\Omega_{\max}$', '0', r'$+\Omega_{\max}$'])
cb.outline.set_visible(False)
cb.ax.tick_params(labelsize=8, length=2)
style.save(fig, __file__)
