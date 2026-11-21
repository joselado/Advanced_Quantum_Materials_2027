"""Session 2, Section 2.3, a picture option of the quiz on the eigenstates of the rotation of a ring of four sites:
the arrows turn by 90 degrees and have two lengths."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g1_ring

_g1_ring.option(__file__, 'lengths')
