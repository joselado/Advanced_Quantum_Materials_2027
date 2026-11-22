# Conventions of Session 7, checked by number

This sheet fixes the signs, the units and the facts of pyqula and dmrgpy that the pages, the figures and the scripts
of Session 7 use. An agent that edits the session reads it first and does not work these out again. Every line was
checked with a number on 2026-11-21. Two drafts were written apart, and a third calculation settled each line where
they differed or where only one of them had it. The entropies are in nats, with the natural logarithm of (7.6),
unless a line says bits, and a number that changes from run to run is given as the range of the runs. The section on
the dimerized Heisenberg chain is written so that Session 8 can use it as it is. The checks ran with pyqula 0.0.95 of
the development tree at commit 7567127, dmrgpy at commit 3f73780 with its ITensor 3 backend, numpy 2.4.6 and scipy
1.18.0. A statement that is not on this sheet is checked before a page claims it. The check is
`webnotes/checks/session07/conventions.py`, which prints one line per bullet below, in the same order, in about
three minutes on a busy machine. The bond dimension of an MPS is $\chi$, as the notebook writes it with `maxm`, and the
matrices of (7.5) are $M^{s_i}_i$, picked by the lecturer on 2026-11-22. When the bonds differ, $\chi_i$ is the
dimension of the bond $i$. The bond dimension of an MPO is $D$. Section 10.4 writes $D$ for the bond dimension of an
MPS, and its line below says so.

## Spins, units and the numbering of sites

- The spins are $\mathbf S=\boldsymbol\sigma/2$ with $\hbar=1$, and $J>0$ is antiferromagnetic. The dimer
  $J\,\mathbf S_0\cdot\mathbf S_1$ has the singlet at $-\frac34J$ and the triplet at $+\frac14J$, so the gap is $J$. A
  product state of two spins at the angle $a$ has $\frac14\cos a$, from $-\frac14$ for antiparallel spins to
  $+\frac14$, and the singlet (7.3) has $\langle S^z_0\rangle=0$. In dmrgpy `sc.Sx[i]`, `sc.Sy[i]` and `sc.Sz[i]` of
  `spinchain.Spin_Chain(["S=1/2"]*L)` are these spins, since two sites give $-0.75$ and
  $\langle\mathbf S_0\cdot\mathbf S_0\rangle=0.75$.
- The logarithm of the pages is the natural one, as in (7.6), in the notebook, in dmrgpy and in pyqula. A figure that
  draws $S/\ln2$ says that it is in bits. The state $\cos\vartheta\,|{\uparrow\downarrow}\rangle+\sin\vartheta\,
  |{\downarrow\uparrow}\rangle$ has $S=-\cos^2\vartheta\ln\cos^2\vartheta-\sin^2\vartheta\ln\sin^2\vartheta$, which is
  0, 0.4165 and $\ln2=0.6931$ at $\vartheta=0$, $\pi/8$ and $\pi/4$. The singlet (7.3) is $\vartheta=-\pi/4$, with the
  same $\ln2$.
- Sites are counted from 0, as in the notebook and in dmrgpy. A cut is named by the number of sites on its left, "the
  cut after $\ell$ sites", and a bond by its two sites, $(i,i+1)$. `wf.get_bond_entropy(i, i+1)` of dmrgpy is the
  entropy of the first $i+1$ sites. So the call `get_bond_entropy(L//2, L//2+1)` of the notebook takes $L/2+1$ sites,
  one more than half, and the plot of the cell "Entanglement entropy of the ground state" puts the cut after $j+1$
  sites at its bond number $j$. For the Heisenberg chain of 10 sites the nine values agree with exact diagonalization
  to $10^{-9}$, 0.6931, 0.4079, 0.7262, 0.4923, 0.7379, 0.4923, 0.7262, 0.4079 and 0.6931.
- The numpy figure scripts store a state in two orders. `schmidt_spectrum.py`, `dmrg_sweeps.py`, `quench_entropy.py`,
  `xx_spectrum.py` and `dimer_entropy.py` build it with `np.kron` and site 0 as the first factor, so the first $\ell$
  sites are `psi.reshape(2**l, -1)`. `random_vs_gapped.py` and `matrix_vs_vector.py` store site $i$ as bit $i$ of the
  index, so the first $\ell$ sites are `psi.reshape(-1, 2**l)`. With a field on site 0 of 8 sites the two give the
  same 0.6715 for the first 3 sites, and the wrong reshape gives 0.6933, the entropy of the last 3 sites.

## The Jordan-Wigner transformation

