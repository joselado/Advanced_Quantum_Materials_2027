"""Session 1, the numbers that page 13 (Section 1.13, the charge density wave) quotes and that no figure script
asserts. One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an
assert, here or in the figure script that draws it. The figure scripts of the page assert their own numbers through
_g4_cdw.check (the imbalance 0.03, 0.34 and 0.89 at V = 0.5t, t and 3t, the gap 2 V dn and 5.35t at V = 3t, the
charges of the three quiz pictures). This script checks the fold, the problem of one pass of the loop on a ring of four
sites, the captions of Figures 1.4 and 1.5, the feedback of the quizzes and the try-it box, with numpy and by a second
route where one exists, and the statement of the caption that the curve is the antiferromagnet of (1.7) at U = 2V,
with pyqula. The chain is (1.6) with the hopping -t, and the sign of t changes no level and no charge on these
bipartite rings. It finds the repository from its own path and writes no file, since pyqula runs in a temporary
folder."""
import contextlib
import io
import os
import tempfile

import numpy as np
from scipy import special, optimize

t = 1.0


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def ring(N, onsite):
    """The single-particle Hamiltonian of a periodic ring of N sites with the hopping -t and the given onsite energies."""
    H = np.diag(np.asarray(onsite, float))
    for i in range(N):
        H[i, (i + 1) % N] = H[(i + 1) % N, i] = -t
    return H


def hartree(V, n):
    """The Hartree onsite energy V (<n_(i-1)> + <n_(i+1)>) of each site of a ring."""
    return V * (np.roll(n, 1) + np.roll(n, -1))


def fill(H, Ne):
    w, v = np.linalg.eigh(H)
    return w, (np.abs(v[:, :Ne]) ** 2).sum(axis=1)


# ------------------------------------------------------------------ the problem, one pass on the ring of four sites
V = 3.0
guess = np.array([0.6, 0.4, 0.6, 0.4])
eps = hartree(V, guess)
check('onsite energies 2.4t on the sites with 0.6 and 3.6t on the sites with 0.4', np.allclose(eps, [2.4, 3.6, 2.4, 3.6]), eps)
w, new = fill(ring(4, eps), 2)
D = V * (0.6 - 0.4)
closed = [3 - np.sqrt(D ** 2 + 4 * t ** 2), 2.4, 3.6, 3 + np.sqrt(D ** 2 + 4 * t ** 2)]
check('the four levels 0.91t, 2.4t, 3.6t and 5.09t, with 3 -+ sqrt(0.36 + 4) for the cells in phase', np.allclose(w, closed) and
      abs(w[0] - 0.91) < 0.005 and abs(w[3] - 5.09) < 0.005, np.round(w, 4))
check('the two lowest levels are 0.91t and 2.4t', abs(w[0] - 0.912) < 1e-3 and abs(w[1] - 2.4) < 1e-12, w[:2])
check('the new charges 0.82 and 0.18, closed form 3/4 + D/(4 sqrt(4t^2 + D^2))',
      np.allclose(new, [0.8218, 0.1782, 0.8218, 0.1782], atol=1e-4) and np.isclose(new[0], 0.75 + D / (4 * np.sqrt(4 + D ** 2))), new)
check('the total charge is 1 per pair of sites before and after', np.isclose(guess[:2].sum(), 1) and np.isclose(new[:2].sum(), 1),
      new[:2].sum())
# the two momenta of the cells K = 0 and pi: in phase the cells couple with 2t, in antiphase with 0
for K, off in ((0.0, 2 * t), (np.pi, 0.0)):
    hk = np.array([[2.4, -t * (1 + np.exp(-1j * K))], [-t * (1 + np.exp(1j * K)), 3.6]])
    check('the cell of two sites at K = %g couples the two sites with %g' % (K, off), np.isclose(abs(hk[0, 1]), off), abs(hk[0, 1]))
# K is the momentum per cell, K = 2k: the bands of the fold, V -+ sqrt((V dn)^2 + 4t^2 cos^2 k) with dn = 0.2, give the
# levels of the cells in phase at k = 0 and those in antiphase at the zone edge k = pi/2, and not at k = pi
fold = lambda k: 3.0 + np.array([-1, 1]) * np.sqrt((V * 0.2) ** 2 + 4 * t ** 2 * np.cos(k) ** 2)
check('the bands of the fold give 0.91t and 5.09t at k = 0 and 2.4t and 3.6t at the zone edge k = pi/2, so K = 2k',
      np.allclose(fold(0.0), [w[0], w[3]]) and np.allclose(fold(np.pi / 2), [2.4, 3.6]) and np.allclose(fold(np.pi), fold(0.0)),
      (fold(0.0), fold(np.pi / 2)))
