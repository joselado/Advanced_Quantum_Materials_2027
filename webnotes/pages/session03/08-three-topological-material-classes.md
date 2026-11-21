## Three topological material classes {#sec-3-8 number="3.8"}

Which kinds of topological matter are there, and what makes them different from each other? We will now see three classes. All of them have a gap in the bulk and gapless states at the boundary, and they differ in the symmetry that they keep and in the kind of state that the boundary has.

With the general tools in place, let us name three classes of topological matter, before we build explicit models for two of them.

- **Chern insulators.** They have a bulk Chern number $C \neq 0$ and chiral edge states, and time-reversal symmetry is necessarily broken, since we will see in Section [3.10](#sec-3-10) that time-reversal symmetry forces $\sigma_{xy}=0$. Without a backscattering channel there are no electrical losses at the edge, which makes them an attractive platform for dissipationless electronics.

- **Quantum spin Hall insulators.** They are two copies of a Chern insulator, one for each spin, with opposite Chern numbers, so the net Chern number vanishes and time-reversal symmetry is preserved. However, the edge states are **helical**, meaning that spin-up and spin-down propagate in opposite directions along the same edge. This is the natural platform for dissipationless spin transport, which is spintronics.

- **Topological superconductors.** They combine a bulk superconducting gap with gapless surface excitations that are their own antiparticle, which are called Majorana excitations. Since the corresponding quantum information is stored non-locally, the usual local decoherence channels do not act on it directly, and this is the basis of topological quantum computing. We will build the minimal model for this case, the Kitaev chain, in Section [5.16](#sec-5-16). There we will see that, written with Majorana operators, it has the same form as the chain that we construct next.

![The edge dispersions of the first two classes, from Section [3.11](#sec-3-11). In (a) a Chern insulator has one chiral branch per edge. In (b) a quantum spin Hall insulator has a helical pair, with the two branches propagating in opposite directions. Look at the colors, which are the two spins.](figures/s03f06_helical.svg){alt="Edge branches inside the bulk gap, one branch for a Chern insulator and two opposite branches for a quantum spin Hall insulator."}

::: quiz
An insulator has time-reversal symmetry and a total Chern number of zero. At each edge the two spins move in opposite directions. Which class is it?

- [x] A quantum spin Hall insulator.

    This is true. It is made of two copies of a Chern insulator with opposite Chern numbers. The total Chern number vanishes, and the edge states of the two spins form a helical pair.

- [ ] A Chern insulator.

    This is false. A Chern insulator with $C=1$ has one chiral mode at each edge and $\sigma_{xy}=e^2/h$, and it needs broken time-reversal symmetry. Its total Chern number is not zero.

- [ ] A trivial insulator.

    This is false. A trivial insulator has $C=0$ and time-reversal symmetry, but no state crosses its gap. A ribbon of the honeycomb lattice with a staggered potential of $0.5\,t$ has no level between $-0.5\,t$ and $0.5\,t$, so it has no edge state that could move in any direction.

:::

::: quiz
The Hall conductivity of a system with two spin sectors is

$$\sigma_{xy} = \frac{e^2}{h}\,\big(C_\uparrow + C_\downarrow\big),$$

with $C_\uparrow$ and $C_\downarrow$ the Chern numbers of the two spins. A quantum spin Hall insulator has $C_\uparrow=1$ and $C_\downarrow=-1$. What is its Hall conductivity?

- [ ] $\sigma_{xy}=2e^2/h$

    This is false. This is the value for $C_\uparrow=C_\downarrow=1$, which is two copies with the same sign. That system breaks time-reversal symmetry, and it is a Chern insulator with $C=2$.

- [x] $\sigma_{xy}=0$

    This is true. The two spins give opposite Hall currents, so no net charge flows across the sample. Spin up and spin down still move to opposite sides, which is a spin current, and each edge keeps its pair of states.

- [ ] $\sigma_{xy}=e^2/h$

    This is false. This counts only one of the two spins. We would get it for $C_\uparrow=1$ and $C_\downarrow=0$, and then the two spins are not related by time reversal.

:::

## The SSH model as a minimal one-dimensional topological insulator {#sec-3-9 number="3.9a"}

What is the simplest model of a topological insulator that we can solve on paper? We will now see that it is a chain with two alternating hoppings. In this first part we take the limit in which the chain is a set of separate dimers. It has a gap and no state at zero energy, and it will be our reference for a trivial insulator.

::: {.recall eq="2.13"}
This is the chain with two orbitals per cell of Section [2.7](#sec-2-7), with its Bloch Hamiltonian and its two bands, where $\varphi$ is the phase between neighboring cells. There the intracell hopping is $1$ and the intercell hopping is $\eta$. In this section the intracell hopping is $t$ and the intercell hopping is $1$, which is the same chain with $\eta=1/t$, $\varphi=-k$ and all the energies multiplied by $t$.
:::

We now build the simplest model that shows this physics explicitly, which is the Su-Schrieffer-Heeger (SSH) chain. We already met it as the two-orbital chain of [(2.13)](#eq-2-13) in Section [2.7](#sec-2-7). It looks too simple to be useful, but we should take it seriously. One reason is that the simplest model for a topological superconductor, the Kitaev chain, has the form of this model when we write it with Majorana operators.

We take a one-dimensional lattice with two sites per unit cell, $A$ and $B$, and two hopping amplitudes. The first one is an intracell hopping $t$, within a unit cell, and the second one is an intercell hopping fixed to $1$, between neighboring unit cells.

Let us first take the extreme limit in which the intracell hopping dominates, $t \gg 1$, so that the chain is fully dimerized with alternating bonds. Strong bonds of strength $t$ couple the sites $(0,1)$, $(2,3)$, $(4,5)$, ..., and the coupling between $(1,2)$, $(3,4)$, ... is negligible. Each dimer is then an isolated two-level system with bonding and antibonding eigenstates at energies $\pm t$. The spectrum of the whole chain is this pair of levels repeated once for each dimer, and there is nothing at zero energy.

::: key
In the limit $t\gg1$ the chain is a set of separate dimers, and each dimer has the two levels

$$E_\pm = \pm t .$$

A chain of $N$ dimers has $N$ levels at $+t$ and $N$ levels at $-t$. The gap is $2t$ and no state is at zero energy, since no site is left without a partner, also at the two ends.
:::

::: {.steps title="From one dimer to the levels of the dimerized chain"}
The first step is one dimer. In the basis of its two sites $A$ and $B$ the Hamiltonian is a matrix with the hopping $t$ off the diagonal,

$$H_{\text{dimer}} = \begin{pmatrix} 0 & t \\ t & 0 \end{pmatrix}, \qquad
H_{\text{dimer}}\,\frac{1}{\sqrt2}\begin{pmatrix} 1 \\ \pm1 \end{pmatrix} = \pm t\,\frac{1}{\sqrt2}\begin{pmatrix} 1 \\ \pm1 \end{pmatrix}.$$

So the eigenstates are the sum and the difference of the two sites, which are the bonding and the antibonding combination. The hopping enters this matrix with a positive sign, so the sum has the energy $+t$ and the difference has the energy $-t$. With a hopping $-t$ the two energies would be exchanged, and nothing else would change.

The second step is the chain of $N$ dimers with no hopping between them. Its Hamiltonian is made of $N$ blocks $H_{\text{dimer}}$ on the diagonal, and the eigenvalues of such a matrix are the eigenvalues of its blocks. So there are $N$ levels at $+t$ and $N$ levels at $-t$.

The third step is to put back the intercell hopping $1$, which is small compared with $t$. We call $|s_n\rangle=(|A_n\rangle+|B_n\rangle)/\sqrt2$ the state with the energy $+t$ on the dimer $n$. The intercell hopping joins the site $B_n$ with the site $A_{n+1}$, and each of them has the amplitude $1/\sqrt2$, so

$$\langle s_n|H|s_{n+1}\rangle = \frac{1}{\sqrt2}\cdot 1\cdot\frac{1}{\sqrt2} = \frac12 .$$

The states $|s_n\rangle$ form a chain of their own, with the onsite energy $t$ and the hopping $1/2$. The same happens for the states at $-t$, with the hopping $-1/2$. A chain with one orbital per cell has a cosine band, as in [(2.8)](#eq-2-8), so each group of levels becomes a band,

$$E_\pm(k) \simeq \pm\,(t+\cos k),$$

of width $2$ around $\pm t$. Here we do not include the coupling between the two groups, which changes the energies by terms of order $1/t$. For $t=4$ and eight sites the upper levels are $3.22$, $3.76$, $4.37$ and $4.83$, which are inside the band from $3$ to $5$. The two groups stay far from zero energy, so the weak hopping does not change the conclusion.
:::

::: quiz
A dimer of two sites with the hopping $t$ has the Hamiltonian

$$H_{\text{dimer}} = \begin{pmatrix} 0 & t \\ t & 0 \end{pmatrix}.$$

A chain has four such dimers and no hopping between them. How many levels are at the energy $+t$ and how many are at zero energy?

- [ ] Eight at $+t$ and none at zero energy.

    This is false. Each dimer is the matrix with $t$ off the diagonal and gives $\pm t$. The trace of the Hamiltonian is zero, but eight levels at $+t$ would give $8t$.

- [x] Four at $+t$ and none at zero energy.

    This is true. Each dimer has one level at $+t$, which is the sum of its two sites, and one level at $-t$, which is their difference. Four dimers give four levels at each energy, and no site is left uncoupled.

    ![The dimerized chain, lower row, with the levels at $\pm t$ and a gap around zero.](figures/s03f03_ssh.svg){alt="Two chains of eight sites with their spectra, one with strong intracell bonds and a gap around zero, and one with strong intercell bonds and two levels at zero energy."}

- [ ] Four at $+t$ and two at zero energy.

    This is false. Each dimer gives one level at $+t$ and one at $-t$, so the number at $+t$ equals the number at $-t$. Four dimers use all eight sites, so with four levels at $+t$ the other four are at $-t$ and none is left at zero.

:::

::: quiz
A chain of dimers has the intracell hopping $t\gg1$. The state $|s_n\rangle=(|A_n\rangle+|B_n\rangle)/\sqrt2$ of the dimer $n$ has the energy $t$. We add a weak hopping $1$ between the site $B_n$ and the site $A_{n+1}$. Which band do the states $|s_n\rangle$ form?

- [ ] $E(k)\simeq t+2\cos k$

    This is false. This band would go from $t-2$ to $t+2$. For $t=4$ and a chain of 40 sites the upper levels go from $3.01$ to $4.99$, and not from $2$ to $6$. The hopping between two dimer states is $1/2$ and not $1$.

- [x] $E(k)\simeq t+\cos k$

    This is true. Each of the two sites that the weak hopping joins has the amplitude $1/\sqrt2$, so the hopping between neighboring dimer states is $1/2$. A chain with the hopping $1/2$ has a band of width $2$.

- [ ] $E(k)=t$

    This is false. A flat level needs zero hopping between the dimers. For $t=4$ and eight sites the four upper levels are $3.22$, $3.76$, $4.37$ and $4.83$, so they are spread around $t$.

:::

:::: problem
We take an open chain of four sites with the bonds $t$, $1$ and $t$, which is two dimers joined by the intercell hopping. Find its four energies for any $t$, with the help of the mirror symmetry of the chain. Then give them for $t\gg1$.

::: solution
The mirror exchanges the sites $1$ and $4$, and the sites $2$ and $3$. It commutes with the Hamiltonian, so the eigenstates are even or odd under it, as in Section [2.4](#sec-2-4). We use the states $|e_\pm\rangle=(|1\rangle\pm|4\rangle)/\sqrt2$ of the two end sites and $|c_\pm\rangle=(|2\rangle\pm|3\rangle)/\sqrt2$ of the two central sites. The bonds $t$ join $|e_\pm\rangle$ with $|c_\pm\rangle$, and the central bond gives $\langle c_\pm|H|c_\pm\rangle=\pm1$. In each sector the Hamiltonian is then a matrix of size two,

$$H_\pm = \begin{pmatrix} 0 & t \\ t & \pm1 \end{pmatrix}.$$

Its eigenvalues are the solutions of $E^2\mp E-t^2=0$, so the even sector and the odd sector give

$$E = \frac{1\pm\sqrt{1+4t^2}}{2} \qquad\text{and}\qquad E = \frac{-1\pm\sqrt{1+4t^2}}{2} .$$

For $t\gg1$ the square root is $2t$ up to terms of order $1/t$, and the four levels are $\pm t\pm\tfrac12$. These are the levels $\pm t$ of the two dimers, split by the hopping $1/2$ between the dimer states. For $t=4$ the exact values are $\pm3.53$ and $\pm4.53$. The level closest to zero is $\tfrac12\big(\sqrt{1+4t^2}-1\big)$, which is about $t-\tfrac12$. So the gap around zero is about $2t-1$, and no level is close to zero energy.

For a measurement it means that the tunneling spectrum of such a chain, which is what STM measures, has no peak at zero bias on any site, also at the two ends. For a calculation it is a check with no free parameter, since the diagonalization of the chain of four sites must give these four numbers. The formula holds for any $t$, and in Section [3.9b](#sec-3-9b) we will see what changes when $t$ is small.
:::
::::

::: {.widget name="sshwinding"}
Move the intracell hopping $t$ of [(3.5)](#eq-3-5), with the intercell hopping equal to one. The left panel shows $d(k)=t+e^{ik}$ in the complex plane, and the right panel shows the levels of an open chain with 20 cells. For $t<1$ the curve encloses the origin, the winding is one, and two levels sit in the gap, one at each end. For $t>1$ the curve does not enclose the origin and the gap is empty. At $t=1$ the curve touches the origin and the gap closes.
:::

::: comesback
- In Section [4.20](#sec-4-20) the Chern insulator at zero field comes back in real materials, Cr-doped (Bi,Sb)$_2$Te$_3$ and twisted graphene on boron nitride.
- In Section [5.16](#sec-5-16) the Kitaev chain, written with Majorana operators, has the form of the SSH chain, and in Section [5.18](#sec-5-18) a topological superconductor is built from a quantum spin Hall insulator.
- In Section [9.8](#sec-9-8) a vacancy binds an in-gap mode in a Chern insulator of the Haldane model and in a chiral p-wave superconductor, but not in a trivial insulator with the same gap.
:::
