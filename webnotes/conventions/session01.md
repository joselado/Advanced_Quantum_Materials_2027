# Conventions of Session 1, checked by number

This sheet fixes the signs, the units and the pyqula facts that the pages, the figures and the pyqula scripts of
Session 1 use. An agent that edits the session reads it first and does not work these out again. Every bullet was
checked with a number on 2026-11-21. Two drafts were written apart, and a third calculation settled each line where
they differed or where only one of them had it. The energies are in units of the hopping $t$. The section on the
Hubbard term is written so that Sessions 6 and 9 can quote it as it is. The pyqula of the checks is the development
tree at commit 7567127. The notebook and the downloaded scripts run the release 0.0.96 of PyPI, whose code was read,
and run only for the point below. Its `get_mean_field_hamiltonian` takes `return_total_energy`, its spinless loop
takes `compute_cross` and `write`, and it has the same default meshes, `nk=8` for the loop and 30 cells for `get_vev`,
and the same guess `"CDW"`. It differs in one point, which is in the bullet on the mean-field call. A statement that
is not on this sheet is checked before a page claims it. The check is `webnotes/checks/session01/conventions.py`,
which prints one line per bullet below, in the same order.

## Operators and the Fock space

- A Fock state is written with the creation operators in the order of the sites,
  $|n_0n_1n_2\rangle=(c_0^\dagger)^{n_0}(c_1^\dagger)^{n_1}(c_2^\dagger)^{n_2}|0\rangle$. Then
  $c_0^\dagger c_1^\dagger|0\rangle=+|110\rangle$, $c_1^\dagger c_0^\dagger|0\rangle=-|110\rangle$ and
  $c_2^\dagger c_0^\dagger|0\rangle=-|101\rangle$, so $c_j^\dagger$ carries the sign $(-1)^{n_0+\dots+n_{j-1}}$. These
  are the Jordan-Wigner matrices, and they satisfy (1.1) and (1.3) exactly.
- The sign matters in the Fock space. The hop $c_0^\dagger c_2$ has the matrix element $-1$ across an occupied site 1
  and $+1$ across an empty one. On a triangle with the hopping $-t$, two fermions have $-t$, $-t$ and $2t$, which are
  the sums of two of the single-particle levels $-2t$, $t$ and $t$. Two hard-core bosons, the same matrices without
  the sign, have $-2t$, $t$ and $t$ instead.
- The Hamiltonian (1.5) commutes with the number of particles, checked with random $t_{ij}$ and $V_{ijkl}$, so its
  matrix splits into blocks of fixed $N$. Three spinless sites have $2^3=8$ states, 1, 3, 3 and 1 by particle number.
  Three spinful sites have $4^3=64=\sum_N\binom6N$ states for a $6\times6$ single-particle matrix, and
  $2^{20}=1\,048\,576$.
- With the $+t$ of (1.2) and $t>0$, one electron has $-t$ on the antisymmetric state $(1,-1)/\sqrt2$ and $+t$ on the
  symmetric one, as the caption of the two-site figure says. Two fermions have the energy 0, and two bosons have
  $-2t$, 0 and $2t$, from the Fock space with up to two bosons per site.

## The sign of the hopping

- (1.2) is written with $+t$, while (1.6), (1.7), (6.1) and the island of Section 1.10 use $-t$. pyqula puts $+1$
  between first neighbors, so its chain has the band $2\cos k$, and `tij=[-1.]` gives $-2\cos k$. The notebook
  writes $E_n=2t\cos k_n$ for this reason. On a bipartite lattice the two signs give the same levels and the same
  densities, and level $n$ of one sign is level $n$ of the other with the sign $(-1)^j$ on site $j$, checked on a
  chain of 30 sites. On the triangle, which is not bipartite, $-t$ gives $-2t,t,t$ and $+t$ gives $-t,-t,2t$.
- The lowest state of an open chain of 10 sites changes sign on all 9 bonds with the $+1$ of pyqula and on none with
  $-1$, and its weight is the box $2\sin^2(\pi j/(N+1))/(N+1)$ in both cases. So "the lowest state has no node"
  holds for the density, which the widget of Section 1.10 draws from pyqula, and for the wave function only with $-t$.
