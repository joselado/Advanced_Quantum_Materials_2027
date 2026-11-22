# Conventions of Session 10, checked by number

This sheet fixes the signs, the units and the numbers that the pages, the figures and the scripts of Session 10 use.
An agent that edits the session reads it first and does not work these out again. Every line was checked with a
number on 2026-11-21. Two drafts were written apart, and a third calculation settled each line where they differed or
where only one of them had it. The check is `webnotes/checks/session10/conventions.py`, which prints one line per
bullet below, in the same order. A statement that is not on this sheet is checked before a page claims it.

Most of this session is not pyqula. The networks, the tensor networks and the Monte Carlo are numpy, and the second
route for the spin chains is the exact diagonalization of dmrgpy. The energies are in units of $J$ or of the hopping
$t$, and the temperature is in the same units with $k_B=1$. The figure scripts of `webnotes/figures/session10/` write
their SVG when they run, so the check repeats their computation with their seed and never runs them. The units of
(10.8) are Gaussian, with $\hbar$, $m$ and $e$, while the quiz of Section 10.5 writes $-\nabla^2/2$, which is atomic
units, so a page that writes the Kohn-Sham Hamiltonian says which. The Fashion-MNIST accuracies of Section 10.4 are
on page 31 of the slides of the lecture, `slides_prerecordings/lecture10.pdf`, which the check of that page reads, and
they are the numbers of Section VI of arXiv 1801.00315, a classifier of ten labels. The sizes $L=10$ to 60 of Section
10.6a and $L=4$ to 28 of Section 10.6b are in the legends of the figures on pages 46 and 49 of the same slides, which
were read on 2026-11-22 and are not checked by a script. None of them is a stored source of `labsource.py`, since
the pages have no lab box.

The pyqula of the checks is the development tree of version 0.0.95, at commit 7567127. The students install the
release 0.0.96 of PyPI, whose code was read, and run only once for the loop that does not converge. It builds
`LatticeIsing.add_interaction` from the Bloch matrix at $k=0$ of `tij=Jij`, so it counts every bond twice, as the
development tree does. It has
`constrains=["no_magnetism"]` and the guess `mf="potential"` of the mean field, and its `get_dos` has no
`integration="triangle"`. A mean-field loop that does not converge prints a line in the release and returns `None` in
place of the Hamiltonian, and `(None, energy)` with `return_total_energy=True`, with spin and without, as a run with
`maxite=2` gave and as the sheet of Session 1 says, while the development tree raises `MeanFieldConvergenceError`.

## Units and signs

- In (10.9) a positive $J$ favors parallel spins, since $-J\sigma_1\sigma_2$ has its two ground states
  $\uparrow\uparrow$ and $\downarrow\downarrow$ at $-J$. In (6.5) a positive $J$ is antiferromagnetic, since
  $J\,\mathbf S_1\cdot\mathbf S_2$ with $\mathbf S=\boldsymbol\sigma/2$ has the singlet at $-3J/4$ and the triplet at
  $+J/4$, and dmrgpy gives $-0.75$. With Pauli matrices in place of $\mathbf S$ the two levels are $-3J$ and $+J$.
  The $E_0=-3J/4$ of the quiz of Section 10.3a is the spin-1/2 form. The Ising dimer (8.1) of Session 8,
  $S^z_0S^z_1$ with $\mathbf S=\boldsymbol\sigma/2$, has $-1/4$ for antiparallel and $+1/4$ for parallel spins, so it
  is one bond of (10.9) with $J=-1/4$.

## The loss and gradient descent of Section 10.2

- For $\mathcal L=\theta^2/2$ the update of (10.1) is $\theta\to(1-\eta)\theta$, checked with a numerical gradient.
  The step $\eta=0.5$ halves $\theta$, $\eta=1$ reaches the minimum at once, $\eta=2$ jumps between $+1$ and $-1$, and
  $\eta=2.5$ multiplies $\theta$ by $-1.5$ and the loss by $2.25$ at every step, as the figure `lrate` and the quiz
  draw. For a curvature $\kappa$ the loop converges only for $\eta<2/\kappa$, checked with $\kappa=3$ at $\eta=0.6$
  and $0.7$.
