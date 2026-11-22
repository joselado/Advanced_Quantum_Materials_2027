"""Session 6, the statements and numbers of page 16 (Section 6.16, topological magnons). One check script per page is the rule.

The numbers that the two figures draw are asserted in figures/session06/dm_honeycomb.py, ribbon_magnons.py and the three
g5_quiz_ribbon_*.py, on the data of the pyqula scripts scripts/session06/g5_magnon_honeycomb.py and g5_magnon_ribbon.py. This
script checks what the text, the fold, the key box, the lab box, the quizzes and the problem state:

- the identity z.(S_i x S_j) = (i/2)(S_i^+ S_j^- - S_i^- S_j^+) as an operator, and the sign of the fold, on the exact spins 1/2 of
  a hexagon: with D sum nu_ij z.(S_i x S_j), nu_ij = +1 when the path from i to j turns left, a magnon that hops counterclockwise
  gets the amplitude +i D S with the moments along +z and -i D S with the moments along -z, and the Heisenberg part gives the
  hopping -|J|S and the onsite energy z|J|S;
- the zero at Gamma of the solution and of the caption: the Heisenberg part commutes with S^x_tot, the Dzyaloshinskii-Moriya part
  does not and commutes with S^z_tot, and the uniform magnon is still an exact eigenstate with zero energy;
- that the lattice built with this rule, the phases of panel (a) of dm_honeycomb, has C = -1 and +1 for the two bands, the same as
  pyqula with add_haldane(-2 DS/sqrt(3)), and that add_haldane(x) is the hopping sqrt(3) x/2, so DS = 0.1 is x = -0.1155;
- the Bloch matrix of the solution as it is printed, with -|J|S f* above the diagonal and m(k) = -2 DS sum sin(k.b_n): its
  diagonal at K is 3|J|S + m(K) with m(K) = -3 sqrt(3) DS, it has C = -1 for the lower band, like the lattice of the fold, and its
  bands are those of pyqula;
- the gap at K, 6 sqrt(3) DS = 1.04 for DS = 0.1, from 2.48 to 3.52, with the first-neighbor term zero there and the second-neighbor
  term -+3 sqrt(3) DS on the two sublattices, the vectors b_n with K.b_n = 2 pi/3 modulo 2 pi, the bands 0 and 6 at Gamma, that
  6 sqrt(3) DS is the smallest gap of the two bands only for DS < 1/(3 sqrt(3)) = 0.19, that the smallest gap is 2|J|S at M from
  there to DS = 1/sqrt(3) = 0.58, and that above 0.58 the lower band is below zero at K;
- that the gap is the same for DS and -DS, while C changes sign;
- the ribbon: one branch per edge crosses the gap, with opposite slopes, reversed with DS, also with the onsite energy 2|J|S on the
  sites of the edge, which have two neighbors while the others have three; the flat branch of the plain magnet at 3|J|S is on the
  two zigzag edges; the onsite energy 2M on one sublattice gives C = 0 with the gap 2M = 1.04;
- the conversion of the lab box, DS = 4 meV / (6 sqrt(3)) = 0.4 meV.

Not asserted: the feedback "Reversing the vector is a mirror operation" of the second quiz and the "bosonic Bogoliubov Hamiltonian"
of the text, which are open for the lecturer, and the sentence "the phase +pi/2 gives C=+1" of the third option of the second
quiz, whose sign depends on which hops carry the phase. The script prints C for the two readings. It writes no file, since pyqula
runs in a temporary folder.

Run it from anywhere:  python3 webnotes/checks/session06/g5_16_topological_magnons.py"""
import os
import sys
import tempfile
from functools import reduce

import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures', 'session06'))
import physcheck as pc  # noqa: E402
import _haldane as hd  # noqa: E402


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


os.chdir(tempfile.mkdtemp())
from pyqula import geometry  # noqa: E402

# ---------------------------------------------------------------- the fold, on exact spins 1/2 of a hexagon
sx = np.array([[0, 0.5], [0.5, 0]], complex); sy = np.array([[0, -0.5j], [0.5j, 0]]); sz = np.diag([0.5, -0.5]).astype(complex)
sp, sm = sx + 1j * sy, sx - 1j * sy
N = 6


