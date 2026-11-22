"""Session 4, section 4.5, a picture option of the quiz on the Hall conductance of a ribbon: the chemical potential
mu = 2 hbar omega_c, in the gap above the level number 2, so 2 crossing(s) at each edge."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g2_qhribbon

_g2_qhribbon.option(__file__, mu=2.0, expect=2)
