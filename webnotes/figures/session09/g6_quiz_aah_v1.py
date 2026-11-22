"""Session 9, Section 9.10a, a picture option of the quiz on the Aubry-Andre chain: the lowest state at V0 = t, extended.

The weight is spread over the whole ring. N times the IPR is 1.20 on rings of 55, 233 and 987 sites, so the IPR falls
as 1/N, from 0.0052 on 233 sites to 0.0012 on 987 sites."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g6_aah as q

d = q.option(__file__, 1.0)
ipr = {n: d['ipr'][(n, 1.0)] for n in (55, 233, 987)}
assert all(abs(n * ipr[n] - 1.20) < 0.01 for n in ipr), ipr
assert round(ipr[233], 4) == 0.0052 and round(ipr[987], 4) == 0.0012, ipr
assert d['weight'][(233, 1.0)].min() > 1e-4                 # no site of the ring is empty
