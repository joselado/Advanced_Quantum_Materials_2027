# Conventions of Session 8, checked by number

This sheet fixes the signs, the units and the pyqula and dmrgpy facts that the pages, the figures and the scripts of
Session 8 use. An agent that edits the session reads it first and does not work these out again. Every bullet was
checked with a number on 2026-11-21. Two drafts were written apart, and a third calculation settled each line where
they differed or where only one of them had it. The spin energies are in units of the exchange $J$ and the band
energies in units of the hopping $t$, which pyqula takes as $+1$. A number from a mesh of momenta is given with the
mesh that holds it, or with two digits when the mesh moves the third. The pyqula of the checks is the development tree
at commit 7567127, and the release that the students install was not run for these lines. A statement that is not on
this sheet is checked before a page claims it. The check is `webnotes/checks/session08/conventions.py`, which prints
one line per bullet below, in the same order and the open points included, in about two minutes.

## Spins and the exchange

- The Heisenberg coupling of (8.2), (8.4) and (8.13) is the one of (6.5), of Section 7.6 and of Section 9.9,
  $H=\sum_{\langle ij\rangle}J_{ij}\,\mathbf S_i\cdot\mathbf S_j$ with each bond once, $\mathbf S=\boldsymbol\sigma/2$
  and $\hbar=1$, and $J>0$ is antiferromagnetic.
- As a reference, the Hubbard dimer at $U=20t$ has its singlet $0.1980t$ below the triplet, where $4t^2/U$ of (6.4)
  gives $0.2t$. Checked on the six states with two electrons.
- The Heisenberg dimer (8.2) has the singlet at $-3J/4$ and the threefold triplet at $+J/4$, so the gap is $J$. For
  $J<0$ the triplet at $J/4$ is the ground level, threefold degenerate. The Ising dimer (8.1) has $-1/4$ and $+1/4$,
  twice each, the lower for antiparallel spins. It is one bond of the Ising model (10.9) of Session 10,
  $-J\sigma_0\sigma_1$ with $\sigma=\pm1$, for $J=-1/4$, since there a positive $J$ favors parallel spins, as the sheet
  of Session 10 says. Checked on the $4\times4$ matrices and with the exact diagonalization of dmrgpy.
- The singlet (8.3) has $\langle\mathbf S_i\rangle=0$, and time reversal maps it to itself. Its two Schmidt weights are
  1/2 and 1/2, so its entanglement entropy is $\ln2=0.693$, with the natural logarithm of (7.7).
- The total spin of $N$ spins one half is an integer for even $N$ and a half-integer for odd $N$, and the spin $S$
  appears $\binom{N}{N/2-S}-\binom{N}{N/2-S-1}$ times. Four sites have $S=0$ twice, $S=1$ three times and $S=2$ once.
  Checked against the eigenvalues of $\mathbf S^2_\text{tot}$ for $N=2$ to 7.
- With (8.8), $\langle a_i^\dagger a_i\rangle=S-\langle S^z_i\rangle$. One site of the singlet is up with the
  probability 1/2, so $\langle a_i^\dagger a_i\rangle=1/2=S$, which is (8.9), with no boson and one boson on the site
  with the probability 1/2 each.

## Frustration

- On a triangle of Ising spins $S^z=\pm1/2$ with $J=1$, six of the eight configurations have one unsatisfied bond and
  the energy $-1/4$, and the two aligned ones have $+3/4$.
- The Heisenberg triangle of three spins one half has its ground level $-3J/4$ four times, two doublets with $S=1/2$,
  since $H=\frac J2(\mathbf S^2_\text{tot}-\frac94)$. An odd number of spins one half has no singlet, so a ground state
  with $S_\text{tot}=0$ and $\langle\mathbf S_i\rangle=0$ needs an even number of sites.