- In (7.2) an occupied site is an up spin, $n_i=S^z_i+\frac12$, and
  $K_i=\exp(i\pi\sum_{j<i}n_j)=\prod_{j<i}(1-2n_j)$, which is $-1$ to the power of the number of fermions on the left.
  With $c_i=K_iS^-_i$ the operators anticommute and $S^+_i=c^\dagger_iK_i$, checked as $32\times32$ matrices on 5
  sites. $K_6$ is $-1$ for three fermions on the sites 0 to 5 and $+1$ for two, as the quiz of Section 7.2b says, and
  the string of the first site is 1, since its sum is empty.
- For neighbors the strings cancel, $S^+_iS^-_{i+1}=c^\dagger_ic_{i+1}$ and $S^-_iS^+_{i+1}=c^\dagger_{i+1}c_i$, so
  the open XX chain $J\sum_i(S^x_iS^x_{i+1}+S^y_iS^y_{i+1})$ is free fermions with the hopping $+J/2$. The 64 levels
  of 6 sites are the sums of the single-particle levels $J\cos(\pi k/7)$, $k=1$ to 6, with $N=S^z_\text{tot}+3$
  fermions, which is the figure `xx_spectrum`. The hopping $-J/2$ gives the same levels on an open chain, and so does
  pyqula `chain()` with the hopping $\frac12$, so a page does not take the sign of the hopping from the levels.
- The term $S^z_iS^z_{i+1}$ is $(n_i-\frac12)(n_{i+1}-\frac12)$, a density interaction between neighbors, so the
  Heisenberg chain is a chain of interacting fermions and only the XX chain is free. For 8 sites the spins give
  $-3.374933J$, and so do the dmrgpy fermions of `pyqula2dmrgpy` with this interaction added, while the free part
  alone gives $-2.379385J$. The correlation matrix of pyqula gives the XX chain, and the Heisenberg chain needs dmrgpy
  or exact diagonalization.
- The entropy of a block of consecutive sites is the same for spins and for fermions. The string of a site of the
  block runs over the sites on its left, and the part outside the block cancels in every operator that keeps the
  number of fermions. The XX chain of 10 sites has the energy $-3.01334J$ and the same entropies from the spins, from
  the fermion correlation matrix and from the dmrgpy fermions, $\ln2$ at the first cut and 0.7578 at the center. On
  12 sites the block of the sites 3 to 6 has 1.2666 in both languages, and the sites 3 to 7 have 1.1889. Two separate
  blocks do not agree, and the sites 1 to 3 with 8 and 9 have 1.7365 with spins and 1.8007 with fermions.
- On a ring the closing bond is $S^+_{L-1}S^-_0=-(-1)^Nc^\dagger_{L-1}c_0$, so the fermions are periodic for an odd
  number $N$ of fermions and antiperiodic for an even $N$. The XX rings of 6 and 8 sites have $-2.000000J$ and
  $-2.613126J$, which the free fermions give with periodic conditions for $N=3$ and antiperiodic ones for $N=4$. So a
  half-filled ring of $N=2$ modulo 4 sites in pyqula, which is periodic, is exactly the XX spin ring.

## The size of the Hilbert space and the memory

- The dimension is $2^L$, so 4, 8 and 16 for $L=2$, 3 and 4, and the step from 10 to 11 sites adds 1024 coefficients.
- numpy stores a complex number in 16 bytes, and the dashed lines of `memory_scaling` and `matrix_vs_vector` are $10^9$
  bytes, so a page uses GB for $10^9$ bytes. The state of $L=26$ spins is the first one above this line, with
  $2^{30}=1.07\times10^9$ bytes, and the dense matrix of $4^L$ numbers passes it at $L=13$. $L=30$ needs
  $1.72\times10^{10}$ bytes, 17.2 GB or 16 GiB, and $L=40$ needs $1.76\times10^{13}$ bytes, 17.6 TB or 16 TiB.
- The open Heisenberg chain has $(L+1)\,2^{L-1}$ nonzero elements in the basis of $S^z$ products for even $L$, 40,
  224, 1152, 5632 and 26624 for $L=4$ to 12, so the sparse matrix is $(L+1)/2$ times the vector. For odd $L$ some
  diagonal elements vanish, and $L=5$ and 7 have 84 and 472 instead of 96 and 512. The counts come from the sparse
  matrix and, for 8 sites, from the `np.kron` matrix too.

## Matrix product states

