# Conventions of Session 9, checked by number

This sheet fixes the signs, the units and the pyqula facts that the pages, the figures and the pyqula scripts of
Session 9 use. An agent that edits the session reads it first and does not work these out again. Every bullet was
checked with a number on 2026-11-21. Two drafts were written apart, and a third calculation settled each line where
they differed or where only one of them had a line that a page needs. The energies are in units of the hopping $t$,
and the lattice constant is 1. The pyqula of the checks is the development tree of version 0.0.95, at commit
7567127, as `pyqula.__version__` gives. Session 9 takes the $U$ of the Hubbard model (1.7), the density of states $D(E_F)$ of the Stoner criterion
(6.3) and the Nambu spinor (5.6) as `webnotes/conventions/session06.md` and `webnotes/conventions/session05.md` define
them, with no change. A statement that is not on this sheet is checked before a page claims it. The check is
`webnotes/checks/session09/conventions.py`, which prints one line per bullet below, in the same order.

## The definitions shared with Sessions 5 and 6

- $D(E_F)$ is the $g(\omega)$ of (2.16) at $\omega=E_F$, per spin and per site, and at a temperature it is
  $-\frac1N\sum_k n_F'(\varepsilon_k)$, the same density of states averaged over the thermal window. The half-filled
  chain has $D(E_F)=1/(2\pi t)=0.159/t$, and `h.get_dos(mode="Green", delta=1e-3)` gives 0.159 with `has_spin=False`
  and 0.318 with the two spins, since it sums over the spins of the Hamiltonian. The bare `h.get_dos()` gives 0.18
  with `has_spin=False`, on its default mesh and energy grid, so a page quotes the call with the Green mode. The
  identity $Un_\uparrow n_\downarrow=\frac U4(n^2-m^2)$
  of Section 9.5b holds as an operator on the four states of one site.
- pyqula builds the BdG Hamiltonian in the basis (5.6). After `h.add_exchange([0,0,0.3])` and `h.add_swave(0.1)` the
  onsite block of the chain has $0.3,-0.3,0.3,-0.3$ on its diagonal and 0.1 at the places (0,2) and (1,3). So an
  exchange field has the same sign in the electron and in the hole block, while the hopping $+t$ is $-t$ in the hole
  block. `h.get_gap()` is the full gap $2\Delta$, 0.6 for `add_swave(0.3)`, and the notebook divides it by two to get
  $\Delta$.

## The classical magnet and perturbation theory

- In the mean-field Ising magnet with $zJ=T_c$ on two sublattices, $1/\chi=T$ for the paramagnet, $T-T_c$ for the
  ferromagnet and $T+T_c$ for the antiferromagnet, the three lines of (9.1). The self-consistent moments in a small
  field give $1/\chi=0.500$ and 2.500 for the two magnets at $T=1.5T_c$, and 2.000 and 4.000 at $3T_c$. The quiz line
  $1/\chi\propto T+30$ gives 90 at 60 K, where the paramagnet gives 60.
- The coefficient of $|m\rangle$ in (9.3) is $\langle m|V|n\rangle/(E_n^{(0)}-E_m^{(0)})$. It is negative for a level
  above $|n\rangle$ when $\langle m|V|n\rangle>0$, as the figure `mixing` draws. The exact eigenvector of five levels
  with $\langle m|V|n\rangle=10^{-4}$ gives the same four coefficients to $10^{-3}$.

## The sign of the response

- The static Lindhard function (9.4) is positive, and an onsite energy $v$ lowers the density,
  $\delta n(q)=-\chi_0(q)\,v(q)$. So $\chi_0$ is the response to a shift of the chemical potential, which is $-v$, and
  it is minus the $\chi_A=\partial A/\partial\lambda$ of (9.3) for the density and the perturbation $V=\sum_iv_in_i$.
  On a ring of 400 sites at $\mu=-t$ and $T=0.05t$ the exact $\delta n/v$ is $-0.1848$, $-0.1929$ and $-0.3475$ at
  three values of $q$, where (9.4) gives the same three numbers with a plus sign.
- One impurity $v_0$ on one site gives $\delta n(x)=-v_0\int\frac{dq}{2\pi}e^{iqx}\chi_0(q)$, with a minus sign, so a
  repulsive impurity lowers the density on its site. On the same ring $\delta n(0)/v_0=-0.250$, and the Fourier sum
  of (9.4) with the minus sign agrees with the exact density to $10^{-5}$ on every site.