- The open chain of $N$ sites has the levels $-2t\cos(n\pi/(N+1))$, $n=1,\dots,N$, in the window from $-2t$ to $2t$.
  The spacing at the center is $4t\sin(\pi/(2(N+1)))$, which is $0.569t$ for $N=10$ and $0.0622t$ for $N=100$, close
  to $2\pi t/(N+1)$, 0.571 and 0.0622. pyqula gives these levels to $10^{-15}$ with
  `geometry.chain().get_supercell(N)` and `g.dimensionality = 0`, so this is an open chain and not a ring.

## The finite systems of the pages

- The hexagonal island of Section 1.10 is the union of the hexagons at most three steps from the central one, with
  $6\cdot4^2=96$ sites and the spectrum of `islands.get_geometry(name="honeycomb", n=4, nedges=6, rot=0)`. With $-t$
  its lowest level is not degenerate, has one sign on every site and is largest on the central hexagon. The mean
  distance of the density from the center is 2.87, 3.74 and 4.43 for the first, the second and the sixth level,
  counting a degenerate level once.
- The two chains of the quiz of Section 1.2, with the hoppings 1 and 2, have the bulk gap $2|t_1-t_2|=2$. With 20
  sites and the weak bond at both ends, two levels are at $|E|=1.5\cdot10^{-3}$ and the next at 1.11, and with the
  strong bond at the ends the lowest $|E|$ is 1.07.
- A chain with two sites per cell, the onsite energies $\pm m$ and the hopping $t$ has the bands
  $\pm\sqrt{m^2+(2t\sin q)^2}$, with $q$ the momentum per site measured from the zone edge, and the gap $2m$ at the
  edge. This is `h.add_sublattice_imbalance(m)` on `geometry.bichain()`, and the $m=0.6t$ of the filling figure of
  Section 1.2 gives the gap $1.2t$. The same chain gives the gap $2m$ of the figure of Section 1.1.

## The Hubbard term and its mean field

This section is written for Sessions 6 and 9 as well.

- The Hubbard term is $Un_\uparrow n_\downarrow$ on each site, with no shift by $1/2$, so $U$ is the energy of a doubly
  occupied site. $Uc_\uparrow^\dagger c_\uparrow c_\downarrow^\dagger c_\downarrow$ of (1.7) and (6.1) and
  $Uc_\uparrow^\dagger c_\downarrow^\dagger c_\downarrow c_\uparrow$ of (5.2) are the same operator. On the four states
  of a site it is exactly $\tfrac U4(n^2-m^2)$, the form of Section 9.5b, and $\tfrac U2n-\tfrac{2U}3\mathbf S^2$, the
  form of Section 6.3, with $n=n_\uparrow+n_\downarrow$, $m=n_\uparrow-n_\downarrow$ and
  $\mathbf S^2=\tfrac34(n-2n_\uparrow n_\downarrow)$.
- The Hartree decoupling is
  $Un_\uparrow n_\downarrow\to U(\langle n_\uparrow\rangle n_\downarrow+n_\uparrow\langle n_\downarrow\rangle-\langle n_\uparrow\rangle\langle n_\downarrow\rangle)$,
  which is exactly $\tfrac U2\langle n\rangle n-\tfrac U2m\,(n_\uparrow-n_\downarrow)-\tfrac U4(\langle n\rangle^2-m^2)$
  with $m=\langle n_\uparrow\rangle-\langle n_\downarrow\rangle$. So a spin $\sigma=\pm1$ feels
  $U\langle n_{-\sigma}\rangle=\tfrac U2(\langle n\rangle-\sigma m)$, its bands are
  $E(\mathbf k)+\tfrac U2\langle n\rangle-\sigma\tfrac U2m$, and the exchange splitting between the two spins is $Um$.
  These are the $E_\sigma(\mathbf k)$ of Section 6.6 with the constant $\tfrac U2\langle n\rangle$ left out. For a
  moment along $z$ the Fock term of $U$ needs $\langle c_\uparrow^\dagger c_\downarrow\rangle$, which is zero, so this
  is the whole mean field, and the dimer of pyqula along $z$ has $m_x=m_y=0$.
