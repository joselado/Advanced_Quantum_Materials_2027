# pyqula recipes of the course

These are the calls of pyqula for the tasks of Session 3 of the web notes, one recipe per task, and the other
sessions add theirs here. Each recipe is a script of a few lines that runs alone, and the sentences under it say
what comes back, in which units and with which sign. The energies are in units of the first-neighbor hopping, which
pyqula takes as $+1$, and the lengths are in units of the geometry, which for the honeycomb lattice is the bond
length. The recipes come from the scripts of `webnotes/scripts/session03/` and from the notebook `session3.ipynb`,
and what the sentences state was checked with a number. pyqula writes files such as `BANDS.OUT` in the folder where
a script runs.

All the recipes run with one command, which stops at the first recipe that fails and names it.

```
python3 webnotes/checks/test_recipes.py
```

## Bands on a k-path

```python
from pyqula import geometry

g = geometry.honeycomb_lattice()  # honeycomb lattice
h = g.get_hamiltonian(has_spin=False)  # spinless Hamiltonian with first-neighbor hopping 1
(k, e) = h.get_bands(kpath=["G", "K", "M", "G"], nk=200)  # bands along the path
nbands = h.intra.shape[0]  # number of bands, 2 here
energies = e.reshape(-1, nbands)  # energy of band n at step i of the path
```

The two arrays are flat with one entry per state, `k` is the number of the step along the path and `e` is the
energy in units of the hopping. The path has 273 steps here, more than `nk`, and pyqula writes the step of each
named point in the file `BANDLINES.OUT`.

## Bands of a ribbon with the position of the states

```python
import numpy as np
from pyqula import geometry

g = geometry.honeycomb_armchair_ribbon(20)  # ribbon with armchair edges, of width 20
h = g.get_hamiltonian(has_spin=False)  # Hamiltonian of the ribbon
h.add_haldane(0.1)  # Haldane coupling, the gap of the bulk is 0.9
nk = 201  # number of momenta
kpath = [[k, 0., 0.] for k in np.linspace(-0.5, 0.5, nk)]  # momentum along the ribbon, in units of 2 pi
(ik, e, y) = h.get_bands(operator="yposition", kpath=kpath)  # bands with the position of each state
energies = np.array(e).reshape(nk, -1)  # energy of band n at momentum k
positions = np.array(y).reshape(nk, -1)  # where each state sits across the ribbon
```

The momentum of `kpath` is in units of $2\pi$ over the period of the ribbon, so $-0.5$ and $0.5$ are the two ends
of the zone. `positions` is the average of $y$ in each state in the units of `g.y`, so a state at an edge is close
to `g.y.min()` or to `g.y.max()`, as the two bands that cross the gap are here, one at each edge.

## A ribbon in a magnetic field

```python
import numpy as np
from pyqula import geometry

g = geometry.square_ribbon(40)  # ribbon of the square lattice, 40 sites wide
h = g.get_hamiltonian(has_spin=False, tij=[-1.])  # first-neighbor hopping -1
h.add_orbital_magnetic_field(0.02)  # magnetic flux per plaquette, in flux quanta
nk = 201  # number of momenta
kpath = [[k, 0., 0.] for k in np.linspace(-0.5, 0.5, nk)]  # momentum along the ribbon, in units of 2 pi
(ik, e, y) = h.get_bands(operator="yposition", kpath=kpath)  # bands with the position of each state
energies = np.array(e).reshape(nk, -1)  # energy of band n at momentum k
positions = np.array(y).reshape(nk, -1)  # where each state sits across the ribbon
```

The argument of the field is the flux through one plaquette of the square lattice in units of the flux quantum
$h/e$, so the levels are those of the Harper chain $-2\cos(2\pi(k+0.02\,y))$ and the lowest Landau levels are 0.24
apart. With this sign the states of the lowest level with a positive slope sit at the edge of positive $y$, and
the opposite field exchanges the two edges.

## A finite island and its local density of states

```python
import numpy as np
from pyqula import islands

g = islands.get_geometry(name="honeycomb", n=12, nedges=6, rot=np.pi/6)  # flake with six armchair edges
h = g.get_hamiltonian(has_spin=False)  # Hamiltonian of the flake
h.add_haldane(0.1)  # Haldane coupling, the gap of the bulk is 0.9
(x, y, ldos) = h.get_ldos(e=0., delta=0.03)  # local density of states at the energy e
```

