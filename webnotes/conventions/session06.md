# Conventions of Session 6, checked by number

This sheet fixes the signs, the units and the pyqula facts that the pages, the figures and the pyqula scripts of
Session 6 use. Sessions 1, 8 and 9 take the mean-field decoupling, the Stoner criterion, the exchange $J$ and the
magnon bands from it. An agent that edits the session reads it first and does not work these out again. Every bullet
was checked with a number on 2026-11-21. Two drafts were written apart, and a third calculation settled each line
where they differed or where only one of them had it. The energies are in units of the hopping $t$. The notes write
the hopping as $-t$, and pyqula takes it as $+1$. A moment is $m=n_\uparrow-n_\downarrow$ of one site. A number of a
self-consistent loop is given with the k-mesh and the seed it holds for, or as a range over them. The pyqula of the
checks is the development tree of version 0.0.95, at commit 7567127, and the release 0.0.96 that the students install
was not run for these lines, except for the loop that does not converge, which is on the sheet of Session 1. A
statement that is not on this sheet is checked before a page claims it. The check is
`webnotes/checks/session06/conventions.py`, which prints one line per bullet below, in the same order.

## The magnetization and the Hubbard term

- The $m$ of (1.8) and (6.2) is $n_\uparrow-n_\downarrow=2\langle S^z\rangle$ of one site, so it saturates at 1, one
  Bohr magneton. The bold $\mathbf m\equiv\langle\mathbf S\rangle$ of Section 6.3 and of its quiz is half of it. The
  spinor $(1,1)/\sqrt2$ has $n_\uparrow-n_\downarrow=0$ and $\langle S^x\rangle=1/2$, and a page that uses both says
  which one it means.
- On the four states of one site $Un_\uparrow n_\downarrow=\tfrac U2n-\tfrac{2U}{3}\mathbf S^2=\tfrac U4(n^2-m^2)$
  holds as an operator identity, with $\mathbf S^2=\tfrac34(n-2n_\uparrow n_\downarrow)$. The first form is the one of
  Section 6.3, and the last one is the one of Section 9.5b.
- The Hartree decoupling is $Un_\uparrow n_\downarrow\approx U\langle n_\downarrow\rangle n_\uparrow+U\langle
  n_\uparrow\rangle n_\downarrow-U\langle n_\uparrow\rangle\langle n_\downarrow\rangle$. So the bands are
  $E_\sigma=\varepsilon_{\mathbf k}+Un/2-\sigma Um/2$, the coefficient of $\sigma_z$ is $-Um/2$, and the exchange
  splitting is $Um$. With the Fock terms the field is $-\tfrac U2\mathbf m\cdot\boldsymbol\sigma$ in every direction,
  a splitting of $0.2U$ for $m=0.2$ along $z$ and along $x$. The decoupling
  $\mathbf S^2\approx2\langle\mathbf S\rangle\cdot\mathbf S-\langle\mathbf S\rangle^2$ of Section 6.3 gives
  $\tfrac23Um$, two thirds of it, so a page uses that route for the direction of the field and not for its size.
- `mf="XY"` gives the same magnet in the plane. The half-filled bichain at $U=4t$ has $|m|=0.7690$ with
  `mf="antiferro"` along $z$ and with `mf="XY"` in the plane, the same gap 3.076 and energies within $2\cdot10^{-5}$
  per cell, which is the rotation invariance of Section 6.3.

## The half-filled chain in mean field

- The antiferromagnet has $1=\tfrac U2\langle1/E_k\rangle$, with $E_k=\sqrt{\varepsilon_k^2+\Delta^2}$ and
  $\Delta=Um/2$, and it exists for every $U>0$, since the two Fermi points are nested. It gives $m=0.0299$, 0.3404,
  0.7690 and 0.9844 at $U$ equal to $t$, $2t$, $4t$ and $16t$, and the energy $-0.46911$ per site at $4t$. At small $U$
  the field is $\Delta\approx8t\,e^{-2\pi t/U}$, 0.0149 at $U=t$. pyqula gives 0.0302 at $U=t$ with `nk=1001`, 0.3404 at
  $2t$ with `nk=200`, and at $4t$ the gap of its bands is $3.076=Um$. In mean field the double occupancy is
  $4\langle n_\uparrow n_\downarrow\rangle=1-m^2$, 0.409 at $4t$.
