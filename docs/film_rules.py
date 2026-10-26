"""Draw film_rules.png, the chart of which iteration of the film rules each film follows. Run from docs/."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
V = [("v1  10-15", "First films: mind palace, voice as narrator,\ncaptions in a game dialogue box"),
     ("v2  10-17", "Photographic look C, physics in the landscape,\nlegible text, plots name their axes"),
     ("v3  10-19", "Pedagogical plan (SETS.md) before render,\nvoice slips made true by the picture"),
     ("v4  10-20", "Set kit and palace engine, formulas on\nblackboards, every card framed"),
     ("v5  10-21", "Partial overlap of old formulas allowed,\ncaptions and preflight made for builders"),
     ("v6  10-22 am", "Frames per world, majestic themed gates,\nphotoreal worlds, layout screen checks"),
     ("v7  10-22 noon", "Essence dialogue, distant mist, photoreal\nhorizon, 2D winding world with hills"),
     ("v8  10-23", "Uniform sound matched to session 6,\nrecording pipeline with per-film options"),
     ("v9  10-25", "Overture of the session's schematics, silent\npre-roll, index check, floating formulas")]
done = {3: 0, 4: 0, 6: 2, 7: 8, 2: 8, 1: 6, 10: 6, 8: 7, 9: 7, 5: 7}   # session -> version index of its latest full render
prep = {}                                            # being made now, target version
sound = {1, 2, 3, 4, 6, 7, 10}                             # finished films remuxed with the uniform sound of v8
SOUND = 7
ink, muted, grid, fill, surf = '#1f2328', '#6b7280', '#d8dce2', '#2a6fdb', '#ffffff'
fig, ax = plt.subplots(figsize=(9, 5.1), dpi=150); fig.patch.set_facecolor(surf)
nr, nc = len(V), 10
for r in range(nr):
    for c in range(nc):
        ax.add_patch(FancyBboxPatch((c + 0.06, r + 0.08), 0.88, 0.84, boxstyle='round,pad=0,rounding_size=0.08',
                                    fc='#f4f5f7', ec='none'))
for s, r in done.items():
    ax.add_patch(FancyBboxPatch((s - 1 + 0.06, r + 0.08), 0.88, 0.84, boxstyle='round,pad=0,rounding_size=0.08', fc=fill, ec='none'))
    ax.text(s - 0.5, r + 0.5, 'render', ha='center', va='center', color='white', fontsize=8, weight='bold')
for s in sound - set(prep):
    ax.add_patch(FancyBboxPatch((s - 1 + 0.1, SOUND + 0.12), 0.8, 0.76, boxstyle='round,pad=0,rounding_size=0.08',
                                fc='#dbe7fb', ec='none'))
    ax.text(s - 0.5, SOUND + 0.5, 'sound', ha='center', va='center', color=fill, fontsize=8, weight='bold')
for s, r in prep.items():
    ax.add_patch(FancyBboxPatch((s - 1 + 0.1, r + 0.12), 0.8, 0.76, boxstyle='round,pad=0,rounding_size=0.08', fc='none',
                                ec=fill, lw=2, ls=(0, (3, 2))))
    ax.text(s - 0.5, r + 0.5, 'next', ha='center', va='center', color=fill, fontsize=8, weight='bold')
ax.set_xlim(-1.1, nc); ax.axis('off')
for c in range(nc):
    ax.text(c + 0.5, -0.35, f'S{c + 1}', ha='center', va='center', color=ink, fontsize=11, weight='bold')
for r, (v, d) in enumerate(V):
    ax.text(-1.0, r + 0.5, v.split()[0], ha='left', va='center', color=ink, fontsize=11, weight='bold')
ax.text(-1.0, -0.95, 'Iteration of the film rules in the latest render', ha='left', va='center', color=ink,
        fontsize=13, weight='bold')
ax.text(-1.0, nr + 0.45, 'Each iteration includes the ones above it. Sound: the finished film was remuxed with the '
        'uniform track, with no new render.', ha='left', va='center', color=muted, fontsize=8)
ax.set_ylim(nr + 0.7, -1.2)
fig.savefig('film_rules.png', bbox_inches='tight', facecolor=surf)
