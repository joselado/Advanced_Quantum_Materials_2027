# Conventions of Session 5, checked by number

This sheet fixes the signs, the units and the pyqula facts that the pages, the figures and the pyqula scripts of
Session 5 use. An agent that edits the session reads it first and does not work these out again. Every bullet was
checked with a number on 2026-11-21. Two drafts were written apart, and a third calculation settled each line where
they differed or where only one of them had a line that a page needs. The energies are in units of the hopping $t$.
The pyqula of the checks is the development tree of version 0.0.95, at commit 7567127. The Berry curvature, the sign
of the Chern number and the units of `h.get_berry_curvature()` are those of `webnotes/conventions/session03.md`,
taken as they are. Session 9 adds magnetic impurities to the BdG Hamiltonian of this session, so the first section is
written so that Session 9 can use it as it is. A statement that is not on this sheet is checked before a page claims
it. The check is `webnotes/checks/session05/conventions.py`, which prints one line per bullet below, in the same order.

## The Nambu spinor and the BdG Hamiltonian

- pyqula uses the spinor (5.6), $\Psi=(c_\uparrow,c_\downarrow,c^\dagger_\downarrow,-c^\dagger_\uparrow)$, on every
  site, with the four entries of site $i$ at the indices $4i$ to $4i+3$. So the order is site first, then electron
  and hole, then spin. `h.add_swave(0.2)` on one site puts 0.2 at the entries (0,2) and (1,3) and nothing at (0,3) and
  (1,2). For an open chain of 3 sites, `tij=[-1.]`, `h.add_onsite(-0.4)` and `h.add_swave(0.3+0.2j)` give (5.7)
  written in real space, with a difference of 0. A Nambu Hamiltonian of pyqula always has the two spins, and
  `add_swave` or `setup_nambu_spinor()` on a chain made with `has_spin=False` turns its $1\times1$ matrix into a
  $4\times4$ one.
- The factor one half. Without the constant $-\sum_n|\Delta_n|^2/U$, the mean-field Hamiltonian (5.4) is
  $\frac12\sum\Psi^\dagger H_\text{BdG}\Psi+\frac12\mathrm{Tr}\,h$, with $h$ the electron block. This holds as an
  operator on four sites with hopping, onsite energy, Rashba coupling, an exchange field in a general direction and
  $\Delta=0.3e^{0.7i}$, to $10^{-15}$ in the 256 states. The many-body levels are
  $E_0=\frac12\mathrm{Tr}\,h-\frac12\sum_{E_n>0}E_n$ plus sums of the positive BdG levels, so each excitation is one
  positive level and the negative levels are copies of them. All 64 levels of a chain of 3 sites with $\mu=0.4$,
  $\Delta=0.3+0.2i$ and an exchange $(0.3,0.2,0.1)\cdot\boldsymbol\sigma$ agree with this to $4\cdot10^{-15}$, with
  $E_0=-4.6646$.
- `h.add_swave(Delta)` is the term $\Delta c^\dagger_\uparrow c^\dagger_\downarrow+\Delta^*c_\downarrow c_\uparrow$ of
  (5.4) with the same $\Delta$, complex or real, and `h.add_pairing(mode="swave", delta=Delta)` gives the same
  matrix. One site at $\mu=0$ with $\Delta=0.5$ has the ground state
  $(|0\rangle-c^\dagger_\uparrow c^\dagger_\downarrow|0\rangle)/\sqrt2$ at $-0.5$, the odd states at 0, and
  $\langle c_\downarrow c_\uparrow\rangle=-0.5$. $\Delta=-0.5$ gives the plus sign and $+0.5$. On the chain of 3 sites
  above, the exact $\langle c_\downarrow c_\uparrow\rangle$ of the middle site is $-0.1102-0.0735i$, the same as
  $\sum_{E_n<0}\phi_n(3)^*\phi_n(1)$ and $\sum_{E_n<0}\phi_n(4)^*\phi_n(2)$ from the BdG eigenvectors. So
  $\langle c_\downarrow c_\uparrow\rangle$ has the phase of $-\Delta$, which is the $g>0$ of the quiz of Section 5.5.
- In this basis $H_\text{BdG}(\mathbf k)=\begin{pmatrix}h(\mathbf k)&P(\mathbf k)\\P(\mathbf k)^\dagger&-\sigma_y
  h(-\mathbf k)^*\sigma_y\end{pmatrix}$. A term that keeps time reversal, the hopping, the onsite energy, the chemical
  potential or the Rashba coupling, enters as $\tau_z\otimes h(\mathbf k)$. An exchange or Zeeman field enters as
  $\tau_0\otimes\mathbf B\cdot\boldsymbol\sigma$, and an s-wave pairing as
  $\mathrm{Re}\Delta\,\tau_x-\mathrm{Im}\Delta\,\tau_y$. So an onsite energy 0.7 is $-0.7$ in the hole block, and an
  exchange keeps its sign. A magnetic impurity of Session 9 is then $\tau_0\otimes J\mathbf S\cdot\boldsymbol\sigma$
  on its site, and a potential impurity is $\tau_z\otimes V$. In the order of the notebook of Session 9,
  `add_onsite(1.8)`, `add_swave(0.2)` and then `add_exchange` and `add_onsite` with a function of the position that is
  nonzero on one site, the change is $\tau_0\otimes1.1\sigma_z+\tau_z\otimes0.6$ on that site, to $10^{-16}$, and
  nothing elsewhere.
