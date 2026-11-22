# Conventions of Session 4, checked by number

This sheet fixes the signs, the units and the pyqula facts that the pages, the figures and the pyqula scripts of
Session 4 use. An agent that edits the session reads it first, together with the sheet of Session 3, and does not
work these out again. Two drafts were written apart on 2026-11-21, and a third calculation settled each line where
they differed or where only one of them had it. Every line was checked with a number, and the line says what was
computed. The check is `webnotes/checks/session04/conventions.py`, which prints one line per bullet below, in the same
order, in about two minutes. A statement that is not on this sheet is checked before a page claims it.

## From Session 3

- The Berry curvature, the Chern number and the Hall conductivity are the lines of
  `webnotes/conventions/session03.md`, taken as they are. With
  $\Omega_n=-2\,\mathrm{Im}\langle\partial_{k_x}u_n|\partial_{k_y}u_n\rangle$, (3.4) and (4.1) write
  $\sigma_{xy}=(e^2/h)\,C$, which is the current along $y$ for a voltage along $x$, and the current along $x$ for a
  voltage along $y$ is $-(e^2/h)\,C$. The lecturer kept this sign on 2026-11-21, so (4.1) stays as it is. The check
  repeats only the anchor, `h.get_chern()` is $+1$ for `add_haldane(0.1)` and the form with no phase gives $+1.0000$.
- The Haldane model of Section 4.19 is the one of Session 3, with its pyqula lines as they are. `add_haldane(x)` has
  the gap $9x$, 0.90 for $x=0.1$ and 0.63 for $x=0.07$, and $C=+1$ for $x>0$, while the numpy model
  `_honeycomb.bloch(t2=0.1)` has the gap 1.04. A page says which of the two it quotes.

## Units and scales

- The pages set $e=1$ and keep $\hbar$, as Sections 4.7 and 4.9 say, so $\omega_c=B/m$ and $\ell_B=\sqrt{\hbar/B}$,
  and the phase of (4.4) is $(1/\hbar)\int\mathbf A\cdot d\boldsymbol\ell$, as the key box of Section 4.7 says since
  2026-11-22, where (4.4) is printed with $\hbar=1$. With the units back, $\ell_B=\sqrt{\hbar/eB}$ is 25.66 nm at 1 T and 12.83 nm at 4 T, so it goes as
  $1/\sqrt B$, and $2\pi\ell_B^2B$ is the flux quantum $h/e$, so the phase $(e/\hbar)Ba^2$ of a plaquette of side $a$
  is $2\pi$ times its flux in flux quanta.
- A Landau level holds one state per flux quantum, $eB/h=1/2\pi\ell_B^2$ per unit area, which is 241.8 per square
  micrometre at 1 T. So a sample of $1\,\mu\mathrm m^2$ holds 242 states at 1 T and 484 at 2 T, the numbers of the
  quiz of Section 4.9. A $24\times24$ torus of the square lattice with the flux 1/12 per plaquette has exactly 48
  states in its lowest level, flat to $10^{-5}$, with a gap 0.92 above them.
- GaAs, with $m=0.067\,m_e$, has $\hbar\omega_c=\hbar eB/m=1.73$ meV at 1 T, 6.91 meV at 4 T and 17.3 meV at 10 T,
  and 1.73 meV is the thermal energy of 20 K. The lattice form $4\pi\phi\,t$ of the square lattice, with
  $t=\hbar^2/2ma^2$ and $\phi=eBa^2/h$, gives the same for any lattice constant $a$.
- Graphene, with $v=10^6$ m/s, has $E_1=v\sqrt{2\hbar eB}=36.3$ meV at 1 T, 72.6 meV at 4 T, 108.8 meV at 9 T and
  114.7 meV at 10 T, the numbers of the quizzes of Sections 4.1 and 4.10. The lattice form
  $E_1=\tfrac32\sqrt{4\pi\phi}\,t$ of the honeycomb lattice, with the bond 0.142 nm and $t=2\hbar v/3a$, gives the
  same.
