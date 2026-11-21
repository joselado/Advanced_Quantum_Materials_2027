"""Runs every recipe of webnotes/scripts/RECIPES.md and checks what the sentences under it state.

A recipe is a fenced python block under a heading of level two, and the heading is its name. Each block runs alone
in a temporary folder, since pyqula writes files. The script stops with the name of the recipe when a block raises,
when a block breaks a rule of the downloadable scripts (it imports pyqula, it imports no plotting package, it defines
no function and no class, it has at most 40 lines), or when a number of EXPECT does not hold. A recipe with no entry
in EXPECT is only run. It prints one line per recipe and exits 0 when all hold.

Run it from anywhere:  python3 webnotes/checks/test_recipes.py
One recipe:            python3 webnotes/checks/test_recipes.py Zak"""
import ast, os, re, sys, tempfile, time, traceback
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
    return bool(np.all(np.abs(np.asarray(x, float) - y) < tol))


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