def op(o, i):
    return reduce(np.kron, [o if j == i else np.eye(2) for j in range(N)])


S = {(c, i): op(m, i) for c, m in (('x', sx), ('y', sy), ('z', sz), ('+', sp), ('-', sm)) for i in range(N)}
cross = lambda i, j: S['x', i] @ S['y', j] - S['y', i] @ S['x', j]
ident = max(np.abs(cross(i, j) - 0.5j * (S['+', i] @ S['-', j] - S['-', i] @ S['+', j])).max() for i in range(N) for j in range(N) if i != j)
check('z.(S_i x S_j) = (i/2)(S_i^+ S_j^- - S_i^- S_j^+), as an operator', ident < 1e-14, '%.1e' % ident)

pos = np.array([[np.cos(np.pi / 2 + n * np.pi / 3), np.sin(np.pi / 2 + n * np.pi / 3)] for n in range(N)])   # counterclockwise
J, D, Sv = -1.0, 0.3, 0.5
H = sum(J * (S['x', i] @ S['x', (i + 1) % N] + S['y', i] @ S['y', (i + 1) % N] + S['z', i] @ S['z', (i + 1) % N]) for i in range(N))
for i in range(N):
    for j in ((i + 2) % N, (i - 2) % N):
        k = (i + 1) % N if j == (i + 2) % N else (i - 1) % N            # the common neighbor
        d1, d2 = pos[k] - pos[i], pos[j] - pos[k]
        nu = np.sign(d1[0] * d2[1] - d1[1] * d2[0])                       # +1 when the path i -> k -> j turns left
        H = H + 0.5 * D * nu * cross(i, j)                               # each pair once, from the two orders
up = np.zeros(2 ** N); up[0] = 1                                          # all spins up, the state |0...0>
flip = [S['-', i] @ up for i in range(N)]                                 # one magnon on site i
M1 = np.array([[flip[a] @ H @ flip[b] for b in range(N)] for a in range(N)])
E0 = up @ H @ up
leak = max(np.linalg.norm(H @ flip[b] - sum(M1[a, b] * flip[a] for a in range(N))) for b in range(N))
ccw = M1[2, 0]                                                            # the hop from site 0 to site 2, counterclockwise
cw = M1[0, 2]
first = M1[1, 0]
onsite = M1[0, 0] - E0
check('a ccw hop gets +i D S for D>0, a cw hop -i D S',
      leak < 1e-12 and abs(ccw - 1j * D * Sv) < 1e-12 and abs(cw + 1j * D * Sv) < 1e-12,
      'ccw %s, cw %s, D S = %.2f' % (np.round(ccw, 12), np.round(cw, 12), D * Sv))
check('the Heisenberg part gives the hopping -|J|S and the onsite energy z|J|S, z = 2 on the ring',
      abs(first + abs(J) * Sv) < 1e-12 and abs(onsite - 2 * abs(J) * Sv) < 1e-12, 'hopping %.3f, onsite %.3f' % (first.real, onsite.real))
down = np.zeros(2 ** N); down[-1] = 1                                     # all spins down, the moments along -z
flipd = [S['+', i] @ down for i in range(N)]                              # one magnon on site i is now S^+
M1d = np.array([[flipd[a] @ H @ flipd[b] for b in range(N)] for a in range(N)])
leakd = max(np.linalg.norm(H @ flipd[b] - sum(M1d[a, b] * flipd[a] for a in range(N))) for b in range(N))
check('with the moments along -z a ccw hop gets -i D S, so every second-neighbor amplitude changes sign',
      leakd < 1e-12 and abs(M1d[2, 0] + 1j * D * Sv) < 1e-12 and abs(M1d[0, 2] - 1j * D * Sv) < 1e-12 and abs(M1d[1, 0] - first) < 1e-12,
      'ccw %s, cw %s' % (np.round(M1d[2, 0], 12), np.round(M1d[0, 2], 12)))