- The last term is the double counting. The mean-field energy is the sum of the filled levels minus
  $U\sum_i\langle n_{i\uparrow}\rangle\langle n_{i\downarrow}\rangle$, and it is $\langle H\rangle$ of the Slater
  determinant. On the dimer it is $-1.5t$ at $U=t$ and $-0.5t$ at $U=4t$, both from $\langle H\rangle$ in the Fock
  space and from the levels, while the levels alone give $-1.0t$ and 0. The exact energy at $U=4t$ is $-0.83t$, so
  mean field stays above it, as a variational method does. `return_total_energy=True` of pyqula gives this number,
  per cell.
- With the decoupling of the densities the splitting is $U|m|$ for a moment in any direction. The chain at $U=4t$
  with `filling=0.1` and `nk=50`, which is $n=0.2$ per site, the 20% filling of Section 6.4, ends with $|m|=0.2$ and
  the splitting $0.8t$ with the guess `"ferroZ"` along $z$ and with `"ferroX"` along $x$. With the default `nk=8` this
  filling holds 1.6 electrons on the mesh, so a script at $n=0.2$ takes an `nk` that is a multiple of 5. The Hartree
  decoupling of the rewritten form, $\mathbf S^2\approx2\langle\mathbf S\rangle\cdot\mathbf S-\langle\mathbf S\rangle^2$,
  gives only $\tfrac{2U}3m$, two thirds of it. So a page that uses $\mathbf S^2$ to show that no axis is preferred does
  not take the size of the field from there.
- The Stoner criterion (6.3) uses $D(E_F)$ per spin and per site, which is $g(\omega)$ of (2.16) for one site per cell
  and $\chi_0(0,0)$ of (9.4) at $T=0$. With the bands $E\mp\tfrac U2m$ the loop $m\to m'$ has the slope $UD(E_F)$ at
  $m=0$. The chain has $D(E_F)=1/(2\pi t\sin(\pi n/2))$, $0.159/t$ at half filling and $0.515/t$ at $n=0.2$, and the
  slope agrees with it to $10^{-3}$ at $U=t$. The half-filled square lattice at $T=0.1t$ has
  $-\int f'(E)D(E)\,dE=0.264/t$ on meshes of $240^2$ and $480^2$, the $D(E_F)\approx0.26/t$ of Section 9.5b.
  `get_dos` of pyqula counts both spins per cell, 0.318 for the spinful chain at $E=0$, so $D$ is half of it divided
  by the number of sites of the cell.
- The criterion gives the point where the paramagnet becomes unstable, and a first-order jump can come before it.
  The uniform state of the half-filled chain has $E(m)=-\frac{4t}\pi\cos\frac{\pi m}2+\frac U4(1-m^2)$ per site, the
  same as a mesh, with a negative quartic term. The fully polarized state is a solution from $U=4t$, where the two
  bands stop overlapping, and it is lower than the paramagnet from $U=16t/\pi=5.09t$, while the curvature at $m=0$
  changes sign only at $U=2\pi t=6.28t$, where $UD(E_F)=1$. At $U=5.5t$ the paramagnet is locally stable and $0.10t$
  above. At $n=0.2$ the full polarization is a solution from $1.91t$ and lower from $1.93t$, just below
  $1/D(E_F)=1.94t$. The semicircle of half width $2t$ of the widget of Section 6.6 has $D(E_F)=1/\pi t$ at its
  maximum, and its onset is continuous, with $m=0.03$ at $U=1.0001\pi t$ and 0.63 at $1.05\pi t$. So whether the
  moment grows continuously depends on the shape of $D$ close to $E_F$.

## The repulsion between neighbors and its mean field

- The repulsion of (1.6) is $V\sum_nn_nn_{n+1}$, each bond once. In Hartree site $n$ feels
  $V(\langle n_{n-1}\rangle+\langle n_{n+1}\rangle)$, and the double counting is
  $-V\sum_n\langle n_n\rangle\langle n_{n+1}\rangle$. On the ring of four sites with $V=3t$ and the guess 0.6 and 0.4
  the onsite energies are $2.4t$ and $3.6t$, and filling the two lowest levels gives 0.8218 and 0.1782, the 0.82 and
  0.18 of Figure 1.4. The closed form is $\tfrac34+\Delta/(4\sqrt{4t^2+\Delta^2})$ with $\Delta=V(0.6-0.4)$.
