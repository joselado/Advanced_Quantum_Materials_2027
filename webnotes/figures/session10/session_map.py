"""Session 10, where the session sits in the course, a small concept map.

Built from lecture_notes/WEB_NOTES_CONCEPTS.md, in the shape of webnotes/figures/session01/session_map.py. The left
column holds what the session takes from earlier sessions (Bond dimension and MPS, Mean field, Spontaneous symmetry
breaking and the Chern number, Linear response and ARPES, and the forward arrow of Section 1.4), the middle column
what it builds (Sections 10.3 to 10.7), and the right column where it points. This is the last session, so the right column closes the
loop, back to Section 1.4 and to the summary of Section 10.8.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import style

FS = 12
W, H = 12.7, 8.95                                   # in cm, the axes are in cm too
fig = plt.figure(figsize=(W * style.CM, H * style.CM))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')

COL = {'before': (0.05, 3.55), 'here': (4.35, 3.75), 'after': (8.9, 3.75)}
HEAD = H - 0.4


def box(col, y, text, kind):
    x0, w = COL[col]
    fc, ec, tc = {'before': ('white', style.MUTED, style.INK),
                  'here': ('#e8eef5', style.ACCENT, style.ACCENT),
                  'after': ('white', style.BROKEN, style.INK)}[kind]
    ax.add_patch(FancyBboxPatch((x0, y - 0.6), w, 1.2, boxstyle='round,pad=0,rounding_size=0.18',
                                fc=fc, ec=ec, lw=1.0))
    ax.text(x0 + w / 2, y, text, ha='center', va='center', fontsize=FS, color=tc, linespacing=1.15)
    return (x0, x0 + w, y)


def edge(a, b, color=style.MUTED):
    ax.add_patch(FancyArrowPatch((a[1], a[2]), (b[0], b[2]), arrowstyle='-|>', mutation_scale=9,
                                 color=color, lw=0.9, shrinkA=1, shrinkB=1))


for col, txt in (('before', 'before'), ('here', 'Session 10'), ('after', 'closes the loop')):
    x0, w = COL[col]
    ax.text(x0 + w / 2, HEAD, txt, ha='center', va='center', fontsize=FS + 0.5,
            color=style.ACCENT if col == 'here' else style.INK)

def row(r):
    return H - 1.35 - 1.36 * r


s7 = box('before', row(0.5), 'Session 7\nMPS, variational', 'before')
s1 = box('before', row(2), 'Session 1\nmean field', 'before')
s13 = box('before', row(3), 'Sessions 1, 3\norder, topology', 'before')
s9 = box('before', row(4), 'Sessions 2, 9\nARPES, response', 'before')
s14 = box('before', row(5), 'Section 1.4\n$H\\to\\mathcal{O}$', 'before')

nqs = box('here', row(0), 'network\nwavefunctions', 'here')
tn = box('here', row(1), 'tensor networks\nas classifiers', 'here')
dft = box('here', row(2), 'learning\nin DFT', 'here')
pha = box('here', row(3), 'phase\nclassification', 'here')
ham = box('here', row(4.5), 'Hamiltonian\nlearning', 'here')

a1 = box('after', row(3), 'Section 10.8\nthe loop closed', 'after')
a2 = box('after', row(4.5), 'Section 1.4\nrun backwards', 'after')

edge(s7, nqs); edge(s7, tn); edge(s1, dft); edge(s13, pha); edge(s9, ham); edge(s14, ham)
edge(pha, a1, style.ACCENT)
edge(ham, a2, style.ACCENT)
style.save(fig, __file__)