- `h.get_chi(energies=..., q=..., nk=..., delta=..., T=...)` returns minus the complex conjugate of (9.5), per site,
  with `delta` in the place of $0^+$ and `q` in units of $2\pi$. At $\omega=0$ it is $-\chi_0(q)$ of (9.4), negative
  like $dn/dv$, and for $\omega>0$ its imaginary part is positive, as the imaginary part of (9.5) is. At $q=0.1$ and
  $\omega=0.5t$ with `T=delta=0.05`, (9.5) is $0.1977+0.0081i$ and pyqula gives $-0.1977+0.0081i$. With no `T` the
  temperature is `delta`, and with the two spins the result is twice as large, $-0.329$ where `has_spin=False` gives
  $-0.164$.

## The Lindhard function

- $\chi_0(q\to0)=D(E_F)$ per spin. The chain gives $0.1838=1/(\pi v_F)$ at $\mu=-t$, 0.2251 at quarter filling and
  $1/(2\pi t)=0.1592$ at half filling, where pyqula gives the same number.
- The 1D free-electron form $\chi_0(q)=\frac{m}{\pi\hbar^2q}\ln\left|\frac{2k_F+q}{2k_F-q}\right|$ of Section 9.6a is
  spinless and per unit length. It agrees with the sum over the Fermi sea to $10^{-3}$ at $q/k_F=0.3$, 1.0, 1.7 and
  2.6, and its limit at $q\to0$ is $1/(\pi\hbar v_F)$.
- $\chi_0(2k_F)$ grows as $\ln(1/T)$. Its slope against $\ln(1/T)$ is $D(E_F)=0.1592$ for the half-filled chain, where
  $2k_F=\pi$ and $-2k_F$ are the same vector, so two pairs of Fermi points add. At a generic filling only one pair
  enters and the slope is $D(E_F)/2$, 0.1126 at quarter filling and 0.0919 at $\mu=-t$. So
  $\chi_0(2k_F)\approx\frac{D(E_F)}{2}\ln(W/T)$ at a generic filling, and $D(E_F)\ln(W/T)$ at half filling. The
  half-filled chain has $\chi_0(\pi)=0.863$ at $T=0.02t$ and 0.974 at $0.01t$, and pyqula gives the same 0.863.
- At quarter filling of the spinless chain $k_F=\pi/4$, the Fermi level is at $-\sqrt2\,t$, and $\chi_0(q)$ at
  $T=0.01t$ is largest at $q=\pi/2=2k_F$, as the quiz of Section 9.4b says.
- The half-filled square lattice at $T=0.1t$ has $\chi_0(0,0)=0.264/t$ and $\chi_0(\pi,\pi)=0.677/t$, on k-meshes of
  120 and 240 and from the elliptic density of states, with the ratio 2.57 and the thresholds $1/\chi_0=1.48t$ for
  the antiferromagnet and $3.79t$ for the ferromagnet. These numbers hold at $T=0.1t$ only. At $T=0.05t$ they are
  $0.299/t$ and $0.872/t$, with the thresholds $1.15t$ and $3.35t$. The value at $\Gamma$ is the density of states
  averaged over $-\partial f/\partial\varepsilon$, as on the sheet of Session 6, since $D(E)$ itself diverges at the van
  Hove point $E=0$. A page that quotes 0.26, 0.68, 2.6, 1.5 or 3.8 says $T=0.1t$.
- At half filling $\chi_0(0,0)$ grows as $\ln(1/T)$, by $\ln2/(2\pi^2)=0.035$ for each halving of $T$, and
  $\chi_0(\pi,\pi)$ grows as $\ln^2(1/T)$, with the second differences $\ln^22/(2\pi^2)=0.024$, from $T=0.2t$ to
  $0.0125t$. So the enhancement at $(\pi,\pi)$ is the square of a logarithm.
