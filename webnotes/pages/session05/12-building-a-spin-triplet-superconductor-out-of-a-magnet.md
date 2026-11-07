## Building a spin-triplet superconductor out of a magnet {#sec-5-12 number="5.12"}

Since spin-triplet order is so fragile, how could we ever build one on purpose? One way is a toy model that has both a ferromagnetic exchange field and an attractive interaction in the same Hamiltonian,

$$H = -t\sum_{\langle ij\rangle,\sigma}c_{i\sigma}^\dagger c_{j\sigma} \;\underbrace{-\, h\sum_i \left(c_{i\uparrow}^\dagger c_{i\uparrow} - c_{i\downarrow}^\dagger c_{i\downarrow}\right)}_{\text{exchange field}} \;+\; \underbrace{U\sum_{\langle ij\rangle} c_{i\sigma}^\dagger c_{j\sigma'}^\dagger c_{j\sigma'}c_{i\sigma}}_{\text{attractive interaction}}, \qquad U<0.$$

If we solve it self-consistently at the mean-field level, both order parameters, the ferromagnetic exchange field and the pairing amplitude, can be nonzero at the same time. The ground state then breaks both time-reversal symmetry, since it is magnetic, *and* gauge symmetry, since it is superconducting. The pairing that survives is necessarily spin-triplet, because the exchange field explicitly splits the $\uparrow$ and $\downarrow$ Fermi surfaces, and in this way it suppresses the singlet channel, which needs them to be degenerate. Physically, s-wave singlet pairing is usually the leading instability because it can gap the *entire* Fermi surface, which gives the largest condensation energy. When the exchange field suppresses this channel, a different pairing channel becomes the leading instability instead, which here is the odd-parity, spin-triplet channel, which is effectively p-wave.

![A chain with an exchange field $h$. The bands of the two spins are shifted by $\mp h$, so their Fermi momenta differ. A pair of two $\uparrow$ electrons sits on one Fermi surface, while the $\downarrow$ partner of an $\uparrow$ electron at $k_{F\uparrow}$ sits $2h$ above the Fermi level.](figures/web/session05/spin_split_pairing.svg){#sch:s05:spin_split_pairing alt="Two cosine bands for spin up and spin down, shifted in energy, with the Fermi points of each marked and an arrow of size 2h between the two bands at the Fermi momentum of spin up."}

::: quiz
In the model of this section, why does the exchange field suppress $s$-wave singlet pairing but not the pairing of two $\uparrow$ electrons?

- [ ] The exchange field breaks gauge symmetry explicitly.

    This is false. The exchange field $-h(n_\uparrow-n_\downarrow)$ conserves the particle number, so $c\to e^{i\varphi}c$ is still a symmetry of it. Gauge symmetry is broken only by the pairing itself.

- [x] An $\uparrow\downarrow$ pair at $\mathbf k$ and $-\mathbf k$ has an energy mismatch of $2h$, while an $\uparrow\uparrow$ pair does not.

    This is true. The field shifts the two spin bands by $\mp h$. The $\downarrow$ partner of an $\uparrow$ electron on its Fermi surface sits $2h$ above the Fermi level, while two $\uparrow$ electrons share one band.

- [ ] The $\uparrow$ electrons have no kinetic energy in a field.

    This is false. In the field the $\uparrow$ band is $-2t\cos k-h$, which still has the bandwidth $4t$. The $\uparrow$ electrons move normally, and they can form a Fermi surface to pair on.
:::

The most interesting feature of this state appears when we put it on a finite ribbon instead of an infinite plane. The bulk spectrum is gapped, as we expect for a superconductor, but the edges of the ribbon have gapless excitations. A superconductor that is fully gapped in the bulk and gapless at the edge is a signature that we already know from Session 3 and Session 4, through the bulk-boundary correspondence of Section [3.7](#sec-3-7). These edge modes have a topological origin. They are tied to a finite Chern number of the BdG band structure, in the same way as the edge states of a Chern insulator are tied to its Chern number [(3.4)](#eq-3-4).

::: notebookbox
**Notebook check-in:** [`session5.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session5.ipynb), "The impact of a spin splitting in an electronic structure" (Reminder), "A spin triplet superconductor" (Core) and "Majorana modes in a spin triplet superconductor" (Challenge). The notebook goes further in "Interaction-induced spin-triplet superconductivity" (Challenge) and "Topological modes in interaction-driven spin triplet superconductors".

Start from the plain spin-split band structure, with only an exchange field, to build intuition. Then run the self-consistency loop for the model above and check that a spin-triplet $\Delta$ emerges. Move to a ribbon geometry and find the gapless edge modes described here, and then, in the later challenge sections of the notebook, connect them to the Majorana physics of Section [5.15](#sec-5-15) to Section [5.17](#sec-5-17).
:::

::: {.tryit notebook="session5.ipynb" cell="The impact of a spin splitting in an electronic structure"}
In the cell, the line `h.add_exchange([0.,0.,1.0])` splits the two spin bands of the chain. Change `1.0` to `2.0`. The two bands move apart from 2 to 4 at a fixed momentum, so each spin has its own Fermi momentum.
:::

::: comesback
- In Section [5.14](#sec-5-14) we compute the Chern number of the BdG bands and see why a chiral $p$-wave superconductor has edge modes.
- In Section [5.18](#sec-5-18) a magnet and an $s$-wave superconductor are put together again, on the helical edge of a quantum spin Hall insulator, to give Majorana zero modes.
- In Section [9.8](#sec-9-8) a vacancy in a chiral spin-triplet superconductor hosts a mode inside the gap, because of the same Chern number.
:::
