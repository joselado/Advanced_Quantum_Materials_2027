"""Session 5, the statements of page 04 (Sections 5.4 and 5.5), in the order of the page.

The caption of the phonon interaction and the cobweb are asserted again here by hand, since their figure scripts
write an SVG. The caption of the gap against U and the feedback of the picture quiz are asserted by
_g1_gapbands.check on the variables of the pyqula script, which this script runs with style.run_script. It also holds
the decoupling of the steps fold, the quiz on U > 0 with the condition on the pair susceptibility g, the density and
the notebook settings of the caption, the mesh of 100 momenta at U = -0.5, the problem of one site and the one-digit
values of the try-it. pyqula runs in temporary folders, so the script writes no file. The lab box quotes 203 K,
which labsource.py checks."""
import os, sys, json, tempfile
import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'webnotes', 'figures', 'session05'))
import _g1_gapbands
from _g1_gapbands import style

# the caption of the phonon interaction, V_eff = V_c - 1/(1 - x^2) in units of 2 g^2/omega_0 with V_c = 0.5, as in
# phonon_exchange.py: V(0) = -0.5, at most -0.5 below omega_0, above V_c over omega_0, and down to V_c at high frequency
Vc = 0.5
V = lambda x: Vc - 1.0 / (1 - x ** 2)
xb, xa = np.linspace(0, 0.98, 500), np.linspace(1.02, 200, 4000)
check('V_eff(0) = -0.5, V_eff <= -0.5 below omega_0, V_eff > V_c above it and decreasing to V_c',
      abs(V(0.0) + 0.5) < 1e-12 and np.all(V(xb) <= -0.5 + 1e-12) and np.all(V(xa) > Vc)
      and np.all(np.diff(V(xa)) < 0) and abs(V(200.0) - Vc) < 1e-4, V(0.0))

# one site, the modes up and down with the Jordan-Wigner order (up, down), in the basis |n_up n_dn>
a = np.array([[0., 1.], [0., 0.]])
cu = np.kron(a, np.eye(2))
cd = np.kron(np.diag([1., -1.]), a)
d = lambda m: m.conj().T
nu, nd = d(cu) @ cu, d(cd) @ cd
B = cd @ cu                                               # c_dn c_up, which removes a pair
I4 = np.eye(4)
vac = np.array([1., 0., 0., 0.])                          # |0>, the empty site
updn = d(cu) @ d(cd) @ vac                                # |up dn> = c_up^dag c_dn^dag |0>, as the problem defines it

# the fold: the interaction of (5.2) is U B^dag B, equal to U n_up n_dn of (1.7), and the decoupling differs from it by
# U dB^dag dB, for a random complex <B>, so the only approximation is the product of the two fluctuations
check('c_up^dag c_dn^dag c_dn c_up = B^dag B = n_up n_dn', np.allclose(d(cu) @ d(cd) @ cd @ cu, d(B) @ B) and
      np.allclose(d(B) @ B, nu @ nd), 'ok')
rng = np.random.default_rng(3)
ok = True
for U in (-2.0, -0.7, 1.3):
    b = rng.normal() + 1j * rng.normal()                  # <B>
    expand = np.conj(b) * b * I4 + np.conj(b) * (B - b * I4) + (d(B) - np.conj(b) * I4) * b \
        + (d(B) - np.conj(b) * I4) @ (B - b * I4)
    ok = ok and np.allclose(d(B) @ B, expand)             # B^dag B = <B^dag><B> + <B^dag> dB + dB^dag <B> + dB^dag dB
    Delta = U * b
    mf = Delta * d(B) + np.conj(Delta) * B - abs(Delta) ** 2 / U * I4
    ok = ok and np.allclose(mf, U * b * d(B) + U * np.conj(b) * B - U * abs(b) ** 2 * I4)
    ok = ok and np.allclose(U * d(B) @ B - mf, U * (d(B) - np.conj(b) * I4) @ (B - b * I4))
check('U B^dag B = Delta B^dag + Delta^* B - |Delta|^2/U + U dB^dag dB, with Delta = U <B>', ok, 'U = -2, -0.7, 1.3')

# the caption of the gap against U: the settings of the notebook cell "Dependence on the strength of the attractive
# interaction" are filling=0.1, nk=100, mix=0.5 and mf="swave", for U = -1, -1.5 and -2
nb = json.load(open(os.path.join(ROOT, 'jupyter-notebooks', 'session5.ipynb')))
cells = nb['cells']
head = [i for i, c in enumerate(cells) if c['cell_type'] == 'markdown'
        and ''.join(c['source']).startswith('## Dependence on the strength of the attractive interaction')]
