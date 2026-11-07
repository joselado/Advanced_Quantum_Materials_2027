"""Session 2, where the session sits in the course, a small concept map.

Built from lecture_notes/WEB_NOTES_CONCEPTS.md. The middle column holds the concepts that this session defines,
the right column the sessions where they come back. Each edge is one row of the table: Bloch's theorem and
Bloch Hamiltonian (s03/09c, s05/17), Dirac cone (s03/10, s04/10), Flat bands (s04/09, s06/06), Density of states
(s06/06, s09/04), Nesting (s09/04b), ARPES (s10/07), Spin waves and magnons (s06/15), Nambu spinor and BdG (s05/08).
The left column is what the index page of Session 2 takes from Session 1, the hopping (1.2) and mean field.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import style

FS = 10.5
W, H = 12.5, 9.6                                    # in cm, the axes are in cm too
fig = plt.figure(figsize=(W * style.CM, H * style.CM))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')

# columns: x of the left edge and width of the boxes
COL = {'before': (0.05, 2.75), 'here': (3.75, 3.6), 'after': (8.45, 4.0)}
HEAD = H - 0.45


def box(col, y, text, kind):
    x0, w = COL[col]
    fc, ec, tc = {'before': ('white', style.MUTED, style.INK),
                  'here': ('#e8eef5', style.ACCENT, style.ACCENT),
                  'after': ('white', style.BROKEN, style.INK)}[kind]
    ax.add_patch(FancyBboxPatch((x0, y - 0.48), w, 0.96, boxstyle='round,pad=0,rounding_size=0.18',
                                fc=fc, ec=ec, lw=1.0))
    ax.text(x0 + w / 2, y, text, ha='center', va='center', fontsize=FS, color=tc, linespacing=1.15)
    return (x0, x0 + w, y)


def edge(a, b, color=style.MUTED):
    ax.add_patch(FancyArrowPatch((a[1], a[2]), (b[0], b[2]), arrowstyle='-|>', mutation_scale=9,
                                 color=color, lw=0.9, shrinkA=1, shrinkB=1))


for col, txt in (('before', 'from Session 1'), ('here', 'Session 2'), ('after', 'comes back in')):
    x0, w = COL[col]
    ax.text(x0 + w / 2, HEAD, txt, ha='center', va='center', fontsize=FS + 0.5,
            color=style.ACCENT if col == 'here' else style.INK)

ys = [H - 1.45 - 1.32 * i for i in range(6)]
hop = box('before', ys[0] - 0.3, 'hopping' + '\n' + r'$t_{ij}\,c_i^{\dagger} c_j$', 'before')
mfb = box('before', ys[2] - 0.3, 'mean field', 'before')

yh = [H - 1.45 - 1.32 * i for i in range(6)]
bloch = box('here', yh[0], "symmetry,\nBloch's theorem", 'here')
hk = box('here', yh[1], r'Bloch Hamiltonian' + '\n' + r'$H(\mathbf{k})$', 'here')
dirac = box('here', yh[2], 'Dirac cone', 'here')
flat = box('here', yh[3], 'flat bands', 'here')
dos = box('here', yh[4], 'density of states', 'here')
arpes = box('here', yh[5], 'ARPES', 'here')

s3 = box('after', ys[0], 'Session 3\nSSH, Chern insulator', 'after')
s5 = box('after', ys[2], 'Session 5\nBdG bands', 'after')
s4 = box('after', ys[1], 'Session 4\nLandau levels', 'after')
s6 = box('after', ys[3], 'Session 6\nStoner, magnons', 'after')
s9 = box('after', ys[4], 'Session 9\nnesting, Lindhard', 'after')
s10 = box('after', ys[5], 'Session 10\nHamiltonian learning', 'after')

edge(hop, bloch)
x_mid = (bloch[0] + bloch[1]) / 2                     # the theorem gives the Bloch Hamiltonian
ax.add_patch(FancyArrowPatch((x_mid, bloch[2] - 0.48), (x_mid, hk[2] + 0.48), arrowstyle='-|>', mutation_scale=9,
                             color=style.ACCENT, lw=0.9, shrinkA=0, shrinkB=0))
edge(mfb, hk)
edge(hk, s3, style.ACCENT)
edge(hk, s5, style.ACCENT)
edge(dirac, s3, style.ACCENT)
edge(dirac, s4, style.ACCENT)
edge(flat, s4, style.ACCENT)
edge(flat, s6, style.ACCENT)
edge(dos, s6, style.ACCENT)
edge(dos, s9, style.ACCENT)
edge(arpes, s10, style.ACCENT)
style.save(fig, __file__)
