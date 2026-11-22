"""Session 9, Section 9.10a, a picture option of the quiz on the Aubry-Andre chain: the lowest state at V0 = 3t, localized.

Almost all the weight is on one site, 0.91, and the IPR is 0.83 on rings of 55, 233 and 987 sites, so it does not change
as the ring grows."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g6_aah as q

d = q.option(__file__, 3.0)
ipr = {n: d['ipr'][(n, 3.0)] for n in (55, 233, 987)}
assert all(round(v, 2) == 0.83 for v in ipr.values()) and max(ipr.values()) - min(ipr.values()) < 1e-3, ipr
assert round(float(d['weight'][(233, 3.0)].max()), 2) == 0.91