- No line $w\cdot x+b$ separates $(0,0),(1,1)$ from $(0,1),(1,0)$, since the largest margin that a linear program
  finds is zero. The best linear fit gives $0.5$ at the four corners, with the loss (10.1) equal to 1. Two hidden step
  neurons on the lines $x+y=1/2$ and $x+y=3/2$, with the output their difference, give XOR exactly, and this is the
  band of the figure `xor`.
- The widget `netfit` trains one hidden layer of tanh units on 41 points of $\sin(3\pi x)$ in $[-1,1]$, which has six
  extrema, and the network has $3H+1$ parameters. Its code takes the mean of the squared error, not the sum of (10.1),
  and 4000 steps of Adam, not the plain update of (10.1). The mean squared error is $0.46$, $0.38$ and $0.23$ for
  $H=1$, 2 and 3, against $0.49$ for an output that is zero. For $H=4$ to 12 it is below $10^{-2}$, from
  $7.3\cdot10^{-3}$ at $H=4$ to $2.3\cdot10^{-4}$ at $H=12$, and it does not fall at every step of $H$, with
  $3.0\cdot10^{-3}$ at $H=5$, $3.4\cdot10^{-3}$ at $H=6$ and $5.0\cdot10^{-3}$ at $H=7$. So three neurons fail too,
  and the widget starts at $H=3$.

## The table of coefficients and the variational principle

- A complex coefficient in double precision takes 16 bytes. So 16 GB hold $L=29$ and 1 TB holds $L=35$, as the
  figure `memory` says in decimal units, while 16 GiB and 1 TiB hold exactly $L=30$ and $L=36$. The table of $L=40$
  is $1.76\cdot10^{13}$ bytes, which is 17.6 TB or 16 TiB. $L=30$ needs 17.2 GB, $L=26$ needs 1.07 GB and $L=20$
  needs 16.8 MB, the "about 16 MB" of the quiz of Section 10.3a. The matrix product state with $D=10$ and $d=2$ is
  960000 bytes at $L=300$ and stays below $10^6$ bytes up to $L=312$. Section 7.3 counts in binary units for its
  "sixteen gigabytes at $L=30$" and in decimal units for its "about 17 terabytes", so a page says which of the two
  units it uses.
- For the open Heisenberg chain of 8 spins with $J=1$, the basis of (10.2), Kronecker products of Pauli matrices and
  dmrgpy all give $E_0=-3.374933$. 2000 random complex states with Gaussian components give $E[\theta]$ between
  $-0.3$ and $0.3$, far above $E_0$, and each one equals $\sum_n|c_n|^2E_n/\sum_n|c_n|^2$ in the eigenbasis to
  $10^{-14}$.

## The restricted Boltzmann machine

- With visible spins $s_i=\pm1$, hidden spins $h_j=\pm1$, biases $a_i$ and $b_j$ and weights $W_{ji}$, the sum over
  the hidden spins of $e^{\sum_ia_is_i+\sum_jb_jh_j+\sum_{ij}h_jW_{ji}s_i}$ is $C(s)=e^{\sum_ia_is_i}\prod_j2\cosh\theta_j$
  with $\theta_j=b_j+\sum_iW_{ji}s_i$, checked against the explicit sum to $10^{-14}$. There are $N+M+NM$ parameters,
  1680 for $N=M=40$, which is the "few thousand parameters" of the quiz of Section 10.3a.
- With real parameters every $C(s)$ is positive, so a real network has no signs, and a state with signs needs complex
  parameters or a sign put in by hand. A complex network vanishes only where some $\theta_j=i\pi(n+1/2)$. A
  fine-tuned parameter reaches it, while 20 random draws of complex parameters keep $|C(s)|$ above 0.08 on all the
  configurations. So "a non-zero amplitude for every configuration" of Section 10.3b holds for real parameters and
  for generic complex ones.