v2 = np.linalg.eigh(ring(4, eps))[1][:, 1]
check('the second level 2.4t sits only on the sites with 0.6', np.allclose(np.abs(v2[[1, 3]]), 0) and
      np.allclose(np.abs(v2[[0, 2]]) ** 2, 0.5), np.round(np.abs(v2) ** 2, 4))
# the loop continued from there converges on the ring of four sites
n = guess.copy()
for _ in range(500):
    n = 0.5 * n + 0.5 * fill(ring(4, hartree(V, n)), 2)[1]
check('the loop on the ring of four sites goes on past 0.82, to 0.95 and 0.05', abs(n[0] - 0.951) < 1e-3 and
      abs(n[1] - 0.049) < 1e-3, np.round(n, 4))
v1 = np.linalg.eigh(ring(4, eps))[1][:, 0]
wA = np.sum(np.abs(v1[[0, 2]]) ** 2)
check('the lowest level has the weight (1 + 0.6/sqrt(0.36 + 4))/2 = 0.64 on the two sites with 0.6, 0.32 on each',
      np.isclose(wA, 0.5 * (1 + 0.6 / np.sqrt(4.36))) and abs(wA - 0.64) < 0.005 and abs(wA / 2 - 0.32) < 0.005, wA)
check('the new charge 0.5 + 0.32 = 0.82', np.isclose(0.5 + wA / 2, new[0]), 0.5 + wA / 2)


# ------------------------------------------------------------------ the fold, Hartree with <n> = (1 +- dn)/2
for dn in (0.2, 0.892):
    nn = np.array([(1 + dn) / 2, (1 - dn) / 2] * 4)
    e = hartree(V, nn)
    ok = np.allclose(e[0::2], V * (1 - dn)) and np.allclose(e[1::2], V * (1 + dn))
    ok &= np.allclose(e - V, np.array([-V * dn, V * dn] * 4))
    check('dn = %g: onsite energies V(1 -+ dn), a staggered potential -+ V dn around V' % dn, ok, e[:2])
    ks = np.linspace(-np.pi / 2, np.pi / 2, 2001)
    bands = np.sqrt((V * dn) ** 2 + 4 * t ** 2 * np.cos(ks) ** 2)
    check('dn = %g: the bands V -+ sqrt((V dn)^2 + 4t^2 cos^2 k) have the gap 2 V dn at the zone edge' % dn,
          np.isclose(2 * bands.min(), 2 * V * dn), 2 * bands.min())
# the double counting: <H> of the self-consistent Slater determinant of the ring of eight sites against the levels
N8 = 8
nn = np.array([0.7, 0.3] * 4)
for _ in range(400):
    nn = 0.5 * nn + 0.5 * fill(ring(N8, hartree(V, nn)), 4)[1]
H8 = ring(N8, hartree(V, nn))
w8, v8 = np.linalg.eigh(H8)
occ = v8[:, :4]
rho = occ @ occ.T                                                 # <c_i^+ c_j> of the determinant
T8 = ring(N8, np.zeros(N8))
nd = np.diag(rho)
exact_V = V * sum(nd[i] * nd[(i + 1) % N8] - rho[i, (i + 1) % N8] ** 2 for i in range(N8))   # Wick, Hartree minus Fock
hartree_V = V * sum(nd[i] * nd[(i + 1) % N8] for i in range(N8))
check('the filled levels minus V sum <n_n><n_(n+1)> is the kinetic energy plus the Hartree energy',
      np.isclose(w8[:4].sum() - hartree_V, np.trace(T8 @ rho) + hartree_V), (w8[:4].sum() - hartree_V))
check('the Fock part that the fold leaves out is not zero on a bond', abs(exact_V - hartree_V) > 1e-3, exact_V - hartree_V)


def imbalance(V):
    """Hartree imbalance of the infinite chain, 1 = (V/pi) int dk / sqrt(D^2 + 4t^2 cos^2 k), D = V dn, with the complete
    elliptic integral K(m) of parameter m = 4t^2/(D^2 + 4t^2)."""
    if V == 0:
        return 0.0
    f = lambda D: V * (2 / np.pi) * special.ellipk(4 * t ** 2 / (D ** 2 + 4 * t ** 2)) / np.sqrt(D ** 2 + 4 * t ** 2) - 1
    return optimize.brentq(f, 1e-12, 2 * V) / V