- On the periodic clusters of the figure `ising_degeneracy` of Section 8.4, the antiferromagnetic Ising model has 2
  ground states on the square clusters of 8, 16 and 24 sites, 1698 on the triangular cluster $6\times4$, which is 0.310
  per site for the logarithm, and 8882 and 181122 on the kagome clusters of 18 and 24 sites, 0.505 and 0.504 per site.
  Two counts give these numbers, the configurations of lowest energy among all $2^N$, and the configurations with
  every bond antiparallel on the square clusters and with no triangle of three equal spins on the others. The infinite triangular lattice has 0.3231 per site, from $\frac2\pi\int_0^{\pi/3}\ln(2\cos\omega)\,d\omega$,
  and the kagome lattice about 0.50, where the Pauling count $\ln2+\frac23\ln\frac34$ gives 0.501. These are the slopes
  0.32 and 0.50 of the figure.
- In pyqula `square_lattice()` and `kagome_lattice()` have 4 first neighbors and `triangular_lattice()` has 6, so the
  kagome and the square lattice have the same coordination, as the quiz of Section 8.4 says. The kagome cell has
  $a_1=(2,0)$ and $a_2=(1,\sqrt3)$, the bond length 1 and the lattice constant 2.

## The dimerized chain

- The same chain has two notations. (8.4) writes $J$ inside the dimers, the figure `dimerized_levels` of Section 8.5
  adds $J'$ between them, and the widget of Section 7.6 writes $J_1=J$ and $J_2=J'$ for the same two. The notebook gives the
  bond between $i$ and $i+1$ the value $1+0.2(-1)^i$, so the bond between sites 0 and 1 is the strong one, $J=1.2$
  and $J'=0.8$, with $J'/J=2/3$. The open chain of 40 sites starts and ends with a strong bond, so no spin is left
  free at an end.
- The open chain of four sites with the bonds $J$, $J'$, $J$ has the ground level $-1.50096J$ and the threefold level
  $-0.52749J$ at $J'=0.1J$, a gap $0.973J$, and the gap $0.659J$ at $J'=J$. The ground state is a nondegenerate
  singlet for every $J'$ from 0 to $J$, with the energy
  $E_0=-\frac12\big(J+\frac{J'}2\big)-\frac12\sqrt{(2J-\frac{J'}2)^2+\frac34J'^2}$ from the two singlets of the
  dimers. Checked with numpy, with this closed form and with dmrgpy.
- The 0.973 of four sites is a finite-size number. The infinite chain of dimers with $J'=0.1J$ has the triplet gap
  $0.9463J$, the same on rings of 12, 16 and 20 sites to $10^{-6}$, and the series
  $J(1-\frac\alpha2-\frac{3\alpha^2}8+\frac{\alpha^3}{32})$ with $\alpha=J'/J$ gives 0.9463 too. Open chains with a
  strong bond at each end are above it, $0.9517J$ and $0.9496J$ for 12 and 16 sites, the numbers of the sheet of
  Session 7, since there the lowest triplet is a standing wave above the bottom of its band. So a page that quotes the
  gap says whether it is the open chain or the infinite one.
- The dimerized chain of the notebook, with the bonds $1\pm0.2$, has the spin gap 0.623, 0.605 and 0.600 on rings of
  12, 16 and 20 sites, from Lanczos in the sectors of $S^z$. With the bonds $1\pm0.05$ the gap is not converged on
  these rings, it falls from 0.38 to 0.27, so a page says only that it is below 0.27.
- In the notebook cells with a field on site 0, the term $+B_zS^z_0$ with $B_z=1$ gives $\langle S^z_0\rangle=-0.41$
  on the uniform chain, so the moment points against the coefficient. It alternates in sign from site to site, and the
  total stays 0. With dmrgpy on 40 sites, $|\langle S^z_n\rangle|$ at $n=10$ and $n=20$ is 0.121 and 0.081 on the
  uniform chain, 0.0056 and $1.2\cdot10^{-4}$ for the dimerization 0.2, and 0.055 and 0.014 for 0.05. These give the
  decay lengths 2.6 and 7.2 sites, while the uniform chain decays much more slowly. The 2.6 is close to $v/\Delta$ with
  the spinon velocity $v=\pi J/2$ and the gap 0.600 above, and Lanczos on 20 sites gives the same 0.0056 at $n=10$.
