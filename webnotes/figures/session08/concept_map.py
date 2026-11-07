"""Session 8, where the session sits, what it takes from earlier sessions and what it gives to later ones
(a concept map built from lecture_notes/WEB_NOTES_CONCEPTS.md and the comesback boxes of the session)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _conceptmap

before = [
    ['Heisenberg model', 'Section 6.8'],
    ['frustration', 'Section 6.10'],
    ['singlet, entropy', 'Sections 7.3, 7.5'],
    ['Nambu spinor, BdG', 'Section 5.8'],
    ['Holstein-Primakoff', 'Section 6.14'],
    ['mean field', 'Sections 1.12, 1.14'],
]
now = [
    ['singlet, frustration', 'Sections 8.3, 8.4'],
    ['RVB state', 'Section 8.6'],
    ['spinons', 'Sections 8.8, 8.9'],
    ['gauge field, visons', 'Section 8.10'],
    ['Kondo lattice', 'Sections 8.11 to 8.13'],
]
after = [
    ['spinons screen an', 'impurity, 9.9'],
    ['Ising gauge theory', 'Section 10.6b'],
    ['topological order', 'Section 10.6'],
    ['Kondo temperature', 'Section 9.3'],
]
edges = [((0, 0), (1, 0)), ((0, 1), (1, 0)), ((0, 2), (1, 1)), ((0, 3), (1, 1)), ((0, 4), (1, 2)),
         ((0, 5), (1, 2)), ((0, 5), (1, 4)),
         ((1, 2), (2, 0)), ((1, 3), (2, 1)), ((1, 3), (2, 2)), ((1, 4), (2, 3))]
_conceptmap.draw(__file__, [before, now, after], edges, ['from before', 'Session 8', 'where it comes back'])
