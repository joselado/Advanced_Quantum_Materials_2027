"""Session 6, Section 6.12, a picture option of the quiz on the Dzyaloshinskii-Moriya chain: a row of spins that turns
by 101.3 degrees from site to site, clockwise seen from +z."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g3_spiral

_g3_spiral.option(__file__, 101.3)