- In Hartree the charge density wave of (1.6) at half filling is the antiferromagnet of (1.7) with $U=2V$. The order
  parameter is $\delta n=\langle n_\text{even}\rangle-\langle n_\text{odd}\rangle$, between 0 and 1, the staggered
  potential is $\pm V\delta n$, and the gap is $2V\delta n$. So $\delta n$ is the $m$ of $U=2V$, 0.340, 0.769 and
  0.892 at $V=t$, $2t$ and $3t$, with the gap $5.35t$ at $3t$, and the charge density wave of the infinite chain has
  no threshold in mean field. pyqula gives the same with `compute_cross=False`.
- The rings of Figure 1.5 have eight sites. At $V=0$ the four electrons fill $-2t$, $-1.41t$ twice and one of the
  pair at 0, so the Fermi level is inside a degenerate pair. At $V=3t$ the charges are 0.946 and 0.054, with the gap
  $5.35t$.
- The Fock term of the same product is $-V\langle c_{n+1}^\dagger c_n\rangle c_n^\dagger c_{n+1}+\text{h.c.}$ with its
  own double counting, and it makes the hopping larger. The notes leave it out. The default call of pyqula keeps it,
  which gives the hopping 1.316, 1.570 and 1.725 on both bonds and $\delta n=0.168$, 0.513 and 0.704 at $V=t$, $2t$
  and $3t$, and $\delta n=0.962$ at $10t$, the same as a Hartree-Fock ring of 100 sites in real space, with the gap
  still $2V\delta n$. `compute_cross=False` gives Hartree alone. The spinful mean field refuses `compute_cross` with
  a `TypeError`, so with spin it is always Hartree-Fock.
- The exact chain (1.6) is the XXZ chain with $J_{xy}=2t$ and $J_z=V$, with $n=S_z+\tfrac12$, a field $-V/2$ on the
  two end sites, the term $VS_z^\text{tot}$, which is a constant at fixed $N$, and the constant $V(L-1)/4$. The spectra of an open chain of 8 sites agree to $10^{-13}$, and the total $\mathbf S^2$
  commutes with the XXZ part only at $V=2t$, the isotropic point. That the exact chain has a charge density wave only
  for $V>2t$ is the result for the XXZ chain, and it is not checked here by a number. So mean field gives the charge
  density wave for any $V>0$, and the exact chain only above $V=2t$.

## The order parameters

- $m$ of (1.8) and (6.2) is $n_\uparrow-n_\downarrow$, between $-1$ and 1, and $\langle S_z\rangle=m/2$.
  `get_vev("mz")` of pyqula is $m$. On the dimer at $U=9.8t$ it is $\mp0.979=\mp\sqrt{1-(2t/U)^2}$, where
  $\langle S_z\rangle$ would be 0.490, and with the guess `"antiferro"` it is negative on the first site.
- `extract("mz")` is not the moment. It is the exchange field $(H_{\uparrow\uparrow}-H_{\downarrow\downarrow})/2=-Um/2$
  of the mean-field Hamiltonian, $+0.931$ where $m=-0.621$ on the even sites of the chain at $U=3t$.
- Time reversal $i\sigma_yK$ sends $\sigma_x$, $\sigma_y$ and $\sigma_z$ to minus themselves, so it exchanges
  $n_\uparrow$ and $n_\downarrow$ and changes the sign of $m$. (1.7) is real, and it commutes with $S_z$ and with the
  time reversal for $U=4t$ and $U=-4t$, checked on a ring of three sites.
- $\Delta$ of (1.9) is the number $\langle c_ic_j\rangle$, and the order of the operators fixes its sign,
  $\langle c_\downarrow c_\uparrow\rangle=-\langle c_\uparrow c_\downarrow\rangle$. (5.3) defines
  $\Delta_n=U\langle c_{n\downarrow}c_{n\uparrow}\rangle$, an energy, and the gap $2\Delta$ of the figure of Section 1.1
  and of (5.9) is that energy. On the half-filled chain at $U=-3t$ the gap equation gives $|\Delta|=0.931$ and
  $|\langle c_\downarrow c_\uparrow\rangle|=0.310$, `extract("swave")` of pyqula has the modulus 0.931, and the
  Bogoliubov-de Gennes (BdG) bands have the gap $2|\Delta|=1.862$. This sheet checks only the modulus, and the sign of
  the pairing of pyqula against (5.3) is on the sheet of Session 5.
