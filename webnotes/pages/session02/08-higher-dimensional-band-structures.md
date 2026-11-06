## Higher-dimensional band structures {#sec-2-8 number="2.8"}

A two-dimensional lattice has two independent translations that commute with each other, $T_x$ and $T_y$, so Bloch eigenstates have two independent phases, $\varphi_x$ and $\varphi_y$, one for each direction. These phases are related to the crystal momentum along the two lattice vectors by the same Taylor-expansion argument as in [(2.10)](#eq-2-10), applied once for each direction. The space of allowed pairs $(\varphi_x,\varphi_y)$ is the **Brillouin zone**. Since $\varphi=0$ and $\varphi=2\pi$ give the same translation eigenvalue in both directions, the Brillouin zone is not an open square but a periodic one. When we identify the left and right edges, and the top and bottom edges, it becomes a torus, in the same way as it is a circle in the one-dimensional case of Section [2.5](#sec-2-5). This compactness of the Brillouin zone will be very important when topological invariants appear in the next session.

When we apply the Fourier method of Section [2.5](#sec-2-5) once for each spatial direction, we obtain for a square lattice with a single orbital and nearest-neighbour hopping $t$, with the same sign convention as in [(2.5)](#eq-2-5),

$$\epsilon(\varphi_x,\varphi_y) = -2t\left(\cos\varphi_x + \cos\varphi_y\right), \tag{2.14}$$

and, when we apply the same argument a third time, for a cubic lattice with a single orbital,

$$\epsilon(\varphi_x,\varphi_y,\varphi_z) = -2t\left(\cos\varphi_x+\cos\varphi_y+\cos\varphi_z\right). \tag{2.15}$$

The same method extends in a systematic way to four, five or more dimensions, since nothing in the argument depends on being in three-dimensional space. Equations [(2.14)](#eq-2-14) and [(2.15)](#eq-2-15) come from the slides and the transcript, and there is no counterpart for them in `session2.ipynb`. The two-dimensional example of the notebook goes directly to the honeycomb lattice of Section [2.11](#sec-2-11) and does not treat the plain square lattice, and there is no section on the three-dimensional cubic lattice. If you want to check [(2.14)](#eq-2-14) or [(2.15)](#eq-2-15) numerically, the same construction that we use for the honeycomb lattice in the box below can be extended directly, with a square or cubic Bravais lattice with a single orbital instead.

[](#sch:s02:square_bands) shows the band of [(2.14)](#eq-2-14).

![The band of the square lattice from [(2.14)](#eq-2-14). On the left, the energy along the path from $\Gamma$ to $X$ to $M$ and back, which goes from $-4t$ to $4t$. On the right, the contour lines of the same band over the Brillouin zone, with the line $\epsilon=0$ in red. The contours continue across the dashed border, so the zone is a torus.](figures/web/session02/square_bands.svg){#sch:s02:square_bands alt="The energy of the square lattice along a path of the Brillouin zone, and its contour lines over the zone."}

::: quiz
What is the width of the band of the cubic lattice in [(2.15)](#eq-2-15), from the lowest to the highest energy?

- [ ] $4t$
- [ ] $8t$
- [x] $12t$
- [ ] $6t$

The lowest energy is at $\varphi_x=\varphi_y=\varphi_z=0$, where all three cosines are $1$ and the energy is $-6t$. The highest is at $\pi$ in every direction, which gives $+6t$, so the width is $12t$.
:::

::: quiz
We switch off the hopping along $y$ in the square lattice. What does the energy depend on?

- [x] Only on $\varphi_x$, so the band is flat along $\varphi_y$.
- [ ] Only on $\varphi_y$.
- [ ] On $\varphi_x+\varphi_y$.
- [ ] It does not depend on either.

Without hopping along $y$ the lattice is a set of decoupled chains. Each chain has the band of [(2.8)](#eq-2-8), and nothing depends on $\varphi_y$.
:::

Before we continue, let us say explicitly that everything above applies far beyond electrons. The same Bloch-Hamiltonian method diagonalizes phonon bands, magnon bands and the bands of Bogoliubov-de Gennes quasiparticles in a superconductor. It applies in the same way to artificial lattices that are engineered and have no relation to real crystals, such as cold atoms trapped in optical lattices. We will focus on electronic bands for concreteness, but this generality is the reason why the same method appears again for magnons, and for Bogoliubov quasiparticles, later in the course. The physics that single-particle band theory gives in this way is very rich. It includes Dirac fermions with zero Dirac mass, Weyl semimetals, which are Dirac points generalized to higher dimensions, quantum spin Hall insulators, Chern insulators, crystalline topological phases and topological superconductors. All of this is built only on the Bloch Hamiltonian $H(\mathbf{k})$ that we constructed here.

::: {.tryit notebook="session2.ipynb" cell="Infinite two-dimensional graphene"}
In the cell of the band structure, replace the honeycomb lattice by `geometry.square_lattice()`. Check that the band goes from $-4t$ to $4t$, which is the range of [(2.14)](#eq-2-14). The notebook uses the opposite sign of the hopping, so the two extremes are exchanged.
:::