- An open MPS of spins $\frac12$ stores $\sum_i2\chi_{i-1}\chi_i$ numbers, with $\chi_0=\chi_L=1$. For $L=100$ and $\chi=10$ this is
  18888 when every bond is $\chi_i=\min(\chi,2^i,2^{L-i})$, and 19640 when every inner bond is $\chi$. Both are the
  $2L\chi^2=2\times10^4$ of Section 7.4. The case $\chi=1$ is a product state with 2 numbers per site, 200 for 100 sites and
  80 for 40. `memory_scaling.py` draws $L\chi^2$, without the factor $d=2$. Session 10 writes the trace form (10.6), with
  a $D\times D$ matrix on every site and the bond dimension called $D$, so its $D=10$ is the $\chi=10$ here, and it stores
  exactly 20000 numbers for $L=100$, as its sheet says. The $D=5$ of the MPO below is the bond dimension of an
  operator, another quantity.
- The Schmidt rank at a bond is at most $\chi$. A random MPS with $\chi=4$ on 10 sites has the ranks 2, 4, 4, 4, 4, 4, 4,
  4, 2, and a random state has $2^{\min(\ell,L-\ell)}$, so 2, 4, 8, 16, 32, 16, 8, 4, 2, which is the $\chi\sim2^{L/2}$
  of a volume law. An MPS with these bonds stores 2728 numbers, more than the 1024 coefficients.
- An MPS holds at most $\ln \chi$ across a bond, (7.10), and only $\chi$ equal Schmidt weights reach it. Sixteen equal
  weights give $2.7726=4\ln2$. A ground state stays far below the bound, as the notebook cells below show.
- The Heisenberg chain is an MPO of bond dimension $D=5$, with $I$, $S^+$, $S^-$, $S^z$ in the first column and
  $\frac12S^-$, $\frac12S^+$, $S^z$, $I$ in the last row. It gives the dense matrix of 6 sites exactly, and 5 is the
  operator Schmidt rank of $H$ at its center. On a random MPS with $\chi=4$ of 10 sites it gives $H|\psi\rangle$ to
  $10^{-15}$ with the bonds $\chi D=20$ in the bulk, the dimension before any truncation.
- A tensor has one number for each combination of its indices, 64 for three legs of dimension 4, 8 for three legs of
  dimension 2, and 256 for four legs of dimension 4.
- The AKLT chain $\sum_i[\mathbf S_i\cdot\mathbf S_{i+1}+\frac13(\mathbf S_i\cdot\mathbf S_{i+1})^2]$ of spins 1 is
  an MPS with $\chi=2$, with the matrices $A^{+1}=\sqrt{2/3}\,\sigma^+$, $A^0=-\sqrt{1/3}\,\sigma^z$ and
  $A^{-1}=-\sqrt{2/3}\,\sigma^-$. On 8 sites the four choices of the end vectors give eigenstates at
  $-\frac23(L-1)=-4.666667$ to $10^{-14}$, and exact diagonalization gives this level four times, for the two free
  spins $\frac12$ at the ends, and then $-3.9080$. This is the AKLT chain of the quizzes of Sections 7.8a and 7.8b.
- The local problem of a one-site update has $d\chi^2=2\chi^2$ numbers in the bulk and $d\chi$ at an end, as Section 7.10
  says, and $d^2\chi^2=4\chi^2$ for the two-site update, which dmrgpy uses by default. One product of the effective
  Hamiltonian with the tensor costs $4dD\chi^3+2d^2D^2\chi^2$ operations by the count of `np.einsum_path`, with $D=5$ the
  bond dimension of the MPO, so $4.2\times10^7$, $3.3\times10^8$ and $6.8\times10^8$ at $\chi=100$, 200 and 256, a
  factor 7.81 from 100 to 200. So the time of a sweep grows as $L\chi^3$, while $L\chi^2$ is the storage, and the notebook
  writes the cost as $O(N\chi^3)$.

## The entanglement entropy of the solvable states

- In the dimer product state (7.8), with the singlets on $(0,1)$, $(2,3)$, ..., a block has $S=n_\text{cut}\ln2$. On
  12 sites a block that starts at site 1 alternates between $\ln2$ and $2\ln2$, as in `dimer_entropy`, and one that
  starts at site 0 between $\ln2$ and 0. The blocks of the quizzes of Section 7.6 give $\ln2$ for the sites 1 to 3,
  $2\ln2$ for 1 to 4, 0 for 2 to 5 and $2\ln2$ for 3 to 6. dmrgpy with $J_2=0$ on 8 sites gives $\ln2$ and 0 in turn.
- The tetramer of Section 7.7 is taken as the plaquette, the Heisenberg ring of four sites. Its ground state is a
  singlet at $-2J$. One site holds $\ln2$, and so do three sites. Two sites on a side hold $0.8370=1.2075\ln2$, from
  the Schmidt weights $\frac34$ and three times $\frac1{12}$, and the two sites of a diagonal hold $\ln3=1.585\ln2$,
  since they are in a triplet.