- The uniform states are the paramagnet, with $-4t/\pi+U/4$ per site, and the saturated ferromagnet, with zero energy.
  The saturated state is self-consistent only from $U=4t$, where the two spin bands stop overlapping. It is the lower
  of the two only above $U=16t/\pi=5.09t$, and the paramagnet is unstable only above $U=2\pi t=6.28t$. The
  antiferromagnet is below both at $U$ equal to $t$, $3t$, $4.5t$, $6t$, $10t$ and $20t$. pyqula started from the field
  of the saturated state, a copy of the Hamiltonian with `clean()` and `add_zeeman`, stays there with $|m|=1.000$ and
  zero energy at $4.1t$ and $4.5t$, and goes back to the paramagnet, $|m|=0.025$, at $3.9t$.
- $E_\text{FM}-E_\text{AFM}$ per cell of two sites is 0.1995 at $U=20t$ and 0.0999 at $U=40t$, in pyqula and in numpy,
  and $U$ times it is 3.990 and 3.998. So it is $J=4t^2/U$ per cell and $J/2$ per bond, which is $2JS^2$ for $S=1/2$,
  the classical Néel state below the ferromagnet. This is the $1/U$ law of Section 6.5 and the "one half of the
  exchange coupling" of Section 6.8.
- The mean-field dimer, the cell "The interacting Hubbard dimer" of the notebooks of Sessions 1 and 6, has its
  threshold at $U=2t$. Below it the moment is zero and the gap is $2t$, and above it $m=\sqrt{1-4t^2/U^2}$ and the gap
  is $U$. pyqula gives less than 0.001 at $1.8t$ and $1.9t$, then 0.305 at $2.1t$, 0.4165 at $2.2t$, 0.600 at $2.5t$,
  0.866 at $4t$ and 0.980 at $10t$. The exact dimer has no moment, since its ground state is the singlet, with
  $\mathbf S^2=0$.

## pyqula in mean field

- `hmf.get_vev("mz")` is $n_\uparrow-n_\downarrow$ of each site, $\mp0.7690$ for the antiferromagnet of the bichain at
  $U=4t$, and the same as `get_vev("up")` minus `get_vev("dn")`. It sums over a mesh of its own, 30 k-points by
  default, and not over the `nk` of the loop. At $U=t$, where the gap is 0.03, it reads 0.0503 without `nk` for the
  moment 0.0302 of a loop with `nk=1001`, so a script passes `nk`. The cell "Intermediate coupling regime and Stoner
  instability" of the notebook reads it without `nk`, so its titles show 0.13 at $U=1.8t$, where the mesh of the
  loop gives 0.087.
- `hmf.extract("mz")` is the coefficient of $\sigma_z$ in the onsite mean field, $-Um/2$, so it has the sign opposite
  to the moment, $+1.538$ where $m=-0.769$ at $U=4t$. The notebook plots `extract("mz")` in the cells of the chain, of
  the Lieb lattice and of the square lattice, so those maps show the field, with the sign of the moment reversed. It
  calls `get_vev("mz")` $\langle S_z\rangle$, which is twice $\langle S_z\rangle$ and saturates at 1.
- `filling` is the fraction of all the states, with the two spins, that are filled. `filling=0.1` is $n=0.2$ electrons
  and 0.1 spin up per site in the paramagnet, 0.25 is $n=0.5$, and the default 0.5 is half filling. The guess
  `mf="ferro"` is the field $+0.1\,\sigma_z$ on every site, so the majority spin is down, $m=-0.200$ at $n=0.2$ and $U=3t$, and
  $-1.000$ at half filling and $U=20t$. A page gives $|m|$.