code = next(''.join(c['source']) for c in cells[head[0] + 1:] if c['cell_type'] == 'code')
check('the notebook cell runs U = -1, -1.5, -2 with filling=0.1, nk=100, mix=0.5, mf="swave"',
      len(head) == 1 and 'Us = [-1.0,-1.5,-2.0]' in code
      and 'get_mean_field_hamiltonian(U=U,filling=0.1,nk=100,mix=0.5,mf="swave")' in code, 'cell %d' % (head[0] + 1))

# the figure and the picture quiz, on the variables of the download script: 0.10, 0.22, 0.36, the ratio 3.5, the
# smallest energy |Delta|, the two branches 2|Delta| apart, the agreement with the BCS gap equation and the upward bend
dd = style.run_script('session05/g1_meanfield_swave_chain.py')
_g1_gapbands.check(dd)
D = dict(zip(dd['Us'], dd['deltas']))
check('the pyqula script gives 0.10, 0.22 and 0.36 at U = -1, -1.5 and -2, a ratio 3.5',
      [round(D[U], 2) for U in (-1.0, -1.5, -2.0)] == [0.10, 0.22, 0.36] and round(D[-2.0] / D[-1.0], 1) == 3.5,
      [round(D[U], 4) for U in (-1.0, -1.5, -2.0)])
ok = True
for U in (-1.0, -1.5, -2.0):
    e = dd['bands'][list(dd['Us']).index(U)]
    ok = ok and abs((e[:, 2].min() - e[:, 1].max()) - 2 * D[U]) < 5e-4
check('the two branches are 2|Delta| apart at U = -1, -1.5 and -2, as the feedback of the picture quiz says', ok, 'ok')

# the try-it, old text: "from about 0.1 to 0.2 and 0.4" is the same three values to one digit
check('the try-it: 0.1031, 0.2226 and 0.3606 are 0.1, 0.2 and 0.4 to one digit',
      [round(D[U], 1) for U in (-1.0, -1.5, -2.0)] == [0.1, 0.2, 0.4], [round(D[U], 1) for U in (-1.0, -1.5, -2.0)])

from pyqula.scftk.convergence import MeanFieldConvergenceError
cwd = os.getcwd()
with tempfile.TemporaryDirectory() as tmp:
    os.chdir(tmp)
    try:
        h = dd['h']                                       # the Nambu chain of the script, tij=[-1.]
        # the caption: 0.2 electrons per site, read from the eigenvectors of the solution on 2000 momenta. In the basis
        # (c_up, c_dn, c_dn^dag, -c_up^dag) the density is the weight of the states with E < 0 on the first two entries
        dens = {}
        for U in (-1.0, -1.5, -2.0):
            hk = h.get_mean_field_hamiltonian(U=U, filling=0.1, nk=100, mix=0.5, mf="swave").get_hk_gen()
            n = 0.0
            for k in (np.arange(2000) + 0.5) / 2000:
                w, v = np.linalg.eigh(hk([k, 0., 0.]))
                n += np.sum(np.abs(v[:2, w < 0]) ** 2)
            dens[U] = n / 2000
        # the caption: a mesh of 100 momenta at U = -0.5 gives 0.017, against 0.015 on a dense mesh, and at U = -0.75
        # the two agree to 1e-3, which is why the plot starts there
        vals = {U: abs(h.get_mean_field_hamiltonian(U=U, filling=0.1, nk=100, mix=0.5, mf="swave").intra[0, 2])
                for U in (-0.5, -0.75)}
        # the quiz on U > 0: with the settings of the notebook at U = +1 the loop does not converge. It sits in a
        # two-cycle, so the error after 60 and after 150 steps is the same, far above maxerror = 1e-5
        res = {}
        for mi in (60, 150):
            try:
                h.get_mean_field_hamiltonian(U=1.0, filling=0.1, nk=100, mix=0.5, mf="swave", maxite=mi)
                res[mi] = None
            except MeanFieldConvergenceError as ex:
                res[mi] = ex.scf.residual
    finally:
        os.chdir(cwd)
check('the density of the solution is 0.2 electrons per site at U = -1, -1.5 and -2, so the loop keeps it fixed',
      all(abs(n - 0.2) < 1e-4 for n in dens.values()), {U: round(n, 5) for U, n in dens.items()})
dense = {U: _g1_gapbands.bcs(U)[0] for U in vals}
check('U = -0.5: nk = 100 gives 0.017 against 0.015 of the dense gap equation, more than 5 percent apart',
      round(vals[-0.5], 3) == 0.017 and round(dense[-0.5], 3) == 0.015 and abs(vals[-0.5] - dense[-0.5]) > 0.05 * dense[-0.5],
      (round(vals[-0.5], 4), round(dense[-0.5], 4)))
