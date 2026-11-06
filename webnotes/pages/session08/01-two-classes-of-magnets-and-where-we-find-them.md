## Two classes of magnets and where we find them {#sec-8-1 number="8.1"}

In the language of this lecture, every magnetic material belongs to one of two classes. **Classical magnets** break time-reversal symmetry, and examples are conventional ferromagnets, antiferromagnets and spin spirals. For the electrons, these magnets can be described with mean-field theory, in the same way as we did in Sessions 1 and 6. Most magnetic materials in nature are of this type, for example iron, copper oxide, or any material with a well-defined Néel temperature.

**Quantum magnets** are the opposite case. They cannot be described with mean-field theory in terms of electrons, and their ground states have long-range entanglement. This entanglement is not a small detail, since it gives rise to excitations that do not exist in a symmetry-broken magnet. In this session we will study two physical realizations of quantum magnetism, which are quite different from each other.

- **Quantum spin liquids (QSLs)**, which are the first class that we build in detail. The best-known candidate material is herbertsmithite, a compound where the magnetic ions form a kagome lattice of spin-$1/2$ sites.

- **Heavy-fermion Kondo insulators**, which are often rare-earth compounds, and the standard example is samarium hexaboride (SmB$_6$). We build the theory for this class in the second half of the session.

## Two emergent excitations, magnons and spinons {#sec-8-2 number="8.2"}

The strong many-body interactions between electrons are the origin of the emergent collective excitations of magnetic materials. In a symmetry-broken magnet, this collective excitation is the **magnon**, which has spin $1$ and no charge. The reason is that the strong repulsion between electrons freezes the charge degree of freedom completely, so only the spin can fluctuate. In a quantum magnet, the excitation is of a different kind. It is the **spinon**, which has spin $1/2$ and also no charge. It is useful to think of a spinon as the spin half of an electron. If we take this picture one step further, we obtain the standard language of fractionalization for a QSL, where the electron splits into a **chargon**, which has the charge, and a **spinon**, which has the spin.

There is a simple argument with pictures that shows why the spin of the two excitations differs by exactly a factor of two. Let us take a ferromagnet, where the ground state has all spins up, $|{\uparrow\uparrow\uparrow\cdots}\rangle$. If we flip one spin to build an excited state, the total spin of the excited state differs from the one of the ground state by $\Delta S = 1$, and this is a local magnon. Let us now take a quantum spin liquid, where the ground state is a collection of singlets everywhere and no spin points in a specific direction. If we build an excited state by leaving one spin without a partner, instead of putting it in a singlet, the difference in total spin is $\Delta S = 1/2$, and in this picture this is a spinon. This picture is too simple on purpose, since real spinons are more subtle than "an unpaired spin," but it is the right first intuition for why symmetry-broken magnets and quantum spin liquids have fundamentally different excitations. Figure [8.1](#fig:s08:magnonspinon) shows the two counting arguments next to each other.

![Why the two kinds of magnet have excitations whose spin differs by exactly a factor of two. (a) In a symmetry-broken magnet every site has a definite spin, shown with arrows. Flipping one costs $\Delta S=1$, and this excitation is the magnon of session 6. The single flipped spin drawn here, next to the ghost of its old direction, only does the counting of $\Delta S$, since the real magnon is the delocalized precession of figure [6.5](#fig:s06:magnon) and not one flipped site. (b) In a quantum magnet no site has a definite spin at all. The sites are paired into singlets [(8.3)](#eq-8-3), drawn as capsules, so $\langle\mathbf S_i\rangle=0$ everywhere and $S_\text{tot}=0$. When we break one pair, we leave *unpaired* sites, drawn as open balls, and each one of them has $S=1/2$. This is a spinon, which is half a magnon. For this reason spinons are always created in pairs, and figure [8.3](#fig:s08:vbsrvb) shows whether the pair stays bound or separates.](figures/s08f01_magnon_spinon.svg){#fig:s08:magnonspinon number="8.1"}

::: quiz
A quantum spin liquid has an even number of spin-1/2 sites, and its ground state has $S_\text{tot}=0$. Can the lowest excited state contain a single spinon?

- [x] No, since one spinon would give a total spin of $1/2$, which an even number of spin-1/2 sites cannot have.
- [ ] Yes, since the spinon has spin $1/2$ and the ground state has spin $0$.
- [ ] Yes, but only if a magnetic field is applied.
- [ ] No, since spinons carry charge.

The total spin of an even number of spin-1/2 particles is an integer. A spinon with $S=1/2$ must then come together with a second one, and this is why spinons are created in pairs.
:::

::: quiz
A magnon has spin $1$. What does this tell us about its relation to spinons?

- [ ] A magnon is a single spinon with spin $1$.
- [ ] Four spinons are needed, since each carries a quarter of the spin.
- [x] Two spinons with parallel spins carry the same spin, so a magnon is like a bound pair of spinons.
- [ ] A magnon has no relation to spinons, since spinons carry no spin.

Two spin-1/2 excitations can add up to spin $1$. The magnon of a symmetry-broken magnet is then the bound version of what a quantum spin liquid can split into two free parts.
:::
