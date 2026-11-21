"""Session 2, Section 2.11b, a picture option of the quiz on the flat bands: the kagome lattice with tij=[1.], the sign of the notebook."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g4_bands

_g4_bands.option_flat(__file__, 'bands_kagome_plus')
