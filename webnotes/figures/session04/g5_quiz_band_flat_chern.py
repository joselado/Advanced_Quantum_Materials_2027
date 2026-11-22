"""Session 4, section 4.20, a picture option of the quiz on the flat Chern band: t2=0.3 with the phase 0.4 pi and t3=-0.2, a flat lower band with C=1, width 0.212 and gap 2.965.

Drawn from webnotes/scripts/session04/g5_haldane_t3_bands.py by _g5_bands.option, which asserts the numbers."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g5_bands as gb

d = gb.load(gb.style.run_script('session04/g5_haldane_t3_bands.py'))
gb.option(__file__, d, 1)