check('U = -0.75: nk = 100 agrees with the dense gap equation to 1e-3', abs(vals[-0.75] - dense[-0.75]) < 1e-3,
      (round(vals[-0.75], 4), round(dense[-0.75], 4)))
check('U = +1 with filling=0.1, nk=100, mix=0.5: pyqula does not converge, the error stays the same in a two-cycle',
      res[60] is not None and res[150] is not None and res[150] > 1e-3 and abs(res[150] - res[60]) < 1e-9, res)

# the quiz on U > 0: the response of one site to a small Delta is <c_dn c_up> = -g Delta with g > 0, here at U = 0 and
# mu = 0, so Delta_new = U <c_dn c_up> = -U g Delta flips the sign for U > 0 and keeps it for U < 0
for Delta in (0.01, -0.01, 0.01j):
    H = Delta * d(B) + np.conj(Delta) * B
    w, v = np.linalg.eigh(H)
    gs = v[:, 0]
    g = -(gs.conj() @ B @ gs) / Delta
    assert abs(g.imag) < 1e-12 and g.real > 0
check('the sign of the response: <c_dn c_up> = -g Delta with g > 0 on one site, for Delta = 0.01, -0.01 and 0.01i',
      True, round(g.real, 4))
# the answer: a finite Delta is never self-consistent for U > 0. On the chain -2 cos k the self-consistency
# Delta = U <c_dn c_up> = -U Delta (1/N) sum_k 1/(2 E_k) needs 1 + U (1/N) sum_k 1/(2 E_k) = 0, which has no root for
# U > 0 at any Delta and any mu, and has one for U < 0
k = 2 * np.pi * (np.arange(4000) + 0.5) / 4000
eps = -2 * np.cos(k)
lhs = lambda U, D, mu: 1 + U * np.mean(1 / (2 * np.sqrt((eps - mu) ** 2 + D ** 2)))
grid = [(D, mu) for D in np.geomspace(1e-4, 3, 40) for mu in np.linspace(-3, 3, 25)]
check('U = +1: 1 + U (1/N) sum 1/(2E) > 1 for every Delta and mu, so no finite Delta is self-consistent',
      min(lhs(1.0, D, mu) for D, mu in grid) > 1, round(min(lhs(1.0, D, mu) for D, mu in grid), 4))
check('U = -1, mu = -1.89: 1 + U (1/N) sum 1/(2E) changes sign between Delta = 0.01 and 1, so a root exists',
      lhs(-1.0, 0.01, -1.89) < 0 < lhs(-1.0, 1.0, -1.89), (round(lhs(-1.0, 0.01, -1.89), 3), round(lhs(-1.0, 1.0, -1.89), 3)))


# the condition of the quiz. The pair susceptibility g(Delta) = (1/N) sum_k tanh(E_k/2T)/(2 E_k) of the chain at 0.2
# electrons per site, mu = -2 cos(0.1 pi), on N momenta, shifted off k = 0 or plain
def gsus(D, T=0.0, N=4000, shifted=True):
    kk = 2 * np.pi * (np.arange(N) + (0.5 if shifted else 0.0)) / N
    E = np.sqrt((-2 * np.cos(kk) + 2 * np.cos(0.1 * np.pi)) ** 2 + D ** 2)
    return np.mean((np.tanh(E / (2 * T)) if T > 0 else 1.0) / (2 * E))


gs0 = [gsus(D) for D in (0.1, 0.01, 1e-3)]
check('a metal at T = 0: g grows as Delta goes to zero, 1.02, 2.23 and 3.42 at Delta = 0.1, 0.01 and 0.001',
      gs0[0] < gs0[1] < gs0[2], np.round(gs0, 3))
# the plain loop Delta -> -U g(Delta) Delta at U = +1 and T = 0, from Delta = 0.01, jumps between +Delta and -Delta
# and does not go to zero, on the dense mesh and on the plain mesh of 100 momenta, with no mixing and with mix = 0.5
ok, ends = True, []
for mix in (0.0, 0.5):
    for N, sh in ((4000, True), (100, False)):
        Dl, seq = 0.01, []
        for _ in range(400):
            Dl = mix * Dl + (1 - mix) * (-1.0 * gsus(Dl, N=N, shifted=sh) * Dl)
            seq.append(Dl)
        ok = ok and abs(seq[-1]) > 1e-3 and np.sign(seq[-1]) == -np.sign(seq[-2]) and np.isclose(abs(seq[-1]), abs(seq[-3]))
        ends.append(round(abs(seq[-1]), 4))