- The uniform open chain of 40 sites of the notebook has the gap 0.096 to the lowest triplet, from dmrgpy. A uniform
  field $+B_z\sum_iS^z_i$ commutes with the Heisenberg term, so it leaves the total $S^z$ at zero until $|B_z|$
  reaches this gap. With the $B_z=-0.01$ of the notebook every $|\langle S^z_i\rangle|$ is below $10^{-5}$, and with
  $B_z=-0.15$ the ground state has $S^z=1$, since $B_z<0$ favors $S^z>0$.

## The resonating valence bond state

- The projector $P_G=\prod_in_i(2-n_i)$ of (8.7) is 1 on a singly occupied site and 0 on an empty or a doubly
  occupied one.
- On the plaquette of the figure `rvb_plaquette` of Section 8.6, with $J$ on its four bonds, the coverings
  $|a\rangle=(01)(23)$ and $|b\rangle=(12)(30)$, and each singlet $(|{\uparrow\downarrow}\rangle-|{\downarrow\uparrow}\rangle)/\sqrt2$
  in the order of its pair, $\langle a|b\rangle=+1/2$ and a single covering has $-3J/2$. Then $|a\rangle+|b\rangle$
  has $-2J$ at $\theta=\pi/4$, the exact ground state, with $S_\text{tot}=0$ and both diagonals $(02)$ and $(13)$ in a
  triplet, so $\frac J2(0-2-2)$. The other combination $|a\rangle-|b\rangle$ is a singlet at 0. With $|b\rangle$
  written as $(12)(03)$ the overlap is $-1/2$ and the two combinations exchange their roles, so a page that writes the
  sign of the resonance also writes the order of the pairs.

## Abrikosov fermions

- On the four states of a site, (8.10) gives $[S^x,S^y]=iS^z$ and its cyclic partners, $\mathbf S^2=3/4$ on the two
  singly occupied states and 0 on the empty and on the doubly occupied one, and $f^\dagger_\uparrow$ raises $S^z$ by
  1/2. Checked with fermion matrices that carry the Jordan-Wigner signs.
- The Fierz identity of Section 8.8 holds for all 16 sets of indices. (8.12) holds exactly with one fermion on each of
  the two sites and misses by up to 0.75 elsewhere, so it needs (8.11). On the constrained space
  $\chi^\dagger_{ij}\chi_{ij}$ is 2 on the singlet and 0 on the triplet, as the quiz of Section 8.8 says.
- (8.19), $f^\dagger_\alpha f_\beta-\frac n2\delta_{\alpha\beta}$, is the spin (8.10) written as the matrix
  $(\mathbf S\cdot\boldsymbol\sigma)_{\beta\alpha}$, and its trace is zero on all four states of a site, also on the
  empty and on the doubly occupied one. So it does not hold the constraint (8.11).

## The spinon mean field

- In (8.14) the coefficient of $f^\dagger_{i\sigma}f_{j\sigma}$ is
  $-(J_{ij}/2)\langle\chi_{ij}\rangle^*=-(J_{ij}/2)\sum_\sigma\langle f^\dagger_{j\sigma}f_{i\sigma}\rangle$, and (8.15)
  calls this coefficient $\chi_{ij}$. So the spinon hopping is proportional to $J$. On the uniform chain at half filling
  $|\langle f^\dagger_if_{i+1}\rangle|=1/\pi$ per spin, so $|\chi|=J/\pi=0.318J$ and the band is $2\chi\cos k$. Both
  signs of $\chi$ are fixed points of the loop, since $f_j\to(-1)^jf_j$ maps one to the other. pyqula's
  `SpinonHamiltonian` with `decoupling="bond"` gives $|t|=0.3183$ with one fermion per site and a phase that changes
  from run to run, so a page quotes $|\chi|$.