- The gauge transformation (1.10) is the operator identity $e^{-i\varphi N}c\,e^{i\varphi N}=e^{i\varphi}c$. Then
  $c^\dagger c$ does not change, $c_ic_j$ gets $e^{2i\varphi}$, and $c_i^\dagger c_j^\dagger$ gets $e^{-2i\varphi}$,
  which is the sign of (5.5). For $\varphi=\pi/2$ the pair gets $-1$.
- A pairing term keeps the parity $(-1)^N$ and not $N$. On one site, $-0.3n+0.8(c_\uparrow^\dagger c_\downarrow^\dagger+\text{h.c.})$
  has an even ground state, and $N$ has the variance 0.877 in it.

## The models of the pages

- The Hubbard dimer at half filling in mean field, with the antiferromagnetic guess, has $m=0$ up to $U=2t$ and
  $m=\sqrt{1-4t^2/U^2}$ above, 0.305, 0.745, 0.866 and 0.968 at $U=2.1t$, $3t$, $4t$ and $8t$. Its energy is $-2t+U/2$
  up to $2t$ and exactly $-2t^2/U$ above, for every $U>2t$ and not only at large $U$, and its gap is $\max(2t,U)$. A
  numpy loop gives these forms to $10^{-12}$, and pyqula to $10^{-4}$ in the energy and to $10^{-3}$ in $m$ and in
  the gap, which is the tolerance of its loop next to $U=2t$.
- The exact dimer has $E_0=U/2-\sqrt{U^2/4+4t^2}$, $-0.828t$ at $U=4t$ and $-0.0998t$ at $U=40t$, which is 0.998
  times $-4t^2/U$, while mean field gains only $-2t^2/U$. Its ground state is the singlet, with $m=0$ for every $U$. A
  staggered field $h$ at $U=4t$ gives $m=4.12h$, which goes to zero with $h$, while mean field keeps $m=0.866$.
- The half-filled Hubbard chain in Hartree has the antiferromagnet for every $U>0$, with no threshold. The moment is
  0.0299, 0.340, 0.621, 0.769, 0.892, 0.939 and 0.984 at $U=t$, $2t$, $3t$, $4t$, $6t$, $8t$ and $16t$, from the gap
  equation $1=\frac U2\cdot\frac1\pi\int_{-\pi/2}^{\pi/2}dk/\sqrt{\Delta^2+4t^2\cos^2k}$ with $\Delta=Um/2$, written
  with the elliptic integral, and from a mesh of 20000 cells. At small $U$, $m\approx(16t/U)e^{-2\pi t/U}$, 0.0299 at
  $U=t$. The gap is $2\Delta=Um$, $1.862t$ at $U=3t$, so it approaches $U$. A ring of 120 sites and pyqula give
  $|m|=0.6206$ at $U=3t$. The 0.77 at $U=4t$ of Sections 6.4 and 6.7 and the 0.98 at $U=16t$ of Section 6.7 are
  these numbers.
- The half-filled honeycomb lattice in Hartree has the antiferromagnet only above $U_c=2/\langle1/|f_\mathbf k|\rangle=2.23t$,
  with $f_\mathbf k=1+e^{ik_1}+e^{ik_2}$, from midpoint meshes of $600^2$ and $1200^2$, which give 2.2329 and 2.2320,
  and 2.231 extrapolated. At $U=3t$ pyqula with `nk=20` and a numpy loop on the same mesh give $m=0.444$, and the gap
  is $Um=1.33t$, at $K$.
- The antiferromagnet is the lowest state of the half-filled chain. Per cell of two sites it has $-2.047t$,
  $-1.190t$, $-0.648t$ and $-0.396t$ at $U=t$, $3t$, $6t$ and $10t$, against the paramagnet $2(-4t/\pi+U/4)$, which
  is $-2.046t$, $-1.046t$, $0.454t$ and $2.454t$, and the full ferromagnet, which is 0 where it exists. pyqula gives
  $-0.648t$ at $U=6t$.
