## Topological quantum computing with Majoranas {#sec-5-19 number="5.19"}

Majorana modes get so much attention, beyond their own unusual properties, because of their proposed use in fault-tolerant quantum computing. Majoranas are **non-Abelian anyons**. Exchanging, or braiding, one Majorana around another does not only multiply the many-body ground state by a phase. It acts as a unitary matrix on a degenerate ground-state manifold, so the *order* in which different braiding operations are done matters. This means that the algebra does not commute, and this is what is called non-Abelian. This follows directly from the structure of the BdG Hamiltonian when more than two Majoranas are present.

For concreteness, four Majorana operators $\gamma_1,\gamma_2,\gamma_3,\gamma_4$ can be combined again, with pairings of the type of [(5.18)](#eq-5-18), into two ordinary fermionic operators, which we can call artificial fermions. So a system with four Majoranas encodes two ordinary fermionic modes. The resulting many-body ground-state manifold, with the states empty, one mode filled, the other mode filled and both filled, is four-fold degenerate. All four states cost zero energy, by the same argument that made $\gamma_1$ and $\gamma_{2N}$ zero-energy modes in the Kitaev chain, and this degenerate manifold is the proposed computational basis for a topological qubit.

![Four Majoranas make two ordinary fermion modes. The four states of the two modes sit at $E=0$, and the total fermion parity splits them into two even and two odd states. A braid of two Majoranas keeps the parity.](figures/web/session05/four_majoranas.svg){#sch:s05:four_majoranas alt="Four circles for the Majoranas grouped in two pairs on the left, and four short lines at zero energy on the right, two colored for even parity and two for odd parity."}

::: quiz
Four Majoranas form two ordinary fermion modes. With the total fermion parity fixed to even, how many ground states are available?

- [ ] One.

    This is false. A single ground state would give no qubit. With four Majoranas, $|00\rangle$ and $|11\rangle$ have even parity and the same zero energy, so there are two states.

- [x] Two.

    This is true. Two modes give $2\times2=4$ states, all at zero energy. Only $|00\rangle$ and $|11\rangle$ have even parity, so two states remain for a fixed parity.

- [ ] Four.

    This is false. The four states include $|01\rangle$ and $|10\rangle$ with odd parity. A move from $|00\rangle$ to $|01\rangle$ changes $N$ by one, which no term of a superconductor does, so these are not reached.
:::

Braiding two Majoranas, for example $\gamma_1$ around $\gamma_2$, acts on the ground-state manifold as a unitary

$$U_{12} = \exp\left(\frac{\pi}{4}\,\gamma_1\gamma_2\right), \tag{5.23}$$

which multiplies states by a relative phase built from $e^{i\pi/4}$ times the Majorana product. The exact form is less important than what it implies. Two exchanges that share a Majorana do not commute. Braiding the pair $(1,2)$ and then the pair $(2,3)$ gives a different final state than braiding $(2,3)$ first and $(1,2)$ second, since $\gamma_1\gamma_2$ and $\gamma_2\gamma_3$ anticommute. Exchanges of disjoint pairs, such as $(1,2)$ and $(3,4)$, commute instead. This braid algebra that does not commute is what allows sequences of purely topological and geometric moves, which physically means moving Majoranas around one another, to implement non-trivial quantum logic gates. The resulting qubit is stored non-locally, divided between spatially separated Majoranas instead of being in one local degree of freedom. For this reason it is intrinsically resistant to local decoherence and to weak local disorder, and this robustness is the main reason for the interest in topological quantum computing. No section of `session5.ipynb` implements braiding dynamics or a qubit manifold, since braiding is a dynamical calculation and not a static tight-binding diagonalization.

Schematic [](#sch:s05:braid_order) draws the three cases as worldlines, with time going up. The two exchanges that share a Majorana give two different arrangements, and the two disjoint exchanges give the same one.

![Exchanges of Majoranas as worldlines. (a) The exchange of $(1,2)$ followed by $(2,3)$. (b) The same exchanges in the opposite order, which ends in a different arrangement. (c) The exchange of $(1,2)$ and $(3,4)$, which gives the same result in either order. The operators $i\gamma_1\gamma_2$ and $i\gamma_2\gamma_3$ anticommute, and $i\gamma_1\gamma_2$ and $i\gamma_3\gamma_4$ commute, as we checked on four Majoranas of two fermion modes.](figures/web/session05/braid_order.svg){#sch:s05:braid_order alt="Three braid diagrams with worldlines that cross. The first two use the same two exchanges in opposite order and end in different arrangements. The third uses two exchanges of disjoint pairs."}

::: quiz
Which two braiding operations give the same final state in either order?

- [ ] The exchange of Majoranas $(1,2)$ and the exchange of $(2,3)$.

    This is false. The braid $(1,2)$ is generated by $i\gamma_1\gamma_2$ and $(2,3)$ by $i\gamma_2\gamma_3$. These generators anticommute, like $\sigma_z$ and $\sigma_x$, so the two braids do not commute and the order changes the final state.

- [x] The exchange of $(1,2)$ and the exchange of $(3,4)$.

    This is true. The braids of $(1,2)$ and $(3,4)$ share no Majorana, so $\gamma_1\gamma_2$ and $\gamma_3\gamma_4$ commute and the order does not matter.

- [ ] The exchange of $(2,3)$ and the exchange of $(3,4)$.

    This is false. These two share the Majorana $\gamma_3$, so $\gamma_2\gamma_3$ and $\gamma_3\gamma_4$ anticommute. In the even sector $i\gamma_3\gamma_4$ acts like $\sigma_z$ and $i\gamma_2\gamma_3$ like $\sigma_x$, which do not commute.
:::

::: comesback
- In Session 6 we go to the other branch of the Hubbard model, $U>0$, which gives magnetism, starting from Section [6.3](#sec-6-3).
- In Section [8.10](#sec-8-10) a quantum spin liquid has its own topological excitations, the visons, which are fluxes of an emergent gauge field.
- In Section [10.6b](#sec-10-6b) a phase that no local quantity can tell apart, as for the states of a topological qubit, is the hard case of phase classification.
:::