- The logarithmic derivatives are $O_{a_i}=s_i$, $O_{b_j}=\tanh\theta_j$ and $O_{W_{ji}}=s_i\tanh\theta_j$, checked
  with finite differences to $10^{-8}$ for complex parameters.

## The local energy, the sampled energy and the gradient

- In the basis of (10.2) the Heisenberg chain has the element $+J/2$ between two configurations that differ by the
  swap of an antiparallel pair, and $\pm J/4$ per bond on the diagonal. A row has at most $L$ elements on an open
  chain, the $L-1$ bonds and the diagonal, and $L+1$ on a periodic chain, checked for $L=10$. So "at most $L$ terms"
  of Section 10.3b and the 39 bonds of $L=40$ of its quiz are the open chain. The open chain of 10 sites has
  $(L+1)\,2^{L-1}=5632$ elements in all, as Section 7.3 says for even $L$, and the $s$ of the figure `local_energy` is
  connected to three other configurations.
- With $p(s)=|C(s)|^2/\sum_{s'}|C(s')|^2$, the sum $\sum_sp(s)E_{\rm loc}(s)$ of (10.4) is $E[\theta]$ of (10.3) to
  $10^{-14}$, by enumeration for a complex network on the open Heisenberg chain of 8 spins. At an eigenstate
  $E_{\rm loc}(s)$ is the same number for every $s$ with $C(s)\neq0$, to $10^{-12}$ for the ground state of the
  transverse-field chain below, so the sampled energy then has no statistical error.
- 4000 configurations drawn from $p(s)$ of the same network give $E[\theta]=-0.50$ with a statistical error of
  $0.009$ to $0.012$ in 5 runs, and the mean is within two errors of $E[\theta]$.
- (10.5) is $\partial E/\partial\theta_k$ for a real parameter $\theta_k$ and a complex amplitude, checked against
  finite differences of (10.3) to $10^{-9}$. The conjugate sits on $O_k$, and with $O_k$ in its place the result is
  off by up to 1.4. For a complex parameter $\theta_k=x_k+iy_k$ the two derivatives are
  $\partial E/\partial x_k=2\,\mathrm{Re}\,F_k$ and $\partial E/\partial y_k=2\,\mathrm{Im}\,F_k$, with
  $F_k=\langle E_{\rm loc}O_k^*\rangle-\langle E_{\rm loc}\rangle\langle O_k^*\rangle$, so the step of gradient
  descent is $\theta_k\to\theta_k-2\eta F_k$. A page that writes (10.5) says that $\theta_k$ is real, or says which
  part it means.

## The signs of the ground states and a trained network

- The ground state of the open Heisenberg chain of 8 spins has 70 non-zero amplitudes of both signs, and the sign is
  $(-1)^{N_\uparrow}$ on all of them, with $N_\uparrow$ the number of up spins on the sites 1, 3, 5 and 7 counted from
  0. This is the Marshall sign, so a network with real parameters, which is positive, needs it put in by hand. The
  ground state of the transverse-field chain below has all 256 amplitudes positive for $h>0$, so a real network can
  hold it. For $h<0$ it is the same state times $\prod_is_i=(-1)^{n_\downarrow}$, with $n_\downarrow$ the number of
  down spins.
- The transverse-field Ising chain $H=-J\sum_i\sigma^z_i\sigma^z_{i+1}-h\sum_i\sigma^x_i$, with Pauli matrices, is
  not on the pages yet, and it is here for a problem or a lab box on networks. On a ring of 8 sites with $J=h=1$ the
  ground-state energy is $-10.251662$ by exact diagonalization, by the sum over the free fermions
  $-\sum_k\sqrt{J^2+h^2-2Jh\cos k}$ with $k=(2n+1)\pi/L$, which is $-2/\sin(\pi/16)$ here, and by dmrgpy with
  $-4S^zS^z-2S^x$ in its spin operators. The sum also gives the $-8.509082$ and $-17.018164$ of the diagonalization
  for $h=0.5$ and $h=2$, and $-4/\pi=-1.2732$ per site for a long chain at $h=J$. The notebook of Session 7 writes the
  same chain as $-\sum_iS^z_iS^z_{i+1}+B_x\sum_iS^x_i$, which is this $H/4$ with $J=1$ and $h=-2B_x$. So its critical
  field $B_x=0.5$ is $h=J$ here, and its ring of 8 sites has $-10.251662/4=-2.562915$ there, in dmrgpy. A field of
  either sign gives the same levels.