- At half filling the attractive chain has a charge density wave and an s-wave state with the same gap, which is the
  gap of the antiferromagnet of the repulsive chain. At $U=-3t$ the Hartree map of $m$ has the opposite sign of $m$
  everywhere, so $m=0$ is its only fixed point. The charge density wave has the charges 0.379 and 1.621 in pyqula
  with the gap $1.862t$, and the s-wave state has $2|\Delta|=1.862t$, the gap $Um$ of the antiferromagnet at
  $U=+3t$. That the s-wave state wins away from half filling is not checked here.
- For $U>0$ the gap equation of the pairing is $\Delta=-UF(\Delta)$, with $F=\langle\Delta/2E\rangle$ of the sign of
  $\Delta$. Its right side has the opposite sign of $\Delta$ for every $\Delta\neq0$, checked from $-1$ to 1 at
  $U=3t$, so $\Delta=0$ is the only solution.
- A seed only picks one of the ordered states. On the dimer a loop started exactly at $m=0$ stays there. At $U=4t$
  the seeds $+10^{-3}$ and $-10^{-3}$ end at $+0.866$ and $-0.866$ with the same energy $-0.5t$. At $U=t$ the seed
  dies, and at $U=-4t$ a seed 0.5 ends at $m=0$. A staggered field $b=10^{-3}$ that stays in the Hamiltonian gives
  $|m|=b/(1-U/2t)=0.002$ at $U=t$, which goes to zero with $b$, and 0.866 at $U=4t$. pyqula gives the same with
  `h.add_antiferromagnetism(b)`.
- The open quantum Ising chain $H=-J\sum_i\sigma^z_i\sigma^z_{i+1}-g\sum_i\sigma^x_i$ has an even ground state under
  the flip of all spins, and the splitting of its two lowest states is $\Delta=2J(1-(g/J)^2)(g/J)^L$ to
  $3\cdot10^{-4}$ for $L=8$ and 12 at $g=0.3J$ and $0.5J$. So "roughly as $(g/J)^L$" of Section 1.11 holds. Exact
  diagonalization and the free fermions of the chain agree on the splitting.
- The double well of the quiz of Section 1.11, $-\psi''+8(x^2-1)^2\psi$ with $\hbar^2/2m=1$, has $2\Delta=0.925$ on
  grids of 1200 and 2400 points, the 0.92 of the quiz.

## pyqula

- `geometry.bichain()` has two sites per cell and the hopping $+1$, and `g.get_hamiltonian()` is spinful by default.
  The dimer of the notebook, with `g.dimensionality = 0`, has the levels $-1,-1,1,1$, and $-1,1$ with
  `has_spin=False`, and `h.get_gap()` is 2 at $U=0$.
- `h.get_mean_field_hamiltonian(U=..., V1=..., mf=..., mix=..., nk=..., filling=...)` takes the $U$ of (1.7) and the
  $V$ of (1.6) per bond. The onsite part of the Hamiltonian that it returns is
  $\tfrac U2\langle n_i\rangle-\sigma Um_i/2$ plus one constant, which puts the middle of the gap between the last
  filled and the first empty level at zero energy. On the dimer both sites hold one electron, so only $-\sigma Um_i/2$
  is left. On the charge density wave of the attractive chain at $U=-3t$ the two sites differ by
  $\tfrac U2(\langle n_0\rangle-\langle n_1\rangle)=1.862t$, and the Kohn-Sham toy of the sheet of Session 10, 40
  electrons on 60 sites at `U=4`, has $v_\text{ext}+2n_i$ plus the constant 0.048.
  `filling` is the fraction of all the single-particle states that are filled, so the default 0.5 is half filling,
  one electron per site with spin and one per cell of two sites without, and `filling=0.1` is $n=0.2$ per site with
  spin. `return_total_energy=True` also returns the energy per cell with the double counting. In the development
  tree a loop that does not converge in `maxite` steps raises `MeanFieldConvergenceError`. The release 0.0.96 prints
  "No convergence has been reached" and returns `None` in place of the Hamiltonian, and `(None, energy)` with
  `return_total_energy=True`, with spin and without. This was read in its code and run once with `maxite=2` apart from
  the check, as the sheet of Session 10 says.
