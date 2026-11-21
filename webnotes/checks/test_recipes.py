"""Runs every recipe of webnotes/scripts/RECIPES.md and checks what the sentences under it state.

A recipe is a fenced python block under a heading of level two, and the heading is its name. Each block runs alone
in a temporary folder, since pyqula writes files. The script stops with the name of the recipe when a block raises,
when a block breaks a rule of the downloadable scripts (it imports pyqula, it imports no plotting package, it defines
no function and no class, it has at most 40 lines), or when a number of EXPECT does not hold. A recipe with no entry
in EXPECT is only run. It prints one line per recipe and exits 0 when all hold.

A few statements of the sentences take long runs with random starts, and the check scripts of the sessions assert
them in place of this script: |C| = 1 of the triplet superconductor on other starts (session05/conventions.py), and
the random start of the Hartree loop, |m| at T=3.5 of the Ising model and the errors of Hamiltonian learning over the
seeds 0 to 9 (session10/conventions.py). The linear algebra runs on one thread, since the matrices of the recipes are
small and several threads only cost time.

Run it from anywhere:  python3 webnotes/checks/test_recipes.py
One recipe:            python3 webnotes/checks/test_recipes.py Zak"""
import ast, os, re, sys, tempfile, time, traceback
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_v, '1')     # numpy reads this when it is imported
import numpy as np

WEBNOTES = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECIPES = os.path.join(WEBNOTES, 'scripts', 'RECIPES.md')


def recipes(path=RECIPES):
    """The list of (name, code, line) of the python blocks of the file, with the name of the heading above each."""
    out, name, block, start = [], None, None, 0
    for n, line in enumerate(open(path, encoding='utf-8').read().split('\n'), 1):
        if block is None:
            if line.startswith('## '):
                name = line[3:].strip()
            elif re.match(r'^```\s*python\s*$', line):
                block, start = [], n + 1
        elif line.startswith('```'):
            out.append((name, '\n'.join(block) + '\n', start))
            block = None
        else:
            block.append(line)
    return out


def rules(code):
    """The rules of a downloadable script that the block breaks, as a list of sentences."""
    tree = ast.parse(code)
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods.update(a.name.split('.')[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            mods.add((node.module or '').split('.')[0])
    bad = []
    if 'pyqula' not in mods:
        bad.append('it does not import pyqula')
    if mods & {'matplotlib', 'pylab', 'seaborn', 'plotly'}:
        bad.append('it imports a plotting package')
    if any(isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Lambda)) for node in ast.walk(tree)):
        bad.append('it defines a function or a class')
    if len([l for l in code.splitlines() if l.strip()]) > 40:
        bad.append('it has more than 40 lines')
    return bad


def run(code, name):
    """Runs one block in a temporary folder, and the entry of EXPECT for it in the same folder, since both call
    pyqula. Returns the statements that do not hold."""
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            d = {'__name__': '__recipe__'}
            exec(compile(code, name, 'exec'), d)
            return [what for what, ok in EXPECT[name](d) if not ok] if name in EXPECT else []
        finally:
            os.chdir(cwd)


def near(x, y, tol=1e-6):
    """True when every entry of x is within tol of y."""
    return bool(np.all(np.abs(np.asarray(x, complex) - np.asarray(y, complex)) < tol))


def bands_path(d):
    e = d['energies']
    yield 'two bands on 273 steps', e.shape == (273, 2) and len(d['k']) == 546 and d['k'][-1] == 272
    yield 'the bands are sorted and go from -3 to 3', np.all(e[:, 0] <= e[:, 1]) and near([e.min(), e.max()], [-3, 3])


def ribbon(d):
    E, Y, g = d['energies'], d['positions'], d['g']
    yield 'one row per momentum', E.shape == (201, len(g.r)) and Y.shape == E.shape
    yield 'the positions are inside the ribbon', g.y.min() < Y.min() and Y.max() < g.y.max()
    m = E.shape[1] // 2
    i = 110                                         # k = 0.05, where the two bands that cross the gap are inside it
    yield 'the two bands in the gap sit at opposite edges', (abs(E[i, m - 1]) < 0.45 and abs(E[i, m]) < 0.45
                                                             and Y[i, m - 1] * Y[i, m] < 0 and min(abs(Y[i, m - 1:m + 1])) > 0.8 * g.y.max())


def field(d):
    E, Y = d['energies'], d['positions']
    gaps = np.diff(E[100, :3])
    yield 'the lowest Landau levels are 0.24 apart', near(gaps, 0.24, 0.01) and abs(4 * np.pi * 0.02 - 0.24) < 0.02
    slope = np.gradient(E[:, 0])
    yield 'a positive slope sits at positive y', slope[160] > 0 and Y[160, 0] > 10 and slope[40] < 0 and Y[40, 0] < -10
    W = len(d['g'].r)
    harper = np.diag(-2 * np.cos(2 * np.pi * (d['kpath'][130][0] + 0.02 * d['g'].y))) - np.diag(np.ones(W - 1), 1) - np.diag(np.ones(W - 1), -1)
    yield 'the levels are those of the Harper chain', near(E[130], np.linalg.eigvalsh(harper), 1e-9)


def island(d):
    x, y, ldos, h = d['x'], d['y'], d['ldos'], d['h']
    es = np.linalg.eigvalsh(np.asarray(h.intra.todense() if hasattr(h.intra, 'todense') else h.intra))
    yield '834 sites', len(x) == 834 and len(ldos) == 834
    yield 'the sum is the density of states with Lorentzians', near(ldos.sum(), np.sum(0.03 / np.pi / (es ** 2 + 0.03 ** 2)), 1e-6)
    # distance of each site to the closest of the six sides of the flake
    ang = np.arctan2(y, x)[np.argmax(np.hypot(x, y))] + np.pi / 6 + np.arange(6) * np.pi / 3
    depth = np.max(np.outer(x, np.cos(ang)) + np.outer(y, np.sin(ang)), axis=1)
    edge = depth > depth.max() - 2.0
    yield '56 percent of the weight on 19 percent of the sites', near([ldos[edge].sum() / ldos.sum(), edge.mean()], [0.56, 0.19], 0.01)


def mesh_gap(d):
    yield 'the gap is 0.9', near(d['gap'], 0.9, 1e-9)
    yield 'h.get_gap() agrees here', near(d['h'].get_gap(), 0.9, 1e-6)


def berry_map(d):
    kx, ky, b, om = np.array(d['kx']), np.array(d['ky']), np.array(d['b']), d['omega']
    yield 'the average is the Chern number +1', near(d['average'], 1.0, 1e-5)
    yield 'the first index runs along kx', kx[0] == kx[1] and ky[0] != ky[1] and om[3, 5] == b[3 * 120 + 5]
    yield 'the window', near([kx.min(), ky.min()], [-1 / np.sqrt(3), -1.0], 1e-9)
    corner = 2.0 / 3.0                              # K and K' are at (0, 2/3) and (0, -2/3) in units of 2 pi over a
    iK, iKp = (np.argmin(np.abs(kx) + np.abs(ky - s * corner)) for s in (1, -1))
    yield 'positive at K and at K\', where it is largest', near([b[iK], b[iKp]], 84.2, 0.1) and b.max() < 1.02 * b[iK]


def chern(d):
    yield '+1 and 0', near(d['chern'], 1.0) and near(d['chern_staggered'], 0.0)
    h = d['g'].get_hamiltonian(has_spin=False)
    h.add_haldane(-0.1)
    yield '-1 for the opposite coupling', near(h.get_chern(nk=60), -1.0)
    h = d['g'].get_hamiltonian()
    h.add_haldane(0.1)
    yield '2 with the two spins', near(h.get_chern(nk=60), 2.0)


def hall(d):
    mu, s, h = d['mu'], np.array(d['sigma_xy']), d['h']
    yield 'one value per chemical potential', s.shape == mu.shape
    yield '+1 in the gap, as h.get_chern()', near(s[np.abs(mu) < 0.3], 1.0, 1e-4) and near(h.get_chern(nk=60), 1.0)
    yield 'zero when the bands are empty or full', abs(s[0]) < 1e-3 and abs(s[-1]) < 1e-3


def ssh(d):
    lv = d['levels']
    yield 'the gap of the infinite chain is 1', near(d['gap'], 1.0, 1e-3)
    yield '40 levels, two of them at 7e-7', len(lv) == 40 and near(np.abs(lv[19:21]), 7e-7, 1e-7)
    h = d['g'].get_hamiltonian(has_spin=False)
    h.inter = 0.5 * h.inter
    lv = np.sort(h.set_finite_system(n=20).get_bands()[1])
    yield 'none in the gap with the weak hopping between cells', near(np.abs(lv[19:21]), 0.51, 5e-3)


def zak(d):
    from pyqula import topology
    yield 'pi with the weak hopping inside the cell', near(d['zak'], np.pi, 1e-9)
    h = d['g'].get_hamiltonian(has_spin=False)
    h.inter = 0.5 * h.inter
    yield '0 with the weak hopping between cells', near(topology.berry_phase(h, nk=100), 0.0, 1e-9)
    signs = set()
    for nk in (20, 50, 100, 101):
        for t in (0.3, 0.5):
            h = d['g'].get_hamiltonian(has_spin=False)
            h.intra = t * h.intra
            signs.add(float(np.sign(topology.berry_phase(h, nk=nk))))
    yield 'pyqula returns both signs of pi', signs == {1.0, -1.0}


def qsh(d):
    nk, g = d['nk'], d['g']
    E, S, Y = (np.array(d[n]).reshape(nk, -1) for n in ('energy', 'spin', 'position'))
    yield 'spin between -1 and 1, position inside the ribbon', near([S.min(), S.max()], [-1, 1], 1e-6) and np.abs(Y).max() < g.y.max()
    yield 'the momentum goes from 0 to 2 pi', near([d['momentum'][0], d['momentum'][-1]], [0, 2 * np.pi], 1e-9)
    slope = np.gradient(E, axis=0)
    gapped = (np.abs(E) < 0.3) & (np.abs(Y) > 0.8 * g.y.max())
    out = {(e, s): np.sign(slope[gapped & (np.sign(Y) == e) & (np.sign(S) == s)]) for e in (1, -1) for s in (1, -1)}
    yield 'one state of each spin at each edge', all(len(v) > 20 for v in out.values())
    yield 'opposite slopes, spin up at positive y goes down', (np.all(out[1, 1] < 0) and np.all(out[1, -1] > 0)
                                                               and np.all(out[-1, 1] > 0) and np.all(out[-1, -1] < 0))


def z2(d):
    yield '-1 with the spin-orbit coupling and +1 with the staggered potential', d['z2'] == -1 and d['z2_staggered'] == 1


def conductance(d):
    from pyqula import heterostructures
    G, en = d['conductance'], d['energies']
    yield '2 inside the gap', near(G[np.abs(en) < 0.4], 2.0, 5e-3)
    h = d['g'].get_hamiltonian()
    h.add_sublattice_imbalance(0.45)
    ht = heterostructures.Heterostructure(h)
    yield '0 inside the gap of the staggered potential', abs(ht.landauer(energy=0.2)) < 1e-4


S3 = np.sqrt(3.0)
DELTA2 = np.array([[1.0, 0.0], [-0.5, S3 / 2], [-0.5, -S3 / 2]])     # the bonds from site 0 to site 1 of honeycomb_lattice


def notes_sign(d):
    from pyqula import geometry
    e, e3 = np.asarray(d['e']), np.asarray(d['e3'])
    yield 'one energy per momentum, 301 of them', len(e) == 301 and len(d['k']) == 301
    yield '-4, 0, 4 and -4 at Gamma, X, M and Gamma', near(e[[0, 100, 200, 300]], [-4, 0, 4, -4], 1e-12)
    p = np.asarray(d['kpath'])[:, :2] * 2 * np.pi
    yield 'the band of (2.14)', near(e, -2 * (np.cos(p[:, 0]) + np.cos(p[:, 1])), 1e-12)
    yield 'the cubic band from -6 to 6 on 201 steps', len(e3) == 201 and near([e3[0], e3[-1], e3.min(), e3.max()], [-6, 6, -6, 6], 1e-9)
    hp = d['g'].get_hamiltonian(has_spin=False)
    ep = np.asarray(hp.get_bands(kpath=d['kpath'])[1])
    yield 'upside down without tij', near(ep[[0, 100, 200]], [4, 0, -4], 1e-12)
    from pyqula.kpointstk.labels import label2k
    yield 'this tree takes "M" as (1/2,1/2) on the square lattice', near(label2k(d['g'], 'M'), [0.5, 0.5, 0], 1e-12)


def second_neighbor(d):
    from pyqula import geometry
    e, phi, ks = np.asarray(d['e']), d['phi'], d['ks']
    eq29 = -2 * np.cos(phi) - 0.6 * np.cos(2 * phi)
    yield 'the band is (2.9) with t=1 and eta=0.3', near(e, eq29, 1e-12)
    ep = np.asarray(d['g'].get_hamiltonian(has_spin=False, tij=[1.0, 0.3]).get_bands(kpath=[[k, 0., 0.] for k in ks])[1])
    yield 'tij=[1.0,0.3] gives minus this band', near(ep, -e, 1e-12)
    eo = np.asarray(d['g'].get_hamiltonian(has_spin=False, tij=[-1.0, 0.3]).get_bands(kpath=[[k, 0., 0.] for k in ks])[1])
    yield 'one sign changed is not (2.9)', np.abs(eo - eq29).max() > 1
    fine = np.linspace(-np.pi, np.pi, 200001)
    for eta, dip in ((0.3, 0.0333), (0.5, 0.5)):
        b = -2 * np.cos(fine) - 2 * eta * np.cos(2 * fine)
        i = np.argmax(b)
        yield 'the dip at pi for eta=%.1f' % eta, near(b.max() - b[-1], dip, 1e-4) and near(np.cos(fine[i]), -1 / (4 * eta), 1e-4)


def folding(d):
    ks, bands, g = d['ks'], d['bands'], d['g']
    phi = 2 * np.pi * ks
    ref = np.sort(np.array([[-2 * np.cos((p + 2 * np.pi * m) / 3) for m in range(3)] for p in phi]), axis=1)
    yield 'three folded cosines', bands.shape == (101, 3) and near(bands, ref, 1e-12)
    yield '-2, 1 and 1 at k=0', near(bands[50], [-2, 1, 1], 1e-12)
    yield 'three sites and the lattice vector 3', len(g.r) == 3 and near(g.a1, [3, 0, 0], 1e-12)
    yield '-1, -1 and 2 with the default', near(np.linalg.eigvalsh(g.get_hamiltonian(has_spin=False).get_hk_gen()([0, 0, 0])), [-1, -1, 2], 1e-12)
    yield 'six bands when spinful', g.get_hamiltonian().intra.shape == (6, 6)


def density(d):
    from pyqula import geometry
    e, dc, dh = np.asarray(d['e']), np.asarray(d['dos_chain']), np.asarray(d['dos_honeycomb'])
    i0, i15 = np.argmin(np.abs(e)), np.argmin(np.abs(e - 1.5))
    yield 'the grid holds 0 and 1.5', abs(e[i0]) < 1e-12 and abs(e[i15] - 1.5) < 1e-12
    yield 'the chain gives 0.159 and 0.241', near([dc[i0], dc[i15]], [1 / (2 * np.pi), 1 / (np.pi * np.sqrt(4 - 2.25))], 1e-4)
    ds = geometry.chain().get_hamiltonian().get_dos(energies=[0.0, 1.5], mode='Green', delta=1e-3)[1]
    yield 'twice with the default spinful Hamiltonian', near(ds, 2 * dc[[i0, i15]], 1e-4)
    yield 'D(E_F) is 0.159 for the half-filled chain', near(ds[0] / 2, 1 / (2 * np.pi), 1e-4)
    yield '0.041 at zero energy', near(dh[i0], 0.041, 1e-3) and dh[i0] < dh[i0 + 5] and dh[i0] < dh[i0 - 5]
    vh = [e[np.argmax(np.where(e > 0, dh, 0))], e[np.argmax(np.where(e < 0, dh, 0))]]
    yield 'the peaks are at 1 and -1', near(vh, [1, -1], 0.011)
    yield 'the total is 1.98', near(d['total'], 1.98, 0.005)


