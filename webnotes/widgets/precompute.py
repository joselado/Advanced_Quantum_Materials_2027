"""Precomputes the JSON of every widget: python3 webnotes/widgets/precompute.py [id ...]

Each webnotes/widgets/defs/ID.py has META (the parameters) and compute(p). This script runs compute on the grid of the
sliders with the Python of this machine and writes data/ID.json, which notes.js plots at once and when Pyodide is not
loaded. The file records the sha1 of ID.py, and build.py stops when a def is newer than its JSON.
"""
import hashlib
import importlib.util
import itertools
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DEFS = os.path.join(HERE, 'defs')
DATA = os.path.join(HERE, 'data')


def sha(path):
    return hashlib.sha1(open(path, 'rb').read()).hexdigest()[:12]


def clean(o):
    """Same rounding and conversion as the Python glue of notes.js: lists, 5 significant digits."""
    import numpy as np
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items() if v is not None}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, np.ndarray):
        return clean(o.tolist())
    if isinstance(o, (float, np.floating)):
        x = float(f'{float(o):.5g}')
        return 0.0 if x == 0 else x
    if isinstance(o, np.integer):
        return int(o)
    return o


def load(wid):
    path = os.path.join(DEFS, wid + '.py')
    spec = importlib.util.spec_from_file_location('widget_' + wid, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, path


def values(par):
    n = int(round((par['max'] - par['min']) / par['step'])) + 1
    return [par['min'] + i * par['step'] for i in range(n)]


def run(wid):
    mod, path = load(wid)
    meta = dict(mod.META)
    pars = meta['params']
    grid = {}
    t0 = time.time()
    for idx in itertools.product(*[range(len(values(p))) for p in pars]):
        p = {par['name']: values(par)[i] for par, i in zip(pars, idx)}
        grid[','.join(map(str, idx))] = clean(mod.compute(p))
    meta['sha'] = sha(path)
    out = os.path.join(DATA, wid + '.json')
    os.makedirs(DATA, exist_ok=True)
    text = json.dumps(dict(meta=meta, grid=grid), separators=(',', ':'))
    with open(out, 'w') as f:
        f.write(text)
    print(f'{wid}: {len(grid)} points, {len(text) / 1024:.0f} kB, {time.time() - t0:.1f} s')


def main():
    ids = sys.argv[1:] or sorted(f[:-3] for f in os.listdir(DEFS) if f.endswith('.py'))
    for wid in ids:
        run(wid)


if __name__ == '__main__':
    main()