- On a $200\times200$ mesh at $T=0.1t$, $\chi_0(\pi,\pi)/\chi_0(0)=2.57$ at half filling. The figure `lindhard_map`
  uses `h.get_chi` with `integration="triangle"` on a $31\times31$ k-mesh, which gives $0.264/t$ and $0.677/t$ and the
  ratio 2.56, the 2.6 of its caption. On the $200\times200$ mesh at $\mu=-3t$ the Fermi surface has $k_F=1.03$ from
  its area, $\pi k_F^2=(2\pi)^2n$, between 1.02 along the diagonal
  and 1.05 along the axes. Along $q_x$ the ratio $\chi_0(q)/\chi_0(0)$ is 1.03 and 1.06 at 0.5 and 0.9 times $2k_F$,
  and 0.68 and 0.56 at 1.2 and 1.5 times $2k_F$. So it is flat inside $|q|=2k_F$ to six percent and falls outside it.
- pyqula's chain has the band $2\cos k$, and `h.add_onsite(mu)` adds `mu` to every onsite energy, so the band moves
  up and the Fermi level, at zero, goes down in it. So the `mu` of the notebook is $-\mu$ of the notes, as the sheet
  of Session 5 says for `add_onsite`, and `mu = 1.` is the $\mu=-t$ of the lines above, where `get_dos` of the
  spinless chain gives $D(E_F)=0.1838$. With `mu = 0.` the Fermi points are at 0.25 and 0.75 and the
  vector between them is 0.5. With `mu = 1.` they are at 1/3 and 2/3, so the vector is 1/3 and its mirror 2/3, in
  units of $2\pi$. The static pyqula $\chi_0$ with `mu = 1.` is largest at $q=1/3$ of the four values 0.25, 1/3, 0.4
  and 0.5, as the try-it of Section 9.4b says.

## The random phase approximation and the Stoner instability

- With $\chi_0$ per spin and positive, the Hubbard $U$ of (1.7) gives the response $-2\chi_0/(1+U\chi_0)$ of the total
  density to an onsite energy, so $dn/d\mu=2\chi_0/(1+U\chi_0)$, and the response $2\chi_0/(1-U\chi_0)$ of
  $n_\uparrow-n_\downarrow$ to a field $-h(n_\uparrow-n_\downarrow)$. The factor 2 counts the spins and drops out of
  the ratio $\chi/\chi_0$ of (9.6) and of (9.8). On a Hubbard ring of 200 sites with $U=t$, $\mu=-t$ and $T=0.1t$, the
  self-consistent Hartree response is $-0.3442$ for the density and 0.5248 for the spin, the two formulas to four
  digits.
- pyqula has the same denominators. On the paramagnetic chain with $U=t$ and `delta=0.01`, `get_densitychi_RPA` at
  $q=\pi/2$ is $-0.331=-2\chi_0/(1+U\chi_0)$ with $\chi_0=0.198$. Minus the trace of `get_spinchi_ladder` with
  `RPA=False` is the $\chi_0$ of (9.4) per spin, 0.198 at $q=\pi/2$ and 0.970 at $q=\pi$, and `RPA=True` multiplies
  it by $1/(1-U\chi_0)$, which is 1.247 and 33.7.
- (9.8) is the threshold of the self-consistent mean field. A real-space Hartree-Fock loop of (1.7) on a $16\times16$
  torus at $T=0.1t$ and $U=t$ multiplies a small staggered moment by 0.7038 and a uniform one by 0.3490 in one step,
  which are $\chi_0(\pi,\pi)$ and $\chi_0(0)$ on the same mesh. So the moment grows when $U\chi_0>1$. At $U=1.7t$ the
  loop converges to the moment 0.270 that the gap equation gives.
- The quizzes of Sections 9.5a and 9.5b use $U\chi_0=0.68$. This gives $\chi=0.68/1.68=0.405/t$ for $U=t$,
  $\chi/\chi_0=0.595$ for the charge and 3.125 for the spin, and $1.5\times0.26=0.39$ for the ferromagnetic channel at
  $U=1.5t$.
- `geometry.bichain()` has both hoppings equal to 1, so its bands touch at zero energy at $k=\pi$ and it is not a
  dimerized chain. In the second cell of "The charge-charge response function", `add_antiferromagnetism(0.5)` is only
  the starting point `mf` of the loop. Started from 0.5 or from 0.2, the loop at $U=2t$ ends at the same splitting
  $Um=0.681$, which the gap equation of the antiferromagnet gives.

## The plasmon

