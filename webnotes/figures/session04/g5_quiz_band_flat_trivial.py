"""Session 4, section 4.20, a picture option of the quiz on the flat Chern band: real hoppings t2=0.2 and a staggered potential M=1.5, a flat lower band with C=0, width 0.200 and gap 3.000.

Drawn from webnotes/scripts/session04/g5_haldane_t3_bands.py by _g5_bands.option, which asserts the numbers."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g5_bands as gb

d = gb.load(gb.style.run_script('session04/g5_haldane_t3_bands.py'))
gb.option(__file__, d, 2)