HJ = sum(J * (S['x', i] @ S['x', (i + 1) % N] + S['y', i] @ S['y', (i + 1) % N] + S['z', i] @ S['z', (i + 1) % N]) for i in range(N))
HD = H - HJ
Sxt, Szt = sum(S['x', i] for i in range(N)), sum(S['z', i] for i in range(N))
comm = lambda a, b: np.linalg.norm(a @ b - b @ a)
unif = sum(flip) / np.sqrt(N)                                             # the uniform magnon, k = 0
e_unif = unif @ H @ unif - E0
check('the zero at Gamma: [H_J, Sx_tot] = 0, [H_DM, Sx_tot] != 0, [H, Sz_tot] = 0, and the uniform magnon has zero energy',
      comm(HJ, Sxt) < 1e-12 and comm(HD, Sxt) > 1 and comm(H, Szt) < 1e-12 and abs(e_unif) < 1e-12
      and np.linalg.norm(H @ unif - (E0 + e_unif) * unif) < 1e-12,
      '%.1e %.3f %.1e, energy %.1e' % (comm(HJ, Sxt), comm(HD, Sxt), comm(H, Szt), abs(e_unif)))

# ---------------------------------------------------------------- the lattice with the rule of the fold, against pyqula
DS = 0.1
gb = geometry.honeycomb_lattice()
r0 = np.array(gb.r)[:, :2]; a1 = np.asarray(gb.a1, float)[:2]; a2 = np.asarray(gb.a2, float)[:2]
cells = [(n, m) for n in range(-2, 3) for m in range(-2, 3)]
site = lambda s, n, m: r0[s] + n * a1 + m * a2


def magnon_hk(DS, JS=1.0):
    """The Bloch matrix sum_R <0,s|H|R,s'> exp(i k.R) of the rule of the fold: -|J|S between first neighbors, 3|J|S onsite, and
    the amplitude +i DS for a second-neighbor hop that turns left (counterclockwise), -i DS for one that turns right."""
    terms = []
    for s in (0, 1):
        for s2 in (0, 1):
            for n, m in cells:
                rj, ri = site(s2, n, m), site(s, 0, 0)                   # the hop from j = (R, s2) to i = (0, s)
                dist = np.linalg.norm(ri - rj)
                if abs(dist - 1) < 1e-9:
                    terms.append((s, s2, n, m, -JS))
                elif abs(dist - np.sqrt(3)) < 1e-9:
                    rk = [site(1 - s, a, b) for a, b in cells if abs(np.linalg.norm(site(1 - s, a, b) - rj) - 1) < 1e-9
                          and abs(np.linalg.norm(site(1 - s, a, b) - ri) - 1) < 1e-9][0]
                    d1, d2 = rk - rj, ri - rk
                    terms.append((s, s2, n, m, 1j * DS * np.sign(d1[0] * d2[1] - d1[1] * d2[0])))

    def hk(k):
        h = 3 * JS * np.eye(2, dtype=complex)
        for s, s2, n, m, amp in terms:
            h[s, s2] += amp * np.exp(1j * k @ (n * a1 + m * a2))
        return h
    return hk


B = pc.reciprocal([a1, a2])
K = (B[0] + B[1]) / 3
mine = magnon_hk(DS)
c_mine = [pc.chern_links(mine, B, bands=b, nk=24) for b in (0, 1)]
c_kubo = pc.chern_kubo(mine, B, bands=0, nk=48)
hq = gb.get_hamiltonian(has_spin=False, tij=[-1.])
hq.add_haldane(-2 * DS / np.sqrt(3))
hkq, Bq = pc.from_pyqula(hq)
c_q = pc.chern_links(hkq, Bq, bands=0, nk=24)
c_get = hq.get_chern()
ks = np.random.default_rng(3).uniform(-3, 3, (6, 2))
same_e = max(np.abs(np.linalg.eigvalsh(mine(k)) - 3 - np.linalg.eigvalsh(hkq(k))).max() for k in ks)
check('the rule of the fold gives C = -1 and +1 to the two bands, links and Kubo',
      abs(c_mine[0] + 1) < 1e-9 and abs(c_mine[1] - 1) < 1e-9 and abs(c_kubo + 1) < 1e-3, '%+.0f %+.0f, Kubo %+.4f' % (c_mine[0], c_mine[1], c_kubo))
check('pyqula add_haldane(-2 DS/sqrt 3) is the same magnet: C, get_chern and the bands',
      abs(c_q + 1) < 1e-9 and abs(c_get + 1) < 1e-6 and same_e < 1e-12, 'links %+.0f, get_chern %+.4f, bands within %.0e' % (c_q, c_get, same_e))
