"""Session 10, Section 10.6b, a picture option of a quiz: the bonds of 3 x 3 plaquettes of the Ising gauge theory, a gauge copy of the uniform state."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g4_igtlattice

_g4_igtlattice.draw(__file__, 'ground')
