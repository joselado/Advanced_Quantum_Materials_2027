## Flat bands from the geometry of the lattice, the Lieb and the kagome lattices {#sec-2-11b number="2.11b"}

Can a band be flat when every hopping of the lattice is nonzero? We will now see that it can, in the Lieb and the kagome lattices, where a state on one plaquette cancels on every site outside it. This gives a flat band at $\epsilon=0$ for the Lieb lattice and at $\epsilon=2t$ for the kagome lattice, with the sign of [(2.5)](#eq-2-5).

::: {.recall eq="2.16"}
This is the density of states of Section [2.9](#sec-2-9). It counts the states per unit of energy at the energy $\omega$, for one band $E(\mathbf k)$ and for one spin, per unit length, area or volume of the lattice in $d$ dimensions.
:::

Two standard lattices realize truly flat bands only from their geometry in real space, and not from a fine-tuning of hopping parameters to zero. The **Lieb lattice** is built from a square lattice where one site out of every four is removed in a regular pattern. Its dispersion has two dispersive bands, which come from the bands of the square lattice [(2.14)](#eq-2-14), and in addition one exactly flat band at zero energy. Near the corner $M$ of the Brillouin zone the two dispersive bands form a linear, Dirac-like cone, and the flat band goes through the tip of this cone.

The **kagome lattice** is built instead from a triangular lattice where one site out of every four is removed. Its dispersion is closer to the one of the honeycomb lattice, with linear crossings similar to Dirac cones, and in addition it has a flat band at the edge of the spectrum. With the sign convention of [(2.5)](#eq-2-5) this flat band is at the top, at $\epsilon=2t$, and it would be at the bottom for the opposite sign of $t$. In both cases the flat band comes from destructive interference between hopping paths in real space. This is a purely geometric effect and not an effect of interactions, and the physics of strong correlations only enters once electrons are placed into these bands, which are already flat. Figure [2.6](#fig:s02:flatbands) shows both lattices, both dispersions, and the localized state where the hopping paths cancel.

![Flat bands that come only from geometry, with the bands computed from the Bloch Hamiltonian of each lattice and the flat band drawn as the red tube. **(a)** The Lieb lattice, which is a square lattice with one site in four removed, and **(b)** its bands. There are two dispersive bands and a band that is exactly flat at $\epsilon=0$, and all three touch at $M$. **(c)** The kagome lattice, made of triangles that share corners, and **(d)** its bands, with a Dirac-like crossing at $K$ and a flat band at $\epsilon=2t$. **(e)** The reason why the flat band exists. An eigenstate can be confined to a single kagome hexagon, with amplitudes of alternating sign around it, the filled and the ghost balls. Every path by which it could hop onto a site outside arrives twice with opposite sign, the two arrows, so the two contributions cancel at the cross. Nothing is fine-tuned to zero, since the flatness is a property of the geometry of the lattice, and by [(2.16)](#eq-2-16) it makes the density of states diverge.](figures/s02f05_flatbands.svg){#fig:s02:flatbands number="2.6"}

The localized state of panel (e) is the whole reason for the flat band of the kagome lattice, and one line of algebra shows that it is an exact eigenstate.

::: key
On the kagome lattice with $H=-t\sum_{\langle ij\rangle}c_i^\dagger c_j$ over first neighbors, the state $\psi$ with the amplitudes $+1,-1,+1,-1,+1,-1$ around one hexagon, and zero on every other site, obeys

$$H\psi = 2t\,\psi$$

for any value of $t$. Such a state sits on every hexagon of the lattice, so the energy $2t$ does not depend on the momentum, which is the flat band. It holds one third of all the states.
:::

::: {.steps title="Why the state on one hexagon has the energy 2t"}
We write $H\psi$ site by site, $(H\psi)_i=-t\sum_j\psi_j$, where the sum runs over the four neighbors $j$ of the site $i$. First a site $i$ of the hexagon. Two of its four neighbors are its neighbors on the hexagon, and both have the amplitude $-\psi_i$, since the signs alternate. Its two other neighbors are outside the hexagon, where $\psi$ is zero. So

$$(H\psi)_i=-t\,(-\psi_i-\psi_i)=2t\,\psi_i.$$

Next a site outside the hexagon that touches it. In the kagome lattice every bond of the hexagon is the side of a triangle, and such a site is the third corner of that triangle. Its other two corners are neighbors on the hexagon, with the amplitudes $a$ and $-a$, so the site gets

$$-t\,(a-a)=0.$$

Every other site has no neighbor on the hexagon and gets zero. Together this is $H\psi=2t\,\psi$, with no condition on the value of $t$.

The Lieb lattice has the same kind of state at zero energy. We put the amplitudes $+1,-1,+1,-1$ on the four edge sites around one square plaquette, which are the sites with two neighbors, and zero elsewhere. An edge site has only corner sites as neighbors, where the amplitude is zero, so it gets zero. Each corner of the plaquette is bonded to two of the four edge sites, with opposite amplitudes, so it gets $-t\,(1-1)=0$. So $H\psi=0$, and the flat band of the Lieb lattice sits at $\epsilon=0$ for either sign of $t$.
:::

The flat band is one band of three, so it puts one third of the states at a single energy, and in [(2.16)](#eq-2-16) it gives a delta peak. The bands and the density of states of the kagome lattice, computed with pyqula, are in [](#sch:s02:kagome_dos). There the peak sits on top of the smooth density of the two other bands.

![The bands and the density of states of the kagome lattice with $H=-t\sum_{\langle ij\rangle}c_i^\dagger c_j$ over first neighbors, computed with pyqula, with the energy in units of $t$. The flat band at $\epsilon=2t$, in red, holds one third of all the states at a single energy. So in [(2.16)](#eq-2-16) it gives a delta peak, which the broadening turns into a narrow peak that the plot cuts. The two dispersive bands give a continuous density of states between $-4t$ and $2t$, with two peaks at the energies of the bands at $M$, $-2t$ and $0$. It has a V at $-t$, where the two bands cross at $K$. The density is per unit cell, summed over the three bands and for one spin, with every level broadened into a Lorentzian of half width $0.04\,t$ on a mesh of $200\times200$ momenta.](figures/web/session02/kagome_dos.svg){#sch:s02:kagome_dos alt="On the left the three bands of the kagome lattice along Gamma, K, M and Gamma, with a red flat band at 2t. On the right the density of states, smooth below, with a V at minus t, two peaks at minus 2t and zero, and a cut red peak at 2t." script="g4_kagome_bands.py"}

::: lab
In the kagome system CoSn, ARPES sees the flat band. The preprint of this article, arXiv 2002.01452, describes it as a state with no dispersion along the path from $\Gamma$ to $M$. There its width is below $150$ meV, which is an order of magnitude smaller than the width of the Dirac bands that come from the same orbitals. The published abstract gives no width in meV, and it says that the width of the flat band is an order of magnitude smaller over the whole Brillouin zone. In the first-neighbor model of this section the width is zero. Our reading is that the $d$ orbitals of CoSn and its longer-range hoppings give the small width that is measured. The measurement is in [this article](https://www.nature.com/articles/s41467-020-17465-1).
:::

::: quiz
The kagome lattice has the Hamiltonian

$$H=-t\sum_{\langle ij\rangle}c_i^\dagger c_j,$$

with the sum over first neighbors. We change the value of $t$. Where is the flat band?

- [x] At $\epsilon=2t$, so its energy changes with $t$ but it stays flat.

    This is true. The flat band comes from interference between hopping paths, which works for any value of the hopping. So the band scales with $t$, and it stays flat.

- [ ] At zero energy, for any $t$.

    This is false. Zero energy is the flat band of the Lieb lattice. For the kagome lattice with $t=1$ it is at $2$, and with $t=2$ it is at $4$.

- [ ] It becomes dispersive.

    This is false. The state on one hexagon obeys $H\psi=2t\psi$ exactly, for any $t$, since the cancellation does not involve its value. A change of $t$ only moves the energy.

The flatness is a property of the geometry, and $t$ sets only the energy scale.
:::

::: quiz
Around one hexagon of the kagome lattice we put the amplitudes $+1,-1,+1,-1,+1,-1$, and zero elsewhere. Why does this state not spread to the sites outside?

- [x] Every outside site is reached by two paths with opposite signs, so the amplitudes cancel.

    This is true. The alternating amplitudes around the hexagon make the two contributions to each outside site equal and opposite. Nothing is tuned to zero, since this is a property of the geometry.

    ![The state on one hexagon, with amplitudes of alternating sign, the filled and the ghost balls. The two arrows that reach a site outside arrive with opposite signs and cancel at the cross.](figures/s02f05_flatbands.svg){panel="e" alt="A hexagon of the kagome lattice with balls of alternating sign on its corners and two arrows that meet at a site outside."}

- [ ] The hopping to the outside sites is zero.

    This is false. Every bond of the kagome lattice has the same hopping $t$, and an outside site is bonded to two sites of the hexagon. The two terms are $-ta$ and $+ta$, each of them nonzero, and they add up to zero.

- [ ] The state is localized by the interaction.

    This is false. The tight-binding Hamiltonian has no interaction, and the state is still an exact eigenstate with energy $2t$. The localization comes from the interference alone.

The localization is a single-particle effect of the geometry.
:::

::: quiz
The kagome lattice with first-neighbor hopping has the Hamiltonian

$$H=-t\sum_{\langle ij\rangle}c_i^\dagger c_j,\qquad t>0.$$

Each picture shows the bands of a lattice with three sites per cell. The energy is in units of $t$. Which one is this kagome lattice?

- [x] ![Three bands along Gamma, K, M and Gamma, with a flat band at the top at two.](figures/web/session02/g4_quiz_flat_kagome_minus.svg)

    This is true. The flat band is the top band, at $2t$, as the state on one hexagon gives. The two other bands run from $-4t$ at $\Gamma$ to $2t$, and they cross at $-t$ at $K$.

- [ ] ![Three bands along Gamma, K, M and Gamma, with a flat band at the bottom at minus two.](figures/web/session02/g4_quiz_flat_kagome_plus.svg)

    This is false. The flat band is at $-2t$, at the bottom, and the bands run from $-2t$ to $4t$. These are the bands of $H=+t\sum c_i^\dagger c_j$, the sign of the notebook, which turns the kagome bands upside down.

- [ ] ![Three bands along Gamma, X, M and Gamma, with a flat band at zero in the middle.](figures/web/session02/g4_quiz_flat_lieb.svg)

    This is false. The flat band is at zero, between the two other bands, and all three meet at $M$. This is the Lieb lattice, whose flat band stays at zero for either sign of $t$.

The sign of the hopping decides whether the kagome flat band is at the top or at the bottom of the spectrum.
:::

::: quiz
The kagome lattice has the Hamiltonian

$$H=-t\sum_{\langle ij\rangle}c_i^\dagger c_j.$$

The state $\psi$ has the amplitudes $+1,-1,+1,-1,+1,-1$ around one hexagon, and zero elsewhere. What is $H\psi$?

- [x] $H\psi=2t\,\psi$

    This is true. A site of the hexagon gets $-t$ times the sum of its two neighbors on the hexagon, which are both $-\psi_i$, so it gets $2t\,\psi_i$. A site outside gets $-t\,(1-1)=0$.

- [ ] $H\psi=-2t\,\psi$

    This is false. Take $t=1$ and a site with $\psi_i=1$. Its two neighbors on the hexagon have $-1$, so $(H\psi)_i=-1\cdot(-1-1)=2$, and not $-2$. The energy $-2t$ belongs to $H=+t\sum c_i^\dagger c_j$, the sign of the notebook.

- [ ] $H\psi=0$

    This is false. For $t=1$ the site with $\psi_i=1$ gets $2$, which is not zero. Zero is what the sites outside the hexagon get, and it is the energy of the state on one plaquette of the Lieb lattice.

The two neighbors on the hexagon add up, and the two paths to a site outside cancel.
:::

:::: problem
The Lieb lattice has three sites per cell. A corner site $C$ has four neighbors, and two edge sites, $X$ between two corners along $x$ and $Y$ between two corners along $y$, have two neighbors each. We take the hopping $-t$ and the bond length $1$, so the lattice constant is $2$. Write the Bloch Hamiltonian, and find its energies at $\Gamma=(0,0)$ and at the corner $M=(\pi/2,\pi/2)$ of the Brillouin zone.

::: solution
We put each orbital at its position in the cell, with $C$ at the origin, $X$ at $(1,0)$ and $Y$ at $(0,1)$. The corner $C$ is bonded to the site $X$ of its own cell, at $(1,0)$, and to the site $X$ of the cell before it along $x$, at $(-1,0)$. Its entry with $X$ is then $-t\,(e^{ik_x}+e^{-ik_x})=-2t\cos k_x$, and in the same way its entry with $Y$ is $-2t\cos k_y$. The sites $X$ and $Y$ are not bonded, so

$$H(\mathbf k)=-2t\begin{pmatrix}0&\cos k_x&\cos k_y\\ \cos k_x&0&0\\ \cos k_y&0&0\end{pmatrix}.$$

The vector $(0,\cos k_y,-\cos k_x)$ has the energy $0$ at every $\mathbf k$, which is the flat band. The other two energies are

$$\epsilon_\pm(\mathbf k)=\pm2t\sqrt{\cos^2k_x+\cos^2k_y}.$$

At $\Gamma$ this gives $\pm2\sqrt2\,t\approx\pm2.83\,t$ and $0$. At $M$ both cosines vanish, so all three energies are $0$, and the two dispersive bands touch the flat band there, as panel (b) of Figure [2.6](#fig:s02:flatbands) shows. In a calculation, these energies at $\Gamma$ and at $M$ are a quick test that a code has the right lattice and the right size of the hopping. They do not test its sign, since the Lieb bands are the same for $t$ and $-t$. The kagome flat band, at $+2t$ or at $-2t$, does test the sign.
:::
::::

The notebook `session2.ipynb` treats the honeycomb lattice in depth, but it has no section on the Lieb lattice or on the kagome lattice. The box below builds both from the cell of the honeycomb lattice.

::: {.tryit notebook="session2.ipynb" cell="Infinite two-dimensional graphene"}
In the cell with the bands, replace the honeycomb lattice by `lieb_lattice()` or by `kagome_lattice()`. Find the band that does not disperse. With the sign of the hopping of the notebook, the Lieb flat band is at zero energy and the kagome one is at the bottom.
:::

::: comesback
- In Session 4 the Landau levels are flat bands with Chern number one, in Section [4.4](#sec-4-4), and Section [4.20](#sec-4-20) shows topological flat bands in real materials.
- In Section [6.6](#sec-6-6) the flat band of the Lieb lattice makes the Stoner criterion true for any interaction $U>0$.
- The kagome lattice comes back in Section [8.4](#sec-8-4), where its triangles frustrate a quantum magnet.
- In Section [8.13](#sec-8-13) the Kondo lattice gives a heavy band that is almost flat.
:::
