"""Session 6, the statements of page 02 (Sections 6.2 and 6.3) that the key box, the fold, the quizzes and the
problem make.

One site is built with Jordan-Wigner matrices. The script checks the identity U n_up n_dn = U n/2 - (2U/3) S^2 and
the value of each term on the four states, the Hartree decoupling of the densities and the splitting Um that it
gives, the field -U <S>.sigma of the decoupling with the spin-flip averages, which splits the two spins by
2U|<S>| along any direction and by U m only along z, and the factor 2/3 of the decoupling of S^2. Since 2026-11-22
the bold moment of the text is m = 2<S>, and the last block checks that the field is -(U/2) m.sigma. It checks that
the exact Hubbard energy of a Slater determinant of the site is the Hartree-Fock one and that the S^2 route gives
U/3 for one electron with spin up, where the exact value is 0, and the reading of the lab box on a toy model of
two layers, two valleys and two spins. Then the numbers of the quizzes, the spinor (1,1)/sqrt2, the pair amplitude
that changes N by two and the counterexamples at U = 4t, and the fully polarized chain with n = 0.2 electrons per
site at U = 4t of the problem, with a self-consistent loop on a k-mesh of the band -2t cos k. It needs numpy only
and writes no file."""
import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


a = np.array([[0., 1.], [0., 0.]])                        # destroys a fermion in one mode
Z = np.diag([1., -1.])
I2, I4 = np.eye(2), np.eye(4)
cu, cd = np.kron(a, I2), np.kron(Z, a)                   # one site, the modes (up, down)
d = lambda m: m.conj().T
nu, nd = d(cu) @ cu, d(cd) @ cd
n = nu + nd
Sx = 0.5 * (d(cu) @ cd + d(cd) @ cu)
Sy = 0.5 * (-1j * d(cu) @ cd + 1j * d(cd) @ cu)
Sz = 0.5 * (nu - nd)
S2 = Sx @ Sx + Sy @ Sy + Sz @ Sz

# the identity of the text and of the fold, and the value of each term on the four states
check('S^2 = (3/4)(n - 2 n_up n_dn) on one site', np.allclose(S2, 0.75 * (n - 2 * nu @ nd)), 'ok')
check('U n_up n_dn = U n/2 - (2U/3) S^2, as operators', np.allclose(nu @ nd, n / 2 - (2 / 3) * S2), 'ok')
check('n_up - n_dn = 2 S^z, so the m of (6.2) is 2<S^z>', np.allclose(nu - nd, 2 * Sz), 'ok')
idx = {'empty': 0, 'down': 1, 'up': 2, 'double': 3}       # kron basis |n_up n_dn> with a = |0><1|, 1 = occupied
vals = {}
for name, i in idx.items():
    vals[name] = (n[i, i].real, (nu @ nd)[i, i].real, S2[i, i].real)
check('n is 0, 1, 1, 2 on the empty, up, down and doubly occupied states',
      [vals[k][0] for k in ('empty', 'up', 'down', 'double')] == [0, 1, 1, 2], vals)
check('n_up n_dn is 0, 0, 0, 1 and S^2 = S(S+1) is 0, 3/4, 3/4, 0 on the same states',
      np.allclose([vals[k][1] for k in ('empty', 'up', 'down', 'double')], [0, 0, 0, 1]) and
      np.allclose([vals[k][2] for k in ('empty', 'up', 'down', 'double')], [0, 0.75, 0.75, 0]), 'ok')
U = 1.0
energy = {k: U * v[0] / 2 - (2 * U / 3) * v[2] for k, v in vals.items()}
check('of the quiz, only the doubly occupied state pays U, the singly occupied ones give U/2 - U/2 = 0',
      np.isclose(energy['double'], U) and np.isclose(energy['up'], 0) and np.isclose(energy['down'], 0)
      and np.isclose(energy['empty'], 0), energy)

# the Hartree decoupling of the densities drops only the product of the two fluctuations
rng = np.random.default_rng(3)
ok = True
for _ in range(4):
    pu, pd, Ur = rng.uniform(0, 1), rng.uniform(0, 1), rng.uniform(0.5, 5)
    mf = Ur * (pd * nu + pu * nd - pu * pd * I4)
    ok = ok and np.allclose(Ur * nu @ nd - mf, Ur * (nu - pu * I4) @ (nd - pd * I4))
