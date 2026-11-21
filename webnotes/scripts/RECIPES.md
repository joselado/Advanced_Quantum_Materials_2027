# pyqula recipes of the course

These are the calls of pyqula for the tasks of Session 3 of the web notes, one recipe per task, and the other
sessions add theirs here. Each recipe is a script of a few lines that runs alone, and the sentences under it say
what comes back, in which units and with which sign. The energies are in units of the first-neighbor hopping, which
pyqula takes as $+1$, and the lengths are in units of the geometry, which for the honeycomb lattice is the bond
length. The recipes come from the scripts of `webnotes/scripts/session03/` and from the notebook `session3.ipynb`,
and what the sentences state was checked with a number. pyqula writes files such as `BANDS.OUT` in the folder where
a script runs.

The recipes were checked with the development tree of pyqula, while the students install the release 0.0.96 of PyPI.
Every recipe was also run with a copy of that release, and a recipe whose call fails there or gives other numbers at
the digits of its sentences says so in one sentence. Two differences of that release concern many scripts. Its label
"M" is $(1/2,0)$ on every lattice, so on the square and Lieb lattices `kpath=["G","X","M","G"]` never reaches
$(\pi,\pi)$, and its `get_dos` raises a `TypeError` with `integration="triangle"`. A script to download gives such a
path as a list of reduced momenta and avoids that keyword. The recipes of Session 2, from "Bands with the sign of the
notes" on, use `tij=[-1.]` for the sign of the notes, as `webnotes/conventions/session02.md` says.

The other sessions follow in their order, each with the conventions of its sheet in `webnotes/conventions/`. The
recipes of Session 1, from "The levels of an open chain" on, take the Hubbard term
$U\sum_i n_{i\uparrow}n_{i\downarrow}$ of (1.7) and the term $V\sum_{\langle ij\rangle}n_in_j$ of (1.6) with each bond
once, and they keep the hopping $+1$ of pyqula, whose sign changes no energy and no density on the chain and on the
honeycomb lattice. The recipes of Session 4, from "The Chern number of a Landau level" on, take the argument of
`h.add_orbital_magnetic_field` as the flux per unit area of the geometry in units of the flux quantum $h/e$, with the
sign of an electron in a field along $+z$, so for the charge $+e$ of the pages it is the field along $-z$. The recipes
of Session 5, from "Bands of a superconductor with the electron weight" on, write every superconductor in the Nambu
basis $(c_\uparrow,c_\downarrow,c^\dagger_\downarrow,-c^\dagger_\uparrow)$ of (5.6), four entries per site, where
`h.add_onsite(x)` is the chemical potential $\mu=-x$ of the notes. The recipes of Session 6, from "The ferromagnet
against the antiferromagnet at large U" on, take the Hubbard term $Un_\uparrow n_\downarrow$ of (6.1), and
`get_vev("mz")` is the $m=n_\uparrow-n_\downarrow$ of (6.2) on each site, which saturates at 1. The recipes of Session
7, from "The entanglement entropy of a block of free fermions" on, give the entropies in nats, with the natural
logarithm of (7.6), while the interacting spin chains of that session are dmrgpy or numpy lines of its sheet, since a
script to download imports pyqula. The recipes of Session 8, from "The spinon Fermi surface at half filling" on, leave
out the spin chains of the notebook, which use dmrgpy and whose numbers are on the sheet. The recipes of Session 9,
from "The static Lindhard function of a chain" on, use `h.add_onsite(mu)` as the shift $+\mu$ of every onsite energy,
which moves the bands up while the Fermi level stays at zero. The recipes of Session 10, from "A disordered ring" on,
take the sign $-t$ of the notes with `tij=[-1.]` and the temperature in units of the hopping or of the coupling $J$
with $k_B=1$, while the Heisenberg chain, the neural network states, the tensor networks and the gauge theory of that
session have no recipe, since pyqula has no many-body spin chain and no neural network.

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

`kx` and `ky` are in units of $2\pi$ over the lattice constant, which is $\sqrt3$ here, on a rectangle around $\Gamma$
that is a period of the map and holds two zones. `b` is
$\Omega=-2\,\mathrm{Im}\langle\partial_{k_x}u|\partial_{k_y}u\rangle$ of the filled band times the area of the zone,
so its average over the map divided by $2\pi$ is the Chern number with its sign, and with the coupling $+0.1$ it is
positive at $K$ and at $K'$. In the release 0.0.96 `kx` and `ky` run from $-1$ to 1 without the end, on another
window, and the average of `b` divided by $2\pi$ is 0.926 and not the Chern number, so a script there takes the Chern
number from `h.get_chern()`.

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
thermal energy in units of the hopping. Inside the gap it is the Chern number of `h.get_chern()` with the same sign,
$+1$ here, and it goes to zero when the two bands are empty or full. The release 0.0.96 has no
`get_anomalous_hall_conductivity` and raises an `AttributeError`, so there a value inside a gap is `h.get_chern()`,
and the curve against the chemical potential needs the development tree.

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

## Bands with the sign of the notes

```python
import numpy as np
from pyqula import geometry

g = geometry.square_lattice()  # square lattice, lattice constant 1
h = g.get_hamiltonian(has_spin=False, tij=[-1.])  # first-neighbor hopping -1, the sign of (2.14)
nodes = np.array([[0., 0., 0.], [0.5, 0., 0.], [0.5, 0.5, 0.], [0., 0., 0.]])  # Gamma, X, M, Gamma, reduced units
kpath = [nodes[i] + (nodes[i+1] - nodes[i])*j/100 for i in range(3) for j in range(100)] + [nodes[3]]  # 301 momenta
(k, e) = h.get_bands(kpath=kpath)  # the band, one energy per momentum of the path
g3 = geometry.cubic_lattice()  # cubic lattice, lattice constant 1
h3 = g3.get_hamiltonian(has_spin=False, tij=[-1.])  # the sign of (2.15)
(k3, e3) = h3.get_bands(nk=200)  # the default path Gamma, X, M, Gamma, R
```

With `tij=[-1.]` the square band is $-2t(\cos\varphi_x+\cos\varphi_y)$ of (2.14) for $t=1$, so `e` is $-4$, $0$, $4$
and $-4$ at the steps 0, 100, 200 and 300, which are $\Gamma$, $X$, $M$ and $\Gamma$. The path is a list of reduced
momenta, and not `["G","X","M","G"]`, since the release 0.0.96 of PyPI takes "M" as $(1/2,0)$ on every lattice, so on
the square lattice its "M" is $X$. pyqula takes such a list as it is, with no point added. The cubic band goes from
$-6$ at $\Gamma$ to $6$ at $R$ on 201 steps, the width $12t$ of (2.15). Without `tij` both bands are upside down,
$4$, $0$, $-4$ at $\Gamma$, $X$, $M$. pyqula writes `BANDS.OUT`, and the default path also writes `BANDLINES.OUT`.

## The chain with a second-neighbor hopping

```python
import numpy as np
from pyqula import geometry

g = geometry.chain()  # chain with one site per cell, a = 1
eta = 0.3  # second-neighbor hopping
h = g.get_hamiltonian(has_spin=False, tij=[-1., -eta])  # both hoppings with the sign of (2.9)
ks = np.linspace(-0.5, 0.5, 201)  # momentum in units of 2 pi, one zone
(ik, e) = h.get_bands(kpath=[[k, 0., 0.] for k in ks])  # the band, one energy per momentum
phi = 2*np.pi*ks  # the Bloch phase of (2.6), from -pi to pi
```

The place $n$ of `tij` is the hopping to the neighbor at distance $n$, so `e` is $-2\cos\varphi-0.6\cos2\varphi$, which
is (2.9) with $t=1$ and $\eta=0.3$. The notebook writes `tij=[1.0,0.3]`, which gives exactly minus this band, and
changing only the first sign does not give (2.9). Above $\eta=t/4$ the point $\varphi=\pi$ is a local minimum, and
for $\eta=0.3$ it lies only 0.033 below the two maxima at $\cos\varphi=-t/4\eta$, so the extra extremum is there but
hard to see. For $\eta=0.5$ it is 0.5 deep.

## Band folding in a supercell

```python
import numpy as np
from pyqula import geometry

g = geometry.chain().get_supercell(3)  # the same chain with three sites per cell, a = 3
h = g.get_hamiltonian(has_spin=False, tij=[-1.])  # first-neighbor hopping -1, the sign of (2.5)
hk = h.get_hk_gen()  # Bloch Hamiltonian, the momentum is in units of 2 pi over the new cell
ks = np.linspace(-0.5, 0.5, 101)  # the zone of the cell of three sites
bands = np.array([np.linalg.eigvalsh(hk([k, 0., 0.])) for k in ks])  # three bands at each momentum
```

`g` has three sites and the lattice vector 3, so the Bloch Hamiltonian is $3\times3$ and gives three bands in a zone
three times narrower. They are the band of the chain folded, $-2\cos[(\varphi+2\pi m)/3]$ with $m=0,1,2$ and
$\varphi=2\pi k$ the phase per cell of three sites, so at $k=0$ they are $-2$, $1$ and $1$, the $-2t$, $t$, $t$ of the
quiz of Section 2.7. With the default hopping they are $-1$, $-1$ and $2$, and with `g.get_hamiltonian()` the
Hamiltonian is spinful and has six bands, in degenerate pairs.

## The density of states

```python
import numpy as np
from pyqula import geometry

energies = np.linspace(-3.5, 3.5, 701)  # energies in units of the hopping, the window of the notebook
h = geometry.chain().get_hamiltonian(has_spin=False)  # spinless chain, first-neighbor hopping +1
(e, dos_chain) = h.get_dos(energies=energies, mode="Green", delta=1e-3)  # density of states per site
h = geometry.honeycomb_lattice().get_hamiltonian(has_spin=False)  # spinless honeycomb lattice
(e, dos_honeycomb) = h.get_dos(energies=energies, delta=4e-2, nk=200)  # the delta and nk of the notebook
total = np.sum(dos_honeycomb)*(e[1] - e[0])  # number of states per cell in the window
```

`h.get_dos` returns the energies and the number of states per unit cell and per unit of energy, summed over every
band and over both spins, so the default spinful Hamiltonian gives twice the numbers below. `mode="Green"` takes the
Green function with the broadening `delta`, and `dos_chain` is $1/(\pi\sqrt{4-E^2})$ of the chain, 0.159 at zero
energy and 0.241 at $E=1.5$. With no `mode` the call sums Lorentzians of half width `delta` over a mesh of `nk` by
`nk` momenta, as the honeycomb cell of the notebook does. `dos_honeycomb` has the V of the Dirac cones rounded by
`delta`, 0.041 at zero energy in place of 0, two peaks at $\pm1$ from the saddle points $M$, and `total` is 1.98, two
states per cell less the tails. The density of (2.16) is per unit area and per band, so it is `dos_honeycomb`
divided by the cell area $3\sqrt3/2$ and summed over the two bands. The $D(E_F)$ of the Stoner criterion of Sessions 1
and 6, per site and per spin, is the `dos` of the spinful Hamiltonian at $E_F$ divided by 2 and by the number of
sites of the cell, so $1/(2\pi)=0.159$ for the half-filled chain.

## A band on a map of the Brillouin zone

```python
import numpy as np
from pyqula import geometry

g = geometry.honeycomb_lattice()  # honeycomb lattice, bond length 1
h = g.get_hamiltonian(has_spin=False)  # spinless, first-neighbor hopping +1
nk = 60  # points per side of the map
(k, e) = h.get_bands_map(n=0, nk=nk)  # the lowest band on a square window
a = np.linalg.norm(g.a1)  # the unit of the map is 2 pi/a, with a = sqrt(3) here
kx = 2*np.pi/a*np.array(k)[:, 0].reshape(nk, nk)  # Cartesian kx, the first index runs along kx
ky = 2*np.pi/a*np.array(k)[:, 1].reshape(nk, nk)  # Cartesian ky
band = np.array(e).reshape(nk, nk)  # the energy of the lowest band at each point
```

`k` holds `nk*nk` points with both components from $-1$ to `1-2/nk`, without the end, in units of $2\pi$ over the
length of `g.a1`, which is the lattice constant $\sqrt3$ for the honeycomb lattice and 2 for the kagome and Lieb
lattices. `n` counts the bands from 0 at the lowest energy. Here `band` is $-|f(\mathbf k)|$ of (2.19), $-3$ at
$\Gamma$ and 0 at the corners of the zone, such as $(0,\pm2/3)$ in the units of `k`. The window is a square, so it is
not a period of the band, and here it holds $2\sqrt3=3.46$ zones. pyqula writes the map in `BANDS_2D.OUT`.

## The Fermi surface

```python
import numpy as np
from pyqula import geometry

g = geometry.honeycomb_lattice()  # honeycomb lattice, bond length 1
h = g.get_hamiltonian(has_spin=False)  # spinless, first-neighbor hopping +1
nk = 61  # points per side, with nk - 1 a multiple of 6, so Gamma and the corners are on the mesh
delta = 0.05  # half width of each level
(x, y, w) = h.get_fermi_surface(e=0.5, delta=delta, nk=nk)  # spectral weight at the energy e
weight = np.array(w).reshape(nk, nk)  # the map, the first index runs along x
```

`x` and `y` run from $-1$ to $1$ with both ends, in units of $2\pi$ over the length of `g.a1`, as in the map above,
and `w` is $\sum_n\delta/((e-E_n)^2+\delta^2)$, $\pi$ times the spectral function with no $1/\pi$, so a state exactly
at the energy `e` gives $1/\delta$. At $e=0.5$ the weight sits on small rings around the corners $K$ and $K'$, at
about $0.33$ from them in units of the inverse bond length, which is the cone $E=\frac32t|\mathbf q|$. The rings grow
with $e$ and touch at $e=1$, at the saddle points $M$, and for $e$ between 1 and 3 there is one contour around
$\Gamma$. The notebook takes the default spinful Hamiltonian, where every weight is twice. pyqula writes the map in
`FERMI_MAP.OUT`.

## The flat bands of the Lieb and kagome lattices

