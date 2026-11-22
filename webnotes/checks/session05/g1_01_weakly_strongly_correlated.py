"""Session 5, the statements of page 01 (Section 5.1) that the new quiz on the three decouplings makes.

The quiz writes three mean-field terms of the onsite interaction U n_up n_dn and says which one changes the number
of electrons. This script builds the four states of one site as matrices and checks the identities behind the signs
of the options, which operators keep the number of electrons, and the counterexample of the first option. The old
quiz of the page keeps its feedback, and its numbers, the filling 1/3 and the charge e/3, are asserted at the end, as
the Laughlin state with m = 3 and against the page of Section 4.16, which states the same values. Its third feedback,
corrected on 2026-11-22 to name the Majorana state as the fraction of an electron, is checked last. It needs numpy only
and writes no file."""
import os
import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# one site, the modes up and down with the Jordan-Wigner order (up, down), in the basis |n_up n_dn>
a = np.array([[0., 1.], [0., 0.]])                        # destroys a fermion in one mode
Z = np.diag([1., -1.])                                    # the string (-1)^n
I2 = np.eye(2)
cu = np.kron(a, I2)                                       # c_up
cd = np.kron(Z, a)                                        # c_dn, with the sign of the string
d = lambda m: m.conj().T
nu, nd = d(cu) @ cu, d(cd) @ cd
N = nu + nd
check('the anticommutators of one site', np.allclose(cu @ d(cu) + d(cu) @ cu, np.eye(4)) and
      np.allclose(cu @ cd + cd @ cu, 0) and np.allclose(cu @ d(cd) + d(cd) @ cu, 0), 'ok')

# the interaction n_up n_dn is the pair term of (5.2) and of the first option, and n_up - c_up^dag c_dn c_dn^dag c_up,
# which is why the spin-flip term of the second option carries a minus sign
B = cd @ cu                                               # c_dn c_up, which destroys a pair
check('n_up n_dn = c_up^dag c_dn^dag c_dn c_up', np.allclose(nu @ nd, d(cu) @ d(cd) @ cd @ cu), 'ok')
check('n_up n_dn = B^dag B with B = c_dn c_up', np.allclose(nu @ nd, d(B) @ B), 'ok')
check('n_up n_dn = n_up - c_up^dag c_dn c_dn^dag c_up, the sign of the spin-flip option',
      np.allclose(nu @ nd, nu - d(cu) @ cd @ d(cd) @ cu), 'ok')

# the decoupling of the spin-flip channel, -U <c_up^dag c_dn> c_dn^dag c_up - U c_up^dag c_dn <c_dn^dag c_up> + const,
# differs from U n_up n_dn by -U times the product of the two fluctuations, for a random complex expectation value
rng = np.random.default_rng(1)
U = 2.0
ok = True
for _ in range(3):
    s = rng.normal() + 1j * rng.normal()                  # <c_up^dag c_dn>
    S = d(cu) @ cd                                        # c_up^dag c_dn
    mf = -U * s * d(S) - U * S * np.conj(s) + U * abs(s) ** 2 * np.eye(4) + U * nu
    fluct = -U * (S - s * np.eye(4)) @ (d(S) - np.conj(s) * np.eye(4))
    ok = ok and np.allclose(U * nu @ nd, mf + fluct)
check('U n_up n_dn = the spin-flip decoupling plus -U times the product of the fluctuations', ok, 'ok')

# the pairing option is the term Delta c_up^dag c_dn^dag of (5.4), with Delta = U <c_dn c_up>
b = 0.3 - 0.2j                                            # <c_dn c_up>
mf = U * b * d(B) + U * np.conj(b) * B - U * abs(b) ** 2 * np.eye(4)
check('the pairing decoupling differs from U B^dag B by U (B - b)^dag (B - b)',
      np.allclose(U * d(B) @ B, mf + U * d(B - b * np.eye(4)) @ (B - b * np.eye(4))), 'ok')

# the first two options keep the number of electrons and the third changes it by two
opt1 = U * 0.8 * d(cd) @ cd
opt2 = -U * (0.1 + 0.2j) * d(cd) @ cu
opt3 = U * b * d(cu) @ d(cd)
comm = lambda X: np.abs(X @ N - N @ X).max()
check('[option 1, N] = 0 and [option 2, N] = 0', comm(opt1) < 1e-14 and comm(opt2) < 1e-14, (comm(opt1), comm(opt2)))
check('[N, c_up^dag c_dn^dag] = 2 c_up^dag c_dn^dag, the third option changes N by two',
      np.allclose(N @ d(cu) @ d(cd) - d(cu) @ d(cd) @ N, 2 * d(cu) @ d(cd)), 'ok')
check('the third option is Delta c_up^dag c_dn^dag of (5.4) with Delta = U <c_dn c_up>',
      np.allclose(opt3, (U * b) * d(cu) @ d(cd)), U * b)

