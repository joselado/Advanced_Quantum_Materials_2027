"""Session 9, the numbers that page 04 (Section 9.4a) states and that no figure script asserts.

The windows of the figure occupation (k_F = pi/2, the summand about 1/t inside, zero outside) are asserted in
webnotes/figures/session09/occupation.py, and the windows and the numbers of the picture quiz (2.4/t, -0.30t and 0.30t,
-2t and -1.91t, the heights 1.7 and 2 to 2.7 of the alt texts) in webnotes/figures/session09/_g2_summand.py. This script
holds the rest, the steps fold, the first quiz and the problem. It uses numpy and one call of pyqula, which runs in a
temporary folder, and it writes no file. Since 2026-11-22, the pick of the lecturer, the page states after the key box
that the density changes by delta n(q) = -chi_0(q) v_q, with v_q = <k+q|V|k>, and the sentence before (9.4) has the
denominator eps(k) - eps(k+q) of the mixing (9.3). The second to last block asserts the sign by three routes, and the
last one asserts that with the two spins the total density changes by -2 chi_0(q) v_q.

Run it from anywhere:  python3 webnotes/checks/session09/g2_04_fermi_sea.py"""
import os
import tempfile

import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def nF(e, mu, T):
    return 0.5 * (1 - np.tanh((e - mu) / (2 * T)))


def chi0(q, mu, T, N=20000):
    """(9.4) for the chain eps = -2t cos k, t=1, on N momenta."""
    k = 2 * np.pi * np.arange(N) / N
    e1, e2 = -2 * np.cos(k), -2 * np.cos(k + q)
    f1, f2 = nF(e1, mu, T), nF(e2, mu, T)
    de = e2 - e1
    small = np.abs(de) < 1e-12
    return np.where(small, f1 * (1 - f1) / T, (f1 - f2) / np.where(small, 1, de)).mean()


# ---- the problem and the first quiz: D(E_F) = 1/(pi v_F) = 0.159/t at half filling and 0.225/t at quarter filling
for name, kF, text in (('half filling', np.pi / 2, '0.159'), ('quarter filling', np.pi / 4, '0.225')):
    vF = 2 * np.sin(kF)
    D = 1 / (np.pi * vF)
    EF = -2 * np.cos(kF)
    N = 400000
    k = 2 * np.pi * (np.arange(N) + 0.5) / N - np.pi
    n = (-2 * np.cos(k) < EF).mean()
    check(f'problem: {name}, k_F = {kF:.4f} holds the fraction {n:.4f} of the states', abs(n - kF / np.pi) < 1e-4, n)
    check(f'problem: {name}, D(E_F) = 1/(pi v_F) = {text}/t', f'{D:.3f}' == text, D)
    hist = np.abs(-2 * np.cos(k) - EF) < 1e-3
    check(f'problem: {name}, the count of states at E_F per site and per energy gives D(E_F)', abs(hist.mean() / 2e-3 - D) < 2e-3,
          hist.mean() / 2e-3)
    small_q = chi0(1e-3, EF, 0.01)
    check(f'fold: chi_0(q -> 0) = -(1/N) sum n_F\' = D(E_F) for {name} at T=0.01t', abs(small_q - D) < 2e-3, small_q)
check('problem: quarter filling has E_F = -sqrt2 t and v_F = sqrt2 t', np.isclose(-2 * np.cos(np.pi / 4), -np.sqrt(2))
      and np.isclose(2 * np.sin(np.pi / 4), np.sqrt(2)), (-2 * np.cos(np.pi / 4), 2 * np.sin(np.pi / 4)))
check('quiz 1: at half filling v_F = 2t and 1/(pi v_F) = 0.159/t', np.isclose(2 * np.sin(np.pi / 2), 2) and f'{1 / (2 * np.pi):.3f}' == '0.159',
      1 / (2 * np.pi))

# ---- the problem: h.get_dos(mode="Green", delta=1e-3) of pyqula for the spinless chain at E = 0 and E = -sqrt2, the call the page writes
from pyqula import geometry
cwd = os.getcwd()
with tempfile.TemporaryDirectory() as d:
    os.chdir(d)
    try:
        h = geometry.chain().get_hamiltonian(has_spin=False)
        (e, dos) = h.get_dos(energies=np.array([-np.sqrt(2), 0.]), mode="Green", delta=1e-3)
    finally:
        os.chdir(cwd)
check('problem: pyqula h.get_dos(mode="Green", delta=1e-3) of the spinless chain gives 0.225 at -sqrt2 and 0.159 at 0', f'{dos[0]:.3f}' == '0.225'
      and f'{dos[1]:.3f}' == '0.159', np.round(dos, 4))