check('T = 0, U = +1: the plain loop ends in a two-cycle +-Delta and not at zero', ok, ends)
# at a finite temperature T = 0.1 the susceptibility stays finite near Delta = 0, so Ug = 0.5 is a real case. The
# loop from a small guess flips the sign and halves it, 1, -0.5, 0.25, which is the cobweb, and it goes to zero
gT = gsus(1e-6, T=0.1)
UT = 0.5 / gT
Dl, seq = 1e-3, [1e-3]
for _ in range(6):
    Dl = -UT * gsus(Dl, T=0.1) * Dl
    seq.append(Dl)
r = np.array(seq) / seq[0]
check('T = 0.1: g is finite near Delta = 0, and U g = 0.5 gives 1, -0.5, 0.25 and a loop that goes to zero',
      abs(gsus(1e-3, T=0.1) - gT) < 1e-4 and np.allclose(r[:3], [1, -0.5, 0.25], atol=1e-4) and abs(r[-1]) < 0.02,
      (round(gT, 4), np.round(r[:3], 4)))
# the same finite g with Ug = 1.5 makes the guess grow, so the condition Ug < 1 of the question is needed
Dl = -(1.5 / gT) * gsus(1e-3, T=0.1) * 1e-3
check('T = 0.1 and U g = 1.5: one step multiplies a small guess by -1.5, so the loop needs U g < 1',
      np.isclose(Dl / 1e-3, -1.5, atol=1e-4), round(Dl / 1e-3, 4))
# the cobweb, Delta_new = -0.5 Delta from Delta_0 = 1: 1, -0.5, 0.25, as in pairing_cobweb.py
f = lambda x: -0.5 * x
check('the cobweb: 1, -0.5, 0.25', f(1.0) == -0.5 and f(f(1.0)) == 0.25, (1.0, f(1.0), f(f(1.0))))

# the counterexample of the first option: one site with U = +t and mu = 0 has the energies 0, 0, 0 and t, and every
# ground state has <c_dn c_up> = 0, also a superposition of the three degenerate states
H = 1.0 * nu @ nd
E = np.linalg.eigvalsh(H)
check('U = +t, mu = 0: the empty and singly occupied states at 0, the doubly occupied at +t', np.allclose(E, [0, 0, 0, 1]),
      E)
ground = [0, 1, 2]                                        # |00>, |01>, |10>, the states with E = 0 in this basis
check('the energies 0 are |0>, |dn> and |up>, the energy t is |up dn>', np.allclose(np.diag(H), [0, 0, 0, 1]), np.diag(H))
Bg = B[np.ix_(ground, ground)]
check('<c_dn c_up> vanishes on the whole ground space', np.abs(Bg).max() < 1e-15, np.abs(Bg).max())

# the problem: one site with U = -2t, mu = U/2 = -t, the empty and doubly occupied states at 0 and the singly occupied
# ones at t. A small pairing Delta = |Delta| e^{i phi} gives the ground state (|0> - e^{i phi} |up dn>)/sqrt 2 at -|Delta|,
# with |up dn> = c_up^dag c_dn^dag |0>, so the minus sign for Delta > 0 and the plus sign for Delta < 0, and
# |<c_dn c_up>| = 1/2
U, mu = -2.0, -1.0
H = U * nu @ nd - mu * (nu + nd)
check('U = -2t: E_0 = 0, E_up = E_dn = -mu = t, E_updn = U - 2 mu = 0 at mu = U/2 = -t',
      np.allclose(np.diag(H), [0, 1, 1, 0]) and np.isclose(U / 2, mu), np.diag(H))
for Delta in (1e-3, 0.02, -0.02, 0.01 * np.exp(0.7j), 0.02 * np.exp(-2.1j)):
    w, v = np.linalg.eigh(H + Delta * d(B) + np.conj(Delta) * B)
    gs = v[:, 0]
    target = (vac - np.exp(1j * np.angle(Delta)) * updn) / np.sqrt(2)
    pair = gs.conj() @ B @ gs
    assert np.isclose(abs(gs.conj() @ target), 1.0) and np.isclose(abs(pair), 0.5) and np.isclose(w[0], -abs(Delta))
    assert w[1] - w[0] > abs(Delta)                       # the ground state is not degenerate
check('a small pairing gives (|0> - e^{i phi} |up dn>)/sqrt 2 at -|Delta| with |<c_dn c_up>| = 1/2', True,
      'Delta = 0.001, 0.02, -0.02, 0.01 e^{0.7i}, 0.02 e^{-2.1i}')
check('for a real Delta the sign is minus for Delta > 0 and plus for Delta < 0',
      np.isclose(np.exp(1j * np.angle(0.02)), 1) and np.isclose(np.exp(1j * np.angle(-0.02)), -1), 'ok')
