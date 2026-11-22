"""Session 5, Section 5.13, a picture option of the quiz on the nodal superconductor: the BdG bands with fwave pairing."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g3_tribands
from _g3_tribands import style

_g3_tribands.option(__file__, style.run_script('session05/g3_triangular_pairing_bands.py'), 2)
