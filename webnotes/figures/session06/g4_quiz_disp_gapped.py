"""Session 6, Section 6.15, a picture option of the quiz on the magnon of the antiferromagnetic chain near k = 0: the ferromagnetic parabola lifted by a gap of 0.2."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g4_dispersions

_g4_dispersions.option(__file__, 'gapped')
