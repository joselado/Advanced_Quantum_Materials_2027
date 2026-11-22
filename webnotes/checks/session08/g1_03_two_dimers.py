"""Session 8, the statements of page 03 (Section 8.3), the Ising dimer (8.1) and the Heisenberg dimer (8.2).

It checks the levels of the two dimers and of H = J S0.S1 for J = -1 (the caption of dimer_levels, the second quiz
and its figure), the opener and the caption (the Ising ground level is twofold, its two product states |up down> and
|down up> each break time reversal, while the singlet in the same level keeps it), the steps of the fold (|up up> at +1/4, the 2x2 block of the antiparallel states, the identity
S0.S1 = (S(S+1) - 3/2)/2 with S_i^2 = 3/4, and <S_i> = 0 in the singlet), the key box and the text (the singlet is
unique, time reversal maps it to itself while it maps |up down> to -|down up>, and its entanglement entropy is
log 2 = 0.693), the first quiz (the Ising energies -1/4 and +1/4), the third quiz (the triplet state with S^z = 0 at
+1/4, H|up down> = -1/4 |up down> + 1/2 |down up>, and its mean energy -1/4), and the problem (each of the three terms
gives -1/4 in the singlet, sigma^a sigma^a turns the singlet into minus itself for a = x, y, the Ising minimum is
-1/4, and a product state has <S0.S1> = <S0>.<S1> >= -1/4). The recall box quotes J = 4t^2/U > 0 of (6.5), and the
exact Hubbard dimer at U = 20t is compared with it as the conventions sheet does.

Every level comes from the 4x4 matrices, and the main numbers also from the closed form with the total spin. It needs
numpy only and writes no file."""
from functools import reduce
import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


SX, SY, SZ = np.array([[0, 1], [1, 0]]) / 2, np.array([[0, -1j], [1j, 0]]) / 2, np.diag([.5, -.5])
I2 = np.eye(2)
UP, DN = np.array([1., 0.]), np.array([0., 1.])
UU, UD, DU, DD = (np.kron(a, b) for a in (UP, DN) for b in (UP, DN))
HEIS = sum(np.kron(s, s) for s in (SX, SY, SZ))
ISING = np.kron(SZ, SZ)
S = [np.kron(s, I2) + np.kron(I2, s) for s in (SX, SY, SZ)]
S2 = sum(s @ s for s in S)
SINGLET = (UD - DU) / np.sqrt(2)
T0 = (UD + DU) / np.sqrt(2)


def levels(H):
    e = np.round(np.linalg.eigvalsh(H), 10)
    return [(v, int((e == v).sum())) for v in sorted(set(e))]


# the levels, the caption of dimer_levels and the second quiz with its figure
check('Ising dimer, -1/4 and +1/4 twice each', levels(ISING) == [(-0.25, 2), (0.25, 2)], levels(ISING))
check('Heisenberg dimer, the singlet at -3/4 once and the triplet at +1/4 three times, a gap of 1 (J)',
      levels(HEIS) == [(-0.75, 1), (0.25, 3)], levels(HEIS))
check('quiz 2, J = -1: the triplet at -1/4 three times is the ground level, the singlet at +3/4',
      levels(-HEIS) == [(-0.25, 3), (0.75, 1)], levels(-HEIS))
check('quiz 2, J = -1: |down down> and the triplet with S^z = 0 have the same energy J/4 = -1/4',
      np.allclose(-HEIS @ DD, -0.25 * DD) and np.allclose(-HEIS @ T0, -0.25 * T0), -0.25)

# the steps of the fold
Sp, Sm = SX + 1j * SY, SX - 1j * SY
check('fold, S0.S1 = Sz0 Sz1 + (S+0 S-1 + S-0 S+1)/2', np.allclose(HEIS, ISING + 0.5 * (np.kron(Sp, Sm) + np.kron(Sm, Sp))), 'ok')
check('fold, |up up> and |down down> have +1/4, the bracket gives zero on them',
      np.allclose(HEIS @ UU, 0.25 * UU) and np.allclose(HEIS @ DD, 0.25 * DD)
      and np.allclose((np.kron(Sp, Sm) + np.kron(Sm, Sp)) @ UU, 0), 0.25)
block = np.array([[np.vdot(a, HEIS @ b) for b in (UD, DU)] for a in (UD, DU)]).real
check('fold, the block of |up down>, |down up> is [[-1/4, 1/2], [1/2, -1/4]]', np.allclose(block, [[-.25, .5], [.5, -.25]]), block.tolist())
check('fold, +1/4 for (ud + du)/sqrt2 and -3/4 for (ud - du)/sqrt2, which is (8.3)',
      np.allclose(HEIS @ T0, 0.25 * T0) and np.allclose(HEIS @ SINGLET, -0.75 * SINGLET), (0.25, -0.75))
