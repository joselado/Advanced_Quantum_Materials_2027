"""Session 6, the statements of page 01 (Section 6.1) that its quiz on magnons in a Mott insulator makes.

The quiz says that a magnon is created by S^-, which changes S^z by one and keeps the number of electrons, that a
charge e needs an electron added or removed, and, in the feedback of its first option, that the triplet of the
Hubbard dimer at half filling and large U lies above the singlet by J = 4t^2/U and moves no charge, since every site
keeps one electron. This script builds one site and the dimer with Jordan-Wigner matrices and checks these
statements, and the ratios of the conventions sheet of the session at U = 4t, 8t and 16t. It needs numpy only and
writes no file."""
import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


a = np.array([[0., 1.], [0., 0.]])                        # destroys a fermion in one mode
Z = np.diag([1., -1.])                                    # the string (-1)^n
I2 = np.eye(2)
d = lambda m: m.conj().T


def modes(L):
    """The annihilation operators of L fermionic modes, with the Jordan-Wigner string."""
    out = []
    for j in range(L):
        ops = [Z] * j + [a] + [I2] * (L - j - 1)
        M = ops[0]
        for o in ops[1:]:
            M = np.kron(M, o)
        out.append(M)
    return out


# one site, the modes (up, down)
cu, cd = modes(2)
nu, nd = d(cu) @ cu, d(cd) @ cd
N = nu + nd
Sz = 0.5 * (nu - nd)
Sm = d(cd) @ cu                                           # S^- = c_dn^dag c_up
comm = lambda A, B: A @ B - B @ A
check('[S^z, S^-] = -S^-, so S^- lowers S^z by one', np.allclose(comm(Sz, Sm), -Sm), 'ok')
check('[N, S^-] = 0, so S^- keeps the number of electrons', np.allclose(comm(N, Sm), 0), 'ok')
check('[N, c_up^dag] = c_up^dag, a charge e needs an electron added', np.allclose(comm(N, d(cu)), d(cu)), 'ok')

# the Hubbard dimer, modes (0 up, 0 dn, 1 up, 1 dn), at half filling
c = modes(4)
n = [d(x) @ x for x in c]
Ntot = sum(n)
t = 1.0


def dimer(U):
    H = np.zeros((16, 16))
    for s in (0, 1):
        hop = d(c[s]) @ c[2 + s]
        H += -t * (hop + d(hop))
    H += U * (n[0] @ n[1] + n[2] @ n[3])
    return H


def spin(i):
    up, dn = c[2 * i], c[2 * i + 1]
    sx = 0.5 * (d(up) @ dn + d(dn) @ up)
    sy = 0.5 * (-1j * d(up) @ dn + 1j * d(dn) @ up)
    sz = 0.5 * (d(up) @ up - d(dn) @ dn)
    return np.array([sx, sy, sz])


Stot = spin(0) + spin(1)
S2tot = sum(Stot[k] @ Stot[k] for k in range(3))
half = np.where(np.isclose(np.diag(Ntot), 2))[0]           # the six states with two electrons


def levels(U):
    H = dimer(U)[np.ix_(half, half)]
    w, v = np.linalg.eigh(H)
    return w, v


ratios = []
for U in (4.0, 8.0, 16.0, 50.0, 100.0):
    w, v = levels(U)
    ES = U / 2 - np.sqrt(U ** 2 / 4 + 4 * t ** 2)
    ok = np.isclose(w[0], ES) and np.allclose(w[1:4], 0.0)
    check(f'U = {U:g}t, the singlet at U/2 - sqrt(U^2/4 + 4t^2) and three triplet levels at 0', ok, np.round(w, 4))
    ratios.append((0 - w[0]) / (4 * t ** 2 / U))
check('(E_T - E_S)/(4t^2/U) is 0.8284, 0.9443, 0.9848 at U = 4t, 8t, 16t, the values of the sheet',
      np.allclose(ratios[:3], [0.8284, 0.9443, 0.9848], atol=1e-4), np.round(ratios[:3], 4))
check('(E_T - E_S)/(4t^2/U) goes to 1 at large U as 1 - 4t^2/U^2, 0.9984 at 50t and 0.9996 at 100t',
      np.allclose(ratios[3:], [1 - 4 / 50 ** 2, 1 - 4 / 100 ** 2], atol=1e-5), np.round(ratios[3:], 5))

