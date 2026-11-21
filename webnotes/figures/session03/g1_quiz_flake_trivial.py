"""Session 3, section 3.1, a picture option of the quiz on the bulk and the edge: the flake with the staggered potential (key ldos_staggered)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g1_flake

_g1_flake.draw(__file__, 'ldos_staggered')