```python
import numpy as np
from pyqula import geometry

ks = np.arange(30)/30  # a mesh of the zone in units of the reciprocal vectors, with K and M on it
hk = geometry.kagome_lattice().get_hamiltonian(has_spin=False, tij=[-1.]).get_hk_gen()  # kagome, hopping -1
e_kagome = np.array([np.linalg.eigvalsh(hk([k1, k2, 0.])) for k1 in ks for k2 in ks])  # three bands on the mesh
hk = geometry.lieb_lattice().get_hamiltonian(has_spin=False, tij=[-1.]).get_hk_gen()  # Lieb, hopping -1
e_lieb = np.array([np.linalg.eigvalsh(hk([k1, k2, 0.])) for k1 in ks for k2 in ks])  # three bands on the mesh
flat_kagome = e_kagome[:, 2]  # the top band, 2 at every momentum
flat_lieb = e_lieb[:, 1]  # the middle band, 0 at every momentum
```

With `tij=[-1.]`, the sign of the notes, the flat band of the kagome lattice is the top one at $+2$, with the two
other bands between $-4$ and $2$, and the flat band of the Lieb lattice is the middle one at 0. Each holds one third
of the states. With the default $+1$ of pyqula and of the notebook the kagome flat band is the lowest band, at $-2$,
and the Lieb flat band stays at 0. Both lattices have the bond length 1 and the lattice constant 2. The three Lieb
bands meet at zero energy at $(1/2,1/2)$, and the kagome bands cross at $-1$ at $(1/3,-1/3)$, the corner that
`label2k` calls "K'" on this lattice.

## The Dirac velocity of the honeycomb lattice

```python
import numpy as np
from pyqula import geometry

g = geometry.honeycomb_lattice()  # honeycomb lattice, bond length 1
h = g.get_hamiltonian(has_spin=False)  # spinless, first-neighbor hopping +1
hk = h.get_hk_gen()  # Bloch Hamiltonian, the momentum is in units of the reciprocal vectors
A = np.array([g.a1[:2], g.a2[:2]])  # lattice vectors as rows
B = 2*np.pi*np.linalg.inv(A).T  # reciprocal vectors as rows
K = -(B[0] + B[1])/3  # the point "K" of get_bands, (-1/3,-1/3), at (0, -4 pi/3 sqrt3)
q = 1e-4*np.array([0.6, 0.8])  # a small step away from K, in Cartesian momentum
kr = A @ (K + q)/(2*np.pi)  # the same momentum in units of the reciprocal vectors
e = np.linalg.eigvalsh(hk([kr[0], kr[1], 0.]))  # the two energies close to K
velocity = e[1]/np.linalg.norm(q)  # slope of the cone
```

`velocity` is $\hbar v_F$ of (2.20) in units of $t$ times the bond length, $3/2$ as $v_F=3ta/2\hbar$ says, and it is
the same for every direction of `q`. In units of the lattice constant $\sqrt3$ it is 0.866. The momentum that `hk`
takes is $\mathbf k\cdot\mathbf a_i/2\pi$, which is why `kr` is built from the lattice vectors. `K` is the point that
`h.get_bands(kpath=["G","K",...])` calls "K". The other corner, $(\mathbf b_1+\mathbf b_2)/3$, is "K'" there, while
the default path of `h.get_bands()` names it "K" in `BANDLINES.OUT`, and the slope is the same at both.

## The chain with two sites per cell of (2.13)

```python
import numpy as np
from pyqula import geometry

g = geometry.bichain()  # chain with two sites A and B per cell, a = 2
h = g.get_hamiltonian(has_spin=False)  # every hopping +1
eta = 0.6  # hopping between cells
h.inter = eta*h.inter  # the bond from B of a cell to A of the next cell becomes eta
hk = h.get_hk_gen()  # H(phi) of (2.12), with phi = 2 pi k
ks = np.linspace(-0.5, 0.5, 101)  # momentum in units of 2 pi over the cell of two sites
bands = np.array([np.linalg.eigvalsh(hk([k, 0., 0.])) for k in ks])  # the two bands of (2.13)
gap = bands[0, 1] - bands[0, 0]  # the gap at the edge of the zone, phi = pi
```

`hk([k,0,0])` is the matrix (2.13) entry by entry, with $A$ the first site and $\varphi=2\pi k$, since pyqula builds
`h.intra + h.inter*exp(2j*pi*k)` plus its Hermitian conjugate, which is (2.12) with `h.inter` as $\gamma$. The bands
are $\pm|1+\eta e^{-i\varphi}|$, the gap at the edge of the zone is $2|1-\eta|=0.8$, and with `eta = 1.` it closes.
The recipe "The SSH chain and its open chain" builds the same chain with the weak hopping inside the cell, as Session
3 does, and looks at the open chain. This one keeps the strong hopping inside the cell, as (2.13) does, and gives the
bands over the zone.

## The levels of an open chain

```python
import numpy as np
from pyqula import geometry

N = 10  # number of sites
g = geometry.chain().get_supercell(N)  # N sites in one cell
g.dimensionality = 0  # cut the chain, so that it has two ends
h = g.get_hamiltonian(has_spin=False)  # spinless, hopping +1 between neighbors
levels = np.linalg.eigvalsh(h.intra)  # the N levels, sorted
spacing = levels[N//2] - levels[N//2 - 1]  # spacing at the center of the band
hm = g.get_hamiltonian(has_spin=False, tij=[-1.])  # hopping -1, the sign of (1.6)
(e, v) = np.linalg.eigh(hm.intra)  # the same levels, and one state per column
lowest = v[:, 0]  # the lowest state
```

The levels are $2\cos(n\pi/(N+1))$ for $n=1,\dots,N$, which is the same set as $-2t\cos(n\pi/(N+1))$ of the notes,
since the chain is bipartite. The spacing at the center is $4\sin(\pi/(2(N+1)))=0.569$ for $N=10$, close to
$2\pi/(N+1)$. With the hopping $+1$ the lowest state changes sign on every bond, while with `tij=[-1.]` it has one
sign on every site, and in both cases its weight on site $j$ is the box $2\sin^2(\pi j/(N+1))/(N+1)$. Without
`has_spin=False` every level comes twice.

## The Hubbard dimer in mean field

```python
import numpy as np
from pyqula import geometry

g = geometry.bichain()  # chain with two sites per cell
g.dimensionality = 0  # keep only the two sites, the dimer
h = g.get_hamiltonian()  # with the two spins, hopping +1
Us = np.array([0., 1., 1.5, 2.5, 3., 4., 6.])  # interactions, in units of the hopping
moment, gap, energy = [], [], []
for U in Us:
    (hmf, e) = h.get_mean_field_hamiltonian(U=U, mf="antiferro", mix=0.9, return_total_energy=True)  # two electrons
    moment.append(abs(hmf.get_vev("mz")[1]))  # |n_up - n_dn| on the second site
    gap.append(hmf.get_gap())  # gap between the filled and the empty levels
    energy.append(e)  # mean-field energy with its double counting
exact = Us/2 - np.sqrt(Us**2/4 + 4)  # the exact ground-state energy, for comparison
```

`get_vev("mz")` is $m=\langle n_\uparrow\rangle-\langle n_\downarrow\rangle$ of (1.8) on each site, between $-1$ and $1$,
which is twice $\langle S_z\rangle$, and with the guess `"antiferro"` it is negative on the first site. The moment
is zero up to $U=2$ and $\sqrt{1-4/U^2}$ above, $0.745$ at $U=3$ and $0.866$ at $U=4$, the gap is $2$ up to $U=2$ and
$U$ above, and the energy is $-2+U/2$ up to $U=2$ and exactly $-2/U$ above, which stays above `exact`, $-0.83$ at
$U=4$. Below $U=2$ the loop stops with a moment smaller than $10^{-3}$, which is its tolerance and not a moment. This
is the cell "The interacting Hubbard dimer" of the notebooks of Sessions 1 and 6. The exact dimer has no moment at
any $U$, and `exact` is its singlet, which lies $\sqrt{U^2/4+4t^2}-U/2$ below the triplet at zero energy, a splitting
that the mean field does not give.

## The antiferromagnet of the half-filled Hubbard chain

```python
import numpy as np
from pyqula import geometry

g = geometry.bichain()  # chain with two sites per cell
h = g.get_hamiltonian()  # with the two spins, hopping +1
U = 3.0  # the U of U n_up n_dn in (1.7)
nk = 100  # cells of the mesh, the default of the loop is 8
(hmf, energy) = h.get_mean_field_hamiltonian(U=U, mf="antiferro", mix=0.5, nk=nk, return_total_energy=True)
m = hmf.get_vev("mz", nk=nk)  # n_up - n_dn on the two sites, the m of (1.8)
gap = hmf.get_gap()  # the gap of the mean-field bands
field = hmf.extract("mz")  # the exchange field on the two sites, not the moment
```

`m` is $-0.621$ and $+0.621$ on the two sites, the sign set by the guess, and the gap is $U|m|=1.862$. `energy` is the
mean-field energy per cell of two sites with its double counting,
$\langle H_\text{kin}\rangle+U\langle n_\uparrow\rangle\langle n_\downarrow\rangle$, which is $-1.190$ here and
$-8/\pi$ at $U=0$. `field` is $(H_{\uparrow\uparrow}-H_{\downarrow\downarrow})/2=-Um/2$, $+0.931$ where `m` is
$-0.621$, so a picture of the moment takes `get_vev` and not `extract`, and a plot of `extract("mz")`, as the notebook
of Session 6 makes, draws the moments reversed. The onsite energies of `hmf.intra` hold the splitting $U|m|$, 0.681 at
$U=2$, as the gap equation $1=U\frac1N\sum_k 1/(2\sqrt{\varepsilon_k^2+(Um/2)^2})$ gives, and at $U=4$, the value of
Session 6, `m` is $\mp0.769$, the gap 3.076 and `energy` $-0.938$. The guess `mf="XY"` gives the same $|m|$, gap and
energy with the moment in the plane. The chain of `bichain()` is not dimerized, and its cell of two sites only holds
the antiferromagnet. The loop runs on a mesh of `nk` cells, 8 when it gets none, and `get_vev` sums on a mesh of its
own, 30 cells when it gets none, so a script passes the same `nk` to both. At small $U$ the gap $Um$ is smaller than
the spacing of a coarse mesh, and with the default `nk=8` the loop gives $m=0.192$ at $U=1$, where the converged value
is $0.0299$, and after a loop with `nk=1001`, which gives 0.030, `get_vev("mz")` with no `nk` reads 0.050.

## The antiferromagnet of the honeycomb lattice

```python
import numpy as np
from pyqula import geometry

g = geometry.honeycomb_lattice()  # honeycomb lattice
h = g.get_hamiltonian()  # with the two spins, hopping +1
nk = 20  # cells of the mesh along each direction
hmf = h.get_mean_field_hamiltonian(U=3.0, mf="antiferro", mix=0.9, nk=nk)  # half filling
m = hmf.get_vev("mz", nk=nk)  # n_up - n_dn on the two sublattices
gap = hmf.get_gap()  # the gap, at K
```

`m` is $\mp0.444$ at $U=3$ and the gap is $U|m|=1.33$. The moment appears only above $U_c=2.23$ on a dense mesh. A
mesh that does not hold $K$ moves the onset up, to $2.375$ for the `nk=10` of the notebook and $2.29$ for `nk=20`,
and a mesh with `nk` a multiple of 3 holds the Dirac points, which give a moment below $U_c$, $0.015$ at $U=2$ with
`nk=30`. A page quotes the threshold from the dense mesh.

## The charge density wave of the spinless chain

```python
import numpy as np
from pyqula import geometry

g = geometry.bichain()  # chain with two sites per cell
h = g.get_hamiltonian(has_spin=False)  # spinless, hopping +1
V = 3.0  # the V of V n_i n_(i+1) in (1.6)
nk = 100  # cells of the mesh
hf = h.get_mean_field_hamiltonian(V1=V, mf="CDW", filling=0.5, mix=0.5, nk=nk, write=False)  # Hartree-Fock, the default
hartree = h.get_mean_field_hamiltonian(V1=V, mf="CDW", filling=0.5, mix=0.5, nk=nk, write=False, compute_cross=False)
n_hf = hf.get_vev(nk=nk)  # charge of the two sites
n_hartree = hartree.get_vev(nk=nk)  # charge of the two sites
imbalance_hf = abs(n_hf[0] - n_hf[1])  # with the Fock term
imbalance_hartree = abs(n_hartree[0] - n_hartree[1])  # Hartree alone, the decoupling of Section 1.13
hopping_hf = abs(hf.intra[0, 1])  # the hopping inside the cell after the Fock term
```

`V1` is the repulsion per bond between first neighbors and `filling=0.5` is half filling, one electron per cell. The
default call is Hartree-Fock, so besides the onsite energies $\pm V\delta n$ it raises the hopping from 1 to 1.725 on
both bonds, and the imbalance is 0.704. With `compute_cross=False` it is Hartree alone, the decoupling of the pages
and of Figures 1.4 and 1.5, and the imbalance is 0.892, the moment of the Hubbard chain at $U=2V$. In both the gap is
$2V\delta n$. The guess `mf="CDW"` adds the onsite energies $\pm1$, a strong seed. `compute_cross` is accepted only
by the spinless mean field, and the spinful one raises a `TypeError`. The spinless mean field writes the file
`MF.pkl` unless it gets `write=False`, and with `mf=None` it reads that file back as its first guess, so a script
always gives `mf`.

## A seed field that stays in the Hamiltonian

```python
import numpy as np
from pyqula import geometry

g = geometry.bichain()  # two sites per cell
g.dimensionality = 0  # the dimer
moments = []  # |m| for each U
for U in (1.0, 4.0):  # below and above the threshold U=2
    h = g.get_hamiltonian()  # with the two spins
    h.add_antiferromagnetism(0.001)  # a staggered field b that stays in the Hamiltonian
    hmf = h.get_mean_field_hamiltonian(U=U, mf="antiferro", mix=0.5)
    moments.append(abs(hmf.get_vev("mz")[0]))  # the moment on the first site
```

`add_antiferromagnetism(b)` adds $+b$ to the spin up and $-b$ to the spin down of the first site and the opposite on
the second. Below the threshold the moment follows the field, $b/(1-U/2)=0.002$ at $U=1$, and it vanishes with it.
Above the threshold it stays at $\sqrt{1-4/U^2}=0.866$, so the field only picks one of the two ordered states.

## The s-wave superconductor of the attractive Hubbard chain