# the triplet moves no charge, every site keeps one electron, and it has total spin one
U = 20.0
w, v = levels(U)
P = v[:, 1:4]                                             # the three triplet states, in the basis of the six states
sub = lambda O: O[np.ix_(half, half)]
n0 = sub(n[0] + n[1])
docc = sub(n[0] @ n[1] + n[2] @ n[3])
on_site = [P[:, i] @ n0 @ P[:, i] for i in range(3)]
fluct = [P[:, i] @ sub((n[0] + n[1]) @ (n[0] + n[1])) @ P[:, i] - on_site[i] ** 2 for i in range(3)]
dbl = [P[:, i] @ docc @ P[:, i] for i in range(3)]
check('on the triplet each site has exactly one electron, with no fluctuation of the charge',
      np.allclose(on_site, 1) and np.allclose(fluct, 0) and np.allclose(dbl, 0), (np.round(on_site, 12), np.round(dbl, 12)))
S2 = [P[:, i] @ sub(S2tot).real @ P[:, i] for i in range(3)]
check('the three degenerate levels have S(S+1) = 2, a triplet of spin one', np.allclose(S2, 2), np.round(S2, 12))
gs = v[:, 0]
check('the ground state is the singlet, S(S+1) = 0', np.isclose(gs @ sub(S2tot).real @ gs, 0), 'ok')
# of the opener: a quantum magnet made of such singlets, a valence bond, has its lowest excitation at spin 1, so
# the spin-1/2 excitations of the opener are those of the quantum spin liquids and not of every quantum magnet
check('the lowest excitation of the singlet of the dimer is the triplet of spin one, below every other level',
      np.allclose(S2, 2) and w[4] > w[1] + 1e-6, np.round(w, 4))

# a magnon on a ferromagnet of four spins 1/2 changes the total S^z by one, and a spinon is a free S = 1/2
sz1, sm1 = np.diag([0.5, -0.5]), np.array([[0., 0.], [1., 0.]])


def site(op, j, L=4):
    ops = [np.eye(2)] * L
    ops[j] = op
    M = ops[0]
    for o in ops[1:]:
        M = np.kron(M, o)
    return M


SzT = sum(site(sz1, j) for j in range(4))
fm = np.zeros(16)
fm[0] = 1.0                                               # all four spins up
mag = site(sm1, 2) @ fm
check('S^- on one site of the ferromagnet of four spins changes the total S^z from 2 to 1, Delta S = 1',
      np.isclose(fm @ SzT @ fm, 2) and np.isclose(mag @ SzT @ mag / (mag @ mag), 1), 'ok')
s2half = sum(m @ m for m in (0.5 * np.array([[0, 1], [1, 0]]), 0.5 * np.array([[0, -1j], [1j, 0]]), sz1))
check('a spin 1/2 has S(S+1) = 3/4, the spin of a spinon', np.allclose(s2half, 0.75 * np.eye(2)), 'ok')

# corrected on 2026-11-22, "Magnons have no charge, so an electric field does not push them as it pushes an electron".
# A potential V_i n_i commutes with S^- of every site, so it gives no force on a spin flip, which moves no charge. The old
# "electric fields do not affect them at all" is too strong: a potential difference V between the two sites of the dimer
# changes the singlet-triplet splitting, from 4t^2/U to about 4t^2 U/(U^2 - V^2) at second order, which we check by
# exact diagonalization and by that formula at U = 20t.
Sm_site = [d(c[2 * i + 1]) @ c[2 * i] for i in (0, 1)]
Vpot = 0.7 * (n[0] + n[1]) - 0.3 * (n[2] + n[3])
check('a potential V_i n_i commutes with S^- of each site, so it does not act on a spin flip as a force',
      all(np.allclose(comm(Vpot, s), 0) for s in Sm_site), 'ok')
split = {}
for V in (0.0, 4.0):
    Hb = dimer(20.0) + V / 2 * (n[0] + n[1]) - V / 2 * (n[2] + n[3])
    wb = np.linalg.eigvalsh(Hb[np.ix_(half, half)])
    split[V] = wb[1] - wb[0]
pert = 4 * t ** 2 * 20.0 / (20.0 ** 2 - 4.0 ** 2)
check('a potential difference V = 4t between the two sites raises the singlet-triplet splitting of the dimer at U = 20t '
      'from 0.198t to 0.206t, close to 4t^2 U/(U^2 - V^2) = 0.208t, so an electric field does change the magnon energy',
      round(split[0.0], 3) == 0.198 and round(split[4.0], 3) == 0.206 and abs(split[4.0] - pert) / pert < 0.02,
      (round(split[0.0], 4), round(split[4.0], 4), round(pert, 4)))
print('page 01 of Session 6: all statements hold')
