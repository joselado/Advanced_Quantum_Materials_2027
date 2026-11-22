"""Session 9, Section 9.8, a picture option of the quiz on a vacancy: the Haldane model with t2 = 0.15t and M = 1.0t, C = 0.

The mass is larger than 3 sqrt(3) t2 = 0.78t, the gap is 0.44t, and the vacancy leaves no level inside it. The Chern
numbers of the three models are asserted in webnotes/checks/session09/g5_08_vacancies.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import _g5_vacancy as gv

d = gv.option(__file__, 'both')
gap, e = d['gaps']['both'], d['levels']['both']
assert abs(gap - 2 * (1.0 - 3 * np.sqrt(3) * 0.15)) < 1e-4 and abs(round(gap, 2) - 0.44) < 1e-12
assert not np.any(np.abs(e) < gap / 2 - 1e-3)
