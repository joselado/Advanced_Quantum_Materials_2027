## Building a spin-triplet superconductor out of a magnet {#sec-5-12 number="5.12"}

Since spin-triplet order is so fragile, how could we ever build one on purpose? One way is a toy model that has both a ferromagnetic exchange field and an attractive interaction in the same Hamiltonian,

$$H = -t\sum_{\langle ij\rangle,\sigma}c_{i\sigma}^\dagger c_{j\sigma} \;\underbrace{-\, h\sum_i \left(c_{i\uparrow}^\dagger c_{i\uparrow} - c_{i\downarrow}^\dagger c_{i\downarrow}\right)}_{\text{exchange field}} \;+\; \underbrace{U\sum_{\langle ij\rangle} c_{i\sigma}^\dagger c_{j\sigma'}^\dagger c_{j\sigma'}c_{i\sigma}}_{\text{attractive interaction}}, \qquad U<0.$$

If we solve it self-consistently at the mean-field level, both order parameters, the ferromagnetic exchange field and the pairing amplitude, can be nonzero at the same time. The ground state then breaks both time-reversal symmetry, since it is magnetic, *and* gauge symmetry, since it is superconducting. The pairing that survives is necessarily spin-triplet, because the exchange field explicitly splits the $\uparrow$ and $\downarrow$ Fermi surfaces, and in this way it suppresses the singlet channel, which needs them to be degenerate. Physically, s-wave singlet pairing is usually the leading instability because it can gap the *entire* Fermi surface, which gives the largest condensation energy. When the exchange field suppresses this channel, a different pairing channel becomes the leading instability instead, which here is the odd-parity, spin-triplet channel, which is effectively p-wave.

![A chain with an exchange field $h$. The bands of the two spins are shifted by $\mp h$, so their Fermi momenta differ. A pair of two $\uparrow$ electrons sits on one Fermi surface, while the $\downarrow$ partner of an $\uparrow$ electron at $k_{F\uparrow}$ sits $2h$ above the Fermi level.](figures/web/session05/spin_split_pairing.svg){#sch:s05:spin_split_pairing alt="Two cosine bands for spin up and spin down, shifted in energy, with the Fermi points of each marked and an arrow of size 2h between the two bands at the Fermi momentum of spin up."}

::: quiz
In the model of this section, why does the exchange field suppress $s$-wave singlet pairing but not the pairing of two $\uparrow$ electrons?

- [ ] The exchange field breaks gauge symmetry explicitly.
- [x] An $\uparrow\downarrow$ pair at $\mathbf k$ and $-\mathbf k$ has an energy mismatch of $2h$, while an $\uparrow\uparrow$ pair does not.
- [ ] The exchange field turns the interaction repulsive.
- [ ] The $\uparrow$ electrons have no kinetic energy in a field.

A pair at the Fermi level needs both electrons at zero energy. The field shifts the two spins by opposite amounts, so the partners of an $\uparrow\downarrow$ pair cannot both sit on their Fermi surfaces. Two $\uparrow$ electrons share one band, and they can.
:::

The most interesting feature of this state appears when we put it on a finite ribbon instead of an infinite plane. The bulk spectrum is gapped, as we expect for a superconductor, but the edges of the ribbon have gapless excitations. A superconductor that is fully gapped in the bulk and gapless at the edge is a signature that we already know from the topological-band-structure and quantum-Hall sessions. Indeed, these edge modes have a topological origin, and they are tied to a finite Chern number of the underlying BdG band structure, in the same way as the edge states of a Chern insulator were tied to its Chern number.

::: notebookbox
**Notebook check-in:** [`session5.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session5.ipynb), "The impact of a spin splitting in an electronic structure" (Reminder), "A spin triplet superconductor" (Core), "Majorana modes in a spin triplet superconductor" (Challenge), "Interaction-induced spin-triplet superconductivity" (Challenge), and "Topological modes in interaction-driven spin triplet superconductors"

Start from the plain spin-split band structure, with only an exchange field, to build intuition. Then run the self-consistency loop for the model above and check that a spin-triplet $\Delta$ emerges. Move to a ribbon geometry and find the gapless edge modes described here, and then, in the later challenge sections of the notebook, connect them to the Majorana physics of sections [5.15](#sec-5-15)-[5.17](#sec-5-17).
:::

::: {.tryit notebook="session5.ipynb" cell="The impact of a spin splitting in an electronic structure"}
In the cell, the line `h.add_exchange([0.,0.,1.0])` splits the two spin bands of the chain. Change `1.0` to `2.0`. The two bands move apart from 2 to 4 at a fixed momentum, so each spin has its own Fermi momentum.
:::