def band_map(d):
    kx, ky, band, nk = d['kx'], d['ky'], d['band'], d['nk']
    u = 2 * np.pi / np.sqrt(3)
    yield 'from -1 to 1 without the end, in units of 2 pi/sqrt3', near([kx[0, 0] / u, ky[0, 0] / u, kx[-1, 0] / u, ky[0, -1] / u],
                                                                       [-1, -1, 1 - 2 / nk, 1 - 2 / nk], 1e-12)
    yield 'the first index runs along kx', kx[1, 0] > kx[0, 0] and kx[0, 1] == kx[0, 0] and ky[0, 1] > ky[0, 0]
    f = np.abs(np.exp(1j * np.c_[kx.ravel(), ky.ravel()] @ DELTA2.T).sum(1)).reshape(nk, nk)
    yield 'the band is -|f(k)|', near(band, -f, 1e-9)
    i0, iK = nk // 2, nk // 2 + nk // 3
    yield '-3 at Gamma and 0 at (0, 2/3)', near([band[i0, i0], band[i0, iK]], [-3, 0], 1e-9) and near(ky[i0, iK] / u, 2 / 3, 1e-12)
    B = 2 * np.pi * np.linalg.inv(np.array([d['g'].a1[:2], d['g'].a2[:2]])).T
    yield 'the window holds 3.46 zones', near((2 * u) ** 2 / abs(np.linalg.det(B)), 2 * S3, 1e-12)
    from pyqula import geometry
    k2, e2 = geometry.kagome_lattice().get_hamiltonian(has_spin=False).get_bands_map(n=2, nk=12)
    a1, a2 = np.array([2.0, 0.0]), np.array([1.0, S3])
    ref = []
    for q in np.asarray(k2)[:, :2] * np.pi:
        c1, c2, c3 = np.cos(q @ a1 / 2), np.cos(q @ a2 / 2), np.cos(q @ (a2 - a1) / 2)
        ref.append(np.linalg.eigvalsh(2 * np.array([[0, c1, c2], [c1, 0, c3], [c2, c3, 0]]))[2])
    yield 'the unit is pi for kagome_lattice', near(e2, ref, 1e-9)


def fermi(d):
    x, y, w, nk, delta, h = np.asarray(d['x']), np.asarray(d['y']), np.asarray(d['w']), d['nk'], d['delta'], d['h']
    yield 'from -1 to 1 with both ends', near([x[0], x[-1], y[0], y[-1]], [-1, 1, -1, 1], 1e-12) and len(x) == nk * nk
    yield 'the first index runs along x', x[0] == x[1] and y[1] > y[0]
    u = 2 * np.pi / np.sqrt(3)
    f = np.abs(np.exp(1j * (u * np.c_[x, y]) @ DELTA2.T).sum(1))
    yield 'w is the sum of delta/((e-E)^2+delta^2)', near(w, delta / ((0.5 - f) ** 2 + delta ** 2) + delta / ((0.5 + f) ** 2 + delta ** 2), 1e-9)
    corners = [4 * np.pi / (3 * S3) * np.array([np.sin(t), np.cos(t)]) for t in np.arange(6) * np.pi / 3]
    P = u * np.c_[x, y][w > 0.5 * w.max()]
    dist = np.min(np.linalg.norm(P[:, None] - np.array(corners)[None], axis=2), axis=1)
    yield 'the rings at about 0.33 from the corners', near(np.median(dist), 1 / 3, 0.03)
    x0, y0, dz = h.get_fermi_surface(e=0.0, delta=delta, nk=nk)
    iK = np.argmin(np.abs(np.asarray(x0)) + np.abs(np.asarray(y0) - 2 / 3))
    yield '2/delta at a corner for e=0', near(dz[iK], 2 / delta, 1e-6) and near(y0[iK], 2 / 3, 1e-12)
    from pyqula import geometry
    _, _, dss = geometry.honeycomb_lattice().get_hamiltonian().get_fermi_surface(e=0.5, delta=delta, nk=nk)
    yield 'twice with the spinful Hamiltonian', near(dss, 2 * w, 1e-9)


def flat(d):
    from pyqula import geometry
    ek, el = d['e_kagome'], d['e_lieb']
    yield 'kagome flat at 2 and Lieb flat at 0', near(d['flat_kagome'], 2, 1e-12) and near(d['flat_lieb'], 0, 1e-12)
    yield 'the kagome bands between -4 and 2', near(ek[:, :2].min(), -4, 1e-12) and ek[:, :2].max() < 2 + 1e-12
    hk = geometry.kagome_lattice().get_hamiltonian(has_spin=False).get_hk_gen()
    yield 'kagome flat at -2 and lowest with the default', near([np.linalg.eigvalsh(hk([a, b, 0]))[0] for a in d['ks'][:6] for b in d['ks'][:6]], -2, 1e-12)
    hk = geometry.lieb_lattice().get_hamiltonian(has_spin=False).get_hk_gen()
    yield 'Lieb flat at 0 with the default', near([np.linalg.eigvalsh(hk([a, b, 0]))[1] for a in d['ks'][:6] for b in d['ks'][:6]], 0, 1e-12)
    yield 'bond 1 and lattice constant 2', all(near(np.linalg.norm(gg.a1), 2, 1e-12) and near(np.linalg.norm(gg.r[0] - gg.r[1]), 1, 1e-12)
                                               for gg in (geometry.lieb_lattice(), geometry.kagome_lattice()))
    yield 'the Lieb bands meet at (1/2,1/2)', near(el[15 * 30 + 15], 0, 1e-12)
    yield 'the kagome bands cross at -1 at (1/3,-1/3)', near(ek[10 * 30 + 20], [-1, -1, 2], 1e-12)
    from pyqula.kpointstk.labels import label2k
    yield 'which label2k calls K\'', near(label2k(geometry.kagome_lattice(), "K'"), [1 / 3, -1 / 3, 0], 1e-9)


def dirac(d):
    from pyqula.kpointstk.labels import label2k
    yield 'the slope is 1.5', near(d['velocity'], 1.5, 1e-3)
    hk, A, K, B = d['hk'], d['A'], d['K'], d['B']
    v, v2 = [], []
    for th in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        q = 1e-5 * np.array([np.cos(th), np.sin(th)])
        for KK, out in ((K, v), ((B[0] + B[1]) / 3, v2)):
            kr = A @ (KK + q) / (2 * np.pi)
            out.append(np.linalg.eigvalsh(hk([kr[0], kr[1], 0]))[1] / 1e-5)
    yield 'the same in every direction and at both corners', near(v, 1.5, 1e-4) and near(v2, 1.5, 1e-4)
    yield 'K is the label K, at (0, -4 pi/3 sqrt3)', near(K, [0, -4 * np.pi / (3 * S3)], 1e-12) and near(label2k(d['g'], 'K'), [-1 / 3, -1 / 3, 0], 1e-9)
    kp = np.asarray(d['g'].get_kpath(None, nk=400))
    marks = open('BANDLINES.OUT').read().split()
    yield 'the default path names (1/3,1/3) K', marks[3] == 'K' and near(float(marks[2]), 400 / 3, 1e-9) and near(kp[132][:2], [133 / 400] * 2, 1e-12)


def two_site(d):
    ks, bands, hk = d['ks'], d['bands'], d['hk']
    phi = 2 * np.pi * ks
    yield 'the bands are +-|1 + eta exp(-i phi)|', near(bands[:, 1], np.abs(1 + 0.6 * np.exp(-1j * phi)), 1e-12) and near(bands[:, 0], -bands[:, 1], 1e-12)
    yield 'hk is (2.13) entry by entry', all(np.allclose(hk([k, 0, 0]), [[0, 1 + 0.6 * np.exp(-2j * np.pi * k)], [1 + 0.6 * np.exp(2j * np.pi * k), 0]], atol=1e-12) for k in (0.1, 0.37))
    yield 'the gap is 0.8', near(d['gap'], 0.8, 1e-12)
    yield 'the only intercell bond is h.inter[1,0]', near(np.asarray(d['h'].inter), [[0, 0], [0.6, 0]], 1e-12)
    h = d['g'].get_hamiltonian(has_spin=False)
    yield 'it closes for eta = 1', near(np.linalg.eigvalsh(h.get_hk_gen()([0.5, 0, 0])), 0, 1e-12)



def s01_chain_m(U, nk=20000):
    """The moment of the half-filled Hubbard chain in Hartree, converged on a mesh of nk cells."""
    k = 2 * np.pi * np.arange(nk) / nk
    m = 0.3
    for i in range(20000):
        new = np.mean((U * m / 2) / np.sqrt((U * m / 2) ** 2 + np.abs(1 + np.exp(1j * k)) ** 2))
        if abs(new - m) < 1e-13:
            break
        m = new
    return new


def s01_honeycomb_onset(nk, midpoint=False):
    """2/<1/|f_k|> of the honeycomb lattice on the nk x nk mesh of pyqula, or on a midpoint mesh."""
    k = 2 * np.pi * (np.arange(nk) + (0.5 if midpoint else 0.0)) / nk
    f = np.abs(1 + np.exp(1j * k)[:, None] + np.exp(1j * k)[None, :])
    return 2 / np.mean(1 / f)


def s01_open_chain(d):
    N, levels, lowest = d['N'], d['levels'], d['lowest']
    n = np.arange(1, N + 1)
    yield 'the levels are 2 cos(n pi/(N+1))', near(levels, np.sort(2 * np.cos(n * np.pi / (N + 1))), 1e-12)
    yield 'the spacing at the center is 0.569', near(d['spacing'], 4 * np.sin(np.pi / (2 * (N + 1))), 1e-12) and near(d['spacing'], 0.569, 1e-3)
    plus = np.linalg.eigh(np.asarray(d['h'].intra))[1][:, 0]
    yield 'with +1 the lowest state changes sign on every bond', np.all(plus[:-1] * plus[1:] < 0)
    yield 'with -1 it has one sign', np.all(lowest * lowest[0] > 0)
    box = 2 * np.sin(np.pi * n / (N + 1)) ** 2 / (N + 1)
    yield 'its weight is the box in both cases', near(lowest ** 2, box, 1e-12) and near(plus ** 2, box, 1e-12)
    spinful = d['g'].get_hamiltonian()
    yield 'with spin every level comes twice', near(np.linalg.eigvalsh(np.asarray(spinful.intra)), np.repeat(levels, 2), 1e-12)


def s01_dimer(d):
    Us, m, gap, E, exact = d['Us'], np.array(d['moment']), np.array(d['gap']), np.array(d['energy']), d['exact']
    below = Us < 2
    yield 'the moment is below 1e-3 up to U=2', np.all(m[below] < 1e-3)
    yield 'and sqrt(1-4/U^2) above, 0.745 at U=3 and 0.866 at U=4', (near(m[~below], np.sqrt(1 - 4 / Us[~below] ** 2), 1e-3)
                                                                     and near([m[Us == 3][0], m[Us == 4][0]], [0.745, 0.866], 1e-3))
    yield 'the gap is max(2, U)', near(gap, np.maximum(2, Us), 1e-3)
    yield 'the energy is -2+U/2 and then -2/U', near(E, np.where(below, -2 + Us / 2, -2 / np.maximum(Us, 1e-9)), 1e-4)
    yield 'it stays above the exact energy, -0.83 at U=4', np.all(E >= exact - 1e-9) and near(exact[Us == 4], -0.83, 5e-3)
    hm = d['h'].get_mean_field_hamiltonian(U=4.0, mf="antiferro", mix=0.9)
    yield 'negative on the first site with the guess antiferro', np.real(hm.get_vev("mz"))[0] < -0.8
    U = 4.0
    H = np.array([[0, 0, -1, -1], [0, 0, 1, 1], [-1, 1, U, 0], [-1, 1, 0, U]], float)   # two electrons with Sz=0, hopping 1
    yield 'exact is the singlet, sqrt(U^2/4+4)-U/2 below the triplet at zero', near(np.linalg.eigvalsh(H)[:2], [exact[Us == 4][0], 0], 1e-12)


def s01_afm_chain(d):
    from scipy.optimize import brentq
    m, U, g = np.real(d['m']), d['U'], d['g']
    yield 'm is -0.621 and +0.621', near(m, [-0.621, 0.621], 1e-3) and near(m, [-s01_chain_m(U), s01_chain_m(U)], 2e-4)
    yield 'the gap is U|m| = 1.862', near(d['gap'], U * abs(m[0]), 2e-3) and near(d['gap'], 1.862, 2e-3)
    yield 'the energy per cell is -1.190', near(d['energy'], -1.190, 1e-3)
    yield 'the field is -U m/2, +0.931 where m is -0.621', near(np.real(d['field']), -U * m / 2, 2e-3) and near(np.real(d['field'])[0], 0.931, 2e-3)
    h0, e0 = g.get_hamiltonian().get_mean_field_hamiltonian(U=0., nk=100, return_total_energy=True)
    yield 'the energy is -8/pi at U=0', near(e0, -8 / np.pi, 2e-3)
    h2 = g.get_hamiltonian().get_mean_field_hamiltonian(U=2., mf="antiferro", mix=0.5, nk=100)
    on = np.real(np.diag(dense(h2.intra)))
    k = 2 * np.pi * (np.arange(4000) + 0.5) / 4000
    ref = 2 * brentq(lambda D: 2.0 * np.mean(1 / (2 * np.sqrt((2 * np.cos(k)) ** 2 + D ** 2))) - 1, 1e-6, 5)
    yield 'the onsite energies hold U|m| = 0.681 at U=2, the gap equation', (near(on[0] - on[1], -(on[2] - on[3]), 1e-6)
                                                                             and near(abs(on[0] - on[1]), ref, 1e-3) and near(ref, 0.681, 1e-3))
    h4, e4 = g.get_hamiltonian().get_mean_field_hamiltonian(U=4., mf="antiferro", nk=40, mix=0.9, return_total_energy=True)
    yield 'at U=4 m is -+0.769, the gap 3.076 and the energy -0.938', (near(np.real(h4.get_vev("mz", nk=40)), [-0.769, 0.769], 5e-4)
                                                                       and near(h4.get_gap(), 3.076, 1e-3) and near(e4, -0.938, 5e-4))
    np.random.seed(2)
    hx, ex = g.get_hamiltonian().get_mean_field_hamiltonian(U=4., mf="XY", nk=40, mix=0.9, return_total_energy=True)
    mx = np.array([np.real(hx.get_vev(o, nk=40)) for o in ("mx", "my", "mz")]).T
    yield 'mf="XY" gives the same |m|, gap and energy in the plane', (near(np.linalg.norm(mx, axis=1), 0.769, 5e-4) and near(mx[:, 2], 0, 1e-6)
                                                                      and near(hx.get_gap(), 3.076, 1e-3) and near(ex, e4, 5e-5))
    hb = d['h']
    inter = [dense(t.m) for t in hb.get_multicell().hopping if tuple(t.dir) == (1, 0, 0)][0]
    yield 'the two hoppings of bichain are equal', near(dense(hb.intra).real[0, 2], 1.0) and near(np.abs(inter).max(), 1.0)
    h8 = g.get_hamiltonian().get_mean_field_hamiltonian(U=1.0, mf="antiferro", mix=0.5)
    yield 'the default nk=8 gives 0.192 at U=1 against 0.0299', near(abs(np.real(h8.get_vev("mz", nk=8))[0]), 0.192, 1e-3) and near(s01_chain_m(1.0), 0.0299, 1e-4)
    h1 = g.get_hamiltonian().get_mean_field_hamiltonian(U=1., mf="antiferro", nk=1001, mix=0.9)
    yield 'after a loop with nk=1001, 0.030, get_vev with no nk reads 0.050', (near(abs(np.real(h1.get_vev("mz", nk=1001))[0]), 0.030, 5e-4)
                                                                               and near(abs(np.real(h1.get_vev("mz"))[0]), 0.050, 5e-4))


