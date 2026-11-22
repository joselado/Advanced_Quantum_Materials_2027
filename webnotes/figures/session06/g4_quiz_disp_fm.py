"""Session 6, Section 6.15, a picture option of the quiz on the magnon of the antiferromagnetic chain near k = 0: the ferromagnetic band (6.8) of the chain, 2|J|S (1 - cos k) with S = 1/2."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g4_dispersions

_g4_dispersions.option(__file__, 'fm')
