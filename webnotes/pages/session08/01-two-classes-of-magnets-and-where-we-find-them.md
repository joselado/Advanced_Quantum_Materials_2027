## Two classes of magnets and where we find them {#sec-8-1 number="8.1"}

In this session, we put every magnetic material into one of two classes, as in Section [6.1](#sec-6-1). **Classical magnets** break time-reversal symmetry, and examples are conventional ferromagnets, antiferromagnets and spin spirals. For the electrons, these magnets can be described with mean-field theory, in the same way as we did in Section [1.14](#sec-1-14) and Section [6.4](#sec-6-4). Most magnetic materials in nature are of this type, for example iron, copper oxide, or any material with a well-defined Néel temperature.

**Quantum magnets** are the opposite case. They cannot be described with mean-field theory in terms of electrons, and their ground states have long-range entanglement. This entanglement is not a small detail, since it gives rise to excitations that do not exist in a symmetry-broken magnet. In this session we will study two physical realizations of quantum magnetism, which are quite different from each other.

- **Quantum spin liquids (QSLs)**, which are the first class that we build in detail. The main candidate material is herbertsmithite, a compound where the magnetic ions form a kagome lattice of spin-$1/2$ sites.

- **Heavy-fermion Kondo insulators**, which are often rare-earth compounds, and the standard example is samarium hexaboride (SmB$_6$). We build the theory for this class in the second half of the session.

## Two emergent excitations, magnons and spinons {#sec-8-2 number="8.2"}

The strong many-body interactions between electrons are the origin of the emergent collective excitations of magnetic materials. In a symmetry-broken magnet, this collective excitation is the **magnon** of Section [6.13](#sec-6-13), which has spin $1$ and no charge. The reason is that the strong repulsion between electrons freezes the charge degree of freedom completely, so only the spin can fluctuate. In a quantum magnet, the excitation is of a different kind. It is the **spinon**, which has spin $1/2$ and also no charge. It is useful to think of a spinon as the spin half of an electron. If we take this picture one step further, we obtain the standard language of fractionalization for a QSL. In this language the electron splits into a **chargon**, which has the charge, and a **spinon**, which has the spin.

There is a simple argument with pictures that shows why the spin of the two excitations differs by a factor of two. Let us take a ferromagnet, where the ground state has all spins up, $|{\uparrow\uparrow\uparrow\cdots}\rangle$. If we flip one spin to build an excited state, the total spin of the excited state differs from the one of the ground state by $\Delta S = 1$, and this is a local magnon. Let us now take a quantum spin liquid, where the ground state is a collection of singlets everywhere and no spin points in a specific direction. If we build an excited state by leaving one spin without a partner, instead of putting it in a singlet, the difference in total spin is $\Delta S = 1/2$, and in this picture this is a spinon. This picture is too simple on purpose, since a real spinon is more subtle than an unpaired spin. Still, it is the right first intuition for why symmetry-broken magnets and quantum spin liquids have different excitations. Figure [8.1](#fig:s08:magnonspinon) shows the two counting arguments next to each other.

![Why the two kinds of magnet have excitations whose spin differs by a factor of two. (a) In a symmetry-broken magnet every site has a definite spin, shown with arrows. Flipping one costs $\Delta S=1$, and this excitation is the magnon of Session 6. The single flipped spin drawn here, next to the ghost of its old direction, only does the counting of $\Delta S$. The real magnon is the delocalized precession of Figure [6.5](#fig:s06:magnon) and not one flipped site. (b) In a quantum magnet no site has a definite spin at all. The sites are paired into singlets [(8.3)](#eq-8-3), drawn as capsules, so $\langle\mathbf S_i\rangle=0$ everywhere and $S_\text{tot}=0$. When we break one pair, we leave *unpaired* sites, drawn as open balls, and each one of them has $S=1/2$. This is a spinon, which is half a magnon. For this reason spinons are always created in pairs, and Figure [8.3](#fig:s08:vbsrvb) shows whether the pair stays bound or separates.](figures/s08f01_magnon_spinon.svg){#fig:s08:magnonspinon number="8.1"}

::: quiz
A quantum spin liquid has an even number of spin-1/2 sites, and its ground state has $S_\text{tot}=0$. Can the lowest excited state contain a single spinon?

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

::: comesback
- In Section [8.8](#sec-8-8) the spinon is written in a formal way as an Abrikosov fermion, with spin $1/2$ and no charge.
- In Section [8.13](#sec-8-13) the second class, the Kondo insulator SmB$_6$, comes from a gap that a hybridization opens.
- In Section [9.9](#sec-9-9) spinons screen a magnetic impurity in a quantum magnet.
:::
