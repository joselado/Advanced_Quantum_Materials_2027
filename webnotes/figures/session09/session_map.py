"""Session 9, where the session sits in the course, a small concept map.

Built from lecture_notes/WEB_NOTES_CONCEPTS.md, in the shape of webnotes/figures/session01/session_map.py. The left
column holds what the session takes from earlier sessions (Density of states, Linear response, Hubbard model and
Mean field, Nambu spinor and BdG with Majorana modes, Edge states and bulk-boundary correspondence with the Chern
number, Stoner criterion, Spinons and Kondo physics), the middle column what it builds, and the right column the
pages of Session 10 where it comes back (10.6b, 10.7).
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import style

FS = 12
W, H = 12.7, 9.5                                   # in cm, the axes are in cm too
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


for col, txt in (('before', 'before'), ('here', 'Session 9'), ('after', 'comes back in')):
    x0, w = COL[col]
    ax.text(x0 + w / 2, HEAD, txt, ha='center', va='center', fontsize=FS + 0.5,
            color=style.ACCENT if col == 'here' else style.INK)

yb = [H - 1.35 - 1.42 * i for i in range(7)]
s2 = box('before', yb[0], 'Session 2\nFermi sea, DOS', 'before')
s3a = box('before', yb[1], 'Session 3\nlinear response', 'before')
s16 = box('before', yb[2], 'Sessions 1, 6\nHubbard, Stoner', 'before')
s5 = box('before', yb[3], 'Session 5\nBdG, p-wave', 'before')
s3b = box('before', yb[4], 'Session 3\nbulk-boundary', 'before')
s8 = box('before', yb[5], 'Session 8\nspinons', 'before')

yh = [H - 2.06 - 1.95 * i for i in range(4)]
lind = box('here', yh[0], 'Lindhard function\nand nesting', 'here')
rpa = box('here', yh[1], 'RPA, plasmon,\nStoner instability', 'here')
imp = box('here', yh[2], 'one impurity\nas a diagnostic', 'here')
loc = box('here', yh[3], 'Anderson\nlocalization', 'here')

a1 = box('after', yh[0], 'Section 10.7\nlearning $H$', 'after')
a2 = box('after', yh[2], 'Section 10.6b\nno local order', 'after')
a3 = box('after', yh[3], 'Section 10.7\nhidden disorder', 'after')

edge(s2, lind); edge(s3a, lind)
edge(s16, rpa)
edge(s5, imp); edge(s3b, imp); edge(s8, imp)
edge(lind, a1, style.ACCENT)
edge(imp, a2, style.ACCENT)
edge(loc, a3, style.ACCENT)
style.save(fig, __file__)