- One site with $\mu$, $\Delta$ and an exchange $J$ along $z$ has the BdG levels $\pm J\pm\sqrt{\mu^2+\Delta^2}$. The
  exact ground state of the site is even below $J=\sqrt{\mu^2+\Delta^2}$, where this level crosses zero, and odd above
  it. For $\Delta=0.3$ and $\mu=0$, $J=0.2$ gives an even ground state at $-0.30$ and $J=0.4$ an odd one at $-0.40$, and
  $\mu=0.2$ moves the crossing to 0.361. pyqula with `add_exchange([0,0,J])` and `add_swave` on one site gives the same
  levels. This is the limit of one site of the bound state of Section 9.7, and the curve (9.10) is not checked here.
- Particle-hole symmetry reads $\tau_y\sigma_y H(\mathbf k)^*\tau_y\sigma_y=-H(-\mathbf k)$ in this basis, so a level
  $E$ at $\mathbf k$ has a partner $-E$ at $-\mathbf k$. It holds to 0 on the square lattice with Rashba coupling,
  exchange, onsite energy, s-wave and d-wave pairing at 5 random momenta, and on the triangular lattice with a complex
  $\Delta$, where the spectrum at one $\mathbf k$ alone is not symmetric. The 16 levels of the cluster of four sites
  come in pairs $\pm E$.
- The minus sign of the last entry of (5.6) makes the two blocks identical, with $\Delta$ in both, and it gives the
  rule of $\tau_z$ and $\tau_0$ above. Without the sign the pairing block of an s-wave $\Delta$ is $\Delta\sigma_z$,
  and the matrix still splits into the blocks $(e\uparrow,h\downarrow)$ and $(e\downarrow,h\uparrow)$, with a coupling
  0 between them, $+\Delta$ and $-\Delta$ and the same spectrum. An exchange $0.4\sigma_x$ then has the hole block
  $-0.4\sigma_x$, where it has $+0.4\sigma_x$ with the sign, while $0.4\sigma_z$ keeps its sign in both.
- `h.get_bands(operator="electron")` returns the weight of each state on the first two entries of each site, from 0
  to 1. For the upper branch of an s-wave chain it is $u^2=(1+\varepsilon/E)/2$, to $10^{-16}$, and with $\Delta=0$
  it is 1 for the bands $\varepsilon$ and 0 for the bands $-\varepsilon$. `h.get_dos()` counts the four BdG states
  of a site and is symmetric in $E$, `operator="electron"` counts the two electron states, and the electron and the
  hole parts add up to the full one. For the notebook cell with `set_filling(0.2)` and `add_swave(0.8)` on the chain,
  `delta=0.01` and `nk=1000`, the integrals on $(-5,5)$ are 3.993 and 1.996, and the peak of the full one is at 0.81.
  A numpy sum of Lorentzians over the BCS bands gives the same curves. The electron part is the one that STM
  measures, and it is not symmetric when $\mu\neq0$.
- `h.get_gap()` of a BdG Hamiltonian is the distance between the two branches. It gives 0.6000 for the s-wave chain
  with $\Delta=0.3$, as `physcheck.gap` with half of the bands filled does, and 0.5992 for the $2\times2$ triangular
  cell of the notebook of Session 9 with `add_onsite(-4.0)` and `chiral_pwave` 0.1, where a minimization over
  $\mathbf k$ gives the same. So the `h.get_gap()/2` of that notebook is the smallest quasiparticle energy, 0.2996, just
  below three times `delta`, as the sheet of Session 9 says. The warning of the sheet of Session 3 on
  `h.get_gap()` still holds for other models.

## pyqula, the normal state

- The first-neighbor hopping of pyqula is $+1$. The chain has $2\cos k$, with 2 at $k=0$, the square lattice
  $2(\cos k_x+\cos k_y)$, with 4 at $\Gamma$ and $-4$ at $M$, and the triangular lattice runs from $-3$ to 6, with the
  top at $\Gamma$. This is the $\varepsilon(\mathbf k)$ of the notes with $t=-1$, and `tij=[-t]` gives the $t$ of the
  notes. On the chain and on the square lattice the sign of $t$ is the gauge $c_n\to(-1)^nc_n$, which is the same as
  a shift of $\mathbf k$ by $\pi$ or by $(\pi,\pi)$. It keeps the spectrum and changes the sign of a pairing on the
  bonds, which does not change the Chern number, so `chiral_pwave` 0.25 on the square lattice gives the same $C$ for
  `tij=[1.]` and `[-1.]`, $+2$, $+2$, $-2$, $-2$ for `add_onsite` 2, 1, $-1$, $-3$. On the triangular lattice the
  sign is not a gauge, and `tij=[-1.]` gives another band, from $-6$ to 3.
