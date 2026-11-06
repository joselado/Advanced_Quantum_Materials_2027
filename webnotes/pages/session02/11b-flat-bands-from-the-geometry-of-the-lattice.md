## Flat bands from the geometry of the lattice, the Lieb and the kagome lattices {#sec-2-11b number="2.11b"}

Two standard lattices realize truly flat bands only from their geometry in real space, and not from a fine-tuning of hopping parameters to zero. The **Lieb lattice** is built from a square lattice where one site out of every four is removed in a regular pattern. Its dispersion has two dispersive bands, which come from the bands of the square lattice [(2.14)](#eq-2-14), and in addition one exactly flat band at zero energy. Near the corner $M$ of the Brillouin zone the two dispersive bands form a linear, Dirac-like cone, and the flat band goes through the tip of this cone. The **kagome lattice** is built instead from a triangular lattice where one site out of every four is removed. Its dispersion is closer to the one of the honeycomb lattice, with linear crossings similar to Dirac cones, and in addition it has a flat band at the edge of the spectrum. With the sign convention of [(2.5)](#eq-2-5) this flat band is at the top, at $\epsilon=2t$, and it would be at the bottom for the opposite sign of $t$. In both cases the flat band comes from destructive interference between hopping paths in real space. This is a purely geometric effect and not an effect of interactions, and the physics of strong correlations only enters once electrons are placed into these bands, which are already flat. Figure [2.6](#fig:s02:flatbands) shows both lattices, both dispersions, and the localized state where the hopping paths cancel.

![Flat bands that come only from geometry, with the bands computed from the Bloch Hamiltonian of each lattice and the flat band drawn as the red tube. **(a)** The Lieb lattice, which is a square lattice with one site in four removed, and **(b)** its bands. There are two dispersive bands and a band that is exactly flat at $\epsilon=0$, and all three touch at $M$. **(c)** The kagome lattice, made of triangles that share corners, and **(d)** its bands, with a Dirac-like crossing at $K$ and a flat band at $\epsilon=2t$. **(e)** The reason why the flat band exists. An eigenstate can be confined to a single kagome hexagon, with amplitudes of alternating sign around it, the filled and the ghost balls. Every path by which it could hop onto a site outside arrives twice with opposite sign, the two arrows, so the two contributions cancel at the cross. Nothing is fine-tuned to zero, since the flatness is a property of the geometry of the lattice, and by [(2.16)](#eq-2-16) it makes the density of states diverge.](figures/s02f05_flatbands.svg){#fig:s02:flatbands number="2.6"}

::: quiz
We change the value of the hopping $t$ of the kagome lattice. Where is the flat band?

- [x] At $\epsilon=2t$, so its energy changes with $t$ but it stays flat.

    This is true. The flat band comes from interference between hopping paths, which works for any value of the hopping. So the band scales with $t$, and it stays flat.

- [ ] At zero energy, for any $t$.

    This is false. Zero energy is the flat band of the Lieb lattice. For the kagome lattice with $t=1$ it is at $2$, and with $t=2$ it is at $4$.

- [ ] It becomes dispersive.

    This is false. The state on one hexagon obeys $H\psi=2t\psi$ exactly, for any $t$, since the cancellation does not involve its value. A change of $t$ only moves the energy.

The flatness is a property of the geometry, and $t$ sets only the energy scale.
:::

::: quiz
Why does the state on one hexagon of the kagome lattice not spread to the sites outside?

- [x] Every outside site is reached by two paths with opposite signs, so the amplitudes cancel.

    This is true. The alternating amplitudes around the hexagon make the two contributions to each outside site equal and opposite, as in panel (e) of the figure. Nothing is tuned to zero, since this is a property of the geometry.

- [ ] The hopping to the outside sites is zero.

    This is false. Every bond of the kagome lattice has the same hopping $t$, and an outside site is bonded to two sites of the hexagon. The two terms are $-ta$ and $+ta$, each of them nonzero, and they add up to zero.

- [ ] The state is localized by the interaction.

    This is false. The tight-binding Hamiltonian has no interaction, and the state is still an exact eigenstate with energy $2t$. The localization comes from the interference alone.

The localization is a single-particle effect of the geometry.
:::

This material is only on the slides and has no counterpart in `session2.ipynb`. The notebook treats the honeycomb lattice in depth, but it has no section on the Lieb lattice or on the kagome lattice. The band-structure plots for both lattices are shown directly on the slides. The description above gives their qualitative structure, but to see the actual flat-band dispersion one needs the figure itself.

::: {.tryit notebook="session2.ipynb" cell="Infinite two-dimensional graphene"}
In the cell with the bands, replace the honeycomb lattice by `lieb_lattice()` or by `kagome_lattice()`. Find the band that does not disperse. With the sign of the hopping of the notebook, the Lieb flat band is at zero energy and the kagome one is at the bottom.
:::