# a second route, the self-consistent ring of 200 sites in real space
for Vv, ref in ((1.0, 0.340), (3.0, 0.892)):
    N = 200
    n = np.array([0.8, 0.2] * (N // 2))
    for _ in range(400):
        n = 0.5 * n + 0.5 * fill(ring(N, hartree(Vv, n)), N // 2)[1]
    dn_ring = abs(n[0] - n[1])
    check('V = %g: the imbalance %.3f from the gap equation and from a ring of 200 sites' % (Vv, ref),
          abs(imbalance(Vv) - ref) < 1e-3 and abs(dn_ring - ref) < 2e-3, (imbalance(Vv), dn_ring))
# the picture quiz: the imbalance and the gap 2 V dn at V = 0.5t, t and 3t, and the charges (1 +- dn)/2
for Vv, dn_q, gap_q, big, small in ((0.5, 0.03, 0.03, 0.515, 0.485), (1.0, 0.34, 0.68, 0.67, 0.33), (3.0, 0.89, 5.35, 0.95, 0.05)):
    dn = imbalance(Vv)
    ok = abs(dn - dn_q) < 0.005 and abs(2 * Vv * dn - gap_q) < 0.005
    ok &= abs((1 + dn) / 2 - big) < 0.005 and abs((1 - dn) / 2 - small) < 0.005
    check('V = %g: the imbalance %g, the gap %gt and the charges %g and %g' % (Vv, dn_q, gap_q, big, small), ok,
          (dn, 2 * Vv * dn))
I = lambda D: (2 / np.pi) * special.ellipkm1(D ** 2 / (D ** 2 + 4 * t ** 2)) / np.sqrt(D ** 2 + 4 * t ** 2)  # K(1 - p)
check('the integral of the fold grows without bound as D = V dn goes to zero, as log(1/D)',
      all(I(D / 10) - I(D) > 0.7 for D in (1e-2, 1e-4, 1e-6)) and abs((I(1e-7) - I(1e-6)) - np.log(10) / np.pi) < 1e-6,
      [round(I(D), 3) for D in (1e-2, 1e-4, 1e-6)])
check('at small V the imbalance is (8t/V) exp(-pi t/V), 0.03 at V = 0.5t', abs(imbalance(0.5) - 16 * np.exp(-2 * np.pi)) < 1e-3,
      (imbalance(0.5), 16 * np.exp(-2 * np.pi)))

# ------------------------------------------------------------------ Figure 1.5, the ring of eight sites at half filling
w0 = np.linalg.eigvalsh(ring(8, np.zeros(8)))
check('V = 0: the levels -2t, -1.41t twice, 0 twice, and four electrons end inside the pair at 0',
      np.allclose(w0[:5], [-2, -np.sqrt(2), -np.sqrt(2), 0, 0]) and np.isclose(w0[3], w0[4]), np.round(w0, 3))
n = np.array([0.8, 0.2] * 4)
for _ in range(400):
    n = 0.5 * n + 0.5 * fill(ring(8, hartree(3.0, n)), 4)[1]
w3 = np.linalg.eigvalsh(ring(8, hartree(3.0, n)))
check('V = 3t on eight sites: the charges 0.946 and 0.054 and the gap 5.35t', abs(max(n) - 0.946) < 1e-3 and
      abs(min(n) - 0.054) < 1e-3 and abs(w3[4] - w3[3] - 5.35) < 0.01, (np.round(n[:2], 4), w3[4] - w3[3]))

# ------------------------------------------------------------------ the quiz on the number of degenerate states
pat = np.array([0.8, 0.2] * 2)
check('a translation maps (0.8, 0.2, 0.8, 0.2) to (0.2, 0.8, 0.2, 0.8), two patterns',
      np.allclose(np.roll(pat, 1), [0.2, 0.8, 0.2, 0.8]) and len({tuple(np.roll(pat, s)) for s in range(4)}) == 2, 2)
p4 = np.array([0.9, 0.5, 0.1, 0.5])
check('the pattern (0.9, 0.5, 0.1, 0.5) gives four states under translations, at the same filling',
      len({tuple(np.roll(p4, s)) for s in range(4)}) == 4 and np.isclose(p4.mean(), 0.5), 4)

# ------------------------------------------------------------------ pyqula, the curve at U = 2V and the try-it box
from pyqula import geometry
with tempfile.TemporaryDirectory() as tmp:
    cwd = os.getcwd(); os.chdir(tmp)
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            g = geometry.bichain()
            nk = 100
            hc = g.get_hamiltonian(has_spin=False).get_mean_field_hamiltonian(V1=3.0, mf="CDW", filling=0.5, mix=0.9, nk=nk,
                                                                                compute_cross=False, write=False)
            ha = g.get_hamiltonian().get_mean_field_hamiltonian(U=6.0, mf="antiferro", mix=0.9, nk=nk)
            # the default call, with the Fock term, on the mesh of 400 cells of the caption of the figure
            hf = g.get_hamiltonian(has_spin=False).get_mean_field_hamiltonian(V1=3.0, mf="CDW", filling=0.5, mix=0.9, nk=400,
                                                                                write=False)
            dn_f = abs(np.diff(hf.get_vev(nk=400))[0])
            hop_f = [abs(np.array(hf.intra)[0, 1])] + [abs(np.array(d.m)).max() for d in hf.hopping]
            hop_c = [abs(np.array(hc.intra)[0, 1])] + [abs(np.array(d.m)).max() for d in hc.hopping]
            dn_c = abs(np.diff(hc.get_vev(nk=nk))[0]); m_a = abs(ha.get_vev("mz", nk=nk)[0])
            # the try-it box: the cell with cdw = 0.1 at V = 0 and the default call at V = 10t
            h0 = g.get_hamiltonian(has_spin=False); h0.add_sublattice_imbalance(0.1)
            n0 = h0.get_mean_field_hamiltonian(V1=0., mf="CDW", mix=0.5, filling=0.5, write=False).get_vev(operator=None)
            n10 = g.get_hamiltonian(has_spin=False).get_mean_field_hamiltonian(V1=10., mf="CDW", mix=0.5, filling=0.5,
                                                                              write=False).get_vev(operator=None)
        left = os.listdir(tmp)
    finally:
        os.chdir(cwd)
check('pyqula: the Hartree charge density wave at V = 3t is the antiferromagnet at U = 6t, 0.892',
      abs(dn_c - m_a) < 1e-4 and abs(dn_c - 0.892) < 1e-3, (dn_c, m_a))
check('pyqula: the default call keeps the Fock term and gives the smaller imbalance 0.70 at V = 3t on 400 cells',
      abs(dn_f - 0.704) < 2e-3, dn_f)
check('pyqula: the Fock term changes the hopping, 1.725 on both bonds at V = 3t, while Hartree keeps 1',
      np.allclose(hop_f, 1.725, atol=1e-3) and np.allclose(hop_c, 1.0), (hop_f, hop_c))
check('try-it box: with cdw = 0.1 the imbalance at V = 0 is finite, 0.14', abs(abs(n0[0] - n0[1]) - 0.1417) < 1e-3, n0)
check('try-it box: the cell saturates close to 1 at V = 10t, 0.96 with its default Fock term',
      abs(abs(n10[0] - n10[1]) - 0.962) < 2e-3, n10)
check('the calls with write=False leave no file', left == [], left)

# the notebook box, old text corrected on 2026-11-22: both cells start the loop from the guess mf="CDW", which picks one
# of the two charge patterns, while the Hamiltonian keeps the symmetry, since the cells set the external imbalance
# cdw = 0. Route 1 reads the two cells, route 2 asks pyqula for the guess and runs the loop of the cells from it and from
# the opposite guess
import json
import re
from pyqula import meanfield
nb = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'jupyter-notebooks',
                                 'session1.ipynb'), encoding='utf-8'))