- `geometry.chain()` has the hopping $+1$, so its band is $+2t\cos2\pi k$ with $k$ in units of $2\pi$, $+2$ at $k=0$
  and $-2$ at $k=0.5$. It is the band $-2t\cos k$ of the notes moved by $\pi$, so no energy changes. The mean-field
  Hamiltonian is shifted so that the Fermi level is at zero energy, and the ferromagnet with $n=0.2$ has its filled
  band from $-0.382=-(2t-2t\cos\pi n)$ to 0. In the frame of the notes the same band starts at $-2t$, the Fermi level
  is $-2t\cos\pi n=-1.618$, and at $U=4t$ the empty band starts at $-2t+Um=-1.2$.
- `return_total_energy=True` gives the energy per unit cell, $\langle H_\text{kin}\rangle+U\sum_i\big(\langle
  n_{i\uparrow}\rangle\langle n_{i\downarrow}\rangle-|\langle c^\dagger_{i\uparrow}c_{i\downarrow}\rangle|^2\big)$. The
  bichain gives $-8/\pi=-2.546$ at $U=0$ and $-0.93819$ at $U=4t$, twice the $-0.46911$ of numpy. The second term
  in the bracket is tested on the Rashba chain below, where it is nonzero.
- At the default temperature, $10^{-7}$, the occupations of a k-mesh change by whole k-points, so a loop can stop at
  a moment of a few k-points that is not the lowest state. At half filling the guess `mf="ferro"` with the default
  `nk=8` stays at $|m|=1/8$ at $U$ equal to $6t$, $9t$ and $12t$, with the energies 0.44, 1.92 and 3.39 per cell, above
  the zero of the saturated ferromagnet, and it reaches the saturated state at $U=20t$, the range of the cell "The
  strongly interacting limit". The ferro guess of the cell "Magnetic order driven by interactions in a chain", at
  $U=6t$ and with no `mix`, gives the same $|m|=1/8$. With `nk=51` it stops at $2/51$ at $6t$ and $9t$ and saturates
  at $10t$. A moment is quoted only when it holds for an odd and an even `nk`, and the energies of the guesses are
  compared.
- `geometry.square_lattice_bipartite()` has four sites per cell. At $U=3t$ the energy of the ferro guess minus the
  antiferro guess is 0.296, 0.298 and 0.300 per cell for `nk` 8, 12 and 21, and numpy gives
  $E_\text{PM}-E_\text{AFM}=0.302$ per four sites, with $|m|=0.566$ and the energy $-3.7864$ per cell. pyqula has
  $|m|=0.566$ on every site, with opposite directions on the two sublattices, but the whole pattern is turned away from
  $z$, so $m_z$ is $\pm0.21$ with the default `nk=8`, equal on the four sites with alternating sign. The ferro guess
  ends close to the paramagnet, with $|m|$ below 0.15. A moment is read from its three components, and the try-it box
  of Section 6.10 holds as written, with "about 0.3 lower" per cell of four sites.
- The Lieb lattice has a band at zero energy that is flat to $10^{-12}$. With `mf="ferro"` at half filling the total
  moment is $-1.000$ per cell at $U$ equal to $0.3t$, $t$ and $2t$, with the sign of the guess. At $U=t$ and the default
  `nk` the two sites with two neighbors have $-0.551$ each and the site with four neighbors $+0.102$, so the state is a
  ferrimagnet. The moments of the sites change by less than 0.003 between the default `nk`, 12 and 24, and the total
  does not change.

## The Stoner criterion

