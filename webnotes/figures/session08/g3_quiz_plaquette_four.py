"""Session 8, Section 8.10, a picture option of the quiz on the flux, a plaquette with the hopping -1 on all four links."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g3_plaquette

_g3_plaquette.draw(__file__, [-1, -1, -1, -1], flux=1)