- Above the particle-hole continuum $\chi_0(q,\omega)$ of (9.5) is negative. Summed over the two spins it goes to
  $-nq^2/(m\omega^2)$, with $n$ the density of both spins, and for one spin to half of it. At $q=0.1k_F$ and
  $\omega=1.2\hbar k_F^2/m$ the closed form of Lindhard and the sum over the Fermi sea of both spins give $-0.002325$
  in units of the $N(0)$ of both spins, and $-nq^2/(m\omega^2)$ is $-0.002315$. Since 2026-11-22, the pick of the
  lecturer, Section 9.5a says that the $\chi_0$ of (9.6) counts one spin and that an interaction on the total density
  gives the denominator $1+2v(q)\chi_0$. So the plasmon is a zero of $1+2v(q)\chi_0$, at $\omega_p$ as $q\to0$. The
  denominator $1+v(q)\chi_0$ would put it at $\omega_p/\sqrt2$, 0.7073 for $q=0.02k_F$, and $1-2v(q)\chi_0$ has no
  zero above the continuum. The zero gives $(\omega^2-\omega_p^2)/(v_Fq)^2=0.6000$ as $q\to0$, the $\tfrac35$ of (9.7).
- The particle-hole continuum of the electron gas lies below $\omega_+=v_Fq+\hbar q^2/2m$, and above
  $\omega_-=\hbar q^2/2m-v_Fq$ when $q>2k_F$, as the caption of Figure 9.2 says. A sampling of the Fermi sphere at
  $q=0.5$, 1.5 and $2.5k_F$ gives these edges to 0.005.

## Friedel oscillations

- The density around one impurity decays as $1/r^d$, as (9.9) says. A fit by $r^{-p}(A\cos2k_Fr+B\sin2k_Fr)$ gives
  $p=1.00$, 1.98 and 2.97 for the continuum forms in $d=1,2,3$, and 1.00 and 1.98 for the first-order density of the
  chain at $\mu=-t$ and of the square lattice at $\mu=-3t$.
- The change of the LDOS at one energy decays as $1/r^{d-1}$, one power slower. The fit gives 0.00, 1.01 and 1.99 in
  $d=1,2,3$ with the damping of the broadening divided out. In a chain the LDOS change at $E_F$ falls only through
  the broadening, as $e^{-2\delta x/v_F}$, which is $e^{-0.0115x}$ for `delta=0.01` at $\mu=-t$. The figure `friedel`
  and the widget show the density, with $1/x$, and the figure `friedel2d` and the notebook cells show the LDOS at one
  energy. The notebook text $\delta\rho(x)\propto\cos(2k_Fx)/x$ for the LDOS of the chain holds for the density only.
- The figure `friedel`, one impurity $v_0=t$ in a chain of 4001 sites, has the periods $\pi/k_F=4.88$ and 3.00 sites
  for $\mu=-1.6t$ and $-t$, the power 1.00 for both beyond the first few sites, and $\delta n(0)=-0.147$ and $-0.188$
  on the impurity.
- pyqula's chain with `tij=[1]` and `add_onsite(mu)` has the band $2t\cos k$ plus `mu`, so for `mu` close to 2 the Fermi
  level is close to the band bottom at $k=\pi$, and $k_F$ is measured from there. Then $\pi/k_F$ is 14.0, 5.66 and
  3.00 sites for `mu` = 1.95, 1.7 and 1.0, and the embedding LDOS of the cell "Impurity in a 1d metal" oscillates with
  the periods 14.2, 5.65 and 3.00. On the square lattice the LDOS maxima along $x$ repeat every 7.0 and 3.0 sites for
  `mu` = 3.8 and 3.0, the $\pi/k_F$ of the pocket around $(\pi,\pi)$, 6.97 and 3.00. So the try-its of Sections 9.6a
  and 9.6b hold.
- At $E=-3.4t$ the square lattice has $k_F=0.795$ along the axes, so $\pi/k_F=3.95$ sites, as the caption of
  `friedel2d` says. A chain with $k_F=\pi/4$ has the period 4 of the quiz of Section 9.6a.
- `add_sublattice_imbalance(m)` on `bichain` gives the onsite energies $\pm m$ and the gap $2m$, so the cell "Impurity
  in an electronic insulator" with `gaps = [0.1,0.3]` has the gaps 0.2 and 0.6, as its plot titles print. At $E=0$,
  the middle of the gap, the LDOS change decays as $e^{-\kappa x}$ with $\kappa=2\,\mathrm{asinh}(m/2t)$, which is
  0.100 per site for $m=0.1$ and 0.299 for $m=0.3$, the lengths 10.0 and 3.35 sites.

