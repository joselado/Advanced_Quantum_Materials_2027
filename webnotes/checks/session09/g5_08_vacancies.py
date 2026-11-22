"""Session 9, the numbers that page 08 (Section 9.8, vacancies in topological matter) states and that no figure script
asserts.

The caption of vacancy_dos (the gaps 1.56t, the level at E=0 with 45 percent on the three neighbors, the empty gap of the
trivial insulator, the vacancy on the site with +M) is asserted in webnotes/figures/session09/vacancy_dos.py, and the facts of
each picture of the quiz in g5_quiz_vacancy_*.py, both on the output of the pyqula script g5_vacancy_honeycomb.py. This script
runs the same pyqula script, and it adds the Chern numbers of the three models from the link variables of physcheck, the
infinite lattice of the third model, the first two quizzes, and the problem. The Green's function of the Haldane model is
written again here from webnotes/checks/session09/conventions.py, with the mass +M on the sublattice A.

The third option of the second quiz said that t2=0.1t, phi=pi/2 and M=0.5t give a vacancy state at -0.016t. The
conventions sheet contradicts it, and since 2026-11-22 the feedback says that this vacancy gives no level separated from the
band edges. Here the gap 0.04t of that option is asserted, and also the value of G_AA at -0.016t, which is not zero, as a
record of the old text. The caption of Figure 9.4 no longer says "if and only if" or "The rule is as direct as it looks".
The two conditions written next to it are checked here: the opener (close to the closing of the gap no separate peak, the
model t2=0.1t and M=0.5t with C=1 and no zero of G_AA or G_BB away from the edges) and the key box (a vacancy in the SSH
ring gives a level at zero in both orders of the hoppings). The italic rule of the key box is point 4 of "For the
lecturer" in the plan of the session. So is the condition of the second quiz on the neighbor joined to the vacancy by the
strong bond, and its third feedback, the trivial insulator with M=0.78t and no level in its large gap.

Run it from anywhere:  python3 webnotes/checks/session09/g5_08_vacancies.py"""
import os, sys, tempfile
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures'))
import physcheck as pc
import style


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


D1 = np.array([[1, 0], [-0.5, np.sqrt(3) / 2], [-0.5, -np.sqrt(3) / 2]])      # A to B, bond length 1
NNN = np.array([D1[1] - D1[2], D1[2] - D1[0], D1[0] - D1[1]])                  # second neighbors, one turn
BH = 2 * np.pi * np.linalg.inv(np.array([D1[0] - D1[1], D1[0] - D1[2]])).T


def blocks(u1, u2, t2, M, phi=np.pi / 2):
    """h_AA, h_BB and h_AB of the Haldane model with the mass +M on A, at the reduced momenta u1, u2."""
    kx, ky = u1 * BH[0, 0] + u2 * BH[1, 0], u1 * BH[0, 1] + u2 * BH[1, 1]
    f = -sum(np.exp(1j * (kx * d[0] + ky * d[1])) for d in D1)
    haa = M + 2 * t2 * sum(np.cos(kx * v[0] + ky * v[1] + phi) for v in NNN)
    hbb = -M + 2 * t2 * sum(np.cos(kx * v[0] + ky * v[1] - phi) for v in NNN)
    return haa, hbb, f


def green(E, t2, M, sub=0, nk=600):
    """G_AA(E) (sub=0) or G_BB(E) (sub=1) of the infinite lattice at a real E in the gap. A vacancy on that sublattice
    binds a state where it vanishes."""
    u = (np.arange(nk) + 0.5) / nk
    U1, U2 = np.meshgrid(u, u, indexing='ij')
    haa, hbb, f = blocks(U1, U2, t2, M)
    num = (E - hbb) if sub == 0 else (E - haa)
    return float(np.mean(num / ((E - haa) * (E - hbb) - np.abs(f) ** 2)))


def edges(t2, M, nk=300):
    """The edges of the gap at half filling, on a mesh that holds K and K'."""
    u = np.arange(nk) / nk
    U1, U2 = np.meshgrid(u, u, indexing='ij')
    haa, hbb, f = blocks(U1, U2, t2, M)
    avg, dif = (haa + hbb) / 2, np.sqrt(((haa - hbb) / 2) ** 2 + np.abs(f) ** 2)
    return float((avg - dif).max()), float((avg + dif).min())


