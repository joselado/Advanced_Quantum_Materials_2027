"""Session 10, Section 10.7, a picture option of the quiz on the training set of Hamiltonian learning: the predicted
t2 against the true one for the 200 test rings of the seed 3, from a network that gives 0.2 for every input."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _g5_hlquiz

_g5_hlquiz.option(__file__, 'flat')
