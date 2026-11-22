"""Session 9, Section 9.10a, a picture option of the quiz on the Aubry-Andre chain: the lowest state at V0 = 2t, critical.

The IPR is 0.23, 0.099 and 0.062 on rings of 55, 233 and 987 sites. It falls as the ring grows, but slower than 1/N,
since from 233 to 987 sites it falls by 0.62, while 1/N falls by 0.24."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g6_aah as q

d = q.option(__file__, 2.0)
ipr = {n: d['ipr'][(n, 2.0)] for n in (55, 233, 987)}
assert round(ipr[55], 2) == 0.23 and round(ipr[233], 3) == 0.099 and round(ipr[987], 3) == 0.062, ipr
assert ipr[55] > ipr[233] > ipr[987]
assert round(ipr[987] / ipr[233], 2) == 0.62 and round(233 / 987, 2) == 0.24, ipr[987] / ipr[233]
