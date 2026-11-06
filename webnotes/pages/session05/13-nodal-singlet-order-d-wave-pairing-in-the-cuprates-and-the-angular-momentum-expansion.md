## Nodal singlet order, d-wave pairing in the cuprates and the angular-momentum expansion {#sec-5-13 number="5.13"}

Inside the spin-singlet, even-parity order there is a further useful distinction, since a singlet gap can be uniformly nonzero, as in the s-wave case of section [5.9](#sec-5-9), or it can be nodal. The standard example of the second case is **d-wave** order on the square lattice,

$$\Delta_{d}(\mathbf k) = \Delta_0\left(\cos k_x - \cos k_y\right), \tag{5.13}$$

which vanishes exactly along the diagonals of the Brillouin zone, $k_x = \pm k_y$. Together with [(5.9)](#eq-5-9), this means that the quasiparticle spectrum $E(\mathbf k) = \sqrt{\varepsilon(\mathbf k)^2 +
\Delta_d(\mathbf k)^2}$ is gapless where the Fermi surface crosses these diagonals, which gives a nodal singlet superconductor. This is the pairing symmetry of the cuprate high-temperature superconductors, which have critical temperatures up to about 130 K at ambient pressure, above the boiling point of liquid nitrogen, and are spin-singlet, but clearly *not* s-wave.

Behind this there is a clear and general way to organize the possible cases, which is analogous to the expansion of an atomic orbital wave function in spherical harmonics. We expand the superconducting gap in an angular-momentum basis on the Fermi surface,

$$\Delta(\mathbf k) \;\sim\; \sum_L \Delta_L\, Y_L(\mathbf k), \tag{5.14}$$

$$\begin{aligned}
L=0:\quad &\text{s-wave (conventional, typically phonon-driven)},\\
L=1:\quad &\text{p-wave (spin-triplet, often ferromagnetic-magnon-driven)},\\
L=2:\quad &\text{d-wave (spin-singlet, often antiferromagnetic-magnon-driven; cuprates)}.
\end{aligned}$$

In real and reciprocal space, s-wave order is flat and constant, with no momentum dependence at all. The $d_{x^2-y^2}$ order of [(5.13)](#eq-5-13) changes sign around the Fermi surface in a pattern of four lobes, $+,-,+,-$, with the same name and the same lobe structure as an atomic $d$ orbital. There is also a third possibility, which is called *extended s-wave*. It is still $L=0$, meaning that it has the same overall symmetry as plain s-wave under the lattice point group, but it is nodal along the *radial* direction, since it is positive near the zone center $\Gamma$, goes through a node and is negative further out. Figure [5.3](#fig:s05:gapsymmetry) shows these sign structures over the Brillouin zone, together with the p- and f-wave cases below.

The lecture repeats the same classification into three cases, uniform s-wave, a nodal order and extended s-wave, on the triangular lattice. There the nodal case has six lobes of alternating sign around the Fermi surface, and it is an **f-wave order, $L=3$**. The instructor confirmed this, and the \"L equal to two\" in the raw recording was a mistake, since a pattern of six lobes with alternating sign is the standard signature of $L=3$ and not of $L=2$, which is already used above for the four-lobed $d_{x^2-y^2}$ state of the square lattice. Note that this order is outside the singlet family of this section. Six lobes with alternating sign mean that the gap changes sign under a half turn, so $\Delta(-\mathbf k) =
-\Delta(\mathbf k)$, and by [(5.12)](#eq-5-12) an $L=3$ order has odd parity and is therefore necessarily *spin-triplet*, and not singlet like the s-, extended-s- and d-wave cases above.

![The sign structure of $\Delta(\mathbf k)$ over the Brillouin zone, ordered by angular momentum $L$ as in [(5.14)](#eq-5-14). The positive regions are raised and the negative ones are sunk, in two colors, and the nodes are where the two colors meet. A reflection of a panel through its centre sends $\mathbf k\to-\mathbf k$. Panels with even $L$ do not change and are therefore spin singlets, and panels with odd $L$ come back with every sign flipped and are spin triplets, which is [(5.12)](#eq-5-12) seen in a picture. Counting lobes is the fastest way to identify the order. Two lobes mean $L=1$, four mean $L=2$ and six mean $L=3$, and any pattern whose lobes alternate an odd number of times in a half turn is necessarily odd in $\mathbf k$, so it is a triplet. This is why the $f$-wave state (e), which has six lobes on the hexagonal zone of the triangular lattice, is a spin triplet, even though it is similar to the singlet $d$-wave state in every other respect. Extended $s$-wave (b) deserves a second look, since its node is radial and not angular. It has the same even parity and the same point-group symmetry as plain $s$-wave, and only the position of its node ring relative to the Fermi surface decides whether it is nodal in the spectrum. The overall sign of $\Delta$ is a gauge choice, and only the sign *changes* are physical.](figures/s05f03_gapsymmetry.svg){#fig:s05:gapsymmetry number="5.3"}

::: quiz
On the triangular lattice a gap has six lobes of alternating sign around the Fermi surface. What are its parity, its angular momentum and its spin?

- [ ] Even parity, $L=2$, spin singlet.

    This is false. A $d$-wave gap such as $\cos k_x-\cos k_y$ has four lobes. Six lobes of alternating sign cannot be even, because a half turn moves each lobe by three places and flips its sign.

- [x] Odd parity, $L=3$, spin triplet.

    This is true. A half turn moves every lobe by three places, and the sign alternates, so $\Delta(-\mathbf k)=-\Delta(\mathbf k)$. By [(5.12)](#eq-5-12) this is odd parity and a spin triplet, and six lobes mean $L=3$.

- [ ] Even parity, $L=3$, spin singlet.

    This is false. A function $\cos3\theta$ has $L=3$ and six lobes. Under $\theta\to\theta+\pi$ it becomes $\cos(3\theta+3\pi)=-\cos3\theta$, so it is odd and an odd $L$ cannot be a singlet.
:::

::: notebookbox
**Notebook check-in:** [`session5.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session5.ipynb), "Gapped and nodal superconducting orders" (Core)

Implement the $d_{x^2-y^2}$ gap of [(5.13)](#eq-5-13) on the square lattice, plot $\Delta(\mathbf k)$ over the Brillouin zone, and check the pattern of four lobes with alternating sign and the position of its nodes relative to a given Fermi surface. The nodal $L=3$ (f-wave) case of the triangular lattice discussed above is also in this section of the notebook, if you want to see the pattern of six lobes directly.
:::

::: {.tryit notebook="session5.ipynb" cell="Gapped and nodal superconducting orders"}
In the cell, compare the bands along the path `G`, `K`, `M`, `G` for the two orders. The $s$-wave bands keep a gap of $|\Delta|=0.4$ at the Fermi surface. The nodal $f$-wave bands touch zero energy, even though $\Delta=0.2$ is nonzero.
:::