check('U n_up n_dn minus the decoupling is U dn_up dn_dn, the product of the fluctuations', ok, 'ok')
# in a product state of the two modes the decoupling and U n_up n_dn have the same average, U<n_up><n_dn>, while
# the two bilinear terms alone give twice it, which is what the constant -U<n_up><n_dn> corrects
pu, pd, Ur = 0.6, 0.4, 4.0
occ_up, occ_dn = np.diag(nu).real, np.diag(nd).real
R = np.diag([(pu if ou else 1 - pu) * (pd if od else 1 - pd) for ou, od in zip(occ_up, occ_dn)])
mf = Ur * (pd * nu + pu * nd - pu * pd * I4)
check('in a product state <decoupling> = <U n_up n_dn> = U<n_up><n_dn>, and without the constant it is twice it',
      np.isclose(np.trace(R @ mf), Ur * pu * pd) and np.isclose(np.trace(R @ (Ur * nu @ nd)), Ur * pu * pd)
      and np.isclose(np.trace(R @ (mf + Ur * pu * pd * I4)), 2 * Ur * pu * pd), np.trace(R @ mf))

# the onsite energies U<n_dn> for spin up and U<n_up> for spin down, and their difference Um
U, pu, pd = 4.0, 0.6, 0.4
mf = U * (pd * nu + pu * nd - pu * pd * I4)
E_up = mf[idx['up'], idx['up']] - mf[idx['empty'], idx['empty']]
E_dn = mf[idx['down'], idx['down']] - mf[idx['empty'], idx['empty']]
m = pu - pd
check('spin up feels U<n_dn> = 1.6t and spin down U<n_up> = 2.4t for U = 4t, <n_up> = 0.6, <n_dn> = 0.4',
      np.isclose(E_up, U * pd) and np.isclose(E_dn, U * pu), (E_up, E_dn))
check('E_dn - E_up = Um = 0.8t for m = 0.2 at U = 4t', np.isclose(E_dn - E_up, U * m) and np.isclose(U * m, 0.8),
      E_dn - E_up)
check('the coefficient of sigma_z is -Um/2 = -0.4t, the sign of the conventions sheet', np.isclose((E_up - E_dn) / 2, -U * m / 2),
      (E_up - E_dn) / 2)

# the counterexamples of the decoupling quiz at U = 4t, <n_up> = 0.6, <n_dn> = 0.4
check('U<n_up><n_dn> = 0.96t is a number, it does not split the spins', np.isclose(U * pu * pd, 0.96), U * pu * pd)
check('in mean field <n_up n_dn> = <n_up><n_dn> = 0.24', np.isclose(pu * pd, 0.24), pu * pd)
wrong = U * pu * pd * n                                   # U <n_up n_dn> n, which couples to the total density
check('U<n_up n_dn> n shifts both spins by 0.96t and splits them by zero',
      np.isclose(wrong[idx['up'], idx['up']], 0.96) and np.isclose(wrong[idx['down'], idx['down']], 0.96), 'ok')

# the spinor (1,1)/sqrt2 of the quiz on m_x, one electron in the spin state (up + down)/sqrt2
vac = np.zeros(4)
vac[idx['empty']] = 1.0
psi = (d(cu) @ vac + d(cd) @ vac) / np.sqrt(2)
ev = lambda O: (psi.conj() @ O @ psi)
check('the spinor (1,1)/sqrt2 has n_up = n_dn = 1/2, so n_up - n_dn = 0',
      np.isclose(ev(nu), 0.5) and np.isclose(ev(nd), 0.5) and np.isclose(ev(nu - nd), 0), (ev(nu), ev(nd)))
check('it has <c_up^dag c_dn> = 1/2, real, so <S^x> = 1/2 and <S^y> = 0',
      np.isclose(ev(d(cu) @ cd), 0.5) and np.isclose(ev(Sx), 0.5) and np.isclose(ev(Sy), 0), (ev(d(cu) @ cd), ev(Sx)))
check('it has <c_up c_dn> = 0, since it holds one electron', np.isclose(ev(cu @ cd), 0), ev(cu @ cd))
check('[N, c_up c_dn] = -2 c_up c_dn, so the pair amplitude changes N by two',
      np.allclose(n @ (cu @ cd) - (cu @ cd) @ n, -2 * cu @ cd), 'ok')
