"""Session 5, Section 5.5, a picture option of the quiz on the attractive chain: the mean-field bands at U=-2."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g1_gapbands
from _g1_gapbands import style

_g1_gapbands.option(__file__, style.run_script('session05/g1_meanfield_swave_chain.py'), -2.0)