# ---- the recall box, the picture quiz: the Chern numbers of the three models of the pyqula script
d = style.run_script('session09/g5_vacancy_honeycomb.py')
cwd = os.getcwd()
with tempfile.TemporaryDirectory() as tmp:
    os.chdir(tmp)
    try:
        from pyqula import geometry, algebra
        C, nbrs = {}, {}
        for name, (x, M) in d['models'].items():
            h = geometry.honeycomb_lattice().get_hamiltonian(has_spin=False)
            h.add_haldane(x)
            h.add_sublattice_imbalance(M)
            hk, B = pc.from_pyqula(h)
            C[name] = pc.chern_links(hk, B, bands=0, nk=60)
            # the neighbors that the script picks on the torus, with the same test, for each model
            ht = d['g'].get_hamiltonian(has_spin=False)
            ht.add_haldane(x)
            ht.add_sublattice_imbalance(M)
            Ht = algebra.todense(ht.get_hk_gen()([0., 0., 0.]))
            nbrs[name] = np.where((np.abs(np.abs(Ht[d['v']]) - 1.) < 1e-9) & (np.arange(len(Ht)) != d['v']))[0]
        # the opener: the Haldane model with t2 = 0.1t (add_haldane(0.2/sqrt 3)) and M = 0.5t, close to the transition
        hs = geometry.honeycomb_lattice().get_hamiltonian(has_spin=False)
        hs.add_haldane(0.2 / np.sqrt(3))
        hs.add_sublattice_imbalance(0.5)
        hk, B = pc.from_pyqula(hs)
        C_small = pc.chern_links(hk, B, bands=0, nk=120)
        gap_small = pc.gap(hk, B, nfilled=1, nk=60, points=[(B[0] + B[1]) / 3, 2 * (B[0] + B[1]) / 3])
    finally:
        os.chdir(cwd)
r = d['g'].r
check('figures: for each model the script sums the LDOS on three sites at the distance 1 from the vacancy, never on the vacancy',
      all(len(n) == 3 and d['v'] not in n and np.allclose(np.linalg.norm(r[n] - r[d['v']], axis=1), 1.0) for n in nbrs.values()),
      {k: n.tolist() for k, n in nbrs.items()})
check('picture quiz: C = 1 for t2 = 0.15t, 0 for M = 0.78t, 0 for t2 = 0.15t with M = 1.0t',
      abs(C['chern'] - 1) < 1e-6 and abs(C['trivial']) < 1e-6 and abs(C['both']) < 1e-6, {k: round(v, 6) for k, v in C.items()})
x, M = d['models']['chern']
check('picture quiz: add_haldane(0.3/sqrt 3) is t2 = 0.15t, 3 sqrt(3) t2 = 0.78t, and M = 1.0t is above it',
      abs(np.sqrt(3) / 2 * x - 0.15) < 1e-12 and abs(round(3 * np.sqrt(3) * 0.15, 2) - 0.78) < 1e-12 and d['models']['both'][1] == 1.0,
      round(3 * np.sqrt(3) * 0.15, 4))
g = d['gaps']
check('picture quiz: the gaps of the torus are 1.56t, 1.56t and 0.44t',
      abs(round(g['chern'], 2) - 1.56) < 1e-12 and abs(round(g['trivial'], 2) - 1.56) < 1e-12 and abs(round(g['both'], 2) - 0.44) < 1e-12,
      {k: round(v, 4) for k, v in g.items()})
inside = {k: [(round(float(e), 6), round(float(w), 4)) for e, w in zip(d['levels'][k], d['weights'][k]) if abs(e) < g[k] / 2 - 1e-3]
          for k in g}
check('picture quiz: one level at E=0 with 0.45 on the neighbors for C=1, none in the gap for the two others',
      len(inside['chern']) == 1 and abs(inside['chern'][0][0]) < 1e-6 and abs(inside['chern'][0][1] - 0.45) < 0.005
      and not inside['trivial'] and not inside['both'], inside)
# the third model in the infinite lattice: G_AA keeps its sign over the gap, so the vacancy on the site with +M binds no level
lo, hi = edges(0.15, 1.0)
scan = np.array([green(E, 0.15, 1.0, sub=0) for E in np.linspace(lo + 1e-3, hi - 1e-3, 41)])
check('picture quiz: t2 = 0.15t, M = 1.0t, gap edges of the infinite lattice and G_AA over the gap, with no zero',
      abs(hi - lo - 0.4412) < 2e-4 and (np.all(scan < 0) or np.all(scan > 0)), (round(lo, 4), round(hi, 4), round(scan.min(), 3), round(scan.max(), 3)))

