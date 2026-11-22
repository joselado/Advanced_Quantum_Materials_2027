"""Session 6, the numbers that page 09 (Sections 6.9 and 6.10) quotes, checked in the order of the page.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here or
in the figure script that draws it. The figure g3_triangular_meanfield asserts its own numbers when it is drawn, and this
script runs its downloadable pyqula script again, in a temporary folder, and asserts them again, with the reading of
get_vev("mx") as n_up - n_dn along x, a finer k-mesh, and the four guesses again with the tighter maxerror=1e-8 of the
loop, which the caption quotes. The old schematic hubbard_to_heisenberg is checked here with the
same exact diagonalization, so that its script is not touched. The lattice pictures of the quiz are checked through their
helper. The lab box is checked against the stored source. It finds the repository from its own path and writes no file.

Run it from anywhere:  python3 webnotes/checks/session06/g3_09_heisenberg_lattice.py"""
import os, sys, runpy, tempfile, itertools
sys.dont_write_bytecode = True
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
assert os.path.exists(os.path.join(REPO, 'webnotes', 'pages', 'session06'))

import numpy as np
from functools import reduce


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# the recall box and the key box: on one bond the singlet is at -4t^2/U and the triplet at 0 for U >> t,
# which is J (S_i.S_j - 1/4); S_i.S_j is -3/4 on the singlet and +1/4 on the triplet
sx = np.array([[0, 1], [1, 0]]) / 2; sy = np.array([[0, -1j], [1j, 0]]) / 2; sz = np.diag([1., -1.]) / 2
SS = sum(np.kron(s, s) for s in (sx, sy, sz)).real
check('fold, S_i.S_j - 1/4 is -1 on the singlet and 0 on the triplet', np.allclose(np.linalg.eigvalsh(SS - np.eye(4) / 4), [-1, 0, 0, 0]),
      np.linalg.eigvalsh(SS - np.eye(4) / 4))

# the schematic hubbard_to_heisenberg: the open Hubbard chain of four sites at half filling against the Heisenberg chain
L, M = 4, 8
I2, Z, a = np.eye(2), np.diag([1., -1.]), np.array([[0., 1.], [0., 0.]])
cs = [reduce(np.kron, [Z] * m + [a] + [I2] * (M - m - 1)) for m in range(M)]   # modes (i, up) = 2i, (i, dn) = 2i+1
nn = [x.T @ x for x in cs]
keep = np.where(abs(np.diag(sum(nn)) - L) < 1e-9)[0]
assert len(keep) == 70
Hkin = np.zeros((2 ** M, 2 ** M))
for i in range(L - 1):
    for s in (0, 1):
        hop = cs[2 * i + s].T @ cs[2 * (i + 1) + s]
        Hkin -= hop + hop.T
Hint = sum(nn[2 * i] @ nn[2 * i + 1] for i in range(L))
Hkin, Hint = Hkin[np.ix_(keep, keep)], Hint[np.ix_(keep, keep)]


def site(op, i):
    return reduce(np.kron, [np.eye(2)] * i + [op] + [np.eye(2)] * (L - i - 1))


Hh = sum(site(s, i) @ site(s, i + 1) for i in range(L - 1) for s in (sx, sy, sz)).real
eh = np.linalg.eigvalsh(Hh)
heis = eh - eh[0]
levels = np.unique(np.round(heis, 9))
check('schematic, the Heisenberg levels are 0.66, 1.37, 1.73, 2.07 and 2.37 in units of J',
      [round(x, 2) for x in levels[1:]] == [0.66, 1.37, 1.73, 2.07, 2.37], np.round(levels, 3))
worst = {}
for U in (10.0, 30.0):
    e = np.linalg.eigvalsh(Hkin + U * Hint)
    lev = (e[:16] - e[0]) / (4 / U)
    rel = np.abs(lev[1:] - heis[1:]) / heis[1:]
    worst[U] = rel.max()
    assert e[16] - e[0] > 0.6 * U                         # the next level is a charge excitation of order U
