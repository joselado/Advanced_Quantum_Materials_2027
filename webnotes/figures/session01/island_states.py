"""Session 1, the lowest levels of a hexagonal honeycomb island, H = -t sum c_i^+ c_j over first neighbors.

Each panel is the density of one level, averaged over its degenerate states, which is what a scanning tunneling
microscope maps at that energy. The area of a disc is proportional to the density on that site. The calculation is the
pyqula script scripts/session01/g2_honeycomb_island.py, and the drawing and the checks are in _g2_island.py.
"""
import os, sys
sys.dont_write_bytecode = True  # no __pycache__ next to the figures
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import style
import _g2_island

_g2_island.main(__file__, style.run_script('session01/g2_honeycomb_island.py'))