hpure = gb.get_hamiltonian(has_spin=False)
hpure.add_haldane(0.1)
t2p = max(abs(t.m[0, 0]) for t in hpure.get_multicell().hopping)
check('add_haldane(x) is the hopping sqrt(3) x/2, so DS = 0.1 is |x| = 0.1155', abs(t2p - np.sqrt(3) / 2 * 0.1) < 1e-12
      and abs(2 * 0.1 / np.sqrt(3) - 0.1155) < 5e-5, 't2 = %.5f for x = 0.1' % t2p)
Bh = pc.reciprocal([hd.a1, hd.a2])
c_sheet = pc.chern_links(lambda k: 3 * np.eye(2) + hd.hk(k, 1.0, -DS), Bh, bands=0, nk=24)
gK_sheet = np.diff(np.linalg.eigvalsh(hd.hk(np.array([4 * np.pi / 3, 0.0]), 1.0, -DS)))[0]
check('the magnon matrix of the sheet, 3|J|S + _haldane.hk(t=|J|S, t2=-DS) for D>0, has the same C and gap at K',
      abs(c_sheet + 1) < 1e-9 and abs(gK_sheet - 6 * np.sqrt(3) * DS) < 1e-12, 'C = %+.0f, gap %.4f' % (c_sheet, gK_sheet))
c_phi = pc.chern_links(lambda k: hd.hk(k, 1.0, 0.1), Bh, bands=0, nk=24)
print('INFO   the third option of the second quiz: _haldane.hk with phi=+pi/2 has C = %+.0f for the lower band, while the '
      'phases of panel (a), +pi/2 counterclockwise, give %+.0f' % (c_phi, c_mine[0]))

# ---------------------------------------------------------------- the key box and the problem: the gap at K and at Gamma
hK = mine(K)
bvec = [a1, a2, -a1 - a2]
phases = [np.mod(K @ b, 2 * np.pi) for b in bvec]


def turn(s, b):
    """+1 when the hop of a site of sublattice s along b turns left at the common neighbor, -1 when it turns right."""
    ri, rj = r0[s], r0[s] + b
    rk = [site(1 - s, a, c) for a, c in cells if abs(np.linalg.norm(site(1 - s, a, c) - ri) - 1) < 1e-9
          and abs(np.linalg.norm(site(1 - s, a, c) - rj) - 1) < 1e-9][0]
    d1, d2 = rk - ri, rj - rk
    return np.sign(d1[0] * d2[1] - d1[1] * d2[0])


angles = sorted(np.degrees(np.arctan2(b[1], b[0])) % 360 for b in bvec)
check('the b_n are at 120 degrees, |b_n| = sqrt 3, a hop along them turns left on A and right on B',
      np.allclose(np.diff(angles), 120) and np.allclose([np.linalg.norm(b) for b in bvec], np.sqrt(3))
      and all(turn(0, b) == 1 and turn(1, b) == -1 for b in bvec), 'angles %s' % np.round(angles, 6))
m_sol = 1j * DS * sum(np.exp(1j * K @ b) - np.exp(-1j * K @ b) for b in bvec)        # m(K) of the solution, as it writes it
check('K.b_n = 2 pi/3 modulo 2 pi, sum of sin = 3 sqrt(3)/2, and m(K) = -3 sqrt(3) DS in the form of the solution',
      np.allclose(phases, 2 * np.pi / 3) and abs(sum(np.sin(p) for p in phases) - 3 * np.sqrt(3) / 2) < 1e-12
      and abs(m_sol + 3 * np.sqrt(3) * DS) < 1e-12, '%s, m(K) = %.4f' % (np.round(phases, 6), m_sol.real))
deltas = [site(1, n, m) - r0[0] for n, m in cells if abs(np.linalg.norm(site(1, n, m) - r0[0]) - 1) < 1e-9]
f_sol = lambda k: sum(np.exp(1j * (k @ dl)) for dl in deltas)
m_of = lambda k, DS=DS: 1j * DS * sum(np.exp(1j * (k @ b)) - np.exp(-1j * (k @ b)) for b in bvec)