- The first level of graphene over the spacing of GaAs goes as $1/\sqrt B$. It is 21 at 1 T and 6.6 at 10 T, and it
  is 100 only at 0.044 T, a field where no plateau is seen.
- $h/e^2=25812.807\,\Omega$, so the plateaus with $N=2$ and $N=4$ are at 12.906 k$\Omega$ and 6.453 k$\Omega$.

## The charge, the field and the sign of $C$

- The pages take the charge $+e$, with $\boldsymbol\pi=\mathbf p-e\mathbf A$ of (4.3) and the phase of (4.4). For
  $\mathbf B=B\hat z$, the field of Section 4.8, this gives $[\pi_x,\pi_y]=+i\hbar eB=i\hbar^2/\ell_B^2$ in the Landau
  and in the symmetric gauge, checked with sympy, and the amplitudes of (4.4) around a plaquette, taken
  counterclockwise, have the phase $+2\pi$ times the flux in flux quanta.
- In the symmetric gauge $\pi_x+i\pi_y=-2i\hbar\,(\partial_{\bar z}+z/4\ell_B^2)$ for the charge $+e$, so
  $z^me^{-|z|^2/4\ell_B^2}$ is in the lowest level, with the energy $\hbar\omega_c/2$ and $L_z=+m\hbar$, while
  $\bar z^me^{-|z|^2/4\ell_B^2}$ has $(m+\tfrac12)\hbar\omega_c$. For the charge $-e$ the two exchange, and the lowest
  level is $\bar z^m$ with $L_z=-m\hbar$. So (4.9) to (4.14) hold as printed for $qB>0$. This was checked with sympy
  for $m=0$, 1 and 3.
- For $qB>0$ the Dirac Hamiltonian of Section 4.10 is $(\sqrt2\hbar v/\ell_B)\begin{pmatrix}0&a^\dagger\\a&0\end{pmatrix}$,
  its levels are $\sqrt{2|n|}\,\hbar v/\ell_B$ and its zero mode lives in the upper component, as `dirac_levels.py`
  draws. For $qB<0$ the zero mode lives in the lower component. This was checked by diagonalizing
  $v(\pi_x\sigma_x+\pi_y\sigma_y)$ with $x$ and $p_x$ written in a basis of 100 oscillator states, which does not use
  the ladder operators of the page.
- A particle of either charge drifts with $\mathbf v=\mathbf E\times\mathbf B/B^2$. For $qB>0$ its cyclotron orbit
  turns clockwise seen from $+z$, and its edge channels go around the sample counterclockwise. In the Landau gauge the guiding center is
  $x_0=\hbar k_y/eB$, and the right wall has $v_y>0$, as the caption of Figure 4.1 says. In the continuum ribbon of
  $12\,\ell_B$ the lowest state of $k_y\ell_B=-2$, 0 and 2 sits at $x=-2$, 0 and $2\,\ell_B$, the branch at the right
  wall has a positive slope, and a field $E_x$ gives every bulk state of the two lowest levels
  $dE/dk_y=-eE_x\ell_B^2$, so $v_y=-E_x/B$. In an island of $14\times14$ sites with the flux 1/16 a state of the first
  gap carries the current $-0.196$ along $x$ in its upper half and $+0.196$ in its lower half.
- For $qB>0$ every Landau level has $C=-1$ with the $\Omega$ of Session 3, and $C=+1$ for $qB<0$. The link variables
  of a magnetic cell with the flux 1/12 and the phase of (4.4) give $-1$ for each of the three lowest levels, and the
  form with no phase gives $-0.9998$. The drift gives a filled level of density $eB/h$ the current
  $j_y=-(e^2/h)E_x$, so $j_x=+(e^2/h)E_y$, which is the $-(e^2/h)\,C$ of Session 3 with $C=-1$. So (3.4), read as the
  lecturer kept it, gives $\sigma_{xy}=-N\,e^2/h$ for $N$ filled levels, and the current along $x$ for a voltage along
  $y$ is $+N\,e^2/h$. $C=+1$ per level is the case of an electron in the field $+B\hat z$, or of the charge $+e$ in
  $-B\hat z$, and it is the sign that pyqula gives.