- The loop runs on its own mesh, `nk=8` cells by default, which holds $k=0$ and the zone edge, while `get_vev` sums on
  a mesh of its own, 30 cells when it gets no `nk`. In a large gap this does not matter, and near a small gap it
  does. On the half-filled chain at $U=t$ the loop on 8 cells converges to $m=0.192$, `get_vev("mz")` with no `nk`
  reads 0.138 from the same Hamiltonian, and the converged value is 0.0299. At $U=2t$ the three are 0.367, 0.358 and
  0.340, and at $U=3t$ they are 0.6210, 0.6208 and 0.6206. The Hartree charge density wave at $V=t$ is the case
  $U=2t$, 0.367 and 0.358, and with the Fock term it is 0.263 and 0.235, against the converged 0.168. A page quotes a
  moment at small $U$ from the gap equation, and a script passes the same `nk` to the loop and to `get_vev`.
- The cell "Symmetry breaking in the spinless fermionic chain" with `cdw=0.1` prints 0.1417 at $V=0$, the sum of
  `get_vev` on 30 cells, where 8 cells give 0.1948 and the converged value is
  $\Delta\cdot\frac1\pi\int_{-\pi/2}^{\pi/2}dk/\sqrt{\Delta^2+4t^2\cos^2k}=0.1394$ with $\Delta=0.1$. The imbalance
  goes to zero with the seed, 0.0213 and 0.0029 for 0.01 and 0.001.
- `mf="ferro"` adds the onsite energies $+0.1$ to the spin up and $-0.1$ to the spin down of every site. `mf="antiferro"`
  is `h.add_antiferromagnetism(0.1)`, which adds $+0.1$ to the spin up and $-0.1$ to the spin down of the first site
  and the opposite on the second. `mf="CDW"` adds the sublattice index, $\pm1$, to the onsite energies, so it is a
  strong seed and not an unbiased start. With `mf=None` the spinless loop starts from the file `MF.pkl` that the last
  call left in the folder, when its shape matches, and from a random guess otherwise, as its source says, so a script
  always gives `mf`.
- The ferromagnetic guess of the notebook does not give a ferromagnet. On the half-filled chain at $U=6t$ with the
  default `nk=8` it ends at $m=1/8$, one k-point of eight, with the field $U/16=0.375$, no gap and the energy $0.439t$
  per cell, against the paramagnet $0.454t$ of the infinite chain and the antiferromagnet $-0.648t$. `get_vev("mz")`
  reads 0.100 on its 30 cells. The arrows of the cell "Magnetic order driven by interactions in a chain" are divided
  by their largest value, so they are all equal and the panel looks like a ferromagnet. The commented line of the
  cell "Gap opening of the Hubbard model in a chain" gives the largest gap $2\cdot10^{-15}$ for its 40 values of $U$,
  so "the gap stays closed" of Section 1.12 holds for `nk=8`. A strong seed,
  `mf=meanfield.guess(h, "ferro", fun=3.0)`, gives the fully polarized state at $U=6t$, with $m=1$, the gap $U-4t=2t$
  and the energy 0, and at $U=3t$ it falls back to $|m|=0.025$, since the full polarization is a solution only from
  $4t$.
- On the honeycomb lattice the mesh decides the onset. The $10\times10$ mesh of the notebook, which does not hold $K$,
  moves it to $2.375t$, and a $20\times20$ mesh to $2.290t$. pyqula with `nk=10` and `mix=0.9` gives $|m|=10^{-3}$ at
  $U=2.3t$ and 0.085 at $2.4t$, where the converged loop on that mesh gives 0.086, since the default tolerance stops
  the loop early next to the onset. A mesh with `nk` a multiple of 3 holds $K$, and its Dirac points give a moment
  below $U_c$, 0.015 at $U=2t$ with `nk=30`. A page quotes the threshold $2.23t$ of the dense mesh.
