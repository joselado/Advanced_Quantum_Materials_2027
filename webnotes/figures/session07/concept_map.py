"""Session 7, where the session sits, what it takes from earlier sessions and what it gives to later ones
(a concept map built from lecture_notes/WEB_NOTES_CONCEPTS.md and the comesback boxes of the session)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _conceptmap

before = [
    ['mean field', 'Section 1.12'],
    ['fractional Chern', 'insulators, 4.20'],
    ['frustration', 'Sections 6.10, 6.12'],
    ['Heisenberg model', 'Section 6.8'],
]
now = [
    ['no order parameter', 'Section 7.1'],
    ['Jordan-Wigner', 'Section 7.2b'],
    [r'$2^L$ coefficients', 'Section 7.3'],
    ['entropy, area law', 'Sections 7.5 to 7.7'],
    ['MPS, DMRG,', 'MERA, PEPS', 'Sections 7.4 to 7.11'],
]
after = [
    ['Abrikosov fermions', 'Section 8.8'],
    ['RVB state', 'Section 8.6'],
    ['neural network', 'states, 10.3'],
    ['valence bond solid', 'Section 8.5'],
    ['networks that', 'classify, 10.4'],
]
edges = [((0, 0), (1, 0)), ((0, 1), (1, 0)), ((0, 2), (1, 0)), ((0, 3), (1, 2)),
         ((1, 1), (2, 0)), ((1, 2), (2, 1)), ((1, 2), (2, 2)), ((1, 3), (2, 3)), ((1, 4), (2, 4))]
_conceptmap.draw(__file__, [before, now, after], edges, ['from before', 'Session 7', 'where it comes back'])