- `h.add_onsite(x)` adds $+x$ to every electron energy, so it is $\mu=-x$ of the notes, and it is $\tau_zx$ in the
  Nambu matrix. `h.set_filling(f)` fills the fraction $f$ of the two states of each site, so 0.2 on the chain adds
  1.6180 and leaves a fraction 0.2000 of the band $2\cos k+1.618$ below zero. Both give the same matrix before or after
  `setup_nambu_spinor`. The notebook of Session 9 calls the argument `mu`, so its `mu = 1.` is $\mu=-t$ of the notes,
  where the spinless chain has $D(E_F)=0.1838$ from `get_dos`, as the sheet of Session 9 says.
- `h.add_exchange([0,0,J])` is $+J(n_\uparrow-n_\downarrow)$, so the spin-up band moves up by $J$, and
  `h.add_zeeman` is the same term. The chain bands split by 2 for $J=1$ and by 4 for $J=2$, and the upper band has
  $s_z=+1$. The exchange field $-h(n_\uparrow-n_\downarrow)$ of Section 5.12 is `add_exchange([0,0,-h])`.

## pyqula, the pairing

- For a pairing on the bonds, `delta` of `add_pairing` is not the $\Delta_0$ of the notes. On the square lattice
  `mode="dx2y2"` with `delta=x` gives $2x(\cos k_x-\cos k_y)$ at the entries (0,2) and (1,3), so $\Delta_0$ of
  (5.13) is $2x$, with $-4x$ at $X$, and `"extended_swave"` gives $2x(\cos k_x+\cos k_y)$, read at four momenta. The
  onsite `"swave"` gives $x$.
- `mode="chiral_pwave"` with `delta=x` gives $-2ix(\sin k_x+i\sin k_y)$ at (0,2) and $+2ix(\sin k_x+i\sin k_y)$ at
  (1,3). This is a triplet with its d-vector along $z$, the $p_x+ip_y$ of (5.15) with $\Delta_0=2x$ up to the constant
  phase $-i$, and its two blocks carry $\Delta$ and $-\Delta$. pyqula has no mode for $p_x-ip_y$, and `L=-1` as a
  keyword of `chiral_pwave` raises a TypeError. The pairing `mode=partial(get_triplet, df=get_callable([0.,0.,1.]),
  L=-1)`, with `partial` from `functools`, `get_triplet` from `pyqula.sctk.pairing` and `get_callable` from
  `pyqula.utilities`, defines no function, so a script to download can use it, and it puts $-2ix(\sin k_x-i\sin k_y)$
  at (0,2). On the triangular model of the notebook, with `add_onsite(-3.0)`, `chiral_pwave` gives $C=-2$ and this
  pairing $C=+2$, with `get_chern` and with the Kubo form, and the sign of `delta` changes neither.
- `mode="pwave"` on a chain with `delta=x` and a vector `d` gives the block $-2ix\sin k\,(\mathbf d\cdot\boldsymbol
  \sigma)$, for `d` along $x$, along $z$ and `[1,1,0]`, so `d` is not normalized. `d=[1,0,0]` pairs up with up and down
  with down, and the amplitude of the down-down pair is $x|d_x+id_y|$, so `d=[1,1,0]` gives $\sqrt2\,x$.
- `mode="nodal_fwave"` on the triangular lattice is odd in $\mathbf k$, zero on the three lines $\Gamma$-$M$, with the
  largest entry $10^{-15}$, and up to 1.42 on $\Gamma$-$K$. At $\mu=0$ the Fermi surface crosses $\Gamma$-$M$ at 2/3 of
  the way to $M$, where $|E|$ is below $10^{-15}$, so the nodes are on the Fermi surface. On the path `G`, `K`, `M`, `G` of
  the notebook the smallest $|E|$ is set by the steps of the path, 0.0182 with the default 546 steps and 0.0036 with
  `nk=2000`, and the s-wave 0.4 gives 0.4004 and 0.4000 there, against 0.4 on the Fermi surface. A page quotes the
  value on the Fermi surface.

## The gap

- For s-wave pairing the smallest quasiparticle energy of (5.9) is $|\Delta|$, at $\varepsilon=0$, and the two
  branches are $2|\Delta|$ apart, for any $\mu$ inside the band and on any lattice. On the square lattice with
  `set_filling(0.2)`, `add_swave(0.8)`, `0.4` and `0.2` give 0.8000, 0.4000 and 0.2000 on the path of the notebook.
  A minimization over $\mathbf k$ gives 0.3000 on the chain with $\Delta=0.3$ for $\mu=-1.2$, 0 and 1.2, which is the
  figure of Section 5.9, 0.3000 on the triangular lattice with $\Delta=0.3$ for `add_onsite` $-4$, 0 and 2, and 0.5000
  on the honeycomb lattice of the notebook cell with $\Delta=0.5$ for `add_onsite` from $-1$ to 2.5. Outside the band
  it is larger, 0.5831 for $\mu=2.5$ on the chain, which is $\sqrt{0.5^2+0.3^2}$. `physcheck.gap` with half of the
  bands filled returns $2|\Delta|$.

