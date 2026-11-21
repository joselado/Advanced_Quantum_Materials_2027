"""Session 3, section 3.9c, a picture option of the quiz on the winding of d(k): t=1.5 and t'=1, the origin outside."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g3_winding

_g3_winding.option(__file__, 1.5, 1.0, winding=0, lowest=0.53)
