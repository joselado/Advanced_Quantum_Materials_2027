"""Session 9, Section 9.7, the density of states around one magnetic impurity in an s-wave chain, against the exchange.

The data come from the downloadable script webnotes/scripts/session09/g5_ysr_chain.py, the cell "Single magnetic impurity
in a superconductor" of session9.ipynb at half filling, without its add_onsite(1.8). The chain has the hopping 1 of pyqula,
add_swave(0.2) is Delta = 0.2t (h.get_gap() is 2 Delta, webnotes/conventions/session09.md), and add_exchange with m_z = J
puts +J and -J on the two spins of one site, so J is the J S of (9.10). At half filling nu_0 = 1/(2 pi t) per spin, so
alpha = pi nu_0 J S = J S/2t, and the sheet gives (9.10) on this chain to 0.004 Delta at Delta = 0.2t. The map is the DOS of
the cell of three sites that holds the impurity at its end, from the embedding in the infinite chain, in units of the normal
state, with the broadening eta = Delta/40, where the notebook cell has Delta/10, and the color scale clipped at 4. The
dashed lines are +-E_b of (9.10). The asserts below are the numbers that the caption quotes. The crossing of the lattice
level, J S = sqrt(4 + Delta^2) = 2.010t from det(1 - J g) = 0, is asserted in webnotes/checks/session09/g5_07_ysr.py."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import matplotlib.pyplot as plt
import style

d = style.run_script('session09/g5_ysr_chain.py')
Js, E, dos, D = np.array(d['Js']), np.array(d['energies']), np.array(d['dos']), d['delta']
assert abs(D - 0.2) < 1e-12 and abs(Js[0]) < 1e-12 and abs(Js[-1] - 4) < 1e-12 and len(Js) == 41
assert abs(d['eta'] - D / 40) < 1e-15                      # the broadening Delta/40 of the caption
assert np.allclose(np.diff(Js), 0.1)                       # the grid of 0.1t in J S of the caption
# the cell of three sites is at x = -1, 0, 1, and the exchange sits on its first site, so the impurity is at one end of the
# cell and the DOS is summed on the impurity and the two sites on one side of it
assert np.allclose(d['g'].r[:, 0], [-1, 0, 1]) and np.allclose(d['m'][:, 2], [Js[-1], 0, 0]) and np.allclose(d['m'][:, :2], 0)
assert abs(d['normal'] - 6 / (2 * np.pi)) < 1e-3          # three sites, two spins, 1/(2 pi t) each, at E_F
eb = lambda J: D * (1 - (J / 2) ** 2) / (1 + (J / 2) ** 2)  # (9.10) with alpha = J S/2t

# the clean gap: at J=0 nothing inside |E| < 0.5 Delta, and the coherence peak above 1
assert dos[0][np.abs(E) < 0.5 * D].max() < 0.05 and dos[0].max() > 1
# the unit: divided by twice the normal state, the clean chain at E = 1.5 Delta gives the BCS ratio E/sqrt(E^2 - Delta^2),
# so the BdG DOS of the embedding counts each state twice, once as an electron and once as a hole
assert abs(E[-1] - 1.5 * D) < 1e-12 and abs(dos[0][-1] / (1.5 / np.sqrt(1.5 ** 2 - 1)) - 1) < 0.01
# the peak of each row at E > 0, refined by a parabola through three points of the energy grid
pos = E >= 0
peaks = []
for row in dos:
    r, ep = np.where(np.abs(E[pos]) < 0.97 * D, row[pos], 0), E[pos]
    k = int(np.argmax(r))
    off = 0.5 * (r[k - 1] - r[k + 1]) / (r[k - 1] - 2 * r[k] + r[k + 1]) if 0 < k < len(r) - 1 else 0.0
    peaks.append(ep[k] + off * (ep[1] - ep[0]))
peaks = np.array(peaks)
sel = Js >= 0.5                                            # away from the coherence peak at the gap edge
dev = np.abs(peaks[sel] - np.abs(eb(Js[sel]))).max() / D
assert dev < 0.01, dev                                     # from J S = 0.5t on the peaks follow +-E_b of (9.10) to 0.01 Delta
i0 = int(np.argmin(np.abs(E)))
assert abs(E[i0]) < 1e-12 and abs(Js[np.argmax(dos[:, i0])] - 2.0) < 1e-9   # the two peaks meet at zero at J S = 2t
assert abs(eb(4.0) / D + 0.6) < 1e-12                      # alpha = 2 gives -0.6 Delta
print('normal DOS', round(d['normal'], 4), 'largest |peak - (9.10)|', round(dev, 4), 'Delta; DOS at E=0 largest at J S =',
      Js[np.argmax(dos[:, i0])])

FS = 11
plt.rcParams.update({'font.size': FS})
fig, ax = plt.subplots(figsize=(11.0 * style.CM, 6.4 * style.CM))
dJ, dE = Js[1] - Js[0], (E[1] - E[0]) / D
edgesJ = np.r_[Js - dJ / 2, Js[-1] + dJ / 2]
edgesE = np.r_[E / D - dE / 2, E[-1] / D + dE / 2]
vmax = 4                                                   # the color scale is clipped at 4, as the caption says
assert dos.max() > vmax                                    # so the clip is real, the peaks of the bound state go above it
mesh = ax.pcolormesh(edgesJ, edgesE, dos.T, cmap='Blues', vmin=0, vmax=vmax, shading="flat", rasterized=True)
Jf = np.linspace(0, 4, 401)
for s in (1, -1):
    ax.plot(Jf, s * eb(Jf) / D, color=style.BROKEN, lw=1.1, ls=(0, (4, 2.5)))
style.guide(ax, x=2.0, color=style.MUTED, lw=0.8, ls=(0, (2, 2)), zorder=3)
style.label(ax, 2.0, 1.62, r'$\alpha=1$', fontsize=FS - 0.5, va='bottom', color=style.MUTED)
ax.set_xlim(edgesJ[0], edgesJ[-1]); ax.set_ylim(-1.5, 1.5)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
for s in ('left', 'bottom'):
    ax.spines[s].set_linewidth(0.6)
ax.set_xticks([0, 1, 2, 3, 4]); ax.set_yticks([-1, 0, 1])
ax.tick_params(length=2.5, width=0.6, pad=2, labelsize=FS - 1)
ax.set_xlabel(r'exchange $JS/t$', fontsize=FS, labelpad=1)
ax.set_ylabel(r'$E/\Delta$', fontsize=FS, labelpad=1)
cb = fig.colorbar(mesh, ax=ax, ticks=[0, 1, 2, 3, 4], extend='max', pad=0.03, fraction=0.06)
cb.ax.tick_params(labelsize=FS - 1, length=2, width=0.6)
cb.outline.set_linewidth(0.6)
cb.set_label('DOS / normal state', fontsize=FS - 0.5, labelpad=3)
style.save(fig, __file__)
