"""Session 1, Section 1.13, a picture option of the quiz on the mean-field charges of the chain (1.6): the charges
at V = 0.5t, where the imbalance is 0.03. The data and the asserts are in _g4_cdw.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g4_cdw

_g4_cdw.option(__file__, 0.5)
