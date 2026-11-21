# Conventions of Session 2, checked by number

This sheet fixes the signs, the units and the pyqula facts that the pages, the figures and the pyqula scripts of
Session 2 use. An agent that edits the session reads it first and does not work these out again. Every bullet was
checked with a number on 2026-11-21. Two drafts were written apart, and a third calculation settled each line where
they differed or where only one of them had it. The energies are in units of the hopping $t$, and the figures take
$t=\hbar=a=1$. The pyqula of the checks is the development tree of version 0.0.95, at commit 7567127. The notebook
and the downloaded scripts run the release 0.0.96 of PyPI, and the two differences that matter here were read in its
code and not run. They are in the bullets on the labels and on the density of states of pyqula. The figure scripts of
`webnotes/figures/session02/` and the Blender scripts `s02f02` to `s02f05` were read on the same day. They take the
sign of the formula that they draw, $-t$ for the chain, the square, the Lieb and the kagome lattices, $+t$ for
graphene as (2.19) does, and the matrix (2.13) for the chain with two sites per cell, while `band_sign_t` draws both
signs. A statement that is not on this sheet is checked before a page claims it. The check is
`webnotes/checks/session02/conventions.py`, which prints one line per bullet below, in the same order.

## The sign of the hopping

- The notes write $H=-t\sum_n(c_n^\dagger c_{n+1}+\text{h.c.})$ with $t>0$, as (2.5) says. So the chain has the band
  $-2t\cos\varphi$, with the minimum $-2t$ at $\varphi=0$ and the maximum $2t$ at $\varphi=\pi$, and a ring of 12
  sites has these levels. The square lattice (2.14) goes from $-4t$ at $\Gamma$ to $4t$ at $(\pi,\pi)$, and the cubic
  lattice (2.15) from $-6t$ to $6t$, so the widths are $4t$, $8t$ and $12t$. pyqula with `tij=[-1.]` gives the same.
- The dimer (1.2) of Session 1 is $H=t(c_0^\dagger c_1+c_1^\dagger c_0)$ with a plus sign, and Section 2.3 writes the
  same dimer with the sites 1 and 2. For $t>0$ the symmetric state $(c_0^\dagger+c_1^\dagger)|0\rangle/\sqrt2$ has
  the energy $+t$ and the mirror eigenvalue $+1$, and the antisymmetric state has $-t$ and $-1$. So the lower state is
  the antisymmetric one, and two electrons have the energy $0$. The symmetric state is the lower, bonding, state only
  when the matrix element is negative, as in (1.6) and (2.5).
- The graphene form (2.19) is written with $+t$, and its bands $\pm|f(\mathbf k)|$ are the same for $+t$ and $-t$,
  checked at 20 momenta. The default hopping $+1$ of `honeycomb_lattice()` gives these bands directly.
- pyqula puts $+1$ on every first-neighbor bond of `chain`, `square_lattice`, `cubic_lattice`, `triangular_lattice`,
  `honeycomb_lattice`, `lieb_lattice`, `kagome_lattice`, `ladder` and `bichain`. The default $H(\mathbf k)$ is minus
  the one of `tij=[-1.]`, so a band of pyqula is the band of the notes for $t=-1$.
- The downloaded scripts take `tij=[-1.0]` for the chain, the square and the kagome lattices, the sign of the notes,
  and the default $+1$ for the honeycomb lattice, the $+t$ of (2.19). The notebook takes $+1$ everywhere. What the
  change of sign does depends on the lattice, in three ways. The chain, the square and the cubic lattices keep the
  same energies moved by $\pi$ in every direction, so the notebook has its bottom at $\varphi=\pi$ and its top $2$,
  $4$, $6$ at $\Gamma$. The honeycomb lattice, the Lieb lattice and `bichain` keep the same energies at every
  momentum. The triangular lattice, the kagome lattice and the chain with a second-neighbor hopping turn upside down.
  The triangular band runs from $-6t$ to $3t$ in the notes and from $-3$ to $6$ in the notebook, and the kagome bands
  from $-4t$ to $2t$ with the flat band at $+2t$ in the notes, and from $-2$ to $4$ with the flat band at $-2$ in the
  notebook.