# ---- the fold: b = -a*, so a filled pair does not change the density, and every term of (9.4) is positive
rng = np.random.default_rng(1)
for _ in range(5):
    vq = rng.normal() + 1j * rng.normal()
    ek, ekq = rng.uniform(-2, 2, 2)
    a = vq / (ek - ekq)
    b = np.conj(vq) / (ekq - ek)
    check('fold: b = -a*, the modulations a e^{iqx} and b* e^{iqx} of a filled pair cancel', np.isclose(b, -np.conj(a))
          and np.isclose(a + np.conj(b), 0), a + np.conj(b))
k = np.linspace(-np.pi, np.pi, 2001)
for mu, T, q in ((0., 0.02, 0.5), (-1., 0.05, 1.3), (-np.sqrt(2), 0.01, 0.3)):
    e1, e2 = -2 * np.cos(k), -2 * np.cos(k + q)
    de = e2 - e1
    ok = np.abs(de) > 1e-9
    term = (nF(e1, mu, T) - nF(e2, mu, T))[ok] / de[ok]
    check(f'fold: every term of (9.4) is positive, mu={mu:.3f}, T={T}, q={q}', term.min() >= -1e-15, term.min())

# ---- the fold: the pair sum is (9.4) in size, against the exact density of a ring with a weak cosine potential
L, mu, T, v = 400, -1.0, 0.05, 1e-5
x = np.arange(L)
ring_rows = []
for m in (20, 100, 160):
    q = 2 * np.pi * m / L
    H = np.diag(v * 2 * np.cos(q * x)) - np.eye(L, k=1) - np.eye(L, k=-1)
    H[0, -1] = H[-1, 0] = -1
    w, U = np.linalg.eigh(H)
    dens = (np.abs(U)**2 * nF(w, mu, T)).sum(axis=1)
    w0, U0 = np.linalg.eigh(H - np.diag(np.diag(H)))
    dn = dens - (np.abs(U0)**2 * nF(w0, mu, T)).sum(axis=1)
    amp = 2 * np.mean(dn * np.cos(q * x)) / (2 * v)                       # the e^{iqx} part per unit of v_q
    ref = chi0(q, mu, T, N=L)
    ring_rows.append((m, amp, ref))
    check(f'fold: |delta n_q / v_q| on a ring of {L} sites equals chi_0(q) of (9.4), q = 2 pi {m}/{L}',
          abs(abs(amp) - ref) < 1e-3 * ref, (round(abs(amp), 5), round(ref, 5)))
# ---- the paragraph before the key box. Since the pick of the lecturer of 2026-11-22 it gives the denominator
# eps(k) - eps(k+q) of the mixing (9.3), which is minus the one of (9.4). Before the pick it had eps(k+q) - eps(k), the
# point 1 of "For the lecturer". The mixing of (9.3) for |k> and |k+q> has the denominator eps(k) - eps(k+q).
# A ring of 16 sites with a flux 0.1 per bond, so that no two levels are equal, and V = lam cos(q x). Route 1, the exact
# eigenvector of H0 + V at a small lam, its component on |k+q> divided by its component on |k>. Route 2, the first
# order <k+q|V|k>/(eps(k) - eps(k+q)), with <k+q|V|k> = lam/2.
Nr, lam, phi = 16, 1e-5, 0.1
xr = np.arange(Nr)
H0r = np.zeros((Nr, Nr), complex)
H0r[xr, (xr + 1) % Nr] = -np.exp(1j * phi); H0r += H0r.conj().T
ks = 2 * np.pi * np.arange(Nr) / Nr
eps = lambda kk: -2 * np.cos(kk + phi)                                   # e^{ikx}/sqrt(N) has this energy
mq = 3
Vr = np.diag(lam * np.cos(ks[mq] * xr))
ee, vv = np.linalg.eigh(H0r + Vr)
rows = []
for mk in (1, 2, 5):
    pw = np.exp(1j * ks[mk] * xr) / np.sqrt(Nr); pwq = np.exp(1j * ks[(mk + mq) % Nr] * xr) / np.sqrt(Nr)
    j = np.argmax(np.abs(pw.conj() @ vv))
    exact = (pwq.conj() @ vv[:, j]) / (pw.conj() @ vv[:, j])
    first = (lam / 2) / (eps(ks[mk]) - eps(ks[(mk + mq) % Nr]))
    rows.append((mk, exact.real, first))
check('the sentence before (9.4): the coefficient of |k+q> in the perturbed |k> is <k+q|V|k>/(eps(k) - eps(k+q)), and not with the other order',
      all(abs(e / f - 1) < 1e-3 and abs(e.imag if hasattr(e, 'imag') else 0) < 1e-12 for m_, e, f in rows),
      [(m_, '%.4e' % e, '%.4e' % f) for m_, e, f in rows])