Si2 = sum(s @ s for s in (SX, SY, SZ))
check('fold, S_i^2 = 3/4 for a spin one half', np.allclose(Si2, 0.75 * I2), 0.75)
check('fold, S0.S1 = (S^2 - S0^2 - S1^2)/2', np.allclose(HEIS, 0.5 * (S2 - 1.5 * np.eye(4))), 'ok')
check('fold, (S(S+1) - 3/2)/2 is -3/4 for S = 0 and +1/4 for S = 1, and 2S+1 = 3',
      (0 - 1.5) / 2 == -0.75 and (2 - 1.5) / 2 == 0.25 and 2 * 1 + 1 == 3, (-0.75, 0.25))
check('fold, the singlet has S = 0 and the three states at +1/4 have S = 1',
      np.allclose(S2 @ SINGLET, 0) and all(np.allclose(S2 @ v, 2 * v) for v in (UU, T0, DD)), 'ok')
mean = [np.vdot(SINGLET, np.kron(s, I2) @ SINGLET).real for s in (SX, SY, SZ)] + \
       [np.vdot(SINGLET, np.kron(I2, s) @ SINGLET).real for s in (SX, SY, SZ)]
check('fold and (8.3), <S_i> = 0 for every component on both sites', np.allclose(mean, 0), mean)
flipped = np.kron(SX, I2) @ SINGLET
check('fold, S^x_0 takes the singlet to |down down> and |up up>, orthogonal to it',
      np.isclose(np.vdot(SINGLET, flipped), 0) and np.isclose(abs(np.vdot(UU, flipped)) ** 2 + abs(np.vdot(DD, flipped)) ** 2,
                                                          np.vdot(flipped, flipped).real), 'ok')

# the key box and the three points of the text: unique, time-reversal symmetric, maximally entangled
check('key box, the ground level of the Heisenberg dimer is not degenerate', levels(HEIS)[0][1] == 1, 1)
theta = np.kron(1j * 2 * SY, 1j * 2 * SY)          # time reversal is theta K with theta = i sigma^y on each spin
TR = lambda v: theta @ v.conj()
check('key box, time reversal maps the singlet to itself', np.allclose(TR(SINGLET), SINGLET), 'ok')
check('text, time reversal maps |up down> to -|down up>, so it exchanges the two Ising ground states',
      np.allclose(TR(UD), -DU) and np.allclose(TR(DU), -UD), 'ok')
# the opener and the caption of dimer_levels: the Ising ground level is twofold, spanned by the product states |up down>
# and |down up>, and each of them breaks time reversal, since theta K takes it to a state orthogonal to it. The level
# also holds states that keep the symmetry, such as the singlet, with theta K s = s and <S^z_0> = 0, so the statement
# is made for the two product states and not for every state of the level.
e, v = np.linalg.eigh(ISING)
P = v[:, np.isclose(e, -0.25)] @ v[:, np.isclose(e, -0.25)].conj().T
check('opener and caption, the Ising ground level at -1/4 is twofold and is the span of |up down> and |down up>',
      int(np.isclose(e, -0.25).sum()) == 2 and np.allclose(P, np.outer(UD, UD) + np.outer(DU, DU)), 2)
check('opener and caption, <up down|theta up down> = <down up|theta down up> = 0, so each product state breaks time reversal',
      np.isclose(np.vdot(UD, TR(UD)), 0) and np.isclose(np.vdot(DU, TR(DU)), 0)
      and np.isclose(np.vdot(UD, np.kron(SZ, I2) @ UD).real, 0.5), (0, 0.5))
check('opener and caption, the singlet lies in the Ising ground level with theta K s = s and <S^z_0> = 0',
      np.allclose(ISING @ SINGLET, -0.25 * SINGLET) and np.allclose(TR(SINGLET), SINGLET)
      and np.isclose(np.vdot(SINGLET, np.kron(SZ, I2) @ SINGLET).real, 0), -0.25)
rho = np.outer(SINGLET, SINGLET).reshape(2, 2, 2, 2).trace(axis1=1, axis2=3)
p = np.linalg.eigvalsh(rho)
ent = -sum(x * np.log(x) for x in p if x > 1e-12)
check('text, the Schmidt weights are 1/2 and 1/2 and the entropy is log 2 = 0.693', np.allclose(p, 0.5) and round(ent, 3) == 0.693,
      round(ent, 6))

# quiz 1: the Ising energies of |up down> and |up up>
check('quiz 1, the Ising dimer gives -1/4 for |up down> and +1/4 for |up up>',
      np.isclose(np.vdot(UD, ISING @ UD), -0.25) and np.isclose(np.vdot(UU, ISING @ UU), 0.25), (-0.25, 0.25))

# quiz 3
check('quiz 3, the triplet state with S^z = 0 has S = 1 and +1/4, one above the singlet',
      np.allclose(S2 @ T0, 2 * T0) and np.allclose(HEIS @ T0, 0.25 * T0), 0.25)
check('quiz 3, H|up down> = -1/4 |up down> + 1/2 |down up>, not an eigenstate',
      np.allclose(HEIS @ UD, -0.25 * UD + 0.5 * DU), 'ok')
check('quiz 3, the mean energy of |up down> is -1/4, above -3/4', np.isclose(np.vdot(UD, HEIS @ UD).real, -0.25), -0.25)