```python
import numpy as np
from pyqula import geometry

g = geometry.chain()  # chain with one site per cell
h = g.get_hamiltonian()  # with the two spins, hopping +1
h.setup_nambu_spinor()  # Nambu basis, with no pairing yet
hmf = h.get_mean_field_hamiltonian(U=-3.0, mf="swave", mix=0.5, nk=100)  # attractive U, half filling
delta = np.abs(hmf.extract("swave"))  # the modulus of the pairing, |U <c_dn c_up>|, an energy
hk = hmf.get_hk_gen()  # Bogoliubov-de Gennes Hamiltonian, momentum in units of 2 pi
ks = np.linspace(0., 1., 401)  # momenta across the zone
e = np.array([np.linalg.eigvalsh(hk([k, 0., 0.])) for k in ks])  # quasiparticle energies
gap = 2*np.min(np.abs(e))  # the gap between the two branches
```

`delta` is $0.931$, which is $|U||\langle c_\downarrow c_\uparrow\rangle|$ with
$|\langle c_\downarrow c_\uparrow\rangle|=0.310$, the energy $\Delta_n$ of (5.3) and not the number $\Delta$ of (1.9),
and the gap is $2|\Delta|=1.862$. `U` is the $U n_\uparrow n_\downarrow$ of (1.7) and (5.2), and the Hamiltonian is in
the Nambu basis (5.6) of Session 5, where `hmf.intra[0, 2]` is $\Delta=U\langle c_\downarrow c_\uparrow\rangle$ with
its sign, real and $+0.931$ for the guess `"swave"`, so $\langle c_\downarrow c_\uparrow\rangle=-0.310$. At half
filling this is the gap of the antiferromagnet at $U=+3$, since the attractive and the repulsive chains map onto each
other, and a guess `mf="CDW"` at $U=-3$ gives a charge density wave with the charges 0.379 and 1.621 and the same gap.
`filling` is the fraction of the two states of a site that is filled, and with `filling=0.1`, which is 0.2 electrons
per site, the loop gives $\Delta=0.103$ at $U=-1$, the solution of the BCS gap equation at the same density, 0.223 at
$U=-1.5$ and 0.361 at $U=-2$, the same on every run. With the release 0.0.96 the half-filled numbers are the same,
while at `filling=0.1` the loop gives 0.103, 0.222 and 0.372, and at $U=-1$ it keeps 0.188 electrons per site.

## The Chern number of a Landau level

```python
import numpy as np
from pyqula import geometry

q = 20  # plaquettes per flux quantum
g = geometry.square_lattice().get_supercell((1, q))  # magnetic cell of q sites along y
h = g.get_hamiltonian(has_spin=False)  # spinless Hamiltonian with first-neighbor hopping 1
h.add_orbital_magnetic_field(1/q)  # one flux quantum through the cell, so the gauge is periodic
levels = np.linalg.eigvalsh(h.get_hk_gen()([0., 0., 0.]))[:3]  # the three lowest Landau levels
h.add_onsite(-0.5*(levels[0] + levels[1]))  # zero of energy in the gap above the lowest level
chern = h.get_chern(nk=20)  # Chern number of the states below zero energy, it gives 1
fermi = np.array([-0.5, 0., 0.55])  # below the lowest level, in the first gap and in the second gap
sigma_xy = h.get_anomalous_hall_conductivity(fermi=fermi, T=0.01, nk=20)  # it gives 0, 1 and 2
```

The levels are $-3.70$, $-3.12$ and $-2.58$, below $-4+4\pi\phi\,(n+\tfrac12)$ by the lattice correction of the
conventions sheet. `h.get_chern()` counts the states below zero energy, and `add_onsite` adds its argument to every
onsite energy, so it sets the Fermi energy, and `chern` is the Chern number of the lowest level. It is $+1$ with this
sign of the field and $-1$ with `add_orbital_magnetic_field(-1/q)`. `sigma_xy` is in units of $e^2/h$ and counts the
filled levels. The flux through the cell, `q` times the argument, has to be an integer. With the field $0.013$ in the
cell of 10 sites, one plaquette of each cell carries $0.117$ of the opposite sign in place of $0.013$, and pyqula
gives no warning. The release 0.0.96 has no `get_anomalous_hall_conductivity` and raises an `AttributeError`, and
there the same 0, 1 and 2 come from `h.get_chern()` after a further `h.add_onsite(-fermi)` for each Fermi energy.

## The density of states of the bulk of a ribbon

```python
import numpy as np
from pyqula import geometry

g = geometry.square_ribbon(20)  # ribbon of the square lattice, 20 sites wide
h = g.get_hamiltonian(has_spin=False)  # spinless Hamiltonian with first-neighbor hopping 1
h.add_orbital_magnetic_field(0.02)  # flux per plaquette, in flux quanta
energies = np.linspace(-4.5, 4.5, 1801)  # the whole band, in steps of 0.005
(e, dos) = h.get_dos(energies=energies, delta=1e-2, nk=400)  # states per unit of energy per cell
(e, dos_bulk) = h.get_dos(energies=energies, delta=1e-2, nk=400, operator="bulk")  # the same on the bulk sites
```

`dos` is the number of states per unit of energy per cell of the ribbon, with every level a Lorentzian of half width
`delta`, so its integral over the band is 19.96, the 20 sites of the cell less the tails of the Lorentzians. With
`operator="bulk"` only the sites in the middle 80 percent of the width count, the integral is 15.97, and the edge
states drop out, so the peaks are the bulk Landau levels, at $-3.875$, $-3.630$ and $-3.395$, the levels $-3.876$,
$-3.633$ and $-3.397$ of the lattice. Their spacings are 0.245 and 0.235, below $\hbar\omega_c=4\pi\cdot0.02=0.251$
because of the lattice. pyqula writes the file `DOS.OUT`.

## The Dirac Landau levels of the honeycomb lattice

```python
import numpy as np
from pyqula import geometry

g = geometry.honeycomb_armchair_ribbon(40)  # armchair ribbon of the honeycomb lattice, bond length 1
h = g.get_hamiltonian(has_spin=False)  # spinless Hamiltonian with first-neighbor hopping 1
h.add_orbital_magnetic_field(0.01)  # flux per unit area, a hexagon holds 2.6 times this
energies = np.linspace(-0.8, 0.8, 321)  # energies around the Dirac point, in steps of 0.005
(e, dos) = h.get_dos(energies=energies, delta=1e-2, nk=100, operator="bulk")  # density of states of the middle
E1 = 3*np.sqrt(np.pi*0.01)  # the first level of (4.7), with hbar v = 3/2 for the bond length 1
```

The argument is the flux per unit area and not per hexagon, so $\ell_B=1/\sqrt{2\pi\cdot0.01}=4.0$ bond lengths and
the continuum gives $E_1=3\sqrt{\pi\phi}\,t=0.53$. The peaks of `dos` are at $0$, $\pm0.52$ and $\pm0.715$, the
levels $0$, $\pm E_1$ and $\pm\sqrt2E_1$ of (4.7) lowered by the lattice by about $0.1\,(E/t)^2$ of their energy. The
fields 0.005 and 0.02 of the notebook move the first peak to 0.37 and 0.71, a factor 1.92 for a field four times
larger, and near 0.02 the lattice broadens the first level, as the conventions sheet says.

## The local density of states of a ribbon in a field

```python
import numpy as np
from pyqula import geometry

g = geometry.honeycomb_armchair_ribbon(20)  # armchair ribbon of the honeycomb lattice, 80 sites per cell
h = g.get_hamiltonian(has_spin=False)  # spinless Hamiltonian with first-neighbor hopping 1
h.add_orbital_magnetic_field(0.01)  # flux per unit area, the first Landau level is at 0.52
(x, y, ldos) = h.get_ldos(e=0.53/3, nrep=20, delta=1e-2, nk=50)  # local density of states on 20 cells
lB = 1/np.sqrt(2*np.pi*0.01)  # magnetic length, 4.0 bond lengths
edge = np.abs(y - np.mean(y)) > (np.max(y) - np.min(y))/2 - lB  # sites within l_B of an edge
fraction = np.sum(ldos[edge])/np.sum(ldos)  # weight at the edges, 0.57
```

`x`, `y` and `ldos` have one entry per site of `nrep` cells along the ribbon, 1600 here, and the sum of `ldos` over
one cell is the density of states at the energy `e`, 1.06. The energy $0.177$, one of the four of the notebook, is in
the gap between the zero level and the first level at 0.52, so the 25 percent of the sites within $\ell_B$ of the two
edges hold 57 percent of the weight, and the states at this energy are the chiral edge states. At $0.353$ they hold
54 percent, while at zero energy, in the zero level, they hold 4 percent, and at $0.53$, on the first level, 16
percent. pyqula writes the file `LDOS.OUT`.

## An island in a magnetic field

```python
import numpy as np
from pyqula import islands

g = islands.get_geometry(name="honeycomb", n=12, nedges=6, rot=np.pi/6)  # flake with six armchair edges
h = g.get_hamiltonian(has_spin=False)  # Hamiltonian of the flake
h.add_orbital_magnetic_field(0.01)  # flux per unit area, Landau gauge
levels = np.sort(h.get_bands()[1])  # the 834 levels of the flake
h2 = g.get_hamiltonian(has_spin=False)  # the same flake again
h2.add_orbital_magnetic_field(0.01, gauge="symmetric")  # the same field in the symmetric gauge
levels2 = np.sort(h2.get_bands()[1])  # the same levels
(x, y, ldos) = h.get_ldos(e=0.25, delta=0.03)  # local density of states inside the gap above the zero level
```

The two gauges give the same levels to $10^{-12}$, since an island has no translation that the gauge has to keep.
`gauge="symmetric"` is only for an island, and on the square ribbon it gives the levels of the Landau gauge with half
the field. Between the zero level and the first bulk level, at 0.51, the flake has a ladder of edge levels about 0.06
apart, and at the energy 0.25 the sites within two bond lengths of the edge, 19 percent of them, hold 37 percent of
the weight, twice their share, where at zero energy, in the zero level, they hold 9 percent. The edge states of a
field are about $\ell_B=4$ bond lengths wide, so they reach further in than those of the Haldane flake of the recipe
"A finite island and its local density of states".

## The Chern number of a Landau gap of the honeycomb lattice

```python
import numpy as np
from pyqula import geometry

n = 20  # cells of the magnetic supercell
g = geometry.honeycomb_lattice_square_cell().rotate(90)  # rectangular cell of 4 sites with a bond along y
g = g.get_supercell((n, 1))  # magnetic supercell of 80 sites, stretched along y
phi = 1/(3*np.sqrt(3)*n)  # one flux quantum through the cell of area 3 sqrt(3) n
h = g.get_hamiltonian(has_spin=False)  # spinless Hamiltonian with first-neighbor hopping 1
h.add_orbital_magnetic_field(phi)  # flux per unit area, in flux quanta
h.add_onsite(-0.25)  # zero of energy in the gap between the zero level and the first level at 0.51
chern = h.get_chern(nk=8)  # Chern number of the states below the gap, it gives 1
```

The cell of this orientation keeps every hexagon at the flux $\phi$ for any whole number of flux quanta through the
cell, and the cell `honeycomb_lattice_square_cell().get_supercell((1, n))` of the other orientation needs an even
number of them. Here $\phi=0.0096$, the first level is at $0.509$, and the gap above the zero level has $C=+1$, the
gap below it $-1$, with `h.add_onsite(0.25)` in place of $-0.25$, and the gap above the first level $+3$, since every
level of the honeycomb lattice holds the two valleys. This is the sign of `h.add_haldane(0.07)`, which gives $+1$ in
the same cell.

## From the Haldane model to the quantum Hall state

```python
import numpy as np
from pyqula import geometry

g = geometry.honeycomb_armchair_ribbon(20)  # armchair ribbon of the honeycomb lattice
H_hall = g.get_hamiltonian(has_spin=False)  # the quantum Hall state
H_hall.add_orbital_magnetic_field(0.01)  # flux per unit area, the first level is at 0.52
H_hall.add_onsite(-0.2)  # zero energy now sits in the gap above the zero level
H_chern = g.get_hamiltonian(has_spin=False)  # the Chern insulator
H_chern.add_haldane(0.07)  # Haldane coupling, C = 1 and the gap 0.63
central = np.abs(g.y) < 0.5*np.max(g.y)  # the middle half of the ribbon
nus = np.linspace(0., 1., 11)  # steps of the interpolation
closest = []  # for each step, the bulk state closest to zero energy
for nu in nus:
    hk = (H_hall*nu + H_chern*(1 - nu)).get_hk_gen()  # Bloch Hamiltonian of the interpolation
    e_min = 10.
    for k in np.linspace(-0.5, 0.5, 41):
        (e, v) = np.linalg.eigh(np.array(hk([k, 0., 0.])))  # states at the momentum k
        bulk = np.sum(np.abs(v[central])**2, axis=0) > 0.5  # states with most weight in the middle
        e_min = min(e_min, np.min(np.abs(e[bulk])))
    closest.append(e_min)
```

`closest` is never below 0.198, which it reaches at `nu=1`, so no bulk state comes to zero energy along the path and
the bulk gap stays open. The two ends have the same Chern number, $+1$, since the field of
`add_orbital_magnetic_field(0.01)` has this sign above its zero level. With `add_haldane(-0.07)`, with the field
$-0.01$, or with `add_onsite(+0.2)`, which puts zero energy below the zero level, the two ends have opposite Chern
numbers and a bulk state comes to zero energy on the way. `H_hall*nu + H_chern*(1 - nu)` adds the matrices bond by
bond, so at `nu=0.5` a bond with the Peierls phase $\theta$ becomes $(e^{i\theta}+1)/2$, of modulus 0.86 at the edge,
and the mix is not a field of half the strength.

## A domain wall in the onsite energy

```python
import numpy as np
from pyqula import geometry

g = geometry.square_ribbon(80)  # ribbon of the square lattice, 80 sites wide
g.center()  # the middle of the ribbon at y = 0
h = g.get_hamiltonian(has_spin=False)  # spinless Hamiltonian with first-neighbor hopping 1
h.add_orbital_magnetic_field(0.02)  # flux per plaquette, in flux quanta
h.add_onsite(np.where(g.y > 0., 3.5, -3.5))  # one onsite energy per site, +3.5 above y = 0 and -3.5 below
nk = 401  # number of momenta
kpath = [[k, 0., 0.] for k in np.linspace(-0.5, 0.5, nk)]  # the whole zone, in units of 2 pi
(ik, e, y) = h.get_bands(operator="yposition", kpath=kpath)  # bands with the position of each state
energies = np.array(e).reshape(nk, -1)  # energy of band n at momentum k
positions = np.array(y).reshape(nk, -1)  # where each state sits across the ribbon
```