def sol_hk(k, DS=DS, swap=False):
    """The Bloch matrix of the solution as it is printed, 3|J|S + [[m, -f*], [-f, -m]], or with f and f* swapped."""
    fk, mk = f_sol(k), m_of(k, DS)
    up, lo = (-fk, -np.conj(fk)) if swap else (-np.conj(fk), -fk)
    return 3 * np.eye(2) + np.array([[mk, up], [lo, -mk]])


c_sol = pc.chern_kubo(sol_hk, B, bands=0, nk=48)
c_swap = pc.chern_kubo(lambda k: sol_hk(k, swap=True), B, bands=0, nk=48)
same_sol = max(np.abs(np.linalg.eigvalsh(sol_hk(k)) - 3 - np.linalg.eigvalsh(hkq(k))).max() for k in ks)
same_ent = max(max(np.abs(np.diag(sol_hk(k)) - np.diag(mine(-k)))) + abs(abs(sol_hk(k)[0, 1]) - abs(mine(-k)[0, 1]))
               for k in ks)    # the printed matrix is the fold at -k, the phase e^{ik.R} of mine being the momentum of the state,
#                                up to the phase of the off-diagonal entry, which mine takes with the cell R and not with delta
check('the matrix of the solution as printed: [A,A] at K is 3 + m(K) = 3 - 3 sqrt(3) DS, C = -1 for the lower band (Kubo), '
      'bands of pyqula', abs(sol_hk(K)[0, 0] - 3 + 3 * np.sqrt(3) * DS) < 1e-12 and abs(sol_hk(K)[0, 0].real - 2.48) < 5e-3
      and abs(c_sol + 1) < 1e-3 and same_sol < 1e-12 and same_ent < 1e-12,
      'H_AA(K) = %.4f, C = %+.4f, bands within %.0e, the fold at -k within %.0e' % (sol_hk(K)[0, 0].real, c_sol, same_sol, same_ent))
print('INFO   with f in the upper right and f* in the lower left, the old form of the matrix, the lower band has C = %+.4f' % c_swap)
kd = sorted(np.round(np.angle(np.exp(1j * (K @ dl))), 9) for dl in deltas)
check('the three phases K.delta are 0 and +-2 pi/3, so f(K) = 0', len(deltas) == 3 and np.allclose(kd, [-2 * np.pi / 3, 0, 2 * np.pi / 3])
      and abs(sum(np.exp(1j * (K @ dl)) for dl in deltas)) < 1e-12, np.round(kd, 6))
check('at K the first-neighbor term vanishes and the diagonal is 3|J|S -+ 3 sqrt(3) DS',
      abs(hK[0, 1]) < 1e-12 and np.allclose(sorted(np.diag(hK).real), [3 - 3 * np.sqrt(3) * DS, 3 + 3 * np.sqrt(3) * DS]),
      'off-diagonal %.0e, diagonal %s' % (abs(hK[0, 1]), np.round(np.diag(hK).real, 4)))
gK = np.diff(np.linalg.eigvalsh(hK))[0]
eG = np.linalg.eigvalsh(mine(np.zeros(2)))
eK = np.linalg.eigvalsh(hK)
check('the gap at K is 6 sqrt(3) DS = 1.04 for DS = 0.1, from 2.48 to 3.52, the bands at Gamma are 0 and 6',
      abs(gK - 6 * np.sqrt(3) * DS) < 1e-12 and abs(gK - 1.04) < 5e-3 and abs(eK[0] - 2.48) < 5e-3 and abs(eK[1] - 3.52) < 5e-3
      and np.allclose(eG, [0, 6]), 'gap %.4f from %.4f to %.4f, Gamma %s' % (gK, eK[0], eK[1], eG))
rng = []
for d in (0.1, 0.18, 0.19, 0.20, 0.25):
    hd_ = magnon_hk(d)
    rng.append((d, np.diff(np.linalg.eigvalsh(hd_(K)))[0], pc.gap(hd_, B, 1, nk=90)))
