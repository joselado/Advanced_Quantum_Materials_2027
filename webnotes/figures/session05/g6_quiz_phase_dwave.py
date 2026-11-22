"""Session 5, section 5.20, a picture option of the quiz on the winding of the pairing function: the case 'dwave'.

The arrows of Delta(k) on the Fermi pocket of the square lattice at mu=-t, in the plane kx, ky, from _g6_phase."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g6_phase

_g6_phase.option(__file__, 'dwave')
