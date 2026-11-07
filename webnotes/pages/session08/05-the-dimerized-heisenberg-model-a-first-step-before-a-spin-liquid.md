## The dimerized Heisenberg model, a first step before a spin liquid {#sec-8-5 number="8.5"}

Before we study a frustrated Hamiltonian, it is useful to build the simplest possible *macroscopic* quantum magnet and to check explicitly that its ground state does what [(8.3)](#eq-8-3) told us. Let us take a **fully dimerized Heisenberg model**, which is made of dimers that are completely decoupled from each other, placed on a chain or on a two-dimensional lattice,

$$H = \sum_n J\, \mathbf S_{2n}\cdot \mathbf S_{2n+1}, \qquad J>0. \tag{8.4}$$

Since every dimer is decoupled from its neighbors, we can write the many-body ground state exactly, as a product of singlets over the pairs of the dimers,

$$|\Psi\rangle \sim \bigotimes_n \Big(|{\uparrow_{2n}\downarrow_{2n+1}}\rangle -
|{\downarrow_{2n}\uparrow_{2n+1}}\rangle\Big), \qquad \langle \mathbf S_i\rangle = 0 \text{ on every
site}. \tag{8.5}$$

On a chain this is the dimerized model of Section [7.6](#sec-7-6), and [(8.5)](#eq-8-5) is the product of singlets [(7.8)](#eq-7-8), whose entanglement entropy does not grow with the subsystem. In one sense this is a trivial Hamiltonian, a collection of independent zero-dimensional problems. But it already shows something important. A macroscopic Heisenberg Hamiltonian *can* have a ground state that does not break time-reversal symmetry, and this state is the direct generalization of the two-site singlet [(8.3)](#eq-8-3) to an extensive system. If we add small couplings between the dimers, the state changes smoothly and it still does not break time-reversal symmetry. In a small chain we can follow this directly, and [](#sch:s08:dimerized_levels) does so for four sites.

![The lowest levels of the open chain of four sites with the bonds $J$, $J'$ and $J$, from exact diagonalization, against $J'/J$. The ground state is a nondegenerate singlet for every $J'$ shown, and the gap to the lowest triplet is $0.97J$ at $J'=0.1J$ and $0.66J$ at $J'=J$. Look at the vertical line at $J'=0.1J$, where the two lowest energies are $-1.501J$ and $-0.527J$. With four sites this is a finite-size result.](figures/web/session08/dimerized_levels.svg){#sch:s08:dimerized_levels alt="The lowest energy levels of a four-site chain against the coupling between the dimers, with a nondegenerate singlet ground state well below a threefold triplet."}

There is, however, an important difference to make here, because this state is *not yet* a quantum spin liquid. Its fundamental excitations still have spin $1$. If we turn one singlet into its triplet partner, we obtain a **triplon**, which is a local transition from singlet to triplet. It has the same structure as a magnon, with only a different name. A state that is built in this way, from a fixed and static pattern of singlets, is called a **valence bond solid (VBS)**. To obtain a real quantum spin liquid, with spin-$1/2$ excitations instead of spin-$1$ triplons, we need more than a static dimer covering. We need the singlets to fluctuate and to resonate over the whole lattice, and this is the frustrated case that we study in the next section. Figure [8.3](#fig:s08:vbsrvb) shows this difference explicitly.

![The frozen dimer covering of this section and its excitation. Look at the left panels (a1) and (a2), where separating the two unpaired spins breaks every singlet between them, so the pair stays bound as a triplon. The right panels show what the next section adds, a superposition of many coverings.](figures/s08f03_vbs_rvb.svg){alt="A valence bond solid with its two unpaired spins confined, and a resonating valence bond state with free spin one-half excitations."}

::: quiz
We turn one singlet of [(8.5)](#eq-8-5) into a triplet. What is the spin of this excitation?

- [ ] $1/2$, so it is a spinon.

    This is false. Both spins stay on the same bond, and two spin-1/2 give $0$ or $1$ and never $1/2$. The state $|{\uparrow\uparrow}\rangle$ on the bond has $S^z=1$.

- [ ] $0$, since the state is still a product of dimers.

    This is false. The product of dimers with one of them in $|{\uparrow\uparrow}\rangle$ has total $S^z=1$, so it is not a singlet. Being a product state does not fix the spin.

- [x] $1$, so it is a triplon and not a spinon.

    This is true. The two spins of the dimer are in a triplet, which has $S=1$. Both spins stay on the same bond, so this excitation has the structure of a magnon.
:::

::: quiz
We add a weak coupling between the dimers of [(8.4)](#eq-8-4). What happens to the ground state?

- [ ] It breaks time-reversal symmetry immediately.

    This is false. For four sites with $J=1$ and $J'=0.1$ between the dimers, the ground state has energy $-1.501$ and it is nondegenerate with $S=0$. The gap of order $J$ forbids a symmetry-broken state.

- [x] It changes smoothly and it still does not break time-reversal symmetry.

    This is true. The singlet-triplet gap protects the state, so a small perturbation changes it only a little. The state remains a valence bond solid until the coupling is of the order of the gap.

- [ ] It becomes degenerate.

    This is false. For four sites with $J=1$ and $J'=0.1$ the lowest energy is $-1.501$ and the next one is $-0.527$. The ground state is unique and the gap is about $0.97$.

    ![The lowest levels of the four-site chain against $J'/J$. The vertical line marks $J'=0.1J$.](figures/web/session08/dimerized_levels.svg){alt="The lowest energy levels of a four-site chain against the coupling between the dimers, with a nondegenerate singlet ground state well below a threefold triplet."}

:::

::: {.tryit notebook="session8.ipynb" cell="Magnetization of a dimerized Heisenberg model with a magnetic impurity"}
Run the dimerized chain with $J=1\pm0.2$ and compare the profile with the uniform chain. The magnetization induced by the local field should decay much faster along the dimerized chain. Change 0.2 to 0.05 and see how the decay length grows when the dimerization is weaker.
:::

::: comesback
- In Section [8.6](#sec-8-6) the singlets stop being frozen and resonate, and the two halves of a broken singlet separate as free spinons.
- In Section [8.9](#sec-8-9) the alternating bonds of this valence bond solid give a gapped band of spinons.
- In Section [9.9](#sec-9-9) a gapped chain, the spin-$1$ one, screens an impurity with an exponential decay, as the dimerized chain of the notebook does.
:::
