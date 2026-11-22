"""Session 6, Section 6.15, a picture option of the quiz on the magnon of the antiferromagnetic chain near k = 0: the antiferromagnetic band (6.9) of the chain, 2JS|sin k| with S = 1/2."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g4_dispersions

_g4_dispersions.option(__file__, 'afm')