## The mean field

- $\Delta_n=U\langle c_{n\downarrow}c_{n\uparrow}\rangle$ of (5.3) is the fixed point of
  `h.get_mean_field_hamiltonian(U=U, filling=0.1, nk=100, mix=0.5, mf="swave")` after `h.setup_nambu_spinor()`, with
  the $U$ of the term $Un_\uparrow n_\downarrow$ of (5.2). `filling` is the fraction of the electron states that are
  filled, so 0.1 is 0.2000 electrons per site. $U=-1$, $-1.5$ and $-2$ give the real $\Delta=0.1031$, 0.2226 and
  0.3606 at the entry (0,2) of `hscf.intra`. This is $U\langle c_\downarrow c_\uparrow\rangle$ from the eigenvectors of
  the solution and the BCS gap equation solved with numpy at the same density, to $10^{-4}$. The smallest $|E|$ is
  $|\Delta|$, and a run with another random seed gives the same value.
- The interaction-driven triplet of the notebook, the triangular lattice with `add_exchange([0,0,-2])`, `V1=-1`,
  `filling=0.3`, `mix=0.3` and `mf="random"`, converges to a pure up-up triplet with $|C|=1$ on every random start.
  The sign of $C$ is chosen by the start, $+1$, $-1$, $-1$, $+1$ for the seeds 0 to 3. The two branches are 0.373 apart,
  so the smallest energy is 0.186. A mesh only bounds this from above, and it gives 0.376 with 48 points and 0.375 with
  60. A page gives $|C|=1$ for this state, and not 2, since only one spin pairs, and it says that the sign is chosen
  spontaneously.

## The Chern number of the BdG bands

- `h.get_chern()` of a BdG Hamiltonian counts all the BdG bands below zero, with no factor one half and with the sign
  of Session 3. For the chiral p-wave of the notebook it is $-2.0000$, and `physcheck.chern_links` on the two bands
  below zero agrees.
- The block (5.8) with $\Delta_0(\sin k_x+i\sin k_y)$, $\varepsilon=-2t(\cos k_x+\cos k_y)-\mu$, $t=1$ and
  $\Delta_0=0.5$ has $C=+1$ for $\mu=-3.5$, $-2$ and $-1$, a pocket of filled states around $\Gamma$, $C=-1$ for
  $\mu=1$ and 3, a pocket of empty states around $M$, and $C=0$ for $\mu=5$, by the links and by the Kubo form.
  $p_x-ip_y$ gives the opposite signs. So the sign of $C$ is set by the chirality together with the side of the
  Fermi surface, and the two spin blocks give $\pm2$.
- `chiral_pwave` 0.25 on the square lattice with `tij=[-1.]` and `add_onsite(-mu)` gives $C=+2$, $+2$, $-2$ and 0 for
  $\mu=-2$, $-1$, 1 and $-5$. The triangular model of the notebook, with the hopping $+1$ and `add_onsite(-3.0)`, has
  $\varepsilon(\Gamma)=+3$, a pocket of empty states around $\Gamma$, and gives $C=-2$ for `chiral_pwave` 0.4 and 0.8
  and 0 for `swave` 1.0. With `tij=[-1.]` and `add_onsite(3.0)` the same Fermi surface encloses filled states, and
  `chiral_pwave` 0.4 gives $+2$. `get_chern` and the links agree in every case. The magnitude 2 of the try-it of
  Section 5.14 holds.
- On the ribbon `ribbon.bulk2ribbon(g, n=20)` of the notebook model, whose bulk has the smallest energy 1.336, the
  energies 0.1, 0.3, 0.5 and $-0.5$ are crossed by two branches going down with $k$ at the edge of positive $y$ and by
  two going up at the other edge. $p_x-ip_y$ reverses all of them, and the s-wave ribbon keeps its smallest energy
  1.0000. A page states the number of branches and that the chirality reverses them, and it takes the direction at
  a given edge from this computation and not from the sign of $C$, as the sheet of Session 3 asks.
- The notebook cell of the transition against the exchange field, the triangular lattice with `add_onsite(-5.7)`,
  `add_rashba(1.0)`, `add_zeeman([0,0,J])` and `add_swave(0.3)`, has the band at 0.3 at $\Gamma$, the levels
  $\pm J\pm\sqrt{0.3^2+0.3^2}$ at $\Gamma$, and the closing at $J=0.4243$. On the 9 values of $J$ of the cell, from 0
  to 0.6, the smallest $|E|$ on the path `M1`, `G`, `M1` is 0.300, 0.290, 0.258, 0.199, 0.124, 0.049, 0.026, 0.101 and
  0.176. At $J=0$ it sits on the Fermi pocket, while the level at $\Gamma$ starts at 0.424 and is the lowest from
  about $J=0.2$ on. $C$ is 0 at $J=0.3$ and 0.375 and $+1$ at $J=0.525$ and 0.6. The try-it of Section 5.18 holds.
