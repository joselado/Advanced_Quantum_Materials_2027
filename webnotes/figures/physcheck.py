"""Berry curvature, Chern number, Zak phase and gap of a Bloch Hamiltonian, in the convention of the web notes.

The convention is the one of webnotes/conventions/session03.md. The connection is A = i <u|d_k u>, the curvature is
Omega_n = -2 Im <d_kx u_n | d_ky u_n>, its curl, and the Chern number is C = sum over the filled bands of
(1/2 pi) int Omega_n d^2k. With this sign the lower band of H = d.sigma has Omega = +(1/2) d.(d_kx d x d_ky d)/|d|^3,
the Haldane model of figures/session03/_honeycomb.bloch with t2=0.1 has C = +1, and pyqula's h.get_chern() agrees.

A Bloch Hamiltonian is a function hk(k) that returns a Hermitian matrix. In two dimensions k is the Cartesian
momentum, an array (kx, ky), and B holds the reciprocal vectors as its rows b1 and b2. In one dimension k is a number
and B is the length of the zone. The bands are counted from 0 at the lowest energy, and the argument bands is one
index or a list of them, for instance range(2) for two filled bands.

The Kubo form needs no phase of the eigenvectors and no periodic hk, so it is the reference. The link variables and
the Wilson loop close a loop across the zone, so they need hk(k + b) = hk(k), the gauge where every orbital sits at
the origin of its cell. pyqula's h.get_hk_gen() is in that gauge, and from_pyqula turns it into such a function.

This file needs numpy only. A figure script or a check script imports it, and it writes no figure and no file.
The checks are webnotes/checks/test_physcheck.py."""
import numpy as np


def reciprocal(A):
    """The reciprocal vectors, as rows b_i with a_i.b_j = 2 pi delta_ij, of the lattice vectors given as the rows of A."""
    A = np.atleast_2d(np.asarray(A, float))
    return 2 * np.pi * np.linalg.inv(A).T


def kmesh(B, nk, points=()):
    """The uniform mesh k = (i b1 + j b2)/nk of one zone, with the Cartesian points given in points added at its end.
    In one dimension B is the length of the zone and the mesh is k = i B/nk. The mesh has no weights, so it is for a
    minimum such as a gap. A mesh with nk a multiple of 3 holds K and K' of a hexagonal lattice, and an even nk holds M."""
    s = np.arange(nk) / nk
    if np.ndim(B) == 0 or np.size(B) == 1:
        ks = s * float(np.ravel(B)[0])
        return np.concatenate([ks, np.asarray(points, float).ravel()])
    B = np.asarray(B, float)
    ks = (s[:, None, None] * B[0] + s[None, :, None] * B[1]).reshape(-1, 2)
    if len(points):
        ks = np.concatenate([ks, np.asarray(points, float).reshape(-1, 2)])
    return ks


def _bands(bands):
    """The list of band indices for one index or a list of them."""
    return [int(bands)] if np.ndim(bands) == 0 else [int(n) for n in bands]


def _derivative(f, step):
    """d f(s)/ds at s=0 by the central difference of fourth order, exact to rounding for a tight-binding hk."""
    return (8 * (f(step) - f(-step)) - (f(2 * step) - f(-2 * step))) / (12 * step)


def berry_curvature(hk, k, bands=0, step=1e-3):
    """The Berry curvature Omega = -2 Im <d_kx u|d_ky u> of a band at the Cartesian k, positive for the lower band of
    the Haldane model of the notes at K. It is the Kubo form
    Omega = i sum_{n in bands, m not} [<n|d_x H|m><m|d_y H|n> - (x <-> y)]/(e_n - e_m)^2,
    which needs no phase of the eigenvectors. For a list of bands it is the sum of their curvatures, and the terms
    between two bands of the list cancel, so the filled bands may be degenerate with each other."""
    k = np.asarray(k, float)
    e, v = np.linalg.eigh(hk(k))
    ex, ey = np.array([1.0, 0.0]), np.array([0.0, 1.0])
    X = v.conj().T @ _derivative(lambda s: hk(k + s * ex), step) @ v
    Y = v.conj().T @ _derivative(lambda s: hk(k + s * ey), step) @ v
    S = _bands(bands)
    R = [m for m in range(len(e)) if m not in S]
    z = X[np.ix_(S, R)] * Y[np.ix_(R, S)].T / (e[S][:, None] - e[R][None, :]) ** 2
    return float(-2 * np.imag(z.sum()))


def chern_kubo(hk, B, bands=0, nk=48):
    """The Chern number C = (1/2 pi) int Omega d^2k of the bands, with Omega = -2 Im <d_kx u|d_ky u> from the Kubo
    form on the nk x nk mesh of the zone of B, so C = +1 for pyqula's add_haldane(0.1). It converges fast with nk
    but it is an integer only in the limit, so chern_links is the one that counts and this one is the check of the sign."""
    area = abs(np.linalg.det(np.asarray(B, float)))
    om = [berry_curvature(hk, k, bands) for k in kmesh(B, nk)]
    return float(area * np.mean(om) / (2 * np.pi))