- A real network with $M=L=8$ hidden spins on this chain, 80 parameters from small random values, trained with (10.5)
  on the exact sums over the 256 configurations and $\eta=0.05$, ends $7.4\cdot10^{-5}$ to $9.2\cdot10^{-5}$ above
  $E_0$ in relative terms after 2000 steps, and $4.7\cdot10^{-5}$ to $7.2\cdot10^{-5}$ after 3000, in 3 runs.

## Tomography and the fidelity

- When $p_\theta$ is free on all the configurations, the maximum of $\sum_sn(s)\ln p_\theta(s)$ is at
  $p(s)=n(s)/\sum_{s'}n(s')$, the observed frequencies. Gradient ascent from the counts of 1000 shots of a state of 3
  spins ends there to $10^{-15}$. The states $(|\uparrow\rangle\pm|\downarrow\rangle)/\sqrt2$ give $0.5$ and $0.5$
  along $z$, and $(1,0)$ and $(0,1)$ along $x$, as the figure `tomo_phase` draws.
- We take the fidelity of two pure states as $F=|\langle\psi|\phi\rangle|^2$ for normalized states, and not its square
  root, which some texts take. The pages do not use it yet, so a page that quotes a fidelity says which. $F$ is 0 for
  $(|\uparrow\rangle+|\downarrow\rangle)/\sqrt2$ and $(|\uparrow\rangle-|\downarrow\rangle)/\sqrt2$, whose counts
  along $z$ agree, 1 for a global phase, and 0.054 for a state of 3 spins against the same state with a random phase
  on each configuration. So the counts along one axis do not fix the fidelity.
- The state $\sqrt{p(s)}$ built from the counts along $z$ has $F=0$ with the singlet and $F=0.0038$ with the ground
  state of the open Heisenberg chain of 8 spins. With the Marshall sign put in, the same moduli give $F=1$. So for
  this chain all the missing information is the sign.

## Matrix product states and the classifier

- (10.6) is the trace form with a $D\times D$ matrix on every site, $L\,d\,D^2=20000$ numbers for $L=100$, $d=2$ and
  $D=10$, against $2^{100}=1.27\cdot10^{30}$, which is 25.8 orders of magnitude more, the "26 orders of magnitude" of
  the quiz. The open form (7.5) of Session 7 has vectors at the two ends, 19640 numbers here, and calls the bond
  dimension $\chi$. $D=1$ is a product state with $L\,d=200$ numbers, and 80 for the 40 spins of the quiz of
  Section 10.3a.
- The singlet has two Schmidt values $1/\sqrt2$ and the entropy $\ln2$, so it needs $D=2$. The trace form with
  $A^\uparrow=\mathrm{diag}(1,0)$, $A^\downarrow=\mathrm{diag}(0,1)$ on the first site and
  $B^\uparrow=-\mathrm{diag}(0,1)$, $B^\downarrow=\mathrm{diag}(1,0)$ on the second gives it. The trace closes the
  chain into a ring, so a cut crosses two bonds, and a random trace form of 8 sites with $D=2$ has the Schmidt rank
  $4=D^2$ across half of the ring. A random state of 10 spins has the rank $32=2^{L/2}$ at the middle, so a generic
  state needs a bond dimension that grows exponentially.