- The cells "Artificial topological superconductivity" and "Edge states of an artificial topological
  superconductor", the triangular lattice with `add_rashba(1.0)`, `add_onsite(2.0)`, the Zeeman field $-0.6$ or
  $+0.6$ and `add_swave(0.3)`, give $C=+3$ and $-3$, with `get_chern` and with the Kubo form, and the smallest energy
  0.2101 in both.

## The Kitaev chain

- The Majorana operators (5.17) have $\gamma_A^2=\gamma_B^2=1$, $\{\gamma_A,\gamma_B\}=0$,
  $i\gamma_A\gamma_B=2c^\dagger c-1$, which is $-1$ on the empty mode, $\gamma_A\gamma_B|0\rangle=i|0\rangle$,
  $\gamma_B\gamma_A|0\rangle=-i|0\rangle$ and $c=(\gamma_A+i\gamma_B)/2$, checked with the matrices of one mode.
- With $c_n=(\gamma_{2n-1}+i\gamma_{2n})/2$, (5.19) at $\Delta=t$ and $\mu=0$ is exactly (5.21),
  $it\sum_n\gamma_{2n}\gamma_{2n+1}$, on an open chain of 4 sites, and $\gamma_1$ and $\gamma_8$ commute with it. The
  same holds for $t=\Delta=-1$. For $\Delta=-t$ it is $-it\sum_n\gamma_{2n-1}\gamma_{2n+2}$, with $\gamma_2$ and
  $\gamma_7$ free, so the pattern of (5.21) needs $\Delta=t$.
- The BdG matrix of (5.19) in the basis $(c_1,\dots,c_N,c^\dagger_1,\dots,c^\dagger_N)$ has the pairing matrix
  $d_{n+1,n}=\Delta=-d_{n,n+1}$. It is the matrix of the figure scripts and of the widget, and it gives the 16
  many-body levels of 4 sites at four pairs of $\mu$ and $\Delta$ to $10^{-14}$. With the Fourier transform (2.7) its
  entry above the diagonal on a ring is $-2i\Delta\sin k$, with $-2t\cos k-\mu$ on the diagonal. (5.20) writes
  $+2i\Delta\sin k$, which is the entry below the diagonal. The two differ by $\Delta\to-\Delta$, a gauge, so the
  spectrum and the Zak phase are the same, $\pi$ at $\mu=t$ and 0 at $\mu=3t$, while the signed winding of
  $(\varepsilon,\mathrm{Im}\,\Delta(k))$ is $-1$ with one sign and $+1$ with the other.
- At $\Delta=t$ and $\mu=0$ the bulk energy is $E(k)=2t$ for every $k$. In pyqula this point is `add_onsite(4.0)`,
  `add_exchange([0.,0.,4.])` and `mode="pwave"` with `delta=1.0` and `d=[1.,0.,0.]`, and the two lowest $|E|$ are
  below $2\cdot10^{-15}$ for 5, 12 and 31 sites, with the next level at $2t$.
- The smallest bulk energy of the Kitaev chain is $\Delta\sqrt{4-\mu^2/(t^2-\Delta^2)}$ when $\Delta<t$ and
  $|\mu|t\le2(t^2-\Delta^2)$, and $|2t-|\mu||$ otherwise. It is $0.8165t$ for $\mu=t$ and $\Delta=0.5t$, $0.5790t$ for
  $\mu=0.5t$ and $\Delta=0.3t$, $0.1000t$ for $\mu=1.9t$ and $\Delta=0.5t$, and $t$ for $\mu=\Delta=t$, by the formula
  and by a minimization over $k$. For $\mu=t$ and $\Delta=0.5t$ the two branches are $1.633t$ apart, and an open chain
  of 200 sites has its first bulk level at $0.8167t$.
- The topological range (5.22) is $|\mu|<2t$ for $\Delta\neq0$. For $\mu=0$, $t$ and $1.5t$ the sign of
  $\varepsilon(0)\varepsilon(\pi)$ is $-1$, the Zak phase of the BdG bands below zero is $\pi$ with
  `physcheck.zak_phase` and with `topology.berry_phase`, and an open chain of 60 sites with $\Delta=0.7t$ has a level
  below $10^{-3}$. For $\mu=2.5t$ and $3t$ the sign is $+1$, the phase 0, and the lowest levels $0.507t$ and $1.005t$.
  pyqula returns $+\pi$ or $-\pi$ for the same chain, both in a few runs with other $\mu$ and `nk`, so a page says
  $\pi$ modulo $2\pi$. With $\Delta=0.5t$ the smallest energy is $0.100t$ at $\mu=1.9t$ and at $2.1t$.
