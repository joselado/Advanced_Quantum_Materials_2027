"""Session 5, section 5.14, a picture option of the quiz on the ribbons: the ribbon with chiral p-wave pairing, with two branches at each edge inside the gap, C = -2.
The data come from webnotes/scripts/session05/g4_pwave_ribbon.py, and _g4_ribbon.check asserts what the feedback states."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g4_ribbon

_g4_ribbon.option(__file__, _g4_ribbon.load(_g4_ribbon.style.run_script('session05/g4_pwave_ribbon.py')), 1)