- The levels at the top of the band of the square lattice are hole levels, and each of them has the same Chern number
  as a level at the bottom. With pyqula and the flux 1/9 the lowest and the highest of the nine bands both have
  $C=+1$, and the eight bands below the top have $-1$ together, which is the plateau with one empty hole level.

## pyqula and the magnetic field

- `h.add_orbital_magnetic_field(phi)` multiplies every matrix element $\langle i|H|j\rangle$, also those to the next
  cells, by $\exp[i2\pi\phi\,(x_i-x_j)(y_i+y_j)/2]$, which is a Landau gauge with $\mathbf A$ along $x$, the direction
  of a ribbon. A counterclockwise plaquette then has the phase $-2\pi\phi$, with either sign of the hopping. So `phi`
  is the field along $+z$ for an electron, and the field along $-z$ for the charge $+e$ of the pages.
- `phi` is the flux per unit area of the geometry in units of $h/e$, so $\ell_B=1/\sqrt{2\pi\phi}$ in the units of the
  geometry. On the square lattice it is the flux per plaquette, which is the line of the sheet of Session 3, checked
  there on the Harper chain of the square lattice. On the honeycomb lattice of pyqula, with the bond 1, a
  hexagon holds $\tfrac{3\sqrt3}{2}\phi=2.60\,\phi$, so the values `B = 0.005, 0.01, 0.02` of the honeycomb cells of
  the notebook are a flux per unit area and not per plaquette, and $\ell_B$ is 4.0 bond lengths for 0.01.
- With `phi > 0` every Landau level at the bottom of the square lattice has $C=+1$. `h.get_chern()` counts the states
  below zero energy, and `add_onsite(c)` adds $c$ to every onsite energy, so it sets the Fermi energy. With the flux
  1/15, `h.get_chern()` gives $+1$ and $+2$ with the zero of energy in the first and in the second gap, and
  `h.get_anomalous_hall_conductivity` gives 0, 1 and 2 below the lowest level and in the two gaps.
- The ribbons of pyqula are periodic along $x$ and finite along $y$, while the ribbons of the pages are finite along
  $x$ and periodic along $y$. The $x$ of a page is minus the $y$ of pyqula and its $y$ is the $x$ of pyqula, which is a
  rotation, so the field keeps its sign. On the square ribbon of 40 the guiding center moves as $dy_0/dk=1/\phi$, 50.0
  for 0.02 with $k$ in units of $2\pi$, with the hopping $+1$ and with $-1$. So with `phi > 0` the branch with a
  positive slope sits at the edge of positive $y$, as the recipe "A ribbon in a magnetic field" says, which is the
  clockwise sense of $qB<0$. The zigzag ribbon of 20 with `add_haldane(0.1)`, which also has $C=+1$, has the positive
  slope at the edge of positive $y$ too, at $k$ from 0.45 to 0.55. The numpy ribbon `_haldane.ribbon` of Session 6 takes
  minus the momentum, so there the positive slope of $C=+1$ is at the lower edge, as the sheet of Session 6 says.
- `gauge="symmetric"` is for islands. On an island it gives the levels of the Landau gauge to $10^{-12}$, while on a
  ribbon it is another field, and on the square ribbon of 20 it gives the levels of the Landau gauge with half the
  field. A ribbon or a two-dimensional cell keeps the default gauge.
