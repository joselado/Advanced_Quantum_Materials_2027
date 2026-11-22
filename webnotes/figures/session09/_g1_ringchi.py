"""Shared code of the picture options of the quiz of Section 9.1 that asks which of three rings of 40 sites is clean.
This file writes no figure, the scripts g1_quiz_ring_*.py call draw.

Each picture is the static density response chi(x, x') of a spinless ring of 40 sites with the hopping -t, at half
filling (mu = 0) and T = 0.05 t, in the sign of webnotes/conventions/session09.md: a potential v at site x changes the
density at x' by -chi(x, x') v, so chi is positive on the diagonal. The quiz says it as an onsite energy lowered by
delta mu, a local shift of the chemical potential, which changes the density at x' by +chi(x, x') delta mu, the sign
of delta A = chi f in the key box of Section 9.1. It is the sum over the pairs of eigenstates a, b
of (f_a - f_b)/(E_b - E_a) psi_a(x) psi_b(x) psi_a(x') psi_b(x'), with -f'(E) for a pair of equal energies. This is
numpy and not pyqula, since the quiz needs the full matrix of a finite ring, which is a few lines of exact
diagonalization. The asserts check the sign against a finite difference of the density and the numbers that the
feedback of the quiz quotes. The three maps share one diverging color scale, white at zero, which saturates at 0.1/t,
so that the weak stripes away from the diagonal can be seen."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

N, MU, T, VMAX = 40, 0.0, 0.05, 0.1
V_IMPURITY, SITE_IMPURITY, W_RANDOM, SEED = 2.0, 20, 1.5, 3


def fermi(e):
    return 0.5 * (1 - np.tanh((e - MU) / (2 * T)))


def hamiltonian(onsite):
    H = np.diag(np.asarray(onsite, dtype=float))
    i = np.arange(N)
    H[i, (i + 1) % N] = H[(i + 1) % N, i] = -1.0
    return H


def density(onsite):
    e, w = np.linalg.eigh(hamiltonian(onsite))
    return (w ** 2) @ fermi(e)


def response(onsite):
    """chi(x, x') of the ring with these onsite energies, positive on the diagonal."""
    e, w = np.linalg.eigh(hamiltonian(onsite))
    f = fermi(e)
    de, df = e[None, :] - e[:, None], f[:, None] - f[None, :]       # E_b - E_a and f_a - f_b
    same = np.abs(de) < 1e-10
    F = np.where(same, (f * (1 - f) / T)[:, None] * np.ones(N), df / np.where(same, 1.0, de))
    A = np.einsum('xa,xb->xab', w, w)
    return np.einsum('xab,ab,yab->xy', A, F, A)


def rings():
    """The onsite energies of the three rings: clean, one impurity, a random potential in [-W, W]."""
    imp = np.zeros(N)
    imp[SITE_IMPURITY] = V_IMPURITY
    rnd = np.random.default_rng(SEED).uniform(-W_RANDOM, W_RANDOM, N)
    return {'clean': np.zeros(N), 'impurity': imp, 'random': rnd}


def spread(chi):
    """The largest change of chi along a line parallel to the diagonal, zero when chi depends only on x' - x."""
    return max(np.ptp([chi[x, (x + d) % N] for x in range(N)]) for d in range(N))


def check():
    """The sign and the numbers of the feedback of the quiz."""
    out = {}
    for name, o in rings().items():
        chi = response(o)
        for j in (0, 7, SITE_IMPURITY):                              # route 2, a finite difference of the density
            dv = 1e-5
            up, dn = o.copy(), o.copy()
            up[j] += dv; dn[j] -= dv
            assert np.abs(chi[:, j] + (density(up) - density(dn)) / (2 * dv)).max() < 1e-7, name
        assert np.allclose(chi, chi.T, atol=1e-12)
        out[name] = chi
    clean, imp, rnd = out['clean'], out['impurity'], out['random']
    d0 = clean[0, 0]
    # the clean ring: one value on every line parallel to the diagonal, 0.25/t on the diagonal
    assert spread(clean) < 1e-10 and round(d0, 2) == 0.25 and np.ptp(np.diag(clean)) < 1e-12
    # one impurity 2t on site 20: chi(20, 20) = 0.09/t against 0.25/t far from it, at site 0
    assert round(imp[SITE_IMPURITY, SITE_IMPURITY], 2) == 0.09 and round(imp[0, 0], 2) == 0.25
    assert spread(imp) > 0.1 and spread(rnd) > 0.1
    # the scale: the diagonal saturates, and the strongest stripe off the diagonal of the clean ring is inside it
    off = np.abs(clean - np.diag(np.diag(clean))).max()
    assert off < VMAX < d0
    print('chi(x,x) of the clean ring %.4f, spread along the diagonals %.1e; impurity chi(20,20) %.4f and chi(0,0) %.4f, '
          'spread %.3f; random spread %.3f; largest |chi| off the diagonal of the clean ring %.4f'
          % (d0, spread(clean), imp[SITE_IMPURITY, SITE_IMPURITY], imp[0, 0], spread(imp), spread(rnd), off))
    return out


def draw(script, name):
    """Writes the map of one ring."""
    chi = check()[name]
    # the map is an image of 40 x 40 cells, drawn at 300 dpi with sharp cells, so that the SVG stays a few tens of kB
    fig, ax = style.plt.subplots(figsize=(4.9 * style.CM, 4.2 * style.CM), dpi=300)
    im = ax.imshow(chi.T, origin='lower', cmap='RdBu_r', vmin=-VMAX, vmax=VMAX, interpolation='nearest',
                   extent=(-0.5, N - 0.5, -0.5, N - 0.5))
    ax.set_aspect('equal')
    ax.set_xlim(-0.5, N - 0.5); ax.set_ylim(-0.5, N - 0.5)
    ticks = [0, 20, 39]
    ax.set_xticks(ticks); ax.set_yticks(ticks)
    ax.set_xticklabels([str(t) for t in ticks], fontsize=10); ax.set_yticklabels([str(t) for t in ticks], fontsize=10)
    ax.tick_params(length=2.5, width=0.6, pad=2)
    ax.set_xlabel(r'$x$', fontsize=12, labelpad=0); ax.set_ylabel(r"$x'$", fontsize=12, labelpad=0)
    cb = fig.colorbar(im, ax=ax, fraction=0.05, pad=0.05, ticks=[-VMAX, 0, VMAX])
    cb.ax.set_yticklabels([r'$-0.1$', r'$0$', r'$0.1$'], fontsize=10)
    cb.ax.tick_params(length=2, width=0.6, pad=1.5)
    cb.outline.set_linewidth(0.5)
    style.save(fig, script)
