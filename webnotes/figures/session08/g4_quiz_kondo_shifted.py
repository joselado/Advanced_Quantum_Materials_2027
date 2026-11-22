"""Session 8, Section 8.13, a picture option of the quiz on the Kondo insulator: the bands of the chain with
the same hybridization with 0.6 particles per momentum and spin, so the Fermi level cuts the lower band."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g4_kondo

_g4_kondo.option(__file__, gamma=0.6, count=0.6)
