"""Session 1, Section 1.15, a picture option of the quiz on the gauge transformation (1.10) with phi = pi/4: the
pairing amplitude turned by pi/2, the right answer. The drawing and the asserts are in _g4_gauge.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g4_gauge

_g4_gauge.option(__file__, np.pi / 2)
