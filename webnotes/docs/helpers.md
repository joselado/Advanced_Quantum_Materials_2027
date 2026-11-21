# The physics helpers of the web notes

A page of the notes states signs, units and numbers, and every one of them is checked with a calculation before
it is written. This part of the toolkit holds what such a check needs, so that an author or a checker does not
write it again. It has a small module for the Berry curvature and the invariants, a file of pyqula recipes, and
three scripts that keep both true. The signs are those of `webnotes/conventions/session03.md`.

## The module

`webnotes/figures/physcheck.py` computes the Berry curvature, the Chern number, the Zak phase and the gap of a
Bloch Hamiltonian. It needs numpy only, so a figure script and a check script can both import it. A Bloch
Hamiltonian is a function `hk(k)` that returns a matrix, with the Cartesian momentum `k`, and `B` holds the
reciprocal vectors as its rows. In one dimension `k` is a number and `B` is the length of the zone.

The convention is $A=i\langle u|\partial_k u\rangle$ and $\Omega_n=-2\,\mathrm{Im}\langle\partial_{k_x}u_n|\partial_{k_y}u_n\rangle$,
with $C=\frac{1}{2\pi}\int\Omega\,d^2k$ summed over the filled bands. With this sign `h.add_haldane(0.1)` of pyqula
has $C=+1$, as `h.get_chern()` gives. The usual plaquette phase of the link variables is minus this $\Omega$ times
the area, and the module puts that sign in, so we never do it by hand.

- `berry_curvature(hk, k, bands=0)` is $\Omega$ of a band at one momentum, from the Kubo form that needs no phase
  of the eigenvectors. We use it for a value at a point and as the reference for the sign.
- `chern_links(hk, B, bands=0, nk=24)` is the Chern number from the link variables, an integer on any mesh that
  resolves the gap. A list of bands enters through the determinant of the overlaps, so the filled bands may cross.
- `chern_kubo(hk, B, bands=0, nk=48)` is the Chern number from the integral of the Kubo form. It is an integer
  only in the limit of a dense mesh, so we use it to check the sign of the other one.
- `zak_phase(hk, B, bands=0, nk=200)` is the Zak phase of a chain from a Wilson loop, modulo $2\pi$, with $-\pi$
  written as $\pi$.
- `gap(hk, B, nfilled, nk=60, points=())` is the gap between the filled and the empty bands on a k-mesh. The
  momenta given in `points` are added to the mesh, which we need when the gap closes away from the mesh.
- `from_pyqula(h)` returns `(hk, B)` for a pyqula Hamiltonian in one or two dimensions, so the functions above
  run on what pyqula builds.
- `reciprocal(A)` and `kmesh(B, nk, points=())` are the reciprocal vectors of a lattice and the mesh of its zone.

The argument `bands` is one band, counted from 0 at the lowest energy, or a list such as `range(2)`. The link
variables and the Wilson loop need `hk(k + b) = hk(k)`, which is the gauge of pyqula and of `_honeycomb.bloch`, and
they stop with an error for another gauge. The Kubo form has no such condition.

A check of a page with a pyqula model is then a few lines.

```python
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # webnotes/figures
import physcheck
from pyqula import geometry

g = geometry.honeycomb_lattice()
h = g.get_hamiltonian(has_spin=False)
h.add_haldane(0.1)
hk, B = physcheck.from_pyqula(h)                  # hk(k) with the Cartesian k, and the reciprocal vectors
K = (B[0] + B[1]) / 3                             # a corner of the zone
print(physcheck.berry_curvature(hk, K, bands=0))  # Omega of the filled band at K, 5.56
print(physcheck.chern_links(hk, B, bands=0))      # the Chern number, 1
print(physcheck.gap(hk, B, nfilled=1, nk=60))     # the gap, 0.9
```

The `sys.path` line is the one of a figure script in `webnotes/figures/sessionNN/`. A script in `webnotes/checks/`
finds `webnotes/figures` from its own path in the same way. A mesh with `nk` a multiple of 3 holds $K$ and $K'$ of
a hexagonal lattice, and an even `nk` holds $M$.

## The recipes

`webnotes/scripts/RECIPES.md` holds the pyqula calls for the tasks of Session 3, one recipe per task, and another
session adds its own there. A recipe is a script of a few lines in the style of the scripts that a student
downloads, and it runs alone. The sentences
under it say what comes back, in which units and with which sign. An author takes the calls from there and does
not read the source of pyqula again. A new recipe is a heading of level two, a fenced python block and its
sentences, and the heading is the name that the test prints.

## The checks

Three scripts keep the module, the recipes and the sheet true. Each one prints one line per check and exits with
an error at the first check that does not hold. They find the repository from their own path and they run pyqula
in a temporary folder, so they can be started from anywhere. The times below are for a free machine, and they
grow several times when it is busy.

```
python3 webnotes/checks/test_physcheck.py
```

This is the test of the module, 28 checks in about 11 s. The Kubo form is compared with the literal definition
in a smooth gauge and with the closed form of a two-band model, which fixes the sign. The two routes to the Chern
number are then compared on a two-band model, on a random four-band model with two filled bands, on
`_honeycomb.bloch` and on pyqula, and the Zak phase on the SSH chain.

```
python3 webnotes/checks/test_recipes.py
```

This runs the 13 recipes, in about 20 s. It fails with the name of the recipe when a block raises, when a block
breaks a rule of the downloadable scripts, or when a number that the sentences state does not hold. The numbers
are in the table `EXPECT` of the script, one function per recipe, so a new sentence with a number gets a line
there. With a word after the command only the recipes with that word in the name run.

```
python3 webnotes/checks/test_recipes.py Zak
```

The third script asserts the statements of the conventions sheet of Session 3, 24 checks in about 17 s.

```
python3 webnotes/checks/session03/conventions.py
```

Its docstring lists the statements of the sheet that it does not assert. When a check fails after a change of
pyqula we correct the sheet and the pages that quote it, and not the check.

## Another session

The sheet of another session gets a script `webnotes/checks/sessionNN/conventions.py` of the same shape, with one
`check(name, ok, detail)` per statement, in the order of the sheet. The folder `webnotes/checks/` holds only
scripts that run as checks, with no helper module, so what two of them share goes to `physcheck.py`.