heads = [''.join(c['source']).strip() for c in nb['cells']]
mixes = {}
for title, part in (('## Symmetry breaking in the spinless fermionic chain', 'Core'),
                    ('## Gap opening in a spinless interacting model', 'Challenge')):
    i = [j for j, s in enumerate(heads) if s.startswith(title)][0]
    src = ''.join(nb['cells'][i + 1]['source'])
    zero = re.search(r'^cdw = 0\.?\s*(#.*)?$', src, re.M) is not None
    check('notebook box: the %s cell passes mf="CDW" and sets cdw = 0' % part, 'mf="CDW"' in src and zero, zero)
    mixes[part] = float(re.search(r'mf="CDW",mix=([0-9.]+)', src).group(1))
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    G = np.array(meanfield.guess(geometry.bichain().get_hamiltonian(has_spin=False), "CDW"))
gcdw = np.real(np.diag(G))
check('notebook box: the guess "CDW" is the onsite energies +1 and -1 on the two sites of the cell', np.allclose(gcdw, [1, -1]), gcdw)
with tempfile.TemporaryDirectory() as tmp:
    cwd = os.getcwd(); os.chdir(tmp)
    try:
        res = {}
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            for part, mix in mixes.items():
                for V in (0., 3.):
                    for sign in (+1, -1):
                        h0 = geometry.bichain().get_hamiltonian(has_spin=False); h0.add_sublattice_imbalance(0.)
                        hs, Es = h0.get_mean_field_hamiltonian(V1=V, mf="CDW" if sign > 0 else -G, mix=mix, filling=0.5,
                                                               write=False, return_total_energy=True)
                        res[part, V, sign] = (np.real(hs.get_vev(operator=None)), Es)
        left = os.listdir(tmp)
    finally:
        os.chdir(cwd)
