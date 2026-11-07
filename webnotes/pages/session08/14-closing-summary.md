## Closing summary {#sec-8-14 number="8.14"}

We started from what we built before. These were the mean-field method of Section [1.12](#sec-1-12), the Heisenberg model [(6.5)](#eq-6-5) from the Hubbard dimer of Section [6.8](#sec-6-8), the magnons and the Holstein-Primakoff transformation of Section [6.14](#sec-6-14), and the singlet [(7.3)](#eq-7-3) of Session 7. In this session we saw the following.

- Magnetism, in all the forms that we saw in Session 1, Session 6 and in this session, comes from strong repulsive interactions between electrons.

- Frustrated magnetic models, such as those on triangular and kagome lattices of Section [8.4](#sec-8-4), can show **quantum spin liquid** behavior. This is a highly entangled ground state with zero local spin expectation value on every site, as already for the singlet [(8.3)](#eq-8-3) and the valence bond solid [(8.5)](#eq-8-5). The RVB state [(8.6)](#eq-8-6) to [(8.7)](#eq-8-7) goes beyond both, because its singlets resonate over every pairing of the frustrated lattice. Conventional mean-field theory cannot describe it by construction.

- The zero magnetization of a QSL is the opposite regime from the one that Holstein-Primakoff needs [(8.9)](#eq-8-9). For this reason, its fundamental excitations are not magnons but **spinons**, with $S=1/2$. These are emergent fermions without charge that we obtain from the Abrikosov or parton construction, [(8.10)](#eq-8-10) to [(8.15)](#eq-8-15). This construction is the mean-field method for electrons of Session 1 and Session 6, now applied to the spin sector. Spinon bands can be gapless, gapped, or of Dirac type, as in Section [8.9](#sec-8-9).

- The parton construction has an emergent gauge redundancy [(8.16)](#eq-8-16). The mean-field bond variable is a link field, and its topological defects are gauge excitations called **visons**, which are in general coupled to the spinons, as in Section [8.10](#sec-8-10).

- Quantum entanglement that mixes spin and fermion degrees of freedom also appears in **Kondo systems**. The same parton method, applied to a lattice of local moments inside a metal, [(8.17)](#eq-8-17) to [(8.21)](#eq-8-21), turns the Kondo exchange coupling into a mean-field **hybridization** $\gamma_K$. This hybridization opens a gap in the conduction band at the anti-crossing and turns a metal into a **Kondo insulator**, also called a heavy-fermion insulator. The gap grows monotonically with the strength of the Kondo coupling, as in Section [8.13](#sec-8-13).

![The central difference of the session. Look at the counting of $\Delta S$ in panel (a) and in panel (b), which is the reason why the excitations of a quantum spin liquid are spinons and not magnons.](figures/s08f01_magnon_spinon.svg){alt="A magnet with one flipped spin, and a pattern of singlets with one broken pair that leaves two unpaired spins."}

::: quiz
Which excitation carries spin $1/2$, no charge, and appears in the parton construction of a quantum spin liquid?

- [x] The spinon.

    This is true. The spinon is the fermion of the parton construction, which carries the spin of the electron. The magnon and the triplon have spin $1$, and the vison is a flux of the gauge field with no spin.

- [ ] The magnon.

    This is false. Flipping one spin of a ferromagnet changes $S^z$ by $1$. Its spin is $1$ and not $1/2$.

- [ ] The vison.

    This is false. The vison is a plaquette with flux $\Phi=-1$ and it is a spin singlet. It carries no spin at all.
:::

::: comesback
- In Section [9.9](#sec-9-9) the Abrikosov fermions and spinons of this session are used again for a single magnetic impurity in a quantum magnet, with the same mathematics as the Friedel oscillations of Section [9.6](#sec-9-6).
- In Section [9.3](#sec-9-3) the Kondo effect is a case where linear response fails, since the Kondo temperature is non-perturbative in the coupling.
- In Section [10.6b](#sec-10-6b) a gauge theory with spins on the links comes back, with the plaquette product as the quantity that a local gauge flip does not change.
:::