- A two-dimensional cell with a field needs a whole number of flux quanta through the cell. The square supercell
  `(1, q)` takes the field `p/q`, and with 0.013 in the supercell `(1, 10)` one plaquette of each cell carries
  $-0.117$ in place of $0.013$, with no warning. A whole number is not enough, since $\mathbf A$ is along $x$ and
  changes only along $y$. The supercell `(2, 1)` with 0.5 holds one flux quantum and leaves every hopping real, with the
  bands from $-4$ to 4 of no field, as the sheet of Session 8 says, while `(1, 2)` has the bands of the $\pi$ flux,
  from $-2\sqrt2$ to $2\sqrt2$. For the honeycomb lattice the cell
  `honeycomb_lattice_square_cell().rotate(90).get_supercell((n, 1))` keeps every hexagon at the flux $\phi$ with any
  whole number $F$ of flux quanta, $\phi=F/(3\sqrt3\,n)$, while `honeycomb_lattice_square_cell().get_supercell((1, n))`
  needs an even $F$. This was checked by the loop phase of every hexagon of the cell, with $F=1$ and $1/2$ in the first
  cell and $F=2$ and 1 in the second.
- `h.get_dos(energies=..., delta=..., nk=...)` is the number of states per unit of energy and per unit cell, with
  Lorentzians of half width `delta`. On the square ribbon of 20 with the field 0.02, with `delta=1e-2` and `nk=400` as
  in the notebook, its integral is 19.96, the 20 sites less the tails, for the spinless Hamiltonian of the notebook.
  The spinful default counts both spins, as on the sheets of Sessions 1, 2 and 6, and gives 39.92. With
  `operator="bulk"`, which keeps the middle 80 percent of the width, the spinless integral is 15.97, and its peaks
  $-3.875$, $-3.630$ and $-3.395$ are the levels $-3.876$, $-3.633$ and $-3.397$ of the lattice.
- `h.get_ldos(e=..., nrep=..., delta=..., nk=...)` of a ribbon returns `nrep` cells, 1600 points for 20 cells of the
  armchair ribbon of 20, and the sum over one cell is the density of states at `e`. In the notebook cell
  "Localization of the edge states in the quantum Hall effect in a ribbon", with the field 0.01, the 25 percent of the
  sites within $\ell_B=4$ of an edge hold 57 and 54 percent of the weight at $E=0.177$ and $0.353$, in the gap above
  the zero level, and 4 and 16 percent at $E=0$ and $0.53$, on the zero level and on the first level, as the try-it
  box of Section 4.5 says.
- The default hopping $+1$ of `square_lattice()` puts the band bottom $-4$ at $M=(\pi,\pi)$ and the top at $\Gamma$, as
  the sheet of Session 2 says, while the notebook cell "The dispersion of the square lattice" expands around $\Gamma$.
  The Landau levels are the same with `tij=[-1.]`. The cells "Landau levels of conventional electrons" and "Bands in
  the Dirac quantum Hall state" use the spinful default, which has every level twice.

## The lattice against the continuum

- The square lattice with the hopping $t$ and the flux $\phi$ per plaquette has $\hbar\omega_c=4\pi\phi\,t$, and to
  second order $E_n=-4t+4\pi\phi\,t\,(n+\tfrac12)-(\pi\phi)^2t\,(2n^2+2n+1)/2$, which holds to $2\cdot10^{-3}$,
  $5\cdot10^{-4}$ and $10^{-4}$ for $\phi=1/40$, $1/60$ and $1/100$ and $n\le3$. The relative error of (4.6), at the
  energy $\varepsilon$ above the band bottom, is $\varepsilon/8t$ for $n=0$, $\varepsilon/14.4t$ for $n=1$ and close to
  $\varepsilon/16t$ for large $n$. It reaches 5 percent at $\varepsilon=0.41\,t$ for $n=0$, $0.73\,t$ for $n=1$ and
  about $0.8\,t$ for $n\ge2$, so a level within $0.4\,t$ of the band bottom is within 5 percent of (4.6) at any flux.
- At the flux 1/20 of `landau_chern.py` the four lowest bands are 0.012, 0.060, 0.155 and $0.295\,t$ below their
  dashed lines, which is 0.02, 0.10, 0.25 and 0.47 of the spacing $0.628\,t$, and they are flat to $10^{-5}$.