check('schematic, at U=10t every level is within 5 percent of the Heisenberg value', worst[10.0] < 0.05, round(worst[10.0], 4))
check('schematic, at U=30t every level is within 1 percent', worst[30.0] < 0.01, round(worst[30.0], 4))
# the fold: the constant -sum J/4 that (6.5) leaves out, three bonds of the open chain
U = 400.0
e0 = np.linalg.eigvalsh(Hkin + U * Hint)[0]
check('fold, at U=400t the Hubbard ground energy is J (E_Heis - 3/4) for the three bonds, the constant -sum J/4',
      abs(e0 / (4 / U) - (eh[0] - 0.75)) < 0.01, (round(e0 / (4 / U), 4), round(eh[0] - 0.75, 4)))

# the key box of 6.10 and the fold: three classical spins on a triangle
rng = np.random.default_rng(0)
v = rng.normal(size=(1000, 3, 3)); v /= np.linalg.norm(v, axis=2)[:, :, None]
bonds = np.einsum('nk,nk->n', v[:, 0], v[:, 1]) + np.einsum('nk,nk->n', v[:, 1], v[:, 2]) + np.einsum('nk,nk->n', v[:, 2], v[:, 0])
tot = np.linalg.norm(v.sum(axis=1), axis=1)
check('fold, sum over the bonds = (S_tot^2 - 3S^2)/2 for random classical spins', np.allclose(bonds, (tot ** 2 - 3) / 2), True)
ang = 2 * np.pi / 3
v120 = np.array([[np.cos(k * ang), np.sin(k * ang), 0] for k in range(3)])
check('key box, at 120 degrees every bond has -S^2/2 and the triangle -3/2 J S^2',
      np.allclose([v120[i] @ v120[j] for i, j in ((0, 1), (1, 2), (2, 0))], -0.5) and abs(sum(
          v120[i] @ v120[j] for i, j in ((0, 1), (1, 2), (2, 0))) + 1.5) < 1e-12, True)
coll = [s1 * s2 + s2 * s3 + s3 * s1 for s1, s2, s3 in itertools.product((1, -1), repeat=3)]
check('key box and fold, the best collinear state has -J S^2, with |S_tot| = S', min(coll) == -1, min(coll))
best = bonds.min()
check('key box, no random state goes below -3/2 J S^2', best >= -1.5 - 1e-12, round(best, 4))
check('figure 6.3, the collinear state costs +J S^2 on the frustrated bond and -J S^2 in total, the 120 degree state is lower '
      'by half of that', abs((-1 - 1 + 1) + 1) < 1e-12 and abs((-1.5) - (-1) + 0.5 * 1) < 1e-12, True)

# the new schematic: the downloadable pyqula script, run again in a temporary folder
script = os.path.join(REPO, 'webnotes', 'scripts', 'session06', 'g3_triangular_meanfield.py')
cwd = os.getcwd()
with tempfile.TemporaryDirectory() as tmp:
    os.chdir(tmp)
    try:
        d = runpy.run_path(script)
        from pyqula import geometry
        # get_vev("mx") is n_up - n_dn along x: a chain in a large Zeeman field along x at half filling has 1 per site
        hc = geometry.chain().get_hamiltonian()
        hc.add_zeeman([5., 0., 0.])
        mxc = np.real(hc.get_vev("mx", nk=20))
        # a finer k-mesh, nk=12 instead of the default, for the guess of seed 1
        np.random.seed(1)
        hf, ef = d['g'].get_hamiltonian().get_mean_field_hamiltonian(U=10., mf="XY", mix=0.9, maxite=4000, nk=12,
                                                                     return_total_energy=True)
        mf = np.array([np.real(hf.get_vev(o, nk=12)) for o in ("mx", "my", "mz")]).T
        # the same four guesses with the tighter maxerror=1e-8 of the loop: the spread of the angles is where the loop stops
        tight = []
        for seed in range(4):
            np.random.seed(seed)
            ht, et = d['g'].get_hamiltonian().get_mean_field_hamiltonian(U=10., mf="XY", mix=0.9, maxite=4000, nk=8,
                                                                         maxerror=1e-8, return_total_energy=True)
            mt = np.array([np.real(ht.get_vev(o, nk=8)) for o in ("mx", "my", "mz")]).T
            st = np.linalg.norm(mt, axis=1)
            ct = np.array([mt[i] @ mt[j] / (st[i] * st[j]) for (i, j) in d['pairs']])
            tight.append((np.max(np.abs(np.degrees(np.arccos(np.clip(ct, -1., 1.))) - 120.)), st, et))
    finally:
        os.chdir(cwd)