ok = all(abs(gk - gf) < 1e-9 for d, gk, gf in rng if d < 0.19245) and all(gf < gk - 0.05 for d, gk, gf in rng if d > 0.19245)
Mpt = B[0] / 2
eM = [np.linalg.eigvalsh(magnon_hk(d)(Mpt)) for d in (0.1, 0.2, 0.25)]
check('6 sqrt(3) DS is the smallest gap for DS < 1/(3 sqrt 3) = 0.19, above it the gap is 2|J|S, at M where the bands are 2 and 4',
      ok and abs(1 / (3 * np.sqrt(3)) - 0.19) < 5e-3 and all(abs(gf - 2) < 1e-9 for d, gk, gf in rng if d > 0.19245)
      and all(np.allclose(e, [2, 4]) for e in eM) and abs(np.linalg.norm(Mpt) - np.sqrt(3) / 2 * np.linalg.norm(K)) < 1e-12,
      ', '.join('%.2f: %.3f %.3f' % x for x in rng))
mesh = pc.kmesh(B, 90, points=[K, -K, Mpt])
up_to = []
for d in (0.2, 0.3, 0.4, 0.5, 0.57, 0.577):
    E = np.linalg.eigvalsh(np.array([magnon_hk(d)(k) for k in mesh]))
    up_to.append((d, (E[:, 1] - E[:, 0]).min(), E[:, 1].min() - E[:, 0].max(), E[:, 0].min()))
above = [(d, np.linalg.eigvalsh(magnon_hk(d)(K))[0], np.linalg.eigvalsh(magnon_hk(d)(-K))[0]) for d in (0.58, 0.6, 1.0)]
check('from 0.19 to 1/sqrt 3 = 0.58 the smallest gap is 2|J|S (direct and indirect) and the lower band is not below zero, '
      'above 0.58 the lower band is below zero at K and K\'',
      abs(1 / np.sqrt(3) - 0.58) < 5e-3 and all(abs(gd - 2) < 1e-9 and abs(gi - 2) < 1e-9 and lo > -1e-12 for d, gd, gi, lo in up_to)
      and all(eK_ < 0 and abs(eK_ - (3 - 3 * np.sqrt(3) * d)) < 1e-12 and abs(eKp - eK_) < 1e-12 for d, eK_, eKp in above),
      'below: ' + ', '.join('%.3f: %.3f %.3f %.1e' % x for x in up_to) + '; above, lower band at K: '
      + ', '.join('%.2f: %.4f' % x[:2] for x in above))
neg = magnon_hk(-DS)
check('the gap is the same for -DS, and C changes sign', abs(np.diff(np.linalg.eigvalsh(neg(K)))[0] - gK) < 1e-12
      and abs(pc.chern_links(neg, B, bands=0, nk=24) - 1) < 1e-9, 'C = %+.0f' % pc.chern_links(neg, B, bands=0, nk=24))

# ---------------------------------------------------------------- the ribbon, also with 2|J|S on the edge sites, and the trivial gap
gz = geometry.honeycomb_zigzag_ribbon(12)
yz = np.array(gz.r)[:, 1]
zc = np.full(len(yz), 3.0); zc[np.abs(np.abs(yz) - yz.max()) < 1e-9] = 2.0
dense = lambda m: np.asarray(m.todense() if hasattr(m, 'todense') else m)
rz, a1z = np.array(gz.r), np.asarray(gz.a1, float)
coord = np.array([sum(1 for j in range(len(rz)) for s in (-1, 0, 1) if abs(np.linalg.norm(rz[j] + s * a1z - rz[i]) - 1) < 1e-6)
                  for i in range(len(rz))])
at_edge = np.abs(np.abs(yz) - yz.max()) < 1e-9
check('a spin at the edge of the ribbon has two neighbors, every other spin three', set(coord[at_edge]) == {2} and set(coord[~at_edge]) == {3}
      and at_edge.sum() == 2, '%d edge sites with %s, the others %s' % (at_edge.sum(), set(coord[at_edge]), set(coord[~at_edge])))
hp = gz.get_hamiltonian(has_spin=False, tij=[-1.])
hp.add_onsite(3.)
genp = hp.get_hk_gen()
outer = np.abs(yz) > 0.6 * yz.max()                                      # the outer parts, as the colors of the pictures
wflat, kflat = [], []
for k in np.linspace(0, 1, 401):
    e, v = np.linalg.eigh(dense(genp([k, 0, 0])))
    for n in np.where(np.abs(e - 3) < 1e-3)[0]:
        wflat.append((np.abs(v[:, n]) ** 2)[outer].sum()); kflat.append(2 * np.pi * k)