- With the pixel map $\varphi(x)=(\cos\frac{\pi x}{2},\sin\frac{\pi x}{2})$, which sends white, $x=0$, to up and
  black, $x=1$, to down, the tensor product of $N$ pixels has norm 1 and $2^N$ components. The output of a tree is
  exactly the product of its contracted weights with this vector, checked on a tree of 8 pixels against the
  $256\times2$ matrix, and $2\varphi(x_1)$ in place of $\varphi(x_1)$ doubles it. So the classifier is linear in the
  tensor product, as the quiz of Section 10.4 says.
- The number of parameters of a binary tree on 100 pixels with $D=10$ and a label leg of 2 depends on its shape. It
  is 50200 when neighbors are paired level by level and the top tensor carries the label leg, 51020 with a separate
  $10\times2$ tensor for the label, the "final small tensor" of Section 10.4, and 41240 when the pixels are split into
  halves again and again. When a bond is cut at $\min(D,\text{product of the legs below})$ the three are 28000, 28820
  and 28088. All are between $10^4$ and $10^5$, as the quiz of Section 10.4 says.

## The Kohn-Sham toy of Section 10.5

- The loop of `ks_loop.py` has 40 electrons on 60 sites with the hopping $-1$, the well
  $v_{\rm ext}(i)=-2e^{-((i-29.5)/7)^2}$, the Hartree term $U\,n(i)$ on the total density with $U=2$, and 30 percent
  of the new density mixed in. The density at the center, the sites 29 and 30, is 0.9895 at convergence and 1.2143
  with no Hartree term, the 0.99 and 1.21 of the caption, and 0.831 and 0.949 after the iterations 1 and 3. The
  largest difference $\max_i|\Delta n(i)|$ between the density that the diagonalization gives and the density that
  went in falls below $10^{-10}$ at the iteration 36, and the ratio of two of them stays between 0.48 and 0.53, so
  "the same factor" of the caption is true to about 10 percent. The stored density changes by 0.3 times this
  difference, the weight of the mixing.
- In pyqula the same loop is the Hubbard mean field of an open spinful chain of 60 sites with `tij=[-1.]`, the well in
  `add_onsite`, `U=4`, `filling=40/120` and `mix=0.3`. With `constrains=["no_magnetism"]` it gives the density of the
  toy to $2\cdot10^{-11}$, and its onsite energy is $v_{\rm ext}+2n(i)$ plus the constant 0.048, which puts the middle
  of the gap between the last filled and the first empty level at zero energy. For a density that is the same on every
  site only $-\sigma Um_i/2$ is left, as the sheet of Session 1 says for the dimer. So the `U` of pyqula is the
  Hubbard $U$, each spin feels $U\langle n_{-\sigma}\rangle=Un/2$, and the $U=2$ of the toy is `U=4`. A page says
  which of the two it quotes. The guess `mf="potential"` starts with equal spins and gives the same density, but a
  moment of $5\cdot10^{-7}$ appears in it, so the constraint is the safer call, for the reason that the line on the random start
  below gives.
- With the default random guess and the seed 0 the same call ends at the total energy $-61.79$, below the $-58.01$
  of the state with equal spins. Its local moment reaches 0.77, along an axis of its own, so its $z$ component is only
  0.35. A collinear mean-field loop in numpy gives the same $-58.0094$ for equal spins, so the two count the energy in
  the same way, and from a random start it ends at $-61.42$ with the same moment 0.77. From equal spins with a kick of
  $10^{-6}$ it goes to $-61.80$ and the moment 0.77, so the state with equal spins is unstable. So the density of the
  caption is
  the solution with equal spins, which is what a Hartree term on the total density gives, and not the lowest state of
  the Hubbard mean field.

## The Ising model of Section 10.6a

- $T_c=2J/\ln(1+\sqrt2)=2.2692\,J$, where $\sinh(2J/T_c)=1$. The exact $|m|=(1-\sinh^{-4}(2J/T))^{1/8}$ is 0.9865,
  0.9113, 0.8687 and 0.7848 at $T=1.5$, 2.0, 2.1 and 2.2.
