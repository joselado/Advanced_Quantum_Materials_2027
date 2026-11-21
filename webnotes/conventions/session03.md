# Conventions of Session 3, checked by number

This sheet fixes the signs and the units that the pages, the figures and the pyqula scripts of Session 3 use. An
agent that edits the session reads it first and does not work these out again. Every line was checked with a
number on 2026-11-21, by at least two independent calculations, and the line says what was computed. A statement
that is not on this sheet is checked before a page claims it.

## Berry curvature, Chern number and Hall conductivity

- The Berry curvature of the notes is $\Omega_n=-2\,\mathrm{Im}\langle\partial_{k_x}u_n|\partial_{k_y}u_n\rangle$. It
  is the curl of $A=i\langle u|\partial_k u\rangle$, the form of (3.6) and of Section 4.3.
- A form that needs no phase of the eigenvectors is
  $\Omega_n = i\sum_{m\neq n}\big[\langle n|\partial_xH|m\rangle\langle m|\partial_yH|n\rangle-(x\leftrightarrow y)\big]/(\varepsilon_n-\varepsilon_m)^2$.
  It agrees with the definition at single points to six digits, on two-band and four-band models.
- The Chern number is $C=\sum_{n\ \text{filled}}\frac{1}{2\pi}\int\Omega_n\,d^2k$, on a right-handed grid of $k$.
- The usual link-variable plaquette phase, taken counterclockwise, is minus this $\Omega$ times the area of the
  plaquette. A script that sums the plaquette phases with no sign change gives $-C$.
- For a voltage along $y$ and a current along $x$, with this $\Omega$, the result is $\sigma_{xy}=-(e^2/h)\,C$.
  Three routes agree: the time evolution with a slowly moving $k_y$, a strip with a potential, and the Hofstadter
  band against the classical drift. The printed (3.4), $\sigma_{xy}=+(e^2/h)\,C$, is the same result with $x$ and
  $y$ exchanged. The sign does not depend on the charge, which enters as $q^2$, or on the direction called
  positive, since a mirror changes $\sigma_{xy}$ and $C$ together. It depends only on the order of $x$ and $y$ and
  on the sign chosen for $\Omega$. The lecturer decided on 2026-11-21 to keep (3.4) as printed, with the plus
  sign, and to say once, in the folds of Sections 3.4 and 3.5, that it is the current along $y$ for a voltage
  along $x$. Sessions 4, 5 and 6 inherit this, so (4.1) stays as it is.
- A page writes $\sigma_{xy}=(e^2/h)\,C$ as (3.4) does, and otherwise claims the integer and relative signs,
  such as that $\sigma_{xy}$ changes sign with the Haldane coupling. It does not derive an absolute direction
  of the current from the sign of $C$.

## pyqula

- `geometry.honeycomb_lattice()` has $a_1=(3/2,\sqrt3/2)$ and $a_2=(-3/2,\sqrt3/2)$, so the bond length is 1 and
  the lattice constant is $\sqrt3$. The default first-neighbor hopping is $+1$, and `tij=[-1.]` gives $-t$.
- `g.get_hamiltonian(has_spin=False)` is the spinless Hamiltonian. The default is spinful, so `h.get_chern()` of
  the notebook gives 2 where the spinless one gives 1.
- `h.add_haldane(x)` is a second-neighbor hopping $t_2=(\sqrt3/2)\,x$. It gives a Haldane mass $4.5x$ and a gap
  $9x$, so 0.90 for `add_haldane(0.1)`. The numpy model `_honeycomb.bloch` with $t_2=0.1$ has the mass
  $3\sqrt3 t_2=0.52$ and the gap 1.04. A page says which of the two it quotes.
- `h.add_sublattice_imbalance(m)` gives the onsite energies $\pm m$ and a gap $2m$. With `add_haldane(0.1)` the gap
  closes at $m=0.45$ and $C$ goes from 1 to 0.
- `h.get_chern()` has the sign of the $C$ above. It is $+1$ for `add_haldane(0.1)`, checked with the form of
  $\Omega$ that needs no phase on `h.get_hk_gen()`.
- `(kx, ky, b) = h.get_berry_curvature(nk=N)` returns a rectangular window around $\Gamma$ that is a period of the
  map, two zones for the honeycomb lattice. `kx` and `ky` are in units of $2\pi$ over the lattice constant, and the
  first index runs along `kx`. `b` is the curvature per unit area of the reduced zone, so `np.mean(b)/(2*np.pi)`
  is the Chern number, with the same sign. `style.pyqula_kmap` draws it with true momenta.
- `h.get_anomalous_hall_conductivity(fermi=mu, T=T, nk=N)` is
  $(1/2\pi)\sum_n\int f(\varepsilon_n-\mu)\,\Omega_n$ in units of $e^2/h$. In a gap it equals `h.get_chern()`.
- `h.get_gap()` returned about $10^{-17}$ for a spin-orbit coupling 0.1 with a Rashba coupling 0.15, where a
  k-mesh gives 0.44 (0.441 between the lowest empty and the highest filled state, 0.448 as the smallest gap at one
  $k$). A gap that a page quotes is taken from a k-mesh that holds the points where the gap is smallest.
- The field argument of a ribbon is the flux per plaquette in flux quanta, checked against the Harper chain.
- The SSH chain is `geometry.bichain()` with `h.intra = t*h.intra` or `h.inter`, and the open chain is
  `h.set_finite_system(n=N)`. pyqula gives the Zak phase as $+\pi$ or as $-\pi$, depending on rounding at the
  branch cut (12 and 8 of 20 runs), so a page says $\pi$ modulo $2\pi$.

## The numpy helpers of `webnotes/figures/session03/`

- `_honeycomb.bloch(k, t2=0.1)` has $C=+1$ of the lower band with the $\Omega$ above.
- `_honeycomb.chern` and the script `berry_haldane.py` before 2026-11-21 sum the plaquette phases with no sign
  change, so they return $-C$. `haldane_phase.py` prints $+1$ for the same reason. Their pictures are right, since
  the captions quote $|C|$.
- `_honeycomb.hops` and `_honeycomb.flake` put the Haldane phase on opposite turns. The bulk Hamiltonian built
  from `flake(t2=0.1)` is `bloch(t2=0.1, phi=-pi/2)`, with $C=-1$ where `bloch(t2=0.1)` has $+1$. The figure
  `haldane_flake` shows only the spectrum and the weight, so it is right, but a picture of an edge current drawn
  from `flake` would run against the one from `bloch`.
- The shared module `figures/physcheck.py` has these conventions built in, and `checks/session03/conventions.py`
  asserts the lines of this sheet. An author imports the module and does not write this code again.

## Open points of the old text, left as they are

- Section 3.9c says that the gap closing "requires $t=1$ and $k=\pi$", which holds for $t>0$.
- Section 3.10 says that a real lattice always has an even number of Dirac points, while its quiz uses a lattice
  model with a single gapped cone.
- Section 4.10 says that the graphene levels are two orders of magnitude above those of GaAs, and Section 4.1
  says about seven times at 10 T.
