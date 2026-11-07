"""Session 6, where the session sits in the course, a small concept map.

Built from lecture_notes/WEB_NOTES_CONCEPTS.md and from the index page of the session. The left column holds what
the session takes from before (the Hubbard model (1.7) and its mean field of Section 1.14, the BdG Hamiltonian of
Section 5.8, the Chern number and the Haldane model of Session 3), the middle column the concepts that the session
builds, and the right column the sessions where they come back, which are the ones of the box of the index page
(Section 7.10, Sections 8.1 and 8.7, Section 9.5b). The look is the one of figures/session01/session_map.py.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import style

FS = 11.5
style.plt.rcParams['font.size'] = FS          # labels of the arrows too, for a phone
W, H = 12.5, 8.6                                    # in cm, the axes are in cm too
fig = plt.figure(figsize=(W * style.CM, H * style.CM))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')

COL = {'before': (0.05, 3.05), 'here': (3.7, 3.95), 'after': (8.45, 4.0)}
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


for col, txt in (('before', 'before'), ('here', 'Session 6'), ('after', 'comes back in')):
    x0, w = COL[col]
    ax.text(x0 + w / 2, HEAD, txt, ha='center', va='center', fontsize=FS + 0.5,
            color=style.ACCENT if col == 'here' else style.INK)

yh = [H - 1.45 - 1.45 * i for i in range(5)]
mf = box('here', yh[0], 'mean-field\nFM and AFM', 'here')
st = box('here', yh[1], 'Stoner criterion', 'here')
he = box('here', yh[2], 'Heisenberg model,\nsuperexchange', 'here')
mg = box('here', yh[3], 'magnons from\nHolstein-Primakoff', 'here')
tm = box('here', yh[4], 'topological\nmagnons', 'here')

b1 = box('before', yh[0] - 0.35, 'Session 1\nHubbard model\nand mean field', 'before', h=1.45)
b5 = box('before', yh[3] - 0.1, 'Session 5\nBogoliubov\ntransformation', 'before', h=1.45)
b3 = box('before', yh[4] - 0.35, 'Session 3\nChern number', 'before')

s9 = box('after', yh[1], 'Session 9\nspin response', 'after')
s7 = box('after', yh[2], 'Session 7\nDMRG', 'after')
s8 = box('after', yh[3], 'Session 8\nspinons, where\nmagnons fail', 'after', h=1.25)

edge(b1, mf); edge(b1, st); edge(b1, he)
edge(b5, mg)
edge(b3, tm)
edge(st, s9, style.ACCENT)
edge(he, s7, style.ACCENT)
edge(mg, s8, style.ACCENT)
style.save(fig, __file__)