# ---- the first quiz: t2 = 0.1t, M = 0.3t
lo, hi = edges(0.1, 0.3)
zA = brentq(lambda E: green(E, 0.1, 0.3, sub=0), lo + 1e-4, hi - 1e-4, xtol=1e-7)
zB = brentq(lambda E: green(E, 0.1, 0.3, sub=1), lo + 1e-4, hi - 1e-4, xtol=1e-7)
check('quiz 1: gap edges +-0.22t, a vacancy on the site with +M binds a state at -0.14t, on the other sublattice at +0.14t',
      abs(lo + 0.2196) < 2e-4 and abs(hi - 0.2196) < 2e-4 and abs(round(zA, 2) + 0.14) < 1e-12 and abs(zB + zA) < 1e-3,
      (round(lo, 4), round(hi, 4), round(zA, 4), round(zB, 4)))

# ---- the second quiz: a vacancy in the topological SSH ring, and the onsite energy 2t on the neighbor
Ns = 80
hop = np.array([0.5 if i % 2 == 0 else 1.0 for i in range(Ns)])        # the topological order, weak bond after site 0
H = np.zeros((Ns, Ns))
for i in range(Ns):
    H[i, (i + 1) % Ns] = H[(i + 1) % Ns, i] = hop[i]
Hv = H[1:, 1:]                                                          # site 0 removed
e = np.linalg.eigvalsh(Hv)
strong = Ns - 2                                                         # the neighbor joined to site 0 by the bond 1.0
Hp = Hv.copy(); Hp[strong, strong] += 2.0
ep = np.linalg.eigvalsh(Hp)
check('quiz 2: the vacancy leaves a level at zero, and 2t on the neighbor joined by the strong bond leaves the gap +-0.5t empty',
      np.min(np.abs(e)) < 1e-12 and not np.any(np.abs(ep) < 0.5 - 1e-3), (np.min(np.abs(e)), np.round(np.sort(np.abs(ep))[:2], 4).tolist()))
check('quiz 2: the onsite energy 2t on the other neighbor, joined to the vacancy by the weak bond, keeps the level at zero',
      np.min(np.abs(np.linalg.eigvalsh(Hv + np.diag(2.0 * (np.arange(Ns - 1) == 0))))) < 1e-12,
      np.min(np.abs(np.linalg.eigvalsh(Hv + np.diag(2.0 * (np.arange(Ns - 1) == 0))))))
# the key box: a vacancy in the trivial SSH ring, with the strong bond after site 0, also leaves a level at zero, since the
# open chain that is left has 79 sites, one more on one sublattice, and the clean ring has the gap +-0.5t in both orders
zero = {}
for first in (0.5, 1.0):
    hop2 = np.array([first if i % 2 == 0 else 1.5 - first for i in range(Ns)])
    H2 = np.zeros((Ns, Ns))
    for i in range(Ns):
        H2[i, (i + 1) % Ns] = H2[(i + 1) % Ns, i] = hop2[i]
    zero[first] = (np.min(np.abs(np.linalg.eigvalsh(H2[1:, 1:]))), np.min(np.abs(np.linalg.eigvalsh(H2))))
check('key box: a vacancy in the SSH ring leaves a level at zero in the topological and in the trivial order of the hoppings',
      all(z < 1e-12 and abs(g0 - 0.5) < 1e-9 for z, g0 in zero.values()), zero)
lo, hi = edges(0.1, 0.5)
check('quiz 2: t2 = 0.1t, M = 0.5t has a gap of 0.04t', abs(round(hi - lo, 2) - 0.04) < 1e-12, round(hi - lo, 4))
gA = green(-0.016, 0.1, 0.5, sub=0, nk=1200)
check('quiz 2, the old feedback: G_AA(-0.016t) of that model is -0.197 and not zero, so the state at -0.016t of the old text is not there',
      abs(gA + 0.197) < 0.002, round(gA, 4))