def s01_honeycomb(d):
    m = np.real(d['m'])
    yield 'm is -+0.444 at U=3', near(np.abs(m), 0.444, 1e-3) and m[0] * m[1] < 0
    yield 'the gap is U|m| = 1.33, at K', near(d['gap'], 3 * abs(m[0]), 1e-3) and near(d['gap'], 1.33, 5e-3)
    gen = d['hmf'].get_hk_gen()
    yield 'the smallest gap is at K', near(2 * np.min(np.abs(np.linalg.eigvalsh(gen([1 / 3, 1 / 3, 0])))), d['gap'], 1e-6)
    yield 'U_c = 2.23 on a dense mesh', 2.225 < s01_honeycomb_onset(1200, midpoint=True) < 2.235
    yield 'the onset is 2.375 for nk=10 and 2.29 for nk=20', near(s01_honeycomb_onset(10), 2.375, 1e-3) and near(s01_honeycomb_onset(20), 2.29, 5e-3)
    k = 2 * np.pi * np.arange(30) / 30
    f = np.abs(1 + np.exp(1j * k)[:, None] + np.exp(1j * k)[None, :])
    lo, hi = 1e-9, 5.0
    for i in range(200):                            # bisection of 1 = (U/2) <1/sqrt(Delta^2 + |f|^2)> at U=2
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if np.mean(1 / np.sqrt(mid ** 2 + f ** 2)) > 1 else (lo, mid)
    yield 'nk=30 holds K and gives 0.015 at U=2', f.min() < 1e-12 and near(lo, 0.015, 5e-4)


def s01_cdw(d):
    V = d['V']
    yield 'the Fock term gives 0.704 and the hopping 1.725', near(d['imbalance_hf'], 0.704, 1e-3) and near(d['hopping_hf'], 1.725, 1e-3)
    inter = [np.abs(np.asarray(t.m)).max() for t in d['hf'].get_multicell().hopping if any(t.dir)]
    yield 'on both bonds', near(max(inter), d['hopping_hf'], 1e-6)
    yield 'Hartree alone gives 0.892, the moment of U=2V', near(d['imbalance_hartree'], 0.892, 1e-3) and near(d['imbalance_hartree'], s01_chain_m(2 * V), 2e-4)
    yield 'the hopping stays 1 in Hartree', near(abs(d['hartree'].intra[0, 1]), 1.0, 1e-9)
    yield 'the gap is 2V dn in both', near(d['hf'].get_gap(), 2 * V * d['imbalance_hf'], 3e-3) and near(d['hartree'].get_gap(), 2 * V * d['imbalance_hartree'], 3e-3)
    yield 'one electron per cell', near(np.sum(np.real(d['n_hf'])), 1.0, 1e-9)
    from pyqula import meanfield, geometry
    yield 'the guess CDW is +-1', near(np.real(np.diag(np.asarray(meanfield.guess(d['h'], "CDW")))), [1, -1], 1e-12)
    try:
        geometry.bichain().get_hamiltonian().get_mean_field_hamiltonian(V1=V, mf="CDW", compute_cross=False, nk=8)
        refused = False
    except TypeError:
        refused = True
    yield 'the spinful call refuses compute_cross', refused
    yield 'no file with write=False', os.listdir('.') == []
    d['h'].get_mean_field_hamiltonian(V1=V, mf="CDW", filling=0.5, mix=0.5, nk=8)
    yield 'MF.pkl without write=False', os.path.isfile('MF.pkl')


def s01_seed(d):
    yield 'the moment follows the field at U=1, 0.002', near(d['moments'][0], 0.002, 1e-4)
    yield 'and stays at 0.866 at U=4', near(d['moments'][1], 0.866, 1e-3)
    h = d['g'].get_hamiltonian()
    h.add_antiferromagnetism(0.1)
    yield '+b on the spin up of the first site', near(np.real(np.diag(np.asarray(h.intra))), [0.1, -0.1, -0.1, 0.1], 1e-12)


def s01_swave(d):
    from scipy.optimize import brentq
    from pyqula import geometry
    delta = float(np.max(d['delta']))
    yield 'delta is 0.931, 3 times 0.310', near(delta, 0.931, 2e-3) and near(delta / 3, 0.310, 1e-3)
    yield 'the gap is 2|Delta| = 1.862', near(d['gap'], 2 * delta, 3e-3) and near(d['gap'], 1.862, 3e-3)
    yield 'the gap of the antiferromagnet at U=+3', near(d['gap'], 3 * s01_chain_m(3.0), 3e-3)
    gen, anom = d['hk'], 0
    for x in np.arange(400) / 400:
        e, v = np.linalg.eigh(dense(gen([x, 0, 0])))
        occ = v[:, e < 0]
        anom += np.sum(np.conj(occ[2]) * occ[0]) / 400
    D = complex(d['hmf'].intra[0, 2])
    yield 'hmf.intra[0, 2] is U <c_dn c_up>, real and +0.931, so <c_dn c_up> = -0.310', (near(D, -3 * anom, 1e-4) and near(D, 0.931, 2e-3)
                                                                                         and near(anom, -0.310, 1e-3))
    hc = geometry.bichain().get_hamiltonian().get_mean_field_hamiltonian(U=-3.0, mf="CDW", mix=0.5, nk=50)
    yield 'a CDW guess gives 0.379 and 1.621 with the same gap', near(np.sort(np.real(hc.get_vev(operator=None, nk=50))), [0.379, 1.621], 1e-3) and near(hc.get_gap(), d['gap'], 3e-3)
    out = []
    for U in (-1.0, -1.5, -2.0, -1.0):
        h = geometry.chain().get_hamiltonian()
        h.setup_nambu_spinor()
        out.append(h.get_mean_field_hamiltonian(U=U, filling=0.1, nk=100, mix=0.5, mf='swave'))
    pair = [complex(x.intra[0, 2]) for x in out]
    yield 'filling 0.1 gives 0.103, 0.223 and 0.361 at U=-1, -1.5 and -2, real', near(pair[:3], [0.1031, 0.2226, 0.3606], 1e-4)
    yield 'the same on every run', abs(pair[3] - pair[0]) < 1e-9
    gen, anom, dens = out[0].get_hk_gen(), 0, 0
    for x in np.arange(400) / 400:
        e, v = np.linalg.eigh(dense(gen([x, 0, 0])))
        occ = v[:, e < 0]
        anom += np.sum(np.conj(occ[2]) * occ[0]) / 400
        dens += np.sum(np.abs(occ[0]) ** 2 + np.abs(occ[1]) ** 2) / 400
    yield 'Delta is U <c_dn c_up> at 0.2 electrons per site', near(-anom, pair[0], 1e-4) and near(dens, 0.2, 2e-3)
    kb = 2 * np.pi * (np.arange(4000) + 0.5) / 4000

    def number(Dv):
        return brentq(lambda mu: np.mean(1 - (2 * np.cos(kb) - mu) / np.sqrt((2 * np.cos(kb) - mu) ** 2 + Dv ** 2)) - 0.2, -12, 12)
    bcs = brentq(lambda Dv: np.mean(1 / (2 * np.sqrt((2 * np.cos(kb) - number(Dv)) ** 2 + Dv ** 2))) - 1, 1e-4, 5)
    yield 'the BCS gap equation at the same density', near(bcs, pair[0].real, 2e-4)


def dense(m):
    return np.asarray(m.todense() if hasattr(m, 'todense') else m)


def peaks(e, d, lo, hi, rel=0.2):
    """The energies of the local maxima of d between lo and hi that are above rel times the largest one there."""
    w = (e > lo) & (e < hi)
    top = d[w].max()
    return np.array([e[i] for i in range(1, len(e) - 1) if w[i] and d[i] > d[i - 1] and d[i] >= d[i + 1] and d[i] > rel * top])


def loop_fluxes(g, phi, sides):
    """The loop phase over 2 pi of every square (sides=4) or hexagon (sides=6) with its center in one cell of the
    periodic geometry g with add_orbital_magnetic_field(phi), counterclockwise, from a 3 x 3 tiling of the cell built
    with the hoppings <i,0|H|j,R> of pyqula."""
    h = g.get_hamiltonian(has_spin=False)
    h.add_orbital_magnetic_field(phi)
    hm = h.get_multicell()
    T = {tuple(int(round(v)) for v in t.dir[:2]): dense(t.m) for t in hm.hopping}
    T[(0, 0)] = dense(hm.intra)
    a1, a2, n = np.array(g.a1[:2]), np.array(g.a2[:2]), len(g.r)
    cells = [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1)]
    pos = np.array([g.r[s, :2] + c[0] * a1 + c[1] * a2 for c in cells for s in range(n)])
    Hb = np.zeros((9 * n, 9 * n), complex)
    for A, c1 in enumerate(cells):
        for B, c2 in enumerate(cells):
            R = (c2[0] - c1[0], c2[1] - c1[1])
            if R in T:
                Hb[A * n:(A + 1) * n, B * n:(B + 1) * n] = T[R]
    rad = 1 / (2 * np.sin(np.pi / sides))
    dirs = np.array([[np.cos(a), np.sin(a)] for a in np.arange(24) * np.pi / 12])
    cand = np.unique(np.round((pos[:, None, :] + rad * dirs[None]).reshape(-1, 2), 6), axis=0)
    inv, mid, out = np.linalg.inv(np.array([a1, a2]).T), g.r[:, :2].mean(0), []
    for c in cand:
        f = inv @ (c - mid)
        d = np.linalg.norm(pos - c, axis=1)
        ring = np.where(np.abs(d - rad) < 1e-6)[0]
        if not np.all((f > -0.5) & (f <= 0.5)) or len(ring) != sides or d.min() < 0.5 * rad:
            continue
        ring = ring[np.argsort(np.arctan2(pos[ring, 1] - c[1], pos[ring, 0] - c[0]))]
        out.append(np.angle(np.prod([Hb[ring[(k + 1) % sides], ring[k]] for k in range(sides)])) / (2 * np.pi))
    return np.array(out)


def landau_chern(d):
    from pyqula import geometry
    yield 'the levels are -3.70, -3.12 and -2.58', near(d['levels'], [-3.698, -3.118, -2.584], 2e-3)
    yield 'chern is +1', near(d['chern'], 1, 1e-6)
    yield 'sigma_xy is 0, 1 and 2', near(np.array(d['sigma_xy'], float), [0, 1, 2], 2e-3)
    g = d['g']
    h = g.get_hamiltonian(has_spin=False)
    h.add_orbital_magnetic_field(-1 / 20)
    h.add_onsite(-0.5 * (d['levels'][0] + d['levels'][1]))
    yield 'the opposite field gives -1', near(h.get_chern(nk=20), -1, 1e-6)
    fl = loop_fluxes(geometry.square_lattice().get_supercell((1, 10)), 0.013, 4)
    yield 'with 0.013 in the cell of 10 sites one plaquette has 0.117 of the opposite sign', (np.sum([near(f, -0.013, 1e-9) for f in fl]) == 9
                                                                                          and np.sum([near(f, 0.117, 1e-9) for f in fl]) == 1)


def dos_bulk(d):
    e, dos, bulk = d['e'], d['dos'], d['dos_bulk']
    yield 'the integral is 19.96 and 15.97 with the bulk operator', near([np.trapezoid(dos, e), np.trapezoid(bulk, e)], [19.96, 15.97], 0.006)
    pk = peaks(e, bulk, -4, -3.3)
    yield 'the peaks are at -3.875, -3.630 and -3.395', near(pk, [-3.875, -3.630, -3.395], 1e-3)
    x = np.arange(50)
    lat = np.linalg.eigvalsh(np.diag(-2 * np.cos(2 * np.pi * (x - 25) / 50)) - np.eye(50, k=1) - np.eye(50, k=-1))[:3]
    yield 'the lattice levels are -3.876, -3.633 and -3.397', near(lat, [-3.876, -3.633, -3.397], 1e-3) and near(pk, lat, 3e-3)
    yield 'the spacings are 0.245 and 0.235, below 0.251', near(np.diff(pk), [0.245, 0.235], 1e-3) and abs(4 * np.pi * 0.02 - 0.251) < 1e-3


def dirac_levels(d):
    e, dos = d['e'], d['dos']
    pk = peaks(e, dos, 0.05, 0.8, rel=0.05)
    pm = peaks(e, dos, -0.8, -0.05, rel=0.05)
    yield 'l_B is 4.0 and E_1 is 0.53', near(1 / np.sqrt(2 * np.pi * 0.01), 4.0, 0.015) and near(d['E1'], 0.53, 0.005)
    yield 'the peaks are at 0, +-0.52 and +-0.715', (near(peaks(e, dos, -0.05, 0.05), [0], 3e-3) and near(pk, [0.52, 0.715], 4e-3)
                                                    and near(pm, [-0.715, -0.52], 4e-3))
    yield 'the lattice lowers them by about 0.1 (E/t)^2', all(0.07 < (1 - p / c) / p ** 2 < 0.12 for p, c in zip(pk, d['E1'] * np.sqrt([1, 2])))
    first = []
    for phi in (0.005, 0.02):
        h = d['g'].get_hamiltonian(has_spin=False)
        h.add_orbital_magnetic_field(phi)
        (e2, d2) = h.get_dos(energies=e, delta=1e-2, nk=100, operator="bulk")
        first.append(peaks(e2, d2, 0.1, 0.8, rel=0.05)[0])
    yield 'the fields 0.005 and 0.02 put the first peak at 0.37 and 0.71, a factor 1.92', near(first, [0.37, 0.71], 6e-3) and near(first[1] / first[0], 1.92, 0.03)


def ldos_ribbon(d):
    x, y, ldos, h = np.array(d['x']), np.array(d['y']), np.array(d['ldos']), d['h']
    (e, dd) = h.get_dos(energies=np.array([0.53 / 3]), delta=1e-2, nk=50)
    yield '1600 entries and the sum over one cell is the density of states, 1.06', (len(x) == 1600 and near(ldos.sum() / 20, dd[0], 1e-3 * dd[0])
                                                                                  and near(dd[0], 1.06, 0.005))
    yield 'l_B is 4.0, and 25 percent of the sites hold 57 percent of the weight', near([d['lB'], d['edge'].mean(), d['fraction']], [3.99, 0.25, 0.57], 0.01)
    out = []
    for ew in (0.53 * 2 / 3, 0.0, 0.53):
        (x2, y2, l2) = (np.array(a) for a in h.get_ldos(e=ew, nrep=20, delta=1e-2, nk=50))
        edge = np.abs(y2 - np.mean(y2)) > (np.max(y2) - np.min(y2)) / 2 - d['lB']
        out.append(l2[edge].sum() / l2.sum())
    yield '54 percent at 0.353, 4 at zero energy and 16 at 0.53', near(out, [0.54, 0.04, 0.16], 0.01)


def island_field(d):
    lv, lv2, x, y, ldos = d['levels'], d['levels2'], np.array(d['x']), np.array(d['y']), np.array(d['ldos'])
    yield '834 levels, the same in both gauges to 1e-12', len(lv) == 834 and near(lv, lv2, 1e-12)
    ang = np.arctan2(y, x)[np.argmax(np.hypot(x, y))] + np.pi / 6 + np.arange(6) * np.pi / 3
    depth = np.max(np.outer(x, np.cos(ang)) + np.outer(y, np.sin(ang)), axis=1)
    edge = depth > depth.max() - 2.0
    yield '37 percent of the weight on 19 percent of the sites', near([ldos[edge].sum() / ldos.sum(), edge.mean()], [0.37, 0.19], 0.01)
    (x0, y0, l0) = d['h'].get_ldos(e=0.0, delta=0.03)
    yield '9 percent at zero energy', near(np.array(l0)[edge].sum() / np.array(l0).sum(), 0.09, 0.01)
    gap = lv[(lv > 0.05) & (lv < 0.48)]
    yield 'a ladder of edge levels about 0.06 apart below the first bulk level at 0.51', (len(gap) > 5 and near(np.mean(np.diff(gap)), 0.06, 0.01)
                                                                                        and near(np.median(lv[(lv > 0.49) & (lv < 0.53)]), 0.515, 0.01))
    from pyqula import geometry
    gr = geometry.square_ribbon(20)
    lev = []
    for kw, phi in (({'gauge': 'symmetric'}, 0.03), ({}, 0.015)):
        h = gr.get_hamiltonian(has_spin=False)
        h.add_orbital_magnetic_field(phi, **kw)
        gen = h.get_hk_gen()
        lev.append(np.sort(np.concatenate([np.linalg.eigvalsh(dense(gen([k, 0, 0]))) for k in np.linspace(0, 1, 30)])))
    yield 'on the square ribbon the symmetric gauge is the Landau gauge with half the field', near(lev[0], lev[1], 1e-10)