- The uniform chain is a self-consistent solution of (8.14) and not its minimum. The loop started within $10^{-3}$ of
  it, from either sign, ends after about 100 steps at the hoppings $J/2$ and 0 on alternate bonds, with the mean-field
  energy $J/4-(J/2)|\langle\chi\rangle|^2$ equal to 0 per bond, against $0.047J$ for the uniform state. pyqula's loop on
  `bichain()` ends at 0.500 and 0.000 too. A page that uses the gapless uniform chain, as Sections 8.9 and 9.9 do,
  takes it as an ansatz.
- Half filling of the spinons is one fermion per site, which is `filling=0.5` of pyqula for a spinful Hamiltonian,
  since pyqula counts the fraction of all the states and a spinful site has two.
- The three classes of the figure `spinon_bands` of Section 8.9 hold, for one spin and $\chi=1$. The figure takes the
  hopping $-\chi$, so its uniform chain is $-2\chi\cos k$, which crosses zero at $k=\pm\pi/2$. The chain with the hoppings 1 and 0.6 has the gap
  $2|\chi_1-\chi_2|=0.8$, with numpy and with pyqula's `bichain()`. The $\pi$-flux square lattice of the figure, with
  $-\chi$ along $x$ and $-\chi(-1)^x$ along $y$, has $\pm2\chi\sqrt{\cos^2k_x+\cos^2k_y}$ and $\Phi=-1$ on every
  plaquette, with the two Dirac points $(k_x,k_y)=(\pi/2,\pm\pi/2)$ of the zone of its cell of two sites.
- In pyqula the same flux is `square_lattice().get_supercell([1, 2])` with `add_orbital_magnetic_field(0.5)`. This is
  another gauge, with the bands $\pm2\sqrt{\sin^22\pi k_1+\cos^2\pi k_2}$ from $-2\sqrt2$ to $2\sqrt2$ and the Dirac
  points at the reduced momenta $(k_1,k_2)=(0,1/2)$ and $(1/2,1/2)$, which is $(0,\pi/2)$ and $(\pi,\pi/2)$. The gauge
  moves the Dirac points and not the levels. With `get_supercell([2, 1])` the same call leaves every hopping real,
  which is no flux, with the bands from $-4$ to 4. Both cells hold one flux quantum, the whole number that the sheet of
  Session 4 asks for, and only the cell repeated along $y$ carries the field, since the vector potential of pyqula is
  along $x$ and changes only along $y$.
- On a bipartite lattice the sign of $\chi$ is a gauge choice, and $\chi$ and $-\chi$ give the same levels on the open
  $6\times6$ lattice. On the triangular lattice it is not. `tij=[1., 0.5]` and `tij=[-1., -0.5]` fill complementary
  halves of the zone at half filling and so have the same Fermi surface, while `tij=[1., -0.5]` differs from them on
  0.23 of the zone. So the relative sign of $t_2/t_1$ is what the notebook changes.

## The gauge structure

- Under (8.16) the operator $\chi_{ij}=\sum_\sigma f^\dagger_{i\sigma}f_{j\sigma}$ of (8.12) and its expectation value
  get $e^{-i(\theta_i-\theta_j)}$, while the coefficient $\chi_{ij}$ of (8.15), which is
  $-(J/2)\langle\chi_{ij}\rangle^*$, gets $e^{+i(\theta_i-\theta_j)}$, so that $\sum\chi_{ij}f^\dagger_if_j$ keeps its
  form. Section 8.10 and its quizzes use the second, where the link 12 gets $i$ for $\theta_1=\pi/2$. The flux is the
  same for both.