check('S^x = (1/2)(c_up^dag c_dn + c_dn^dag c_up) is the operator of the question', np.allclose(Sx, 0.5 * (d(cu) @ cd + d(cd) @ cu)), 'ok')
ok = True
for _ in range(4):
    u = rng.normal(size=2) + 1j * rng.normal(size=2)
    u /= np.linalg.norm(u)
    phi = u[0] * d(cu) @ vac + u[1] * d(cd) @ vac
    e = lambda O: phi.conj() @ O @ phi
    ok = ok and np.isclose(e(Sx), e(d(cu) @ cd).real) and np.isclose(e(Sy), e(d(cu) @ cd).imag)
check('<S^x> is the real part of <c_up^dag c_dn> and <S^y> its imaginary part, for random spinors', ok, 'ok')

# the decoupling with the spin-flip averages, the field -U<S>.sigma in any direction, and the 2/3 of the S^2 route
sig = [np.array([[0, 1], [1, 0]]), np.array([[0, -1j], [1j, 0]]), np.diag([1., -1.])]
U = 1.0
ok_dir, splits, splits_s2, moments, dens = True, [], [], [], []
for direction in ([0, 0, 1], [1, 0, 0], [0.48, 0.6, 0.64]):
    nvec = np.array(direction) / np.linalg.norm(direction)
    # a mixed state of the site: empty 0.4, one electron along nvec 0.35, against it 0.15, doubly occupied 0.1,
    # so n = 0.7 and m = 2|<S>| = 0.2
    th, ph = np.arccos(nvec[2]), np.arctan2(nvec[1], nvec[0])
    chi = np.cos(th / 2) * d(cu) @ vac + np.exp(1j * ph) * np.sin(th / 2) * d(cd) @ vac
    chib = -np.exp(-1j * ph) * np.sin(th / 2) * d(cu) @ vac + np.cos(th / 2) * d(cd) @ vac
    dbl = d(cu) @ d(cd) @ vac
    R = (0.4 * np.outer(vac, vac) + 0.35 * np.outer(chi, chi.conj()) + 0.15 * np.outer(chib, chib.conj())
         + 0.1 * np.outer(dbl, dbl.conj()))
    tr = lambda O: np.trace(R @ O)
    S = np.array([tr(Sx), tr(Sy), tr(Sz)]).real           # <S>
    nel = tr(n).real
    moments.append((nel, 2 * np.linalg.norm(S)))
    n_up, n_dn = tr(nu).real, tr(nd).real
    dens.append(n_up - n_dn)                               # the m of (6.2)
    upd, dnu = tr(d(cu) @ cd), tr(d(cd) @ cu)              # <c_up^dag c_dn> and <c_dn^dag c_up>
    # the Hartree and Fock terms of U c_up^dag c_up c_dn^dag c_dn, h[a, b] multiplies c_a^dag c_b, basis (up, down)
    h = np.array([[U * n_dn, -U * dnu], [-U * upd, U * n_up]])
    target = U * nel / 2 * I2 - U * sum(S[k] * sig[k] for k in range(3))
    ok_dir = ok_dir and np.allclose(h, target)
    w, v = np.linalg.eigh(h)
    splits.append(w[1] - w[0])
    low = v[:, 0]                                         # the lower level is the spin along <S>
    spin_low = np.array([(low.conj() @ sig[k] @ low).real for k in range(3)])
    ok_dir = ok_dir and np.allclose(spin_low, nvec)
    h_s2 = -(2 * U / 3) * 2 * sum(S[k] * 0.5 * sig[k] for k in range(3))  # -(2U/3) 2<S>.S, with S = sigma/2
    w2 = np.linalg.eigvalsh(h_s2)
    splits_s2.append(w2[1] - w2[0])
check('the three mixed states of the site have n = 0.7 and m = 2|<S>| = 0.2', np.allclose(moments, (0.7, 0.2)), moments)
check('with the averages <c_up^dag c_dn> the field is U n/2 - U<S>.sigma, for a moment along z, x and a tilted axis, '
      'and its lower level is the spin along <S>', ok_dir, 'ok')
check('it splits the spins by 2U|<S>| = Um = 0.2U for m = 0.2 in every direction', np.allclose(splits, 0.2),
      np.round(splits, 12))