# the counterexample of the first option, U = 2 and <n_up> = 0.8 move the spin-down level up by 1.6, and every
# eigenstate of this term has a fixed number of electrons, so <c_dn c_up> = 0
levels = np.linalg.eigvalsh(opt1)
check('U = 2 and <n_up> = 0.8 give the spin-down level 1.6', np.isclose(U * 0.8, 1.6) and np.isclose(levels.max(), 1.6),
      np.round(levels, 4))
w, v = np.linalg.eigh(opt1 + 1e-3 * N)                   # a small chemical potential splits the degenerate levels
pair = max(abs(v[:, i].conj() @ B @ v[:, i]) for i in range(4))
check('every eigenstate of the first option has <c_dn c_up> = 0', pair < 1e-15, pair)

# the second option, the spin flip, gives an in-plane moment: <c_up^dag c_dn> = <S^+> = <S_x + i S_y>
Sx = 0.5 * (d(cu) @ cd + d(cd) @ cu)
Sy = -0.5j * (d(cu) @ cd - d(cd) @ cu)
check('c_up^dag c_dn = S_x + i S_y, a moment in the xy plane', np.allclose(d(cu) @ cd, Sx + 1j * Sy), 'ok')

# the old feedback of the first option of the old quiz: the fractional quantum Hall state at the filling 1/3 has the
# charge e/3. The Laughlin state with m = 3 has the filling 1/m, and a flux quantum h/e threaded through it moves the
# charge sigma_xy h/e = (nu e^2/h)(h/e) = nu e, which is e/m, the charge of the quasihole
h, e = 6.62607015e-34, 1.602176634e-19
m = 3
nu = 1 / m
check('the Laughlin state with m = 3: the filling 1/3 and the charge nu e = e/3 moved by one flux quantum',
      np.isclose(nu, 1 / 3) and np.isclose((nu * e ** 2 / h) * (h / e), e / 3), (nu, (nu * e ** 2 / h) * (h / e) / e))
page = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'pages', 'session04',
                    '16-fractional-filling-and-the-laughlin-wavefunction.md')
text = open(page).read()
check('Section 4.16 states the filling 1/3 and the charge e/3', 'sec-4-16' in text and '$\\nu=1/3$' in text
      and '$e^*=e/3$' in text, 'session04/16')

# the third feedback of the old quiz, corrected on 2026-11-22: the fraction of an electron in a superconductor is a
# Majorana state, not the Bogoliubov quasiparticle. First route, one site: the Bogoliubov operator b = u c_up + v c_dn^dag of
# the block (5.8) with eps = 0.3 and Delta = 0.4 is a whole fermion, {b, b^dag} = 1 and b^2 = 0, a superposition of an
# electron, weight u^2 = 0.8, and a hole. A Majorana gamma = c + c^dag squares to one, so it cannot be empty or filled alone,
# and c = (gamma_A + i gamma_B)/2 takes two of them.
eps_, D_ = 0.3, 0.4
w_, v_ = np.linalg.eigh(np.array([[eps_, D_], [D_, -eps_]]))
u_, vv_ = v_[0, 1], v_[1, 1]
b = u_ * cu + vv_ * d(cd)
check('third feedback: the Bogoliubov operator of eps=0.3, Delta=0.4 is a whole fermion with electron weight u^2 = 0.8',
      np.allclose(b @ d(b) + d(b) @ b, np.eye(4)) and np.allclose(b @ b, 0) and np.isclose(u_ ** 2, 0.8), round(u_ ** 2, 6))
gA, gB = cu + d(cu), -1j * (cu - d(cu))
check('third feedback: a Majorana squares to one and two of them make c = (gA + i gB)/2',
      np.allclose(gA @ gA, np.eye(4)) and np.allclose(cu, (gA + 1j * gB) / 2), 'ok')
# second route, the mean-field Hamiltonian of the Kitaev chain at Delta=t, mu=0 on 10 sites, in the BdG basis (c, c^dag):
# two levels at zero energy, whose space holds the Nambu vector of gamma_1, with equal electron and hole parts on site 1
N = 10
hh, dd = np.zeros((N, N)), np.zeros((N, N))
for n in range(N - 1):
    hh[n, n + 1] = hh[n + 1, n] = -1.0
    dd[n + 1, n], dd[n, n + 1] = 1.0, -1.0
e_, V_ = np.linalg.eigh(np.block([[hh, dd], [dd.T, -hh]]))
Z_ = V_[:, np.abs(e_) < 1e-12]
g1v = np.r_[np.eye(N)[0], np.eye(N)[0]] / np.sqrt(2)
check('third feedback: the Kitaev chain at Delta=t, mu=0 has two zero levels, and their space holds gamma_1, half electron and half hole',
      Z_.shape[1] == 2 and np.abs(Z_ @ Z_.conj().T @ g1v - g1v).max() < 1e-12, Z_.shape[1])
print('all checks of page 01 hold')
