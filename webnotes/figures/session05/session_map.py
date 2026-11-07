"""Session 5, where the session sits in the course, a small concept map.

Built from lecture_notes/WEB_NOTES_CONCEPTS.md and from the index page of the session. The left column holds what
the session takes from before (mean field and the pairing order of Sections 1.12 and 1.15, the Chern number and the
SSH model of Session 3, the fractionalization of Section 4.18), the middle column the concepts that the session
builds, and the right column the sessions where they come back, which are the ones of the box of the index page
(Sections 6.6 and 6.15, Section 8.6, Sections 9.7 and 9.8). The look is the one of figures/session01/session_map.py.
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

COL = {'before': (0.05, 2.9), 'here': (3.8, 3.6), 'after': (8.35, 4.1)}
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


for col, txt in (('before', 'before'), ('here', 'Session 5'), ('after', 'comes back in')):
    x0, w = COL[col]
    ax.text(x0 + w / 2, HEAD, txt, ha='center', va='center', fontsize=FS + 0.5,
            color=style.ACCENT if col == 'here' else style.INK)

yh = [H - 1.45 - 1.45 * i for i in range(5)]
pair = box('here', yh[0], 'pairing from\nattraction', 'here')
bdg = box('here', yh[1], 'Nambu spinor\nand BdG', 'here')
sym = box('here', yh[2], r'$s$-, $p$- and $d$-wave', 'here')
chern = box('here', yh[3], 'BdG Chern\nnumber', 'here')
maj = box('here', yh[4], 'Kitaev chain\nand Majoranas', 'here')

b1 = box('before', yh[0] - 0.2, 'Session 1\nmean field,\n' + r'$\Delta=\langle cc\rangle$', 'before', h=1.45)
b3 = box('before', yh[3] + 0.4, 'Session 3\nChern number,\nSSH model', 'before', h=1.45)
b4 = box('before', yh[4] - 0.25, 'Session 4\nsplit charge', 'before')

ya = [yh[0] + 0.05, yh[1] + 0.1, yh[2] - 0.1, yh[3] + 0.15]
s6m = box('after', ya[0], 'Session 6\nrepulsive Hubbard', 'after')
s6b = box('after', ya[1], 'Session 6\nAFM magnons', 'after')
s8 = box('after', ya[2], 'Session 8\nspinons in Nambu', 'after')
s9 = box('after', ya[3], 'Session 9\nimpurity states', 'after', h=0.96)

edge(b1, pair); edge(b1, bdg)
edge(b3, chern); edge(b3, maj)
edge(b4, maj)
edge(pair, s6m, style.ACCENT)
edge(bdg, s6b, style.ACCENT)
edge(bdg, s8, style.ACCENT)
edge(sym, s9, style.ACCENT)
edge(chern, s9, style.ACCENT)
style.save(fig, __file__)