- The $D(E_F)$ of (6.3) is the density of states per spin and per site, which is the $g(\omega)$ of (2.16) at
  $\omega=E_F$ and the $\chi_0(0,0)$ of (9.4), since (9.4) sums over $k$ and not over the spin. This is what $m\approx
  UmD(E_F)$ gives with the bands $\varepsilon\mp Um/2$, and with the density of both spins the criterion reads
  $UD/2\geq1$. For the chain at density $n$ we have $D(E_F)=1/(2\pi t\sin k_F)$ with $k_F=\pi n/2$, so the threshold is
  $U_c=2\pi t\sin(\pi n/2)$. It is $6.283t$ at half filling, $1.942t$ at $n=0.2$, $0.983t$ at $n=0.1$ and $3.693t$ at
  $n=0.4$, the last two at the fillings 0.05 and 0.2 of the quiz of the notebook. The energy $E(m)$ of the uniform
  state bends down at $m=0$ at these values, and (9.4) at a small $q$ gives $1/2\pi t=0.1592/t$ at half filling.
- `h.get_dos()` counts both spins with the spinful Hamiltonian. For the chain with `delta=0.02` and `nk=2000` it
  integrates to 1.989 per site between $-3t$ and $3t$, and at $E_F=-1.902$ of $n=0.2$ it gives 1.015, close to
  $2D(E_F)=1.030$, since the band edge is only $0.1t$ away. With `has_spin=False` it gives half, 0.507 there, and 0.5145
  with `delta=0.005` and `nk=20000`, against $D(E_F)=0.5150$.
- The chain at $U=4t$ with `filling=0.1`, $n=0.2$, is a saturated ferromagnet with $|m|=0.200$ and the splitting
  $Um=0.800$, the values of the caption of Section 6.4. With `filling=0.2`, $n=0.4$, it is saturated too, with
  $|m|=0.400$ and the splitting 1.600, both with `nk=1000`. With `nk=300` the loop at `filling=0.2` stops at
  $|m|=0.060$, 0.017 per site above the saturated energy.
- The uniform state of the chain does not magnetize continuously. Its energy above the paramagnet is
  $\tfrac{4t}{\pi}\sin\tfrac{\pi n}2\big(1-\cos\tfrac{\pi m}2\big)-\tfrac U4m^2$ for $m$ up to $\min(n,2-n)$, and
  $(1-\cos x)/x^2$ decreases, so the lowest state is $m=0$ or the saturated one, at every filling. At $n=0.2$ the
  saturated state is self-consistent from $1.910t$, the two energies cross at $1.926t$, and the paramagnet is unstable
  at $1.942t$, so $m$ jumps from 0 to 0.2 at $1.926t$. pyqula with the call of the notebook (`filling=0.1`,
  `mf="ferro"`, `nk=300`) gives less than 0.015 at $1.2t$ for `nk` 300, 301 and 1000, and 0.200 at $2.4t$ and $3t$ for
  `nk` 300 and 1000, while between $1.8t$ and $2t$ it stops at moments from 0.026 to 0.2 that change with `nk`. A page
  quotes the two sides of the jump.
- The widget of Section 6.6 has a semicircular density of states of half-bandwidth $2t$, with $D(E_F)=1/\pi t=0.3183/t$
  and the threshold $U=\pi t$. Its density of states has the maximum at $E_F$, so there $m$ grows continuously, with
  $m^2\approx(96t^2/U^2)(1-\pi t/U)$ to leading order. It gives 0.155 and 0.306 at $1.0025\pi t$ and $1.01\pi t$, then
  0.41 at $3.2t$, and 1 from $U=4t$. The rise is steep but has no jump.
- Section 9.5b quotes the half-filled square lattice at $T=0.1t$. On a mesh of $240\times240$, (9.4) gives
  $\chi_0(0,0)=0.264/t$, the density of states per spin averaged over $-\partial f/\partial\varepsilon$, with the
  threshold $U=3.79t$, and $\chi_0(\pi,\pi)=0.677/t$, with the threshold $1.48t$. These are its 0.26, 3.8, 0.68 and 1.5.

## The Hubbard dimer and the Heisenberg model