def _periodic(hk, k, b):
    """Stops when hk(k + b) is not hk(k), since a loop across the zone would then not close."""
    if not np.allclose(hk(k + b), hk(k), atol=1e-9):
        raise ValueError('hk(k + b) is not hk(k), the link variables need the gauge where the Bloch phase of a '
                         'hopping is exp(i k.R) with R a lattice vector')


def _states(hk, ks, bands):
    """The eigenvectors of the bands at the momenta ks, an array of shape (len(ks), dimension, number of bands)."""
    H = np.array([hk(k) for k in ks])
    return np.linalg.eigh(H)[1][:, :, _bands(bands)]


def _link(v1, v2):
    """The link variable det <u(k1)|u(k2)> of the bands, with modulus one, for arrays of states."""
    z = np.linalg.det(np.conj(np.swapaxes(v1, -1, -2)) @ v2)
    return z / np.abs(z)


def chern_links(hk, B, bands=0, nk=24):
    """The Chern number of the bands from the link variables on the nk x nk mesh of the zone of B, an integer for any
    mesh that resolves the gap, with the sign of the notes, so C = +1 for pyqula's add_haldane(0.1). The plaquette
    phase taken counterclockwise is minus Omega times the area, so the sum of the phases is multiplied by -1 here,
    and by the sign of det B when b1, b2 is a left-handed pair. Several bands enter through the determinant of their
    overlaps, the non-abelian form, so they may cross each other."""
    B = np.asarray(B, float)
    k0 = np.array([0.123, 0.456])
    _periodic(hk, k0, B[0]); _periodic(hk, k0, B[1])
    v = _states(hk, kmesh(B, nk), bands)
    v = v.reshape((nk, nk) + v.shape[1:])
    U1 = _link(v, np.roll(v, -1, axis=0)); U2 = _link(v, np.roll(v, -1, axis=1))
    F = np.angle(U1 * np.roll(U2, -1, axis=0) / np.roll(U1, -1, axis=1) / U2)
    return float(-np.sign(np.linalg.det(B)) * F.sum() / (2 * np.pi))


def zak_phase(hk, B, bands=0, nk=200):
    """The Zak phase int A dk across the zone of length B, with A = i <u|d_k u>, so gamma = -Im log prod <u_j|u_j+1>,
    returned modulo 2 pi in the interval from -pi to pi with -pi written as pi. It is a Wilson loop of nk steps and it
    needs hk(k + B) = hk(k). In that gauge the phase depends on the choice of the unit cell, so the SSH chain gives pi
    when the hopping inside the cell is the weak one and 0 when it is the strong one."""
    G = float(np.ravel(B)[0])
    _periodic(hk, 0.123, G)
    v = _states(hk, kmesh(G, nk), bands)
    z = np.prod(_link(v, np.roll(v, -1, axis=0)))
    gamma = float(-np.angle(z))
    return gamma + 2 * np.pi if gamma < -np.pi + 1e-9 else gamma


def gap(hk, B, nfilled, nk=60, points=(), direct=False):
    """The gap between the nfilled lowest bands and the bands above them, the lowest empty energy minus the highest
    filled energy on the mesh kmesh(B, nk, points), which is negative when the bands overlap. With direct=True it is
    the smallest difference at one k. A mesh only bounds the gap from above, so the momenta where it closes are
    given in points, in Cartesian coordinates, or nk is chosen so that the mesh holds them."""
    ks = kmesh(B, nk, points)
    e = np.linalg.eigvalsh(np.array([hk(k) for k in ks]))
    if direct:
        return float(np.min(e[:, nfilled] - e[:, nfilled - 1]))
    return float(np.min(e[:, nfilled]) - np.max(e[:, nfilled - 1]))


def from_pyqula(h):
    """(hk, B) for a pyqula Hamiltonian h in one or two dimensions. hk takes the Cartesian momentum, in units of the
    inverse of the unit of length of the geometry, and B holds the reciprocal vectors as rows, with a_i.b_j = 2 pi
    delta_ij. pyqula's h.get_hk_gen() takes the reduced momentum k.a_i/2 pi and puts every site at the origin of its
    cell, so hk is periodic over B and its Chern number here has the sign of h.get_chern(). In one dimension k is a
    number and B is the length of the zone. The filled bands are the caller's choice, for instance bands=0 for
    has_spin=False at half filling and bands=range(2) for the same lattice with the two spins."""
    d = h.dimensionality
    if d not in (1, 2):
        raise ValueError('from_pyqula needs a Hamiltonian of dimensionality 1 or 2')
    g = h.geometry
    if d == 1:
        A = np.array([[np.linalg.norm(np.asarray(g.a1, float))]])
    else:
        A = np.array([g.a1, g.a2], float)
        if np.abs(A[:, 2]).max() > 1e-9:
            raise ValueError('from_pyqula needs the lattice vectors a1 and a2 in the plane xy')
        A = A[:, :2]
    gen = h.get_hk_gen()

    def hk(k):
        kr = np.zeros(3)
        kr[:d] = A @ np.atleast_1d(np.asarray(k, float)) / (2 * np.pi)
        m = gen(kr)
        return np.asarray(m.todense() if hasattr(m, 'todense') else m)

    B = reciprocal(A)
    return hk, (float(B[0, 0]) if d == 1 else B)