- The notebook has square ribbons of 30 and of 20 sites with the fields 0.02, 0.03 and 0.04, in the cells "Landau
  levels of conventional electrons" and "Magnetic field dependence of Landau levels", and one of 40 sites with the
  field 0.02 in "Bands in the conventional quantum Hall state", which the try-it box of Section 4.7 changes to 0.04. On
  all three the two lowest levels are 0.244, 0.359 and 0.472 apart, a factor 1.94 from 0.02 to 0.04, against
  $4\pi\phi=0.251$, 0.377 and 0.503, and $\ell_B$ is 2.8, 2.3 and 2.0 sites. This is the "roughly twice" of the try-it
  box of Section 4.7 and the "roughly in proportion" of the one of Section 4.9.
- On the honeycomb lattice of pyqula, with the bond 1, $\hbar v=3t/2$ and (4.7) is $E_n=\pm3\sqrt{\pi\phi|n|}\,t$, so
  $E_1=5.32\sqrt\phi\,t$. A level holds two states per flux quantum, one for each valley, and the zero level too. The
  lattice levels are below (4.7) by $c\,(E/t)^2$ of their energy, with $c$ from 0.09 to 0.10, so by 5 percent at about
  $0.7\,t$. The armchair ribbon of 40 of the notebook has $E_1=0.371$, 0.519 and 0.711 for the field 0.005, 0.01 and
  0.02, against 0.376, 0.532 and 0.752, a factor 1.92 for a field four times larger, as the try-it box of Section 4.10
  says. Near the field 0.02 the lattice broadens the first level into a band about 0.017 wide, from 0.692 to 0.708 in
  the cell with $\phi=0.0192$, so its position is 0.71 to two digits.

## The two gauges

- The Landau gauge $\mathbf A=B(0,x)$ and the symmetric gauge $\mathbf A=\tfrac B2(-y,x)$ give a $10\times10$ island
  with (4.4) the same levels to $10^{-10}$. For the plaquette with the lower left corner at $(2,1)$ the bond phases,
  counterclockwise from the bottom bond and in units of the flux of the plaquette, are $0,3,0,-2$ in the Landau gauge
  and $-\tfrac12,\tfrac32,1,-1$ in the symmetric gauge, both with the sum 1, as `plaquette_gauge.py` draws.

## The Laughlin state

- The filled lowest level of 20 electrons, from the orbitals (4.10), has the filling 1 within 0.002 up to
  $\sqrt{2N}\,\ell_B-2\,\ell_B$, and 1/2 at $6.27\,\ell_B$ against $\sqrt{2N}=6.32$, as `droplet_density.py` draws.
  $\sqrt{2(N-1)}$ is 7.07, 10.10, 14.07 and 19.95 for $N=26$, 52, 100 and 200, the radii of the quiz of Section 4.15.
- The Slater determinant of every third orbital, $m=0,3,\dots,57$, has the filling between 0.324 and 0.333 for
  $2\,\ell_B<r<\sqrt{6N}\,\ell_B-2\,\ell_B$, and 1 at the center. So a regular pattern of empty orbitals gives a flat
  density away from the center, and a lump only within about $2\,\ell_B$ of it.
- Two electrons in $(z_1-z_2)^me^{-(|z_1|^2+|z_2|^2)/4\ell_B^2}$ have the distance distribution
  $r^{2m+1}e^{-r^2/4\ell_B^2}$, checked against the integral of $|\Psi|^2$ over the center of mass on a grid, with the
  maximum at $\sqrt{2(2m+1)}\,\ell_B$, which is 2.45, 3.74 and 4.69 for $m=1$, 3 and 5, as `laughlin_pair.py` draws.
- The highest power of $z_1$ in $\prod_{i<j}(z_i-z_j)^3$ is 6 for $N=3$ and 9 for $N=4$, which is $m(N-1)$, so the
  state uses the orbitals from 0 to $m(N-1)$. The power $m=3$ is antisymmetric and $m=2$ symmetric, the factor
  $\prod_iz_i$ of a quasihole at the origin raises the highest power by one, and
  $\det(z_i^{\,j-1})=\prod_{i<j}(z_j-z_i)$ holds to $10^{-12}$ at 6 random points.