# ---- picked by the lecturer on 2026-11-22, after the key box: "The density then changes by delta n(q) = -chi_0(q) v_q",
# with v_q = <k+q|V|k>, so chi_A of Section 9.3 is -chi_0(q) v_q. Route 1, the exact density of the ring of 400 sites above,
# where delta n_q / v_q is negative and equal to -chi_0(q) of (9.4). Route 2, on the ring of 16 sites with the flux 0.1 per
# bond, the first-order states (9.3) taken one by one, delta n_i = sum_a f_a 2 Re[psi_a(i)* sum_b c_ba psi_b(i)] with
# c_ba = <b|V|a>/(eps_a - eps_b), against the exact density of H0 + V and against -chi_0(q) of (9.4) on the same momenta.
check('after the key box: on the ring of 400 sites delta n_q / v_q = -chi_0(q) of (9.4), negative, at q = 2 pi m/400',
      all(a < 0 and abs(a + c) < 1e-3 * c for m_, a, c in ring_rows), [(m_, round(a, 5), round(c, 5)) for m_, a, c in ring_rows])
Tr, mur = 0.05, -1.0
e0, U0r = np.linalg.eigh(H0r)
f0 = nF(e0, mur, Tr)
Vab = U0r.conj().T @ Vr @ U0r                                            # <b|V|a> in the eigenbasis of H0
den = e0[None, :] - e0[:, None]                                          # eps_a - eps_b, rows b and columns a
C = np.where(np.eye(Nr, dtype=bool), 0, Vab / np.where(np.eye(Nr, dtype=bool), 1, den))
dpsi = U0r @ C                                                           # column a is sum_b c_ba |b>
dn_first = (2 * np.real(np.conj(U0r) * dpsi) * f0[None, :]).sum(axis=1)
dn_exact = (np.abs(vv) ** 2 * nF(ee, mur, Tr)).sum(axis=1) - (np.abs(U0r) ** 2 * f0[None, :]).sum(axis=1)
vq = lam / 2
qr = ks[mq]
amp_first, amp_exact = np.mean(dn_first * np.cos(qr * xr)) / vq, np.mean(dn_exact * np.cos(qr * xr)) / vq
kk = ks
fk, fkq = nF(eps(kk), mur, Tr), nF(eps(kk + qr), mur, Tr)
chi_ring = np.mean((fk - fkq) / (eps(kk + qr) - eps(kk)))
check('after the key box: on the ring of 16 sites (9.3) state by state and the exact density give delta n_q / v_q = -chi_0(q)',
      chi_ring > 0 and abs(amp_first + chi_ring) < 1e-6 * chi_ring and abs(amp_exact + chi_ring) < 1e-3 * chi_ring
      and np.abs(np.mean(dn_first * np.sin(qr * xr))) < 1e-12 * lam,
      (round(amp_first, 6), round(amp_exact, 6), round(-chi_ring, 6)))

# ---- after the key box, added after the independent check of 2026-11-22: "Like (9.4), this counts one spin. For spinful
# electrons each spin responds in the same way, and the total density changes by -2 chi_0(q) v_q." The ring of 400 sites
# above, now with the two spins in one matrix of 2L states and the potential on both spins, at the same mu and T.
spin_rows = []
for m_, a_one, c_ in ring_rows:
    q = 2 * np.pi * m_ / L
    H1 = - np.eye(L, k=1) - np.eye(L, k=-1)
    H1[0, -1] = H1[-1, 0] = -1
    H2 = np.kron(H1, np.eye(2))                                          # site i, spin s is the state 2 i + s
    V2 = np.kron(np.diag(v * 2 * np.cos(q * x)), np.eye(2))
    w2, U2 = np.linalg.eigh(H2 + V2)
    w20, U20 = np.linalg.eigh(H2)
    dtot = ((np.abs(U2)**2 * nF(w2, mu, T)).sum(axis=1) - (np.abs(U20)**2 * nF(w20, mu, T)).sum(axis=1)).reshape(L, 2).sum(axis=1)
    amp2 = 2 * np.mean(dtot * np.cos(q * x)) / (2 * v)
    spin_rows.append((m_, amp2, c_))
check('after the key box: with the two spins the total delta n_q / v_q is -2 chi_0(q) of (9.4), on the ring of 400 sites',
      all(abs(a2 + 2 * c_) < 1e-3 * c_ for m_, a2, c_ in spin_rows), [(m_, round(a2, 5), round(-2 * c_, 5)) for m_, a2, c_ in spin_rows])
print('all checks of page 04 hold')
