"""Session 7, Section 7.11, a picture option of the quiz on the entropy of a block: the dimerized chain of free fermions.

On an open chain of 402 sites with the hoppings 1 and 0.6 the entropy is 0.39 at l=2 and stays at about 0.5 from l=6
on, so the curve is flat. The feedback says that this chain is gapped and saturates at about 0.5."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g5_entropycurves as ec
import style

ell, S = ec.dimerized()
print('dimerized', np.round(S, 4))
assert abs(S[0] - 0.39) < 0.005                       # l=2
assert np.all(np.abs(S[ell >= 6] - 0.5) < 0.012)      # flat near 0.5 from l=6 on
assert S.max() < 0.5
ec.option(__file__, ell, S, style.ACCENT)
