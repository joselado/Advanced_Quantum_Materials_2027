"""Session 5, section 5.10, a picture option of the quiz on the energy along one Fermi surface: the case 'metal'.

The curve is E/Delta_0 on the Fermi surface of the square lattice at mu=-t against the angle around Gamma, from _g2_fsgap."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g2_fsgap

_g2_fsgap.option(__file__, 'metal')