check('the decoupling of S^2, 2<S>.S - <S>^2, gives a field along <S> that splits by (2/3)Um',
      np.allclose(splits_s2, (2 / 3) * 0.2), np.round(splits_s2, 12))
# the key box: the splitting is 2U|<S>| in every direction, and it is U m with the m of (6.2) only along z
check('of the key box, along z 2|<S>| = 2<S^z> = m = 0.2 and the splitting 2U|<S>| is U m, along x the m of (6.2) '
      'is 0 while the splitting is still 0.2U', np.isclose(dens[0], 0.2) and np.isclose(moments[0][1], dens[0])
      and np.isclose(splits[0], U * dens[0])
      and np.isclose(dens[1], 0) and np.isclose(splits[1], 0.2), (np.round(dens, 12), np.round(splits, 12)))

# why the size comes from the decoupling of the densities: on a Slater determinant of the site, and on any Gaussian
# state of its two modes, the exact <U n_up n_dn> is the Hartree-Fock energy
# U(<n_up><n_dn> - |<c_up^dag c_dn>|^2) = U(n^2/4 - |<S>|^2), while the S^2 route has the energy
# U n/2 - (2U/3)|<S>|^2, which is not the energy of such a state
U = 1.0
ok = True
for _ in range(6):                                         # one electron in a random spinor, a Slater determinant
    u = rng.normal(size=2) + 1j * rng.normal(size=2)
    u /= np.linalg.norm(u)
    phi = u[0] * d(cu) @ vac + u[1] * d(cd) @ vac
    e = lambda O: phi.conj() @ O @ phi
    G = np.array([[e(d(a_) @ b_) for b_ in (cu, cd)] for a_ in (cu, cd)])
    S = np.array([e(Sx), e(Sy), e(Sz)]).real
    wick = (U * (G[0, 0] * G[1, 1] - abs(G[0, 1]) ** 2)).real
    ok = ok and np.isclose((U * e(nu @ nd)).real, wick) and np.isclose(wick, U * (e(n).real ** 2 / 4 - S @ S))
check('on six random one-electron Slater determinants of the site <U n_up n_dn> = 0 = U(<n_up><n_dn> - '
      '|<c_up^dag c_dn>|^2) = U(n^2/4 - |<S>|^2), the Hartree-Fock energy', ok, 'ok')
ok = True
for _ in range(6):
    A = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    hq = (A + A.conj().T) / 2                             # a random one-body h, rho ~ exp(-sum h_ab c_a^dag c_b)
    ops = [cu, cd]
    Hq = sum(hq[i, j] * d(ops[i]) @ ops[j] for i in range(2) for j in range(2))
    w, v = np.linalg.eigh(Hq)
    R = v @ np.diag(np.exp(-w)) @ v.conj().T
    R /= np.trace(R)
    tr = lambda O: np.trace(R @ O)
    G = np.array([[tr(d(ops[i]) @ ops[j]) for j in range(2)] for i in range(2)])   # G[a, b] = <c_a^dag c_b>
    S = np.array([tr(Sx), tr(Sy), tr(Sz)]).real
    nel = tr(n).real
    exact = (U * tr(nu @ nd)).real
    wick = (U * (G[0, 0] * G[1, 1] - abs(G[0, 1]) ** 2)).real
    ok = ok and np.isclose(exact, wick) and np.isclose(wick, U * (nel ** 2 / 4 - S @ S))
check('on six random Gaussian states exp(-h)/Z of the site, the same holds, by Wick', ok, 'ok')
one = d(cu) @ vac                                          # one electron with spin up
e1 = lambda O: (one.conj() @ O @ one).real
S1 = np.array([e1(Sx), e1(Sy), e1(Sz)])
E_exact = U * e1(nu @ nd)
E_hf = U * (e1(nu) * e1(nd) - abs(one.conj() @ d(cu) @ cd @ one) ** 2)
E_s2 = U * e1(n) / 2 - (2 * U / 3) * (S1 @ S1)
check('one electron with spin up has |<S>| = 1/2, the exact and the Hartree-Fock energy 0, and the S^2 route '
      'U/2 - (2U/3)(1/2)^2 = U/3', np.isclose(np.linalg.norm(S1), 0.5) and np.isclose(E_exact, 0)
      and np.isclose(E_hf, 0) and np.isclose(E_s2, U / 3), (E_exact, E_hf, E_s2))

