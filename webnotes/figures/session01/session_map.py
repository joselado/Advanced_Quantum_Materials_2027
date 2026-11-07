"""Session 1, where the session sits in the course, a small concept map.

Built from lecture_notes/WEB_NOTES_CONCEPTS.md. The middle column holds the concepts that this session defines,
the right column the sessions where they come back, with the section of the table. Each edge is one row of
the table (Mean field, Hubbard model, Charge density wave, Spontaneous symmetry breaking, Nambu spinor and BdG,
Bloch's theorem), plus the counting 2^L of Section 1.9, which Section 7.3 uses.
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


def box(col, y, text, kind, h=0.96):
    x0, w = COL[col]
    fc, ec, tc = {'before': ('white', style.MUTED, style.INK),
                  'here': ('#e8eef5', style.ACCENT, style.ACCENT),
                  'after': ('white', style.BROKEN, style.INK)}[kind]
    ax.add_patch(FancyBboxPatch((x0, y - h / 2), w, h, boxstyle='round,pad=0,rounding_size=0.18',
                                fc=fc, ec=ec, lw=1.0))
    ax.text(x0 + w / 2, y, text, ha='center', va='center', fontsize=FS, color=tc, linespacing=1.15)
    return (x0, x0 + w, y)


def edge(a, b, color=style.MUTED):
    ax.add_patch(FancyArrowPatch((a[1], a[2]), (b[0], b[2]), arrowstyle='-|>', mutation_scale=9,
                                 color=color, lw=0.9, shrinkA=1, shrinkB=1))


for col, txt in (('before', 'before'), ('here', 'Session 1'), ('after', 'comes back in')):
    x0, w = COL[col]
    ax.text(x0 + w / 2, HEAD, txt, ha='center', va='center', fontsize=FS + 0.5,
            color=style.ACCENT if col == 'here' else style.INK)

ys = [H - 1.45 - 1.32 * i for i in range(6)]
b1 = box('before', ys[1], 'one-particle\nquantum\nmechanics', 'before', h=1.42)
b2 = box('before', ys[3], 'linear\nalgebra', 'before')

yh = [H - 1.6 - 1.6 * i for i in range(5)]
sq = box('here', yh[0], 'second\nquantization', 'here')
fock = box('here', yh[1], r'Fock space with' + '\n' + r'$2^L$ states', 'here')
mf = box('here', yh[2], 'mean field', 'here')
orders = box('here', yh[3], 'CDW, magnet,\nsuperconductor', 'here')
ssb = box('here', yh[4], 'symmetry\nbreaking', 'here')

s2 = box('after', ys[0], "Session 2\nBloch's theorem", 'after')
s7 = box('after', ys[1], 'Session 7\ntensor networks', 'after')
s5 = box('after', ys[2], 'Session 5\npairing and BdG', 'after')
s6 = box('after', ys[3], 'Session 6\nHubbard magnet', 'after')
s9 = box('after', ys[4], 'Session 9\nPeierls CDW', 'after')
s10 = box('after', ys[5], 'Session 10\ntopological order', 'after')

for a in (b1, b2):
    edge(a, sq)
edge(b1, fock)
edge(sq, s2, style.ACCENT)
edge(fock, s7, style.ACCENT)
edge(mf, s5, style.ACCENT)
edge(mf, s6, style.ACCENT)
edge(orders, s9, style.ACCENT)
edge(ssb, s10, style.ACCENT)
style.save(fig, __file__)