- On the open $6\times6$ lattice with $\chi=1$, a random gauge rotation keeps every flux and every level to
  $10^{-12}$. The string of three vertical links from the left edge set to $-1$ gives $\Phi=-1$ on the central
  plaquette and $+1$ on the other 24, and the levels move by up to 0.360, the number of the figure `gauge_levels` of
  Section 8.10. A string of three horizontal links from the bottom edge that ends on the same plaquette gives the same
  fluxes and levels, since the two strings differ by a gauge rotation.
- Which flux is the ground state depends on the lattice and the filling, and on the square lattice at half filling it
  is not $\Phi=+1$. Per site and spin the uniform hopping gives $-8/\pi^2=-0.811$ and the $\pi$-flux hopping $-0.958$,
  both with $|\chi|=1$. With $|\chi|=1$ fixed, one flipped plaquette in the uniform background lowers the energy of the
  half-filled spinons by 0.74 per spin on the open $6\times6$ lattice and by 0.69 on $12\times12$, and in the
  $\pi$-flux state one plaquette set back to $+1$ costs between 0.20 and 0.54 per spin on the open lattices of side 6
  to 12. So a vison is a plaquette whose flux differs from that of the ground state, and
  on this lattice it costs energy against the $\pi$-flux background.

## The Kondo impurity and the Kondo lattice

- (8.17) and (8.18) multiply $c^\dagger\boldsymbol\sigma c$ by $J_K$ with no factor 1/2, so $H_K=2J_K\,\mathbf s\cdot
  \mathbf S$ with $\mathbf s=\frac12c^\dagger\boldsymbol\sigma c$ the spin of the conduction electron, and $J_K>0$ is
  antiferromagnetic. The impurity with one electron on its site has the singlet at $-3J_K/2$ and the triplet at
  $+J_K/2$, a splitting $2J_K$. A formula written for $J\,\mathbf s\cdot\mathbf S$ is brought to this sheet with
  $J=2J_K$.
- On the states with one $f$ fermion, $J_K(c^\dagger\boldsymbol\sigma c)\cdot\mathbf S=-J_K\big(\sum_\beta
  c^\dagger_\beta f_\beta\big)\big(\sum_\alpha f^\dagger_\alpha c_\alpha\big)+\frac{J_K}2n_c$, so (8.20) is (8.18) up to
  the potential scattering $\frac{J_K}2n_c$ that its $\sim$ leaves out. On all 16 states of a site the extra terms are
  $J_Kn_c-\frac{J_K}2n_cn_f$.
- Per spin, (8.21) is $\begin{pmatrix}\varepsilon_\mathbf k&-\gamma_K\\-\gamma_K&0\end{pmatrix}$ in the basis
  $(c,f)$, with $E_\pm=\big(\varepsilon_\mathbf k\pm\sqrt{\varepsilon_\mathbf k^2+4\gamma_K^2}\big)/2$. So
  $E_-<0<E_+$ at every $\mathbf k$, and the direct gap is $2\gamma_K$, at $\varepsilon_\mathbf k=0$. The sign of
  $\gamma_K$ is a gauge choice, $f\to-f$, and does not change the bands. On the chain with $\varepsilon=-2t\cos k$ the
  indirect gap is $2(\sqrt{t^2+\gamma_K^2}-t)$, which is 0.0100, 0.236 and 0.332 for $\gamma_K=0.1$, 0.5 and 0.6,
  against $\gamma_K^2/t=0.01$, 0.25 and 0.36. So the gap is $\gamma_K^2/t$ to within 10 percent up to $\gamma_K=0.6t$.