- On the square lattice a square of side 2 and 4 has 8 and 16 bonds to the outside, and a cube of side 2 and 4 has 24
  and 96, counted bond by bond, and $6\ell^2=6\times10^4$ for $\ell=100$. In Figure 7.2 the tetramers sit on the
  $2\times2$ blocks and the squares are offset by one site from them. The small square cuts four tetramers at one site
  each, $4\ln2$ with 8 cut bonds, and the large one adds four tetramers cut along a side, $8.83\ln2$ with 16 cut
  bonds, a factor 2.21. A square aligned with the tetramers cuts none and has $S=0$. So the doubling of Section 7.7
  holds roughly, and only for a boundary that runs through the tetramers.
- A random state of 14 spins has, for the half, the Page value $\sum_{k=n+1}^{mn}1/k-(m-1)/(2n)$ with $m=n=2^7$,
  which is 6.279 bits, 0.72 below the maximum 7, and ten random states give 6.275 to 6.283 bits. Five sites have a
  deficit of only 0.045 bits, and one site has at least 0.9997 bits, so the deficit sits at the middle, as the caption
  of `random_vs_gapped` says.

## The dimerized Heisenberg chain, for Sessions 7 and 8

- The chain is $H=\sum_iJ_i\,\mathbf S_i\cdot\mathbf S_{i+1}$ on the sites 0 to $L-1$, with $J_i=J_1$ on the bonds
  $(0,1)$, $(2,3)$, ..., the dimers, which are the even $i$, and $J_i=J_2$ on $(1,2)$, $(3,4)$, ..., the odd $i$. An
  open chain of even $L$ then begins and ends with a $J_1$ bond. A cut after an odd number of sites goes through a
  $J_1$ bond and a cut after an even number through a $J_2$ bond, so `get_bond_entropy(i, i+1)` with an even $i$ cuts
  a $J_1$ bond. Section 7.6 has $J_2=0$, where the ground state is (7.8) with $-\frac34J_1$ per dimer, $-4.5$ for 12
  sites. The widget of Section 7.6 has $J_1=1$ and moves $J_2$, and `random_vs_gapped.py` and `schmidt_spectrum.py`
  take $J_1=1$ and $J_2=0.5$. Section 8.5 writes $J$ inside the dimers and $J'$ between them, so $J_1=J$ and
  $J_2=J'$. The notebook of Session 8 takes $J=1+0.2(-1)^i$ on the bond $(i,i+1)$, which is $J_1=1.2$ and $J_2=0.8$.
- For the chain of the notebook of Session 8, $J_1=1.2$ and $J_2=0.8$, on 12 sites the cuts through a $J_1$ bond
  carry 0.693 to 0.699 and the cuts through a $J_2$ bond 0.170 to 0.186, by exact diagonalization and by dmrgpy to
  $10^{-9}$.
- For a small $J_2$ the ground energy is $-\frac34J_1$ per dimer and $-\frac3{32}J_2^2/J_1$ per weak bond, to second
  order, and the gap to the lowest triplet is $J_1-J_2/2$ in a long chain, to first order. At $J_1=1$ and $J_2=0.1$
  the energy of 12 and 16 sites agrees with the formula to $2\times10^{-4}$, and the gap is 0.9517 and 0.9496 against
  0.95. These are open chains, whose lowest triplet is a standing wave above the bottom of its band. Rings of 12 and 16
  sites give 0.9463, the gap of the infinite chain on the sheet of Session 8, which is
  $J_1-J_2/2-3J_2^2/8J_1+J_2^3/32J_1^2$ to third order. At $J_2=0.5$ the energy is 0.017 and 0.024 below the formula,
  and the gap is 0.699 and 0.683 against 0.75. So
  the two formulas hold for $J_2$ up to about $0.1J_1$, and a page that quotes them writes this condition next to
  them.
- For $J_1=1$ and $J_2=0.5$ on 14 sites the cuts through a $J_1$ bond give 1.0000 to 1.0021 times $\ln2$ and the cuts
  through a $J_2$ bond 0.139 to 0.145 times $\ln2$, for every position of the cut, by exact diagonalization and by
  dmrgpy to $10^{-9}$. This is the blue curve of `random_vs_gapped`, whose caption gives the weak cuts as about
  $0.14\log2$ since 2026-11-22, in place of the old 0.15.
- At the center of 16 sites, which is a $J_2$ bond, the weight beyond the 16 largest Schmidt weights is
  $1.95\times10^{-7}$ for $J_2=1$ and $2.75\times10^{-11}$ for $J_2=0.5$, and the entropy is 0.5923 and 0.1005. This
  is the figure `schmidt_spectrum`.
