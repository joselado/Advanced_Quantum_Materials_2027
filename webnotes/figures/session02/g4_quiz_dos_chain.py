"""Session 2, Section 2.13, a picture option of the closing quiz on the density of states: the chain."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g4_dos

_g4_dos.option(__file__, 'dos_chain')
