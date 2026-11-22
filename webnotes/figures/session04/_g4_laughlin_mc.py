"""Session 4, Sections 4.15 to 4.17, the shared code of the density pictures of the lowest Landau level.

Lengths are in units of l_B. orbital_density(m, r) is |psi_m|^2 of (4.10), normalized, and filled_filling(N, r) is the
density of the filled level (4.11) of N electrons times 2 pi l_B^2, which reads as a local filling factor. metropolis()
samples |Psi|^2 of the Laughlin state (4.12) with the exponent m, times the quasihole factors prod_i (z_i - h) of (4.14)
for the positions h in `holes`. It is the Metropolis method of droplet_density.py, written as in
webnotes/checks/session04/conventions.py, with nw walkers that move one electron at a time, so that the same seed gives
the same numbers as there. This file is pure numpy and writes no figure, so that a check script can import it."""
from math import lgamma

import numpy as np

EDGES = np.linspace(0, 14, 57)              # bins of 0.25 l_B for the density
RADII = np.arange(0.25, 13.01, 0.25)        # radii of the discs where the electrons are counted


def orbital_density(m, r):
    """|psi_m|^2 = r^(2m) exp(-r^2/2) / (2 pi 2^m m!), normalized to one over the plane."""
    return np.exp(2 * m * np.log(np.maximum(r, 1e-300)) - r ** 2 / 2 - m * np.log(2) - lgamma(m + 1)) / (2 * np.pi)


def filled_filling(N, r):
    """2 pi l_B^2 times the density of the filled level of N electrons, the orbitals m = 0 to N-1."""
    return 2 * np.pi * sum(orbital_density(m, r) for m in range(N))


def metropolis(N, m, holes, seed, nw=300, neq=150, nmeas=350, step=1.0):
    """Samples the Laughlin state of N electrons with the exponent m and quasiholes at the complex positions `holes`.
    Returns the bin centers of EDGES, 2 pi l_B^2 times the density in each bin, and the mean number of electrons
    inside each disc of radius RADII around the origin."""
    rng = np.random.default_rng(seed)
    holes = np.array(holes, complex)
    z = np.sqrt(2 * m * N * rng.random((nw, N))) * np.exp(2j * np.pi * rng.random((nw, N)))
    nin, hist = np.zeros(len(RADII)), np.zeros(len(EDGES) - 1)
    for sweep in range(neq + nmeas):
        for i in range(N):
            zi = z[:, i]
            zn = zi + step * (rng.normal(size=nw) + 1j * rng.normal(size=nw)) / np.sqrt(2)
            o = np.concatenate([z[:, :i], z[:, i + 1:]], axis=1)
            dl = 2 * m * np.log(np.abs((zn[:, None] - o) / (zi[:, None] - o))).sum(1) - (np.abs(zn) ** 2 - np.abs(zi) ** 2) / 2
            for hh in holes:
                dl += 2 * np.log(np.abs((zn - hh) / (zi - hh)))
            ok = np.log(rng.random(nw)) < dl
            z[ok, i] = zn[ok]
        if sweep >= neq:
            r = np.abs(z)
            nin += (r[:, :, None] < RADII[None, None, :]).sum(1).mean(0)
            hist += np.histogram(r.ravel(), EDGES)[0]
    shell = np.pi * (EDGES[1:] ** 2 - EDGES[:-1] ** 2)
    filling = 2 * np.pi * hist / (nmeas * nw) / shell
    return 0.5 * (EDGES[1:] + EDGES[:-1]), filling, nin / nmeas