# the problem
terms = [np.vdot(SINGLET, np.kron(s, s) @ SINGLET).real for s in (SX, SY, SZ)]
check('problem, <s|S^a_0 S^a_1|s> = -1/4 for a = x, y, z, and the sum is -3/4', np.allclose(terms, -0.25) and np.isclose(sum(terms), -0.75), terms)
PX, PY = 2 * SX, 2 * SY
check('problem, sigma^y|up> = i|down> and sigma^y|down> = -i|up>', np.allclose(PY @ UP, 1j * DN) and np.allclose(PY @ DN, -1j * UP), 'ok')
check('problem, sigma^x sigma^x and sigma^y sigma^y turn |up down> into |down up> and the singlet into minus itself',
      np.allclose(np.kron(PX, PX) @ UD, DU) and np.allclose(np.kron(PY, PY) @ UD, DU)
      and np.allclose(np.kron(PX, PX) @ SINGLET, -SINGLET) and np.allclose(np.kron(PY, PY) @ SINGLET, -SINGLET), 'ok')
check('problem, the lowest energy of the Ising dimer is -1/4', np.isclose(np.linalg.eigvalsh(ISING)[0], -0.25), -0.25)
transverse = np.vdot(SINGLET, (np.kron(SX, SX) + np.kron(SY, SY)) @ SINGLET).real
check('problem, the other -1/2 of the singlet is the transverse part, -3/4 - (-1/4)',
      np.isclose(transverse, -0.5) and np.isclose(-0.75 - (-0.25), transverse), round(transverse, 12))
rng = np.random.default_rng(3)
best = 1.0
for _ in range(4000):
    a, b = rng.normal(size=2) + 1j * rng.normal(size=2), rng.normal(size=2) + 1j * rng.normal(size=2)
    v = np.kron(a / np.linalg.norm(a), b / np.linalg.norm(b))
    e = np.vdot(v, HEIS @ v).real
    m0 = [np.vdot(a, s @ a).real / np.vdot(a, a).real for s in (SX, SY, SZ)]
    m1 = [np.vdot(b, s @ b).real / np.vdot(b, b).real for s in (SX, SY, SZ)]
    assert np.isclose(e, np.dot(m0, m1)) and np.linalg.norm(m0) <= 0.5 + 1e-12
    best = min(best, e)
check('problem, a product state has <S0.S1> = <S0>.<S1>, never below -1/4, and the Neel pair reaches -1/4',
      best >= -0.25 - 1e-12 and np.isclose(np.vdot(UD, HEIS @ UD).real, -0.25), round(best, 4))

# the recall box: J = 4t^2/U > 0, the exact Hubbard dimer at U = 20t as the reference of the conventions sheet
U, t = 20.0, 1.0
split = 0 - (U / 2 - np.sqrt(U ** 2 / 4 + 4 * t ** 2))
check('recall box, the Hubbard dimer at U = 20t has the singlet 0.1980t below the triplet, against 4t^2/U = 0.2t',
      round(split, 4) == 0.1980 and 4 * t ** 2 / U == 0.2, round(split, 5))

# corrected on 2026-11-22, old text of the page
# quiz 1, third feedback: the level +1/4 of the Ising dimer is the span of |up up> and |down down>, so both states are
# the ones with energy +1/4, and not |up up> alone
e, v = np.linalg.eigh(ISING)
Pp = v[:, np.isclose(e, 0.25)] @ v[:, np.isclose(e, 0.25)].conj().T
check('corrected, quiz 1: the Ising level +1/4 is the span of |up up> and |down down>, with S^z_0 S^z_1 = +1/4 on both',
      np.allclose(Pp, np.outer(UU, UU) + np.outer(DD, DD)) and np.isclose(np.vdot(DD, ISING @ DD), 0.25)
      and np.isclose(np.vdot(UU, ISING @ UU), 0.25), (np.vdot(UU, ISING @ UU).real, np.vdot(DD, ISING @ DD).real))
# the text, second point: the reason is that time reversal maps the singlet to itself, and this gives <S_i> = 0, since
# theta K S theta^-1 K = -S for every component on each site. A zero net magnetization alone is not the reason, since
# |up down> has it too and theta K maps it to -|down up>, orthogonal to it.
odd = all(np.allclose(theta @ (np.kron(s, I2)).conj() @ np.linalg.inv(theta), -np.kron(s, I2))
          and np.allclose(theta @ (np.kron(I2, s)).conj() @ np.linalg.inv(theta), -np.kron(I2, s)) for s in (SX, SY, SZ))
net_ud = [np.vdot(UD, s_ @ UD).real for s_ in S]
check('corrected, text: theta K reverses every spin component, so a state that it maps to itself has <S_i> = 0, while '
      '|up down> has the net magnetization 0 and still breaks time reversal',
      odd and np.allclose(TR(SINGLET), SINGLET) and np.allclose(net_ud, 0) and np.isclose(np.vdot(UD, TR(UD)), 0), net_ud)
