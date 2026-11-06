"""Session 3, section 3.10, the Haldane model with a staggered potential M, at fixed second-neighbor hopping t2=0.1.

The honeycomb lattice with first-neighbor hopping 1, imaginary second-neighbor hopping t2 exp(i pi/2) and the
sublattice potential +-M, as in the figure of Section 3.10. Top, the gap of the bulk, the smallest energy difference of
the two bands over the Brillouin zone. Bottom, the Chern number of the lower band from the link variables on a
60 x 60 grid. The Haldane mass is m_H = 3 sqrt(3) t2 and the two valley masses are M + m_H and M - m_H, so the gap
closes at M = +-m_H, and the Chern number is (1/2)[sgn(M+m_H) - sgn(M-m_H)] as in (3.8)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

a1 = np.array([1.0, 0.0]); a2 = np.array([0.5, np.sqrt(3) / 2])
A = np.array([a1, a2])
B = 2 * np.pi * np.linalg.inv(A).T
nnn = [a1, a2 - a1, -a2]
t2 = 0.1
mH = 3 * np.sqrt(3) * t2


def H(k, M):
    f = 1 + np.exp(-1j * (k @ a1)) + np.exp(-1j * (k @ a2))
    dz = M - 2 * t2 * sum(np.sin(k @ b) for b in nnn)
    return np.array([[dz, f], [np.conj(f), -dz]])


def grid(N):
    u = np.arange(N) / N
    return np.array([[ui * B[0] + vi * B[1] for vi in u] for ui in u])


def chern_gap(M, N=60, Ng=120):
    ks = grid(N)
    vec = np.zeros((N, N, 2), complex)
    for i in range(N):
        for j in range(N):
            vec[i, j] = np.linalg.eigh(H(ks[i, j], M))[1][:, 0]
    def link(v1, v2):
        z = np.sum(np.conj(v1) * v2, axis=-1)
        return z / np.abs(z)
    U1 = link(vec, np.roll(vec, -1, axis=0)); U2 = link(vec, np.roll(vec, -1, axis=1))
    F = np.angle(U1 * np.roll(U2, -1, axis=0) / np.roll(U1, -1, axis=1) / U2)
    C = F.sum() / (2 * np.pi)
    g = min(np.diff(np.linalg.eigvalsh(H(k, M)))[0] for k in grid(Ng).reshape(-1, 2))
    return C, g


Ms = np.linspace(-1.0, 1.0, 81)
res = np.array([chern_gap(M) for M in Ms])
C = res[:, 0]
Mg = np.sort(np.concatenate([Ms, [-mH, mH]]))      # the gap is also computed exactly at M = +-m_H, where it closes at K
gap = np.array([chern_gap(M, N=3, Ng=120)[1] for M in Mg])
pred = 0.5 * (np.sign(Ms + mH) - np.sign(Ms - mH))
print('mH', mH, 'max |C| deviation from integers', np.abs(C - np.round(C)).max())
bad = [(M, c, p) for M, c, p in zip(Ms, np.abs(C), np.abs(pred)) if abs(round(c) - p) > 0.01 and abs(abs(M) - mH) > 0.03]
print('mismatches away from the transition', bad)
print('gap at M=0', gap[np.argmin(abs(Mg))], 'expected', 2 * mH)

fig, axs = style.figure(nrows=2, height_cm=6.8, sharex=True, gridspec_kw=dict(hspace=0.25))
ax = axs[0]
ax.set_xlim(-1.0, 1.0); ax.set_ylim(0, 1.25)
ax.plot(Mg, gap, color=style.ACCENT)
style.arrows(ax, ylabel=r'gap')
style.guide(ax, x=mH, ls=':'); style.guide(ax, x=-mH, ls=':')
ax = axs[1]
ax.set_ylim(-0.15, 1.45)
ax.step(Ms, np.abs(np.round(C)), where='mid', color=style.ACCENT)
style.guide(ax, x=mH, ls=':'); style.guide(ax, x=-mH, ls=':')
style.arrows(ax, xlabel=r'$M$', ylabel=r'$|C|$')
ax.set_xticks([-mH, 0, mH]); ax.set_xticklabels([r'$-m_H$', '0', r'$m_H$'])
ax.tick_params(length=2.5, width=0.6)
ax.set_yticks([0, 1]); ax.set_yticklabels(['0', '1'])
style.label(ax, 0, 1.2, 'Chern insulator', fontsize=8.5, color=style.ACCENT)
style.label(ax, -0.78, 0.35, 'trivial', fontsize=8.5, color=style.MUTED)
style.label(ax, 0.78, 0.35, 'trivial', fontsize=8.5, color=style.MUTED)
style.save(fig, __file__)