- A Metropolis sampling of $|\Psi_3|^2$ for $N=20$, with two seeds, gives $2\pi\ell_B^2$ times the density 0.332 and
  0.334 for $r<5\,\ell_B$, so $\nu=1/3$, and its largest value, at the edge, is 31 and 32 percent above $1/3$, the
  bump of about 30 percent of the caption of `droplet_density`.
- The charge that a quasihole at the origin removes from a disc of radius $R$ is not $1/3$ at every radius. In the
  droplet of 20 electrons, with two seeds, it rises to 0.42 at $R=2.5$ and $3\,\ell_B$, it is 0.36 at $R=4\,\ell_B$, and
  its mean for $5\,\ell_B\le R\le8\,\ell_B$ is 0.325 and 0.321. The same Monte Carlo for $m=1$ follows the exact orbital
  sums to 0.03. So the charge is $e/3$ for a disc of more than about $4\,\ell_B$, and a page that quotes the charge
  inside a disc says its radius.
- The Berry phase of the quasihole (4.14) on the loop $w=|w|e^{i\theta}$ is
  $2\pi\langle\sum_i\mathrm{Re}\,w/(z_i-w)\rangle$, which is minus $2\pi$ times the number of electrons inside the loop
  when the density there is uniform. A second quasihole at the origin raises this mean by 0.29 and 0.34 for
  $|w|=6\,\ell_B$ and $N=20$, with two seeds, so the braid phase is $2\pi/3$ within the noise of the sampling and the
  exchange phase is $\pi/3$. The pages give the magnitudes of the two phases, and their sign is not used.

## The Haldane model and the field

- In pyqula a positive field with the Fermi energy in the gap above the zero level has $C=+1$, the same as
  `add_haldane(x)` with $x>0$, and below the zero level it has $C=-1$. The gap above the first level has $C=+3$, since
  every level of the honeycomb lattice holds the two valleys. This was checked in the rotated cell of 80 sites with one
  flux quantum, $\phi=0.0096$, where `add_haldane(0.07)` gives $+1$.
- Along $\nu H_\mathrm{QH}+(1-\nu)H_\mathrm C$ of the notebook cell "Topological equivalence between the Quantum Hall
  state and a Chern insulator", the armchair ribbon of 20 with the field 0.01 and `add_onsite(-0.2)` against
  `add_haldane(0.07)`, no bulk state comes closer to zero energy than 0.198, at $\nu=1$, so the bulk gap stays open, as
  Section 4.19 says. A bulk state is one with more than half of its weight in the middle half of the ribbon. With
  `add_haldane(-0.07)`, with the field $-0.01$, or with `add_onsite(+0.2)`, which puts zero energy below the zero level
  where $C=-1$, the two ends have opposite Chern numbers and a bulk state comes to zero energy on the way, near
  $\nu=0.6$ for the first. The mix adds the matrices bond by bond, so at $\nu=0.5$ the bonds at the edge have the
  moduli 0.86 and 0.97, and it is not a field of half the strength.
- The notebook cell "Topological domains in the quantum Hall state" is a square ribbon of 80 with the field 0.02, where
  `add_onsite(mufun)` gives the onsite energy $+3.5$ to the sites with $y>0$ and $-3.5$ to the others, with no Haldane
  coupling. A bulk with $+3.5$ has its band from $-0.5$ to $7.5$, two electron levels below zero energy and $C=+2$, and
  a bulk with $-3.5$ has two hole levels above zero energy and $C=-2$. Zero energy is crossed by four branches at the
  wall and by two at each outer edge.

## The figure scripts of `webnotes/figures/session04/`

