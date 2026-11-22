"""Session 5, Section 5.17, a picture option of the quiz on the lowest state of an open Kitaev chain of 40 sites with Delta=0.5t: mu=3t, trivial.

The weight is spread over the middle, with 2% of it on the four sites at each end, and the level is at 1.01t."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g5_kitaev as kc

w, E = kc.profile_option(__file__, mu=3.0)
assert abs(E - 1.008) < 1e-3 and w[12:28].sum() > 0.6
# the 2% of the feedback, the weight on the eight sites at the two ends, from both sides (it is 0.0202)
assert abs(w[:4].sum() + w[-4:].sum() - 0.02) < 0.0025, w[:4].sum() + w[-4:].sum()
