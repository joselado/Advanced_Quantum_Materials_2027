"""Session 4, the index page, where the session sits in the course, built from lecture_notes/WEB_NOTES_CONCEPTS.md.

From before, the Chern number (3.5) with the bulk-boundary correspondence (3.7), the Dirac cone (2.11) and the Haldane model (3.10b).
In this session, the Landau levels as flat bands with C=1 (4.4, 4.9), the Dirac Landau levels (4.10), the Haldane model as the same
phase (4.19), the edge states (4.5), the Laughlin state (4.16) and the anyons (4.18). Where it comes back, the chiral p-wave
superconductor (5.14), the flux quantum h/2e (5.2), the fractional Chern insulators (7.1), the Majoranas (5.15) and the
topological order (10.6). This is a drawing without computed data."""
import os, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, '..'))
sys.path.insert(0, os.path.join(here, '..', 'session03'))
import style, _conceptmap as cm

X = [1.95, 6.0, 10.05]; W3 = 3.6
Xb = [1.2, 3.6, 6.0, 8.4, 10.8]; W5 = 2.3
boxes = {
    'chern': (X[0], 7.75, W3, 'before', 'Chern number and\nedges, 3.5, 3.7'),
    'dirac': (X[1], 7.75, W3, 'before', 'Dirac cone\n2.11'),
    'haldane': (X[2], 7.75, W3, 'before', 'Haldane model\n3.10b'),
    'll': (X[0], 5.6, W3, 'now', 'Landau levels\n$C=1$, 4.4, 4.9'),
    'dll': (X[1], 5.6, W3, 'now', 'Dirac Landau\nlevels, 4.10'),
    'h419': (X[2], 5.6, W3, 'now', 'same phase as\nquantum Hall, 4.19'),
    'edge': (X[0], 3.9, W3, 'now', 'chiral edge states\n4.5'),
    'laughlin': (X[1], 3.9, W3, 'now', 'Laughlin state\n4.16'),
    'anyon': (X[2], 3.9, W3, 'now', 'anyons with\ncharge $e/m$, 4.18'),
    'pwave': (Xb[0], 1.4, W5, 'later', 'chiral\np-wave\nSession 5'),
    'flux': (Xb[1], 1.4, W5, 'later', 'flux\nquantum\nSession 5'),
    'fci': (Xb[2], 1.4, W5, 'later', 'fractional\nChern\nSession 7'),
    'majorana': (Xb[3], 1.4, W5, 'later', 'Majorana\nmodes\nSession 5'),
    'topo': (Xb[4], 1.4, W5, 'later', 'topological\norder\nSession 10'),
}
arrows = [('chern', 'll'), ('dirac', 'dll'), ('haldane', 'h419'), ('ll', 'dll'), ('ll', 'edge'), ('ll', 'laughlin'),
          ('laughlin', 'anyon'),
          ('edge', 'pwave'), ('edge', 'flux'), ('laughlin', 'fci'), ('anyon', 'majorana'), ('anyon', 'topo')]
headers = [(8.65, 'from before', 'before'), (6.5, 'Session 4', 'now'), (0.3, 'where it comes back', 'later')]
fig = cm.draw(boxes, arrows, headers, height=9.0)
style.save(fig, __file__)