check('the flat branch of the plain magnet at 3|J|S sits on the two zigzag edges', len(wflat) > 20 and min(wflat) > 0.9
      and min(kflat) < 2.6 and max(kflat) > 3.7, '%d states from k = %.3f to %.3f, weight on the outer parts at least %.4f'
      % (len(wflat), min(kflat), max(kflat), min(wflat)))


def ribbon(DS, onsite):
    """The bands of the ribbon on a mesh of k, with the mean position <y> of each state."""
    h = gz.get_hamiltonian(has_spin=False, tij=[-1.])
    h.add_haldane(-2 * DS / np.sqrt(3))
    h.add_onsite(onsite)
    gen = h.get_hk_gen()
    E, Y = [], []
    for k in np.linspace(0, 1, 401):
        e, v = np.linalg.eigh(dense(gen([k, 0, 0])))
        E.append(e); Y.append((np.abs(v) ** 2).T @ yz)
    return np.array(E), np.array(Y)


def crossings(E, Y, level):
    """For the lower and the upper edge, the signs of the slopes of the states of that edge that cross the level."""
    out = {}
    for name, sel in (('lower', Y < -0.6 * yz.max()), ('upper', Y > 0.6 * yz.max())):
        s = []
        for j in range(E.shape[1]):
            for i in np.where(sel[:-1, j] & sel[1:, j] & (np.sign(E[:-1, j] - level) != np.sign(E[1:, j] - level)))[0]:
                s.append(int(np.sign(E[i + 1, j] - E[i, j])))
        out[name] = s
    return out, E[0].min()


res = {}
for DS_ in (0.1, -0.1):
    for name, ons in (('3|J|S', 3.0), ('2|J|S at the edge', zc)):
        E, Y = ribbon(DS_, ons)
        for level in (2.75, 3.25):
            res[DS_, name, level] = crossings(E, Y, level)
ok = True
for name in ('3|J|S', '2|J|S at the edge'):
    for level in (2.75, 3.25):
        p, n = res[0.1, name, level][0], res[-0.1, name, level][0]
        ok = ok and all(len(x[e]) == 1 for x in (p, n) for e in ('lower', 'upper'))
        ok = ok and p['lower'][0] == -p['upper'][0] and p['lower'][0] == -n['lower'][0]
same_dir = all(res[d, '3|J|S', lv][0][e] == res[d, '2|J|S at the edge', lv][0][e]
               for d in (0.1, -0.1) for lv in (2.75, 3.25) for e in ('lower', 'upper'))
check('one branch per edge in the gap, opposite slopes, reversed with DS, for 3|J|S and for 2|J|S on the edge sites, '
      'with the same directions for the two onsite energies', ok and same_dir, {(k[0], k[1], k[2]): v[0] for k, v in res.items()})
check('the bottom of the ribbon at k=0 is 0.0054 with 3|J|S everywhere and 0 with 2|J|S on the edge sites',
      abs(res[0.1, '3|J|S', 2.75][1] - 0.0054) < 5e-5 and abs(res[0.1, '2|J|S at the edge', 2.75][1]) < 1e-12,
      '%.5f %.1e' % (res[0.1, '3|J|S', 2.75][1], res[0.1, '2|J|S at the edge', 2.75][1]))
ht = gb.get_hamiltonian(has_spin=False, tij=[-1.])
ht.add_sublattice_imbalance(0.52)
hkt, Bt = pc.from_pyqula(ht)
check('an onsite energy 2M = 1.04 on one sublattice gives C = 0 and the gap 1.04', abs(pc.chern_links(hkt, Bt, bands=0, nk=24)) < 1e-9
      and abs(pc.gap(hkt, Bt, 1, nk=60) - 1.04) < 1e-9, 'C = %+.0f, gap %.4f' % (pc.chern_links(hkt, Bt, bands=0, nk=24), pc.gap(hkt, Bt, 1, nk=60)))

# ---------------------------------------------------------------- the lab box
check('the lab box, 6 sqrt(3) DS = 4 meV gives DS = 0.4 meV, ours', abs(4 / (6 * np.sqrt(3)) - 0.4) < 0.02, '%.4f meV' % (4 / (6 * np.sqrt(3))))
print('all checks of page 16 hold')