- The open chain of four sites with the bonds $J$, $J'$, $J$ has at $J'=0.1J$ the ground state at $-1.50096J$ and the
  triplet at $-0.52749J$, a gap of $0.9735J$, and at $J'=J$ the ground state at $-1.61603J$ and a gap of $0.6589J$.
  dmrgpy gives $-1.50096J$ too. These are the numbers of Section 8.5.
- An open chain whose end bonds are $J_2$ bonds, which is $J_2$ on the even $i$ for an even $L$, leaves a nearly free
  spin at each end. For $J_1=1$ and $J_2=0.5$ the two end spins give a singlet and a triplet $7.8\times10^{-3}$ apart
  for 10 sites and $7.9\times10^{-4}$ for 14 sites, and the next level is 0.62 above. So the ground state is almost
  fourfold, as the end states of the SSH chain of Session 3. The chain of the notebook of Session 8 starts and ends
  with $J_1$, so it has none of this.

## Critical chains and the central charge

- For a block of $\ell$ sites with two ends, in an infinite chain or on a ring, (7.12) is $S=\frac c3\ln\ell+
  \text{const}$. The free fermions with the hopping 1 at half filling, which are the XX chain, give $S=1.4934$, 2.2611
  and 3.0287 at $\ell=10$, 100 and 1000 from the correlation matrix $C_{ij}=\sin(\pi(i-j)/2)/(\pi(i-j))$, with the
  slope 0.333 and the constant $0.7261=\frac13\ln2+0.4950$. pyqula on a ring of 2002 sites gives 1.4934 and 2.2598,
  as the numpy ring does, which is the infinite chain with $\ell$ replaced by $(N/\pi)\sin(\pi\ell/N)$. The term
  $\frac13\ln\ell$ alone is 0.768 at $\ell=10$ and 2.303 at $\ell=1000$. The growth between the two is
  $\frac13\ln100=1.535$ with or without the constant, and a MERA over 1024 sites has $\log_21024=10$ layers.
- For the cut of an open chain, which has one end, the coefficient is $c/6$, and the notebook writes $\frac c6\ln L$
  for the half chain. The free fermions give 1.0492, 1.1677, 1.2848 and 1.4011 for the left half of $L=100$, 200, 400
  and 800, a slope 0.169, and pyqula gives 1.284805 for $L=400$. With an odd number of sites in the half the slope is
  0.163, between 202 and 402 sites. So the two parities of $L/2$ reach $\frac16$ from the two sides, and a page
  compares lengths of the same parity.
- The free-fermion chain with the hopping 1 on the bonds $(2n,2n+1)$ and 0.6 on the others has the gap
  $2|1-0.6|=0.8$. On a ring of 1000 sites a block whose two ends cut a bond 0.6 has 0.4992, and already 0.4983 with
  10 sites. A block with one end of each kind has 0.9554, and a block whose two ends cut a bond 1 has 1.4117. pyqula
  `bichain()` with `h.inter` times 0.6 gives the same. The red curve of `critical_entropy` is this chain
  open, with 3002 sites and blocks in the middle that start on an even site, so that both ends cut a bond 0.6, and it
  gives 0.4983 at $\ell=10$ and 0.4992 from $\ell=32$ on. It is also the spinon chain of Section 8.9 with the same gap 0.8. It is another model than the dimerized
  Heisenberg chain, so a page names the model next to the number.

## pyqula

- `geometry.chain()` has one site per cell and the hopping $+1$, and `h.set_finite_system(n=L)` is the open chain of
  $L$ sites, ordered along $x$, with the levels $2\cos(\pi k/(L+1))$. In `geometry.bichain()` the two sites of the
  cell are at $x=-0.5$ and $0.5$ and the period is 2. `h.intra` is the bond inside the cell and `h.inter` the bond to
  the next cell, so a block of whole cells cuts two `h.inter` bonds.
- `h.get_entanglement_entropy(region=sites, nsuper=N)` is the entropy of free fermions with the levels below zero
  filled, from the correlation matrix, in nats. For an `h` with a period it builds a ring of `nsuper` cells, and
  `region` lists sites of that ring, so a block has two ends. With no `region` it takes the left half of a finite
  system. A block of 10 sites of a ring of 102 cells gives 1.48818495, as the numpy ring does, the sites 40 to 49 give
  the same, and a finite chain of two sites gives $\ln2$.
- A half-filled ring whose number of sites is a multiple of 4, such as 1000, and an open chain of odd length, such as
  11, have a level at zero energy, and the call raises `ValueError` with the text "A level sits at the Fermi energy".
  A ring of $N=2$ modulo 4 sites, such as 102 or 2002, has no such level.