for part in mixes:
    (np_, Ep), (nm, Em) = res[part, 3., +1], res[part, 3., -1]
    check('notebook box, %s cell: at V = 3t the guess and the opposite guess end in the two mirrored patterns, with the '
          'same energy' % part, np.allclose(np_, nm[::-1], atol=1e-4) and abs(np_[0] - np_[1]) > 0.5 and abs(Ep - Em) < 1e-6,
          (np.round(np_, 4), np.round(nm, 4), Ep - Em))
    n0p, n0m = res[part, 0., +1][0], res[part, 0., -1][0]
    check('notebook box, %s cell: at V = 0 the loop from the guess ends uniform, so the Hamiltonian keeps the symmetry' % part,
          abs(n0p[0] - n0p[1]) < 1e-6 and abs(n0m[0] - n0m[1]) < 1e-6, (n0p, n0m))
check('the notebook-box calls with write=False leave no file', left == [], left)
# the notebook box, sentence added on 2026-11-22: "Both cells also keep the Fock term, so at V = 3t the imbalance is 0.70
# and not the Hartree value 0.89 of the text". Route 1 reads the two cells, which call get_mean_field_hamiltonian with
# no compute_cross, so with the default that keeps the Fock term. Route 2 runs the call of each cell at V = 3t with its
# own mix and the default meshes, nk = 8 for the loop and 30 cells for get_vev, once as the cell does and once with
# compute_cross=False. The Fock term makes the imbalance smaller at the same mesh for every V of a grid from 0.2t to 10t,
# while below about 0.75t the coarse mesh of the cell gives more than the converged Hartree value, so the sentence
# quotes V = 3t and not a range.
for title, part in (('## Symmetry breaking in the spinless fermionic chain', 'Core'),
                    ('## Gap opening in a spinless interacting model', 'Challenge')):
    i = [j for j, s_ in enumerate(heads) if s_.startswith(title)][0]
    src = ''.join(nb['cells'][i + 1]['source'])
    check('notebook box: the %s cell calls the mean field with no compute_cross, so it keeps the Fock term' % part,
          'get_mean_field_hamiltonian(V1=V,mf="CDW"' in src and 'compute_cross' not in src, mixes[part])
with tempfile.TemporaryDirectory() as tmp:
    cwd = os.getcwd(); os.chdir(tmp)
    try:
        dns = {}
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            for part, mix in mixes.items():
                for cc in (True, False):
                    h0 = geometry.bichain().get_hamiltonian(has_spin=False); h0.add_sublattice_imbalance(0.)
                    d_ = h0.get_mean_field_hamiltonian(V1=3.0, mf="CDW", mix=mix, filling=0.5, write=False,
                                                       compute_cross=cc).get_vev(operator=None)
                    dns[part, cc] = abs(d_[0] - d_[1])
            grid = {}
            for V in (0.2, 0.5, 1.0, 2.0, 5.0, 10.0):
                for cc in (True, False):
                    h0 = geometry.bichain().get_hamiltonian(has_spin=False)
                    d_ = h0.get_mean_field_hamiltonian(V1=V, mf="CDW", mix=0.5, filling=0.5, write=False,
                                                       compute_cross=cc).get_vev(operator=None)
                    grid[V, cc] = abs(d_[0] - d_[1])
        left = os.listdir(tmp)
    finally:
        os.chdir(cwd)
for part in mixes:
    check('notebook box, %s cell: at V = 3t its call gives the imbalance 0.70, and 0.89 with compute_cross=False' % part,
          abs(dns[part, True] - 0.704) < 2e-3 and abs(dns[part, False] - 0.892) < 1e-3, (dns[part, True], dns[part, False]))
check('notebook box: at the mesh of the cell the Fock term lowers the imbalance at every V of the grid',
      all(grid[V, True] < grid[V, False] for V in (0.2, 0.5, 1.0, 2.0, 5.0, 10.0)),
      [(V, round(grid[V, True], 3), round(grid[V, False], 3)) for V in (0.2, 0.5, 1.0, 2.0, 5.0, 10.0)])
check('notebook box: at V = 0.5t the cell gives more than the converged Hartree value 0.03, so no range is quoted',
      grid[0.5, True] > 0.1 and abs(imbalance(0.5) - 0.03) < 5e-3, (grid[0.5, True], imbalance(0.5)))
check('the calls of the notebook box leave no file', left == [], left)

print('all checks of page 13 hold')
