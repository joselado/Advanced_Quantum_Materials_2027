"""Session 5, Section 5.16, a picture option of the quiz on the levels of an open Kitaev chain of 10 sites: Delta=0 and mu=0, a metal.

The levels are +-2t cos(pi j/11), j=1..10, from -1.92t to 1.92t, and the closest to zero is 0.28t, with no gap around it."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g5_kitaev as kc

e = kc.levels_option(__file__, mu=0.0, D=0.0)
j = np.arange(1, 11)
assert np.allclose(np.sort(e), np.sort(np.r_[2 * np.cos(np.pi * j / 11), -2 * np.cos(np.pi * j / 11)]), atol=1e-12)
assert abs(np.abs(e).min() - 0.2846) < 1e-4 and abs(e.max() - 1.919) < 1e-3