def chern_gap(d):
    from pyqula import geometry
    g, phi = d['g'], d['phi']
    yield 'phi is 0.0096 and chern is +1', near(phi, 0.00962, 1e-5) and near(d['chern'], 1, 1e-6)
    h = g.get_hamiltonian(has_spin=False)
    h.add_orbital_magnetic_field(phi)
    e = np.sort(np.linalg.eigvalsh(dense(h.get_hk_gen()([0.1, 0.2, 0.]))))
    m = len(e) // 2
    yield 'the first level is at 0.509', near(e[m + 1:m + 3], 0.509, 1e-3)
    cs = []
    for c in (0.25, -0.6):
        hh = g.get_hamiltonian(has_spin=False)
        hh.add_orbital_magnetic_field(phi)
        hh.add_onsite(c)
        cs.append(hh.get_chern(nk=8))
    hh = g.get_hamiltonian(has_spin=False)
    hh.add_haldane(0.07)
    yield 'the gap below the zero level has -1, the gap above the first level +3, and add_haldane(0.07) gives +1', near(cs + [hh.get_chern(nk=8)], [-1, 3, 1], 1e-6)
    sq = geometry.honeycomb_lattice_square_cell()
    rot, unr = sq.rotate(90).get_supercell((10, 1)), sq.get_supercell((1, 10))
    area = lambda gg: abs(np.linalg.det(np.array([gg.a1[:2], gg.a2[:2]])))
    ok = {}
    for name, gg, F in (('rot', rot, 1), ('rot', rot, 0.5), ('unr', unr, 2), ('unr', unr, 1)):
        ok[(name, F)] = near(loop_fluxes(gg, F / area(gg), 6), -F / area(gg) * 1.5 * np.sqrt(3), 1e-9)
    yield 'any whole number of flux quanta in this cell and an even number in the other one', (ok[('rot', 1)] and not ok[('rot', 0.5)]
                                                                                              and ok[('unr', 2)] and not ok[('unr', 1)])


def haldane_path(d):
    c = np.array(d['closest'])
    yield 'closest is never below 0.198, which it reaches at nu = 1', near(c.min(), 0.198, 1e-3) and np.argmin(c) == 10
    g, central = d['g'], d['central']
    lows = []
    for hal, fl, on in ((-0.07, 0.01, -0.2), (0.07, -0.01, -0.2), (0.07, 0.01, 0.2)):
        Hq = g.get_hamiltonian(has_spin=False); Hq.add_orbital_magnetic_field(fl); Hq.add_onsite(on)
        Hc = g.get_hamiltonian(has_spin=False); Hc.add_haldane(hal)
        g1, g2 = Hq.get_hk_gen(), Hc.get_hk_gen()
        low = 9.0
        for k in np.linspace(-0.5, 0.5, 41):
            m1, m2 = dense(g1([k, 0, 0])), dense(g2([k, 0, 0]))
            for nu in np.linspace(0, 1, 11):
                e, v = np.linalg.eigh(nu * m1 + (1 - nu) * m2)
                low = min(low, np.abs(e[np.sum(np.abs(v[central]) ** 2, axis=0) > 0.5]).min())
        lows.append(low)
    yield 'the gap closes with add_haldane(-0.07), with the field -0.01 and with add_onsite(+0.2)', all(l < 0.01 for l in lows)
    Hq = g.get_hamiltonian(has_spin=False); Hq.add_orbital_magnetic_field(0.01)
    mix = dense((Hq * 0.5 + g.get_hamiltonian(has_spin=False) * 0.5).intra)
    top = int(np.argmax(g.y))
    mods = sorted(abs(mix[top, j]) for j in range(len(g.r)) if abs(np.linalg.norm(g.r[j] - g.r[top]) - 1) < 1e-6)
    yield 'at nu = 0.5 a bond at the edge has the modulus 0.86', near(mods[0], 0.86, 0.005) and mods[0] < 0.99


def domain_wall(d):
    from pyqula import geometry
    g, E, Y = d['g'], d['energies'], d['positions']
    h2 = g.get_hamiltonian(has_spin=False)

    def mufun(r):
        return 3.5 if r[1] > 0. else -3.5
    h2.add_onsite(mufun)
    yield 'the array gives the same onsite energies as the function of the notebook', near(np.diag(dense(d['h'].intra)), np.diag(dense(h2.intra)), 1e-12)
    yield 'the halves have +3.5 above y = 0 and -3.5 below', near(np.diag(dense(h2.intra))[g.y > 0], 3.5, 1e-12) and near(np.diag(dense(h2.intra))[g.y < 0], -3.5, 1e-12)
    cnt = {'wall': 0, 'top': 0, 'bottom': 0}
    for n in range(E.shape[1]):
        for j in np.where(np.diff(np.sign(E[:, n])) != 0)[0]:
            cnt['wall' if abs(Y[j, n]) < 15 else ('top' if Y[j, n] > 0 else 'bottom')] += 1
    yield 'four crossings at the wall and two at each outer edge', cnt == {'wall': 4, 'top': 2, 'bottom': 2}
    cs = []
    for c in (3.5, -3.5):
        hq = geometry.square_lattice().get_supercell((1, 50)).get_hamiltonian(has_spin=False)
        hq.add_orbital_magnetic_field(0.02)
        hq.add_onsite(c)
        cs.append(hq.get_chern(nk=10))
    yield 'C is +2 above and -2 below', near(cs, [2, -2], 1e-6)


def sc_kitaev(N, t, mu, D):
    """The BdG matrix of (5.19) on an open chain, in the basis (c_1..c_N, c_1^dag..c_N^dag), d[n+1,n] = D = -d[n,n+1]."""
    h = -mu * np.eye(N) - t * (np.eye(N, k=1) + np.eye(N, k=-1))
    d = D * (np.eye(N, k=-1) - np.eye(N, k=1))
    return np.block([[h, d], [d.conj().T, -h.T]])


def sc_mesh(h, nk):
    """The BdG energies of a Hamiltonian of two dimensions on the nk x nk mesh of reduced momenta, one row per momentum."""
    hk = h.get_hk_gen()
    ks = np.arange(nk) / nk
    return np.array([np.linalg.eigvalsh(np.asarray(hk([kx, ky, 0.]))) for kx in ks for ky in ks])


def sc_bands(d):
    from pyqula import geometry
    E, W = d['energies'], d['weights']
    k = 2 * np.pi * np.linspace(-0.5, 0.5, d['nk'])
    eps = 2 * np.cos(k) - 1
    Eq = np.sqrt(eps ** 2 + 0.09)
    yield 'four BdG states per momentum in pairs +-E', E.shape == (201, 4) and near(np.sort(E, axis=1), np.c_[-Eq, -Eq, Eq, Eq], 1e-9)
    iF = np.argmin(np.min(np.abs(E), axis=1))
    yield 'the smallest energy is Delta=0.3 near k=1/6', near(d['smallest'], 0.3, 2e-3) and abs(abs(d['kpath'][iF][0]) - 1 / 6) < 0.01
    yield 'the branches are 0.6 apart', near(np.sort(E, axis=1)[:, 2].min() - np.sort(E, axis=1)[:, 1].max(), 0.6, 4e-3)
    yield 'the electron weight of +E is (1+eps/E)/2, 1/2 at the Fermi momenta', (near(W[:, -1], (1 + eps / Eq) / 2, 1e-9)
                                                                                 and near(W[iF, -1], 0.5, 0.05)
                                                                                 and near(W.min(), 0, 0.02) and near(W.max(), 1, 0.02))
    h = d['g'].get_hamiltonian()
    h.add_onsite(-1.0); h.add_swave(0.0)
    e0 = np.sort(np.linalg.eigvalsh(h.get_hk_gen()([0.1, 0, 0])))
    yield 'without pairing the hole band is the mirror', near(e0, np.sort([eps[120], eps[120], -eps[120], -eps[120]]), 1e-9)
    hq = geometry.square_lattice().get_hamiltonian()
    hq.set_filling(0.2, nk=20); hq.setup_nambu_spinor(); hq.add_swave(0.8)
    kq, eq, cq = hq.get_bands(operator="electron", nk=800)
    yield 'the square lattice of the notebook gives 0.8', near(np.min(np.abs(eq)), 0.8, 1e-3)
    M = dense(d['h'].intra)
    yield 'Delta at (0,2) and (1,3) of h.intra, and get_gap is 2 Delta', (near(M[[0, 1], [2, 3]].real, 0.3, 1e-12)
                                                                        and near(np.abs(M[[0, 1], [3, 2]]), 0, 1e-12) and near(d['h'].get_gap(), 0.6, 1e-6))
    hx = d['g'].get_hamiltonian()
    hx.add_onsite(-1.0); hx.add_exchange([0., 0., 0.7]); hx.add_swave(0.3)
    yield 'the exchange enters the hole block as (J, -J), the onsite energy with the other sign', near(np.real(np.diag(dense(hx.intra))), [-0.3, -1.7, 1.7, 0.3], 1e-12)


def sc_pairing(d):
    P, ks = d['pairing'], d['ks']
    kc = 2 * np.pi * ks
    want = 0.2 * (np.cos(kc)[:, None] - np.cos(kc)[None, :])
    yield 'the entry is 2 delta (cos kx - cos ky), first index along kx', near(P, want, 1e-12)
    yield '-0.4 at X and zero on the diagonals', near(P[40, 20], -0.4, 1e-12) and near(np.diag(P), 0, 1e-12)
    from pyqula import geometry
    out = {}
    for mode in ('extended_swave', 'swave', 'chiral_pwave'):
        h = geometry.square_lattice().get_hamiltonian()
        h.add_pairing(mode=mode, delta=0.1)
        out[mode] = h.get_hk_gen()([0.1, 0.3, 0.0])
    kx, ky = 2 * np.pi * 0.1, 2 * np.pi * 0.3
    z = np.sin(kx) + 1j * np.sin(ky)
    yield 'extended_swave, swave and chiral_pwave', (near(out['extended_swave'][0, 2].real, 0.2 * (np.cos(kx) + np.cos(ky)), 1e-12)
                                                    and near(out['swave'][0, 2].real, 0.1, 1e-12)
                                                    and abs(out['chiral_pwave'][0, 2] + 0.2j * z) < 1e-12
                                                    and abs(out['chiral_pwave'][1, 3] - 0.2j * z) < 1e-12)


