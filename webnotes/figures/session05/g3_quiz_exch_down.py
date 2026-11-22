"""Session 5, Section 5.12, a picture option of the quiz on the exchange field: the chain with (mu, h) = (-1.5, -1.2)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g3_spinbands
from _g3_spinbands import style

_g3_spinbands.option(__file__, style.run_script('session05/g3_exchange_chain_bands.py'), (-1.5, -1.2))