# the reading of the lab box: a staggered potential V = Delta f(tau, s) l on two layers l = +-1, in two valleys
# tau = +-1 and for two spins s = +-1, with an interlayer hopping g and one electron per (tau, s). The spin of a
# layer is sum s <n_{l tau s}>. With f = s it is nonzero and alternates from layer to layer, an exchange field.
# With f = tau s it is zero on each layer.
Delta, g = 0.3, 1.0
def layer_spin(f):
    spin = {+1: 0.0, -1: 0.0}
    for tau in (+1, -1):
        for s in (+1, -1):
            V = Delta * f(tau, s)
            h2 = np.array([[V, g], [g, -V]])               # layer +1, layer -1
            w, v = np.linalg.eigh(h2)
            low = v[:, 0]
            spin[+1] += s * abs(low[0]) ** 2
            spin[-1] += s * abs(low[1]) ** 2
    return spin
sp_s, sp_ts = layer_spin(lambda tau, s: s), layer_spin(lambda tau, s: tau * s)
check('of the lab box, a potential s*l gives each layer a spin, of opposite sign on the two layers, and tau*s*l '
      'gives zero spin on each layer', abs(sp_s[+1]) > 0.1 and np.isclose(sp_s[+1], -sp_s[-1])
      and np.isclose(sp_ts[+1], 0) and np.isclose(sp_ts[-1], 0), (sp_s, sp_ts))

# the problem, the fully polarized chain with n = 0.2 electrons per site at U = 4t, band -2t cos k
t, U, nel = 1.0, 4.0, 0.2
Nk = 2000
k = 2 * np.pi * (np.arange(Nk) + 0.5) / Nk - np.pi
eps = -2 * t * np.cos(k)
EF = -2 * t * np.cos(np.pi * nel)
check('the Fermi level of a full spin-up band with n = 0.2 is -2t cos(pi n) = -1.618t', np.isclose(EF, -1.618, atol=5e-4), EF)
check('the empty spin-down band starts at -2t + Um = -1.2t, above the Fermi level', np.isclose(-2 * t + U * nel, -1.2)
      and -2 * t + U * nel > EF, -2 * t + U * nel)
pu, pd = nel, 0.0
for it in range(200):
    e_up, e_dn = eps + U * pd, eps + U * pu
    allE = np.concatenate([e_up, e_dn])
    order = np.argsort(allE)
    occ = np.zeros(2 * Nk)
    occ[order[:int(round(nel * Nk))]] = 1
    pu_new, pd_new = occ[:Nk].mean(), occ[Nk:].mean()
    if np.isclose(pu_new, pu) and np.isclose(pd_new, pd):
        break
    pu, pd = pu_new, pd_new
check('the polarized state is a fixed point of the loop, m = 0.2 and splitting Um = 0.8t', np.isclose(pu - pd, 0.2)
      and np.isclose(U * (pu - pd), 0.8) and it == 0, (pu, pd, it))
filled = np.sort(e_up)[:int(round(nel * Nk))]
check('the filled spin-up states go from -2t to the Fermi level -1.618t', np.isclose(filled.min(), -2, atol=1e-5)
      and np.isclose(filled.max(), EF, atol=5e-3), (filled.min(), filled.max()))

# corrected on 2026-11-22, Section 6.3: "Self-consistency gives m=0 for U<0, and in the half-filled chain a magnetic
# solution with m != 0 for every U>0". For U<0 the uniform energy (4t/pi)(1 - cos(pi m/2)) - U m^2/4 grows with m, and
# the right side of the gap equation 1 = (U/2)<1/E_k> of the staggered moment is negative, so only m = 0 is left. For U>0
# the gap equation has a solution at every U, 0.0299 at U = t, while a uniform moment needs the Stoner threshold of 6.6.
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'figures', 'session06'))
import _mf
mg = np.linspace(0, 1, 101)
Eunif = lambda m, U: 4 / np.pi * (1 - np.cos(np.pi * m / 2)) - U * m * m / 4
rhs = [(U / 2) * _mf.avg(lambda e, D: 1 / np.sqrt(e * e + D * D), 0.1) for U in (-1.0, -4.0)]
check('6.3: for U<0 the uniform energy grows with m and the gap equation has a negative right side, so m = 0',
      all(np.all(np.diff(Eunif(mg, U)) > 0) for U in (-1.0, -4.0)) and all(r < 0 for r in rhs), np.round(rhs, 4))