## Yu-Shiba-Rusinov states

- (9.10) holds with $\alpha=\pi\nu_0JS$, where $JS$ is the exchange energy of the site, the `J` of
  `add_exchange([0,0,J])`, which is $+JS$ for one spin and $-JS$ for the other, and $\nu_0=D(E_F)$ per spin. It holds
  to all orders in $J$, and its first order $1-2\alpha^2$ gives 0.5 at $\alpha=0.5$, where the lattice gives 0.600.
  On the lattice it holds when $\Delta$ is small next to the distance from $E_F$ to the band edge. From
  $\det(1-Jg(E))=0$ on the chain the largest error over $JS=0.5$, 1 and 3 is $0.000\Delta$ at half filling with
  $\Delta=0.02t$, $0.004\Delta$ with $\Delta=0.2t$, and $0.105\Delta$ at $\mu=1.8t$ with $\Delta=0.2t$.
- A pyqula ring of 300 sites with `add_exchange` on one site and `add_swave(0.1)` at half filling, where
  $\alpha=JS/2t$, gives $|E_b|=0.6005\Delta$ for $JS=t$ and $0.3837\Delta$ for $3t$. The T-matrix gives the same
  numbers, and (9.10) gives 0.6000 and 0.3846. With $\Delta=0.2t$ the level of the half-filled chain crosses zero at
  $JS=\sqrt{4t^2+\Delta^2}=2.01t$, from $\det(1-Jg(0))=0$ and on a ring of 400 sites, which is the $\alpha=1$ of (9.10)
  to 0.5 percent, as the caption of `g5_ysr_dos` says.
- In the cell "Single magnetic impurity in a superconductor", with `h.add_onsite(1.8)` and $\Delta=0.2t$, the level
  crosses zero at $J=1.04t$, while $\alpha=1$ gives $J=1/(\pi\nu_0)=v_F=0.872t$. $\Delta$ is not small next to the
  $0.2t$ between $E_F$ and the bottom of the band, so (9.10) does not hold there.
- Across the crossing the electronic ground state changes from $S^z_{\rm tot}=0$ to $|S^z_{\rm tot}|=1/2$, as Section
  9.7 says. In the block $(c_\uparrow,c_\downarrow^\dagger)$ of (5.6) on a ring of 400 sites with $\Delta=0.1t$,
  $S^z_{\rm tot}$ is half the number of negative levels minus the number of sites, which is 0 for $JS=t$ and $-1/2$
  for $3t$.
- A non-magnetic impurity leaves the gap. A potential $2t$ or $10t$ on one site of the same ring keeps the lowest level
  at $\Delta$ to $10^{-6}$. The quiz numbers of Section 9.7 hold, 0.6 at $\alpha=0.5$, $-0.6$ at $\alpha=2$ and
  $-0.18$ at $\alpha=1.2$.

## Vacancies in topological matter

- The figure `vacancy_dos` runs the pyqula script `g5_vacancy_honeycomb.py`, with `add_haldane(0.3/sqrt3)`, which is
  $t_2=0.15t$ with the phase $\pi/2$, and `add_sublattice_imbalance(0.78)`, the mass $M=0.78t$. On the $18\times18$
  torus, $t_2=0.15t$ gives the gap $1.559t$ and one level at $E=0$ with 0.45 of its weight on the three neighbors of
  the vacancy, and $M=0.78t$ gives the gap $1.56t$ and no level inside it. A numpy Haldane model of our own, with $t_2$,
  the phase $\pi/2$ and $M$ on the same torus, gives the same numbers.
- For $t_2=0.1t$ and $M=0.3t$ the gap edges are $\pm0.2196t$. In the infinite lattice a vacancy binds a state where
  the local Green's function of its site vanishes. This is at $-0.135t$ for the vacancy on the sublattice with $+M$
  and at $+0.135t$ on the other one, for either sign of the phase. The $18\times18$ torus gives $-0.130t$ and the
  pyqula embedding $-0.14t$. At $M=0.4t$ the edge is $0.120t$ and the state is at $-0.116t$, close to the edge.
