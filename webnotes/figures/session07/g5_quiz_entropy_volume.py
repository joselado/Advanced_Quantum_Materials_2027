"""Session 7, Section 7.11, a picture option of the quiz on the entropy of a block: the volume law S = l log 2.

The curve starts at 2 log 2 = 1.39 at l=2 and leaves the frame S=2.5 at l=2.5/log 2=3.6. No pyqula, it is the largest
entropy of l spins one-half."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g5_entropycurves as ec
import style

ell, S = ec.volume()
print('volume', S[0], ell[-1])
assert abs(S[0] - 1.386) < 1e-3
assert abs(ell[-1] - 3.6) < 0.01                      # leaves the frame at l = 3.6
ec.option(__file__, ell, S, style.ACCENT)
