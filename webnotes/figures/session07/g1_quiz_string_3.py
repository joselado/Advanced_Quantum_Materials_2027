"""Session 7, picture quiz of 7.2b, a chain with 3 fermions on the sites 1 to 5, to the left of the empty site 6."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g1_stringchain
assert _g1_stringchain.draw(__file__, (2, 3, 5)) == 3          # not a chain of Figure 7.1, which has 1, 4 and 1, 3, 4
