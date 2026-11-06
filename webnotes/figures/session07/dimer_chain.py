"""Session 7, quiz of 7.6, the chain of dimers of (7.8) with a block of sites, the singlets that the block cuts are red."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _dimerchain
_dimerchain.draw(__file__, None)
