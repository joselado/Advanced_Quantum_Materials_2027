"""Session 2, Section 2.11a, a picture option of the quiz on the bands of graphene: the triangular lattice with one band."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g4_bands

_g4_bands.option_graphene(__file__, 'band_triangular')
