"""Session 5, Section 5.16, a picture option of the quiz on the levels of an open Kitaev chain of 10 sites: Delta=t and mu=2.5t, trivial.

A gap and no level inside it, the lowest level at 0.71t."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g5_kitaev as kc

e = kc.levels_option(__file__, mu=2.5, D=1.0)
assert abs(np.abs(e).min() - 0.7068) < 1e-4
# the alt text, levels from about minus 4.5 to plus 4.5, from both sides (they end at -4.451 and 4.451)
assert abs(e.max() - 4.5) < 0.06 and abs(e.min() + 4.5) < 0.06, (e.min(), e.max())