`add_onsite` takes an array with one energy per site, and it adds the same as the function `mufun` of the notebook
cell "Topological domains in the quantum Hall state". The half with $y>0$ has its band from $-0.5$ to $7.5$, so zero
energy is 0.5 above its bottom, with two electron levels below it and $C=+2$. The half with $y<0$ has zero energy 0.5
below the top of its band, with two hole levels above it and $C=-2$. Zero energy is crossed by four branches at the
domain wall, one for each unit of the jump of $C$, and by two at each outer edge. The comment of the notebook calls
the upper half a hole band, while it has electron levels.

## Bands of a superconductor with the electron weight

```python
import numpy as np
from pyqula import geometry

g = geometry.chain()  # chain with first-neighbor hopping 1, the band is 2 cos k
h = g.get_hamiltonian()  # Hamiltonian with the two spins
h.add_onsite(-1.0)  # every energy goes down by 1, which is mu=1 for the band 2 cos k
h.add_swave(0.3)  # Nambu spinor and s-wave pairing Delta=0.3
nk = 201  # number of momenta
kpath = [[k, 0., 0.] for k in np.linspace(-0.5, 0.5, nk)]  # momentum in units of 2 pi
(ik, e, c) = h.get_bands(operator="electron", kpath=kpath)  # BdG bands and their electron weight
energies = np.array(e).reshape(nk, -1)  # the four BdG bands at each momentum
weights = np.array(c).reshape(nk, -1)  # electron weight of each state, from 0 to 1
smallest = np.min(np.abs(energies))  # smallest quasiparticle energy, it is Delta
```

Each momentum has four BdG states, two spins times electron and hole, and they come in pairs $\pm E$ with
$E=\sqrt{\varepsilon^2+\Delta^2}$ and $\varepsilon=2\cos k-1$. The smallest energy is $|\Delta|=0.3$, at the Fermi
momenta $k=\pm1/6$ in units of $2\pi$, and the gap between the two branches is $2|\Delta|=0.6$. The electron weight
of the state at $+E$ is $u^2=(1+\varepsilon/E)/2$, so it is 1/2 at the Fermi momenta, close to 1 where
$\varepsilon\gg\Delta$ and close to 0 where $\varepsilon\ll-\Delta$. With `h.add_swave(0.)` the hole band is the
mirror $-\varepsilon$ of the electron band, and the two cross at the Fermi momenta. The notebook cell does the same on
the square lattice with `h.set_filling(0.2, nk=20)`, `h.setup_nambu_spinor()` and `h.add_swave(0.8)`, and there
`h.get_bands(operator="electron", nk=800)` gives the smallest energy 0.8. `h.intra` is the $4\times4$ onsite matrix
in the Nambu basis (5.6), with $\Delta$ at the places (0,2) and (1,3), and `h.get_gap()` is the full gap $2|\Delta|$,
0.6 here, so the notebook of Session 9 divides it by two to get $\Delta$. `h.add_exchange([0., 0., J])` before
`add_swave` adds $J\sigma_z$, which enters the hole block as $(J,-J)$ in this basis, the same sign as in the electron
block, while the onsite energy changes sign there.

## Pairing of a given symmetry in momentum space

```python
import numpy as np
from pyqula import geometry

g = geometry.square_lattice()  # square lattice, the band is 2 (cos kx + cos ky)
h = g.get_hamiltonian()  # Hamiltonian with the two spins
h.add_pairing(mode="dx2y2", delta=0.1)  # d-wave pairing on the first-neighbor bonds
hk = h.get_hk_gen()  # Bloch Hamiltonian, the momentum in units of 2 pi
ks = np.linspace(-0.5, 0.5, 41)  # momenta along each axis
pairing = np.array([[hk([kx, ky, 0.])[0, 2].real for ky in ks] for kx in ks])  # entry of c_up and c_dn^dag
```

The entry is $2\delta(\cos k_x-\cos k_y)$ with $\delta=0.1$, so $\Delta_0$ of (5.13) is $2\delta=0.2$. It is $-0.4$
at $X=(\pi,0)$ and zero on the diagonals $k_x=\pm k_y$, and the first index of `pairing` runs along $k_x$. The mode
`"extended_swave"` gives $2\delta(\cos k_x+\cos k_y)$, `"swave"` gives the constant $\delta$, and `"chiral_pwave"`
gives $-2i\delta(\sin k_x+i\sin k_y)$ at this entry and the opposite sign at the entry `[1, 3]`, a triplet with the
d-vector along $z$, which is $p_x+ip_y$.

## Spin-triplet superconductivity from an attractive interaction in a magnet

```python
import numpy as np
from pyqula import geometry

np.random.seed(0)  # the loop starts from a random guess
g = geometry.triangular_lattice()  # triangular lattice
h = g.get_hamiltonian()  # Hamiltonian with the two spins
h.add_exchange([0., 0., -2.])  # exchange field, spin up moves down by 2 and spin down up by 2
h.setup_nambu_spinor()  # Nambu spinor with no pairing yet
hscf = h.get_mean_field_hamiltonian(V1=-1., filling=0.3, mix=0.3, mf="random")  # attraction on the bonds
chern = hscf.get_chern(nk=60)  # Chern number of the solution, +1 or -1
hk = hscf.get_hk_gen()  # Bloch Hamiltonian of the solution
ks = np.arange(60)/60  # mesh of the zone
e = np.array([np.linalg.eigvalsh(hk([kx, ky, 0.])) for kx in ks for ky in ks])  # BdG energies on the mesh
gap = e[:, 2].min() - e[:, 1].max()  # gap between the two branches on the mesh
```

This is the loop of the notebook cell "Interaction-induced spin-triplet superconductivity". `V1` is an attractive
interaction between first neighbors, and `mf="random"` starts from a random guess, so the run depends on the seed. The
solution pairs only up with up, a triplet, and it has $|C|=1$ on every seed, while the sign of $C$ is chosen by the
start. A page gives $|C|=1$ and says that the chirality is chosen spontaneously. The mesh of 60 gives the gap 0.375
between the branches, and a mesh bounds a gap from above. A minimization from the best point of the mesh gives 0.373,
so the smallest energy is 0.186. With the release 0.0.96 the same seed ends at a slightly different solution, with
$|C|=1$, the gap 0.375 from the minimization and the smallest energy 0.188.

## The density of states of a superconductor

```python
import numpy as np
from pyqula import geometry

g = geometry.chain()  # chain with first-neighbor hopping 1
h = g.get_hamiltonian()  # Hamiltonian with the two spins
h.add_onsite(-1.0)  # mu=1 for the band 2 cos k
h.add_swave(0.3)  # s-wave pairing Delta=0.3
energies = np.linspace(-4., 4., 801)  # energies of the DOS
(e, dos) = h.get_dos(energies=energies, delta=0.02, nk=2000)  # DOS of all the BdG states
(e, dos_e) = h.get_dos(energies=energies, delta=0.02, nk=2000, operator="electron")  # electron part
```

Every level is a Lorentzian of half width `delta`. `dos` counts the four BdG states of a site, so it integrates to
about 4 and it is symmetric in energy, while `dos_e` is the electron part, which integrates to about 2 and is the
quantity that a tunneling experiment measures. Inside $|E|<0.3$ only the Lorentzian tails remain, `dos_e` is 0.024 at
$E=0$, and it has its coherence peaks just outside $|\Delta|$, at $\pm0.31$, with a height of 0.87. The two higher
peaks of `dos_e`, at 1.03 and $-3.0$, are the band edges of the chain, where $\varepsilon=1$ and $\varepsilon=-3$, and
not the gap. The notebook cell, with `h.set_filling(0.2, nk=20)`, `h.add_swave(0.8)`, `delta=1e-2` and `nk=1000` on
1001 energies from $-5$ to 5, gives the integrals 3.993 and 1.996 and the coherence peaks of `dos` at $\pm0.81$.

## The Chern number of a superconductor

```python
from pyqula import geometry

g = geometry.triangular_lattice()  # triangular lattice, the band runs from -3 to 6
h = g.get_hamiltonian()  # Hamiltonian with the two spins
h.add_onsite(-3.0)  # Fermi level at 3 in the band, the empty states form a pocket around Gamma
h.add_pairing(mode="chiral_pwave", delta=0.4)  # chiral p-wave pairing
chern = h.get_chern()  # Chern number of the BdG bands below zero, it gives -2

h = g.get_hamiltonian()  # the same lattice again
h.add_onsite(-3.0)  # the same Fermi level
h.add_swave(1.0)  # s-wave pairing
chern_s = h.get_chern()  # it gives 0
```

The Chern number counts all the BdG bands below zero, with no factor one half, and has the sign of Session 3. The
chiral p-wave gives $-2$ here, one unit from each spin block, since this Fermi surface encloses empty states. The
same `chiral_pwave` on the square lattice gives $+2$ for a pocket of filled states, for instance with
`h.add_onsite(3.0)`, and $-2$ with `h.add_onsite(-3.0)`. The sign of `delta` does not change it. The other chirality
is not a mode of pyqula, and `L=-1` as a keyword raises a TypeError. A script that needs it passes
`mode=partial(get_triplet, df=get_callable([0., 0., 1.]), L=-1)`, with `partial` from `functools`, `get_triplet` from
`pyqula.sctk.pairing` and `get_callable` from `pyqula.utilities`, which defines no function and gives $+2$ here.

## The edge states of a topological superconductor

```python
import numpy as np
from pyqula import geometry, ribbon

g = geometry.triangular_lattice()  # triangular lattice
gr = ribbon.bulk2ribbon(g, n=20)  # ribbon of width 20, periodic along x
h = gr.get_hamiltonian()  # Hamiltonian of the ribbon with the two spins
h.add_onsite(-3.0)  # the Fermi level of the recipe of the Chern number
h.add_pairing(mode="chiral_pwave", delta=0.4)  # chiral p-wave, Chern number -2 in the bulk
nk = 200  # number of momenta
kpath = [[k, 0., 0.] for k in np.linspace(-0.5, 0.5, nk, endpoint=False)]  # momentum along the ribbon
(ik, e, y) = h.get_bands(operator="yposition", kpath=kpath)  # bands with the position of each state
energies = np.array(e).reshape(nk, -1)  # energy of band n at momentum k
positions = np.array(y).reshape(nk, -1)  # where each state sits across the ribbon
```

The bulk keeps a smallest energy of 1.34, and the states inside this gap sit at the two edges. At $k=0$ the branches
of the two edges meet, at $\pm0.0012$ for this width, and the states there mix the two edges. At each energy inside
the gap there are two branches at each edge, one from each spin block, and with $C=-2$ the two at the edge of
positive $y$ go down with $k$ while the two at the other edge go up. The pairing of the other chirality reverses
both. With `h.add_swave(1.0)` in place of the chiral pairing nothing is left inside the gap, whose smallest energy
is 1.0.

## The open Kitaev chain and its end modes

```python
import numpy as np
from pyqula import geometry

L = 20  # number of sites
g = geometry.chain().get_supercell(L)  # L sites in one cell
g.dimensionality = 0  # an open chain, with no periodicity
h = g.get_hamiltonian()  # Hamiltonian with the two spins
h.add_onsite(4.0)  # every energy goes up by 4
h.add_exchange([0., 0., 4.])  # spin up goes up by 4 more, spin down comes back to the band 2 cos k
h.add_onsite(-1.0)  # mu=1 for the spin-down band
h.add_pairing(mode="pwave", delta=0.5, d=[1., 0., 0.])  # p-wave pairing of two spin-down electrons
(index, levels) = h.get_bands()  # the BdG levels of the open chain
splitting = np.sort(np.abs(levels))[0]  # the level closest to zero, the two end modes
```

pyqula has no spinless Nambu Hamiltonian, so the spinless chain of (5.19) is the spin-down band of a chain whose
spin-up band is far above. The 40 levels closest to zero are those of (5.19) with $t=1$, $\mu=1$ and $\Delta=0.5$,
where $\mu$ is minus the argument of the second `add_onsite`, and $\Delta$ is `delta` times $|d_x+id_y|$, so
`d=[1., 1., 0.]` gives $\sqrt2$ times `delta`. The two end modes are at $\pm1.9\times10^{-5}$, and at $\pm0.011$ for
`L = 8`, while the first bulk level is at 0.83. From `L = 20` to 40 the splitting falls by about
$\sqrt{(1-\Delta)/(1+\Delta)}=0.58$ per site. With `delta=1.0` and no second `add_onsite`, which is $\Delta=t$ and
$\mu=0$, they are at zero to $10^{-15}$. With `h.add_onsite(-2.5)` and `L = 40` the chain is trivial and the lowest
level is 0.51. The same chain is `h.set_finite_system(n=L)` of the bulk Hamiltonian.

## The local density of states at the end of a Kitaev chain

```python
import numpy as np
from pyqula import geometry

L = 100  # number of sites
g = geometry.chain().get_supercell(L)  # L sites in one cell
g.dimensionality = 0  # an open chain
h = g.get_hamiltonian()  # Hamiltonian with the two spins
h.add_onsite(4.0)  # every energy goes up by 4
h.add_exchange([0., 0., 4.])  # the spin-down band at mu=0, the spin-up band far above
h.add_pairing(mode="pwave", delta=0.2, d=[1., 0., 0.])  # the Kitaev chain with Delta=0.2
energies = np.linspace(-1., 1., 201)  # energies of the LDOS, with E=0 at the index 100
ldos = []  # electron LDOS on three sites
for site in [0, L//10, L//2]:  # the end, a tenth of the way in and the middle
    P = h.get_operator("site", index=site)*h.get_operator("electron")  # electron part on this site
    (e, d) = h.get_dos(operator=P, energies=energies, delta=0.02)  # local density of states
    ldos.append(d)  # store it
```