- With a half-filled conduction band that is symmetric around zero and the $f$ level at zero, the lower band holds one
  state per $\mathbf k$ and spin, half a $c$ electron and half an $f$ fermion, with the $f$ weight 0.500 for
  $\gamma_K=0.6t$ on the chain. The Bogoliubov-de Gennes matrix $\begin{pmatrix}\varepsilon&\Delta\\\Delta&-\varepsilon\end{pmatrix}$
  of the figure `kondo_bdg` of Section 8.13 has the gap $2\Delta$, 1.000 for $\Delta=0.5$, and pyqula's
  `add_swave(0.5)` on the chain gives 1.000 on 400 momenta.
- The mean field of (8.20) takes $\gamma_K=J_K\sum_\sigma\langle c^\dagger_\sigma f_\sigma\rangle$ on each site, with
  the constant $\gamma_K^2/J_K$ per site, and $\gamma_K$ is the minimum of the energy of the filled bands plus this
  constant. For a flat band of half width $D$ and the density $\rho=1/(2D)$ per spin, the gap equation is
  $4\rho J_K\,\mathrm{asinh}(D/2\gamma_K)=1$, which gives $0.3121D$ at $J_K=0.4D$, the same as the minimum. On the
  half-filled chain with $t=1$ it is $(2J_K/\pi)K(m)/\sqrt{1+\gamma_K^2}=1$ with $m=1/(1+\gamma_K^2)$, which gives
  $\gamma_K=0.2827$ at $J_K=0.6$ and 0.5270 at $J_K=0.8$, with the $f$ level at zero and one $f$ fermion per site.
  pyqula's `KondoLatticeHamiltonian` gives the same numbers with its coupling $J=2J_K$.
- The Kondo scale in the convention of (8.17) is $T_K\sim D\,e^{-1/(2\rho J_K)}$, with $\rho$ the density of states per
  spin and per site at the Fermi level, which is $D\,e^{-1/(\rho J)}$ for a coupling written $J\,\mathbf s\cdot\mathbf
  S$. The logarithm of the indirect gap of the chain against $1/J_K$ has the slope $-3.14$ between $J_K=0.3$ and 0.35,
  against $-1/(2\rho)=-\pi t$, and on the flat band $\gamma_K^2/D$ is $D\,e^{-1/(2\rho J_K)}$ to $10^{-3}$ at
  $J_K=0.1D$. A page that writes the exponent says which coupling it uses.

## pyqula and dmrgpy

- `triangular_lattice()` has $a_1=(1,0)$ and $a_2=(-1/2,\sqrt3/2)$, one site per cell and the hopping $+1$, so the
  band is $2[\cos2\pi k_1+\cos2\pi k_2+\cos2\pi(k_1+k_2)]$ in reduced momenta, from $-3$ to 6. `tij=[1., t2]` puts
  $t_2$ on the six second neighbors with its sign, and the default Hamiltonian is spinful.
- `h.set_filling(0.5, nk=10)` of the notebook takes the Fermi level from a $10\times10$ mesh, which holds degenerate
  levels, and moves it to zero. For $t_2=0$, $-0.5$ and $0.5$ the zero then sits at $-0.618$, $+0.236$ and $-1.000$,
  which is the filling 0.529, 0.513 and 0.495, where the half filling is at $-0.835$, $+0.103$ and $-0.983$.
  `nk=60` gives 0.5035 and 0.497 for the first two and leaves the third at $-1.000$, the filling 0.495. A page that
  quotes the size of a Fermi surface takes the Fermi level from a dense mesh.
- `(kx, ky, w) = h.get_fermi_surface(e=0., delta=d, nk=n)` returns flat arrays of $n^2$ entries whose first index
  runs along `kx`, with `kx` and `ky` from $-1$ to 1 in units of $2\pi$ over the lattice constant. The weight is
  $\sum_n\delta/((e-E_n)^2+\delta^2)$ with no $1/\pi$, summed over both spins of a spinful `h`, so it is $2/\delta$
  where the two spins of a state sit at $e$, the `vmax` of the notebook. The square lattice at half filling has its
  map on $\cos2\pi k_x+\cos2\pi k_y=0$, which is $|k_x|+|k_y|=\pi$ in true momenta inside the first zone. The triangular
  map differs from its transpose by 0.98 of its largest value, so `imshow(d2d)` of the notebook puts $k_x$ on the
  vertical axis, and a figure draws `d2d.T` with `origin="lower"`. The call writes `FERMI_MAP.OUT`.
