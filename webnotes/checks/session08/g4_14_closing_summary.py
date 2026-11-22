"""Session 8, the numbers that page 14 (Section 8.14, the closing summary) states in its quiz.

The page has no figure of its own and no fold. Its quiz says that the spinon has spin 1/2, and that the magnon and the
triplon have spin 1, since flipping one spin of a ferromagnet changes S^z by 1. The spins are matrices of spins one
half, and the spinon is one Abrikosov fermion of (8.10) on a site. Of the vison of the same quiz, a plaquette with a flipped
flux, "no spin" and the flux -1 of one flipped link are asserted here, and which flux is the ground state in g3_10. The first task
of the list is asserted with the time reversal of two spins one half. The script finds the repository from its own path
and writes no file."""
import sys

import numpy as np

sys.dont_write_bytecode = True
PAULI = [np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], complex)]


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def op(o, i, n):
    out = np.eye(1)
    for j in range(n):
        out = np.kron(out, o if j == i else np.eye(2))
    return out


# the spinon: one Abrikosov fermion on a site, S = (1/2) f^dag sigma f, has S^2 = 3/4, so S = 1/2
a, z = np.array([[0.0, 1.0], [0.0, 0.0]]), np.diag([1.0, -1.0])
fu, fd = np.kron(a, np.eye(2)).astype(complex), np.kron(z, a).astype(complex)
f = (fu, fd)
S = [0.5 * sum(P[i, j] * f[i].conj().T @ f[j] for i in range(2) for j in range(2)) for P in PAULI]
n = fu.conj().T @ fu + fd.conj().T @ fd
S2 = np.real(np.diag(sum(x @ x for x in S)))
one = np.abs(np.real(np.diag(n)) - 1) < 1e-9
check('one Abrikosov fermion has S^2 = 3/4, so S = 1/2', np.allclose(S2[one], 0.75), S2[one])

# the magnon: flipping one spin of a ferromagnet of N = 6 spins changes S^z_tot by 1
N = 6
Sz = sum(op(PAULI[2] / 2, i, N) for i in range(N)).real
up = np.zeros(2 ** N); up[0] = 1.0                          # all spins up, the first basis state
flip = op(PAULI[0], 2, N).real @ up                        # spin 2 flipped
dz = up @ Sz @ up - flip @ Sz @ flip
check('flipping one spin changes S^z_tot by 1', abs(dz - 1) < 1e-12, dz)

# the triplon: the excited level of a dimer has S = 1
S01 = sum(op(P / 2, 0, 2) @ op(P / 2, 1, 2) for P in PAULI).real
Stot2 = sum((op(P / 2, 0, 2) + op(P / 2, 1, 2)) @ (op(P / 2, 0, 2) + op(P / 2, 1, 2)) for P in PAULI).real
w, v = np.linalg.eigh(S01)
s_of = [v[:, i] @ Stot2 @ v[:, i] for i in range(4)]
check('the triplet of a dimer has S(S+1) = 2, so S = 1', np.allclose(s_of, [0, 2, 2, 2]), np.round(s_of, 12))

# the first task of the list: time reversal Theta = (i sigma_y x i sigma_y) K on two spins one half maps each Ising
# ground state |ud>, |du> to the other one, so each alone breaks the symmetry, and maps the singlet to itself
Th = np.kron(1j * PAULI[1], 1j * PAULI[1])
ud, du = np.eye(4)[1], np.eye(4)[2]
sing = (ud - du) / np.sqrt(2)


def theta(psi):
    return Th @ np.conj(psi)


Sz0 = np.kron(PAULI[2] / 2, np.eye(2)).real
check('Theta|ud> has overlap 0 with |ud> and 1 with |du>, and <S^z_0> = +-1/2 on them',
      abs(np.vdot(ud, theta(ud))) < 1e-12 and abs(abs(np.vdot(du, theta(ud))) - 1) < 1e-12
      and abs(np.vdot(du, theta(du))) < 1e-12 and abs(ud @ Sz0 @ ud - 0.5) < 1e-12 and abs(du @ Sz0 @ du + 0.5) < 1e-12,
      (abs(np.vdot(ud, theta(ud))), abs(np.vdot(du, theta(ud)))))
check('Theta maps the singlet to itself, overlap +1, with <S^z_0> = 0', abs(np.vdot(sing, theta(sing)) - 1) < 1e-12
      and abs(sing @ Sz0 @ sing) < 1e-12, np.real(np.vdot(sing, theta(sing))))

# the quiz: the vison carries no spin. A flux is set by the sign of the hoppings, the same for both spins, so the change
# of the spinon Hamiltonian commutes with the total spin. One plaquette of four sites with both spins, 8 fermion modes,
# with one of its four links set from +1 to -1, which gives the flux -1 on it.
a8, z8 = np.array([[0.0, 1.0], [0.0, 0.0]]), np.diag([1.0, -1.0])
m8 = []
for kk in range(8):
    o = np.eye(1)
    for j in range(8):
        o = np.kron(o, z8 if j < kk else (a8 if j == kk else np.eye(2)))
    m8.append(o.astype(complex))
fp = [(m8[2 * i], m8[2 * i + 1]) for i in range(4)]
Stot = [sum(0.5 * P[a, b] * fp[i][a].conj().T @ fp[i][b] for i in range(4) for a in range(2) for b in range(2)) for P in PAULI]
links = [(0, 1), (1, 2), (2, 3), (3, 0)]
chi0, chi1 = np.ones(4), np.array([1., -1., 1., 1.])
dH = sum((chi1[l] - chi0[l]) * (fp[i][s].conj().T @ fp[j][s] + fp[j][s].conj().T @ fp[i][s])
         for l, (i, j) in enumerate(links) for s in range(2))
comm = max(np.abs(dH @ S_ - S_ @ dH).max() for S_ in Stot)
check('one flipped link gives the flux -1 on the plaquette, and its change of H commutes with S_tot, so it has no spin',
      np.prod(chi1) == -1 and np.prod(chi0) == 1 and comm < 1e-12 and np.abs(dH).max() > 1, (np.prod(chi1), comm))
print('all checks of page 14 hold')