At $E=0$ the three sites have 4.427, 0.0843 and 0.0081, so the zero mode sits at the end and decays into the chain.
The value in the middle comes from the tails of the bulk levels at $\pm0.4$, and the far spin-up band adds $10^{-4}$
to it. The weight is that of the electron components only, which is what STM measures.

## The topological transition of a Rashba superconductor

```python
import numpy as np
from pyqula import geometry

g = geometry.triangular_lattice()  # triangular lattice
Js = [0.3, 0.6]  # exchange fields, below and above the transition
gaps, cherns = [], []  # smallest energy at Gamma and Chern number
for J in Js:
    h = g.get_hamiltonian()  # Hamiltonian with the two spins
    h.add_onsite(-5.7)  # the top of the band, at Gamma, comes down to 0.3
    h.add_rashba(1.0)  # Rashba spin-orbit coupling
    h.add_zeeman([0., 0., J])  # exchange field along z
    h.add_swave(0.3)  # s-wave pairing Delta=0.3
    e = np.linalg.eigvalsh(h.get_hk_gen()([0., 0., 0.]))  # BdG levels at Gamma
    gaps.append(np.min(np.abs(e)))  # smallest energy at Gamma
    cherns.append(h.get_chern(nk=40))  # Chern number of the BdG bands below zero
```

At $\Gamma$ the spin-orbit coupling vanishes and the four levels are $\pm J\pm\sqrt{\varepsilon_\Gamma^2+\Delta^2}$
with $\varepsilon_\Gamma=0.3$, so the gap at $\Gamma$ closes at $J=\sqrt{0.3^2+0.3^2}=0.424$. `gaps` is 0.124 and
0.176, and `cherns` goes from 0 to 1. At $J=0$ the smallest energy over the zone is $|\Delta|=0.3$, on the Fermi
pocket, and not at $\Gamma$, where it is 0.424.

## The Zak phase of the Kitaev chain

```python
import numpy as np
from pyqula import geometry, topology

g = geometry.chain()  # chain with first-neighbor hopping 1
phases = []  # Zak phase of the BdG bands below zero
for mu in [1.0, 3.0]:  # inside and outside the topological range
    h = g.get_hamiltonian()  # Hamiltonian with the two spins
    h.add_onsite(4.0)  # every energy goes up by 4
    h.add_exchange([0., 0., 4.])  # the spin-down band back to 2 cos k
    h.add_onsite(-mu)  # chemical potential mu of the spin-down band
    h.add_pairing(mode="pwave", delta=0.3, d=[1., 0., 0.])  # the Kitaev chain with Delta=0.3
    phases.append(np.abs(topology.berry_phase(h, nk=200)))  # pi or 0, the sign is rounding
```

`phases` is $\pi$ for $\mu=1$, inside $|\mu|<2t$ of (5.22), and 0 for $\mu=3$. pyqula returns $+\pi$ or $-\pi$ for
the same chain, as for the SSH chain, so a page says $\pi$ modulo $2\pi$. `h.get_topological_invariant()` gives the
same number for this chain, which breaks time reversal.

## The ferromagnet against the antiferromagnet at large U

```python
from pyqula import geometry

g = geometry.bichain()  # chain with two sites per cell, at half filling
U = 20.  # strong interaction, in units of the hopping
(hf, ef) = g.get_hamiltonian().get_mean_field_hamiltonian(U=U, mf="ferro", nk=20, mix=0.9, return_total_energy=True)  # ferromagnet
(ha, ea) = g.get_hamiltonian().get_mean_field_hamiltonian(U=U, mf="antiferro", nk=20, mix=0.9, return_total_energy=True)  # Neel state
difference = ef - ea  # energy per cell of two sites
product = U*difference  # close to 4 t^2
```

A mean-field call returns a new Hamiltonian, shifted so that the Fermi level is at zero energy. `difference` is
0.1995 at $U=20t$ and 0.0999 at $U=40t$, and `product` is 3.990 and 3.998, so the difference is $J=4t^2/U$ per cell
of two sites and $J/2$ per bond, the $1/U$ law of Section 6.5. The guess `mf="ferro"` is a Zeeman field
$+0.1\,\sigma_z$, so the ferromagnet has $m=-1$. At $U=6t$, with the default `nk=8`, the same guess stops at
$|m|=1/8$, a moment of one k-point, close to the paramagnet and above the saturated ferromagnet, and the recipe "A
mean-field loop that starts from a chosen field" is the way to reach the ferromagnet there.

## A mean-field loop that starts from a chosen field

```python
from pyqula import geometry

g = geometry.bichain()  # chain with two sites per cell
h = g.get_hamiltonian()  # spinful Hamiltonian
U = 4.5  # between 4t, where the saturated ferromagnet appears, and 16t/pi
seed = h.copy()  # a copy of the Hamiltonian
seed.clean()  # remove its hoppings, so that only the field below is the guess
seed.add_zeeman([0., 0., U/2])  # the exchange field of the saturated ferromagnet
(hf, ef) = h.get_mean_field_hamiltonian(U=U, mf=seed, nk=40, mix=0.9, return_total_energy=True)  # loop from this guess
m = hf.get_vev("mz", nk=40)  # the moments, -1 on both sites
```

The loop stays at the saturated ferromagnet, $m=-1$, with the energy 0, while the paramagnet has $-0.296$ per cell and
is lower. At $U=3.9t$ the same seed goes back to the paramagnet, since the saturated state exists only from $U=4t$. A
Hamiltonian passed as `mf` is taken whole, with its hoppings, so without `seed.clean()` the first step has twice the
hopping, and at $U=4.5t$ the loop then ends close to the paramagnet, at $|m|=0.075$, a moment of three k-points. The
seed is only the starting point of the loop and not a field that stays, unlike the field of the recipe "A seed field
that stays in the Hamiltonian", so at $U=2$ with `filling=0.5` the seeds `seed.add_antiferromagnetism(0.5)` and
`seed.add_antiferromagnetism(0.2)` in place of the Zeeman field give the same antiferromagnet, with the splitting
0.681. On `square_lattice_bipartite()` the call `add_antiferromagnetism(0.3)` puts the same sign on the neighbors
at $(0.5,-0.5)$ and $(0.5,0.5)$, a stripe and not the checkerboard, so on that lattice the seed is written site by
site with `seed.add_exchange()`, and the vectors $(0,0,\pm0.3)$ alternating on the four sites give the splitting 1.20
at $U=2.5$, the gap equation of the checkerboard.

## The ferromagnet of the chain away from half filling

```python
import numpy as np
from pyqula import geometry

g = geometry.chain()  # chain with one site per cell
nk = 300  # k-points of the loop, as in the notebook
ms = []  # |n_up - n_down| for each U
for U in [1.2, 2.4, 3.]:  # interactions, in units of the hopping
    h = g.get_hamiltonian()  # spinful Hamiltonian
    hmf = h.get_mean_field_hamiltonian(U=U, filling=0.1, mf="ferro", mix=0.9, nk=nk)  # 0.2 electrons per site
    ms.append(np.mean(np.abs(hmf.get_vev("mz", nk=nk))))  # moment per site, on the mesh of the loop
(k, e, sz) = hmf.get_bands(operator="sz", nk=200)  # bands at U=3 with the spin of each state
onsite = np.real(np.diag(hmf.intra))  # onsite energies of the two spins
splitting = abs(onsite[1] - onsite[0])  # the exchange splitting
```

`filling` is the fraction of all the states with the two spins, so `filling=0.1` is $n=0.2$ electrons per site. `ms`
is 0.007 at $U=1.2t$, a moment of two k-points, and 0.200 at $2.4t$ and $3t$, the saturated value $m=n$. In the
continuum the uniform moment jumps from 0 to 0.2 at $U=1.926t$, just below the Stoner value $1/D(E_F)=1.942t$, and
between $1.8t$ and $2t$ the loop stops at moments that change with `nk`, so a page quotes the two sides of the jump. At
$U=3t$ the splitting is $Um=0.6$, `sz` is $-1$ on the filled band, since the ferro guess puts the majority on spin
down, and the filled band runs from $-0.382$ to 0. The cell of the notebook reads the moment with `get_vev("mz")` and
no `nk`, which gives 0.13 at $U=1.8t$ where the mesh of the loop gives 0.087.

## A noncollinear mean field on the triangular lattice

```python
import numpy as np
from pyqula import geometry

g = geometry.triangular_lattice().get_supercell((3, 3))  # cell of nine sites, which holds the 120 degree order
h = g.get_hamiltonian()  # spinful Hamiltonian with first-neighbor hopping 1
np.random.seed(1)  # the guess mf="XY" is random, this fixes it
hmf = h.get_mean_field_hamiltonian(U=10., mf="XY", mix=0.9, maxite=4000)  # random guess in the plane
m = np.array([np.real(hmf.get_vev(o)) for o in ("mx", "my", "mz")]).T  # moment of each site
size = np.linalg.norm(m, axis=1)  # length of each moment
a1, a2 = np.array(g.a1), np.array(g.a2)  # lattice vectors of the cell
pairs = [(i, j) for i in range(9) for j in range(9) for n1 in (-1, 0, 1) for n2 in (-1, 0, 1)
         if i < j and abs(np.linalg.norm(g.r[j] + n1*a1 + n2*a2 - g.r[i]) - 1.) < 1e-6]  # first-neighbor bonds
cosines = np.array([m[i] @ m[j]/(size[i]*size[j]) for (i, j) in pairs])  # cosine of the angle on each bond
angles = np.degrees(np.arccos(np.clip(cosines, -1., 1.)))  # angles in degrees
```

The 27 bonds of the cell have $120^\circ$ within a quarter of a degree, and every moment has the length 0.922. The
guess is random, so the common direction of the moments changes from seed to seed and only the angles are fixed. A
moment is read from its three components, since a mean-field state can turn away from the axis of its guess, as the
antiferromagnet of `square_lattice_bipartite()` does at $U=3t$. A loop that does not reach `maxerror` within `maxite`
steps raises `MeanFieldConvergenceError`, and the default `maxite=1000` is short for the random guess of the Rashba
chain of the notebook, so this recipe passes 4000. With the release 0.0.96 such a loop prints "No convergence has been
reached" and returns `None`, as the recipe "A Hartree loop on an open chain" says.

## A flat band in mean field

```python
import numpy as np
from pyqula import geometry

g = geometry.lieb_lattice()  # Lieb lattice, three sites per cell and a flat band at zero energy
h = g.get_hamiltonian()  # spinful Hamiltonian with first-neighbor hopping 1
hmf = h.get_mean_field_hamiltonian(U=1., mf="ferro", mix=0.9)  # ferro guess at half filling
m = np.real(hmf.get_vev("mz"))  # n_up - n_down on each site
total = np.sum(m)  # the moment per cell
```

`total` is $-1.000$, with the sign of the guess, also at $U=0.3t$ and $U=2t$, which is the flat band fully
polarized. The two sites with two neighbors, where the flat band lives, carry $-0.551$ each and the site with four
neighbors $+0.102$, so the state is a ferrimagnet with one unit of moment per cell. The flat band is exactly at zero
energy, so a small $U$ already polarizes it, as the Stoner criterion (6.3) says for a divergent density of states.

## Magnon energies of the Hubbard antiferromagnet

```python
import numpy as np
from pyqula import geometry

g = geometry.bichain()  # chain with two sites per cell
h = g.get_hamiltonian()  # spinful Hamiltonian
U = 20.  # strong interaction, the Heisenberg limit
hmf = h.get_mean_field_hamiltonian(U=U, mf="antiferro", nk=20)  # the Neel state
Qs = [0., 0.1, 0.25, 0.4]  # momenta in units of the reciprocal vector of the cell of two sites
spectra = [np.sort(np.real(hmf.get_magnon_energies(Q=[Q, 0., 0.], nk=20))) for Q in Qs]  # spin-flip energies at each Q
magnons = [s[0] for s in spectra]  # the lowest one, the magnon
```

`get_magnon_energies` solves the spin-flip channel of the Bethe-Salpeter equation on top of the mean-field state,
which is time-dependent Hartree-Fock, and its lowest energy is the magnon. The cell has the length 2, so the wave
vector of the chain is $k=\pi Q$, and `magnons` is 0, 0.0618, 0.1414 and 0.1902. This is $J|\sin k|$ with
$J=4t^2/U=0.2$, the linear spin-wave band (6.9) of the chain, $2JS|\sin k|$ for $S=1/2$, with the Goldstone zero at
$k=0$. The next energies, near $U$, are the charge excitations across the Mott gap.

## Magnon bands of a honeycomb ferromagnet

```python
import numpy as np
from pyqula import geometry

g = geometry.honeycomb_lattice()  # honeycomb lattice, bond length 1
h = g.get_hamiltonian(has_spin=False, tij=[-1.])  # magnon hopping -|J|S, with |J|S = 1
h.add_haldane(0.1)  # complex second-neighbor hopping, the Dzyaloshinskii-Moriya term
h.add_onsite(3.)  # the onsite energy |J|S z, so that the lower band starts at zero
(k, e) = h.get_bands(kpath=["G", "K", "M", "G"], nk=200)  # magnon bands along the path
energies = e.reshape(-1, 2)  # the two bands at each step
```

This is the linear spin-wave Hamiltonian of a honeycomb ferromagnet with $|J|S=1$, the hopping $-|J|S$, the onsite
energy $3|J|S$ and a second-neighbor hopping with the phase $\pm\pi/2$, which is the Dzyaloshinskii-Moriya term. It has
no anomalous term, so its bands are the magnon energies. They lie between 0 and 6, with the Goldstone zero at
$\Gamma$, and the gap at $K$ is 0.90, since `add_haldane(0.1)` is a second-neighbor hopping $t_2=0.0866$ with the gap
$6\sqrt3\,t_2$. A page that quotes $t_2=DS=0.1$ has the gap 1.04.

## The Chern number of a magnon band

```python
from pyqula import geometry

g = geometry.honeycomb_lattice()  # honeycomb lattice
h = g.get_hamiltonian(has_spin=False, tij=[-1.])  # magnon hopping -|J|S, with |J|S = 1
h.add_haldane(0.1)  # complex second-neighbor hopping, the Dzyaloshinskii-Moriya term
h.add_onsite(3.)  # the onsite energy |J|S z, every magnon energy is positive
chern_all = h.get_chern()  # 0, since no magnon is below zero energy
h.set_filling(0.5)  # zero energy moved into the gap, with the lower band below it
chern = h.get_chern()  # Chern number of the lower magnon band
```