- The place $n$ of `tij` is the hopping to the neighbor at distance $n$, so on the chain `tij=[t1,t2,t3]` gives
  $2\sum_n t_n\cos(n\varphi)$, the form of the notebook. (2.9) comes out only when both hoppings change sign, with
  `tij=[-1.,-eta]`. `tij=[1.,eta]` gives exactly minus (2.9), and `tij=[-1.,eta]` misses (2.9) by 1.2 for $\eta=0.3$.
- Every `get_hamiltonian` of `session2.ipynb` takes the default or `tij=[1.0,...]`, so its bands are those of the
  notes with $t=-1$, as the try-it boxes of Sections 2.5, 2.8 and 2.11b say. The cell "One dimensional chain" has
  `tij=[1.0,0.]`, so its band is $+2\cos\varphi$. Many cells call `get_hamiltonian()` with no `has_spin=False`, among
  them the Fermi surface and the bands of graphene, so there every band comes twice and the weights are doubled. The
  cell "Density of states of the honeycomb lattice" is spinless.

## The Bloch phase and the momentum of pyqula

- The translation $T$ of Section 2.4 moves each amplitude to the previous site, $(T\psi)_n=\psi_{n+1}$, so the state
  $e^{in\varphi}$ of (2.6) has the eigenvalue $e^{i\varphi}$. The rotation $R$ of Section 2.3 and of the figure
  `dimer_ring_symmetry` moves each amplitude to the next site, $(R\psi)_j=\psi_{j-1}$, which is $T^{-1}$, so the same
  state has the eigenvalue $e^{-i\varphi}$ under $R$. This is why $(1,-i,-1,i)$ has $R=i$ and $(1,i,-1,-i)$ has
  $R=-i$, as Section 2.3 says, while $(1,-i,-1,i)$ is the state $\varphi=-\pi/2$ of (2.6). On three sites the
  rotation $1\to2\to3\to1$ in the sense of $R$ gives $e^{2\pi ij/3}$ the eigenvalue $e^{-2\pi i/3}$.
