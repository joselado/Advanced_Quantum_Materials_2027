"""Session 3, the index page, where the session sits in the course, built from lecture_notes/WEB_NOTES_CONCEPTS.md.

From before, the two-orbital chain (2.13) of Section 2.7, the Bloch Hamiltonian of Section 2.5 and the Dirac cone of Section 2.11.
In this session, the SSH chain and the Zak phase (3.9, 3.9c), linear response (3.2), the Chern number (3.5), the bulk-boundary
correspondence (3.7), the Haldane model (3.10b) and the quantum spin Hall insulator (3.11). Where it comes back, the Kitaev chain
(5.16), the vacancy states (9.8), the invariants without a local order parameter (10.6), the Landau levels with C=1 (4.4) and the
Chern number of magnon bands (6.16). This is a drawing without computed data."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import style, _conceptmap as cm

X = [1.95, 6.0, 10.05]; W3 = 3.6
Xb = [1.2, 3.6, 6.0, 8.4, 10.8]; W5 = 2.3
boxes = {
    'chain': (X[0], 7.75, W3, 'before', 'two-orbital chain\n2.7'),
    'bloch': (X[1], 7.75, W3, 'before', 'Bloch Hamiltonian\n2.5'),
    'dirac': (X[2], 7.75, W3, 'before', 'Dirac cone\n2.11'),
    'ssh': (X[0], 5.6, W3, 'now', 'SSH chain and\nZak phase, 3.9'),
    'kubo': (X[1], 5.6, W3, 'now', 'linear response\n3.2'),
    'haldane': (X[2], 5.6, W3, 'now', 'Haldane model\n3.10b'),
    'bb': (X[0], 3.9, W3, 'now', 'bulk-boundary\n3.7'),
    'chern': (X[1], 3.9, W3, 'now', 'Chern number\n3.5'),
    'qsh': (X[2], 3.9, W3, 'now', 'quantum spin Hall\n3.11'),
    'kitaev': (Xb[0], 1.4, W5, 'later', 'Kitaev\nchain\nSession 5'),
    'vac': (Xb[1], 1.4, W5, 'later', 'vacancy\nstates\nSession 9'),
    'topo': (Xb[2], 1.4, W5, 'later', 'topological\norder\nSession 10'),
    'landau': (Xb[3], 1.4, W5, 'later', 'Landau\nlevels\nSession 4'),
    'magnon': (Xb[4], 1.4, W5, 'later', 'magnon\nbands\nSession 6'),
}
arrows = [('chain', 'ssh'), ('bloch', 'kubo'), ('dirac', 'haldane'), ('ssh', 'bb'), ('kubo', 'chern'), ('chern', 'bb'),
          ('haldane', 'qsh'), ('haldane', 'chern'),
          ('bb', 'kitaev'), ('bb', 'vac'), ('chern', 'topo'), ('chern', 'landau'), ('chern', 'magnon')]
headers = [(8.65, 'from before', 'before'), (6.5, 'Session 3', 'now'), (0.3, 'where it comes back', 'later')]
fig = cm.draw(boxes, arrows, headers, height=9.0)
style.save(fig, __file__)
