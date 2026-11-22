## Two classes of magnets and where we find them {#sec-8-1 number="8.1"}

Which magnets does mean-field theory miss, and what are their excitations? We will now see that magnets fall into two classes, classical magnets that break time-reversal symmetry and quantum magnets that do not. The excitation of an ordered magnet is the magnon, with spin $1$, and the excitation of a quantum spin liquid is the spinon, with spin $1/2$.

In this session, we put every magnetic material into one of two classes, as in Section [6.1](#sec-6-1). **Classical magnets** break time-reversal symmetry, and examples are conventional ferromagnets, antiferromagnets and spin spirals. For the electrons, these magnets can be described with mean-field theory, in the same way as we did in Section [1.14](#sec-1-14) and Section [6.4](#sec-6-4). Most magnetic materials in nature are of this type, for example iron, copper oxide, or any material with a well-defined Néel temperature.

**Quantum magnets** are the opposite case. They cannot be described with mean-field theory in terms of electrons, and their ground states are entangled. This entanglement is not a small detail, since it gives rise to excitations that do not exist in a symmetry-broken magnet. In this session we will study two physical realizations of quantum magnetism, which are quite different from each other.

- **Quantum spin liquids (QSLs)**, which are the first class that we build in detail. The main candidate material is herbertsmithite, a compound where the magnetic ions form a kagome lattice of spin-$1/2$ sites.

- **Heavy-fermion Kondo insulators**, which are often rare-earth compounds, and the standard example is samarium hexaboride (SmB$_6$). We build the theory for this class in the second half of the session.

## Two emergent excitations, magnons and spinons {#sec-8-2 number="8.2"}

The strong many-body interactions between electrons are the origin of the emergent collective excitations of magnetic materials. In a symmetry-broken magnet, this collective excitation is the **magnon** of Section [6.13](#sec-6-13), which has spin $1$ and no charge. The reason is that the strong repulsion between electrons freezes the charge degree of freedom completely, so only the spin can fluctuate. In a quantum magnet, the excitation is of a different kind. It is the **spinon**, which has spin $1/2$ and also no charge. It is useful to think of a spinon as the spin half of an electron. If we take this picture one step further, we obtain the standard language of fractionalization for a QSL. In this language the electron splits into a **chargon**, which has the charge, and a **spinon**, which has the spin.

There is a simple argument with pictures that shows why the spin of the two excitations differs by a factor of two. Let us take a ferromagnet, where the ground state has all spins up, $|{\uparrow\uparrow\uparrow\cdots}\rangle$. If we flip one spin to build an excited state, $S^z_\text{tot}$ of the excited state differs from the one of the ground state by one. When this flip is spread over the lattice with a nonzero momentum, the total spin also differs by $\Delta S = 1$, and this is a magnon.

Let us now take a quantum spin liquid, where the ground state is a collection of singlets everywhere and no spin points in a specific direction. If we build an excited state by leaving one spin without a partner, instead of putting it in a singlet, the difference in total spin is $\Delta S = 1/2$, and in this picture this is a spinon. This picture is too simple on purpose, since a real spinon is more subtle than an unpaired spin. Still, it is the right first intuition for why symmetry-broken magnets and quantum spin liquids have different excitations. Figure [8.1](#fig:s08:magnonspinon) shows the two counting arguments next to each other.

::: key
In a ferromagnet, flipping one spin changes $S^z_\text{tot}$ by one. The magnon is this flip spread over the lattice with a nonzero momentum, and its total spin is one less than the one of the ground state. Leaving one site of a singlet covering without a partner changes the total spin by one half, and this is the spinon,

$$\Delta S_\text{magnon}=1,\qquad \Delta S_\text{spinon}=\tfrac12.$$

With an even number of sites the total spin is an integer, so spinons come in pairs.
:::

![Why the two kinds of magnet have excitations whose spin differs by a factor of two. (a) In a symmetry-broken magnet every site has a definite spin, shown with arrows. Flipping one lowers $S^z_\text{tot}$ by one, and the magnon of Session 6 built from this flip has $\Delta S=1$. The single flipped spin drawn here, next to the ghost of its old direction, only does this counting. The real magnon is the delocalized precession of Figure [6.5](#fig:s06:magnon) and not one flipped site. (b) In a quantum magnet no site has a definite spin at all. The sites are paired into singlets [(8.3)](#eq-8-3), drawn as capsules, so $\langle\mathbf S_i\rangle=0$ everywhere and $S_\text{tot}=0$. When we break one pair, we leave *unpaired* sites, drawn as open balls, and each one of them has $S=1/2$. This is a spinon, which is half a magnon. For this reason spinons are always created in pairs, and Figure [8.3](#fig:s08:vbsrvb) shows whether the pair stays bound or separates.](figures/s08f01_magnon_spinon.svg){#fig:s08:magnonspinon number="8.1"}

::: lab
The spin-1/2 Heisenberg antiferromagnetic chain is one of the simplest quantum many-body systems, and its exact ground state is a singlet of all the spins of the chain. Its elementary excitations are spinons, fractional spin-1/2 quasiparticles that neutron scattering creates and detects in pairs. With inelastic neutron scattering on a compound that realizes this chain, and an absolute normalization of the data, the measurement accounts for the full spectral weight to within $99(8)\%$. Theory predicts that the states of two spinons hold only $71\%$ of this weight, so the rest comes from states with more spinons. The measurement is in [this article](https://www.nature.com/articles/nphys2652).

In our reading, this is the counting of this page seen in a measurement. The neutron couples to one spin operator, so from the singlet ground state it reaches states with $S_\text{tot}=1$, which two spinons can form and one spinon cannot. The two spinons share the energy and the momentum of the neutron in many ways, which gives a broad continuum and not the sharp line of a single magnon.
:::

::: quiz
A quantum spin liquid has an even number of spin-1/2 sites. Its ground state has $S_\text{tot}=0$. Can the lowest excited state contain a single spinon?

- [x] No, since one spinon would give a total spin of $1/2$, which an even number of spin-1/2 sites cannot have.

    This is true. The total spin of an even number of spin-1/2 particles is an integer. A spinon with $S=1/2$ must then come together with a second one, and this is why spinons are created in pairs.

- [ ] Yes, since the spinon has spin $1/2$ and the ground state has spin $0$.

    This is false. Take four spin-1/2 sites. The total spin can be $0$, $1$ or $2$ and never $1/2$, so the state with one spinon does not exist.

    ![The total spins that $N$ spin-$1/2$ sites can have, with the number of times each one appears, checked against $\mathbf S^2$ for $N\le7$. Even $N$ gives an integer spin and odd $N$ gives a half-integer spin.](figures/web/session08/total_spin_ladder.svg){alt="Dots for the allowed total spin of two to seven spins one half, whole numbers for even numbers of sites and half numbers for odd ones, each with its multiplicity."}

- [ ] Yes, but only if a magnetic field is applied.

    This is false. A field changes the energies but not the possible values of the total spin. With four sites in a field, $S^z_\text{tot}$ is still an integer, from $-2$ to $2$.
:::

::: quiz
A magnon has spin $1$. What does this tell us about its relation to spinons?

- [ ] A magnon is a single spinon with spin $1$.

    This is false. A spinon has spin $1/2$, since it is created by a single $f^\dagger_\alpha$ that changes $S^z$ by $1/2$. A single spinon cannot have spin $1$.

- [x] Two spinons with parallel spins carry the same spin, so a magnon is like a bound pair of spinons.

    This is true. Two spin-1/2 excitations can add up to spin $1$, as in the triplet of the dimer. The magnon of a symmetry-broken magnet is then the bound version of what a quantum spin liquid can split into two free parts.

- [ ] A magnon has no relation to spinons, since spinons carry no spin.

    This is false. In the parton construction $\mathbf S_i=\tfrac12 f^\dagger\boldsymbol\sigma f$, so each $f$ fermion carries spin $1/2$. Spinons are neutral but they are not spinless.
:::

::: quiz
Each chain has six spin-1/2 sites. A capsule is a singlet with $S=0$, and an arrow is a free spin. Which state has $S_\text{tot}=1$?

- [ ] ![A chain of six sites paired into three capsules, with no free spin.](figures/web/session08/g1_quiz_spins_paired.svg)

    This is false. Every site is in a singlet, and each singlet has $S=0$, so the total spin is $0$. This state has no spinon.

- [x] ![A chain of six sites with two capsules in the middle and a free spin pointing up at each end.](figures/web/session08/g1_quiz_spins_two.svg)

    This is true. The two singlets have $S=0$. The two free spins both point up, so they are in the triplet state $|{\uparrow\uparrow}\rangle$ with $S=1$, and the whole chain has $S_\text{tot}=1$. These are two spinons, which together have the spin of one magnon.

- [ ] ![A chain of six arrows, five pointing up and the third one pointing down.](figures/web/session08/g1_quiz_spins_flip.svg)

    This is false. Five spins up and one spin down give $S^z_\text{tot}=2$, and the total spin is never smaller than $|S^z_\text{tot}|$, so it is at least $2$. When the flip is spread over the chain with a nonzero momentum, it is the magnon of a ferromagnet, with $S_\text{tot}=2$, one less than the $S_\text{tot}=3$ of the state with all spins up.
:::

:::: problem
Three spin-1/2 sites have $2^3=8$ states. Find the possible values of their total spin $S$, and how many times each value appears. Then show that an even number of spin-1/2 sites always has an integer total spin.

::: solution
We add the spins one at a time. Two spins one half give $S=0$ once and $S=1$ once, the singlet and the triplet, with $1+3=4$ states. A third spin one half added to $S=0$ gives $S=1/2$. Added to $S=1$ it gives $S=1/2$ or $S=3/2$, since the total spin goes from $|1-\tfrac12|$ to $1+\tfrac12$ in steps of one. So three sites have $S=1/2$ twice and $S=3/2$ once. A value $S$ has $2S+1$ states, so we count $2\cdot2+4=8$, which is all the states.

Each new spin one half changes the total spin by $\pm\tfrac12$. One site has $S=1/2$, two sites have an integer $S$, three sites have a half-integer $S$ again, and so on. So an even number of sites always has an integer total spin.

This is why a chain with an even number of sites has no state with a single spinon, since its total spin would be a half-integer. In a measurement the spinons appear in pairs, as in the neutron scattering of the lab box of this page.
:::
::::

::: comesback
- In Section [8.8](#sec-8-8) the spinon is written in a formal way as an Abrikosov fermion, with spin $1/2$ and no charge.
- In Section [8.13](#sec-8-13) the second class, the Kondo insulator SmB$_6$, comes from a gap that a hybridization opens.
- In Section [9.9](#sec-9-9) spinons screen a magnetic impurity in a quantum magnet.
:::
