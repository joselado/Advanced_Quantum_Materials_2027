"""Session 8, Section 8.13, a picture option of the quiz on the Kondo insulator: the bands of the chain with
no hybridization, so the conduction band crosses the flat f level at the Fermi level."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g4_kondo

_g4_kondo.option(__file__, gamma=0., count=1)