`h.get_chern()` counts the states below zero energy, so it gives 0 for magnon bands that are all positive, and the
magnon cell of the notebook gives 0.0 for both signs of `add_haldane` for this reason. After `set_filling(0.5)`, zero
energy is inside the gap and `chern` is $+1$ for `add_haldane(0.1)` and $-1$ for `add_haldane(-0.1)`, with the sign of
the recipe "The Chern number". On the conventions sheet of Session 6 a Dzyaloshinskii-Moriya term $D>0$ gives the
lower band $C=-1$, so `add_haldane(0.1)` is $D<0$ there.

## The entanglement entropy of a block of free fermions

```python
import numpy as np
from pyqula import geometry

g = geometry.chain()  # chain with one site per cell and first-neighbor hopping 1
h = g.get_hamiltonian(has_spin=False)  # spinless free fermions, the levels below zero are filled
ells = [10, 20, 40]  # lengths of the block
S = [h.get_entanglement_entropy(region=list(range(l)), nsuper=1002) for l in ells]  # entropy of each block, in nats
(slope, const) = np.polyfit(np.log(ells), S, 1)  # S against ln l
```

For a chain with a period pyqula builds a ring of `nsuper` cells, and `region` lists sites of that ring, so the block
has two ends. The entropy then follows $\frac13\ln\ell+0.726$, the form (7.12) with $c=1$, and here `S[0]` is 1.4934,
as for the infinite chain, the slope is 0.333 and the constant 0.727. A half-filled ring whose number of sites is a
multiple of 4 has a level at zero energy, and the call raises `ValueError: A level sits at the Fermi energy`, so
`nsuper` is a multiple of 4 plus 2. Such a ring has an odd number of fermions, so it is exactly the XX spin ring,
whose Jordan-Wigner fermions are periodic for an odd number of fermions. Without `has_spin=False` the entropy is twice
as large, but the spinful call gave wrong values for the dimerized `bichain()` on a ring of 300 cells, so a script
keeps `has_spin=False` and doubles the entropy by hand.

## Half of an open chain of free fermions

```python
import numpy as np
from pyqula import geometry

g = geometry.chain()  # chain with one site per cell and first-neighbor hopping 1
h = g.get_hamiltonian(has_spin=False)  # spinless free fermions at half filling
Ls = [100, 200, 400, 800]  # even lengths, an odd one has a level at zero energy
S = [h.set_finite_system(n=L).get_entanglement_entropy() for L in Ls]  # entropy of the left half, in nats
slope = np.polyfit(np.log(Ls), S, 1)[0]  # growth of S per unit of ln L, about 1/6
```

`h.set_finite_system(n=L)` returns an open chain of `L` sites and leaves `h` as it is. With no `region` the entropy is
the one of the left half, a cut with one end, so it grows as $\frac16\ln L$ and not as $\frac13\ln L$. The values are
1.0492, 1.1677, 1.2848 and 1.4011, and the slope is 0.169. These lengths have an even number of sites in the half.
With an odd number, 202 and 402, the slope is 0.163, so the two parities reach $\frac16$ from the two sides, and a
page compares lengths of the same parity of $L/2$.

## The entanglement entropy of the dimerized chain of free fermions

```python
from pyqula import geometry

g = geometry.bichain()  # chain with two sites per cell
h = g.get_hamiltonian(has_spin=False)  # hopping 1 inside the cell and between the cells
h.inter = 0.6*h.inter  # hopping 0.6 between the cells, the gap is 2|1 - 0.6| = 0.8
S_weak = h.get_entanglement_entropy(region=list(range(40)), nsuper=100)  # 20 whole cells, both ends cut a bond 0.6
S_mixed = h.get_entanglement_entropy(region=list(range(41)), nsuper=100)  # one end of each kind
S_strong = h.get_entanglement_entropy(region=list(range(1, 41)), nsuper=100)  # both ends cut a bond 1
```

The sites of the ring are in the order of $x$, two per cell, so `range(40)` is 20 whole cells and its two ends cut
the bonds 0.6 of `h.inter`. The entropy is 0.4992 for this block, 0.9554 for a block with one end of each kind, and
1.4117 when both ends cut a bond 1. A block of 10 sites already has 0.4983, and longer blocks keep these values,
which is the area law of a gapped chain. A page that quotes a saturated value says which bonds the ends of the block
cut. This is the red curve of `critical_entropy` and the spinon chain of Section 8.9, and not the dimerized
Heisenberg chain, which is interacting. The bands of this chain are those of the recipe "The chain with two sites per
cell of (2.13)".

## The XX chain as free fermions

```python
import itertools
import numpy as np
from pyqula import geometry

J = 1.0  # coupling of the XX chain J sum (Sx Sx + Sy Sy)
g = geometry.chain()  # chain with one site per cell and hopping 1
hf = g.get_hamiltonian(has_spin=False).set_finite_system(n=6)  # open chain of 6 sites
hf.intra = 0.5*J*hf.intra  # hopping J/2, what the Jordan-Wigner transformation gives
eps = np.sort(hf.get_bands()[1])  # the 6 single-particle levels
levels = {N: np.sort([sum(c) for c in itertools.combinations(eps, N)]) for N in range(7)}  # levels with N fermions
ground = np.sum(eps[eps < 0])  # all the negative levels filled
```

The single-particle levels are $J\cos(\pi k/7)$ for $k=1$ to 6, and `levels[N]` are the levels of the open spin
chain with $S^z_\text{tot}=N-3$, 64 in all, as exact diagonalization of the spins gives them and as the figure
`xx_spectrum` draws them. The ground state fills the three negative levels, so it has $S^z_\text{tot}=0$ and the
energy $-1.7470J$. The Jordan-Wigner transformation gives the hopping $+J/2$, and on an open chain the sign of the
hopping does not change the levels.

## A pyqula chain solved with dmrgpy

```python
from pyqula import geometry, pyqula2dmrgpy

L = 10  # number of sites
g = geometry.chain()  # chain with one site per cell and hopping 1
hf = g.get_hamiltonian(has_spin=False).set_finite_system(n=L)  # open chain of L sites
hf.intra = 0.5*hf.intra  # hopping 1/2, the XX chain with J = 1 after the Jordan-Wigner transformation
fc = pyqula2dmrgpy.generate_fermionic_chain(hf)  # the same chain as a many-body problem in dmrgpy
wf = fc.get_gs(mode="DMRG")  # ground state as a matrix product state
S = [wf.get_bond_entropy(i, i + 1) for i in range(L - 1)]  # entropy of the first i+1 sites, in nats
S_free = [hf.get_entanglement_entropy(region=list(range(i + 1))) for i in range(L - 1)]  # from the correlation matrix
V = sum((fc.N[i] - 0.5)*(fc.N[i + 1] - 0.5) for i in range(L - 1))  # the image of the Sz Sz terms
fc.set_hamiltonian(fc.hamiltonian + V)  # the Heisenberg chain written with fermions
energy = fc.gs_energy(mode="DMRG")  # ground energy of the Heisenberg chain of 10 spins
```

This needs dmrgpy, as the notebook of the session does. `generate_fermionic_chain` takes a finite pyqula
Hamiltonian, copies its matrix elements into a dmrgpy `Fermionic_Chain`, and drops every element below $10^{-5}$. For
a Hamiltonian with a period it prints "Only implemented for 0d dimensional Hamiltonians". `S` agrees with `S_free` to
$10^{-6}$, with $\ln2$ at the first cut and 0.7578 at the center, since the XX chain is free. With the interaction
$(n_i-\frac12)(n_{i+1}-\frac12)$ added on the dmrgpy side the chain is the Heisenberg chain, and `energy` is
$-4.258035$, the energy of 10 spins, which pyqula alone cannot give.

## The spinon Fermi surface at half filling

```python
import numpy as np
from pyqula import geometry

g = geometry.triangular_lattice()  # triangular lattice, lattice constant 1
h = g.get_hamiltonian(tij=[1., 0.5])  # spinon hopping 1 to first and 0.5 to second neighbors, with the two spins
h.set_filling(0.5, nk=101)  # one fermion per site, the Fermi level is moved to zero
nk = 80  # points per side of the map
(kx, ky, w) = h.get_fermi_surface(e=0., delta=0.1, nk=nk)  # weight of the states at zero energy
fermi_map = np.array(w).reshape(nk, nk)  # the first index runs along kx
image = fermi_map.T  # rows along ky, for imshow with origin="lower"
```

`kx`, `ky` and the weight are those of the recipe "The Fermi surface", flat arrays from $-1$ to 1 in units of $2\pi$
over the lattice constant, so the square window holds $2\sqrt3=3.46$ zones, and the first index of `fermi_map` runs
along `kx`. Here the weight is summed over the two spins, so it is at most $2/\delta$, on the line of the Fermi
surface. The map of the triangular lattice is not symmetric when $k_x$ and $k_y$ are exchanged, so
`imshow(fermi_map)`, as the notebook draws it, puts $k_x$ on the vertical axis, and `image` is the map with $k_x$ to
the right. `set_filling` takes the Fermi level from the levels on an `nk` by `nk` mesh, which on this lattice holds
degenerate levels. `nk=101` gives the filling 0.500 to 0.002 for the three $t_2$ of the notebook, $-0.5$, 0 and 0.5,
while the `nk=10` of the notebook gives 0.513, 0.529 and 0.495, and `nk=60` still 0.495 for $t_2=0.5$. Meshes of 100
to 150 points per side move the filling by about 0.002, so a page that needs more takes the Fermi level from the
levels of a mesh that avoids $\Gamma$. The call writes the file `FERMI_MAP.OUT`.

## The bands of a Kondo lattice

```python
import numpy as np
from pyqula import geometry
from pyqula.specialhamiltonian import H2HFH

g = geometry.triangular_lattice()  # triangular lattice
h = g.get_hamiltonian()  # conduction electrons with hopping 1 and the two spins
h.add_onsite(-2.0)  # onsite energy of the conduction electrons, before the Kondo sites are added
h = H2HFH(h, JK=0.5)  # one Kondo site per site, coupled by the hybridization JK
(k, e, c) = h.get_bands(operator="dispersive_electrons", kpath=["G", "K", "M", "G"])  # bands and weight on c
energies = np.array(e).reshape(-1, 4)  # four bands, the two spins of c and of f
weights = np.array(c).reshape(-1, 4)  # weight of each state on the conduction electrons
```

`H2HFH` puts a Kondo site at $z=+0.5$ above every site of the lattice, while the conduction site moves to $z=-0.5$,
with a flat level at zero energy, and `JK` is the hopping between the two. It is the hybridization $\gamma_K$ of
(8.21) and not the Kondo coupling $J_K$ of (8.17), since nothing here is self-consistent. On this path the direct gap
is $2\,$`JK`, 1.0 here, and the indirect gap is 0.11, between the top of the lower band at $\Gamma$ and the bottom of
the upper band at $K$. `weights` is close to 0 on the flat part of the bands, close to 1 far from it, and one half at
the crossing. The energy zero lies inside the gap for any onsite energy, since every momentum and spin has one level
below it and one above. The constraint (8.11) is not imposed, so at that Fermi level the Kondo sites hold 0.48
fermions here, and only a band that is symmetric around zero, such as `geometry.square_lattice()` with no onsite
energy, holds one. An `add_onsite` after `H2HFH` moves the Kondo level too, which is why the onsite energy goes in
before. The call writes `BANDS.OUT`.

## A Kondo lattice with exchange between the moments

```python
import numpy as np
from pyqula import geometry
from pyqula.specialhamiltonian import H2HFH

g = geometry.triangular_lattice()  # triangular lattice
h = g.get_hamiltonian()  # conduction electrons with hopping 1 and the two spins
h.add_onsite(-4.0)  # onsite energy of the conduction electrons
h = H2HFH(h, JK=0.5, J=0.025)  # hybridization 0.5 and a hopping J between the Kondo sites
hk = h.get_hk_gen()  # Bloch Hamiltonian, the momentum in units of the reciprocal vectors
ks = np.arange(90)/90  # mesh of the zone, a multiple of 3 holds K
e = np.array([np.linalg.eigvalsh(hk([k1, k2, 0.])) for k1 in ks for k2 in ks])  # four energies per momentum
direct = np.min(e[:, 2] - e[:, 1])  # smallest gap at one momentum
indirect = e[:, 2].min() - e[:, 1].max()  # lowest upper state minus highest lower state
```

`J` is the first-neighbor hopping of the Kondo sites, which a page calls a spinon hopping and not an exchange. The
Kondo sites then have the band of the triangular lattice with the hopping $J$, of width $9J$, and `H2HFH` moves it
with `set_filling(0.5)` on its default mesh of 10, so that zero sits at its filling 0.529. The direct gap stays
$2\gamma_K=1.00$, while `indirect` is $-0.062$, so the two bands overlap and the gap at zero energy is gone. It is
0.154 at `J=0` and $-0.276$ at `J=0.05`.

## The pi-flux square lattice

```python
import numpy as np
from pyqula import geometry

g = geometry.square_lattice().get_supercell([1, 2])  # square lattice with two sites along y in the cell
h = g.get_hamiltonian(has_spin=False)  # spinless, hopping 1
h.add_orbital_magnetic_field(0.5)  # half a flux quantum per plaquette, the pi-flux state
hk = h.get_hk_gen()  # Bloch Hamiltonian, the momentum in units of the reciprocal vectors of the cell
ks = np.arange(40)/40  # mesh of the zone of the cell
gap = np.array([[np.diff(np.linalg.eigvalsh(hk([k1, k2, 0.])))[0] for k2 in ks] for k1 in ks])  # direct gap
```

Every plaquette has the flux $\Phi=-1$, and in this gauge the bands are $\pm2\sqrt{\sin^22\pi k_1+\cos^2\pi k_2}$,
from $-2\sqrt2$ to $2\sqrt2$. `gap` vanishes at two Dirac points of the zone of the cell, $(k_1,k_2)=(0,1/2)$ and
$(1/2,1/2)$, which is $(k_x,k_y)=(0,\pi/2)$ and $(\pi,\pi/2)$, and half filling puts the Fermi level there. The gauge
of the figure `spinon_bands` of Section 8.9 has the same bands moved in momentum, with the Dirac points at
$(\pi/2,\pm\pi/2)$. The cell must be doubled along $y$. With `get_supercell([2, 1])` the same call leaves every
hopping real, which is no flux, with the bands from $-4$ to 4.