- `landau_chern.py` draws the pyqula script `g1_landau_levels_square.py`, with `add_orbital_magnetic_field(1/20)` in the
  cell `(1, 20)`. This is the field along $-z$ for the charge $+e$, where each of the four lowest bands has $C=+1$ with
  the $\Omega$ of Session 3, and its caption says that the flux $-1/20$, the field $B\hat z$ of the pages, gives $-1$.
- `lattice_ribbons.py` builds panel (a) as $-2\cos(k_y-Bx)$, which is the field $+B\hat z$ with $k_y$ the momentum, and
  its guiding center moves as $+1/B$ with $k_y$. Panel (b) has the phase (4.4) of the field $+B\hat z$ but the Bloch
  phase $e^{+ik_y(y_i-y_j)}$, so its $k_y$ is minus the momentum and its guiding center moves as $-1/B$, as the caption
  says. The reversal in (b) comes from this sign and is not a property of the honeycomb lattice.
- `flat_chern_band.py` draws the pyqula script `g5_haldane_t3_bands.py`, with `add_haldane(+0.1155)` for $t_2=0.1$ and
  $\phi=\pi/2$, and with `tij=[1, 0.0927, -0.2]` and `add_haldane(+0.3295)` for $t_2=0.3$, $\phi=0.4\pi$ and
  $t_3=-0.2$. Both lower bands have $C=+1$, from `h.get_chern()` and from the link variables. The widths of the lower
  band are 2.48 and 0.212, the gaps 1.04 and 2.97, and the ratio of (b) is 14.0.
- `tij=[1, a, b]` of the honeycomb lattice of pyqula with `add_haldane(c)` is `_honeycomb.bloch(t2, phi, t3)` of Session 3
  with $a=t_2\cos\phi$, $b=t_3$ and $c=2t_2\sin\phi/\sqrt3$. The spectra on a mesh of the zone agree to $2\cdot10^{-15}$
  for `add_haldane` of 0.05, 0.1, 0.1155 and 0.2 alone, and for the two models of (b) and of the trivial quiz option.
- The flat band with $C=0$ of the quiz of Section 4.20, with the real $t_2=0.2$ and the staggered potential $M=1.5$,
  `add_sublattice_imbalance(1.5)`, has the width 0.200 and the gap 3.000.
- In `plateaus.py` the plateau $N$ is flat for the filling from $N-0.36$ to $N+0.36$, and the classical line crosses it
  at $\nu=N$, its middle in $1/B$. In $B$, the axis of the figure, the middle of the flat part is at 1.12, 0.517 and
  0.339 for $N=1$, 2 and 3, against the crossings at 1, 0.5 and 0.333.
- `wall_squeeze.py` has the lowest level of the oscillator with a hard wall at 0.500, 0.734 and $1.500\,\hbar\omega_c$
  for the center at 3, 1 and $0\,\ell_B$ from the wall, by finite differences and by the zero of the parabolic
  cylinder function $D_{E/\hbar\omega_c-1/2}(-\sqrt2\,x_0/\ell_B)$, the 0.50, 0.73 and 1.50 of the quiz of Section
  4.11. The ribbon of $12\,\ell_B$ of `ribbon_three.py` has three crossings per wall at $\mu=3\hbar\omega_c$, and two
  per wall at $\mu=2\hbar\omega_c$, as Figure 4.1 says.
- `hall_setup.py` draws the edge channels counterclockwise with the field into the page. This is the sense of an
  electron, as its docstring says, since an electron in a field into the page has $qB>0$. The charge $+e$ of the pages
  goes around clockwise there, and in the island above with the field into the page it carries $+0.196$ along $x$ in
  the upper half.

## Open points of the old text, settled on 2026-11-22

Each bullet below was an open point of the old text, and it is kept with its history. The plan of the session says how
each one was settled, in its lists "Corrected on the web, to carry over to the .tex" and "Decided on 2026-11-22".

