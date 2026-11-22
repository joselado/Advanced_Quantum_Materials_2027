"""Session 8, Section 8.9, a picture option of the quiz on Dirac spinons, the band structure "piflux" of the pyqula script."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g3_bands

_g3_bands.option(__file__, 'piflux')
