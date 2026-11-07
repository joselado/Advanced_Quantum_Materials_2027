"""Shared tight-binding of the honeycomb lattice for the web schematics of Sessions 3 and 4.

Lattice vectors a1=(1,0) and a2=(1/2, sqrt(3)/2), so the second-neighbor distance is 1 and the bond length is 1/sqrt(3).
Sublattice A sits at the lattice points and B at the displacement (a1+a2)/3. The first-neighbor hopping is -t. The Haldane
hopping is t2 exp(+i phi) along the three steps STEPS on sublattice A and t2 exp(-i phi) along them on sublattice B, which is
the counterclockwise convention, and the Kane-Mele model is this term with phi for spin up and -phi for spin down.
A third-neighbor hopping t3 connects A and B across a hexagon. M is the staggered potential, +M on A and -M on B.
This file writes no figure, the build only runs the scripts that a page uses."""
import numpy as np

a1 = np.array([1.0, 0.0]); a2 = np.array([0.5, np.sqrt(3) / 2])
DELTA = (a1 + a2) / 3
NN = [(0, 0), (-1, 0), (0, -1)]          # B in the cells R + d are the first neighbors of A in the cell R
NNN3 = [(-1, -1), (1, -1), (-1, 1)]      # B in the cells R + d are the third neighbors of A in the cell R
STEPS = [(1, 0), (-1, 1), (0, -1)]


def hops(t=1.0, t2=0.0, phi=np.pi / 2, t3=0.0):
    """(i_sub, j_sub, (dn, dm), amplitude) for H[i in cell R+d, j in cell R], with the sublattice index 0 for A and 1 for B."""
    out = []
    for dn, dm in NN:
        out.append((1, 0, (dn, dm), -t)); out.append((0, 1, (-dn, -dm), -t))
    if t3:
        for dn, dm in NNN3:
            out.append((1, 0, (dn, dm), -t3)); out.append((0, 1, (-dn, -dm), -t3))
    if t2:
        for sub, sgn in ((0, 1), (1, -1)):
            for d in STEPS:
                out.append((sub, sub, d, t2 * np.exp(1j * sgn * phi)))
                out.append((sub, sub, (-d[0], -d[1]), t2 * np.exp(-1j * sgn * phi)))
    return out


def bloch(k, t=1.0, t2=0.0, phi=np.pi / 2, M=0.0, t3=0.0):
    """The 2x2 Bloch Hamiltonian, k in Cartesian coordinates."""
    h = np.diag([M, -M]).astype(complex)
    for i, j, (dn, dm), amp in hops(t, t2, phi, t3):
        h[i, j] += amp * np.exp(1j * (k @ (dn * a1 + dm * a2)))
    return h


def ribbon(k, W, t=1.0, t2=0.0, phi=np.pi / 2, M=0.0, periodic=False):
    """Zigzag ribbon, periodic along a1 with the momentum k and W cells along a2. The basis index is 2*m + sublattice.
    M is a number or an array of W values, one per cell. With periodic=True the W cells close into a cylinder."""
    Ms = np.broadcast_to(np.asarray(M, float), (W,))
    H = np.zeros((2 * W, 2 * W), complex)
    for m in range(W):
        H[2 * m, 2 * m] += Ms[m]; H[2 * m + 1, 2 * m + 1] -= Ms[m]
    for i, j, (dn, dm), amp in hops(t, t2, phi):
        for m in range(W):
            m2 = m + dm
            if periodic:
                m2 %= W
            if 0 <= m2 < W:
                H[2 * m2 + i, 2 * m + j] += amp * np.exp(1j * k * dn)
    return H


SX = np.array([[0, 1], [1, 0]], complex); SY = np.array([[0, -1j], [1j, 0]]); SZ = np.diag([1.0, -1.0]).astype(complex)


