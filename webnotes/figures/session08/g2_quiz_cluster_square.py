"""Session 8, Section 8.4, a picture option of the quiz on which cluster of antiferromagnetic Ising spins can satisfy every bond: the square."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g2_cluster

_g2_cluster.option(__file__, 'square')