- The default Hamiltonian has the two spins and gives twice the entropy, 0.99669 for 10 sites of the dimerized
  `bichain` on a ring of 100 cells, against 0.49835 with `has_spin=False`. On a ring of 300 cells of the same chain
  the spinful call gave wrong values that change from run to run, between 1.2 and 2.2 in the runs of 2026-11-21,
  while `has_spin=False` gives 0.49835 again. The uniform `chain()` gave twice the spinless value on a ring of 602
  cells. The cause was not found, so a script takes `has_spin=False` and doubles the entropy by hand.
- pyqula does not diagonalize an interacting quantum chain, and its solvers for interactions are mean field, classical
  spins and linear spin waves. `pyqula2dmrgpy.generate_fermionic_chain(hf)` turns a finite pyqula
  Hamiltonian into a dmrgpy `Fermionic_Chain`, with `Cdag`, `C` and `N` for each site, and the interaction is added on
  the dmrgpy side. It drops every matrix element below $10^{-5}$, so an onsite energy $5\times10^{-6}$ changes the
  free energy by $2.5\times10^{-6}$ and the dmrgpy energy by 0. For a Hamiltonian with a period it prints "Only
  implemented for 0d dimensional Hamiltonians". The singlet, the Heisenberg chain, DMRG, the Schmidt weights and the
  quench of the session are dmrgpy or numpy calculations, so their figures have no pyqula script.

## The transverse-field Ising chain

- The chain of the notebook, $-\sum_iS^z_iS^z_{i+1}+B_x\sum_iS^x_i$ with $\mathbf S=\boldsymbol\sigma/2$, is
  $-\frac14\sum_i\sigma^z_i\sigma^z_{i+1}+\frac{B_x}2\sum_i\sigma^x_i$. Its gap in the phase of large field is
  $|B_x-\frac12|$, so the transition is at $B_x=0.5$, and a ring of 12 sites has the gap 0.3004 at $B_x=0.8$ and
  0.5000 at $B_x=1$. With $\sigma^x_i=1-2n_i$ the Jordan-Wigner fermions are free, and their Bogoliubov-de Gennes
  ground state of 10 sites has the energy and the entropies of exact diagonalization to $10^{-14}$. Session 10 writes
  the same chain as $-J\sum_i\sigma^z_i\sigma^z_{i+1}-h\sum_i\sigma^x_i$, and the chain of the notebook is that one
  divided by 4, with $J=1$ and $h=-2B_x$. So $B_x=0.5$ is its $h=J$, and a ring of 8 sites has $-2.562915$ there, one
  quarter of the $-10.251662$ of the sheet of Session 10.
- The critical Ising chain has $c=\frac12$. At $B_x=0.5$ the entropy of the left half of an open chain grows by
  0.0582 when $L$ doubles from 160 to 320, where $\frac c6\ln2$ is 0.0578. At the cut of the notebook the exact
  entropy is 0.4427 for 20 sites and 0.5050 for 40 sites, and the cell gives the same.
- On the ordered side the exact ground state of an open chain is the even superposition of the two ferromagnetic
  states, so its entropy at the cut of the notebook is close to $\ln2$, 0.6994 and 0.6995 at $B_x=0.30$ for 20 and 40
  sites. It rises a little to its largest value, 0.7053 at $B_x=0.37$ for 20 sites and 0.7313 at 0.44 for 40 sites on
  a grid of 0.01, and then falls through the transition to 0.4427 and 0.5050 at 0.5. The cell starts DMRG from a
  ferromagnetic guess, and at $B_x=0.30$ on 20 sites DMRG stayed in the broken state in the runs of 2026-11-21, with
  $S$ about 0.01 and a magnetization of 0.46 per site. So the peak of the scan sits on the ordered side, where DMRG
  first finds the even superposition or at the maximum of the exact curve. Its place changes from run to run, from
  0.36 to 0.45 in the runs of 2026-11-21.
- The quench of `quench_entropy.py` evolves 12 sites from all spins up with
  $-\sum_i\sigma^z_i\sigma^z_{i+1}-\sum_i\sigma^x_i$, the same critical point in the Pauli form with $J=h=1$. The
  entropy of half the chain passes $\ln2$, $\ln4$ and $\ln8$ at $t=1.463$, 2.539 and 3.518 and has its maximum, 3.289
  bits, at $t=4.00$. On the grid of 0.05 of the figure the first points above the three lines are 1.50, 2.55 and
  3.55. Krylov steps and the full diagonalization agree.

## DMRG and dmrgpy