- The two end modes of an open chain split by an energy that falls as $|\lambda|^N$, with $\lambda$ the root of larger
  modulus of $(t+\Delta)\lambda^2+\mu\lambda+(t-\Delta)=0$. This $\lambda$ is the ratio $a_{n+1}/a_n$ of the Majorana
  zero mode at the left end, $-0.8937$ for $\mu=1.9t$ and $\Delta=0.5t$, so that mode changes sign from one site to
  the next. For $\mu^2<4(t^2-\Delta^2)$ the roots are complex, $|\lambda|=\sqrt{(t-\Delta)/(t+\Delta)}$, and the
  splitting oscillates. For $\Delta=0.5t$ and $\mu=t$ it is $0.0111t$ for $N=8$, $1.94\cdot10^{-5}t$ for $N=20$ and
  $3.49\cdot10^{-10}t$ for $N=40$, its envelope goes as $e^{-0.55N}$, against $\ln|\lambda|=-0.549$, and the first bulk
  level is $0.8933t$ for $N=8$ and $0.8347t$ for $N=20$. For $\Delta=0.9t$, $\mu=t$ and for $\Delta=0.5t$, $\mu=1.9t$
  the roots are real, and one more site multiplies the splitting by 0.3921 and by 0.8937, so the decay is much slower
  near the transition. The trivial chain of 40 sites with $\mu=2.5t$ and $\Delta=0.5t$ has its lowest level at
  $0.511t$, the $0.51t$ of the figure of Section 5.17.
- pyqula has no spinless BdG Hamiltonian, so the notebook builds the Kitaev chain from the two spins.
  `add_onsite(4.0)`, `add_exchange([0.,0.,4.])`, `add_onsite(m)` and `mode="pwave"` with `delta` and `d` put spin down
  at $2\cos k+m$ and spin up 8 higher, and the $L$ lowest levels of an open chain of $L$ sites are those of (5.19)
  with $t=1$, $\mu=-m$ and $\Delta=\delta|d_x+id_y|$, to $10^{-14}$. `set_finite_system(n=8)` of the bulk chain gives the
  same chain. The cell of Section 5.17, with `delta=0.1`, `d=[1.,1.,0.]` and the last length $L=40$, gives the lowest
  levels $1.65\cdot10^{-3}$, $1.39\cdot10^{-3}$ and 0.506 for `mu` 0.3, 1.0 and 2.5, and $L=30$ gives
  $2.0\cdot10^{-5}$ for `mu=0.3`, since the splitting oscillates with $L$.
- The cell of the local density of states, 100 sites with `delta=0.2`, `d=[1,0,0]` and $\mu=0$, gives with the
  broadening 0.02 the electron density of states at $E=0$ equal to 4.427, 0.0843 and 0.0081 on the sites 0, 10 and 50.
  The spinless chain alone gives 4.427, 0.0842 and 0.0079, and the spin-up band, 6 above zero, adds its tails,
  $10^{-4}$ at most.
- The widget `kitaevbdg`, with 30 sites and $t=\Delta=1$, has the levels of (5.19), and its lowest level is at
  $1.4\cdot10^{-9}$ for $\mu=1$, $1.56\cdot10^{-4}$ for $\mu=1.5$ and 0.0475 for $\mu=1.9$, where the bulk value
  $|2t-|\mu||$ is 0.1. At $\Delta=t$ the root above is $-\mu/2t$, so one more site multiplies the splitting at
  $\mu=1.5$ by 0.7500, and close to $|\mu|=2t$ the two end modes of 30 sites overlap.

## The helical edge

- The edge $\tau_z(vk\sigma_z-\mu)+h\sigma_x+\Delta\tau_x$ in the basis (5.6) has at $k=0$ the levels
  $\pm h\pm\sqrt{\Delta^2+\mu^2}$, so $\pm0.2$ and $\pm0.8$ for $h=0.3$, $\Delta=0.5$ and $\mu=0$. Its gap over all $k$
  closes only at $h=\sqrt{\Delta^2+\mu^2}$, checked for four pairs of $\mu$ and $\Delta$. The closing at $h=\Delta$
  of the figure of Section 5.18 is the case $\mu=0$.
- The two sides of the closing are two phases. On a lattice edge $v\sin k\,\sigma_z+W(1-\cos k)\,\sigma_x$, where the
  second term gaps the doubler at $k=\pi$, the index $\mathrm{sign}[\mathrm{Pf}(0)\,\mathrm{Pf}(\pi)]$ of the BdG
  Hamiltonian in the Majorana basis is $-1$ for $h<\sqrt{\Delta^2+\mu^2}$ and $+1$ above it. A segment with $\Delta=0.3$
  between two magnets with $h=0.6$ has two levels at $10^{-16}$, with all their weight within 15 sites of the two
  interfaces, and the next level at 0.301. With $\Delta=0.3$ everywhere, $h=0.1$ inside and 0.5 outside give two
  levels at $3\cdot10^{-11}$ at the interfaces, while $h=0.1$ inside and 0.2 outside put the two zero levels at the open
  ends of the lattice. So the zero mode sits at the boundary between $h<\Delta$ and $h>\Delta$, as the caption of the
  figure of Section 5.18 says.

