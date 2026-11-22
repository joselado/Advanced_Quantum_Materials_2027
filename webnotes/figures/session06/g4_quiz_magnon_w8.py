"""Session 6, Section 6.14, a picture option of the quiz on the one-magnon band of a ferromagnetic ring: the band 2|J|S (1 - cos k) for S = 2, which reaches 8."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g4_onemagnon

_g4_onemagnon.option(__file__, 'w8')