## The spinon mean field of a Heisenberg chain

```python
import numpy as np
from pyqula import geometry
from pyqula.spinon import SpinonHamiltonian

g = geometry.chain()  # chain of spins one half
h = SpinonHamiltonian(g)  # Abrikosov fermions with no bare hopping, one fermion per site
hmf = h.get_mean_field_hamiltonian(J1=1.0, nk=200, decoupling="bond", integration="ed")  # the mean field of (8.14)
hops = hmf.get_multihopping().get_dict()  # hopping matrices by cell
t = [np.array(m.todense() if hasattr(m, "todense") else m) for d, m in hops.items() if tuple(d) == (1, 0, 0)][0][0, 0]
occupation = hmf.local_occupation  # fermions per site, it gives 1
h2 = SpinonHamiltonian(geometry.bichain())  # the same chain with two sites per cell
hmf2 = h2.get_mean_field_hamiltonian(J1=1.0, nk=100, decoupling="bond", integration="ed")  # free to dimerize
hk2 = hmf2.get_hk_gen()  # Bloch Hamiltonian of the cell of two sites
e2 = np.array([np.linalg.eigvalsh(hk2([k, 0., 0.])) for k in np.linspace(0., 1., 51)])  # spinon bands
```

`J1` is the first-neighbor exchange $J$ of $J\,\mathbf S_i\cdot\mathbf S_j$, and the decoupling `"bond"` keeps only
the bond channel of (8.12), so the coefficient of $f^\dagger_if_j$ is
$-(J/2)\sum_\sigma\langle f^\dagger_{j\sigma}f_{i\sigma}\rangle$, from (8.13) and (8.14). On a chain of one site per
cell this is the uniform state, with $|t|=J/\pi=0.318$ and a cosine band from $-2J/\pi$ to $2J/\pi$. The phase of `t`
comes out different in each run, since on a chain a uniform phase of the hopping is a gauge choice, so a page quotes
$|t|$. With two sites per cell the loop is free to dimerize and it does, from any random start, with the hopping $J/2$
inside the cells and 0 between them, so `e2` has two flat bands at $-0.5$ and 0.5, each with the two spins. The
default decoupling `"hartree-fock"` has a magnetic channel too, so it can leave the spin liquid for an ordered state.
The release 0.0.96 takes neither `decoupling` nor `integration` and raises a `TypeError` with them, and without them
its loop gives $|t|=0.239$ or does not converge, depending on the random start, so this recipe needs the development
tree.

## The self-consistent Kondo lattice

```python
from pyqula import geometry
from pyqula.kondolattice import KondoLatticeHamiltonian

g = geometry.chain()  # chain of conduction electrons
hc = g.get_hamiltonian(has_spin=True)  # hopping 1 and the two spins
JK = 0.6  # Kondo coupling in the convention of (8.17)
h = KondoLatticeHamiltonian(hc)  # one moment per site, written with Abrikosov fermions
hmf = h.get_mean_field_hamiltonian(J=2*JK, filling=0.5, nk=400, mf=([0.3], [0.]), T=2e-3)  # pyqula takes J = 2 J_K
gamma = abs(hmf.hybridization[0])  # the gamma_K of (8.21)
lam = hmf.constraint_lambda[0]  # energy of the f level, zero at half filling
nf = hmf.local_occupation[0]  # f fermions per site, it gives 1
h2 = KondoLatticeHamiltonian(hc)  # the same model with fewer conduction electrons
hmf2 = h2.get_mean_field_hamiltonian(J=1.5, filling=0.15, nk=150, mf=([0.3], [0.]))  # at the default T=0.02
lam2 = hmf2.constraint_lambda[0]  # the f level away from half filling
```

The coupling `J` of pyqula is the Coqblin-Schrieffer one, which enters as $(J/2)\,S_{ab}c^\dagger_bc_a$, equal to
$(J/2)\,(c^\dagger\boldsymbol\sigma c)\cdot\mathbf S$, so it is $2J_K$ in the convention of (8.17). The field
`hybridization` is $V=-(J/2)\sum_\sigma\langle c^\dagger_\sigma f_\sigma\rangle$, whose size is the $\gamma_K$ of
(8.21), 0.283 at $J_K=0.6$ and 0.527 at $J_K=0.8$, the same as the gap equation of the conventions sheet, with one
$f$ fermion per site. The guess `mf` is needed, since the loop started from $V=0$ stays there. `T` is the temperature
of the occupations, in units of the hopping. The multiplier `constraint_lambda` is the energy of the $f$ level that
keeps one $f$ fermion per site. It is zero for the half-filled chain, which is symmetric around zero, and $-1.12$ at
the filling 0.15, where the field is 0.374.

## The static Lindhard function of a chain

```python
import numpy as np
from pyqula import geometry

g = geometry.chain()  # chain with one site per cell
h = g.get_hamiltonian(has_spin=False)  # spinless and half filled at zero energy
qs = np.linspace(0.02, 0.98, 25)  # momentum transfer in units of 2 pi
chi = [h.get_chi(energies=[0.], q=[q, 0., 0.], nk=400, delta=1e-3, T=0.02)[1][0] for q in qs]  # static response
chi0 = -np.real(chi)  # the Lindhard function (9.4), positive
```

At $\omega=0$ the result of `h.get_chi` is minus the function (9.4) of the notes, per site, so it has the sign of the
change of the density by an onsite energy, $dn/dv<0$, and `chi0` is positive. `T` is the temperature in units of the
hopping. At the smallest $q$ the result is $D(E_F)=1/(2\pi)$, and the maximum is at $q=0.5$, which is $2k_F=\pi$,
where it is 0.86 at $T=0.02$. It grows as $\ln(1/T)$ with the slope $D(E_F)$ at half filling and $D(E_F)/2$ at
another filling. A spinful Hamiltonian gives the trace over the two spins, twice this.

## The dynamical response and the particle-hole continuum

```python
import numpy as np
from pyqula import geometry

g = geometry.chain()  # chain with one site per cell
h = g.get_hamiltonian(has_spin=False)  # spinless and half filled
energies = np.linspace(0.05, 4.5, 90)  # frequencies omega
qs = np.linspace(0., 1., 41)  # momentum transfer in units of 2 pi
chi = np.array([h.get_chi(energies=energies, q=[q, 0., 0.], nk=200, delta=5e-2)[1] for q in qs])  # one row per q
spectral = chi.imag  # positive inside the particle-hole continuum
```

The result is minus the complex conjugate of (9.5), with `delta` in the place of $0^+$, so its real part has the sign
of $dn/dv$ and its imaginary part is positive for $\omega>0$, as the imaginary part of (9.5) is. When `T` is not
given the temperature is `delta`. For the half-filled chain the imaginary part is large only for
$2|\sin 2\pi q|<\omega<4|\sin\pi q|$, the particle-hole continuum, so at $q=0.25$ it lives between 2 and 2.83.

## The RPA enhancement of the spin response

```python
import numpy as np
from pyqula import geometry

g = geometry.chain()  # chain with one site per cell
h = g.get_hamiltonian()  # with the two spins, half filled
hmf = h.get_mean_field_hamiltonian(U=1., nk=200, filling=0.5, mf=h.copy())  # paramagnetic mean field with U=1
q = [0.5, 0., 0.]  # q = pi, the nesting vector 2 k_F
(e, bare) = hmf.get_spinchi_ladder(energies=np.array([0.]), q=q, nk=400, imode="mesh", RPA=False, delta=1e-2)
(e, rpa) = hmf.get_spinchi_ladder(energies=np.array([0.]), q=q, nk=400, imode="mesh", RPA=True, delta=1e-2)
enhancement = np.trace(rpa[0]).real/np.trace(bare[0]).real  # it is 1/(1 - U chi_0)
```

The transverse response $\chi^{+-}$ without RPA is minus the $\chi_0$ of (9.4) per spin, 0.970 here at the
temperature `delta`, and the RPA multiplies it by $1/(1-U\chi_0)$, which is 33.7, close to the Stoner instability of
(9.8) at $q=\pi$. The interaction is read from the mean-field Hamiltonian, so the call needs `hmf` and not `h`.

## The spin response of the mean-field antiferromagnet

```python
import numpy as np
from pyqula import geometry

g = geometry.bichain()  # chain with two sites per cell
h = g.get_hamiltonian()  # the two spins
guess = h.copy()  # the starting point of the loop
guess.add_antiferromagnetism(0.5)  # a staggered exchange field
hmf = h.get_mean_field_hamiltonian(U=2.0, nk=100, mf=guess, filling=0.5)  # the antiferromagnet at U=2
energies = np.linspace(0., 4.5, 100)  # frequencies
(e, bare) = hmf.get_spinchi_ladder(energies=energies, q=[0., 0., 0.], nk=100, imode="mesh", RPA=False)
(e, rpa) = hmf.get_spinchi_ladder(energies=energies, q=[0., 0., 0.], nk=100, imode="mesh", RPA=True)
weight_bare = np.array([np.trace(c) for c in bare]).imag  # spectral weight without the interaction
weight_rpa = np.array([np.trace(c) for c in rpa]).imag  # spectral weight with the RPA
```

This is the transverse spin response $\chi^{+-}$ of the mean-field state, one matrix per frequency over the sites of
the cell, and the imaginary part of its trace is positive for $\omega>0$. Without RPA it has its largest weight at
$\omega=4.0$, at the pairs across the antiferromagnetic gap, and with the RPA the weight moves to $\omega=0.14$, the
magnon close to zero energy at $q=0$, 18 times higher. This is the second cell of "The charge-charge response function"
in the notebook.

## The density response with RPA

```python
import numpy as np
from pyqula import geometry

g = geometry.chain()  # chain with one site per cell
h = g.get_hamiltonian()  # with the two spins, half filled
(e, c) = h.get_densitychi_RPA(U=1., energies=np.array([0.]), q=[0.25, 0., 0.], nk=400, delta=1e-2)  # charge response
charge = -np.array(c).ravel()[0].real  # it is 2 chi_0/(1 + U chi_0)
```

The interaction is given in the call, so no mean field is needed. The result is $-2\chi_0/(1+U\chi_0)$ with
$\chi_0=0.198$ the function (9.4) per spin at $q=\pi/2$, so `charge` is 0.331, smaller than $2\chi_0$. This is the
screening of the density channel, and the sign of the denominator is the opposite of the spin channel of the recipe
"The RPA enhancement of the spin response".

## A magnetic impurity in a superconducting ring

```python
import numpy as np
from pyqula import geometry

N = 300  # sites of the supercell
g = geometry.chain().get_supercell(N)  # a ring of 300 sites, repeated
h = g.get_hamiltonian()  # the two spins, half filling
m = np.zeros((N, 3))  # one exchange vector per site
m[0, 2] = 1.0  # J S = 1 along z on site 0, onsite energies +1 and -1 for the two spins
h.add_exchange(m)  # the magnetic impurity
h.add_swave(0.1)  # s-wave pairing 0.1, which builds the BdG Hamiltonian
levels = np.linalg.eigvalsh(h.get_hk_gen()([0., 0., 0.]))  # the 1200 BdG levels of the ring
e_bound = np.min(np.abs(levels))  # the Yu-Shiba-Rusinov level, 0.0600
```

`add_exchange` takes one vector $(m_x,m_y,m_z)$ per site and puts $\vec m\cdot\vec\sigma$ on the site, so $m_z=JS$
gives the onsite energies $\pm JS$. `add_swave` then builds the BdG Hamiltonian in the Nambu basis (5.6), where the
exchange is the same in the electron and in the hole block. With $\nu_0=1/(2\pi t)$ per spin at half filling,
$\alpha=\pi\nu_0JS=0.5$, and (9.10) gives $0.6\Delta$, while the ring gives $0.6005\Delta$. With $JS=3$ the ring gives
$0.3837\Delta$, on the other side of zero, where (9.10) gives $-0.3846\Delta$. The formula holds to all orders in $J$
when $\Delta$ is small next to the distance from the Fermi level to the band edges. The bound state is one
quasiparticle, which the Nambu doubling shows once at $+E_b$ and once at $-E_b$. A ring of 40 sites gives $0.36\Delta$
and one of 80 sites $0.55\Delta$, so the ring must be long next to the coherence length $v_F/\Delta=20$ sites.

## An impurity in an infinite chain

```python
import numpy as np
from pyqula import geometry, embedding, potentials

g = geometry.chain()  # chain with one site per cell
h = g.get_hamiltonian(has_spin=False, tij=[1])  # band 2 cos k
h.add_onsite(1.7)  # the band moves up, the Fermi level is 0.3 above its bottom
hv = h.copy()  # the same chain with an impurity
hv.add_onsite(potentials.impurity(g.r[0], v=0.2))  # potential 0.2 on the site at the origin
eb = embedding.Embedding(h, m=hv)  # one impurity in the infinite chain
(x, y, ldos) = eb.get_ldos(nsuper=101, energy=0., delta=1e-2, nk=400)  # LDOS of 101 sites around it
```

The embedding puts one impurity in the infinite chain, with no image of it. `x` runs from $-50$ to $50$, and `ldos`
is the local density of states at the energy `energy`, the Fermi level here, with a Lorentzian of half width `delta`.
It oscillates with the period $\pi/k_F$, where $k_F$ is measured from the band bottom at $k=\pi$,
$\pi/\arccos(0.85)=5.66$ sites. The LDOS at one energy of a chain decays only through `delta`, as $e^{-2\delta x/v_F}$,
and the density, the integral up to the Fermi level, decays as $1/x$. This is the cell "Impurity in a 1d metal" of
the notebook, and pyqula writes the file `LDOS.OUT`.

## An impurity in an infinite square lattice

```python
import numpy as np
from pyqula import geometry, embedding, potentials

g = geometry.square_lattice()  # square lattice with one site per cell
h = g.get_hamiltonian(has_spin=False)  # band 2 (cos kx + cos ky)
h.add_onsite(3.0)  # the Fermi level is 1 above the band bottom at (pi, pi)
hv = h.copy()  # the same lattice with an impurity
hv.add_onsite(potentials.impurity(g.r[0], v=10.))  # potential 10 on the site at the origin
eb = embedding.Embedding(h, m=hv)  # one impurity in the infinite plane
(x, y, ldos) = eb.get_ldos(nsuper=31, energy=0., delta=1e-2, nk=100)  # LDOS on 31 x 31 sites
```