def sc_triplet(d):
    from scipy.optimize import minimize
    from pyqula import geometry, superconductivity
    yield '|C| = 1', near(abs(d['chern']), 1.0, 1e-6)
    kinds = superconductivity.identify_superconductivity(d['hscf'])
    yield 'only up-up triplet pairing', ('up-up pairing' in kinds and 'down-down pairing' not in kinds
                                         and 'up-down pairing' not in kinds and 'Spin-triplet superconductivity' in kinds)
    yield 'the gap on the mesh of 60 is 0.375', near(d['gap'], 0.3748, 5e-4)
    hk = d['hk']
    i = np.argmin(d['e'][:, 2])
    x0 = [d['ks'][i // 60], d['ks'][i % 60]]
    r = minimize(lambda x: np.linalg.eigvalsh(np.asarray(hk([x[0], x[1], 0.])))[2], x0, method='Nelder-Mead',
                 options=dict(xatol=1e-10, fatol=1e-13))
    yield 'a minimization gives 0.373 between the branches, 0.186 as the smallest energy', near(2 * r.fun, 0.3728, 5e-4) and near(r.fun, 0.186, 5e-4)
    # |C| = 1 on other random starts is asserted by webnotes/checks/session05/conventions.py, on four of them


def sc_dos(d):
    from pyqula import geometry
    e, D, De = d['e'], d['dos'], d['dos_e']
    yield 'dos integrates to about 4 and is symmetric', near(np.trapezoid(D, e), 4.0, 0.03) and near(D, D[::-1], 1e-8)
    yield 'dos_e integrates to about 2', near(np.trapezoid(De, e), 2.0, 0.015)
    w = (e > 0) & (e < 0.6)
    wm = (e < 0) & (e > -0.6)
    yield 'coherence peaks at +-0.31', near(e[w][np.argmax(De[w])], 0.31, 0.006) and near(e[wm][np.argmax(De[wm])], -0.31, 0.006)
    yield 'only tails inside the gap, 0.024 at E=0 against 0.87', near(De[400], 0.024, 1e-3) and near(De[w].max(), 0.87, 0.005)
    hi, lo = (e > 0.7) & (e < 1.5), (e < -2.5)
    yield 'the band edges at 1.03 and -3.0, higher than the coherence peaks', (near(e[hi][np.argmax(De[hi])], 1.03, 0.015)
                                                                               and near(e[lo][np.argmax(De[lo])], -3.0, 0.02)
                                                                               and min(De[hi].max(), De[lo].max()) > De[w].max())
    h = geometry.chain().get_hamiltonian()
    h.set_filling(0.2, nk=20); h.add_swave(0.8)
    es = np.linspace(-5., 5., 1001)
    d1 = np.array(h.get_dos(energies=es, delta=1e-2, nk=1000)[1])
    d2 = np.array(h.get_dos(energies=es, operator="electron", delta=1e-2, nk=1000)[1])
    de = es[1] - es[0]
    yield 'the notebook cell gives 3.993, 1.996 and the peaks at +-0.81', (near([d1.sum() * de, d2.sum() * de], [3.993, 1.996], 1e-3)
                                                                         and near(es[np.argmax(d1 * (es > 0))], 0.81, 1e-9)
                                                                         and near(es[np.argmax(d1 * (es < 0))], -0.81, 1e-9))


def sc_chern(d):
    from functools import partial
    from pyqula import geometry
    from pyqula.sctk.pairing import get_triplet
    from pyqula.utilities import get_callable
    yield '-2 and 0', near(d['chern'], -2.0) and near(d['chern_s'], 0.0)
    out = []
    for x in (3.0, -3.0):
        h = geometry.square_lattice().get_hamiltonian()
        h.add_onsite(x); h.add_pairing(mode='chiral_pwave', delta=0.25)
        out.append(h.get_chern())
    yield '+2 and -2 on the square lattice', near(out, [2.0, -2.0])
    h = d['g'].get_hamiltonian()
    h.add_onsite(-3.0); h.add_pairing(mode='chiral_pwave', delta=-0.4)
    yield 'the sign of delta does not change it', near(h.get_chern(), -2.0)
    try:
        h = d['g'].get_hamiltonian()
        h.add_pairing(mode='chiral_pwave', delta=0.4, L=-1)
        raised = False
    except TypeError:
        raised = True
    yield 'L=-1 raises a TypeError', raised
    h = d['g'].get_hamiltonian()
    h.add_onsite(-3.0)
    h.add_pairing(mode=partial(get_triplet, df=get_callable([0., 0., 1.]), L=-1), delta=0.4)
    yield 'the pairing with L=-1 through partial gives +2', near(h.get_chern(), 2.0)


def sc_crossings(E, Y, E0):
    """Crossings of the level E0 by one sorted band between neighboring momenta, the last joined to the first, as
    counts of (edge, direction), with the edge the sign of y and the direction the sign of the change of energy."""
    out = {(1, 1): 0, (1, -1): 0, (-1, 1): 0, (-1, -1): 0}
    for i in range(E.shape[0]):
        j = (i + 1) % E.shape[0]
        for n in range(E.shape[1]):
            a, b = E[i, n] - E0, E[j, n] - E0
            if a * b < 0:
                out[(int(np.sign(Y[i, n])), int(np.sign(b - a)))] += 1
    return out


def sc_edge(d):
    from functools import partial
    from pyqula import geometry
    from pyqula.sctk.pairing import get_triplet
    from pyqula.utilities import get_callable
    E, Y, gr = d['energies'], d['positions'], d['gr']
    yield 'one row per momentum and positions inside the ribbon', E.shape[0] == 200 and np.abs(Y).max() < np.abs(gr.y).max()
    k0 = np.argmin(np.abs(np.array(d['kpath'])[:, 0]))
    inside = np.abs(E) < 1.0
    inside[k0] = False
    yield 'the states inside the gap sit at the edges away from k=0', inside.sum() > 0 and np.abs(Y[inside]).min() > 0.6 * gr.y.max()
    yield 'at k=0 the two edges meet at +-0.0012', near(np.sort(np.abs(E[k0]))[:4], 0.00119, 2e-5)
    want = {(1, 1): 0, (1, -1): 2, (-1, 1): 2, (-1, -1): 0}
    yield 'two branches per edge, down at positive y', sc_crossings(E, Y, 0.5) == want and sc_crossings(E, Y, -0.5) == want
    h = gr.get_hamiltonian()
    h.add_onsite(-3.0)
    h.add_pairing(mode=partial(get_triplet, df=get_callable([0., 0., 1.]), L=-1), delta=0.4)
    ik, e, y = h.get_bands(operator='yposition', kpath=d['kpath'])
    E2, Y2 = np.array(e).reshape(200, -1), np.array(y).reshape(200, -1)
    rev = {(1, 1): 2, (1, -1): 0, (-1, 1): 0, (-1, -1): 2}
    yield 'the other chirality reverses both', sc_crossings(E2, Y2, 0.5) == rev
    h = gr.get_hamiltonian()
    h.add_onsite(-3.0); h.add_swave(1.0)
    ik, e, y = h.get_bands(operator='yposition', kpath=d['kpath'])
    yield 'the s-wave ribbon keeps 1.0', near(np.abs(e).min(), 1.0, 1e-3)
    hb = geometry.triangular_lattice().get_hamiltonian()
    hb.add_onsite(-3.0); hb.add_pairing(mode='chiral_pwave', delta=0.4)
    eb = sc_mesh(hb, 90)
    yield 'the bulk keeps 1.34', near((eb[:, 2].min() - eb[:, 1].max()) / 2, 1.336, 2e-3)


def sc_kitaev_open(d):
    from pyqula import geometry
    lv = np.sort(d['levels'])
    low = lv[np.argsort(np.abs(lv))[:40]]
    yield 'the 40 levels closest to zero are (5.19) with t=1, mu=1, Delta=0.5', near(np.sort(low), np.sort(np.linalg.eigvalsh(sc_kitaev(20, 1, 1, 0.5))), 1e-9)
    yield 'end modes at 1.9e-5, first bulk level 0.83', near(d['splitting'], 1.94e-5, 1e-7) and near(np.sort(np.abs(lv))[2], 0.835, 0.002)
    out = {}
    for (L, onsite2, delta, dv) in ((8, -1.0, 0.5, [1., 0., 0.]), (12, 0.0, 1.0, [1., 0., 0.]), (40, -2.5, 0.5, [1., 0., 0.]),
                                    (20, -1.0, 0.5, [1., 1., 0.]), (40, -1.0, 0.5, [1., 0., 0.])):
        g = geometry.chain().get_supercell(L)
        g.dimensionality = 0
        h = g.get_hamiltonian()
        h.add_onsite(4.0); h.add_exchange([0., 0., 4.]); h.add_onsite(onsite2)
        h.add_pairing(mode='pwave', delta=delta, d=dv)
        out[(L, onsite2, delta, tuple(dv))] = np.sort(np.abs(h.get_bands()[1]))
    yield '0.011 for L=8', near(out[(8, -1.0, 0.5, (1., 0., 0.))][0], 0.0111, 5e-5)
    yield 'a factor 0.58 per site from L=20 to 40', (near((out[(40, -1.0, 0.5, (1., 0., 0.))][0] / d['splitting']) ** (1 / 20), 0.58, 0.01)
                                                    and near(np.sqrt(0.5 / 1.5), 0.58, 0.01))
    yield 'zero at Delta=t and mu=0', out[(12, 0.0, 1.0, (1., 0., 0.))][1] < 1e-13
    yield '0.51 in the trivial chain of 40 sites', near(out[(40, -2.5, 0.5, (1., 0., 0.))][0], 0.511, 1e-3)
    yield 'd=[1,1,0] gives sqrt(2) delta', near(out[(20, -1.0, 0.5, (1., 1., 0.))][:6:2], np.sort(np.abs(np.linalg.eigvalsh(sc_kitaev(20, 1, 1, 0.5 * np.sqrt(2)))))[:6:2], 1e-9)
    hb = geometry.chain().get_hamiltonian()
    hb.add_onsite(4.0); hb.add_exchange([0., 0., 4.]); hb.add_onsite(-1.0)
    hb.add_pairing(mode='pwave', delta=0.5, d=[1., 0., 0.])
    yield 'set_finite_system gives the same chain', near(np.sort(hb.set_finite_system(n=20).get_bands()[1]), lv, 1e-9)


def sc_ldos_end(d):
    vals = [x[100] for x in d['ldos']]
    yield 'the energy grid holds E=0', abs(d['energies'][100]) < 1e-12
    yield '4.427, 0.0843 and 0.0081 at E=0', near(vals, [4.427, 0.0843, 0.0081], [1e-3, 1e-4, 1e-4])
    E, V = np.linalg.eigh(sc_kitaev(100, 1.0, 0.0, 0.2))
    yield 'the bulk levels start near 0.4', near(np.sort(np.abs(E))[2], 0.4, 0.01)
    spinless = np.sum(np.abs(V[50, :]) ** 2 * 0.02 / np.pi / (E ** 2 + 0.02 ** 2))
    yield 'the spin-up band adds 1e-4 in the middle', 5e-5 < vals[2] - spinless < 2e-4


def sc_rashba(d):
    yield 'the gap at Gamma is 0.124 and 0.176', near(d['gaps'], [np.hypot(0.3, 0.3) - 0.3, 0.6 - np.hypot(0.3, 0.3)], 1e-9) and near(d['gaps'], [0.124, 0.176], 1e-3)
    yield 'the Chern number goes from 0 to 1', near(d['cherns'], [0.0, 1.0])
    h = d['g'].get_hamiltonian()
    h.add_onsite(-5.7); h.add_rashba(1.0); h.add_swave(0.3)
    e0 = np.linalg.eigvalsh(h.get_hk_gen()([0., 0., 0.]))
    kk, e, c = h.get_bands(nk=1000, operator='sx', kpath=['M1', 'G', 'M1'])
    yield 'at J=0 the smallest energy is 0.3 on the pocket and 0.424 at Gamma', near(np.abs(e).min(), 0.3, 1e-3) and near(np.abs(e0).min(), 0.4243, 1e-4)
    h = d['g'].get_hamiltonian()
    h.add_onsite(-5.7); h.add_rashba(1.0); h.add_zeeman([0., 0., np.hypot(0.3, 0.3)]); h.add_swave(0.3)
    yield 'the closing at 0.424', np.abs(np.linalg.eigvalsh(h.get_hk_gen()([0., 0., 0.]))).min() < 1e-12


def sc_zak(d):
    yield 'pi inside the range and 0 outside', near(d['phases'], [np.pi, 0.0], 1e-6)
    from pyqula import topology
    phases = []
    for mu in (0.0, 1.0, 1.5):
        h = d['g'].get_hamiltonian()
        h.add_onsite(4.0); h.add_exchange([0., 0., 4.]); h.add_onsite(-mu)
        h.add_pairing(mode='pwave', delta=0.3, d=[1., 0., 0.])
        phases.append(topology.berry_phase(h, nk=200))
    yield 'pi modulo 2 pi for other mu inside the range', near(np.abs(phases), np.pi, 1e-6)
    h = d['g'].get_hamiltonian()
    h.add_onsite(4.0); h.add_exchange([0., 0., 4.]); h.add_onsite(-1.0)
    h.add_pairing(mode='pwave', delta=0.3, d=[1., 0., 0.])
    yield 'get_topological_invariant is the same', near(abs(h.get_topological_invariant()), np.pi, 1e-6)


def fm_vs_afm(d):
    from pyqula import geometry
    yield 'the difference is 0.1995 and the product 3.990 at U=20', near(d['difference'], 0.1995, 5e-5) and near(d['product'], 3.990, 5e-4)
    g = geometry.bichain()
    (hf, ef) = g.get_hamiltonian().get_mean_field_hamiltonian(U=40., mf="ferro", nk=20, mix=0.9, return_total_energy=True)
    (ha, ea) = g.get_hamiltonian().get_mean_field_hamiltonian(U=40., mf="antiferro", nk=20, mix=0.9, return_total_energy=True)
    yield 'the difference is 0.0999 and the product 3.998 at U=40', near(ef - ea, 0.0999, 5e-5) and near(40 * (ef - ea), 3.998, 1e-3)
    yield 'the ferromagnet has m = -1', near(np.real(d['hf'].get_vev("mz", nk=20)), -1, 1e-4)
    from pyqula.meanfield import guess
    yield 'the guess is the field +0.1 sigma_z', near(np.real(np.diag(np.array(guess(g.get_hamiltonian(), "ferro")))), [0.1, -0.1, 0.1, -0.1], 1e-12)
    e = np.asarray(d['ha'].get_bands(nk=50)[1])
    yield 'the Fermi level of the mean-field Hamiltonian is at zero', np.sum(e < 0) == np.sum(e > 0) == len(e) // 2
    h6, e6 = g.get_hamiltonian().get_mean_field_hamiltonian(U=6., mf="ferro", mix=0.9, return_total_energy=True)
    yield 'at U=6 with the default nk the guess stops at |m| = 1/8 above the saturated ferromagnet', \
        near(np.abs(np.real(h6.get_vev("mz", nk=8))), 1 / 8, 1e-3) and e6 > 0.4


def seeded(d):
    from pyqula import geometry
    yield 'the loop stays at m = -1 with the energy 0', near(np.real(d['m']), -1, 1e-4) and abs(d['ef']) < 1e-6
    yield 'the paramagnet has -0.296 per cell', near(2 * (-4 / np.pi + 4.5 / 4), -0.296, 5e-4)
    g = geometry.bichain()
    out = {}
    for U, clean in ((3.9, True), (4.5, False)):
        h = g.get_hamiltonian()
        seed = h.copy()
        if clean:
            seed.clean()
        seed.add_zeeman([0., 0., U / 2])
        hs = h.get_mean_field_hamiltonian(U=U, mf=seed, nk=40, mix=0.9)
        out[(U, clean)] = np.abs(np.real(hs.get_vev("mz", nk=40))).max()
    yield 'at U=3.9 the seed goes back to the paramagnet', out[(3.9, True)] < 0.05
    yield 'without clean() the loop at U=4.5 ends at |m| = 0.075', near(out[(4.5, False)], 0.075, 1e-3)
    from scipy.optimize import brentq
    sp = []
    for b in (0.5, 0.2):
        h = g.get_hamiltonian()
        seed = h.copy(); seed.clean(); seed.add_antiferromagnetism(b)
        on = np.real(np.diag(dense(h.get_mean_field_hamiltonian(U=2.0, nk=100, mf=seed, filling=0.5, mix=0.9).intra)))
        sp.append(on[0] - on[1])
    yield 'a seed with add_antiferromagnetism(0.5) or 0.2 gives the same splitting 0.681', near(np.abs(sp), 0.681, 1e-3) and near(sp[0], sp[1], 5e-4)
    gs = geometry.square_lattice_bipartite()
    hs = gs.get_hamiltonian()
    st = hs.copy(); st.add_antiferromagnetism(0.3)
    x = np.real(np.diag(dense(st.intra))); x = x[0::2] - x[1::2]
    yield 'add_antiferromagnetism on square_lattice_bipartite is a stripe', (x[1] * x[2] > 0 and x[0] * x[1] < 0
                                                                            and near(gs.r[1][:2], [0.5, -0.5]) and near(gs.r[2][:2], [0.5, 0.5]))
    seed = hs.copy(); seed.clean(); seed.add_exchange(np.array([[0., 0., 0.3 * s] for s in (1, -1, 1, -1)]))
    dg = np.real(np.diag(dense(hs.get_mean_field_hamiltonian(U=2.5, nk=30, mf=seed, filling=0.5, mix=0.9).intra)))
    k = 2 * np.pi * (np.arange(100) + 0.5) / 100
    e2 = (2 * np.cos(k)[:, None] + 2 * np.cos(k)[None, :]) ** 2
    D = brentq(lambda D: 2.5 * np.mean(1 / (2 * np.sqrt(e2 + D ** 2))) - 1, 1e-6, 5)
    yield 'the checkerboard seed gives 1.20 at U=2.5, the gap equation', (near(abs(dg[0] - dg[1]), 2 * D, 2e-3) and near(2 * D, 1.20, 0.01)
                                                                         and dg[0] * dg[4] > 0 and dg[0] * dg[2] < 0)


def chain_fm(d):
    ms, e, sz = d['ms'], np.asarray(d['e']), np.asarray(d['sz'])
    yield 'ms is 0.007 at 1.2 and 0.200 at 2.4 and 3', near(ms[0], 0.007, 5e-4) and near(ms[1:], 0.2, 1e-4)
    yield 'the splitting is 0.6', near(d['splitting'], 0.6, 1e-3)
    yield 'sz is -1 on the filled band', near(sz[e < -1e-9], -1, 1e-6)
    yield 'the filled band runs from -0.382 to 0', near(e.min(), -0.382, 5e-4)
    hm = d['g'].get_hamiltonian().get_mean_field_hamiltonian(U=1.8, filling=0.1, mf="ferro", mix=0.9, nk=300)
    yield 'at U=1.8 the default mesh reads 0.13 and the loop mesh 0.087', \
        near(np.mean(np.abs(np.real(hm.get_vev("mz")))), 0.13, 5e-3) and near(np.mean(np.abs(np.real(hm.get_vev("mz", nk=300)))), 0.087, 5e-4)


def triangular(d):
    yield '27 bonds at 120 degrees within a quarter of a degree', len(d['pairs']) == 27 and near(d['angles'], 120, 0.25)
    yield 'every moment has the length 0.922', near(d['size'], 0.922, 5e-4)


def lieb(d):
    m, g = d['m'], d['g']
    yield 'the total is -1.000', near(d['total'], -1, 1e-3)
    yield 'the sites have -0.551, -0.551 and +0.102', near(np.sort(m), [-0.551, -0.551, 0.102], 5e-4)
    for U in (0.3, 2.):
        hm = g.get_hamiltonian().get_mean_field_hamiltonian(U=U, mf="ferro", mix=0.9)
        yield 'the total is -1.000 at U=%.1f' % U, near(np.sum(np.real(hm.get_vev("mz"))), -1, 1e-3)


def magnons(d):
    m, s = d['magnons'], d['spectra']
    yield 'the magnons are 0, 0.0618, 0.1414, 0.1902', near(m, [0, 0.0618, 0.1414, 0.1902], 5e-5)
    yield 'they are J|sin(pi Q)| with J = 0.2', near(m, [0.2 * abs(np.sin(np.pi * Q)) for Q in d['Qs']], 2e-4)
    yield 'the next energies are near U', all(18 < x[1] < 21 for x in s)


def honeycomb_magnons(d):
    e = d['energies']
    yield 'the bands lie between 0 and 6', near(e.min(), 0, 1e-9) and near(e.max(), 6, 1e-9) and near(e[0, 0], 0, 1e-9)
    hk = d['h'].get_hk_gen()
    eK = np.linalg.eigvalsh(hk([1 / 3, 1 / 3, 0.]))
    yield 'the gap at K is 0.90 = 6 sqrt3 x 0.0866', near(eK[1] - eK[0], 0.9, 1e-6) and near(6 * np.sqrt(3) * np.sqrt(3) / 2 * 0.1, 0.9, 1e-12)
    yield 'the gap 1.04 for t2 = 0.1', near(6 * np.sqrt(3) * 0.1, 1.04, 5e-3)


def magnon_chern(d):
    from pyqula import geometry
    yield 'get_chern gives 0 with every magnon positive', near(d['chern_all'], 0, 1e-9)
    yield 'chern is +1 after set_filling(0.5)', near(d['chern'], 1, 1e-6)
    h = geometry.honeycomb_lattice().get_hamiltonian(has_spin=False, tij=[-1.])
    h.add_haldane(-0.1); h.add_onsite(3.); h.set_filling(0.5)
    yield 'and -1 for add_haldane(-0.1)', near(h.get_chern(), -1, 1e-6)
    for x in (0.1, -0.1):
        hn = geometry.honeycomb_lattice().get_hamiltonian(tij=[1., 0.2])
        hn.add_haldane(x); hn.set_filling(0.0); hn.add_onsite(0.5)
        yield 'the notebook cell gives 0.0 for add_haldane(%+.1f)' % x, near(hn.get_chern(), 0, 1e-9)


def _s07_ff(hop, sites):
    """Entropy of a set of sites for the free fermions of the single-particle matrix hop, levels below zero filled."""
    w, v = np.linalg.eigh(hop)
    occ = v[:, w < 0]
    nu = np.linalg.eigvalsh((occ @ occ.T)[np.ix_(sites, sites)])
    nu = nu[(nu > 1e-13) & (nu < 1 - 1e-13)]
    return float(-np.sum(nu * np.log(nu) + (1 - nu) * np.log(1 - nu)))


def _s07_chain(t, ring=False):
    N = len(t) + (0 if ring else 1)
    h = np.zeros((N, N))
    for i, ti in enumerate(t):
        h[i, (i + 1) % N] = h[(i + 1) % N, i] = ti
    return h


def s07_block(d):
    S = d['S']
    yield 'S(10) is 1.4934, as for the infinite chain', abs(S[0] - 1.4934) < 5e-5
    yield 'the slope is 0.333 and the constant 0.727', abs(d['slope'] - 0.333) < 1e-3 and abs(d['const'] - 0.727) < 1e-3
    h = d['h']
    try:
        h.get_entanglement_entropy(region=list(range(10)), nsuper=1000)
        yield 'a ring of 1000 sites raises ValueError', False
    except ValueError as err:
        yield 'a ring of 1000 sites raises ValueError', 'A level sits at the Fermi energy' in str(err)
    hs = d['g'].get_hamiltonian()
    yield 'the default spinful Hamiltonian gives twice the entropy on a small ring', \
        abs(hs.get_entanglement_entropy(region=list(range(10)), nsuper=102)
            - 2 * h.get_entanglement_entropy(region=list(range(10)), nsuper=102)) < 1e-8


def s07_half(d):
    yield 'the left halves give 1.0492, 1.1677, 1.2848, 1.4011', near(d['S'], [1.0492, 1.1677, 1.2848, 1.4011], 5e-5)
    yield 'the slope is 0.169', abs(d['slope'] - 0.169) < 5e-4
    odd = (_s07_ff(_s07_chain([1.0] * 401), list(range(201))) - _s07_ff(_s07_chain([1.0] * 201), list(range(101)))) / np.log(402 / 202)
    yield 'with an odd number of sites in the half the slope is 0.163', abs(odd - 0.163) < 1e-3


def s07_dimerized(d):
    yield 'the three blocks give 0.4992, 0.9554, 1.4117', near([d['S_weak'], d['S_mixed'], d['S_strong']],
                                                               [0.4992, 0.9554, 1.4117], 5e-5)
    ring = _s07_chain([1.0 if i % 2 == 0 else 0.6 for i in range(200)], ring=True)
    yield 'a numpy ring of 200 sites gives the same', abs(_s07_ff(ring, list(range(40))) - d['S_weak']) < 1e-8 \
        and abs(_s07_ff(ring, list(range(1, 41))) - d['S_strong']) < 1e-8
    yield 'a block of 10 sites already has 0.4983', abs(d['h'].get_entanglement_entropy(region=list(range(10)), nsuper=100)
                                                        - 0.4983) < 5e-5


def s07_xx(d):
    yield 'the levels are J cos(pi k/7)', near(d['eps'], np.sort(np.cos(np.pi * np.arange(1, 7) / 7)), 1e-12)
    sx, sy = np.array([[0, 1], [1, 0]]) / 2, np.array([[0, -1j], [1j, 0]]) / 2

    def site(o, i):
        m = np.eye(1)
        for j in range(6):
            m = np.kron(m, o if j == i else np.eye(2))
        return m
    H = sum(site(s, i) @ site(s, i + 1) for i in range(5) for s in (sx, sy)).real
    ups = np.array([6 - bin(x).count('1') for x in range(64)])
    ok = all(near(np.linalg.eigvalsh(H[np.ix_(ups == N, ups == N)]), d['levels'][N], 1e-12) for N in range(7))
    yield 'levels[N] are the levels of the spins with S^z_tot = N - 3, 64 in all', ok and sum(len(v) for v in d['levels'].values()) == 64
    yield 'the ground energy is -1.7470', abs(d['ground'] + 1.7470) < 5e-5


def s07_dmrgpy(d):
    yield 'S agrees with S_free to 1e-6', near(d['S'], d['S_free'], 1e-6)
    yield 'ln 2 at the first cut and 0.7578 at the center', abs(d['S'][0] - np.log(2)) < 1e-6 and abs(d['S'][4] - 0.7578) < 5e-5
    yield 'the energy of the Heisenberg chain of 10 spins is -4.258035', abs(d['energy'] + 4.258035) < 1e-6


def s8_mesh(h, n):
    """All the levels of a pyqula Hamiltonian on the n x n mesh of reduced momenta that holds Gamma, K and M."""
    hk = h.get_hk_gen()
    ks = np.arange(n) / n
    return np.array([np.linalg.eigvalsh(hk([a, b, 0.])) for a in ks for b in ks])


def s8_triangular(t2, n=1200):
    """The band of triangular_lattice() with the hoppings 1 and t2, by hand, on an n x n mesh shifted off Gamma."""
    k = (np.arange(n) + 0.5) / n
    a, b = np.meshgrid(k, k, indexing='ij')
    c = lambda x: np.cos(2 * np.pi * x)
    return 2 * (c(a) + c(b) + c(a + b)) + 2 * t2 * (c(2 * a + b) + c(a + 2 * b) + c(a - b))


def s8_zero(h, t2):
    """The energy that set_filling moved to zero, from the level at Gamma, which is 6 + 6 t2 before the shift."""
    return 6 + 6 * t2 - np.linalg.eigvalsh(h.get_hk_gen()([0., 0., 0.]))[0]


def s8_kondo_fermions(h, n=40):
    """The fermions on the Kondo sites of an H2HFH Hamiltonian in the states below zero, per Kondo site."""
    hk, kondo = h.get_hk_gen(), np.repeat(np.asarray(h.geometry.r)[:, 2] > 0, 2)
    tot = 0.0
    for a in np.arange(n) / n:
        for b in np.arange(n) / n:
            e, v = np.linalg.eigh(hk([a, b, 0.]))
            tot += np.sum(np.abs(v[kondo][:, e < 0]) ** 2)
    return tot / n ** 2 / (kondo.sum() / 2)


def spinon_fermi_surface(d):
    from pyqula import geometry
    nk, kx, ky, w, fm, g = d['nk'], np.asarray(d['kx']), np.asarray(d['ky']), np.asarray(d['w']), d['fermi_map'], d['g']
    yield 'flat arrays from -1 to 1, the first index along kx', (len(kx) == nk * nk and kx[0] == kx[1] == -1 and ky[1] > ky[0]
                                                                and near([kx.max(), ky.max()], [1, 1], 1e-12) and fm[2, 5] == w[2 * nk + 5])
    B = 2 * np.pi * np.linalg.inv(np.array([g.a1[:2], g.a2[:2]])).T
    yield 'the window holds 3.46 zones', near((4 * np.pi) ** 2 / abs(np.linalg.det(B)), 2 * np.sqrt(3), 1e-9)
    yield 'at most 2/delta and close to it on the line', w.max() <= 2 / 0.1 + 1e-9 and w.max() > 0.5 * 2 / 0.1
    yield 'not symmetric under the exchange of kx and ky, and image is the transpose', (np.abs(fm - fm.T).max() > 0.3 * fm.max()
                                                                                       and near(d['image'], fm.T, 1e-12))
    yield 'it writes FERMI_MAP.OUT', os.path.isfile('FERMI_MAP.OUT')
    fills = {}
    for t2 in (-0.5, 0.0, 0.5):
        e = s8_triangular(t2)
        for nk_ in (10, 60, 101, 151):
            h = g.get_hamiltonian(tij=[1., t2])
            h.set_filling(0.5, nk=nk_)
            fills[t2, nk_] = np.mean(e < s8_zero(h, t2))
    yield 'nk=101 gives 0.500 to 0.002', all(abs(fills[t2, 101] - 0.5) < 2e-3 for t2 in (-0.5, 0.0, 0.5)) and abs(fills[0.5, 101] - np.mean(s8_triangular(0.5) < s8_zero(d['h'], 0.5))) < 1e-12
    move = max(abs(fills[t2, n] - 0.5) for t2 in (-0.5, 0.0, 0.5) for n in (101, 151))
    yield 'meshes of 100 to 150 points move it by about 0.002', 5e-4 < move < 2.5e-3
    yield 'nk=10 gives 0.513, 0.529 and 0.495', near([fills[-0.5, 10], fills[0.0, 10], fills[0.5, 10]], [0.513, 0.529, 0.495], 1e-3)
    yield 'nk=60 still 0.495 for t2=0.5', near(fills[0.5, 60], 0.495, 1e-3)


def kondo_bands(d):
    from pyqula import geometry
    from pyqula.specialhamiltonian import H2HFH
    E, W, h, k = d['energies'], d['weights'], d['h'], np.asarray(d['k'])
    yield 'four states per step', E.shape == (len(np.unique(k)), 4) and W.shape == E.shape
    yield 'the Kondo site above the conduction site', near(sorted(np.asarray(h.geometry.r)[:, 2]), [-0.5, 0.5], 1e-12)
    M = np.asarray(h.intra.todense() if hasattr(h.intra, 'todense') else h.intra)
    yield 'JK is the hopping between c and f, the f level at 0', near(M, [[-2, 0, 0.5, 0], [0, -2, 0, 0.5], [0.5, 0, 0, 0], [0, 0.5, 0, 0]], 1e-12)
    yield 'the direct gap 1.0 and the indirect gap 0.11 on the path', near((E[:, 2] - E[:, 1]).min(), 1.0, 2e-3) and near(E[:, 2].min() - E[:, 1].max(), 0.111, 2e-3)
    hk = h.get_hk_gen()
    top, bottom = np.linalg.eigvalsh(hk([0., 0., 0.]))[1], np.linalg.eigvalsh(hk([1 / 3., 1 / 3., 0.]))[2]
    yield 'between the lower band at Gamma and the upper band at K', near(top, E[:, 1].max(), 1e-9) and near(bottom, E[:, 2].min(), 1e-9)
    i = np.argmin(np.abs(E[:, 1] + E[:, 2] - 0) + np.abs(np.abs(E[:, 1]) - np.abs(E[:, 2])))
    yield 'the weight from 0 to 1, one half at the crossing', W.min() < 0.02 and W.max() > 0.98 and near(W[i, 1], 0.5, 0.03)
    zero_in_gap = []
    for ons in (-10., -3., -1., 6.):
        h2 = geometry.triangular_lattice().get_hamiltonian()
        h2.add_onsite(ons)
        E2 = s8_mesh(H2HFH(h2, JK=0.5), 30)
        zero_in_gap.append(E2[:, :2].max() < 0 < E2[:, 2:].min())
    yield 'zero inside the gap for any onsite energy', all(zero_in_gap)
    yield '0.48 fermions on the Kondo sites', near(s8_kondo_fermions(h), 0.48, 0.01)
    yield 'the square lattice holds one', near(s8_kondo_fermions(H2HFH(geometry.square_lattice().get_hamiltonian(), JK=0.5)), 1.0, 1e-9)
    h3 = geometry.triangular_lattice().get_hamiltonian()
    h3.add_onsite(-2.0)
    h3 = H2HFH(h3, JK=0.5)
    h3.add_onsite(1.0)
    M3 = np.real(np.diag(np.asarray(h3.intra.todense() if hasattr(h3.intra, 'todense') else h3.intra)))
    yield 'an add_onsite after H2HFH moves the Kondo level too', near(M3, [-1, -1, 1, 1], 1e-12)
    yield 'it writes BANDS.OUT', os.path.isfile('BANDS.OUT')


def kondo_exchange(d):
    from pyqula import geometry
    from pyqula.specialhamiltonian import H2HFH
    yield 'the direct gap 1.00 and the overlap 0.062', near(d['direct'], 1.0, 3e-3) and near(d['indirect'], -0.062, 1.5e-3)
    out = {}
    for J in (0.0, 0.05):
        h = geometry.triangular_lattice().get_hamiltonian()
        h.add_onsite(-4.0)
        e = s8_mesh(H2HFH(h, JK=0.5, J=J), 90)
        out[J] = e[:, 2].min() - e[:, 1].max()
    yield '0.154 at J=0 and -0.276 at J=0.05', near([out[0.0], out[0.05]], [0.154, -0.276], 1.5e-3)
    hf = H2HFH(geometry.triangular_lattice().get_hamiltonian(), JK=0.0, J=0.025)
    kondo = np.repeat(np.asarray(hf.geometry.r)[:, 2] > 0, 2)
    hk = hf.get_hk_gen()
    ks = (np.arange(200) + 0.5) / 200
    fl = np.array([np.linalg.eigvalsh(np.asarray(hk([a, b, 0.]))[np.ix_(kondo, kondo)]) for a in ks for b in ks])
    at = lambda q: np.linalg.eigvalsh(np.asarray(hk(q))[np.ix_(kondo, kondo)])
    width = at([0., 0., 0.]).max() - at([1 / 3., 1 / 3., 0.]).min()
    yield 'the Kondo band of width 9J, with zero at its filling 0.529', near(width, 9 * 0.025, 1e-12) and near(np.mean(fl < 0), 0.529, 1e-3)


def pi_flux(d):
    from pyqula import geometry
    hk, ks, gap, h = d['hk'], d['ks'], d['gap'], d['h']
    pts = np.random.default_rng(1).uniform(0, 1, (10, 2))
    err = max(abs(np.linalg.eigvalsh(hk([a, b, 0.]))[1] - 2 * np.sqrt(np.sin(2 * np.pi * a) ** 2 + np.cos(np.pi * b) ** 2)) for a, b in pts)
    yield 'the bands of this gauge', err < 1e-12
    dirac = sorted((float(ks[i]), float(ks[j])) for i, j in np.argwhere(gap < 1e-9))
    yield 'two Dirac points at (0, 1/2) and (1/2, 1/2)', dirac == [(0.0, 0.5), (0.5, 0.5)]
    top = max(np.abs(np.linalg.eigvalsh(hk([a, b, 0.]))).max() for a in ks for b in ks)
    yield 'from -2 sqrt 2 to 2 sqrt 2', near(top, np.sqrt(8), 1e-12)
    T = {tuple(int(c) for c in x.dir): np.asarray(x.m) for x in h.get_multicell().hopping}
    H0 = np.asarray(h.intra)
    y = np.asarray(h.geometry.r)[:, 1]
    lo, up = int(np.argmin(y)), int(np.argmax(y))
    phi = T[(1, 0, 0)][lo, lo] * H0[up, lo] * np.conj(T[(1, 0, 0)][up, up]) * H0[lo, up]
    yield 'the flux -1 on the plaquette', near(phi / abs(phi), -1, 1e-12)
    # the gauge of the figure spinon_bands, two sites along x, -1 along x and -(-1)^x along y
    Hfig = lambda kx, ky: np.array([[-2 * np.cos(ky), -(1 + np.exp(-2j * kx))], [-(1 + np.exp(2j * kx)), 2 * np.cos(ky)]])
    qx, qy = np.linspace(-np.pi / 2, np.pi / 2, 41)[1:], np.linspace(-np.pi, np.pi, 81)[1:]
    zf = sorted((round(a / np.pi, 6), round(b / np.pi, 6)) for a in qx for b in qy if np.diff(np.linalg.eigvalsh(Hfig(a, b)))[0] < 1e-9)
    same = np.allclose(sorted(np.linalg.eigvalsh(Hfig(0.3, 0.7))), sorted(np.linalg.eigvalsh(hk([(0.3 - np.pi / 2) / (2 * np.pi), 0.7 / np.pi, 0.]))))
    yield 'the figure has them at (pi/2, +-pi/2), with the same bands moved', zf == [(0.5, -0.5), (0.5, 0.5)] and same
    hz = geometry.square_lattice().get_supercell([2, 1]).get_hamiltonian(has_spin=False)
    hz.add_orbital_magnetic_field(0.5)
    E = s8_mesh(hz, 20)
    real = all(np.abs(np.imag(np.asarray(x.m))).max() < 1e-12 for x in hz.get_multicell().hopping)
    yield 'doubled along x the hoppings stay real, from -4 to 4', real and near([E.min(), E.max()], [-4, 4], 1e-9)


def spinon_chain(d):
    e2 = np.asarray(d['e2'])
    yield '|t| = J/pi', near(abs(d['t']), 1 / np.pi, 3e-4)
    yield 'one fermion per site', near(np.real(d['occupation']), 1.0, 1e-4)
    yield 'two flat bands at -0.5 and 0.5 with the two spins', (e2.shape == (51, 4) and near(e2[:, :2], -0.5, 2e-4)
                                                               and near(e2[:, 2:], 0.5, 2e-4))
    from pyqula import geometry
    from pyqula.spinon import SpinonHamiltonian
    phases = []
    for seed in (1, 2):
        np.random.seed(seed)
        hm = SpinonHamiltonian(geometry.chain()).get_mean_field_hamiltonian(J1=1.0, nk=200, decoupling="bond", integration="ed")
        m = [np.array(x.todense() if hasattr(x, "todense") else x) for dd, x in hm.get_multihopping().get_dict().items() if tuple(dd) == (1, 0, 0)][0]
        phases.append(np.angle(m[0, 0]))
    yield 'the phase changes from run to run', abs(np.angle(np.exp(1j * (phases[0] - phases[1])))) > 0.05


def kondo_scf(d):
    from pyqula import geometry
    from pyqula.kondolattice import KondoLatticeHamiltonian
    from scipy.optimize import brentq
    from scipy.special import ellipk, expit
    gap_eq = lambda JK: brentq(lambda g: 2 * JK / np.pi * ellipk(1 / (1 + g ** 2)) / np.sqrt(1 + g ** 2) - 1, 1e-6, 10.)
    yield 'gamma_K = 0.283, the gap equation, with one f fermion per site', near(d['gamma'], 0.2827, 1e-4) and near(d['gamma'], gap_eq(0.6), 2e-4) and near(np.real(d['nf']), 1.0, 1e-6)
    h = KondoLatticeHamiltonian(geometry.chain().get_hamiltonian(has_spin=True))
    hmf = h.get_mean_field_hamiltonian(J=1.6, filling=0.5, nk=400, mf=([0.3], [0.]), T=2e-3)
    yield '0.527 at J_K = 0.8', near(abs(hmf.hybridization[0]), 0.5270, 1e-4) and near(abs(hmf.hybridization[0]), gap_eq(0.8), 2e-4)
    gen, T = hmf.get_hk_gen(), hmf.temperature
    s = 0.0
    for k in np.arange(400) / 400:
        e, v = np.linalg.eigh(gen([k, 0., 0.]))
        s += sum(np.sum(expit(-e / T) * np.conj(v[a, :]) * v[2 + a, :]) for a in range(2))
    yield 'V = -(J/2) sum_s <c^dag_s f_s>', near(hmf.hybridization[0], -0.8 * s / 400, 1e-4)
    h0 = KondoLatticeHamiltonian(geometry.chain().get_hamiltonian(has_spin=True)).get_mean_field_hamiltonian(J=1.2, filling=0.5, nk=200, T=2e-3)
    yield 'the loop started from zero stays there', abs(h0.hybridization[0]) < 1e-9
    yield 'lambda zero at half filling and -1.12 at the filling 0.15', near(d['lam'], 0.0, 1e-6) and near(d['lam2'], -1.124, 1e-3)
    yield 'the field 0.374 at the filling 0.15, with one f per site and T=0.02', (near(abs(d['hmf2'].hybridization[0]), 0.374, 1e-3)
                                                                             and near(np.real(d['hmf2'].local_occupation[0]), 1.0, 1e-4)
                                                                             and near(d['hmf2'].temperature, 0.02, 1e-12))


def s09_dense(m):
    return np.asarray(m.todense() if hasattr(m, 'todense') else m)


def s09_lindhard(d):
    c, qs = d['chi0'], d['qs']
    yield 'positive', np.all(c > 0)
    yield 'D(E_F) at the smallest q', near(c[0], 1 / (2 * np.pi), 0.005)
    yield 'the maximum at q = 0.5, 0.86', abs(qs[np.argmax(c)] - 0.5) < 1e-9 and near(c.max(), 0.863, 0.002)
    from pyqula import geometry
    two = -d['g'].get_hamiltonian().get_chi(energies=[0.], q=[0.5, 0., 0.], nk=400, delta=1e-3, T=0.02)[1][0].real
    yield 'twice with the two spins', near(two, 2 * c.max(), 1e-6)
    sl = []
    for mu, q in ((0.0, 0.5), (np.sqrt(2), 0.25)):
        h = geometry.chain().get_hamiltonian(has_spin=False)
        h.add_onsite(mu)
        a, b = (-h.get_chi(energies=[0.], q=[q, 0., 0.], nk=2000, delta=1e-4, T=T)[1][0].real for T in (0.01, 0.005))
        sl.append((b - a) / np.log(2))
    yield 'the slope against ln(1/T) is D(E_F) at half filling and D(E_F)/2 at quarter filling', (
        near(sl[0], 1 / (2 * np.pi), 2e-3) and near(sl[1], 1 / (2 * np.pi * np.sqrt(2)), 2e-3))


def s09_continuum(d):
    s, en, qs = d['spectral'], d['energies'], d['qs']
    i = np.argmin(np.abs(qs - 0.25))
    inside = (en > 2.1) & (en < 2.75)
    outside = (en < 1.6) | (en > 3.3)
    yield 'one row per q', s.shape == (len(qs), len(en))
    yield 'positive inside the continuum at q=0.25', s[i, inside].min() > 0.2
    yield 'small outside it', np.abs(s[i, outside]).max() < 0.1 * s[i, inside].min()
    yield 'the edges 2 and 2.83 at q=0.25', near([2 * abs(np.sin(2 * np.pi * 0.25)), 4 * abs(np.sin(np.pi * 0.25))], [2, 2.83], 0.005)
    h = d['h']
    a = h.get_chi(energies=np.array([0.5, 2.5]), q=[0.25, 0., 0.], nk=200, delta=5e-2)[1]
    b = h.get_chi(energies=np.array([0.5, 2.5]), q=[0.25, 0., 0.], nk=200, delta=5e-2, T=5e-2)[1]
    k = 2 * np.pi * np.arange(200) / 200
    e1, e2 = 2 * np.cos(k), 2 * np.cos(k + np.pi / 2)
    f = lambda e: 0.5 * (1 - np.tanh(e / 0.1))
    page = np.array([np.mean((f(e1) - f(e2)) / (e2 - e1 - w - 0.05j)) for w in (0.5, 2.5)])
    yield 'minus the complex conjugate of (9.5), with T = delta when T is not given', near(a, -np.conj(page), 1e-9) and near(a, b, 1e-12)


def s09_spin_rpa(d):
    hs = d['g'].get_hamiltonian(has_spin=False)
    x0 = -hs.get_chi(energies=[0.0], q=[0.5, 0., 0.], nk=400, delta=1e-2)[1][0].real
    yield 'chi_0 = 0.970', near(x0, 0.970, 1e-3) and near(-np.trace(d['bare'][0]).real, x0, 1e-8)
    yield '1/(1 - U chi_0) = 33.7', near(d['enhancement'], 1 / (1 - x0), 1e-6) and near(d['enhancement'], 33.7, 0.05)


def s09_spinchi(d):
    e, wb, wr = np.asarray(d['energies']), d['weight_bare'], d['weight_rpa']
    yield 'the weight is positive', np.all(wb > -1e-9) and np.all(wr > -1e-9)
    yield 'the maximum moves from 4.0 to 0.14, 18 times higher', (near(e[np.argmax(wb)], 4.0, 0.03) and near(e[np.argmax(wr)], 0.136, 0.01)
                                                                  and 16 < wr.max() / wb.max() < 20)


def s09_density_rpa(d):
    hs = d['g'].get_hamiltonian(has_spin=False)
    x0 = -hs.get_chi(energies=[0.0], q=[0.25, 0., 0.], nk=400, delta=1e-2)[1][0].real
    yield 'chi_0 = 0.198', near(x0, 0.198, 1e-3)
    yield '2 chi_0/(1 + U chi_0) = 0.331', near(d['charge'], 2 * x0 / (1 + x0), 1e-8) and near(d['charge'], 0.331, 1e-3)


def s09_ysr(d):
    lv = np.asarray(d['levels'])
    yield '1200 levels', len(lv) == 1200
    yield 'the bound state at 0.6005 Delta, once at + and once at -', near(d['e_bound'], 0.06005, 2e-5) and np.sum(np.abs(np.abs(lv) - d['e_bound']) < 1e-6) == 2
    yield 'the exchange is the same in the electron and the hole block', near(np.diag(s09_dense(d['h'].intra))[:4].real, [1, -1, 1, -1], 1e-12)
    from pyqula import geometry
    h = geometry.chain().get_supercell(300).get_hamiltonian()
    m = np.zeros((300, 3)); m[0, 2] = 3.0
    h.add_exchange(m); h.add_swave(0.1)
    e3 = np.min(np.abs(np.linalg.eigvalsh(s09_dense(h.get_hk_gen()([0., 0., 0.]))))) / 0.1
    yield '0.3837 Delta at J S = 3, where (9.10) is -0.3846', near(e3, 0.3837, 2e-4) and near((1 - 1.5 ** 2) / (1 + 1.5 ** 2), -0.3846, 1e-4)
    short = []
    for N in (40, 80):
        h = geometry.chain().get_supercell(N).get_hamiltonian()
        m = np.zeros((N, 3)); m[0, 2] = 1.0
        h.add_exchange(m); h.add_swave(0.1)
        short.append(np.min(np.abs(np.linalg.eigvalsh(s09_dense(h.get_hk_gen()([0., 0., 0.]))))) / 0.1)
    yield 'a ring of 40 sites gives 0.36 Delta and one of 80 sites 0.55 Delta', near(short, [0.36, 0.55], 0.005) and near(2 / 0.1, 20, 1e-12)


def s09_chain_impurity(d):
    x, l = np.asarray(d['x']), np.asarray(d['ldos'])
    o = np.argsort(x); x, l = x[o], l[o]
    yield 'x from -50 to 50', len(x) == 101 and near([x.min(), x.max()], [-50, 50])
    s = x >= 2
    qs = np.linspace(0.1, np.pi, 6000)
    q = qs[np.argmax([abs(np.sum((l[s] - l[s].mean()) * np.exp(-1j * qq * x[s]))) for qq in qs])]
    yield 'the period 5.66 sites', abs(2 * np.pi / q - np.pi / np.arccos(0.85)) < 0.15


def s09_plane_impurity(d):
    x, y, l = (np.asarray(d[n]) for n in ('x', 'y', 'ldos'))
    yield 'one entry per site of 31 x 31', len(x) == 31 * 31 and len(l) == 31 * 31
    line = (np.abs(y) < 1e-6) & (x >= 1)
    xl, ll = x[line], l[line]
    o = np.argsort(xl); xl, ll = xl[o], ll[o]
    mx = [xl[i] for i in range(1, len(xl) - 1) if ll[i] > ll[i - 1] and ll[i] > ll[i + 1]]
    yield 'the maxima every 3 sites', abs(np.mean(np.diff(mx)) - 3) < 0.3


def s09_vacancy(d):
    from pyqula import embedding, potentials
    yield 'the bound state is at -0.14', near(d['e_bound'], -0.14, 0.006)
    hv = d['h'].copy()
    hv.add_onsite(potentials.impurity(d['g'].r[1], v=1e3))
    e, dd = embedding.Embedding(d['h'], m=hv).multidos(es=np.linspace(0.10, 0.16, 7), delta=0.004, nk=40)     # the same grid of 0.01
    yield '+0.13 for the vacancy on the other site', near(np.asarray(e)[np.argmax(dd)], 0.13, 0.006)
    yield 'onsite +0.3 on site 0', near(np.diag(s09_dense(d['h'].intra))[0].real, 0.3, 1e-12)


def s09_pwave_vacancy(d):
    from pyqula import geometry, embedding, potentials
    r, en, gap = np.asarray(d['dos']) / np.asarray(d['clean']), d['energies'], d['gap']
    yield 'the gap edge 0.30', near(gap, 0.30, 0.005)
    yield 'peaks at +-0.7 of the gap, about 190 times the clean DOS', (near(np.abs(en[np.argmax(r)]) / gap, 0.7, 0.01)
                                                                   and 120 < r.max() < 260)
    g = d['g']
    hs = g.get_hamiltonian(); hs.add_onsite(-4.0); hs.add_pairing(mode="swave", delta=0.1)
    gs = hs.get_gap() / 2.
    hv = hs.copy(); hv.add_onsite(potentials.impurity(g.r[0], v=100.))
    es = gs * np.linspace(-0.9, 0.9, 10)
    e1, dv = embedding.Embedding(hs, m=hv).multidos(es=es, delta=gs / 60, nk=40)
    e2, dc = embedding.Embedding(hs, m=hs).multidos(es=es, delta=gs / 60, nk=40)
    yield 'with swave the gap is 0.10 and there is no peak inside it', near(gs, 0.10, 1e-4) and np.max(np.asarray(dv) / np.asarray(dc)) < 3
    h1 = geometry.triangular_lattice().get_hamiltonian(); h1.add_onsite(-4.0); h1.add_pairing(mode="chiral_pwave", delta=0.1)
    yield 'h.get_chern() of the spinful chiral p-wave is -2', near(h1.get_chern(), -2.0, 1e-6)


def s09_tails(d):
    from pyqula import geometry, tails as tl
    yield 'the mean decay rate is 0.76, near 2 ln 1.5', near(np.mean(d['rates']), 0.756, 0.01) and near(d['xi'], 2 / 0.756, 0.05)
    yield 'one value per eigenstate', len(d['rates_r']) == 400 and len(d['energies_r']) == 400
    yield 'xi 23 sites at the band center and 7.5 from all the states', near(d['xi_r'], 22.9, 0.1) and near(d['xi_all'], 7.5, 0.05)
    other = []
    for seed in (2, 3):
        hr = d['g'].get_hamiltonian(has_spin=False)
        rng = np.random.default_rng(seed)
        hr.add_onsite(2.0 * rng.random(len(d['g'].r)) - 1.0)
        es, rs = hr.get_tails()
        other.append(2 / np.mean(np.asarray(rs)[np.abs(es) < 0.3]))
    yield 'the seeds 2 and 3 give 20 and 28', near(other, [20, 28], 0.6)
    yield 'the onsite energies are in [-1, 1]', np.abs(np.diag(s09_dense(d['hr'].intra)).real).max() <= 1.0
    w = np.exp(-np.abs(np.arange(400) - 200) / 5.0); w /= np.linalg.norm(w)
    yield 'a state exp(-|n|/5) gives 2/5', near(tl.loclength([w]), 0.4, 1e-9)
    gc = geometry.chain(200)
    gc.dimensionality = 0
    hc = gc.get_hamiltonian(has_spin=False)
    hc.add_onsite(2.0 * (np.arange(200) == 100))
    es, ls = hc.get_tails()
    i = int(np.argmax(es))
    yield 'it is 2 kappa for a bound state with amplitude e^{-kappa n}', near(ls[i], 2 * np.arccosh(es[i] / 2), 1e-6)


def s10_numpy_ring(onsite, t, t2):
    """The ring of the figure ham_learning in numpy, with the matrix elements -t and -t2."""
    n = len(onsite)
    i = np.arange(n)
    H = np.diag(np.asarray(onsite, float))
    H[i, (i + 1) % n] = H[(i + 1) % n, i] = -t
    H[i, (i + 2) % n] = H[(i + 2) % n, i] = -t2
    return H


def s10_ring(d):
    from pyqula import algebra
    from scipy.sparse import issparse
    H = algebra.todense(d['h'].intra).real
    on = np.diag(H).copy()
    ref = s10_numpy_ring(on, 1.0, 0.3)
    yield 'a ring with -1, -0.3 and the onsite energies in [-1, 1]', near(H, ref, 1e-14) and np.abs(on).max() <= 1.0 and np.ptp(on) > 1.5
    yield 'the onsite energies in the order of the sites', near(on, np.random.default_rng(1).uniform(-1., 1., 200), 1e-14)
    yield 'the levels are those of the matrix', near(d['levels'], np.linalg.eigvalsh(ref), 1e-12)
    yield 'the observable sums to 1', near(d['observable'].sum(), 1.0, 1e-12)
    hs = d['g'].get_hamiltonian(has_spin=False, tij=[-1., -0.3]).get_supercell(200)
    hs.add_onsite(on)
    hk0 = hs.get_hk_gen()([0., 0., 0.])
    yield 'get_supercell(200) at k=0 is the same matrix, a sparse one', issparse(hk0) and near(algebra.todense(hk0), H, 1e-14)


def s10_learning(d):
    yield 'the errors of the figure with the seed 3', near(d['rms'], [0.0635, 0.0043], 5e-5)
    yield 'H1 and H2 are the rings of the script', (near(d['H1'], s10_numpy_ring(np.zeros(200), 1.0, 0.0), 1e-14)
                                                   and near(d['H2'], s10_numpy_ring(np.zeros(200), 0.0, 1.0), 1e-14))
    ranks = [np.linalg.matrix_rank(np.hstack([O, np.ones((len(O), 1))])) for O, t2, W in d['data'][1:]]
    yield 'the fits have the rank 27 and 38 of 41', ranks == [27, 38]
    O, t2, W = d['data'][1]
    X = np.hstack([O, np.ones((len(O), 1))])
    sv, Vt = np.linalg.svd(X)[1:]
    null = Vt[sv < 1e-10 * sv[0]]
    Xt = np.hstack([d['Otest'], np.ones((len(d['Otest']), 1))])
    vec = null.T @ np.linalg.svd(Xt @ null.T)[2][0]
    theta = np.linalg.lstsq(X, t2, rcond=None)[0]
    other = np.sqrt(np.mean((Xt @ (theta + vec) - d['t2test']) ** 2))
    yield 'another least-squares solution of the clean fit gives another error', near(X @ (theta + vec), X @ theta, 1e-9) and abs(other - d['rms'][0]) > 0.02


def s10_hartree(d):
    from pyqula import geometry, algebra
    n, occ = d['density'], d['occupied']
    x = np.arange(60)
    vext = -2.0 * np.exp(-((x - 29.5) / 7.0) ** 2)
    T = -np.eye(60, k=1) - np.eye(60, k=-1)
    m = np.full(60, 40 / 60)
    for it in range(300):
        w = np.linalg.eigh(T + np.diag(vext + 2.0 * m))[1]
        new = 2 * (np.abs(w[:, :20]) ** 2).sum(axis=1)
        if np.abs(new - m).max() < 1e-14:
            break
        m = 0.7 * m + 0.3 * new
    w0 = np.linalg.eigh(T + np.diag(vext))[1]
    rx = np.array(d['h'].geometry.r)[:, 0]
    yield 'the sites are in the order of their position', near(rx - rx[0], x, 1e-12)
    yield 'the density of the toy with U=2 to 2e-11', near(n, m, 1e-10) and near(n.sum(), 40.0, 1e-9)
    yield '0.9895 at the center, 1.2143 with no interaction', near(n[30], 0.9895, 5e-5) and near(2 * (np.abs(w0[30, :20]) ** 2).sum(), 1.2143, 5e-5)
    yield 'the two spins are equal', near(occ[0::2], occ[1::2], 1e-12)

    def chain():
        h = geometry.chain().get_hamiltonian(tij=[-1.]).set_finite_system(n=60)
        h.add_onsite(vext)
        return h

    def spins(mf):
        wv = np.linalg.eigh(algebra.todense(mf.intra))[1][:, :40]
        rho = wv @ wv.conj().T
        nn = np.real(np.diag(rho))
        mom = np.array([[2 * np.real(rho[2 * i, 2 * i + 1]), 2 * np.imag(rho[2 * i + 1, 2 * i]), nn[2 * i] - nn[2 * i + 1]] for i in range(60)])
        return nn[0::2] + nn[1::2], np.linalg.norm(mom, axis=1).max()
    mfc, Ec = chain().get_mean_field_hamiltonian(U=4., filling=40 / 120, mix=0.3, maxerror=1e-8, constrains=['no_magnetism'],
                                                 return_total_energy=True)
    mfp = chain().get_mean_field_hamiltonian(U=4., filling=40 / 120, mix=0.3, maxerror=1e-8, mf='potential')
    dp, mp = spins(mfp)
    yield 'mf="potential" gives the same density with a moment of 5e-7', near(dp, m, 1e-10) and 1e-8 < mp < 1e-5
    nu = nd = m / 2                     # a collinear loop in numpy from equal spins with a kick of 1e-6
    kick = 1e-6 * np.random.default_rng(1).normal(size=60)
    nu, nd = nu + kick, nd - kick
    for it in range(200):
        eu, wu = np.linalg.eigh(T + np.diag(vext + 4.0 * nd))
        ed, wd = np.linalg.eigh(T + np.diag(vext + 4.0 * nu))
        k = np.argsort(np.concatenate([eu, ed]))[:40]
        nu = 0.7 * nu + 0.3 * (np.abs(wu[:, k[k < 60]]) ** 2).sum(1)
        nd = 0.7 * nd + 0.3 * (np.abs(wd[:, k[k >= 60] - 60]) ** 2).sum(1)
    yield 'the state with equal spins is unstable, a kick of 1e-6 grows to the moment 0.77', near(np.abs(nu - nd).max(), 0.769, 0.002)
    yield 'the equal spins have the total energy -58.01', near(Ec, -58.0094, 5e-5)
    # the random start with the seed 0, -61.79 and the moment 0.77, is asserted by webnotes/checks/session10/conventions.py
    import contextlib, io
    from pyqula.scftk.convergence import MeanFieldConvergenceError
    try:
        with contextlib.redirect_stdout(io.StringIO()):     # pyqula prints that the loop stopped
            chain().get_mean_field_hamiltonian(U=4., filling=40 / 120, mix=0.3, maxite=5)
        raised = False
    except MeanFieldConvergenceError:
        raised = True
    yield 'a loop that does not converge raises in the development tree', raised


def s10_ising(d):
    from pyqula.latticeising import LatticeIsing
    model, g = d['model'], d['g']
    yield 'all spins up is -512', near(d['energy_all_up'], -512.0, 1e-9)
    s = model.s.copy()
    model.s = np.ones(256)
    e0 = model.get_energy()
    model.s[0] = -1
    yield 'one flip costs 8', near(model.get_energy() - e0, 8.0, 1e-9)
    m2 = LatticeIsing(g, m=1.)
    m2.add_interaction(Jij=[1.])
    yield 'Jij=[1.] doubles the energy', near(m2.get_energy(), -1024.0, 1e-9)
    model.s = s
    yield 'one entry per attempted flip', len(d['es']) == 256 * 1000 and len(d['ms']) == 256 * 1000
    exact = (1 - np.sinh(2 / 1.5) ** -4) ** 0.125
    yield 'the mean |m| is 0.987 at T=1.5, the exact 0.9865', near(d['absm'].mean(), 0.987, 0.0006) and near(exact, 0.9865, 5e-5)
    runs = []
    for i in range(2):
        again = LatticeIsing(g, m=1.)
        again.add_interaction(Jij=[0.5])
        np.random.seed(1)
        runs.append(again.optimize_energy(temp=1.5, ntries=2560)[1])
    yield 'np.random.seed fixes the run', np.array_equal(runs[0], runs[1]) and np.array_equal(runs[0], d['ms'][:2560])
    # |m| about 0.13 at T=3.5 and 0.124 for a long run are asserted by webnotes/checks/session10/conventions.py
    yield 'with no m half of the spins are up', LatticeIsing(g).s.sum() == 0 and len(LatticeIsing(g).s) == 256
    try:
        LatticeIsing(g, m=1.).add_tensor(lambda r1, r2, r3, r4: 1.0)
        raised = False
    except TypeError as err:
        raised = 'r3' in str(err)
    yield 'add_tensor with a function of four positions raises a TypeError', raised
    r = np.array(g.r).reshape(16, 16, 3)
    yield 'the first index of snapshot runs along x', near(r[:, :, 0], np.arange(16)[:, None] - 7.5) and near(r[:, :, 1], np.arange(16)[None, :] - 7.5)
    yield 'T_c is 2.269 for Jij=[0.5] and 4.54 for Jij=[1.]', near(2 / np.log(1 + np.sqrt(2)), 2.269, 5e-4) and near(4 / np.log(1 + np.sqrt(2)), 4.54, 5e-3)


EXPECT = {
    'Bands on a k-path': bands_path,
    'Bands of a ribbon with the position of the states': ribbon,
    'A ribbon in a magnetic field': field,
    'A finite island and its local density of states': island,
    'The gap on a k-mesh': mesh_gap,
    'The Berry curvature map': berry_map,
    'The Chern number': chern,
    'The Hall conductivity against the chemical potential': hall,
    'The SSH chain and its open chain': ssh,
    'The Zak phase': zak,
    'The quantum spin Hall ribbon': qsh,
    'The Z2 invariant': z2,
    'The conductance of a ribbon': conductance,
    'Bands with the sign of the notes': notes_sign,
    'The chain with a second-neighbor hopping': second_neighbor,
    'Band folding in a supercell': folding,
    'The density of states': density,
    'A band on a map of the Brillouin zone': band_map,
    'The Fermi surface': fermi,
    'The flat bands of the Lieb and kagome lattices': flat,
    'The Dirac velocity of the honeycomb lattice': dirac,
    'The chain with two sites per cell of (2.13)': two_site,
    'The levels of an open chain': s01_open_chain,
    'The Hubbard dimer in mean field': s01_dimer,
    'The antiferromagnet of the half-filled Hubbard chain': s01_afm_chain,
    'The antiferromagnet of the honeycomb lattice': s01_honeycomb,
    'The charge density wave of the spinless chain': s01_cdw,
    'A seed field that stays in the Hamiltonian': s01_seed,
    'The s-wave superconductor of the attractive Hubbard chain': s01_swave,
    'The Chern number of a Landau level': landau_chern,
    'The density of states of the bulk of a ribbon': dos_bulk,
    'The Dirac Landau levels of the honeycomb lattice': dirac_levels,
    'The local density of states of a ribbon in a field': ldos_ribbon,
    'An island in a magnetic field': island_field,
    'The Chern number of a Landau gap of the honeycomb lattice': chern_gap,
    'From the Haldane model to the quantum Hall state': haldane_path,
    'A domain wall in the onsite energy': domain_wall,
    'Bands of a superconductor with the electron weight': sc_bands,
    'Pairing of a given symmetry in momentum space': sc_pairing,
    'Spin-triplet superconductivity from an attractive interaction in a magnet': sc_triplet,
    'The density of states of a superconductor': sc_dos,
    'The Chern number of a superconductor': sc_chern,
    'The edge states of a topological superconductor': sc_edge,
    'The open Kitaev chain and its end modes': sc_kitaev_open,
    'The local density of states at the end of a Kitaev chain': sc_ldos_end,
    'The topological transition of a Rashba superconductor': sc_rashba,
    'The Zak phase of the Kitaev chain': sc_zak,
    'The ferromagnet against the antiferromagnet at large U': fm_vs_afm,
    'A mean-field loop that starts from a chosen field': seeded,
    'The ferromagnet of the chain away from half filling': chain_fm,
    'A noncollinear mean field on the triangular lattice': triangular,
    'A flat band in mean field': lieb,
    'Magnon energies of the Hubbard antiferromagnet': magnons,
    'Magnon bands of a honeycomb ferromagnet': honeycomb_magnons,
    'The Chern number of a magnon band': magnon_chern,
    'The entanglement entropy of a block of free fermions': s07_block,
    'Half of an open chain of free fermions': s07_half,
    'The entanglement entropy of the dimerized chain of free fermions': s07_dimerized,
    'The XX chain as free fermions': s07_xx,
    'A pyqula chain solved with dmrgpy': s07_dmrgpy,
    'The spinon Fermi surface at half filling': spinon_fermi_surface,
    'The bands of a Kondo lattice': kondo_bands,
    'A Kondo lattice with exchange between the moments': kondo_exchange,
    'The pi-flux square lattice': pi_flux,
    'The spinon mean field of a Heisenberg chain': spinon_chain,
    'The self-consistent Kondo lattice': kondo_scf,
    'The static Lindhard function of a chain': s09_lindhard,
    'The dynamical response and the particle-hole continuum': s09_continuum,
    'The RPA enhancement of the spin response': s09_spin_rpa,
    'The spin response of the mean-field antiferromagnet': s09_spinchi,
    'The density response with RPA': s09_density_rpa,
    'A magnetic impurity in a superconducting ring': s09_ysr,
    'An impurity in an infinite chain': s09_chain_impurity,
    'An impurity in an infinite square lattice': s09_plane_impurity,
    'A vacancy in a Chern insulator': s09_vacancy,
    'A vacancy in a chiral p-wave superconductor': s09_pwave_vacancy,
    'The tails of the eigenstates of a finite chain': s09_tails,
    'A disordered ring': s10_ring,
    'Learning the second-neighbor hopping from the density of states': s10_learning,
    'A Hartree loop on an open chain': s10_hartree,
    'Monte Carlo of the Ising model': s10_ising,
}


def main(words):
    """Runs the recipes whose name holds every word of the command line, all of them with no word."""
    found = recipes()
    names = [name for name, code, line in found]
    problems = ['EXPECT names "%s", which is not a recipe' % n for n in EXPECT if n not in names]
    problems += ['the recipe "%s" appears twice' % n for n in set(names) if names.count(n) > 1]
    problems += ['a python block at line %d has no heading above it' % line for name, code, line in found if not name]
    t0, done = time.time(), 0
    for name, code, line in found:
        if not name or not all(w.lower() in name.lower() for w in words):
            continue
        t1 = time.time()
        try:
            broken = rules(code)
            failed = run(code, name)
        except Exception:
            traceback.print_exc()
            print('FAIL  %s (RECIPES.md line %d): the recipe raises' % (name, line))
            return 1
        if broken or failed:
            print('FAIL  %s (RECIPES.md line %d): %s' % (name, line, ', '.join(broken + failed)))
            return 1
        print('ok    %s: it runs%s, %.1f s' % (name, ' and its numbers hold' if name in EXPECT else '', time.time() - t1), flush=True)
        done += 1
    if not done:
        problems.append('no recipe has the words ' + ' '.join(words) if found else 'RECIPES.md has no python block')
    for p in problems:
        print('FAIL  ' + p)
    if problems:
        return 1
    print('%d of %d recipes hold, %.1f s' % (done, len(found), time.time() - t0))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
