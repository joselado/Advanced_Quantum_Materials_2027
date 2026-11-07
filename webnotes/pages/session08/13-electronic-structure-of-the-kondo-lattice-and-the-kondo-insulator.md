## Electronic structure of the Kondo lattice and the Kondo insulator {#sec-8-13 number="8.13"}

For each spin, equation [(8.21)](#eq-8-21) is an ordinary two-band Bloch Hamiltonian, in the sense of Section [2.5](#sec-2-5), in the basis $(c_{\mathbf
k\alpha}, f_{\mathbf k\alpha})$. When $\gamma_K = 0$, there is no mixing at all. The spectrum is then the ordinary dispersive conduction band $\varepsilon_{\mathbf k}$, together with a completely **flat** band of $f$-fermion levels at zero energy. This band is flat because the auxiliary fermions have no hopping of their own when the Kondo coupling is zero. When we switch the Kondo coupling on again, $\gamma_K$ becomes finite, and the flat band and the dispersive band have an **anti-crossing**. In every place where the flat spinon band would cross the conduction band, a **gap** opens instead, and the gap is larger when the Kondo coupling is larger. We see this directly when we compare the spectra for increasing $J_K$. At $J_K=0$ the bands cross. At $J_K=0.25$ there is already a visible gap at the crossing. At $J_K=0.5$ the gap is much larger. Figure [8.6](#fig:s08:kondobands) shows the two ends of this comparison, and where the Fermi level is in each case.

![Why a lattice of local moments is an insulator, drawn from [(8.21)](#eq-8-21) per spin in one dimension. (a) With the Kondo coupling switched off, [(8.21)](#eq-8-21) is a dispersive conduction band $\varepsilon_{\mathbf k}$ together with a completely flat band of $f$ levels, the red line. This band is flat because the auxiliary fermions have no hopping of their own, and the two bands cross at the Fermi level, which gives a metal. (b) A finite hybridization $\gamma_K$ removes the crossing. The bands repel each other, the states close to the crossing become mixtures of conduction electron and local moment, and a gap opens at the crossing. With one $f$ fermion per site from the constraint [(8.11)](#eq-8-11) and a half-filled conduction band, the lower hybridized band is full. So the Fermi level is inside the gap, and the metal has become a **Kondo insulator**. The gap grows with $\gamma_K$, and so with the Kondo coupling $J_K$, and the nearly flat band edges that remain are the reason why the remaining quasiparticles are heavy.](figures/s08f06_kondo_bands.svg){#fig:s08:kondobands number="8.6"}

Physically, the ground state of this hybridized system is non-magnetic by construction. It has total spin zero and it is time-reversal symmetric, in the same way as for the single impurity [(8.17)](#eq-8-17) and for the quantum spin liquid of Section [8.9](#sec-8-9). The consequence for the electronic structure, however, is new. A lattice of Kondo impurities turns a system that would otherwise be an ordinary metal into an **insulator**, because every electron at the Fermi surface forms a bound state with a magnetic impurity. This is the **Kondo insulator**, which is also called a heavy-fermion insulator, and SmB$_6$, which we already introduced in Section [8.1](#sec-8-1), is the standard real material example.

Note that there is a similarity with a quite different construction of Session 5. Superconductors also open a gap in their quasiparticle spectrum through a hybridization, the pairing $\Delta$ in the Bogoliubov-de Gennes Hamiltonian of Section [5.8](#sec-5-8). There it is between electrons and holes and not between electrons and auxiliary fermions. The two systems are physically very different, but the *mechanism* that opens a gap in the single-particle spectrum is very similar. The way the effect appears is also similar. The temperature scale at which the gap of the Kondo insulator becomes visible depends on the Kondo coupling in a strongly non-linear way. We know the same kind of non-linear dependence from the superconducting gap as a function of the pairing interaction.

![One mechanism for two gaps, both computed from a $2\times2$ Bloch Hamiltonian in one dimension. On the left is [(8.21)](#eq-8-21) per spin with $t=1$ and $\gamma_K=0.6$. The conduction band $c$ crosses the flat $f$ level at the Fermi level, and the hybridization opens a gap there. On the right is the Bogoliubov-de Gennes Hamiltonian of Section [5.8](#sec-5-8) with $\Delta=0.5$, where the electron band $e$ crosses its hole copy $h$. The dashed lines are the bands without mixing, and the shaded band is the gap. In the Kondo lattice the indirect gap is about $\gamma_K^2/t$, while in the superconductor the gap is $2\Delta$.](figures/web/session08/kondo_bdg.svg){#sch:s08:kondo_bdg alt="Two band plots against momentum, a cosine band and a flat level that repel into a gap on the left, and an electron band and its mirror hole band that repel into a gap on the right."}

::: notebookbox
**Notebook check-in:** [`session8.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session8.ipynb), "Quantum magnetism in the Kondo lattice" (Core) and "Spinon dispersion in the Kondo lattice" (Challenge)

The first exercise builds [(8.21)](#eq-8-21) directly on a lattice of van der Waals type. You identify the flat band of the Kondo sites and the anti-crossing with the conduction band, and you check what happens to the gap when you change the chemical potential. The second exercise adds a direct exchange coupling between the Kondo sites, which gives a dispersion to the spinon band that would otherwise be flat. This is the lattice version of the Doniach picture. The Kondo coupling $J_K$ favors a local screened singlet, while the direct exchange $J$ favors magnetic correlations between the local moments. The competition between them decides which regime is stable, the screened one or the magnetic one.
:::

::: quiz
In [(8.21)](#eq-8-21) we have one $f$ fermion per site and a half-filled conduction band. How many particles per $\mathbf k$ point and spin fill the two bands?

- [ ] One half, so the lower band is half full.

    This is false. This counts only the conduction band. The $f$ level adds another one half, and the sum is one, which fills the lower band.

- [x] One, so the lower hybridized band is full.

    This is true. The conduction band gives one half and the $f$ level gives one half, so there is one particle for the two states at each $\mathbf k$ and spin. The lower band is full, and the Fermi level lies in the gap.

- [ ] Two, so both bands are full.

    This is false. Two particles per $\mathbf k$ and spin would need a full conduction band, with two electrons per site, and two $f$ fermions per site. The constraint allows one $f$ fermion and we have one electron per site.
:::

::: quiz
At the crossing the energy of the conduction band is zero, as for the flat band. If we double $\gamma_K$, what happens to the direct gap there?

- [ ] It does not change.

    This is false. At the crossing the eigenvalues are $\pm\gamma_K$. For $\gamma_K=0.5$ the gap is $1$, and for $\gamma_K=1$ it is $2$.

- [ ] It becomes four times larger.

    This is false. The gap $2\gamma_K$ is linear in $\gamma_K$. Going from $\gamma_K=0.5$ to $1$ the gap goes from $1$ to $2$ and not to $4$.

- [x] It doubles, since the two levels split into $\pm\gamma_K$.

    This is true. At $\varepsilon_{\mathbf k}=0$ the two-by-two Hamiltonian has the eigenvalues $\pm\gamma_K$, so the direct gap is $2\gamma_K$. This is the sense in which a larger Kondo coupling gives a larger gap.

    ![The two bands of [(8.21)](#eq-8-21) for $\gamma_K=0.5$ and $\gamma_K=1$ with $t=1$. The direct gap at the crossing, the arrow, is $2\gamma_K$, so it doubles.](figures/web/session08/hybrid_gap.svg){alt="Two panels of a cosine band and a flat band repelled by a hybridization, with an arrow at the crossing that is twice as long for the larger hybridization."}

:::

::: {.tryit notebook="session8.ipynb" cell="Spinon dispersion in the Kondo lattice"}
Increase the exchange `J` between the Kondo sites in the three panels. The flat band of the local moments should acquire a dispersion, and the gap should become smaller. Then increase `JK` and check that the gapped regime is more stable.
:::

::: {.widget name="kondobands"}
Move the hybridization $\gamma_K$ of [(8.21)](#eq-8-21) for a one-dimensional chain, per spin. The conduction band is $-2t\cos k$ and the $f$ level is flat at zero energy. At $\gamma_K=0$ the two bands cross at the Fermi level, and the system is a metal. For $\gamma_K>0$ the bands repel, the lower band is full, and for small $\gamma_K$ the indirect gap grows roughly as $\gamma_K^2/t$.
:::

::: comesback
- In Section [9.3](#sec-9-3) the Kondo temperature is a non-perturbative function of the Kondo coupling, which is the strongly non-linear dependence of this page.
- In Section [9.9](#sec-9-9) the Abrikosov-fermion construction is used again, for the screening of one magnetic impurity in a quantum magnet.
:::
