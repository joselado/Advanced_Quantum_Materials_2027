## From the Kubo formula to the Chern number, briefly {#sec-4-3 number="4.3"}

We derived this result in full in the last session, so we will not repeat fifteen lines of algebra that would look almost the same. Instead, let us recall the logic and check that it applies here without changes. The Kubo formula is linear response, so it is first order in the applied field, and its sum over states has the form of a second-order perturbation expression. It writes the transverse conductivity as a sum over all pairs of occupied and empty bands, where each term has matrix elements of $\partial H/\partial k_x$ and $\partial H/\partial k_y$ divided by energy differences. There is an identity that relates $\partial H/\partial k$ to the derivative of the eigenstates, which we obtain when we differentiate the eigenvalue equation $H(\mathbf{k})|u_\mathbf{k}\rangle = \varepsilon(\mathbf{k})|u_\mathbf{k}\rangle$ with respect to $\mathbf{k}$. With this identity every explicit energy denominator cancels, and the result depends only on the wavefunctions, through the Berry connection $\mathbf{A}(\mathbf{k}) = i\langle
u_\mathbf{k}|\nabla_\mathbf{k}|u_\mathbf{k}\rangle$ and its curl, the Berry curvature $\Omega(\mathbf{k}) = \nabla_\mathbf{k}\times\mathbf{A}(\mathbf{k})$. The Brillouin zone is a closed, compact manifold, which is a torus, and when we sum over occupied bands and integrate over it we obtain an integer,

$$\sigma_{xy} = \frac{e^2}{h}\, C, \qquad C = \frac{1}{2\pi}\sum_{n\,\text{occ.}}\int_{\text{BZ}} \Omega_n(\mathbf{k})\, d^2k \in \mathbb{Z}, \tag{4.1}$$

which is the Chern number of the occupied bands. This is the same statement as in session 3. The Hall conductance is not only quantized, it is also a topological invariant, so it does not change under any smooth deformation of the Hamiltonian that does not close the bulk gap. What is new in this session is not this derivation. It is the specific band structure that we will use in it, which is the set of Landau levels of a magnetic field, and everything that follows when we ask how the many-body ground state of a *partially filled* Landau level looks.

## Landau levels as Chern-number-one flat bands {#sec-4-4 number="4.4"}

A two-dimensional electron gas in a perpendicular magnetic field develops a set of completely flat bands, the Landau levels, with index $n=0,1,2,\dots$. In this context "flat" means without dispersion, so the energy does not depend on momentum at all, and we will derive the reason for this in Section [4.9](#sec-4-9). Even if they have no dispersion, each Landau level has a finite Chern number, which is also the smallest nonzero value, $C=1$. If the chemical potential is between the $N$-th and the $(N+1)$-th Landau level, the total Chern number of the occupied bands is the sum of $N$ contributions equal to $1$,

$$C_{\text{tot}} = \sum_{n=0}^{N-1} C_n = N \quad\Longrightarrow\quad \sigma_{xy} = N\,\frac{e^2}{h}, \tag{4.2}$$

which is an integer that counts the number of filled Landau levels. This is the integer quantum Hall effect. It is a state built only from flat bands without dispersion, and still its Hall conductance is an exact integer multiple of $e^2/h$, with a sharp quantization.

![The reason why a Landau level is flat, used here to read its Chern number. Every guiding center $x_0=\hbar k_y/B$ has the same oscillator well, and so the same energy. Look at panel (b), where the bands do not depend on $k_y$ at all. A flat band has no group velocity and still has $C=1$, since the Chern number depends only on the wavefunctions.](figures/s04f03_guidingcenter.svg){alt="Harmonic wells with the same ladder of levels at different positions, and flat bands as a function of the momentum."}

::: quiz
Landau levels have no dispersion, so the group velocity of every state is zero. How can such a band have the Chern number $C=1$?

- [ ] The Chern number comes from the edge states and not from the bulk band.
- [x] The Chern number is built from the wavefunctions across the Brillouin zone, and it does not depend on the energies.
- [ ] It cannot, and the Chern number of a Landau level is zero.
- [ ] The Chern number of a flat band is $1$ only at zero temperature.

The energies cancel in [(4.1)](#eq-4-1), as we saw in session 3. A flat band can still have wavefunctions that twist across the Brillouin zone, and this twist is counted by $C$.
:::

::: quiz
The chemical potential is in the gap between the third and the fourth Landau level. What is $\sigma_{xy}$?

- [x] $3e^2/h$.
- [ ] $e^2/h$.
- [ ] $3.5\,e^2/h$.
- [ ] $4e^2/h$.

Three Landau levels are filled, each with $C=1$. By [(4.2)](#eq-4-2) the total is $C=3$, and $\sigma_{xy}=3e^2/h$ is an exact integer multiple.
:::

::: {.tryit notebook="session4.ipynb" cell="Landau levels of conventional electrons"}
Run the cell for the three fields. The dots of the bulk bands form horizontal lines, which means that the Landau levels have no dispersion. The lines move apart when you increase `B`, as expected from the growth of the cyclotron energy with the field.
:::