- pyqula `LatticeIsing` lists every bond in both directions, so `add_interaction(Jij=[0.5])` is the $J=1$ of (10.9).
  On $16\times16$ all spins up then have the energy $-2N=-512$, and one flipped spin costs 8, the $8J$ of (10.9).
  `Jij=[1.]` gives twice the energy of every configuration, which moves $T_c$ to 4.54. Its Metropolis run
  `optimize_energy` gives the mean $|m|$ 0.987 at $T=1.5$ and 0.13 at $T=3.5$.
- For $N=64^2=4096$ independent spins, which is the infinite temperature, $m$ has the root mean square
  $1/\sqrt N=0.0156$ and $\langle|m|\rangle=\sqrt{2/(\pi N)}=0.0125$, which 2000 samples reproduce. So $|m|=0.93$ is
  59.5 standard deviations, the "more than 50" of the quiz of Section 10.6a. At the $T=3.5$ of the figures the root
  mean square of $m$ on $64\times64$ is 0.038 from Monte Carlo, larger than $1/\sqrt N$ since the spins are
  correlated, and 0.93 is still 24 of it.
- The Monte Carlo of the figure `ising_sizes`, with its seed, 1500 sweeps to thermalize and 3000 to average, puts
  $L=8$, 16 and 32 within 0.0065 of the exact value at the seven temperatures from $T=1.5$ to 2.1. At $T=2.2$, the
  last point of the figure
  below $T_c$, they are $+0.031$, $+0.012$ and $-0.013$ away. So the caption says that the three sizes agree with it
  within 0.007 up to $T=2.1$, and that at $T=2.2$ the lattice of 8 is 0.03 above it.
- At $T=3.0$ the same figure has $\langle|m|\rangle=0.352$, 0.170 and 0.086 for $L=8$, 16 and 32, so it halves when
  $L$ doubles, and $L\langle|m|\rangle$ is 2.7 to 2.8, the order $1/L$ of the caption. It is 3.4 to 3.5 times the
  $\sqrt{2/(\pi N)}$ of independent spins, since the spins are correlated.
- The Ising side of the figure `igt_hist` is the pyqula script `g4_ising_snapshots.py` with its seed, 1000 snapshots
  on $16\times16$ every two sweeps after 500 sweeps. Its $|m|$ goes from 0.922 to 1 with the mean 0.987 at $T=1.5$,
  and from 0 to 0.508 with the mean 0.125 at $T=3.5$. So the two histograms do not overlap, while the largest $|m|$ at
  $T=3.5$ is above 0.5. A checkerboard run of 8000 sweeps in numpy gives the mean 0.124 at $T=3.5$.

## The Ising gauge theory of Section 10.6b

- The links are those of `igt_hist.py`, `h[x,y]` from $(x,y)$ to $(x+1,y)$ and `v[x,y]` from $(x,y)$ to $(x,y+1)$,
  and the plaquette at $(x,y)$ is `h[x,y] v[x+1,y] h[x,y+1] v[x,y]`. (10.10) has only the plaquette term, and the star
  of four links at a vertex is the gauge flip, a symmetry of (10.10) and not a term of it. Flipping the star at any
  vertex keeps every plaquette, on the tori of 3 to 6 sites per side, since four plaquettes hold two of the four links
  each and the others hold none. One flipped link changes two plaquettes.
- The configurations with every plaquette at $+1$ on the $L\times L$ torus are $2^{L^2+1}$ of the $2^{2L^2}$, 32 of
  256 for $L=2$ and 1024 of $2^{18}$ for $L=3$, counted one by one. The ones of $L=3$ fall in four sectors of the two
  loops around the torus, with $2^{L^2-1}=256$ gauge copies each, so the degeneracy is not only the gauge flips.