- For $t_2=0.1t$ and $M=0.5t$ the Chern number is still 1 and the gap is $0.039t$, but a vacancy binds no state that
  is separated from the band. $G_{AA}$ of the infinite lattice stays between $-0.24$ and $-0.18$ from the upper edge up
  to $10^{-4}t$ above the lower one, and it is $-0.197$ at $E=-0.016t$. The top of the valence band at the valley with
  the small gap sits on the removed sublattice, so $G_{AA}$ diverges as a logarithm at the lower edge and its zero is
  exponentially close to it. For the vacancy on the other sublattice $G_{BB}$ stays between 0.18 and 0.24, and it is
  0.236 at $E=-0.016t$. The $18\times18$ torus has a level at $-0.006t$ with 0.014 of its weight on the neighbors, a
  level of the finite torus.
- A vacancy in an SSH ring of hoppings $0.5t$ and $t$ leaves a level at zero for either order of the hoppings, since the
  open chain that is left has an odd number of sites. So this zero level does not tell the two phases apart. It sits
  on the neighbor joined to the vacancy by the strong bond, with 0.75 of its weight there, which is the end of the open
  chain whose last bond is weak. An onsite energy $2t$ there leaves no level in the gap $\pm0.5t$, and on the other
  neighbor the zero level stays and a second one appears at $-0.308t$.
- In the notebook cells of the vacancy in a superconductor, `add_pairing(mode="chiral_pwave", delta=0.1)` with
  `add_onsite(-4.0)` has the gap edge 0.2996 = `h.get_gap()/2`, just below three times `delta`, and `h.get_chern()` =
  $-2$, as the link variables give. The $2\times2$ cell of the notebook has the same `h.get_gap()` 0.5992 as the cell
  of one site, the number of the sheet of Session 5. In the infinite lattice a vacancy binds levels at $\pm0.714$ of the
  gap edge, $|E|=0.214$, each
  twice, from the zeros of the local Green's function of the removed site. They are not at zero energy, so they are
  not a protected zero mode. With `mode="swave"` the gap edge is 0.100 and the same Green's function has no zero
  inside it, so there is no bound state.

## Screening in a quantum magnet

- The figure `spinon_impurity` is a mean-field spinon chain, not the Heisenberg chain. For uniform $\chi$ the moment
  changes sign on every site. $n|m_n|$ is between 0.0038 and 0.0045 for $n=2$ to 31 in the open chain of 2000 sites
  of the figure, and between 0.0038 and 0.0040 in the infinite chain, from the Dyson equation. So the points follow
  $1/n$ to about 13 percent, with the largest difference at $n=31$.
- For $\chi$ alternating 1 and 0.6, with the gap $2(1-0.6)\chi=0.8\chi$, the partner of site 0 in its dimer has
  $-0.81$ of the moment of site 0, which is 0.66 of all the moment off site 0, and the other neighbor $-0.05$. The
  moment decays at 0.57 and 0.53 per site on the two sublattices from $n=10$ to 40, which tends to $\ln(1/0.6)=0.51$.
  It falls below $10^{-8}$, the lower end of the panel, from $n=20$ on the sublattice of site 0 and from $n=27$ on the
  other one, so the panel draws the points up to $n=18$ and $n=25$. At every point above $10^{-8}$ the diagonalization
  of the figure agrees with the Dyson equation to $10^{-6}$, so the points of the panel are not round-off.

## Anderson localization

- For $w_n$ uniform in $[-W,W]$, the localization length at $E=0$ from a transfer matrix of $10^5$ sites, with
  $|\psi|\sim e^{-x/\xi}$, has $\xi W^2$ between 23.6 and 28.7 over 6 seeds and $W=0.25t$, $0.5t$ and $t$, so
  $\xi\approx26\,(t/W)^2$, near the $105/4=26.25$ of perturbation theory at the band center. $\xi(0.5t)$ is 98 to 108
  sites, so a sample of 100 sites looks metallic below about $W=0.5t$, as the figure `localization_length` says.
- With this $\xi$ the typical conductance of a segment of length $L$ falls as $e^{-2L/\xi}$. At $W=t$,
  $\langle\ln T\rangle$ is $-16.2$ and $-32.9$ for 200 and 400 sites, a slope 0.084 per site, where $2/\xi=0.079$.
