## Majorana bound states and how to split an electron into two Majoranas {#sec-5-15 number="5.15"}

A **Majorana fermion** is defined algebraically by the condition that its field operator is equal to its own Hermitian conjugate,

$$\gamma^\dagger = \gamma, \tag{5.16}$$

which means that the creation and the annihilation of the quasiparticle are the same operation, so the particle is its own antiparticle. At first this seems to have no place in an ordinary material, since an ordinary electron is clearly not its own antiparticle ($c^\dagger \ne c$), and a semiconductor, for example, never hosts anything of this kind.

However, there is a purely algebraic fact that makes it possible. *Any* ordinary fermionic operator can be written as a combination of two Hermitian Majorana operators that anticommute with each other,

$$\gamma_A = c + c^\dagger, \qquad \gamma_B = -i\left(c - c^\dagger\right), \tag{5.17}$$

so that $\gamma_A^\dagger = \gamma_A$, $\gamma_B^\dagger = \gamma_B$, $\{\gamma_A,\gamma_B\}=0$ and $\gamma_A^2=\gamma_B^2=1$, where we used $\{c,c^\dagger\}=1$. If we invert [(5.17)](#eq-5-17), we obtain

$$c = \frac{1}{2}\left(\gamma_A + i\gamma_B\right), \qquad c^\dagger = \frac{1}{2}\left(\gamma_A - i\gamma_B\right). \tag{5.18}$$

At first this is only a change of variables, a mathematical trick without new physics. Every electron is *always* made of two Majorana operators that are tightly bound together into an ordinary fermion, and normally there is no way to observe $\gamma_A$ or $\gamma_B$ separately, only their fixed combination $c$. Superconductors are special because BdG eigenstates are already mixtures of electrons and holes by construction, since the Nambu spinor of section [5.8](#sec-5-8) explicitly combines $c_{\mathbf k\sigma}$ with $c_{-\mathbf k\sigma'}^\dagger$. So a superconductor is the kind of system where, with the right pairing symmetry and the right geometry, the two Majorana components of an electron can become spatially *separated*, or deconfined, instead of staying together at one site. This deconfinement is the topic of the rest of this section.

![One electron mode and its two Majorana halves. At the top the mode is $\tfrac12(\gamma_A+i\gamma_B)$, and the halves are bound at one site. At the bottom the halves are bound between neighboring sites, and then one half at each end of the chain stays free, which the stars mark.](figures/web/session05/majorana_halves.svg){#sch:s05:majorana_halves alt="At the top, one electron drawn as a single circle and then as two bound circles. At the bottom, four sites with halves bound across neighboring sites and one free half at each end."}

::: quiz
Which statement about the operators $\gamma_A=c+c^\dagger$ and $\gamma_B=-i(c-c^\dagger)$ of [(5.17)](#eq-5-17) is correct?

- [x] Each one squares to one, and the two anticommute.
- [ ] Each one squares to zero, as the fermion $c$ does.
- [ ] They are not Hermitian, since $c$ is not Hermitian.
- [ ] They commute, since both are built from the same $c$.

Both are Hermitian, and $\{c,c^\dagger\}=1$ gives $\gamma_A^2=\gamma_B^2=1$ and $\{\gamma_A,\gamma_B\}=0$. A fermion obeys $c^2=0$ instead.
:::

::: quiz
The electron mode is empty. What is the value of $i\gamma_A\gamma_B$?

- [x] $-1$
- [ ] $+1$
- [ ] $0$
- [ ] $i$

Inserting [(5.17)](#eq-5-17) gives $i\gamma_A\gamma_B=2c^\dagger c-1$. The empty mode has $c^\dagger c=0$, so the value is $-1$, and the filled mode gives $+1$. The product of the two halves measures the occupation of the mode.
:::

::: {.tryit notebook="session5.ipynb" cell="Majorana modes in a spin triplet superconductor"}
In the cell, the density of states is computed on the site `0`, on `L//10` and on `L//2`. The peak at zero energy is large on the end site, small at `L//10` and negligible in the middle. It is the half of a split electron that sits at that end.
:::
