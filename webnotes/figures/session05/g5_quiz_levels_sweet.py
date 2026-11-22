"""Session 5, Section 5.16, a picture option of the quiz on the levels of an open Kitaev chain of 10 sites: Delta=t and mu=0.

Two levels at zero inside a gap, and 9 at each of +-2t."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g5_kitaev as kc

e = kc.levels_option(__file__, mu=0.0, D=1.0)
assert np.sum(np.abs(e) < 1e-12) == 2 and np.sum(np.abs(np.abs(e) - 2) < 1e-12) == 18