- The dimer at half filling has the six levels $E_S=U/2-\sqrt{U^2/4+4t^2}$, three triplet levels at 0, then $U$ and
  $U/2+\sqrt{U^2/4+4t^2}$. The ratio $(E_T-E_S)/(4t^2/U)$ is 0.8284, 0.9443 and 0.9848 at $U/t$ equal to 4, 8 and 16.
  Numpy for $t$ and for $-t$, and dmrgpy, agree with the closed form, so the dimer gives $J>0$ for either sign of $t$.
  With $|\!\uparrow,\downarrow\rangle=c^\dagger_{0\uparrow}c^\dagger_{1\downarrow}|0\rangle$ and
  $|\!\uparrow\downarrow,0\rangle=c^\dagger_{0\uparrow}c^\dagger_{0\downarrow}|0\rangle$, the matrix element of Section
  6.8 is $\langle D|H_t|S\rangle=-2t$, and $H_t$ gives zero on the triplet.
- The Heisenberg coupling of (6.4), (6.5) and (8.2) is $H=J\sum_{\langle ij\rangle}\mathbf S_i\cdot\mathbf S_j$, with
  each bond once and $\mathbf S=\boldsymbol\sigma/2$, and $J>0$ is antiferromagnetic. The dimer has $-3J/4$ for the
  singlet and $+J/4$ for the triplet, in numpy and in dmrgpy, which is $(J/4)\,\boldsymbol\sigma_0\cdot
  \boldsymbol\sigma_1$, and (8.2) is this with $J=1$. Section 10.6 writes the Ising model with the opposite sign.
- The open Heisenberg chain of four sites has the excitation energies 0.659, 1.366, 1.732, 2.073 and 2.366 in units of
  $J$, in dmrgpy and numpy. The 16 lowest levels of the half-filled open Hubbard chain of four sites, divided by
  $4t^2/U$, are within 4.7 percent of them at $U=10t$ and within 0.55 percent at $U=30t$.

## Classical spins and the noncollinear mean field

- Three classical spins on a triangle with $J>0$ have the minimum $-\tfrac32JS^2$, at $120^\circ$ with $\mathbf
  S_i\cdot\mathbf S_j=-S^2/2$ on each bond, from a minimization over all directions, and the best collinear state has
  $-JS^2$.
- The chain $\sum_i\big[J\,\mathbf S_i\cdot\mathbf S_{i+1}+D\,\hat z\cdot(\mathbf S_i\times\mathbf S_{i+1})\big]$, with
  $D$ an energy like $J$, has its spins in the plane normal to $\hat z$ with $\cos\theta=-J/\sqrt{J^2+D^2}$ between
  neighbors. A minimization of an open chain of 30 spins gives $180.0^\circ$, $135.0^\circ$ and $101.3^\circ$ for $D$
  equal to 0, $J$ and $5J$, $135.0^\circ$ also for $J=2$ and $D=2$, and the energy $-S^2\sqrt{J^2+D^2}$ per bond. For
  $D>0$ the cross product $\hat z\cdot(\mathbf S_i\times\mathbf S_{i+1})$ is negative, $-0.707$ at $D=J$, so the spin
  turns clockwise seen from $+z$.
- `h.add_rashba(1.)` on the chain makes the bond $1+i\sigma_y=\sqrt2\,e^{i\pi\sigma_y/4}$, the hopping $\sqrt2$ times
  a rotation of the spin by $90^\circ$ about $y$. A rotation of site $j$ by $j\cdot90^\circ$ about $y$ turns the open
  chain of 10 sites of the notebook into the plain chain with hopping $\sqrt2$, exactly, and the Hubbard term does not
  change. So the mean field has one energy for every direction of the staggered moment, and the angle between
  neighbors is $\arccos(-n_y^2)$, with $n_y$ the component of the unit moment along $y$, anywhere from $90^\circ$ to
  $180^\circ$. The Hartree-Fock code of the check, written apart from pyqula, gives $-3.535751$ at $U=10t$ for three
  random seeds, with angles that change
  with the seed, and the same energy for the plain chain with hopping $\sqrt2$, at $180^\circ$. pyqula with
  `maxite=4000` gives this energy within $10^{-5}$ for four seeds, with angles between $95^\circ$ and $127^\circ$ and
  $\cos\theta=-n_y^2$, and with the default `maxite=1000` the seed 0 raises `MeanFieldConvergenceError`. The release
  0.0.96 of the students prints a line there and returns `None` in place of the Hamiltonian, as the sheets of Sessions
  1 and 10 say. So the angle
  of the cell is set by the random guess and not by the coupling, and the Rashba chain is not the spiral of the line
  above.
