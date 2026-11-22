"""Session 9, Section 9.4b, a picture option of the quiz on nesting: the Fermi surface of the square lattice at mu=-1.0 t.

The map and its checks are in _g2_fermi.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g2_fermi

_g2_fermi.option(__file__, -1.0)