- With the hopping $+1$ of pyqula the flat band of `kagome_lattice()` is the lowest one, at $-2$, the Dirac points at
  $K$ are at the energy 1, which is the filling 2/3, and half filling puts the Fermi level at $-0.47$, inside the
  middle band. A mesh of 960 points per side gives $-0.4715$, and meshes of 120 to 240 points move the third digit.
- `specialhamiltonian.H2HFH(h, JK, J)` puts one Kondo site at $z=+0.5$ above each site of `h`, which moves to
  $z=-0.5$, with its level at zero, and couples the two with the hopping `JK`. It is not self-consistent, so `JK` is the
  $\gamma_K$ of (8.21) and not the $J_K$ of (8.17), and the direct gap is $2\,$`JK`. `J` is a first-neighbor hopping of
  the Kondo sites, a spinon hopping and not an exchange, and `set_filling(0.5)` on its default mesh `nk=10` moves their
  band so that zero sits at its filling 0.529. An `add_onsite` after the call moves the Kondo level too, so the onsite
  energy of the conduction electrons goes into `h` before. The operator `"dispersive_electrons"` is the weight on the
  conduction sites, from 0 to 1.
- In the notebook cell "Quantum magnetism in the Kondo lattice" the conduction band with `add_onsite(-2.0)` runs from
  $-5$ to 4, with 0.774 of it below zero. `JK` equal to 0.25, 0.5 and the 1.0 of the second cell give the direct gaps
  0.50, 1.00 and 2.00 and the indirect gaps 0.028, 0.111 and 0.429, on a mesh of 90 points per side that holds
  $\Gamma$ and $K$. Half of all the states lie below zero for any onsite energy, also one that moves the whole band off
  zero, since $E_-<0<E_+$ at every $\mathbf k$. But at that Fermi level the Kondo sites hold 0.46 and 0.48 fermions for
  `JK=0.25` and 0.5, since `H2HFH` does not impose (8.11). The half-filled case of Figure 8.6, with one $f$ fermion per
  site, needs a band that is symmetric around zero, such as `square_lattice()` with no onsite energy, which holds one of
  each and has the indirect gap $\sqrt{17}-4=0.123$ at `JK=0.5`.
- In the notebook cell "Spinon dispersion in the Kondo lattice", with `add_onsite(-4.0)` and `JK=0.5`, the indirect
  gap is 0.154 at `J=0`, and the bands overlap by 0.062 at `J=0.025` and by 0.276 at `J=0.05`, while the direct gap
  stays 1.00, on the same mesh.
- `pyqula.kondolattice.KondoLatticeHamiltonian` takes the coupling $J$ of $(J/2)S_{ab}c^\dagger_bc_a$ with
  $S_{ab}=f^\dagger_af_b-\frac12n_f\delta_{ab}$, which equals $(J/2)\,(c^\dagger\boldsymbol\sigma c)\cdot\mathbf S$ on
  the 16 states of a site, so its $J$ is $2J_K$. Its field `hybridization` is
  $V=-(J/2)\sum_\sigma\langle c^\dagger_\sigma f_\sigma\rangle$, which is $\gamma_K$ up to the sign of the gauge
  $f\to-f$. The loop started from $V=0$ stays there, so the guess `mf` is needed. The multiplier `constraint_lambda`,
  the energy of the $f$ level that keeps one $f$ fermion per site, is zero on the half-filled chain and $-1.12$ at the
  filling 0.15 of the conduction electrons.