`x` and `y` are the positions of the 834 sites, and `ldos` is the density of states at each site in states per
unit of energy, where every level is a Lorentzian of half width `delta`. Here the energy is inside the gap, and
the sites within two bond lengths of the edge, 19 percent of them, hold 56 percent of the weight.

## The gap on a k-mesh

```python
import numpy as np
from pyqula import geometry

g = geometry.honeycomb_lattice()  # honeycomb lattice
h = g.get_hamiltonian(has_spin=False)  # spinless Hamiltonian, one filled band of two
h.add_haldane(0.1)  # Haldane coupling
hk = h.get_hk_gen()  # Bloch Hamiltonian, the momentum is in units of the reciprocal vectors
ks = np.arange(60)/60  # mesh of the zone, a multiple of 3 holds K and K'
e = np.array([np.linalg.eigvalsh(hk([kx, ky, 0.])) for kx in ks for ky in ks])  # energies on the mesh
gap = e[:, 1].min() - e[:, 0].max()  # lowest empty energy minus highest filled energy
```

The gap is 0.9 in units of the hopping, nine times the argument of `add_haldane`, and a mesh bounds it from above,
so the mesh must hold the momenta where the gap is smallest. A page quotes a gap from a mesh like this one, since
`h.get_gap()` returned zero for a spin-orbit coupling 0.1 with a Rashba coupling 0.15, where the mesh gives 0.44.

## The Berry curvature map

```python
import numpy as np
from pyqula import geometry

g = geometry.honeycomb_lattice()  # honeycomb lattice
h = g.get_hamiltonian(has_spin=False)  # spinless Hamiltonian with first-neighbor hopping 1
h.add_haldane(0.1)  # Haldane coupling, a gap that breaks time reversal
nk = 120  # points per side of the map
(kx, ky, b) = h.get_berry_curvature(nk=nk)  # Berry curvature of the filled band
omega = np.array(b).reshape(nk, nk)  # the map, the first index runs along kx
average = np.mean(b)/(2*np.pi)  # the Chern number, it gives 1
```

`kx` and `ky` are in units of $2\pi$ over the lattice constant, which is $\sqrt3$ here, on a rectangle around
$\Gamma$ that is a period of the map and holds two zones. `b` is $\Omega=-2\,\mathrm{Im}\langle\partial_{k_x}u|\partial_{k_y}u\rangle$
of the filled band times the area of the zone, so its average over the map divided by $2\pi$ is the Chern number
with its sign, and with the coupling $+0.1$ it is positive at $K$ and at $K'$.

## The Chern number

```python
from pyqula import geometry

g = geometry.honeycomb_lattice()  # honeycomb lattice
h = g.get_hamiltonian(has_spin=False)  # spinless Hamiltonian with first-neighbor hopping 1
h.add_haldane(0.1)  # Haldane coupling, a gap that breaks time reversal
chern = h.get_chern(nk=60)  # Chern number of the filled band, it gives 1

h = g.get_hamiltonian(has_spin=False)  # the same lattice again
h.add_sublattice_imbalance(0.5)  # staggered potential, a gap that keeps time reversal
chern_staggered = h.get_chern(nk=60)  # it gives 0
```

This is $C=\frac{1}{2\pi}\int\Omega\,d^2k$ of the states below zero energy, with the $\Omega$ of the recipe above,
so it is $+1$ for `add_haldane(0.1)` and $-1$ for `add_haldane(-0.1)`. Without `has_spin=False` the Hamiltonian
has the two spins and the same call gives 2.

## The Hall conductivity against the chemical potential

```python
import numpy as np
from pyqula import geometry

g = geometry.honeycomb_lattice()  # honeycomb lattice
h = g.get_hamiltonian(has_spin=False)  # spinless Hamiltonian with first-neighbor hopping 1
h.add_haldane(0.1)  # Haldane coupling, it opens a gap of 0.9
mu = np.linspace(-3.3, 3.3, 67)  # chemical potentials
sigma_xy = h.get_anomalous_hall_conductivity(fermi=mu, T=0.02, nk=60)  # Hall conductivity, one value per mu
```

The result is $\frac{1}{2\pi}\sum_n\int f(\varepsilon_n-\mu)\,\Omega_n\,d^2k$ in units of $e^2/h$, with `T` the
thermal energy in units of the hopping. Inside the gap it is the Chern number of `h.get_chern()` with the same
sign, $+1$ here, and it goes to zero when the two bands are empty or full.

## The SSH chain and its open chain

