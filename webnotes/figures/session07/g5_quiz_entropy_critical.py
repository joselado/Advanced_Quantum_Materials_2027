"""Session 7, Section 7.11, a picture option of the quiz on the entropy of a block: the critical chain of free fermions.

On an open chain of 402 sites with hopping 1 the entropy rises on a straight line of the logarithmic axis, with the slope
0.33, which is c/3 with c=1, from 0.94 at l=2 to about 2.2 at l=100. The feedback quotes the slope and the 2.2."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g5_entropycurves as ec
import style

ell, S = ec.critical()
slope, const = np.polyfit(np.log(ell), S, 1)
print('critical', np.round(S, 4), 'slope', round(slope, 4), 'const', round(const, 4))
assert abs(S[0] - 0.94) < 0.01                        # l=2
assert abs(S[-1] - 2.2) < 0.05                        # l=100, about 2.2
assert abs(slope - 1 / 3) < 0.01                      # c/3 with c=1
assert np.all(np.abs(S - (slope * np.log(ell) + const)) < 0.03)   # a straight line on the logarithmic axis
assert S.max() < ec.SMAX
ec.option(__file__, ell, S, style.ACCENT)