# the opener: close to the transition the bound state is not a separate peak. For t2 = 0.1t and M = 0.5t the Chern number
# is still 1 and the gap is 0.039t, and neither G_AA nor G_BB changes sign from 1e-3 t inside one edge to 1e-3 t inside the other
Es = np.linspace(lo + 1e-3, hi - 1e-3, 11)
sA = np.array([green(E, 0.1, 0.5, sub=0) for E in Es])
sB = np.array([green(E, 0.1, 0.5, sub=1) for E in Es])
check('opener: t2 = 0.1t, M = 0.5t has C = 1 and the gap 0.039t, and a vacancy on either sublattice gives no zero of G away from the edges',
      abs(C_small - 1) < 1e-6 and abs(gap_small - (hi - lo)) < 1e-4 and abs(round(gap_small, 3) - 0.039) < 1e-12
      and np.all(sA < 0) and np.all(sB > 0), (round(C_small, 6), round(gap_small, 4), round(sA.min(), 3), round(sA.max(), 3), round(sB.min(), 3), round(sB.max(), 3)))

# quiz 2, the right option and the third feedback: with C = 1 and the gap 0.04t, a vacancy on either sublattice gives no
# level separated from the band edges, which the opener calls a state too close to a band edge to be seen. Second
# route, a k-mesh twice as fine at five energies of the gap, with the same signs.
Es2 = np.linspace(lo + 1e-3, hi - 1e-3, 5)
sA2 = np.array([green(E, 0.1, 0.5, sub=0, nk=1200) for E in Es2])
sB2 = np.array([green(E, 0.1, 0.5, sub=1, nk=1200) for E in Es2])
check('quiz 2: C = 1, the gap 0.04t, and no zero of G_AA or G_BB in the gap away from its edges, on two k-meshes',
      abs(C_small - 1) < 1e-6 and abs(round(hi - lo, 2) - 0.04) < 1e-12 and np.all(sA < 0) and np.all(sB > 0)
      and np.all(sA2 < 0) and np.all(sB2 > 0) and np.allclose(sA2, [green(E, 0.1, 0.5, sub=0) for E in Es2], atol=0.01),
      (np.round(sA2, 3).tolist(), np.round(sB2, 3).tolist()))
# quiz 2, the third feedback: a small gap is not the only reason. The trivial insulator with t2 = 0 and M = 0.78t has
# C = 0 and the large gap 1.56t, and its vacancy leaves no level inside the gap. Route 1, the 18 x 18 torus of the pyqula
# script of the picture quiz. Route 2, G_AA of the infinite lattice keeps its sign over the gap, so the vacancy on the
# site with +M binds no level there.
lo78, hi78 = edges(0.0, 0.78)
s78 = np.array([green(E, 0.0, 0.78, sub=0) for E in np.linspace(lo78 + 1e-3, hi78 - 1e-3, 21)])
check('quiz 2, third feedback: t2 = 0 and M = 0.78t has C = 0 and the gap 1.56t, and its vacancy leaves no level inside it, '
      'on the torus and in the infinite lattice', abs(C['trivial']) < 1e-6 and abs(round(g['trivial'], 2) - 1.56) < 1e-12
      and not inside['trivial'] and abs(hi78 - lo78 - 1.56) < 1e-4 and (np.all(s78 < 0) or np.all(s78 > 0)),
      (round(C['trivial'], 6), round(g['trivial'], 4), inside['trivial'], round(s78.min(), 3), round(s78.max(), 3)))

# ---- the problem: the gap 6 sqrt(3) t2 for t2 < 1/(3 sqrt 3), and the mass with the same gap
for t2, holds in ((0.15, True), (0.19, True), (0.2, False), (0.25, False)):
    lo, hi = edges(t2, 0.0, nk=600)
    check(f'problem: the gap of the Haldane model at t2 = {t2}t is 6 sqrt(3) t2: {holds}',
          (abs(hi - lo - 6 * np.sqrt(3) * t2) < 1e-4) == holds, round(hi - lo, 4))
check('problem: 1/(3 sqrt 3) = 0.19, 6 sqrt(3) x 0.15 = 1.56 and M = 3 sqrt(3) x 0.15 = 0.78',
      abs(round(1 / (3 * np.sqrt(3)), 2) - 0.19) < 1e-12 and abs(round(6 * np.sqrt(3) * 0.15, 2) - 1.56) < 1e-12
      and abs(round(3 * np.sqrt(3) * 0.15, 2) - 0.78) < 1e-12, round(6 * np.sqrt(3) * 0.15, 4))
lo, hi = edges(0.0, 0.78)
check('problem: a sublattice mass M = 0.78t alone has the gap 2M = 1.56t', abs(hi - lo - 1.56) < 1e-4, round(hi - lo, 4))
print('all checks of page 08 hold')
