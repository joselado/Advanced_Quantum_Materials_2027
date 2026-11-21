"""Session 3, section 3.5, a picture option of the quiz on the Berry curvature, the lattice "haldane" of the pyqula script."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _berrymap

_berrymap.draw(__file__, 'haldane', expect=-1)