- (2.7) and the orthogonality sum below it are printed with no normalization. On a ring of $L$ sites
  $\sum_n e^{in(\varphi'-\varphi)}=L\,\delta_{\varphi\varphi'}$, so the inverse of (2.7) as printed gives
  $L\,c_n^\dagger$. With $1/\sqrt L$ on both sides the transform is unitary, and the same steps give $H$ diagonal
  with $-2t\cos\varphi$, which is (2.8) unchanged. Checked on 8 sites.
- $\gamma_{\alpha\beta}$ of (2.11) is the element of $c_{n,\alpha}^\dagger c_{n+1,\beta}$, and `h.inter` of pyqula is
  this $\gamma$. `h.get_hk_gen()([k,0,0])` is `h.intra + h.inter*exp(2j*pi*k)` plus its Hermitian conjugate, the
  form (2.12) with $\varphi=2\pi k$. `bichain()` has its only intercell 1 in `h.inter[1,0]`, the bond from $B$ of a
  cell to $A$ of the next cell, so with `h.inter = eta*h.inter` the Bloch matrix is (2.13) entry by entry, with $A$
  the first site.
- pyqula takes the reduced momentum $k_i=\mathbf k\cdot\mathbf a_i/2\pi$, so its zone runs from 0 to 1 and
  $\varphi=2\pi k$. `(k, e) = h.get_bands()` returns the number of the step in `k` in place of the momentum. On the
  chain the default path has 400 momenta from $k=0$ to $k=1$ with both ends, so the band $+2\cos\varphi$ is $+2$ at
  both ends and $-1.99994$ at step 199, close to its minimum $-2$ in the middle of the plot.

## Lattices, zones and points

- In pyqula the bond length is 1 on every lattice. The lattice constant is 1 for `chain`, `square_lattice`,
  `cubic_lattice` and `triangular_lattice`, $\sqrt3$ for `honeycomb_lattice`, and 2 for `lieb_lattice`,
  `kagome_lattice` and `bichain`. `honeycomb_lattice` has $\mathbf a_1=(3/2,\sqrt3/2)$ and
  $\mathbf a_2=(-3/2,\sqrt3/2)$, with its two sites at $(\pm1/2,0)$, so one bond is along $x$.
  `triangular_lattice` has $\mathbf a_2=(-1/2,\sqrt3/2)$, `kagome_lattice` has $(2,0)$ and $(1,\sqrt3)$,
  `lieb_lattice` has $(2,0)$ and $(0,2)$, and `bichain` has its sites at $x=\pm0.5$.
- `h.get_bands(kpath=[...])` takes the names of the points from `label2k`, in reduced coordinates. On the square and
  Lieb lattices "X" is $(1/2,0)$ and "M" is $(1/2,1/2)$ in the development tree. In the release 0.0.96 of PyPI,
  which the students install, "M" is $(1/2,0)$ on every lattice, read in its code, so there the path
  `["G","X","M","G"]` of the square lattice never reaches $(\pi,\pi)$. A script for students gives the square and
  Lieb paths as a list of reduced momenta, which both versions take as they are, and such a path has $-4$, $0$, $4$
  at $\Gamma$, $X$, $M$ with `tij=[-1.]`. On the honeycomb and triangular lattices "K" is $(-1/3,-1/3)$ and "K'" is
  $(1/3,1/3)$, on the kagome lattice "K" is $(-1/3,1/3)$, and "M" is $(1/2,0)$ on all three.
- The labeled path takes for each point the copy closest to the point before, so on the honeycomb lattice
  `["G","K","M","G"]` walks to the corner $(-2\pi/3,\,2\pi/3\sqrt3)$. This corner is in the valley of the "K" of
  `label2k`, at $(0,\,-4\pi/3\sqrt3)$, which is the $K$ of the notes minus $\mathbf b_1$. The default path writes "K"
  in `BANDLINES.OUT` at the step of $(1/3,1/3)$, the corner $(0,\,4\pi/3\sqrt3)$ that `label2k` calls "K'", and the
  recipe test of Session 3 also calls this corner $K$. So a page gives a corner by its coordinates and says which
  name it carries.
- The default path of `h.get_bands()` in two dimensions is a straight line of 400 steps $s(1,1)$ for the honeycomb and
  triangular lattices and $s(1,-1)$ for the square, Lieb and kagome lattices, with $s$ from $1/400$ to 1. So it starts
  one step after $\Gamma$ and ends at $\Gamma$. On the honeycomb lattice it passes the two corners, $M$ and $\Gamma$,
  and on the square lattice it is $\Gamma$, $M$, $\Gamma$ along the diagonal, with no $X$. No step falls on a corner
  of the honeycomb zone, so the closest steps, 132 and 266, have $|E|=0.009$ in place of 0, while step 199 is $M$
  with $\pm1$ and the last step has $\pm3$. In three dimensions the path goes from $\Gamma$ to $X$, $M$, $\Gamma$ and
  $R$.
- With the sign of the notes the chain has $-2t$ and $2t$ at $\varphi=0$ and $\pi$, the square lattice $-4t$, $0$, $4t$
  at $\Gamma$, $X=(\pi,0)$, $M=(\pi,\pi)$, the cubic lattice $-6t$, $-2t$, $2t$, $6t$ at $\Gamma$, $X$, $M$,
  $R=(\pi,\pi,\pi)$, and the triangular lattice $-6t$, $3t$, $2t$ at $\Gamma$, $K$, $M$, with $|K|=4\pi/3$, $|M|=
  2\pi/\sqrt3$ and a saddle at $M$. The widths are $4t$, $8t$, $12t$ and $9t$.
- The honeycomb lattice of the notes is the one of the figure `graphene_path`, with the bond length $a=1$ and
  $\boldsymbol\delta_j$ at $0^\circ$, $120^\circ$ and $240^\circ$, the frame of pyqula. Its $K=(2\pi/3,\,2\pi/3\sqrt3)$
  has $|K|=4\pi/3\sqrt3=2.418$, its $M=(2\pi/3,0)$ has $|M|=2\pi/3=2.094$, and $|f|$ is $3t$, $t$ and $0$ at
  $\Gamma$, $M$, $K$, so the bands span $-3t$ to $3t$. This $K$ is the "K" of `label2k` plus $\mathbf b_1$. The
  Blender script `s02f04_dirac.py` has the bonds along $y$, with $\mathbf a_1=(\sqrt3,0)\,a$ and the corner
  $K=(4\pi/3\sqrt3a,0)$, where $f$ also vanishes.
- `h.get_hk_gen()` of the honeycomb lattice has the entry $[0,1]$ equal to
  $f(\mathbf k)\,e^{-i\mathbf k\cdot(\mathbf r_1-\mathbf r_0)}$, with $\mathbf r_1-\mathbf r_0=\boldsymbol\delta_1=(1,0)$,
  since pyqula puts every orbital at the origin of its cell. This entry is periodic over the zone, while $f$ of (2.19)
  is not, and the bands are the same.
- The Lieb lattice has the bands $0$ and $\pm2t\sqrt{\cos^2k_x+\cos^2k_y}$, with $k$ in units of the inverse bond
  length, for both signs of $t$. So it has $0$ and $\pm2\sqrt2\,t=\pm2.83\,t$ at $\Gamma$, $0$ and $\pm2t$ at
  $X=(\pi/2,0)$, and three bands at 0 at $M=(\pi/2,\pi/2)$, where the cone has the slope $2t$ times the bond length,
  which is $t$ times the lattice constant. The Blender figure of Section 2.11b takes the lattice constant 1, so there
  $M$ is $(\pi,\pi)$ and the slope is 1.
- The kagome lattice with $-t$ has $-4t$, $2t$, $2t$ at $\Gamma$, where the flat band touches the upper dispersive
  band, $-t$, $-t$, $2t$ at $K$, the Dirac crossing at $-t$, and $-2t$, $0$, $2t$ at $M$. pyqula with its default
  gives $-2$, $-2$, $4$, then $-2$, $1$, $1$, then $-2$, $0$, $2$ at the same points. The Blender figure takes the
  lattice constant 1, so its $K$ is $(4\pi/3,0)$ and its $M$ is $(\pi,\pi/\sqrt3)$, while `kagome_dos.py` takes the
  lattice constant 2, as pyqula does.
- The three sites of `kagome_lattice()` are three of the four sites of a $2\times2$ cell of the triangular lattice of
  spacing 1, and those of `lieb_lattice()` are three of the four sites of a $2\times2$ cell of the square lattice. So
  both lattices keep three sites in four, as Section 2.11b says.
- With $-t$, the six amplitudes $+1,-1,+1,-1,+1,-1$ around one hexagon of the kagome lattice give $H\psi=2t\psi$
  exactly, with no amplitude on any other site. Each of the six sites outside that touch the hexagon is bonded to two
  of its sites with opposite amplitudes, so it gets $-t(1-1)=0$. Checked on a torus of 108 sites for $t=1$ and $t=2$.
  With the default of pyqula the energy is $-2$.

## The Dirac cone

- $v_F=3ta/2\hbar$ of (2.20) holds with $a$ the bond length. The slope of $|f|$ at $K$ is 1.5000 in every direction,
  in the two frames of the scripts and in pyqula, in units of $t$ times the bond length over $\hbar$, and 0.866 in
  units of the lattice constant $\sqrt3$. The largest velocity of the chain, $2ta/\hbar$ at $\varphi=\pm\pi/2$, is
  larger than this.
- At the $K$ of the notes $f(\mathbf K+\mathbf q)=\frac32t\,e^{-5i\pi/6}(q_x-iq_y)$, and at $K'=-K$ it is
  $\frac32t\,e^{-i\pi/6}(q_x+iq_y)$. So (2.20) holds at $K$ once the phase is put into the $B$ orbital, and at $K'$
  it holds with $q_y\to-q_y$, the sign of the $\sigma_y$ term changed. The energies (2.21) are the same at both. A
  page that needs the winding of the cone, as Session 3 does, takes it from this line.
- For the cone (2.21) the matrix (2.18) at $\mathbf q$ is 0 along $\mathbf q$ and $v_F/|\mathbf q|$ across it. So the
  mass is infinite along the radius, as Section 2.11a says, and across the radius it is $\hbar|\mathbf q|/v_F$, which
  goes to zero at the tip. The band $|f|$ at $|\mathbf q|=0.01$ from $K$ has a radial curvature from $-0.76$ to
  $0.74$, the trigonal warping, and a curvature across $\mathbf q$ from 147 to 153, where $v_F/|\mathbf q|=150$.

## The density of states

- The chain has $g(\omega)=1/(\pi\sqrt{4t^2-\omega^2})$ per site, which is $1/(2\pi t)=0.159/t$ in the middle of the
  band and diverges as an inverse square root at $\pm2t$, where the velocity vanishes. A count on $2\cdot10^6$
  momenta and pyqula with `mode="Green"` give 0.1592, 0.1838 and 0.2406 at $\omega=0$, 1 and 1.5.
- The square lattice has $g(\omega)=K(1-\omega^2/16t^2)/(2\pi^2t)$ per site, with $K(m)$ the complete elliptic integral
  of parameter $m$. It is $1/(4\pi t)=0.0796/t$ at the band edges, the $|m^\ast|/2\pi\hbar^2$ of a parabolic band,
  with $m^\ast=\hbar^2/2ta^2$ at the bottom and $m^\ast=-\hbar^2/2ta^2$ at the top, and it diverges as
  $\ln(16t/|\omega|)/(2\pi^2t)$ at $\omega=0$, from the saddle points $X$ and $Y$. A count on $2000^2$ momenta agrees with the formula to two percent at four energies.
- The honeycomb lattice has $g(E)\approx2|E|/(\sqrt3\pi t^2)=0.368|E|/t^2$ close to zero energy, per unit cell, for one
  spin and summed over the two bands, of which only one has states at a given $E$. This is $A_c|E|/(\pi\hbar^2v_F^2)$
  with the cell area $A_c=3\sqrt3a^2/2$, the two valleys and $v_F=3t/2$. A count on $1500^2$ momenta gives 0.01480
  states with $|E|<0.2$, where the formula gives 0.01470. The peaks are at $\pm t$, the saddle points $M$, and the
  band ends at $\pm3t$.
- (2.16) counts per unit length, area or volume, for each band and for one spin, and with $a=1$ for the chain, the
  square and the cubic lattices this is per site. `h.get_dos()` counts per unit cell, summed over every band and over
  both spins, so its area is the number of bands, 1, 2 and 3 for the chain, the honeycomb and the kagome lattices,
  and the default spinful Hamiltonian doubles it, 0.318 for the chain at zero energy. So the notebook gives (2.16) up
  to the cell area and the sum over bands. With no `mode` it sums Lorentzians of half width `delta` over a mesh of
  `nk` by `nk` momenta, and `mode="Green"` takes the Green function. The development tree also takes
  `integration="triangle"`, which the release 0.0.96 does not have, read in its code, so a script for students does
  not use it. The figure `kagome_dos` runs the script `g4_kagome_bands.py`, which calls `h.get_dos` with
  `tij=[-1.]`, `has_spin=False`, `delta=4e-2` and `nk=200`. So it is the density per cell for one spin, summed over the
  three bands, with the area 2.969 on its window from $-5t$ to $3t$, three states less the tails. The flat band is one
  state per cell in a Lorentzian of height $1/\pi\delta=7.96$, and with the tails of the other bands the peak at $2t$ is
  8.10. The peaks at $-2t$ and 0 are 0.70 and the V at $-t$ is 0.042, and the spinful Hamiltonian doubles all of them.
- The cell "Density of states of the honeycomb lattice" calls `h.get_dos(delta=4e-2, energies=np.linspace(-3.5,3.5,400),
  nk=200)` on the spinless Hamiltonian. This gives the area 1.979 over the window, two states per cell less the
  tails, the minimum 0.041 at zero energy, which is the V rounded by `delta`, and the peaks at $\pm1.01$ on its grid.
  With the triangular lattice uncommented, as the try-it of Section 2.9 asks, the same call gives 0.103 to 0.112
  within 0.1 of zero energy, a ripple of the mesh around the 0.107 of a count, with no dip, and its peak is at $-2$.
- With the sign of the notes the van Hove peaks are at saddle points of a band, at 0 for the square lattice (at $X$),
  at $\pm t$ for the honeycomb lattice (at $M$), at $2t$ for the triangular lattice (at $M$), and at $-2t$ and 0 for
  the kagome lattice (both at $M$). pyqula with its default has the same peaks with the opposite sign, $-2$ on the
  triangular lattice and 0 and 2 on the kagome lattice. The chain follows $1/(\pi\sqrt{4t^2-E^2})$ up to its band
  edges, 1.128 at $E=1.98t$, which is $1/(\pi\sqrt{4t(2t-E)})$ there to one percent.
- The kagome flat band at $2t$ is one band of three at every momentum, so it holds exactly one third of the states, a
  delta peak in (2.16), and the dispersive bands fill $-4t$ to $2t$. The middle band of the Lieb lattice is 0 at every
  momentum, also one third of the states, for both signs of $t$.
- The cell "One dimensional chain, with longer range hopping" changes the third-neighbor hopping $t_3$ in
  `tij=[1.0,0.,t3]`, not the $\eta$ of (2.9). For $t_3=1/3$ the band $2\cos k+\frac23\cos3k$ has zero energy, slope
  and curvature at $k=\pi/2$ and the third derivative $-16$, so the density of states diverges at zero energy as
  $|E|^{-2/3}$, more strongly than at a band edge.

## Velocity, mass and the Fermi surface

- For the chain $v=(2ta/\hbar)\sin\varphi$ and $1/m^\ast=(2ta^2/\hbar^2)\cos\varphi$. The velocity is 0, $2ta/\hbar$
  and 0 at $\varphi=0$, $\pi/2$ and $\pi$, and the mass is $\hbar^2/2ta^2$ at the bottom and $-\hbar^2/2ta^2$ at the
  top, with the change of sign at $\pm\pi/2$. Close to the ends the band is $-2t+t\varphi^2$ and $2t-t\delta^2$.
- For the square lattice the inverse mass of (2.18) is $2t$ along both axes at $\Gamma$, $-2t$ along both at $M$, and
  $-2t$ and $+2t$ at $X$, in units of $a^2/\hbar^2$. So $X$ is a saddle point, and it gives the log peak at zero.
- The chain (2.9) has $\epsilon(\pi/2)=2\eta$, and its curvature at $\varphi=\pi$ is $8\eta-2t$, so $\varphi=\pi$
  becomes a local minimum for $\eta>t/4$. The two maxima are then at $\cos\varphi=-t/4\eta$, with the energy
  $2\eta+t^2/4\eta$, and the dip at $\pi$ below them is $(4\eta-t)^2/4\eta$. This is $0.033t$ for $\eta=0.3$ and
  $0.5t$ for $\eta=0.5$, and there is none for $\eta=0.2$. For $\eta=0.5$ the band is $-3t$ at 0, $t$ at $\pi$ and
  $1.5t$ at its maxima, a width of $4.5t$, and pyqula with `tij=[1.,0.5]` has its extrema at $3$, $-1$ and $-1.5$.
- At half filling the square lattice has $\mu=0$, since $\epsilon(\mathbf k+\mathbf Q)=-\epsilon(\mathbf k)$ with
  $\mathbf Q=(\pi,\pi)$ maps the states below zero onto the ones above. The Fermi surface is the square
  $|\varphi_x|+|\varphi_y|=\pi$, and $\mathbf Q$ joins its opposite sides. The chain at half filling has $k_F=\pi/2$,
  so its two Fermi points are $2k_F=\pi$ apart.
- The Fermi surface of the honeycomb lattice is two pockets around $K$ and $K'$ for $|E|<t$. At $|E|=t$ they meet at
  the saddle points $M$, which is a Lifshitz transition, and for $t<|E|<3t$ it is one contour around $\Gamma$. On a
  mesh of $240^2$ momenta there are 2 pockets at $|E|<0.5$ and at $|E|<0.999$ and one region above 1.5, and the
  upper band has the curvatures $-1.5$ and $4.5$ at $M$.
- `(x, y, w) = h.get_fermi_surface(e=E, delta=d, nk=n)` returns $n\times n$ points from $-1$ to $1$ with both ends,
  with `x` the slow index, so `w.reshape(n, n)[i, j]` is at `x[i*n]` and `y[j]`. `x` and `y` are the Cartesian
  momentum in units of $2\pi$ over the length of `g.a1`, which is $2\pi/\sqrt3$ for the honeycomb lattice, so $K$ is
  at $(0,\pm2/3)$. The weight is $\sum_n\delta/((E-E_n)^2+\delta^2)$, with no $1/\pi$, so a state at the energy $E$
  gives $1/\delta$, $2/\delta=40$ at $K$ for `delta=0.05` and $E=0$, and twice that for the spinful Hamiltonian of the
  notebook. `h.get_bands_map(n=0, nk=n)` takes the same units on a mesh from $-1$ to $1-2/n$, with no end point,
  where `n` counts the bands from 0 at the lowest energy. For the honeycomb lattice the window holds
  $2\sqrt3=3.46$ zones and is not a period of the band.

## Chains with more sites per cell

- (2.13) has the bands $\pm|1+\eta e^{-i\varphi}|$, which are $\pm(1+\eta)$ at $\varphi=0$ and $\pm|1-\eta|$ at
  $\varphi=\pi$. So the gap is $2|1-\eta|$, 0.8 for $\eta=0.6$, and it closes at $\eta=1$, where the bands are
  $\pm2|\cos(\varphi/2)|$, the band of the uniform chain folded into the zone of the cell of two sites. `bichain()`
  with `h.inter = eta*h.inter` gives these bands, with $\varphi=2\pi k$ for its cell of length 2.
- A uniform chain described with $N$ sites per cell has the bands $-2t\cos[(\varphi+2\pi m)/N]$, $m=0,\dots,N-1$, with
  $\varphi$ the phase per cell, and a ring of 60 sites has exactly these levels. At $\varphi=0$ this is $-2t$, $t$,
  $t$ for $N=3$ and $-2t$, $0$, $0$, $2t$ for $N=4$. `chain().get_supercell(N)` has $a=N$ and gives the negatives with
  the default hopping, $-1$, $-1$, $2$ at $k=0$ for $N=3$, and $-2$, $1$, $1$ with `tij=[-1.]`. With
  `tij=[-1.,-0.8]`, `get_supercell(5)` at $k=0$ has the five levels of the ring of five sites with $t_2=0.8t$.
- `geometry.ladder()` of the notebook is not the chain of (2.13). It has the rung 1 in `h.intra` and the two legs 1 in
  `h.inter`, so each site is bonded to its partner on the rung and to its own copy in the next cell. Its bands are
  $2\cos\varphi\pm1$ in pyqula, 1 and 3 at $\varphi=0$ and $-3$ and $-1$ at $\varphi=\pi$, where (2.13) with $\eta=1$
  has $\pm2$ and 0.

## Rings and ARPES

- On a ring of $L$ sites with any hopping that keeps the rotation, every Fourier mode is an eigenstate with the weight
  $1/L$ on each site. A level with two modes, $\varphi$ and $-\varphi$, also holds their combinations, which do not
  have this weight. With the plus sign $H=\sum c_i^\dagger c_j$ of Section 2.4 the lowest level of 5 sites is
  $2\cos(4\pi/5)=-1.618$, twice, and a site has a weight from 0 to 0.40 in the states of this level. With $-t$ the
  ground state is $\varphi=0$, single, with 0.2 on every site. The ring of 5 sites with $t_2=0.8t$ has the levels
  $-3.6$, $0.676$ twice and $1.124$ twice, and on 6 sites with $\eta=0.3$ every Fourier mode is an eigenstate.
- $\hbar^2/2m=3.810$ eV Å$^2$, so an electron of 20 eV has $k=22.9$ nm$^{-1}$, and the angles $10^\circ$ and $20^\circ$
  give $k_\parallel=3.98$ and $7.84$ nm$^{-1}$, which round to the 4.0 and 7.8 of Section 2.12.

## Open points of the old text, left as they are

These restate lines above for the pages they concern. Each one is a change of a numbered equation or of the old
text, so it is the lecturer's to decide, and the plan of the session lists them.

- Section 2.3 calls $c_1^\dagger+c_2^\dagger$ the bonding state of $H=t(c_1^\dagger c_2+\text{h.c.})$. With $t>0$, the
  sign of the session, it is the upper level at $+t$, as the caption of `dimer_ring_symmetry` on the same page says.
- Section 2.4 says that $R$, which turns $1\to2\to3\to1$, multiplies a state by $e^{i\varphi_n}$ when
  $\alpha_j\propto e^{i\varphi_nj}$. With the $R$ of Section 2.3, which gives $(1,-i,-1,i)$ the eigenvalue $i$, this
  state has the eigenvalue $e^{-i\varphi_n}$, and $e^{i\varphi_n}$ is the eigenvalue of $T$. The allowed phases and
  the set of eigenstates are the same, and only the label $n$ becomes $-n$.
- (2.7) and the sum $\sum_n e^{in(\varphi'-\varphi)}=\delta_{\varphi\varphi'}$ of Section 2.5 miss the factor $L$, and
  (2.8) holds for the normalized operators.
- Section 2.4 writes the ring of five sites with $H=\sum c_i^\dagger c_j$ and says that the weight of site 1 is $1/5$
  for every $n$, for the lowest energy and for all other states. With this plus sign the lowest level has two states,
  and the weight $1/5$ holds for its two Fourier modes, not for every state of the level. With $-t$, as in the
  figure of the same paragraph, the lowest state is single and it holds as written.
- The try-it of Section 2.5 starts at $\eta=0.3$ and says that the extra extremum comes when it is increased to 0.5.
  Since $0.3>t/4$ the band at 0.3 already has it, with a dip of only $0.033t$.
- The first notebook box of Section 2.5 asks to check the chain of the notebook against $-2t\cos\varphi$, with no
  word on the sign. The cell has `tij=[1.0,0.]`, which gives $+2\cos\varphi$.
- The notebook box of Section 2.7 says that the ladder section can be checked against $\epsilon_\pm$ of (2.13). The
  ladder has the bands $2\cos\varphi\pm1$, and the chain of (2.13) is `bichain()`.
