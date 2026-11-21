"""Session 2, Section 2.9, a picture option of the quiz on nesting, the Fermi surface of the square lattice at the
energy ENERGIES['low'] of _g3_fermi.py, from the pyqula script webnotes/scripts/session02/g3_fermi_surface.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g3_fermi

_g3_fermi.draw(__file__, 'low')