- The triangular lattice of the notebook, a supercell of $3\times3$ at $U=10t$ with `mf="XY"` and `maxite=4000`, has
  $120^\circ$ within $0.2^\circ$ on its 27 bonds and $|m|=0.922$, with the energy $-3.8085$ per cell for two seeds.

## Holstein-Primakoff and the magnons

- The transformation (6.6) reproduces the spin matrices and their algebra exactly on the boson states $n=0,\dots,2S$,
  to $10^{-12}$ for $S$ from 1/2 to 2. $S^-=a^\dagger\sqrt{2S-n}$ adds a boson, so it creates the magnon.
- The ferromagnetic magnon (6.8), $E=|J|Sz(1-\gamma)$ with $\gamma(\mathbf k)=\tfrac1z\sum_{\boldsymbol\delta}
  e^{i\mathbf k\cdot\boldsymbol\delta}$ on a Bravais lattice, is exact for one magnon. On a ring of 10 spins 1/2 and
  on a ring of 8 spins 1 a plane wave of one magnon is an eigenstate with $2|J|S(1-\cos k)$. The magnon hops with
  $-|J|S$, $-0.5$ and $-1.0$ for $|J|=1$, and it has the onsite energy $|J|Sz$, 1.0 and 2.0. On a square torus of
  $4\times4$ spins 1/2 the plane waves have 0 at $\Gamma$, $4|J|S$ at $X$ and $8|J|S$ at $M$. At small $k$ the band is
  $|J|Sk^2$ on the chain and on the square lattice.
- The antiferromagnetic magnon (6.9), $E=JSz\sqrt{1-\gamma^2}$, is $2JS|\sin k|$ on the chain, with zeros at $k=0$ and
  $\pi$. A numerical bosonic Bogoliubov diagonalization gives it to $10^{-12}$, gives $JSz$ at every $k$ when the
  anomalous terms are removed, and gives $v_k^2=\tfrac12\big(1/\sqrt{1-\gamma^2}-1\big)$ bosons per mode in the magnon
  vacuum, 1.192 at $k=0.3$ and exactly 0 at $k=\pm\pi/2$. pyqula `hmf.get_magnon_energies` on the half-filled Hubbard
  bichain at $U=20t$ gives 0, 0.0618, 0.1414 and 0.1902 at $k$ equal to 0, $0.1\pi$, $0.25\pi$ and $0.4\pi$, which is
  $J|\sin k|=2JS|\sin k|$ with $J=4t^2/U$ and $S=1/2$, and the next energies are near $U$.
- (6.9) is linear spin-wave theory, and it leaves out the quantum fluctuations. The zero-point bosons reduce the moment
  of a sublattice by 0.196 on the square lattice, so $\langle S^z\rangle=0.30$ for $S=1/2$. On the chain the reduction
  grows as the logarithm of the number of k-points, 1.23, 1.96 and 2.69 for 100, 1000 and 10000, so the chain has no
  Néel order in this theory. The exact chain of spins 1/2 has its lowest triplet at $(\pi/2)J|\sin k|$, and a ring of
  12 spins gives $1.727J$ at $k=\pi/2$, where (6.9) gives $1.000J$. This is where Section 8.7 can start.