- One sweep of the one-site update of `dmrg_sweeps.py` is $2L-2=18$ updates on 10 sites, and the energy never goes up.
  After three sweeps the error $E-E_0$ is 0.2016 to 0.2018 for $\chi=2$ and $1.461\times10^{-5}$ for $\chi=8$. For $\chi=4$ it
  is $6.12\times10^{-3}$ from the start of the figure, `seed=1`, and $6.1\times10^{-3}$ to $8.9\times10^{-3}$ over the
  seeds 1 to 8. dmrgpy runs the two-site update, and with `maxm` 2, 4 and 8 it stops at 0.2156, $6.1\times10^{-3}$ and
  $1.5\times10^{-5}$ above the exact $-4.258035$, so at $\chi=2$ the one-site sweep ends a little lower.
- dmrgpy takes by default `maxm=30`, `nsweeps=15`, the truncation cutoff $10^{-12}$ and the two-site update. A chain
  of two sites does not run DMRG, since dmrgpy falls back to exact diagonalization and returns a state without
  `get_bond_entropy`, which raises `AttributeError`. `sc.get_site_entropy(wf, 0)` gives the singlet entropy 0.69315
  there. The notebook finds dmrgpy through the variable `DMRGROOT`.
- The energy per site of the infinite Heisenberg chain is $\frac14-\ln2=-0.443147J$. Rings of 16 and 18 sites give
  $-0.44639$ and $-0.44571$, and $-0.44318$ and $-0.44317$ with the finite-size term $\pi^2/(12L^2)$ added. An open
  chain approaches it slowly from above, with $-0.375$ for two sites, the first point of the notebook cell, and
  $-0.43412$ for 20 sites.

## The notebook cells, run on fewer points

- The cell "Energy of the Heisenberg model as a function of the system size" calls `sc.gs_energy(mode="DMRG")` for
  $N=2$, 6, ..., 38, so it runs DMRG, while its text says exact diagonalization. The box of Section 7.3 says that the
  cell runs DMRG since 2026-11-22.
- The cell "The role of the bond dimension in tensor networks" gives on 20 sites the fluctuation per site
  $5.4\times10^{-4}$, $6.1\times10^{-5}$ and $3.1\times10^{-6}$ at `maxm` 3, 11 and 23, while the energy per site is
  $-0.434118$ at 11 and $-0.434124$ at 23. In the range of the cell the energy saturates and the fluctuation does not.
- The cell "Entanglement entropy of the ground state" has 20 sites. With `maxm=20` the cut after 10 sites, the center,
  has 0.6346, and the cuts after 9 and 11 sites, the bond numbers 8 and 10 of its plot, have the largest value
  0.7924. Every cut after an odd number of sites has at least $\ln2$, since the end bonds of an open chain are strong,
  so the center is below all of them. With `maxm=2` the curve reaches about 0.62, under $\ln2$.
- The cell "Size dependence of the entanglement entropy" zigzags, since the number of sites left of its cut, $L/2+1$,
  is odd and even in turn along `Ls = range(10,50,2)`. It gives 0.492, 0.792, 0.709 and 0.867 for $L=10$, 20, 30 and
  40, and the center gives 0.738, 0.635, 0.835 and 0.762. On one parity the entropy grows as $\frac16\ln L$, and the
  centers of 20 and 40 sites differ by 0.127 against $\frac16\ln2=0.116$.
- The cell "Bond dimension dependence of the entanglement entropy" stays far below $\ln\chi$. At its cut, $\chi=2$, 8
  and 19 give 0.271, 0.492 and 0.492 for 10 sites and 0.360, 0.686 and 0.708 for 30 sites, where $\ln\chi$ is 0.693,
  2.079 and 2.944. The chain of 10 sites is converged at $\chi=8$, and the one of 30 sites still grows.
- The quiz of the cell "Entanglement entropy of the ground state" asks for the Ising chain $\sum_iS^z_iS^z_{i+1}$. On
  20 sites dmrgpy gives the Néel energy $-4.75$. The ground level holds the two Néel states, and DMRG returns one of
  them, with a bond entropy of $10^{-16}$, or a mix of the two, whose entropy is the same at every cut and at most
  $\ln2$, the value of the symmetric combination. Which one comes out changes from run to run, so a page says that
  a single Néel state has no entanglement and does not quote the entropy that DMRG gives.
- The cell "Low energy excitations of a Heisenberg model", run on 12 sites. The triplet is 0.2809 above the singlet,
  and `Bz=0.03` lowers its member with $S^z=-1$ to 0.2509, which DMRG then finds, with the largest
  $|\langle1|S^x_i|0\rangle|$ equal to 0.179, as exact diagonalization gives. With `Bz=0` the excited level is the
  whole triplet and DMRG returns a member chosen by the run. Its profile $|\langle1|S^x_i|0\rangle|$ has the same
  shape, times a factor between 0 and $\sqrt2$ that changes from run to run, 0.44 in one run of the check. The sum over
  $x$, $y$ and $z$ of $|\langle1|S^a_i|0\rangle|^2$ is the same in every run, $2\times0.179^2=0.064$ at its largest.

