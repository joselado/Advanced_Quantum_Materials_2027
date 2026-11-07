"""Helper of the concept maps of the index pages, three columns of boxes (from before, this session, where it
comes back) joined by arrows. The same file is in session07/ and session08/, so that the two maps look the same.
Coordinates are in cm, so that a label of a given font size has the same size in every map."""
import style
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

COLS = (                       # edge color, fill, text color of the three columns
    (style.MUTED, '#f2f2f2', style.INK),
    (style.ACCENT, '#e6eef6', style.ACCENT),
    (style.BROKEN, '#f6e7e4', style.BROKEN),
)
FS = 11.0                      # font size of the boxes, about 10.7 px on a phone of 390 px, as the map of Session 1
LINE = 0.46                    # line height in cm


def draw(script, columns, edges, titles, width_cm=13.0, box_w=3.75, gap=0.32, xs=(1.95, 6.5, 11.05)):
    """columns: three lists of nodes, each node a list of text lines. edges: pairs ((col, row), (col, row)).
    Boxes of a column are stacked from the top with the given gap, and every column is centred vertically."""
    heights = [[len(n) * LINE + 0.26 for n in col] for col in columns]
    totals = [sum(h) + gap * (len(h) - 1) for h in heights]
    H = max(totals) + 0.9
    fig, ax = style.plt.subplots(figsize=(width_cm * style.CM, (H + 0.12) * style.CM))
    ax.set_xlim(0, width_cm); ax.set_ylim(-0.12, H); ax.set_aspect('equal'); ax.axis('off')
    fig.subplots_adjust(0, 0, 1, 1)
    top = H - 0.9
    boxes = {}
    for c, (col, hs) in enumerate(zip(columns, heights)):
        ec, fc, tc = COLS[c]
        y = top - (max(totals) - totals[c]) / 2
        for r, (node, h) in enumerate(zip(col, hs)):
            x0 = xs[c] - box_w / 2
            ax.add_patch(FancyBboxPatch((x0, y - h), box_w, h, boxstyle='round,pad=0,rounding_size=0.14',
                                        facecolor=fc, edgecolor=ec, lw=0.9, zorder=2))
            for k, line in enumerate(node):
                style.label(ax, xs[c], y - 0.13 - (k + 0.5) * LINE, line, fontsize=FS,
                            color=style.INK if k == len(node) - 1 else tc, zorder=3)
            boxes[(c, r)] = (x0, y - h, x0 + box_w, y)
            y -= h + gap
    for c, t in enumerate(titles):
        style.label(ax, xs[c], H - 0.38, t, fontsize=FS, color=COLS[c][0])
    def spread(key, box, ends):
        """The k-th of n arrows that leave or enter a box sits at its own height, so the heads do not overlap."""
        k, n = ends.index(key), len(ends)
        y0, y1 = box[1], box[3]
        return (y0 + y1) / 2 if n == 1 else y1 - (y1 - y0) * (0.28 + 0.44 * k / (n - 1))
    for a, b in edges:
        outs = [e for e in edges if e[0] == a]
        ins = [e for e in edges if e[1] == b]
        ya = spread((a, b), boxes[a], outs)
        yb = spread((a, b), boxes[b], ins)
        ax.add_patch(FancyArrowPatch((boxes[a][2], ya), (boxes[b][0], yb), arrowstyle='-|>',
                                     mutation_scale=8, color=style.INK, lw=0.8, shrinkA=2, shrinkB=2, zorder=1))
    style.save(fig, script)
