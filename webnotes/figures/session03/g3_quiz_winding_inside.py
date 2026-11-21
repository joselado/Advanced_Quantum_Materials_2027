"""Session 3, section 3.9c, a picture option of the quiz on the winding of d(k): t=0.25 and t'=0.75, the origin inside."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g3_winding

_g3_winding.option(__file__, 0.25, 0.75, winding=1, lowest=2e-10)
