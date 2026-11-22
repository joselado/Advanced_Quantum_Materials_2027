## Engineering a topological superconductor from a quantum spin Hall insulator {#sec-5-18 number="5.18"}

Chiral and p-wave superconductors of the kind we need are rare in nature, so in practice they are usually *engineered* and not found. Can we build the Kitaev chain out of parts that exist? We will now see that the edge of a quantum spin Hall insulator, two magnets and an ordinary s-wave superconductor are enough. The Majorana zero modes then sit at the two ends of the segment of edge between the magnets.

::: {.recall eq="5.19"}
This is the Kitaev chain of Section [5.16](#sec-5-16), a chain of spinless fermions with the hopping $t$, the chemical potential $\mu$ and a pairing $\Delta$ between neighboring sites. In its topological phase it has one Majorana zero mode at each end. What it needs is a wire with a single channel in each direction of motion.
:::

One instructive recipe uses directly the quantum spin Hall (QSH) insulator of Section [3.11](#sec-3-11). We take a QSH insulator, for concreteness tungsten ditelluride (WTe$_2$). Its edge has helical modes, meaning that spin-up electrons propagate in one direction and spin-down electrons propagate in the other direction on the same edge. Now we place ordinary ferromagnets on two segments of this edge. A magnet breaks time-reversal symmetry locally, and this opens a gap in the helical edge modes below it. We recall from Section [3.11b](#sec-3-11b) that the protection of the QSH edge relies on time-reversal symmetry through Kramers degeneracy, so if we break this symmetry locally, the protection is lost there. What remains without a gap is a short isolated segment of helical edge between the two magnetic regions.

This isolated segment only has spin-up electrons moving right and spin-down electrons moving left, with no spin-down electrons moving right and no spin-up electrons moving left. If we count states only by their direction of propagation, this segment is *effectively spinless*, which is the ingredient that the Kitaev-chain construction of Section [5.16](#sec-5-16) needs. If we then couple this segment by proximity to an ordinary s-wave superconductor, we reproduce on it the physics of [(5.19)](#eq-5-19). This is a one-dimensional p-wave superconductor, with Majorana zero modes pinned at the two ends of the isolated segment. Figure [5.6](#fig:s05:qsh) shows the whole setup.

![How to build the Kitaev chain from parts that exist. The edge of a quantum spin Hall insulator is helical. On the same edge spin-up electrons move in one direction and spin-down electrons in the other, drawn in a warm and a cold color. A ferromagnet placed on a part of this edge breaks time-reversal symmetry locally and removes the Kramers protection there, which opens a gap in the edge below it, where the channels are drawn faded. With two ferromagnets, one short helical segment survives between them. This segment has only one direction of propagation for each spin, so if we count channels it is a *spinless* one-dimensional wire. This is the ingredient that [(5.19)](#eq-5-19) needs, and nature does not give it to us directly. Coupling it by proximity to an ordinary $s$-wave superconductor gives the pairing. The result is a one-dimensional $p$-wave superconductor with a Majorana zero mode at each end of the segment, which means at the two ferromagnet-superconductor interfaces. Note what was *not* needed. No unconventional superconductor appears in the recipe, only an $s$-wave one, a magnet and a topological insulator.](figures/s05f06_qsh.svg){#fig:s05:qsh number="5.6"}

Why do the Majoranas sit at the ends of the segment, and not somewhere else? Let us write the edge in the Nambu basis [(5.6)](#eq-5-6), with the velocity $v$ of the edge, an exchange field $h$ along $x$ from the magnet and an $s$-wave pairing $\Delta$ from the superconductor,

$$H(k)=\tau_z\left(vk\,\sigma_z-\mu\right)+h\,\sigma_x+\Delta\,\tau_x ,$$

where $\sigma$ acts on the spin and $\tau$ on the electron and the hole. The kinetic term and $\mu$ change sign in the hole block, while the exchange field keeps its sign. The simplest case is $k=0$ and $\mu=0$, where only the two terms that open a gap are left.

::: key
At $k=0$ and $\mu=0$ the four BdG levels of this edge are

$$E(k=0)=\pm h\pm\Delta .$$

The gap closes at $h=\Delta$. So a part of the edge where pairing wins, $h<\Delta$, and a part where the magnet wins, $h>\Delta$, are two different phases, and a Majorana zero mode sits at the boundary between them.
:::

::: {.steps title="The levels of the helical edge at k=0"}
At $k=0$ and $\mu=0$ the edge Hamiltonian is $H=h\,\sigma_x+\Delta\,\tau_x$. Let us take each term alone first. With $\Delta=0$ the magnet gives $h\sigma_x$, whose eigenvalues are $\pm h$, once for the electron and once for the hole. With $h=0$ the pairing gives $\Delta\tau_x$, with the eigenvalues $\pm\Delta$, once for each spin.

The two terms act on different indices, so they commute, $[\sigma_x,\tau_x]=0$, and they have common eigenvectors. On such a vector $\sigma_x=s$ and $\tau_x=s'$, with $s,s'=\pm1$, and the energy is the sum

$$E=s\,h+s'\Delta ,$$

which gives the four levels $\pm h\pm\Delta$. The level $h-\Delta$ crosses zero at $h=\Delta$, together with its partner $\Delta-h$, so the gap closes there. The two energies add, and they do not add in quadrature as $\varepsilon$ and $\Delta$ do in [(5.9)](#eq-5-9). The reason for this is that $\varepsilon\tau_z$ and $\Delta\tau_x$ anticommute, while $h\sigma_x$ and $\Delta\tau_x$ commute.
:::

![The two steps of Figure [5.6](#fig:s05:qsh), computed for the edge $H(k)$ above. (a) The helical edge, with spin up moving right and spin down moving left, is drawn with dashed lines, with the energy $E$ and $vk$ in the same unit. A magnet with an exchange field $h=0.7$ along $x$ couples the two branches and opens a gap $2h$ at $k=0$, as the solid lines show. (b) The levels at $k=0$ of the BdG Hamiltonian of the edge with both $h$ and an $s$-wave $\Delta$, for $\mu=0$, with the energy and $h$ in units of $\Delta$. They are $\pm h\pm\Delta$, and the gap closes at $h=\Delta$. For $h<\Delta$ the gap comes from pairing, and for $h>\Delta$ it comes from the magnet. These are two different phases, and the Majorana zero mode sits at the boundary between them.](figures/web/session05/helical_edge_gap.svg){#sch:s05:helical_edge_gap alt="On the left, two crossing dashed lines for the helical edge and a hyperbola with a gap 2h for the edge under a magnet, with the ticks 0.7 and minus 0.7 on the energy axis. On the right, four straight lines of the energy against h over Delta, two of which cross zero at h equal to Delta."}

The notebook builds the same competition in two dimensions, with a triangular lattice, a Rashba spin-orbit coupling, an exchange field $J$ along $z$ and an $s$-wave pairing $\Delta$. At $\Gamma$ the spin-orbit coupling vanishes, and the four levels are $\pm J\pm\sqrt{\varepsilon_\Gamma^2+\Delta^2}$, with $\varepsilon_\Gamma$ the band energy at $\Gamma$. This has the form of the levels of the edge at $k=0$, with $\sqrt{\varepsilon_\Gamma^2+\Delta^2}$ in place of $\Delta$. So the gap closes at $J=\sqrt{\varepsilon_\Gamma^2+\Delta^2}$, and [](#sch:s05:g6_artificial_tsc) shows that the Chern number of the BdG bands changes there.

![The artificial topological superconductor of the notebook against the exchange field $J$, computed with pyqula. This is the model of the notebook, a two-dimensional electron gas with spin-orbit coupling on a triangular lattice, and not the edge of this page. In pyqula the hopping is $+1$, which is $t=-1$ of the notes, so the band runs from $-3$ at $K$ to $6$ at $\Gamma$, and all energies are in units of $|t|$. The call `h.add_onsite(-5.7)` puts the band energy at $\Gamma$ at $\varepsilon_\Gamma=0.3$ above the Fermi level, which is the top of the band before the Rashba coupling is added. The Rashba coupling is `h.add_rashba(1.0)`, the exchange field `h.add_zeeman([0,0,J])` and the pairing `h.add_swave(0.3)`. With the Rashba coupling, $\Gamma$ is the crossing point of the two Rashba bands, and the Fermi level cuts them on two closed lines around $\Gamma$, one of them very close to $\Gamma$. The dots are the smallest quasiparticle energy $E_\mathrm{min}$ on the line $M$, $\Gamma$, $M$, which is also the smallest one over the whole zone, and the dashed line is the level at $\Gamma$, $|J-0.42|$. At $J=0$ the smallest energy is $\Delta=0.3$, on the Fermi surface, and from about $J=0.22$ on it is the level at $\Gamma$. This level goes to zero at $J=\sqrt{0.3^2+0.3^2}=0.42$, where the Chern number of the BdG bands below zero changes from $0$, computed at $J=0.3$, to $1$, computed at $J=0.6$. Look at the dip, since the two sides of it are two different phases.](figures/web/session05/g6_artificial_tsc.svg){#sch:s05:g6_artificial_tsc alt="A curve of the smallest quasiparticle energy against the exchange field. It starts at 0.3 and joins a dashed straight line that comes down from 0.42. From J of about 0.2 on, the curve lies on top of the dashed line. It comes down almost to zero at J equal to 0.42, and rises again. The region on the left is marked C equal to 0 and the one on the right C equal to 1." script="g6_artificial_tsc.py"}

::: lab
The helical edge of the recipe exists in monolayer WTe$_2$. Its quantum spin Hall state is seen in transport at temperatures up to $100$ K, as reported in [this article](https://www.science.org/doi/10.1126/science.aan6003). In another experiment, reported in [this article](https://www.nature.com/articles/s41567-020-0816-x), atomically thin layers of WTe$_2$ are placed on the van der Waals superconductor NbSe$_2$. There STM shows that at the edge of the monolayer the superconducting gap coexists with the spectroscopic signature of the quantum spin Hall edge state. The $100$ K belongs to the quantum spin Hall state of the first article, measured on another sample, and not to the proximity gap.
:::

::: quiz
The segment of helical edge between the two magnets is called effectively spinless. Why?

- [ ] The magnets remove the spin of the electrons.

    This is false. A magnet only breaks time-reversal symmetry and opens a gap below it. The electrons in the segment between the magnets still have spin, since spin-up moves right and spin-down moves left.

- [x] For each direction of motion only one spin is present, so counting channels gives a single spinless wire.

    This is true. On a helical edge spin-up moves in one direction and spin-down in the other. Each direction has one channel, as in the spinless chain that [(5.19)](#eq-5-19) needs.

- [ ] Spin-up and spin-down electrons move in both directions.

    This is false. That is an ordinary spinful wire with two channels in each direction. Pairing it with an $s$-wave superconductor gives a trivial gap and no Majoranas, so it is not the helical edge.
:::

::: quiz
At $k=0$ and $\mu=0$ the helical edge with a magnet and a pairing has

$$H=h\,\sigma_x+\Delta\,\tau_x .$$

Here $\sigma$ acts on the spin and $\tau$ on the electron and the hole. What are its levels?

- [x] $E=\pm h\pm\Delta$

    This is true. $\sigma_x$ and $\tau_x$ act on different indices, so they commute and have common eigenvectors, and their eigenvalues add. For $h=0.3$ and $\Delta=0.5$ the levels are $\pm0.2$ and $\pm0.8$.

- [ ] $E=\pm\sqrt{h^2+\Delta^2}$

    This is false. For $h=0.3$ and $\Delta=0.5$ this gives $\pm0.58$, while the matrix has the levels $\pm0.2$ and $\pm0.8$. A square root appears for two terms that anticommute, as $\varepsilon\tau_z$ and $\Delta\tau_x$ do in the BdG spectrum $E=\pm\sqrt{\varepsilon^2+|\Delta|^2}$.

- [ ] $E=\pm(h+\Delta)$

    This is false. These are only two of the four levels. For $h=0.3$ and $\Delta=0.5$ the matrix also has $\pm0.2$, which is $\pm(h-\Delta)$, and this pair crosses zero at $h=\Delta$.
:::

::: quiz
A helical edge with the velocity $v=1$ and $\mu=0.2$ has the BdG Hamiltonian

$$H(k)=\tau_z\left(vk\,\sigma_z-\mu\right)+h\,\sigma_x+\Delta\,\tau_x .$$

Each picture shows its levels against $k$. One has $h=\Delta=0$, one has only $h=0.5$, and one has only $\Delta=0.3$. Which picture has the gap of the magnet?

- [ ] ![The levels of the edge against k. Four straight lines cross zero at k equal to 0.2 and minus 0.2, and cross each other at k equal to 0.](figures/web/session05/g6_quiz_edge_bare.svg)

    This is false. With $h=\Delta=0$ nothing couples the branches. The lines cross zero at $k=\pm\mu/v=\pm0.2$, so this edge has no gap.

- [x] ![The levels of the edge against k. Four hyperbolas, two above zero and two below, each with its smallest distance from zero at k equal to 0.](figures/web/session05/g6_quiz_edge_magnet.svg)

    This is true. The magnet couples the two directions of motion where they cross, at $k=0$. The electron levels are $-\mu\pm\sqrt{v^2k^2+h^2}$ and the hole levels $\mu\pm\sqrt{v^2k^2+h^2}$, so the smallest energy is $h-\mu=0.3$, at $k=0$.

- [ ] ![The levels of the edge against k. Two levels above zero and two below, with their smallest distance from zero at k equal to 0.2 and minus 0.2, and crossings at k equal to 0.](figures/web/session05/g6_quiz_edge_pairing.svg)

    This is false. Pairing couples an electron and a hole where they cross zero, at the Fermi momenta $k=\pm0.2$. The smallest energy is $\Delta=0.3$ there, and at $k=0$ the levels are $\pm\sqrt{\mu^2+\Delta^2}=\pm0.36$.
:::

:::: problem
The edge has $\Delta=0.3$ and $\mu=0.4$. Show that its levels at $k=0$ are $\pm h\pm\sqrt{\Delta^2+\mu^2}$, and find the exchange field $h$ where the gap closes.

::: solution
At $k=0$ the edge Hamiltonian is $H=-\mu\,\tau_z+\Delta\,\tau_x+h\,\sigma_x$. The first two terms act only on $\tau$, and $\tau_z$ and $\tau_x$ anticommute, so

$$\left(-\mu\,\tau_z+\Delta\,\tau_x\right)^2=\mu^2+\Delta^2 ,$$

and their eigenvalues are $\pm\sqrt{\mu^2+\Delta^2}=\pm0.5$, as for $\varepsilon$ and $\Delta$ in [(5.9)](#eq-5-9). The last term acts only on $\sigma$ and commutes with both, so the energies add, as in the steps of the levels at $k=0$ above,

$$E(k=0)=\pm h\pm\sqrt{\Delta^2+\mu^2} .$$

The level $h-\sqrt{\Delta^2+\mu^2}$ crosses zero at $h=\sqrt{0.09+0.16}=0.5$. A scan over all $k$ gives the same answer, since the smallest energy of the edge vanishes only at $h=0.5$. So the chemical potential enters the condition, as it does in the window [(5.22)](#eq-5-22) of the Kitaev chain. A gate that moves the Fermi level of the edge then moves the boundary between the two phases.
:::
::::

::: notebookbox
**Notebook check-in:** [`session5.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session5.ipynb), "Artificial topological superconductivity" (Challenge), "Edge states of an artificial topological superconductor" (Challenge), and "Topological phase transition as a function of the exchange field"

Build the construction described above, with the QSH edge, the magnets and superconductivity, and check that zero modes localized at the ends emerge as you change the strength of the exchange field. Look at how the system crosses the boundary between the topological and the trivial phase, of the type of [(5.22)](#eq-5-22), as the magnetic gap changes.
:::

::: {.tryit notebook="session5.ipynb" cell="Topological phase transition as a function of the exchange field"}
In the cell, the loop runs over `J` from 0 to 0.6 with `add_swave(0.3)`. Follow the lowest energy near $\mathbf k=0$. It starts at $|\Delta|=0.3$, closes close to `J=0.42` and opens again. Above this value the state is the artificial topological superconductor.
:::

::: comesback
- In Section [5.19](#sec-5-19) the Majorana zero modes at the two ends of such a segment are the building blocks of a topological qubit.
- In Section [6.3](#sec-6-3) we see where the exchange field of a magnet comes from, as the mean-field magnetization of the Hubbard model.
- In Section [9.8](#sec-9-8) a vacancy tells a topological superconductor apart from a trivial one, when the two bulk spectra look the same.
:::