The three arrays have one entry per site of the $31\times31$ window around the impurity. Along the line $y=0$ the
maxima of `ldos` repeat every $\pi/\arccos(1/2)=3$ sites, the $\pi/k_F$ of the pocket around $(\pi,\pi)$. The call
takes a few seconds, and a larger `nsuper` or `nk` grows it fast.

## A vacancy in a Chern insulator

```python
import numpy as np
from pyqula import geometry, embedding, potentials

g = geometry.honeycomb_lattice()  # honeycomb lattice, bond length 1
h = g.get_hamiltonian(has_spin=False)  # spinless, first-neighbor hopping 1
h.add_haldane(0.2/np.sqrt(3))  # second-neighbor hopping t2 = 0.1
h.add_sublattice_imbalance(0.3)  # onsite +0.3 on site 0 and -0.3 on site 1
hv = h.copy()  # the same lattice with a vacancy
hv.add_onsite(potentials.impurity(g.r[0], v=1e3))  # site 0 pushed to 1000, which removes it
eb = embedding.Embedding(h, m=hv)  # one vacancy in the infinite lattice
energies = np.linspace(-0.2, 0.2, 41)  # energies inside the gap
(e, dos) = eb.multidos(es=energies, delta=0.004, nk=40)  # DOS of the cell with the vacancy
e_bound = e[np.argmax(dos)]  # the energy of the bound state, -0.14
```

`add_haldane(x)` is a second-neighbor hopping $(\sqrt3/2)x$, as on the sheet of Session 3, so this is $t_2=0.1$, with
the gap edges at $\pm(3\sqrt3t_2-M)=\pm0.22$. The vacancy on the site with $+M$ binds a state at $-0.14$, and the one
on the site with $-M$ a state at $+0.13$, on this grid of 0.01. The zero of the local Green's function of the
infinite lattice puts them at $\mp0.135$, so a grid finer than 0.01 is needed for a third digit. A large onsite
energy removes the site from the energies that matter, and the embedding puts one vacancy in the infinite lattice, so
the bound state has no image. This takes about two seconds.

## A vacancy in a chiral p-wave superconductor

```python
import numpy as np
from pyqula import geometry, embedding, potentials

g = geometry.triangular_lattice().get_supercell((2, 2))  # a cell of four sites
h = g.get_hamiltonian()  # with the two spins
h.add_onsite(-4.0)  # the Fermi level is 2 below the band top at Gamma
h.add_pairing(mode="chiral_pwave", delta=0.1)  # spin-triplet chiral p-wave pairing
gap = h.get_gap()/2.  # the gap edge
hv = h.copy()  # the same crystal with a vacancy
hv.add_onsite(potentials.impurity(g.r[0], v=100.))  # a very strong potential removes the site
energies = gap*np.linspace(-0.9, 0.9, 19)  # energies inside the gap
(e, dos) = embedding.Embedding(h, m=hv).multidos(es=energies, delta=gap/60, nk=40)  # DOS around the vacancy
(e, clean) = embedding.Embedding(h, m=h).multidos(es=energies, delta=gap/60, nk=40)  # the same without it
```

`gap` is 0.30 here, three times the argument `delta`, since the p-wave gap edge is not `delta`. The vacancy gives two
sharp peaks at $\pm0.7$ of the gap on this grid, where `dos` is about 190 times `clean`. The zeros of the local Green's
function of the removed site put the two levels at $\pm0.714$ of the gap, each twice, so they are not at zero energy.
With `mode="swave"` the gap is 0.10 and there is no peak inside it. The two calls take about a second each, and
`h.get_chern()` of the spinful chiral p-wave without the supercell is $-2$.

## The tails of the eigenstates of a finite chain

```python
import numpy as np
from pyqula import geometry

g = geometry.chain(400)  # a cell of 400 sites
g.dimensionality = 0  # a finite chain with two ends
h = g.get_hamiltonian(has_spin=False)  # spinless, first-neighbor hopping 1
h.add_onsite(3.0*np.cos(np.sqrt(2)*np.pi*g.r[:, 0]))  # quasiperiodic potential of strength 3
(energies, rates) = h.get_tails()  # one decay rate per eigenstate
xi = 2/np.mean(rates)  # mean localization length of the amplitude, |psi| ~ exp(-x/xi)

hr = g.get_hamiltonian(has_spin=False)  # the same chain
rng = np.random.default_rng(1)  # random numbers with a fixed seed
hr.add_onsite(2.0*rng.random(len(g.r)) - 1.0)  # onsite energies uniform in [-W, W] with W = 1
(energies_r, rates_r) = hr.get_tails()  # one value per eigenstate
center = np.abs(energies_r) < 0.3  # the states close to the band center
xi_r = 2/np.mean(rates_r[center])  # the localization length of the amplitude there
xi_all = 2/np.mean(rates_r)  # the same from all the states
```

`h.get_tails()` needs a finite system, and it fits $\ln|\psi_n|^2$ around the largest weight of each eigenstate and
returns minus the slope, so a state with $|\psi_n|\propto e^{-|n|/\xi}$ gives $2/\xi$. The axis $1/\lambda$ of the
notebook is then for $|\psi|^2$ and not for $|\psi|$. For the quasiperiodic chain the mean rate is 0.76, near the exact
$2\ln(V_0/2t)=0.81$ of the Aubry-André model. The notebook takes `v*(np.random.random()-0.5)`, which is uniform in
$[-v/2,v/2]$, so its `v` is $2W$ for the $w_n\in[-W,W]$ of Section 9.10b. For this seed `xi_r` is 23 sites, and the
seeds 2 and 3 give 20 and 28, near the $\xi\approx26\,(t/W)^2$ of the transfer matrix at $E=0$ on the conventions
sheet of Session 9. The mean over all the states,
`xi_all`, is 7.5, since the states at the band edges are much more localized, so a number that a page quotes says at
which energy it is taken, and a quantity of one realization is quoted as a range over several seeds.

## A disordered ring

```python
import numpy as np
from pyqula import geometry, algebra

g = geometry.chain()  # chain with one site per cell
h = g.get_hamiltonian(has_spin=False, tij=[-1., -0.3])  # first and second neighbors, matrix elements -1 and -0.3
h = h.set_finite_system(n=200, periodic=True)  # ring of 200 sites
rng = np.random.default_rng(1)  # the disorder is random
h.add_onsite(rng.uniform(-1., 1., 200))  # onsite energy of each site, uniform in [-W, W] with W=1
levels = np.linalg.eigvalsh(algebra.todense(h.intra).real)  # the 200 levels
bins = np.linspace(-3.5, 3.5, 41)  # 40 bins of energy
observable = np.histogram(levels, bins=bins)[0]/200  # the observable O of Section 10.7
```

`set_finite_system(n=200, periodic=True)` closes the chain into a ring, so the first and the last site are
neighbors, and `add_onsite` with an array of one value per site adds these onsite energies in the order of the
sites. The matrix is the one of the figure `ham_learning`, to $10^{-14}$. `get_supercell(200)` in place of
`set_finite_system` gives the same matrix as its Bloch Hamiltonian at $k=0$, `h.get_hk_gen()([0., 0., 0.])`, which is
a sparse matrix. `observable` is the fraction of the levels in each bin, and here it sums to 1, since no level falls
outside $[-3.5,3.5]$.

## Learning the second-neighbor hopping from the density of states

```python
import os
os.environ["OMP_NUM_THREADS"] = "1"  # small matrices, threads only cost time
import numpy as np
from pyqula import geometry, algebra

g = geometry.chain()  # chain with one site per cell
h1 = g.get_hamiltonian(has_spin=False, tij=[-1.]).set_finite_system(n=200, periodic=True)  # ring, first neighbors
h2 = g.get_hamiltonian(has_spin=False, tij=[0., -1.]).set_finite_system(n=200, periodic=True)  # second neighbors
H1, H2 = algebra.todense(h1.intra).real, algebra.todense(h2.intra).real  # the two matrices, real
bins = np.linspace(-3.5, 3.5, 41)  # 40 bins of energy
rng = np.random.default_rng(3)  # the seed of the figure ham_learning
data = []  # the test set and the two training sets
for (n, wmax) in ((200, 1.5), (600, 0.0), (600, 1.5)):
    t2 = rng.uniform(0., 0.4, n)  # the parameter that we want
    W = rng.uniform(0., wmax, n)  # the strength of the hidden disorder
    O = np.array([np.histogram(np.linalg.eigvalsh(H1 + a*H2 + np.diag(rng.uniform(-b, b, 200))), bins=bins)[0]/200
                  for (a, b) in zip(t2, W)])  # the density of states of each ring
    data.append((O, t2, W))
(Otest, t2test, Wtest) = data[0]
rms = []  # error of the prediction on the test set, trained on clean rings and with disorder
for (O, t2, W) in data[1:]:
    X = np.hstack([O, np.ones((len(O), 1))])  # the 40 numbers of O and a constant
    theta = np.linalg.lstsq(X, t2, rcond=None)[0]  # the linear network of (10.12), fitted by least squares
    prediction = np.hstack([Otest, np.ones((len(Otest), 1))]) @ theta
    rms.append(np.sqrt(np.mean((prediction - t2test)**2)))
```

This is the toy of the figure `ham_learning` with the matrices of pyqula, and with the seed 3 it gives the errors of
the script, 0.0635 trained on clean rings and 0.0043 trained with disorder. These come from one seed, and the seeds 0
to 9 give 0.058 to 0.074 and 0.0040 to 0.0054, so a page gives the range. The bins sum to 1 next to the constant, and
a clean ring leaves bins empty, so the fits have the rank 27 and 38 of 41 and `lstsq` takes the solution of smallest
norm, which the errors above depend on. The line with `OMP_NUM_THREADS` must come before numpy is imported. The 1400
rings take about 6 seconds.

## A Hartree loop on an open chain

```python
import numpy as np
from pyqula import geometry, algebra

g = geometry.chain()  # chain with one site per cell
h = g.get_hamiltonian(tij=[-1.]).set_finite_system(n=60)  # open chain of 60 sites, with the two spins
x = np.arange(60)  # site index, the sites of h are in the order of their position
h.add_onsite(-2.*np.exp(-((x - 29.5)/7.)**2))  # the well v_ext(i) of the figure ks_loop
mf = h.get_mean_field_hamiltonian(U=4., filling=40/120, mix=0.3, maxerror=1e-8,
                                  constrains=["no_magnetism"])  # Hubbard U=4, 40 electrons, the two spins equal
(e, w) = np.linalg.eigh(algebra.todense(mf.intra))  # the orbitals of the converged Hamiltonian
occupied = np.sum(np.abs(w[:, :40])**2, axis=1)  # weight of the 40 filled states on each spin orbital
density = occupied[0::2] + occupied[1::2]  # electrons per site, the two spins together
```

`filling` is the fraction of the 120 spin orbitals that are filled, so 40 electrons on 60 sites is 40/120, and the
orbitals $2i$ and $2i+1$ are the spin up and the spin down of the site $i$. `mix` is the weight of the new mean field
at each step, the 30 percent of the toy. With equal spins each spin feels $U\langle n_{-\sigma}\rangle=Un/2$, so the
Hubbard `U=4` of pyqula is the term $U\,n(i)$ of the toy with $U=2$, and `density` is the one of the figure to
$2\cdot10^{-11}$, 0.9895 at the center against 1.2143 with no interaction. The constraint keeps the two spins equal
at every step. The guess `mf="potential"` in its place starts with equal spins and gives the same density, but a
moment of $5\cdot10^{-7}$ appears in it, since the state with equal spins is unstable. With neither of
the two, the random first guess with `np.random.seed(0)` just before the call ends at a magnetic state, with the
total energy $-61.79$ below the $-58.01$ of equal spins and a local moment of 0.77 along an axis of its own, which is
not the toy. The seed goes after the chain is built, since building it draws random numbers. A loop
that does not converge in `maxite` iterations, 1000 by default, raises `MeanFieldConvergenceError` in the
development tree, while the release 0.0.96 prints "No convergence has been reached" and returns `None`.

## Monte Carlo of the Ising model

```python
import numpy as np
from pyqula import geometry
from pyqula.latticeising import LatticeIsing

g = geometry.square_lattice().get_supercell(16)  # square lattice of 16 x 16 sites, periodic
model = LatticeIsing(g, m=1.)  # classical spins +1 and -1 on the sites, all up
model.add_interaction(Jij=[0.5])  # first neighbors, the J=1 of (10.9), since pyqula counts every bond twice
energy_all_up = model.get_energy()  # -2 J N for all spins up, so -512
np.random.seed(1)  # the Metropolis updates are random, and this fixes them
(es, ms) = model.optimize_energy(temp=1.5, ntries=256*1000)  # 1000 sweeps of single flips at T=1.5 J
absm = np.abs(ms[256*300::256])/256  # |m| once per sweep, after 300 sweeps
snapshot = model.s.reshape(16, 16)  # the last configuration, the first index runs along x
```

pyqula writes the energy as $-\sum J\,s_is_j$ over a list that holds every bond in both directions, so `Jij=[0.5]`
is the $J=1$ of (10.9). All spins up then have the energy $-2N=-512$, one flipped spin costs 8, and $T_c$ is 2.269,
while `Jij=[1.]` doubles every energy and moves $T_c$ to 4.54. `optimize_energy` makes `ntries` attempted single
flips of Metropolis at the temperature `temp`, and returns the energy and the sum of the spins after each of them, so
a sweep is 256 entries. The mean of `absm` is 0.987 at $T=1.5$, where the exact $|m|$ of the infinite lattice is
0.9865, and about 0.13 at $T=3.5$, where a long run gives 0.124. `LatticeIsing(g)` with no `m` starts from a random
configuration with half of the spins up, so $m=0$. The sites of `g.r` run along $y$ first, so `snapshot[i, j]` is the
spin at $x=i-7.5$ and $y=j-7.5$, the kind of array that the classifier of Section 10.6 takes as its input.
`model.add_tensor` with a function of four positions raises a `TypeError`, since it calls the function with the two
positions of a pair, so the four-spin term of the gauge theory of Section 10.6b has no recipe.
