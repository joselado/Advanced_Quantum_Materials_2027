"""Session 7, section 7.9, a picture option of the quiz on which network is a number: the diagram 'hpsi', the MPO on
top of the MPS, with 4 free legs that point up."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g4_nets as q

assert q.draw(__file__, 'hpsi') == 4