def ribbon_spinful(k, W, t=1.0, lso=0.1, lr=0.0, bx=0.0):
    """Kane-Mele zigzag ribbon. The basis index is 2*(2*m + sublattice) + spin, spin 0 is up along z.
    lso is the Haldane hopping t2 with phi=+pi/2 for spin up and -pi/2 for spin down, which is the intrinsic spin-orbit
    coupling. lr is the Rashba coupling i lr (s x d)_z on the first-neighbor bonds, with d the unit bond vector from j to i.
    bx is an in-plane exchange field bx s_x on every site, which breaks time reversal."""
    n = 2 * W
    H = np.zeros((2 * n, 2 * n), complex)
    up = ribbon(k, W, t, lso, np.pi / 2); dn = ribbon(k, W, t, lso, -np.pi / 2)
    H[0::2, 0::2] = up; H[1::2, 1::2] = dn
    if lr:
        for (i, j, (dn_, dm), amp) in hops(t):
            d = (DELTA + dn_ * a1 + dm * a2) if i == 1 else -(DELTA + (-dn_) * a1 + (-dm) * a2)
            d = d / np.linalg.norm(d)
            S = 1j * lr * (SX * d[1] - SY * d[0])
            for m in range(W):
                m2 = m + dm
                if 0 <= m2 < W:
                    a, b = 2 * m2 + i, 2 * m + j
                    H[2 * a:2 * a + 2, 2 * b:2 * b + 2] += S * np.exp(1j * k * dn_)
    if bx:
        for a in range(n):
            H[2 * a:2 * a + 2, 2 * a:2 * a + 2] += bx * SX
    return H


def flake(R, t=1.0, t2=0.0, phi=np.pi / 2, M=0.0):
    """A finite disk of radius R of the honeycomb lattice, with the Haldane hopping and the staggered potential.
    Sites with a single neighbor are removed, so that the edge has no dangling atoms. Returns (positions, H)."""
    n = int(R) + 3
    pts, sub = [], []
    for i in range(-2 * n, 2 * n + 1):
        for j in range(-2 * n, 2 * n + 1):
            r = i * a1 + j * a2
            for s, off in ((0, 0 * DELTA), (1, DELTA)):
                p = r + off - DELTA / 2
                if np.hypot(*p) < R:
                    pts.append(p); sub.append(s)
    pts = np.array(pts); sub = np.array(sub)
    while True:
        D = np.linalg.norm(pts[:, None] - pts[None], axis=-1)
        nn = np.abs(D - 1 / np.sqrt(3)) < 1e-6
        keep = nn.sum(1) > 1
        if keep.all():
            break
        pts, sub = pts[keep], sub[keep]
    D = np.linalg.norm(pts[:, None] - pts[None], axis=-1)
    nn = np.abs(D - 1 / np.sqrt(3)) < 1e-6
    nnn = np.abs(D - 1.0) < 1e-6
    H = -t * nn.astype(complex)
    H += np.diag(np.where(sub == 0, M, -M))
    if t2:
        I, J = np.where(nnn)
        for i, j in zip(I, J):
            ls = np.where(nn[i] & nn[j])[0]
            if len(ls) == 0:
                continue
            l = ls[0]
            u, v = pts[l] - pts[j], pts[i] - pts[l]
            nu = np.sign(u[0] * v[1] - u[1] * v[0])
            H[i, j] += t2 * np.exp(1j * nu * phi)
    assert np.allclose(H, H.conj().T)
    return pts, sub, H


def path(npts=120):
    """The k-path Gamma, K, M, Gamma of the Brillouin zone of these lattice vectors."""
    G = np.array([0.0, 0.0]); K = np.array([4 * np.pi / 3, 0.0]); Mp = np.array([np.pi, np.pi / np.sqrt(3)])
    pts, ticks = [], [0]
    for A, B in ((G, K), (K, Mp), (Mp, G)):
        for s in np.linspace(0, 1, npts, endpoint=False):
            pts.append(A + (B - A) * s)
        ticks.append(len(pts))
    pts.append(G)
    return np.array(pts), ticks


def chern(N=48, band=0, **kw):
    """The Chern number of one band of bloch(**kw) from the link variables on an N x N grid."""
    B = 2 * np.pi * np.linalg.inv(np.array([a1, a2])).T
    vec = np.zeros((N, N, 2), complex)
    for i in range(N):
        for j in range(N):
            vec[i, j] = np.linalg.eigh(bloch(i / N * B[0] + j / N * B[1], **kw))[1][:, band]
    def link(v1, v2):
        z = np.sum(np.conj(v1) * v2, axis=-1)
        return z / np.abs(z)
    U1 = link(vec, np.roll(vec, -1, axis=0)); U2 = link(vec, np.roll(vec, -1, axis=1))
    F = np.angle(U1 * np.roll(U2, -1, axis=0) / np.roll(U1, -1, axis=1) / U2)
    return F.sum() / (2 * np.pi)
