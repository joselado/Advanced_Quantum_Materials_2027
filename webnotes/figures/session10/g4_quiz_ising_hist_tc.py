"""Session 10, Section 10.6a, a picture option of a quiz: the histogram of |m| of single Ising snapshots at k_BT = 2.27 J, at T_c."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g4_isinghist

_g4_isinghist.draw(__file__, 2.27)
