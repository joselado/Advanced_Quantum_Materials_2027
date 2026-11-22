"""Session 5, Section 5.17, a picture option of the quiz on the lowest state of an open Kitaev chain of 40 sites with Delta=0.5t: mu=-1.5t, topological.

The weight is again on the first and the last few sites, and the level is below 1e-9 t."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g5_kitaev as kc

w, E = kc.profile_option(__file__, mu=-1.5)
assert E < 1e-9 and w[:4].sum() + w[-4:].sum() > 0.98