## Braiding and the gauge phase

- The braid (5.23), $U_{12}=\exp(\frac\pi4\gamma_1\gamma_2)=(1+\gamma_1\gamma_2)/\sqrt2$, sends $\gamma_1$ to
  $-\gamma_2$ and $\gamma_2$ to $\gamma_1$, keeps the parity, and multiplies the states with $i\gamma_1\gamma_2=-1$ and
  $+1$ by $e^{i\pi/4}$ and $e^{-i\pi/4}$. $i\gamma_1\gamma_2$ and $i\gamma_2\gamma_3$ anticommute, $i\gamma_1\gamma_2$
  and $i\gamma_3\gamma_4$ commute, $U_{12}U_{23}-U_{23}U_{12}$ has entries up to 1.00, and $U_{12}U_{34}=U_{34}U_{12}$,
  checked as $4\times4$ matrices on two fermion modes.
- Under $c\to c\,e^{i\varphi}$ the term $c^\dagger_\uparrow c^\dagger_\downarrow$ gets $e^{-2i\varphi}$, as (5.5) says,
  and the ground state of one site with $\Delta e^{2i\varphi}$ has $\langle c_\downarrow c_\uparrow\rangle$ multiplied
  by $e^{2i\varphi}$, checked for $\varphi=0.3$. So the $e^{-2i\varphi}$ of (5.5) for the operator and the
  $\Delta\to\Delta e^{2i\varphi}$ of Section 5.7 and of the index page are the same statement.

## Pairing symmetry

- The electron-hole block of pyqula is $P(\mathbf k)=\psi(\mathbf k)\sigma_0+\mathbf d(\mathbf k)\cdot
  \boldsymbol\sigma$, and the pair matrix is $G=P\,i\sigma_y$. Fermi antisymmetry (5.11), $G(\mathbf k)=-G(-\mathbf
  k)^T$, reads $P(\mathbf k)=\sigma_yP(-\mathbf k)^T\sigma_y$ in this basis, and it holds to $10^{-16}$ for `dx2y2`,
  `extended_swave`, `chiral_pwave`, `swave` and `pwave` with `d=[1,1,0]`. The singlet part is $\psi\sigma_0$ and even
  in $\mathbf k$, and the triplet part is odd, as (5.12) says.
- The form (5.7), with one $\Delta(\mathbf k)$ in both blocks, is a pairing only for an even $\Delta(\mathbf k)$. The
  operator of an odd $\Delta(\mathbf k)$ on the identity is $10^{-17}$ on a ring of 4 sites, and the BdG matrix with
  $\Delta_0(\sin k_x+i\sin k_y)$ times the identity breaks particle-hole symmetry, while its smallest energy is still
  0.50 at $\mu=-2$ and $\Delta_0=0.5$. A triplet with its d-vector along $z$ enters as $\Delta(\mathbf k)\sigma_z$, so
  the two blocks carry $+\Delta(\mathbf k)$ and $-\Delta(\mathbf k)$, and it keeps the symmetry and has $C=+2$ there.
- (5.10) is used for its symmetry only. Its sign and its one half are not those of (5.4), and the prime of its sum is
  not defined on the page. With the sum over the whole zone, the s-wave $\Delta$ of (5.4) is
  $\Delta_{\uparrow\downarrow}=-\Delta$ and $\Delta_{\downarrow\uparrow}=+\Delta$, as operators on rings of 3 and 4
  sites to $10^{-16}$. With the sum over half of the zone the same algebra gives $-2\Delta$. A page takes amplitudes
  from (5.4) and (5.7), and not from (5.10).
- $\Delta_d=\Delta_0(\cos k_x-\cos k_y)$ vanishes on $k_x=\pm k_y$, and at $\mu=0$ the Fermi surface of the square
  lattice passes through $(\pi/2,\pi/2)$. On a circle of radius 0.3 around $X$ the factor $|\cos k_x-\cos k_y|$ goes
  from 1.9552 to 1.9553, and down to 1.876 on a radius 0.5, so the energy on a pocket around $X$ is close to
  $2\Delta_0$ and below it.
- The p+ip gap is not uniform on the Fermi surface. With $\Delta_0=0.2t$ at $\mu=-2t$, $|\Delta_{p+ip}|$ goes from
  $0.2000t$ to $0.2449t$ along the Fermi surface, and the smallest energy is $0.2000t$ for s-wave and for p+ip. At
  $\mu=-3.5t$ it is $0.2000t$ for s-wave and $0.1314t$ for p+ip. So the same gap of Section 5.14 needs the two
  amplitudes chosen for it.

## Constants