check('schematic, get_vev("mx") is n_up - n_dn along x, so a full moment is 1', np.allclose(np.abs(mxc), 1, atol=1e-6), np.round(mxc, 4))
check('schematic, the cell of 3 x 3 sites has 27 first-neighbor bonds', len(d['pairs']) == 27, len(d['pairs']))
check('schematic, four random guesses', len(d['angles']) == 4, len(d['angles']))
dev = max(np.max(np.abs(x - 120.)) for x in d['angles'])
check('schematic, the angle between neighbors is 120 degrees within 0.2 degrees for every guess, at the default maxerror',
      dev < 0.2, round(dev, 3))
devt = max(x[0] for x in tight)
check('schematic, with maxerror=1e-8 the angle differs from 120 degrees by less than 0.001 degrees for the four guesses',
      len(tight) == 4 and devt < 0.001, f'{devt:.1e}')
check('schematic, with maxerror=1e-8 the length 0.922 and the energy -3.8085 per cell stay',
      all(np.all(np.round(x[1], 3) == 0.922) and abs(x[2] + 3.8085) < 1e-4 for x in tight), [round(x[2], 5) for x in tight])
sizes = np.concatenate([np.linalg.norm(m, axis=1) for m in d['moments']])
check('schematic, every moment has the length 0.922', np.all(np.round(sizes, 3) == 0.922), (round(sizes.min(), 5), round(sizes.max(), 5)))
check('schematic, the moments lie in the plane', max(np.abs(m[:, 2]).max() for m in d['moments']) < 1e-6, True)
check('schematic, the energy is -3.8085 per cell for each guess', all(abs(e + 3.8085) < 1e-4 for e in d['energies']),
      np.round(d['energies'], 5))
check('schematic, the length 0.922 and the energy do not change with nk=12',
      np.all(np.round(np.linalg.norm(mf, axis=1), 3) == 0.922) and abs(ef + 3.8085) < 1e-4, round(ef, 5))

# the lab box: the stored source, and our numbers
src = ' '.join(open(os.path.join(REPO, 'webnotes', 'sources', 'session06', 'helton2007_physrevlett.98.107204.txt'),
                    encoding='utf-8').read().split())
check('lab box, the source says S=1/2 kagome lattice antiferromagnet ZnCu3(OH)6Cl2', 'S=1/2 kagome lattice antiferromagnet' in src
      and 'ZnCu_3(OH)_6Cl_2' in src, 'found')
check('lab box, the source says a Curie-Weiss temperature of ~ -300 K and no magnetic order down to 50 mK',
      'The susceptibility indicates a Curie-Weiss temperature of ~ -300 K; however, no magnetic order is observed down to 50 mK.'
      in src, 'found')
check('lab box, the source suggests an unusual spin-liquid state with essentially gapless excitations',
      'These results suggest that an unusual spin-liquid state with essentially gapless excitations is realized' in src, 'found')
check('lab box, ours: 300 K over 50 mK is a factor of 6000', abs(300 / 0.050 - 6000) < 1e-9, 300 / 0.050)
z, Sq = 4, 0.5
check('lab box, ours: in mean field theta_CW = -z J S(S+1)/3, which is -J for the kagome lattice with S=1/2',
      abs(z * Sq * (Sq + 1) / 3 - 1) < 1e-12, z * Sq * (Sq + 1) / 3)

# the first quiz: J < 0, parallel spins give -|J| S^2 per bond and -3|J| S^2 per triangle; J > 0 at 120 degrees -J S^2/2
check('quiz 1, -|J|S^2 per parallel bond, -3|J|S^2 per triangle, -JS^2/2 per bond at 120 degrees and -JS^2 on a bipartite bond',
      abs(3 * (-1) + 3) < 1e-12 and abs(np.cos(ang) + 0.5) < 1e-12 and abs(np.cos(np.pi) + 1) < 1e-12, True)