```python
import numpy as np
from pyqula import geometry

g = geometry.bichain()  # chain with two sites per unit cell
h = g.get_hamiltonian(has_spin=False)  # all the hoppings equal to 1
h.intra = 0.5*h.intra  # weak hopping inside the cell, the hopping between cells stays 1
(k, e) = h.get_bands(nk=200)  # bands of the infinite chain
gap = 2*np.min(np.abs(e))  # gap of the infinite chain, it gives 1
hf = h.set_finite_system(n=20)  # open chain of 20 cells, it ends with a weak bond
levels = np.sort(hf.get_bands()[1])  # the 40 levels of the open chain
```

The open chain keeps whole cells, so with the weak hopping in `h.intra` it ends with a weak bond, and the two
levels in the middle of `levels` are the end states, at $\pm 7\cdot10^{-7}$. With `h.inter = 0.5*h.inter` instead
the chain ends with a strong bond, and the levels closest to zero are at $\pm0.51$.

## The Zak phase

```python
import numpy as np
from pyqula import geometry, topology

g = geometry.bichain()  # chain with two sites per unit cell
h = g.get_hamiltonian(has_spin=False)  # all the hoppings equal to 1
h.intra = 0.5*h.intra  # weak hopping inside the cell
zak = topology.berry_phase(h, nk=100)  # Berry phase of the filled band across the zone
zak = np.abs(zak)  # the phase is defined modulo 2 pi, so pi and -pi are the same
```

The phase is $\int i\langle u|\partial_k u\rangle\,dk$ of the states below zero energy, in radians, and it is
$\pi$ when the weak hopping is the one inside the cell and 0 when it is the one between cells. pyqula returns
$+\pi$ or $-\pi$ for the same chain depending on `nk`, which is rounding, so a page says $\pi$ modulo $2\pi$.

## The quantum spin Hall ribbon

```python
import numpy as np
from pyqula import geometry

nk = 201  # number of momenta
kpath = [[k, 0., 0.] for k in np.linspace(0., 1., nk)]  # momentum along the ribbon, in units of 2 pi
g = geometry.honeycomb_zigzag_ribbon(10)  # ribbon with zigzag edges, of width 10
h = g.get_hamiltonian()  # Hamiltonian with the two spins
h.add_soc(-0.1)  # intrinsic spin-orbit coupling, the gap of the bulk is 0.9
h.add_onsite(0.002*g.y)  # small bias across the ribbon, to tell the two edges apart
(ik, energy, spin, position) = h.get_bands(kpath=kpath, operator=["sz", "yposition"])  # bands, spin and position
momentum = 2*np.pi*ik/(nk-1)  # momentum of each state, times the period of the ribbon
```

The four arrays are flat with one entry per state, `spin` is the average of $\sigma_z$ between $-1$ and $1$, and
`position` is the average of $y$ in the units of `g.y`. Inside the gap each edge has one state of each spin with
opposite slopes, and with this sign of the coupling the spin up state at the edge of positive $y$ has a negative
slope.

## The Z2 invariant

```python
from pyqula import geometry, topology

g = geometry.honeycomb_lattice()  # honeycomb lattice
h = g.get_hamiltonian()  # Hamiltonian with the two spins
h.add_soc(0.1)  # intrinsic spin-orbit coupling, the gap is 0.9
z2 = topology.z2_invariant(h)  # it gives -1

h = g.get_hamiltonian()  # the same lattice again
h.add_sublattice_imbalance(0.45)  # staggered potential, with the same gap
z2_staggered = topology.z2_invariant(h)  # it gives 1
```

pyqula returns the sign $(-1)^\nu$ of the states below zero energy and not $\nu$, so $-1$ is the quantum spin
Hall insulator and $+1$ is the ordinary insulator.

## The conductance of a ribbon

```python
import numpy as np
from pyqula import geometry, heterostructures

energies = np.linspace(-0.8, 0.8, 17)  # chemical potentials
g = geometry.honeycomb_zigzag_ribbon(10)  # ribbon with zigzag edges, of width 10
h = g.get_hamiltonian()  # Hamiltonian with the two spins
h.add_soc(0.1)  # intrinsic spin-orbit coupling, the gap of the bulk is 0.9
ht = heterostructures.Heterostructure(h)  # two leads and a central part, all the same ribbon
conductance = np.array([ht.landauer(energy=e) for e in energies])  # transmission at each energy
```

The result is the transmission from one lead to the other, which is the conductance in units of $e^2/h$, and
inside the gap it is 2, one channel for each edge. With `h.add_sublattice_imbalance(0.45)` in place of the
spin-orbit coupling the gap is the same and the conductance inside it is zero.
