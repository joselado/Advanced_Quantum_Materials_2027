"""Session 6, what the anomalous terms a_i b_j do to the antiferromagnetic magnon of a chain.

For each k the linear spin-wave Hamiltonian of the Neel state couples a_k with b^dagger_{-k},
H_k = J S z [[1, lam gamma_k], [lam gamma_k, 1]] with gamma_k = cos k and z=2, where lam multiplies the anomalous
terms (lam=1 is the Heisenberg model). The bosonic (Bogoliubov) diagonalization takes the eigenvalues of
sigma_z H_k, computed here numerically, which gives E = J S z sqrt(1 - lam^2 gamma_k^2), so (6.9) for lam=1.
(a) The dispersion for lam = 0, 0.6 and 1, in units of J S z. Without anomalous terms every magnon costs J S z.
(b) For lam=1, the weight v_k^2 of the eigenvector, normalized with |u|^2 - |v|^2 = 1, which is the number of
Holstein-Primakoff bosons per mode in the new vacuum. It is nonzero for every k, so the magnon vacuum is not the
boson vacuum, and it grows without bound near k=0 and k=pi.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

s3 = np.diag([1., -1.])
k = np.linspace(-np.pi, np.pi, 801)


def bog(lam, kk):
    g = np.cos(kk)
    Hk = np.array([[1, lam * g], [lam * g, 1]])          # in units of J S z
    w, V = np.linalg.eig(s3 @ Hk)
    i = np.argmax(w.real)                                 # the positive branch
    u, v = V[:, i].real
    norm = u * u - v * v
    return w[i].real, v * v / norm


E = {lam: np.array([bog(lam, q)[0] for q in k]) for lam in (0.0, 0.6, 1.0)}
for lam in E:
    assert np.allclose(E[lam], np.sqrt(1 - lam**2 * np.cos(k)**2), atol=1e-9)
kv = k[(abs(k) > 0.08) & (abs(abs(k) - np.pi) > 0.08)]
v2 = np.array([bog(1.0, q)[1] for q in kv])
assert np.allclose(v2, 0.5 * (1 / np.abs(np.sin(kv)) - 1), atol=1e-9) and v2.min() >= -1e-12

FS = 12
style.plt.rcParams['font.size'] = FS          # labels of the arrows too, for a phone
fig, axs = style.figure(height_cm=5.6, width_cm=13.0, ncols=2, gridspec_kw=dict(wspace=0.35))
ax = axs[0]
cols = {0.0: style.MUTED, 0.6: style.LIGHT, 1.0: style.ACCENT}
for lam in (0.0, 0.6, 1.0):
    ax.plot(k, E[lam], color=cols[lam], lw=2.0 if lam == 1.0 else 1.6)
style.arrows(ax, xlabel='$k$', ylabel=r'$E$')
style.label(ax, -2.3, 1.3, r'$\lambda=0$', color=style.MUTED, fontsize=FS - 1)
style.label(ax, 0, 1.3, r'$\lambda=0.6$', color=style.LIGHT, fontsize=FS - 1)
style.label(ax, 2.3, 1.3, r'$\lambda=1$', color=style.ACCENT, fontsize=FS - 1)
for x, lab in ((-np.pi, r'$-\pi$'), (0, '$0$'), (np.pi, r'$\pi$')):
    style.label(ax, x, -0.05, lab, fontsize=FS - 0.5, va='top')
ax.text(-np.pi - 0.12, 1.0, '$1$', ha='right', va='center', fontsize=FS - 0.5)
ax.text(-0.2, 1.07, '(a)', transform=ax.transAxes, fontsize=FS, ha='left', va='bottom')
ax.set_xlim(-np.pi, np.pi); ax.set_ylim(0, 1.42)

ax = axs[1]
for side in (kv < 0, kv > 0):
    for part in ((abs(kv) < np.pi / 2), (abs(kv) > np.pi / 2)):
        m = side & part
        ax.plot(kv[m], v2[m], color=style.ACCENT)
style.arrows(ax, xlabel='$k$', ylabel=r'$v_k^2$')
for x, lab in ((-np.pi, r'$-\pi$'), (0, '$0$'), (np.pi, r'$\pi$')):
    style.label(ax, x, -0.1, lab, fontsize=FS - 0.5, va='top')
ax.text(-np.pi - 0.12, 1.0, '$1$', ha='right', va='center', fontsize=FS - 0.5)
style.guide(ax, y=1.0)
ax.text(-0.3, 1.07, '(b)', transform=ax.transAxes, fontsize=FS, ha='left', va='bottom')
ax.set_xlim(-np.pi, np.pi); ax.set_ylim(0, 2.6)
style.save(fig, __file__)
