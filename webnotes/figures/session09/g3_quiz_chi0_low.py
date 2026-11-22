"""Session 9, Section 9.5b, a picture option of the quiz on (9.8): chi_0(q,0) of the square lattice at T=0.1t, mu = -3t, a nearly flat curve."""
import os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g3_chi0path

_g3_chi0path.option(__file__, 'low')