- dmrgpy's `Spin_Chain(["S=1/2"]*n)` has $S^z=\pm1/2$, and the notebook adds `Bz*sc.Sz[i]`, so `Bz<0` favors up spins.
  A DMRG run of dmrgpy wrote no file in the folder where it ran, while pyqula's `get_bands` writes `BANDS.OUT` and
  `get_fermi_surface` writes `FERMI_MAP.OUT` there.

## Open points of the old text, left as they are

- Section 8.10 calls the state with $\Phi=+1$ on every plaquette of the square lattice "a ground state" and the
  flipped plaquette "an excited state", and the caption of Figure 8.5 says that the flip "costs energy". For
  half-filled spinons with a fixed $|\chi|$ the flip lowers the energy, by 0.74 on the open $6\times6$ lattice, and the
  $\pi$-flux state is the lower one.
- The caption of Figure 8.2 says that on the frustrated triangle quantum fluctuations give "one superposition" with
  $\langle\mathbf S_i\rangle=0$ that does not break time reversal. Three spins one half have a fourfold ground level
  with $S=1/2$, so this holds only for an even number of sites.
- An answer of a quiz of Section 8.12 says that the hybridization "opens a gap $2\gamma_K$ as in the Kondo insulator".
  The gap of the Kondo insulator is the indirect one, 0.332 for $\gamma_K=0.6t$ on the chain, and $2\gamma_K$ is the
  direct gap at the crossing, as Section 8.13 says.
- Section 8.13 compares the spectra "for increasing $J_K$" at $J_K=0.25$ and 0.5, and the try-it box of Section 8.12
  uses the same values. These are the `JK` of the notebook, the $\gamma_K$ of (8.21), with the direct gaps 0.5 and 1.0.
  The same try-it box asks whether the gap stays at the Fermi level when `add_onsite(-2.0)` changes. The energy zero is
  in the gap for any onsite energy, and with `add_onsite(-2.0)` the Kondo sites hold 0.48 fermions there, so the
  notebook model is not the half-filled Kondo insulator of Figure 8.6.
- The try-it box of Section 8.13 says that the gap "should become smaller" when `J` grows. At `J=0.025` the bands
  already overlap by 0.062, so the gap at the Fermi level is gone, and only the direct gap of 1.0 remains.
- Section 8.11 calls $H_K$ a coupling to "the local spin density", while (8.17) couples to twice the spin density.
- Section 8.12 calls (8.19) the "equivalent traceless form" of the constraint (8.11). (8.19) is the spin (8.10) as a
  matrix, and its trace is zero for any occupation, so it does not fix one fermion per site.
- Section 8.12 says that $\gamma_K$ is "the only mean-field parameter". The constraint (8.11) on average adds a
  Lagrange multiplier, the energy of the $f$ level, which is zero only for a half-filled band that is symmetric around
  zero. With the $f$ level at zero the triangular band of the notebook gives 0.48 $f$ fermions per site, and the
  multiplier of `KondoLatticeHamiltonian` is $-1.12$ at the filling 0.15.
- Sections 8.9 and 9.9 use the uniform spinon chain, which the free loop of (8.14) leaves for the dimerized state.
  Section 9.9 says that the spin-1/2 chain "maps onto a gapless tight-binding chain of spinons", which holds for the
  uniform ansatz.
- Section 8.10 and its first quiz write $\chi_{ij}\to e^{i(\theta_i-\theta_j)}\chi_{ij}$ for the bond variable. This is
  right for the coefficient of (8.15), while the operator $\chi_{ij}$ of (8.12), which has the same name, gets the
  opposite phase.
- The caption of the figure `rvb_plaquette` does not give the order of the singlet pairs, which decides whether
  $|a\rangle+|b\rangle$ or $|a\rangle-|b\rangle$ is the ground state.
- The notebook, not a page, draws the Fermi surface with $k_x$ on the vertical axis under the label $k_y$, and sets the
  filling on a $10\times10$ mesh.