- `h.get_tails()` fits $\ln|\psi|^2$ and returns the decay rate of the density, $2/\xi$. The bound state of an
  impurity $2t$ in a chain of 200 sites, $|\psi|\sim e^{-\kappa n}$ with $\kappa=0.881$, gives $1.763=2\kappa$, and a
  state $e^{-|n|/5}$ gives 0.400. On the notebook chain of 400 sites with $v\cos(\sqrt2\pi x)$ its mean is 0.004,
  0.756 and 1.408 for $v=t$, $3t$ and $4t$, against 0, $2\ln(v/2t)=0.811$ and 1.386, so the self-dual point is $v=2t$
  for this wavevector too. The axis $1/\lambda$ of the notebook is for $|\psi|^2$, and its legend
  $|\Psi(r)|\sim e^{-|r|/\lambda}$ is off by a factor 2.
- The notebook draws the random potential as `v*(np.random.random()-0.5)`, uniform in $[-v/2,v/2]$, so its `v` is
  $2W$.
- In the figure `aah_ipr`, $N\cdot\mathrm{IPR}$ is 1.50 at $V_0=0$, since the real eigenvectors of the degenerate pairs
  are standing waves, while a plane wave gives 1. For $N=55$, 233 and 987 it is about 1.7 at $V_0=0.5t$, 2.00 to 2.10
  at $V_0=t$, 2.6 to 2.9 at $1.5t$ and 4.5 to 6.0 at $1.9t$. Above $V_0=2t$ the IPR does not depend on $N$, 0.418,
  0.411 and 0.409 at $V_0=2.5t$ and 0.549, 0.543 and 0.542 at $3t$.
- In the 3D Anderson model at $W=20t$ the density of states at the band center is about 0.022 to 0.027 states per site
  and per unit of energy in $|E|<5t$, over 8 cubes of $10^3$ sites, as the quiz of Section 9.10b says. This is
  $1/(2W)=0.025$, the height of the distribution of $w_n$, and the spectrum lies inside $\pm(6t+W)$.
- The numbers of the quizzes of Sections 9.6, 9.9 and 9.10 hold. The IPR of ten equal sites is 0.1, a factor
  $2^{-0.5}=0.71$ gives $\tau=0.5$, $e^{-4}=0.018$, and $\cos(\pi x/2)$ has the period 4.

## Not checked by a number

Three statements of the figures have no check here. The critical disorder $W_c\approx8t$ of the figure `mobility`,
about $16.5t$ for the full width $2W$ of the box, is a value of numerical work on the 3D Anderson model. The spin-1
Heisenberg chain has a correlation length of about 6 sites in numerical work, so the $\xi=2.5$ of Figure 9.5 and of
its quiz is a drawn value and not the one of the spin-1 chain, and the spin-1/2 chain has a logarithmic correction to
$1/n$ that the mean-field spinons do not have. The script `webnotes/figures/session09/spinon_impurity.py` gives the same
SVG at every run since 2026-11-22, since it draws only the points above $10^{-8}$ and rounds them, so a redraw needs no
restore from git.

## Points of the old text, corrected, decided or open on 2026-11-22

These restate lines above for the pages they concern. They were open points of the old text, and the plan of the
session records what happened to each one on 2026-11-22. The check prints them in this order.

These were wrong by the numbers above, and they are corrected on the web.

- The caption of Figure 9.2 called the plasmon a zero of $1-v(q)\chi_0$. With (9.6), the positive $\chi_0$ of (9.4)
  and the $\chi_0$ of one spin, it is a zero of $1+2v(q)\chi_0$, see the plasmon lines, and the caption on the page now
  says so. The render of the figure and its overlay are not changed.
- Section 9.6a wrote $\delta n(x)=\int\frac{dq}{2\pi}e^{iqx}\chi_0(q)\,v_0$ with no minus sign. The numbers give
  $\delta n(q)=-\chi_0(q)\,v_0$, so a repulsive impurity lowers the density on its site, and the page now has the
  minus sign.
- Section 9.7 said that (9.10) is the classical spin "in the Born approximation". It is the T-matrix to all orders in
  $J$, and its first order gives 0.5 at $\alpha=0.5$ where the lattice gives 0.600. The page now says "In the
  approximation of a classical spin".
- The second quiz of Section 9.8 said that $t_2=0.1t$, $\varphi=\pi/2$ and $M=0.5t$ give a vacancy state at
  $-0.016t$. The infinite lattice has $G_{AA}=-0.197$ and $G_{BB}=0.236$ there and no zero in the gap away from its
  edges, for either sublattice, and the $18\times18$ torus has its level at $-0.006t$. The quiz now says that this
  vacancy gives no level separated from the band edges.