- On an open lattice the plaquettes are independent, so $\langle P\rangle=\tanh(J/T)$ exactly, 0.761594 at $T=J$,
  which is the form of the second quiz of Section 10.6b. On a torus the product of all the plaquettes is $+1$, and
  with $N$ plaquettes and $t=\tanh(J/T)$ the average is $\langle P\rangle=(t+t^{N-1})/(1+t^N)$. Enumeration gives both
  forms to $10^{-14}$ at $T=0.2$, 0.7, 1 and 5, on the open lattice of $2\times2$ plaquettes and on the tori of
  $2\times2$ and $3\times3$. The fraction of plaquettes at $-1$ is $(1-\langle P\rangle)/2$, so $4.5\cdot10^{-5}$ at
  $T=0.2\,J$ and 0.40 at $T=5\,J$ on an open lattice, and $5\cdot10^{-7}$ and 0.40 on the $16\times16$ torus of the
  figure `igt_hist`, where the plaquettes at $-1$ come in pairs. Both forms are smooth in $T$, so there is no
  transition at finite $T$, and this is the crossover of Section 10.6b.
- $\langle m\rangle=0$, and $\langle m^2\rangle$ is one over the number of links at every $T$, $1/18$ on the
  $3\times3$ torus at $T=0.2$, 1 and 5, by enumeration. The reason is the gauge freedom, since for every link a star
  flip changes its sign and not the energy. So "the magnetization is zero at all temperatures" of the quiz of
  Section 10.6b is the mean. On the $16\times16$ torus of 512 links, configurations with every plaquette at $+1$ in a
  random gauge and random links both give $\langle|m|\rangle=0.035$, which is $\sqrt{2/(512\pi)}$, and the root mean
  square 0.044, which is $1/\sqrt{512}$. The "$|m|\approx0.04$" of the caption of `igt_hist` is this number to one
  digit.
- The quantum version with a star term is the toric code $-\sum_vA_v-\sum_pB_p$, with $A_v=\prod\sigma^x$ on the four
  links of a star and $B_p=\prod\sigma^z$ around a plaquette, and the classical star flip is $A_v$ acting in the basis
  of $\sigma^z$. $A_v$ and $B_p$ commute, since they share 0 or 2 links. On the $2\times2$ torus exact diagonalization
  gives 4 ground states at $-8$, with the next level at $-4$. On the $3\times3$ torus 8 of the 9 stars and 8 of the 9
  plaquettes are independent, which leaves $18-16=2$ qubits and again 4 ground states.

## Hamiltonian learning of Section 10.7

- The toy of `ham_learning.py` has the matrix elements $-1$ and $-t_2$, so the band is $-2\cos k-2t_2\cos2k$ with
  $t=1$ in the sign of the notes, checked on the ring of 200 sites to $10^{-14}$. It goes from $-2-2t_2$ to $2-2t_2$
  for $t_2\le1/4$, $-2.4$ to $1.6$ at $t_2=0.2$, and up to $2t_2+1/(4t_2)$ above, $-2.800$ to $1.425$ at $t_2=0.4$.
  pyqula gives it with `tij=[-1., -t2]` on `geometry.chain()`, while `tij=[1., t2]` gives minus it, the mirror
  $E\to-E$.
- `set_finite_system(n=200, periodic=True)` and `get_supercell(200)` at $k=0$, each followed by `add_onsite(w)` with
  an array `w` of 200 values, give the matrix of the script to $10^{-14}$, the ring of 200 sites with the onsite
  energies `w` in the order of the sites.
- The levels of the ring for $t$ and $-t$ are the same at any $t_2$, and $t_2\to-t_2$ turns them into minus
  themselves. So the density of states never fixes the sign of $t$, and $t_2\to-t_2$ gives the mirror image $D(-E)$.
  For $t_2=0$, `get_dos(energies=E, delta=0.005, nk=20000)` gives $1/(\pi\sqrt{4t^2-E^2})$ per site to $10^{-3}$,
  0.1592 at $E=0$, the same for `tij=[1.]` and twice it with the spin. This is the figure `dos_sign` and the second
  quiz of Section 10.7.