ms = [_mf.moment(U) for U in (0.5, 1.0, 2.0)]
check('6.3: in the half-filled chain the staggered moment is finite for every U>0, 0.0299 at U = t, below the uniform '
      'threshold 2 pi t', all(m > 0 for m in ms) and round(ms[1], 4) == 0.0299, np.round(ms, 5))

# picked by the lecturer on 2026-11-22, Section 6.3: the bold moment is m = 2<S>, "so that m_z is the m of (6.2)". The
# text says that the exchange field points along m, in any direction, and that m_z = 2<S^z> is the m of (6.2). For the
# three mixed states above, along z, along x and along a tilted axis, m = 2<S> has |m| = 0.2, m_z equals
# <n_up> - <n_dn>, the Hartree-Fock field is U n/2 - (U/2) m.sigma, its lower level is the spin along m, and it splits
# the two spins by U|m| = 0.2U. The S^2 route gives the same direction and (2/3) U|m|.
U = 1.0
rows = []
for direction in ([0, 0, 1], [1, 0, 0], [0.48, 0.6, 0.64]):
    nvec = np.array(direction) / np.linalg.norm(direction)
    th, ph = np.arccos(nvec[2]), np.arctan2(nvec[1], nvec[0])
    chi = np.cos(th / 2) * d(cu) @ vac + np.exp(1j * ph) * np.sin(th / 2) * d(cd) @ vac
    chib = -np.exp(-1j * ph) * np.sin(th / 2) * d(cu) @ vac + np.cos(th / 2) * d(cd) @ vac
    dbl = d(cu) @ d(cd) @ vac
    R = (0.4 * np.outer(vac, vac) + 0.35 * np.outer(chi, chi.conj()) + 0.15 * np.outer(chib, chib.conj())
         + 0.1 * np.outer(dbl, dbl.conj()))
    tr = lambda O: np.trace(R @ O)
    mb = 2 * np.array([tr(Sx), tr(Sy), tr(Sz)]).real          # the bold m of the text
    n_up, n_dn, nel = tr(nu).real, tr(nd).real, tr(n).real
    upd, dnu = tr(d(cu) @ cd), tr(d(cd) @ cu)
    h = np.array([[U * n_dn, -U * dnu], [-U * upd, U * n_up]])
    w, v = np.linalg.eigh(h)
    low = v[:, 0]
    along = np.array([(low.conj() @ sig[k] @ low).real for k in range(3)])
    w2 = np.linalg.eigvalsh(-(U / 3) * sum(mb[k] * sig[k] for k in range(3)))   # -(2U/3) 2<S>.S = -(U/3) m.sigma
    rows.append((mb, n_up - n_dn, np.allclose(h, U * nel / 2 * I2 - (U / 2) * sum(mb[k] * sig[k] for k in range(3))),
                 np.allclose(along, mb / np.linalg.norm(mb)), w[1] - w[0], w2[1] - w2[0]))
check('6.3, picked 2026-11-22: m = 2<S> has |m| = 0.2 and m_z = <n_up> - <n_dn>, 0.2 along z, 0 along x, 0.128 tilted',
      all(np.isclose(np.linalg.norm(r[0]), 0.2) and np.isclose(r[0][2], r[1]) for r in rows)
      and np.isclose(rows[0][1], 0.2) and np.isclose(rows[1][1], 0) and np.isclose(rows[2][1], 0.128),
      [(np.round(r[0], 4).tolist(), round(r[1], 4)) for r in rows])
check('6.3, picked 2026-11-22: the field is U n/2 - (U/2) m.sigma, its lower level is the spin along m, and it splits '
      'by U|m| = 0.2U in every direction, while the S^2 route splits by (2/3) U|m|',
      all(r[2] and r[3] and np.isclose(r[4], 0.2 * U) and np.isclose(r[5], 2 / 3 * 0.2 * U) for r in rows),
      [(round(r[4], 12), round(r[5], 12)) for r in rows])
print('page 02 of Session 6: all statements hold')