- The try-it of Section 9.9 said that the cell compares a gap of 0.1 with a gap of 0.3. The gaps are 0.2 and 0.6,
  and 0.1 and 0.3 are the onsite energies $\pm m$, as the box now says.
- The notebook box of Section 9.6b said that in the gapped chain the LDOS converges to its bulk value within one or
  two sites. In that cell the LDOS change decays over 10.0 and 3.35 sites, which the box now gives as 10 and 3.3.
- The try-it and the notebook box of Section 9.5b and the notebook box of Section 9.9 called `geometry.bichain()` a
  dimerized chain. Its two hoppings are equal, and the boxes now say so. The cell "The impact of a strong impurity" of
  the box of Section 9.9 compares an s-wave superconductor, a sublattice insulator and a p-wave superconductor, as the
  box now says.
- The second quiz of Section 9.10b gave the density of states of the Anderson insulator at $W=20t$ as about
  $1/W=0.05/t$. It is $1/(2W)=0.025/t$ for $w_n$ in $[-W,W]$, as the quiz now says.

These depended on a condition that the page did not write, and the page now writes it or no longer says it.

- The first quiz of Section 9.8 gives $-0.14t$ for $M=0.3t$. This holds for the vacancy on the sublattice with $+M$,
  as the feedback says, and the other sublattice gives $+0.135t$.
- Section 9.8 and the caption of Figure 9.4 say that a vacancy binds an in-gap mode when the invariant is non-zero.
  Close to the closing of the gap the bound state of the Haldane model lies exponentially close to the band edge, so
  no separate peak is seen, which the opener of the page now says. The caption no longer says "if and only if" or
  "The rule is as direct as it looks".
- The quiz of Section 9.8 on the SSH chain holds only with the onsite energy on the neighbor joined to the vacancy by
  the strong bond, as its feedback now says, and on a ring the vacancy has its zero level for either order of the
  hoppings, as the key box says.
- The caption of the figure `stoner` gives $0.26/t$ as the density of states averaged over the thermal window at
  $T=0.1t$, since $D(E)$ diverges at $E=0$. Section 9.5b called $\chi_0(\pi,\pi)$ "logarithmically enhanced", and it
  grows as $\ln^2(1/T)$, where $\chi_0(0,0)$ grows as $\ln(1/T)$, so the page now says "enhanced" and gives the two laws.
- The second quiz of Section 9.10b wrote the conductance as $e^{-L/\xi}$. With the $\xi$ of the amplitude, which the
  figure `localization_length` draws, it is $e^{-2L/\xi}$, and the quiz now writes it so.
- The caption of the figure `aah_ipr` said that $N\cdot\mathrm{IPR}\approx2$ below $V_0=2t$. It is about 2 at
  $V_0=t$, and it goes from 1.5 at $V_0=0$ to about 6 at $1.9t$, so the caption now quotes $V_0=t$.

These were picked by the lecturer on 2026-11-22, and the pages now say so.

- Section 9.3 defines $\chi_A=\partial A/\partial\lambda$, and Section 9.4a calls (9.4) the response of the density to
  a shift of the onsite energy. With that definition the response is $-\chi_0$. Section 9.4a keeps (9.4) and now says
  after its key box that the density changes by $\delta n(q)=-\chi_0(q)\,v_q$, so $\chi_A=-\chi_0(q)\,v_q$, and the
  sentence before (9.4) has the denominator $\varepsilon(k)-\varepsilon(k+q)$ of (9.3).
- (9.6) is written without the factor 2 of the two spins, which leaves the ratio $\chi/\chi_0$ unchanged. Section 9.5a
  keeps (9.6) and now says after it that $\chi_0$ counts one spin and that an interaction on the total density gives
  the denominator $1+2v(q)\chi_0$, as $U\to2v(q)$, the caption of Figure 9.2 and the fold of the plasma frequency write.

These change a definition, a numbered equation or a rule that the .tex states, so they are the lecturer's to decide.

- The key box of Section 9.8 keeps the italic rule of the .tex, that an in-gap mode means a topological phase and no
  mode a trivial one. A vacancy in the SSH ring leaves its zero level in both orders of the hoppings, and for
  $t_2=0.1t$ and $M=0.5t$, with $C=1$, the bound state is not separated from the band edges.