- The seed 3 of the figure gives the errors 0.0635 trained on clean rings, 0.1027 on the test rings with $W>1$, and
  0.0043 trained with $W$ in $[0,1.5]$, the numbers that the script prints. The seeds 0 to 9 give 0.058 to 0.074,
  0.093 to 0.121 and 0.0040 to 0.0054, so the caption gives the ranges $0.06$ to $0.07$, about
  $0.1$ and $0.004$ to $0.005$ over ten draws. The two fits have
  the rank 27 and 38 of 41, since a clean ring leaves bins empty and the bins sum to 1 next to the constant, and
  `lstsq` takes the solution of smallest norm. Another least-squares solution of the clean fit, with a vector of norm
  1 of its null space added, gives 0.094 in place of 0.0635, so the clean numbers hold for `lstsq`. At most 1 percent
  of the levels of a ring fall outside $[-3.5,3.5]$.
- The script prints the same errors at every run. The clean ring with $t_2=0.35$ of the left panel has two levels at
  exactly $0.7$, and the one with $t_2=0.05$ has one level at exactly $-2.1$. These are edges of the 40 bins, so
  rounding decides their bin. The side changes from one run to another even with one thread. The two levels at
  $0.7$ fell on the two sides of the edge in six small processes and in one run of the check, and not in another run
  of the check, which is why the check prints
  their bins and does not assert them. This is a likely reason why the SVG of the script is not the same file at every
  run, which was not reproduced here with the script itself.
- The pairs $(\mathcal O,t)$ and $(\mathcal O,-t)$ have the smallest squared loss at the output 0, where the sum
  (10.12) over the two pairs is $2t^2$ and the mean is $t^2$. So the quiz of Section 10.7 gives the loss $2t^2$, which is
  $t^2$ per pair.

## pyqula

- pyqula has no many-body spin chain, no neural network and no Monte Carlo of a four-spin term. The attempts give
  `No module named 'pyqula.spinchain'` and `No module named 'pyqula.nnqs'`, and `LatticeIsing.add_tensor` with a
  function of four positions gives `missing 2 required positional arguments: 'r3' and 'r4'`, since it calls its
  function with the two positions of a pair. So the Heisenberg chain, the transverse-field chain and a neural network
  quantum state go to numpy or to dmrgpy, and the plaquette term of (10.10) and its Monte Carlo are numpy. What
  pyqula does for this session is the classical Ising model, the Hubbard mean field, the density of states and the
  ring, with the recipes of `webnotes/scripts/RECIPES.md`.

## Points of the old text, corrected on 2026-11-22

- The quiz on $L=40$ of Section 10.3a says "about 17.6 terabytes" in its option, in the decimal units of the figure
  `memory` and of the feedback of the quiz of Section 7.3, and "roughly 16 TiB" in its feedback. See the line on the
  memory.
- The text of the widget `netfit` in Section 10.2 says "4000 steps of Adam, a form of gradient descent, with the mean of
  the squared error". It says that one to three neurons cannot follow the six extrema, with $0.23$ for three, and that
  the loss goes down on the whole but not at every step of $H$, since it rises from $3.0\cdot10^{-3}$ at $H=5$ to
  $5.0\cdot10^{-3}$ at $H=7$. See the line on the widget.
- The second quiz of Section 10.7 says that the sum (10.12) over the two pairs is $2t^2$, which is $t^2$ per pair. See
  the line on the quiz of two labels.
- Section 10.3b writes (10.5) as the gradient with respect to a real parameter $\theta_k$. See the line on the
  gradient.
- The caption of the figure `ham_learning` gives the ranges over the seeds 0 to 9, $0.06$ to $0.07$, about $0.1$ and
  $0.004$ to $0.005$, of the 0.058 to 0.074, 0.093 to 0.121 and 0.0040 to 0.0054 of the seeds.
- The caption of the figure `ising_sizes` says that the three sizes agree with the exact curve within 0.007 up to
  $T=2.1$, and that at $T=2.2$ the lattice of 8 is 0.03 above it, 0.031 here. See the line on the figure below $T_c$.