- An easy axis $-A(S^z)^2$ with $A>0$ costs $A(2S-1)$ for one magnon on a site, 0, $A$ and $2A$ for $S$ equal to 1/2,
  1 and 3/2, while linear spin waves give $2AS$. For $S=1/2$ the term is the constant $-A/4$ and opens no gap.

## Topological magnons

- For the honeycomb ferromagnet $H=J\sum_{\langle ij\rangle}\mathbf S_i\cdot\mathbf
  S_j+D\sum_{\langle\langle ij\rangle\rangle}\nu_{ij}\,\hat z\cdot(\mathbf S_i\times\mathbf S_j)$ with $J<0$, where
  $\nu_{ij}=+1$ when the path from $i$ to $j$ through their common neighbor turns left, the exact one-magnon matrix of a
  torus of $3\times3$ cells with $S=1/2$ has no term that leaves the one-magnon states, since $D$ along $z$ keeps $S^z$.
  So the magnon Hamiltonian of the ferromagnet needs no Bogoliubov transformation. It is $3|J|S$ plus
  `_haldane.hk(k, t=|J|S, t2=-DS)`, which is the same matrix as `t2=DS, phi=-pi/2`, while `t2=+DS` misses it by 0.07.
- With the Berry curvature of Session 3, `_haldane.hk` with $t_2>0$ and the default phase $+\pi/2$ has $C=+1$ for the
  lower band. So $D>0$ gives $C=-1$ to the lower magnon band and $+1$ to the upper one, and $D<0$ reverses both. The
  gap at $K$ is $6\sqrt3\,DS$, 1.0392 for $DS=0.1$, which is the full gap, and the lower band starts at zero at
  $\Gamma$, the Goldstone mode. The counterclockwise hop on $A$ of `_haldane.hops` with $t_2=+0.1$ has the phase
  $-\pi/2$. So the figure `ribbon_magnons`, which calls its panel with $t_2=+0.1$ "$D>0$", and panel (b) of
  `dm_honeycomb` draw $D<0$ in the convention of this line, while panel (a) of `dm_honeycomb` draws the
  counterclockwise hop on $A$ with $+\pi/2$, which is $D>0$. The bands of panel (b) do not depend on the sign. In a
  ribbon of 24 cells the branch at the lower edge has a positive slope for $t_2=+0.1$ and a negative one for $-0.1$.
  `_haldane.hk` and `_haldane.ribbon` give a hop to the cell $\mathbf R+\mathbf d$ the phase
  $e^{+i\mathbf k\cdot\mathbf d}$, so their $k$ is minus the momentum of the Bloch state, and $C$ is the same for both
  signs of $k$. With the momentum, the ribbon of $t_2=+0.1$, with $C=+1$, has the negative slope at the lower edge and
  the positive one at the upper edge, as the pyqula ribbon with `add_haldane(0.1)` of the sheet of Session 4 has at the
  edge of positive $y$. A
  page says only that reversing $D$ reverses $C$ and the edge branches.
- `h.add_haldane(0.1)` of pyqula is a second-neighbor hopping $t_2=0.0866$, with the gap 0.900 on the honeycomb lattice
  of pyqula, while $DS=0.1$ in `_haldane.hk` gives 1.039, so a page says which one it quotes. `h.get_chern()` counts
  the states below zero energy. The magnon cell of the notebook builds the spinful lattice with `tij=[1.,0.2]` and
  `add_haldane(0.1)`, then `set_filling(0.0)` and `add_onsite(0.5)`. There the bands start at 0.499, and
  `h.get_chern()` gives 0.0 for both signs of `add_haldane`. Before `set_filling(0.0)` it gives $\pm1.019$, since zero
  energy is inside the upper band, and the spinless lower band has $C=+1$ and $-1$ for `add_haldane(0.1)` and
  `add_haldane(-0.1)`, with the gap 0.900. A magnon Chern number is computed band by band, or with zero energy moved
  into the gap, as the recipe "The Chern number of a magnon band" does.