- $h/2e=2.0678\cdot10^{-15}$ Wb and $h/e=4.1357\cdot10^{-15}$ Wb, and the AC Josephson frequency $2eV/h$ is 483.6 MHz
  per microvolt. The phonon interaction $V_\text{eff}(\omega)=V_c-(2g^2/\omega_0)/[1-(\omega/\omega_0)^2]$ of the
  figure of Section 5.4, with $V_c=0.5$ in units of $2g^2/\omega_0$, is at most $-0.50$ below $\omega_0$ and positive
  above it. It is negative for every $\omega<\omega_0$ only when $V_c<2g^2/\omega_0$, and $V_c=1.5$ gives $+0.5$ at
  $\omega=0$.

## Open points of the old text, left as they are

These were found while the sheet was checked. A change of an equation, of a statement of the old text or of a
convention is the lecturer's decision, so they are left as they are, and a page that touches them says the condition.

- Section 5.8 says of the minus sign of (5.6) that "without it, the two spin blocks would mix through a Pauli
  matrix". Without the sign the pairing block is $\Delta\sigma_z$ and the coupling between the two blocks is 0, as the
  bullet on the minus sign above says. The sign makes the two copies identical, as the caption of the figure of the
  blocks says.
- The quiz of Section 5.10 says $|\Delta_d|\approx2\Delta_0$ and $E\geq2\Delta_0$ on a pocket around $X$. On a pocket
  of radius 0.3 it is $1.955\Delta_0$, and $1.876\Delta_0$ for a radius 0.5, so $E$ is slightly below $2\Delta_0$.
- (5.10) in Section 5.11 has the opposite sign of (5.4), $\Delta_{\uparrow\downarrow}=-\Delta$ with the sum over the
  whole zone, and the prime is not defined, as the bullet on (5.10) above says.
- Section 5.14 says that the sign of $C=\pm2$ "is set by the chirality". It is set by the chirality together with the
  side of the Fermi surface. The same $p_x+ip_y$ gives $-2$ with the pocket of empty states of the notebook and $+2$
  with a pocket of filled states, and $p_x-ip_y$ gives $+2$ on the notebook model. The quiz that goes from $+2$ to $-2$
  holds for a pocket of filled states, as in Figure 5.4. The same section and the caption of Figure 5.4 count one
  branch "from each of the two identical spin blocks". For this triplet the blocks
  carry $+\Delta(\mathbf k)$ and $-\Delta(\mathbf k)$, so they have the same spectrum and the same Chern number, but
  they are not (5.8) with one $\Delta$.
- The quiz of Section 5.14 says that both gaps "are the same on the same Fermi surface, since $E=|\Delta|$ there". On
  the Fermi surface of $\mu=-2t$ the p+ip gap goes from $0.200t$ to $0.245t$ while the s-wave one is $0.2t$. The
  smallest energies are both $0.2t$, as the quiz says, and at $\mu=-3.5t$ they differ, $0.2t$ against $0.1314t$.
- (5.20) in Section 5.16 and the quiz of Section 5.20 write $\Delta(k)=2i\Delta\sin k$. With the Fourier transform
  (2.7) the entry of (5.8) is $-2i\Delta\sin k$, and the printed form is the entry below the diagonal. Nothing that a
  page computes depends on it, since the sign changes only the signed winding.
- The try-it of Section 5.5 gives $|\Delta|$ "from about 0.1 to 0.2 and 0.4". The loop gives 0.103, 0.223 and 0.361,
  which is 0.1, 0.2 and 0.4 to one digit, and a page that quotes two digits writes 0.10, 0.22 and 0.36.
- The text of the widget of Section 5.17 says that for $|\mu|<2t$ two levels sit at zero energy. With 30 sites they
  are at $1.6\cdot10^{-4}$ for $\mu=1.5t$ and at $0.047t$ for $\mu=1.9t$, half of the bulk value $0.1t$.
- The word gap means $2|\Delta|$, the distance between the two branches, in Sections 5.8 and 5.9, and the smallest
  quasiparticle energy in the try-it of Section 5.13, in the quiz of Section 5.17 with its $0.82t$, which is
  $0.8165t$ while the branches are $1.633t$ apart, and in the widget. The two differ by a factor two, and a page
  says which one it means.
- The try-it of Section 5.17 says that the line `mu = 0.3` sets the chemical potential. In the cell `mu` is the
  argument of `add_onsite`, so it is $\mu=-0.3$ of (5.22). (5.22) depends only on $|\mu|$, and $\mu=+0.3$ gives the
  same splitting, $1.65\cdot10^{-3}$, so what the try-it says about the levels holds.
- The notebook text, which is not a page, writes the exchange as $-Js_z$ with $E_\uparrow=E-J$, while
  `add_exchange([0,0,J])` moves the spin-up band up by $J$. It also writes the hole block as $-(H_0-\mu)^*$, which holds
  only for a Hamiltonian that does not depend on spin, and for a Rashba coupling 0.3 at the reduced momentum
  $(0.1,0.2)$ it is off by 0.71.
