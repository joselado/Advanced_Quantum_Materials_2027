"""Shared tight-binding of the honeycomb lattice with real first-neighbor hopping and imaginary second-neighbor hopping.

The magnon Hamiltonian of a honeycomb ferromagnet with Dzyaloshinskii-Moriya exchange has this form, up to a constant,
with t = J S and t2 = D S, and a phase of +-pi/2 on the second-neighbor hopping. Lattice vectors a1=(1,0), a2=(1/2, sqrt(3)/2),
sublattice A at the lattice points and B at a displacement (a1+a2)/3."""
import numpy as np

a1 = np.array([1.0, 0.0]); a2 = np.array([0.5, np.sqrt(3) / 2])
# first neighbors of A: B in the cells (0,0), (-1,0), (0,-1)
NN = [(0, 0), (-1, 0), (0, -1)]
# second neighbors, A to A with phase +1 for these three steps (counterclockwise triangle), -1 for the opposite ones, and reversed on B
STEPS = [(1, 0), (-1, 1), (0, -1)]

def hops(t, t2, phi):
    """List of (i_sub, j_sub, (dn, dm), amplitude) for H[i, j] with i in cell R+d and j in cell R."""
    out = []
    for dn, dm in NN:                      # A(R) with B(R+d), hopping -t, both directions
        out.append((1, 0, (dn, dm), -t)); out.append((0, 1, (-dn, -dm), -t))
    for sub, sgn in ((0, 1), (1, -1)):
        for d in STEPS:
            out.append((sub, sub, d, t2 * np.exp(1j * sgn * phi)))
            out.append((sub, sub, (-d[0], -d[1]), t2 * np.exp(-1j * sgn * phi)))
    return out

def hk(k, t, t2, phi=np.pi / 2):
    """Bloch Hamiltonian, 2x2, k in Cartesian coordinates. The phase of a hop is exp(i k . d) with d the lattice vector."""
    h = np.zeros((2, 2), complex)
    for i, j, (dn, dm), amp in hops(t, t2, phi):
        h[i, j] += amp * np.exp(1j * (k @ (dn * a1 + dm * a2)))
    return h

def ribbon(kx, W, t, t2, phi=np.pi / 2):
    """Zigzag ribbon, periodic along a1 and W cells along a2. Basis index 2*m + sublattice. Returns the matrix."""
    H = np.zeros((2 * W, 2 * W), complex)
    for i, j, (dn, dm), amp in hops(t, t2, phi):
        for m in range(W):
            m2 = m + dm
            if 0 <= m2 < W:
                H[2 * m2 + i, 2 * m + j] += amp * np.exp(1j * kx * dn)
    return H

def path(npts=120):
    G = np.array([0.0, 0.0]); K = np.array([4 * np.pi / 3, 0.0]); M = np.array([np.pi, np.pi / np.sqrt(3)])
    pts, ticks = [], [0]
    for A, B in ((G, K), (K, M), (M, G)):
        for s in np.linspace(0, 1, npts, endpoint=False):
            pts.append(A + (B - A) * s)
        ticks.append(len(pts))
    pts.append(G)
    return np.array(pts), ticks