# the picture quiz: the square and honeycomb patches have two colors, the triangular one has none
sys.path.insert(0, os.path.join(REPO, 'webnotes', 'figures', 'session06'))
import _g3_lattices
_g3_lattices.check()
nbrs = {k: max(np.bincount(np.array(_g3_lattices.patch(k)[1]).ravel())) for k in ('square', 'honeycomb')}
check('quiz 2, the square and honeycomb patches are bipartite and the triangular one is not; four and three neighbors',
      nbrs == {'square': 4, 'honeycomb': 3}, nbrs)
# the alt text of the honeycomb picture: four hexagons, counted as centers with six sites at one bond length and six bonds
Ph, Bh = _g3_lattices.patch('honeycomb')
bl, bset = 0.65, set(Bh)
cands = np.unique(np.round([p + bl * np.array([np.cos(w), np.sin(w)]) for p in Ph for w in np.radians(range(30, 360, 60))], 6), axis=0)
hexes = []
for cc in cands:
    ring = [k for k, p in enumerate(Ph) if abs(np.linalg.norm(p - cc) - bl) < 1e-6]
    if len(ring) == 6 and sum((i, j) in bset for i in ring for j in ring if i < j) == 6:
        hexes.append(cc)
check('quiz 2, alt text, the honeycomb patch has four whole hexagons', len(hexes) == 4, len(hexes))

# the third quiz: -3/2, -1 and the bound below
check('quiz 3, the three options -1.5, -1 and -3 J S^2, with the bound -3/2', min(coll) == -1 and best >= -1.5 - 1e-12 and -3 < -1.5, True)

# the problem: the energy per site of the 120 degree state and of the stripe state on a torus of the triangular lattice
Lt = 6
pos = [(i, j) for i in range(Lt) for j in range(Lt)]
idx = {p: k for k, p in enumerate(pos)}
tb = [(idx[(i, j)], idx[((i + di) % Lt, (j + dj) % Lt)]) for (i, j) in pos for di, dj in ((1, 0), (0, 1), (-1, 1))]


def energy(spins):
    return sum(spins[p] @ spins[q] for p, q in tb) / len(pos)


s120 = np.array([[np.cos(ang * ((i - j) % 3)), np.sin(ang * ((i - j) % 3)), 0] for (i, j) in pos])
stripe = np.array([[0, 0, 1 if j % 2 == 0 else -1] for (i, j) in pos])
par = [sum(1 for p, q in tb if (p == k or q == k) and stripe[p] @ stripe[q] > 0) for k in range(len(pos))]
check('problem, every site of the triangular lattice has 6 neighbors, 3 bonds per site', len(tb) == 3 * len(pos), len(tb) / len(pos))
check('problem, the 120 degree state has -3/2 J S^2 per site', abs(energy(s120) + 1.5) < 1e-12, energy(s120))
check('problem, the stripe state has 2 parallel and 4 antiparallel neighbors and -J S^2 per site',
      set(par) == {2} and abs(energy(stripe) + 1) < 1e-12, energy(stripe))
check('problem, the 120 degree state is lower by J S^2/2 per site', abs(energy(stripe) - energy(s120) - 0.5) < 1e-12,
      energy(stripe) - energy(s120))
tri = [(idx[(i, j)], idx[((i + 1) % Lt, j)], idx[(i, (j + 1) % Lt)]) for (i, j) in pos]
check('problem, every triangle of the 120 degree state has one site of each direction',
      all(abs(sum(s120[k] for k in t)).max() < 1e-12 for t in tri), True)

# the try-it box: the square lattice of the notebook at U=3, ferro guess minus antiferro guess about 0.3 per cell of four sites
with tempfile.TemporaryDirectory() as tmp:
    os.chdir(tmp)
    try:
        gsq = geometry.square_lattice_bipartite()
        (hfm, Ef) = gsq.get_hamiltonian().get_mean_field_hamiltonian(U=3.0, mf='ferro', mix=0.9, return_total_energy=True)
        (haf, Ea) = gsq.get_hamiltonian().get_mean_field_hamiltonian(U=3.0, mf='antiferro', mix=0.9, return_total_energy=True)
    finally:
        os.chdir(cwd)
check('try-it, E_ferro - E_antiferro on the square lattice at U=3 is about 0.3 per cell of four sites', abs((Ef - Ea) - 0.3) < 0.01,
      round(Ef - Ea, 4))
