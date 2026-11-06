"""Shared mean-field helpers of the half-filled Hubbard chain, as in mf_chain.py (t=1)."""
import warnings; warnings.filterwarnings("ignore")
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

t = 1.0

def avg(f, D):
    """Average over the reduced zone k in (-pi/2, pi/2) of f(eps_k, D), with eps_k = -2t cos k."""
    return quad(lambda k: f(-2 * t * np.cos(k), D), -np.pi / 2, np.pi / 2, points=[0], limit=200, epsabs=1e-13, epsrel=1e-12)[0] / np.pi

def gap_parameter(U):
    """Delta = U m / 2 from the self-consistency 1 = (U/2) <1/E>."""
    return brentq(lambda D: (U / 2) * avg(lambda e, D: 1 / np.sqrt(e * e + D * D), D) - 1, 1e-9, 5 * U, xtol=1e-14)

def moment(U):
    return 2 * gap_parameter(U) / U
