## The Landau gauge and the symmetric gauge {#sec-4-8 number="4.8"}

For a uniform field $\mathbf{B} = B\hat{z}$, there are two gauges that will be important for us.

- The **Landau gauge**, $\mathbf{A} = (0, Bx, 0)$, puts all the spatial dependence into one coordinate, $x$. Since $\mathbf{A}$ does not depend on $y$, the Hamiltonian built from it still commutes with $p_y$, so translations along $y$ are still a good symmetry, but it does not commute with $p_x$. This gauge keeps *one* translational symmetry, which is what we need to have a band structure at all, and it is the gauge that we use in every ribbon calculation in this session.

- The **symmetric gauge**, $\mathbf{A} = \tfrac{B}{2}(-y, x, 0)$, breaks both translational symmetries but keeps the rotational symmetry of the system instead. It is the natural gauge to write many-body wavefunctions with a good angular momentum, which is what we need when we arrive at the fractional quantum Hall state, from Section [4.13](#sec-4-13) on.

Figure [4.2](#fig:s04:gauge) shows the difference in a concrete way, by writing both gauges as Peierls phases [(4.4)](#eq-4-4) on a square lattice. The phases of the single bonds are completely different in the two gauges, but the sum around any plaquette is the same flux in both. This sum is the only gauge-invariant combination, and it is the only thing that the electrons respond to.

![Two gauges for the same magnetic field, written as Peierls phases [(4.4)](#eq-4-4) on a square lattice, with a dial on every bond whose needle points at the angle of its phase, drawn for $\varphi=\pi/4$. (a) In the Landau gauge the horizontal bonds have no phase at all and the vertical bond in column $x$ has the phase $x\varphi$. The phase pattern depends on $x$ but not on $y$, so translations along $y$ are still an exact symmetry and a band structure in $k_y$ still exists. (b) In the symmetric gauge every bond has a phase and none of them is the same as in (a), so no translation survives. The pattern is instead invariant under rotation about the centre of the plaquette. There is no physical difference between the two. When we go once around any plaquette, such as the shaded one, the phases of the single bonds add up to the same $\varphi$, which is the flux through that plaquette. The bond phases are a choice of gauge and the loop sum is not, and the electrons respond only to the loop sum.](figures/s04f02_gauge.svg){#fig:s04:gauge number="4.2"}

::: quiz
In the Landau gauge $\mathbf{A}=(0,Bx,0)$, which momentum is a good quantum number and can label the eigenstates?

- [ ] Both $p_x$ and $p_y$.

    This is false. The term $(p_y-eBx)^2$ of the Hamiltonian contains $x$, so $[p_x,H]\neq0$. The eigenstates are Gaussians in $x$ and not plane waves.

- [ ] Neither of them.

    This is false. The Hamiltonian does not depend on $y$, so $[H,p_y]=0$. The eigenstates can be chosen as $e^{ik_yy}$ times a function of $x$.

- [x] $p_y$.

    This is true. The vector potential does not depend on $y$, so $[H,p_y]=0$. It depends on $x$, so $p_x$ does not commute with $H$.

:::

::: quiz
Why is the Landau gauge the natural choice for the band structure of a ribbon, and not the symmetric gauge?

- [ ] The Landau gauge gives a different physical field.

    This is false. Both gauges have the same curl. For $\mathbf{A}=(0,Bx,0)$ and for $\mathbf{A}=(-By,Bx,0)/2$ we get $\nabla\times\mathbf{A}=B\hat z$.

- [x] The symmetric gauge breaks both translations, so there is no momentum along the ribbon and no band structure.

    This is true. The physics is the same in both gauges. The Landau gauge keeps the translation along the ribbon, which is what we need to plot energy against momentum.

- [ ] The symmetric gauge has no flux through the plaquettes.

    This is false. The flux through a plaquette of area $a^2$ is $Ba^2$ in both gauges, since it is gauge invariant. Only the way it is written in the bond phases differs.

:::

::: comesback
- In Section [4.13](#sec-4-13) the symmetric gauge gives holomorphic wavefunctions for the lowest Landau level.
- In Section [8.10](#sec-8-10) the mean-field bonds of a spin liquid have a gauge redundancy of their own, and again only the product around a plaquette is physical.
- In Section [5.2](#sec-5-2) a superconductor breaks the gauge symmetry, and the flux through a ring is quantized in units of $h/2e$.
:::