- Sections 4.4, 4.14 and 4.21 and the index of the session said that every Landau level has $C=1$, and (4.2) wrote
  $\sigma_{xy}=N\,e^2/h$. For the charge $+e$ in the field $+B\hat z$ of Sections 4.8 and 4.9 every level has $C=-1$,
  and (3.4) gives $-N\,e^2/h$. The old text holds for $|C|$, or for an electron, which is also the sign of pyqula.
  Decided by the lecturer on 2026-11-22: the pages write $|C_n|=1$, (4.2) writes $|C_\text{tot}|=N$ and
  $|\sigma_{xy}|=N\,e^2/h$, and one sentence of Section 4.4 gives $C_n=-1$ for the charge $+e$ in $B\hat z$ and $+1$ for an
  electron.
- Section 4.9 said that for an electron "every cyclotron orbit and every edge current below goes around in the other
  direction, and nothing else changes". For the charge $-e$ the lowest level is $\bar z^me^{-|z|^2/4\ell_B^2}$ with
  $L_z=-m\hbar$, the Dirac zero mode lives in the lower component, and $C$ and $\sigma_{xy}$ change sign. Corrected on the
  web on 2026-11-22.
- Section 4.2 and its figure take the current along $x$ for a voltage along $y$, $I_x=N(e^2/h)V_y$, which is the
  opposite order of (3.4), and for $qB>0$ this current is $+N\,e^2/h$ while (3.4) gives $-N\,e^2/h$. The figure draws
  the field into the page with counterclockwise channels, the sense of an electron, while the pages take the charge
  $+e$, which goes around clockwise there. `hall_setup.py` writes $V_y$ at the top contact and $0$ at the bottom one,
  and draws $I_x$ out of the left contact. Decided on 2026-11-22 by the rule of the coordinator: the order stays, and
  the caption of `hall_setup` says that its arrows are drawn for electrons and go around the other way for the charge
  $+e$. After an independent check it also says that for the charge $+e$ the channels of the top contact end in the
  right contact, where the current is then read. `g1_01` counts the four contacts with Landauer-Buttiker, with the
  left and the right contact at 0.
- Section 4.10 and the caption of Figure 4.4 said that the levels of graphene are about two orders of magnitude above
  those of GaAs, and Section 4.1 says roughly one order of magnitude and around 100 meV at 10 T. At 10 T the factor is
  6.6, with 115 meV against 17.3 meV, as the quiz of Section 4.2 says. Section 4.1 also gave roughly one
  millielectronvolt for the fields of a laboratory, while the scale is 1.73 meV per tesla, and 6.9 meV at 4 T in the
  quiz of the same page. This was an open point of the sheet of Session 3 too. Section 4.10 and the GaAs scale were
  corrected on the web on 2026-11-22, and the graphene bullet of Section 4.1 was kept by the decision of that day.
- Section 4.16 said that leaving orbitals empty gives a density with lumps, which holds only within about
  $2\,\ell_B$ of the center for a regular choice, since every third orbital gives a density within 3 percent of 1/3
  further out. Decided on 2026-11-22 by the rule of the coordinator: the example is one orbital out of every three,
  and the lumps come from an irregular choice of the empty orbitals.
- The notebook box of Section 4.19 said that in "Topological domains" the two couplings compete, while that cell has a
  field and two onsite energies, with $C=+2$ and $-2$, and no Haldane coupling. The comment of the notebook calls the
  half with $y>0$ a hole band, while `add_onsite(mufun)` adds $+3.5$ there and makes it an electron band. The box was
  corrected on the web on 2026-11-22, and the comment stays, since the notebooks are not edited.
- Section 4.19 said that the gap stays open at every step of the path from the Haldane model to the quantum Hall
  state. This holds for the signs of the notebook, with the field and the Haldane coupling of the same sign of $C$ and
  the chemical potential in the gap above the zero level, and the gap closes with the other sign of either of them.
  Corrected on the web on 2026-11-22.
- The caption of `plateaus` said that every plateau crosses the classical line at its center. This holds in $1/B$,
  while on the $B$ axis of the figure the crossing of $N=1$ is at 1.00 and the middle of its flat part at 1.12.
  Corrected on the web on 2026-11-22.