- The spinless mean field writes `MF.pkl` in the folder where it runs, and `get_bands` and `get_dos` write
  `BANDS.OUT` and `DOS.OUT`. With `write=False` they write nothing, and the spinful mean field writes no file. A
  figure script runs pyqula inside `style.run_script` or passes `write=False`.
- In the cell "The interacting Hubbard dimer", with `Us = np.linspace(0.,10.,50)` and `mix=0.9`, the magnetization
  leaves zero at the point $U=2.04t$ with $|m|=0.198$, after $4\cdot10^{-4}$ at $U=1.84t$. At $U=1.9t$ the loop leaves
  $8\cdot10^{-4}$, which is its tolerance next to the threshold and not a moment.

## Open points of the old text, left as they are

- Section 1.14 says that self-consistency gives "a finite $m$ for $U>0$". This holds for the half-filled chain,
  which has $m=0.0299$ at $U=t$, and not in general. The dimer needs $U>2t$ and the honeycomb lattice $U>2.23t$.
  Section 6.3 repeats the sentence.
- Section 1.14 says that an attractive $U$ "drives superconductivity". At half filling the charge density wave of the
  attractive chain has the same mean-field gap as the s-wave state, $1.862t$ at $U=-3t$.
- The notebook box of Section 1.14 says that the honeycomb challenge "uses the finite islands of Section 1.10". The
  cell uses the periodic `geometry.honeycomb_lattice()` with `nk=10`.
- The notebook box of Section 1.13 says "Start from an unbiased guess", and the cell passes `mf="CDW"`, the onsite
  energies $\pm1$.
- Section 1.13 says that the interaction "becomes a single-particle onsite energy", and the text of the cell
  "Symmetry breaking in the spinless fermionic chain" writes the Hartree decoupling, while the cell calls the default
  of pyqula, which keeps the Fock term. At $V=3t$ the cell gives 0.704, where the Hartree decoupling of the text and
  of Figure 1.5 gives 0.892.
- The tryit box of Section 1.11b calls the arrows of the cell "Magnetic order driven by interactions in a chain" "the
  arrows of the magnetization". They are drawn from `extract("mz")`, the field $-Um/2$, so each arrow points against
  the moment of its site. They alternate, as the box says.
- The cell "Magnetic order driven by interactions in a chain" defines
  $\langle S_z\rangle=\tfrac12(\langle n_\uparrow\rangle-\langle n_\downarrow\rangle)$, and the cell "The interacting
  Hubbard dimer" plots `get_vev("mz")`, which is $n_\uparrow-n_\downarrow$, with the label $\langle S_z\rangle$. So the
  label is a factor 2 off, and the curve saturates at 1, as the $m$ of (1.8) does.
- The cell "Gap opening of the Hubbard model in a chain" says that the even sites have a positive magnetization, and
  `get_vev("mz")` with the guess `"antiferro"` is $-0.621$ there. The opposite pattern has the same energy.
- (1.9) defines $\Delta$ as the number $\langle c_ic_j\rangle$, while the figure of Section 1.1 and (5.3) use $\Delta$ as
  an energy, larger by the factor $|U|$, which is 3 in the example above.
- Section 6.6 says that the magnetization of the chain "stays at zero below a critical $U$, and it grows continuously"
  above it, and Section 6.5 says that the uniform solution is "the paramagnet below $U\approx 4t$ and a fully
  polarized ferromagnet above it". In the half-filled chain the antiferromagnet has no threshold. The full
  polarization is a solution from $4t$, the lowest uniform state jumps from $m=0$ to $m=1$ only at $5.09t$, and
  $UD(E_F)=1$ is at $6.28t$.
- Section 6.3 writes $\mathbf m\equiv\langle\mathbf S\rangle$, and its quiz takes $m_x=1/2$ for the spinor
  $(1,1)/\sqrt2$, while (6.2) defines $m=n_\uparrow-n_\downarrow$, which is $2\langle S_z\rangle$. It also takes the
  exchange field from $\mathbf S^2\approx2\langle\mathbf S\rangle\cdot\mathbf S-\langle\mathbf S\rangle^2$, which gives
  $\tfrac23$ of the splitting $Um$ of the decoupling of the densities.