## Statements of the pages that these numbers contradict

These are left as they are until the lecturer decides. Each one is checked again by its number.

- Section 6.6 says that the self-consistent magnetization of the chain "grows continuously once $U$ is above this
  threshold", and Figure 6.1(b) draws such a rise. In mean field the uniform chain jumps from $m=0$ to $m=0.2$ at
  $U=1.926t$ for $n=0.2$, and it jumps at every filling. A continuous rise needs a density of states with its maximum
  at $E_F$, as in the widget.
- Section 6.5 says that the uniform solution "is the paramagnet below $U\approx 4t$ and a fully polarized ferromagnet
  above it", and the caption of `mf_chain` puts a jump at $4t$, where its script switches from the paramagnet to the
  saturated ferromagnet. The saturated state exists from $4t$, but it stays above the paramagnet, by $0.27t$ per site
  at $4t$, up to $16t/\pi=5.09t$. So the lowest uniform state changes at $5.09t$. Its energy has a kink there, with the
  slope $1/4$ of the paramagnet below and 0 above, and no jump, while its moment jumps from 0 to 1, as the sheet of
  Session 1 says.
- Section 6.3 writes $\mathbf m\equiv\langle\mathbf S\rangle$ next to the $m$ of (6.2), which is twice
  $\langle S^z\rangle$, and it says that self-consistency gives "a magnetic solution with $m\neq0$ for $U>0$". This
  holds for the antiferromagnet of the half-filled chain, with $m=0.030$ at $U=t$, while a uniform moment needs the
  Stoner threshold, $1.93t$ at $n=0.2$.
- Section 6.4 and its notebook box say "20% filling" for the chain that the caption gives as $n=0.2$. That is
  `filling=0.1` in pyqula, 10 percent of the states. With `filling=0.2` the chain has $n=0.4$ and the splitting
  $1.6t$ at $U=4t$, and not $0.8t$.
- The notebook box and the try-it box of Section 6.8 say to diagonalize the dimer with six states in the cell "The
  interacting Hubbard dimer". That cell is a mean-field loop, with no moment below $U=2t$ and $\sqrt{1-4t^2/U^2}$
  above, and the ratios 0.83, 0.94 and 0.98 belong to the exact dimer, which the cell does not have.
- The try-it box of Section 6.12 reads the angle of the Rashba chain as the ground state tilting away from collinear
  order. The Rashba coupling of the chain is a rotation of the spin from bond to bond, which a change of the spin axes
  removes, so the mean field has one energy for every angle from $90^\circ$ to $180^\circ$, and the random guess of the
  cell picks one, between $95^\circ$ and $127^\circ$ in four runs. With the default `maxite=1000` the cell can stop with
  `MeanFieldConvergenceError` in the development tree, and with `None` in place of the Hamiltonian in the release.
- The try-it box of Section 6.16 says that `h.get_chern()` changes sign with `add_haldane(-0.1)` when it is called
  before the ribbon. In the cell, after `set_filling(0.0)` and `add_onsite(0.5)`, it gives 0.0 for both signs.
- Section 6.16 applies the Chern number "to the bosonic Bogoliubov Hamiltonian of Section 6.15". The magnon
  Hamiltonian of the honeycomb ferromagnet has no anomalous term, so it is an ordinary hopping matrix, and the
  Bogoliubov form belongs to the antiferromagnet.
- The quiz of Section 6.17 says that an easy-axis anisotropy $A\,(S^z)^2$ "opens a gap of order $A$". An easy axis is
  $-A(S^z)^2$ with $A>0$, and its gap is $A(2S-1)$, which is of order $A$ for $S\geq1$ and zero for $S=1/2$.
- The caption of `afm_bogoliubov` says of $v_k^2$ that "it is nonzero", while it is exactly zero at $k=\pm\pi/2$, as
  the alt text of the same figure says, and 1.19 at $k=0.3$.