## Statements of the pages that these numbers contradicted, corrected on 2026-11-22

The statements below were left as they were by the builders, and they were corrected on 2026-11-22 by the rule of the
lecturer of that day, "Fix old-text errors". Each bullet says what the page says now, and the check prints the number
that backs it.

- The caption of `memory_scaling` in Section 7.3 said sixteen gigabytes at $L=30$. This is $1.72\times10^{10}$ bytes,
  17.2 GB in the unit of its dashed line, $10^9$ bytes, and 16 only in units of $2^{30}$ bytes, so the caption says about
  seventeen gigabytes. The first quiz of the same page says $1.7\times10^{10}$ bytes.
- Two pages counted a product state in two ways. The first quiz of Section 7.3 calls 640 bytes for 40 sites the storage of
  a product state, one 16-byte number per site, and it now adds that this count keeps only what is left once the norm and
  the phase of each site are fixed, while an MPS with $\chi=1$ stores two numbers per site, 1280 bytes for 40 sites. This is
  the count of the first quiz of Section 7.4, two numbers per site, 200 for 100 sites.
- The notebook box of Section 7.3 said that the first cell computes the energy with exact diagonalization, and the cell
  runs DMRG. The box now says that the code calls `sc.gs_energy(mode="DMRG")`, and the try-it of the same page asks to
  compare the growth of the time with $2^L$.
- The try-it of Section 7.5 called the straight curve of the time against $L$ the $L\chi^2$ structure of (7.5), and the
  notebook box of Section 7.8a called the cost of DMRG the $L\times \chi^2$ scaling of (7.5). The time of a sweep is linear
  in $L$ but grows as $\chi^3$, a factor 7.81 for a step from $\chi=100$ to 200, and $L\chi^2$ is the storage, so both now say the
  linear growth in $L$ of (7.5).
- The try-it of Section 7.8a asked to check that the central bonds have the largest entropy. For 20 sites with
  `maxm=20` the largest, 0.792, sits on the cuts after 9 and 11 sites, beside the center, and the center itself has
  0.635, below every cut after an odd number of sites and below the $\ln2$ of the first cut. The try-it now asks to check
  that the largest entropy sits on the two bonds next to the central bond.
- The notebook box of Section 7.8a said that the fluctuation of the energy becomes smaller and then saturates where
  $\chi$ satisfies the bound (7.10), and the box of Section 7.8b said that the entropy saturates once $\chi$ satisfies it.
  In the cell the fluctuation still falls from `maxm=11` to 23, while the energy per site changes by
  $6\times10^{-6}$, so it is the energy that saturates. The bound holds much earlier, since the 20 sites need at most
  0.792, below $\ln3$. What sets the saturation is the weight of the Schmidt values that are dropped, and both boxes now
  say this.
- The notebook box of Section 7.8b called the slow growth of the entropy with the size the area-law saturation of
  Section 7.6 in a gapless chain. The Heisenberg chain is critical, the notebook itself gives $\frac c6\ln L$ with
  $c=1$, the center grows by 0.127 from 20 to 40 sites, and the cut of the cell zigzags. The box now says that this is
  not the saturation of Section 7.6 and that the entropy grows as $\frac c6\ln L$.
- The try-it of Section 7.8b said that the curves of $L=10$ and $L=30$ follow the bound $\ln\chi$ at small $\chi$. At
  $\chi=2$ they have 0.271 and 0.360 against $\ln2=0.693$, so they stay far below it at every $\chi\geq2$, which the
  try-it now says.
- In Section 7.11 the first answer of the second quiz said "its entropy goes from $0.77$ at $\ell=10$ to $2.3$ at
  $\ell=1000$." These are the term $\frac13\ln\ell$ alone, while the block of the infinite chain has 1.49 and 3.03, and
  the figure `critical_entropy`, an open chain of 3002 sites with the blocks in the middle, gives 1.4929 and 2.9649. The
  feedback now says that the entropy grows by about 1.5, which holds in both. The first quiz takes
  $S=\frac c3\log\ell$ with no constant as its premise, so its 0.77 and 2.3 hold on its own terms.
- The try-it of Section 7.11 said that the peak of the entropy should sit close to $B_x=0.5$. The exact entropy at the
  cut of the notebook has its largest value on the ordered side, at 0.37 for 20 sites and 0.44 for 40 sites, and has
  fallen to 0.4427 and 0.5050 at 0.5. The peak of the scan sits there, or where DMRG first leaves its ferromagnetic
  guess, and its height near $\ln2$ comes from the even superposition of the two ferromagnetic states. The try-it now
  says that the peak sits below 0.5, on the ordered side.
