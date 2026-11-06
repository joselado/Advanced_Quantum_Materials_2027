## Majorana bound states and how to split an electron into two Majoranas {#sec-5-15 number="5.15"}

A **Majorana fermion** is defined algebraically by the condition that its field operator is equal to its own Hermitian conjugate,

$$\gamma^\dagger = \gamma, \tag{5.16}$$

which means that the creation and the annihilation of the quasiparticle are the same operation, so the particle is its own antiparticle. At first this seems to have no place in an ordinary material, since an ordinary electron is clearly not its own antiparticle ($c^\dagger \ne c$), and a semiconductor, for example, never hosts anything of this kind.

However, there is a purely algebraic fact that makes it possible. *Any* ordinary fermionic operator can be written as a combination of two Hermitian Majorana operators that anticommute with each other,

$$\gamma_A = c + c^\dagger, \qquad \gamma_B = -i\left(c - c^\dagger\right), \tag{5.17}$$

so that $\gamma_A^\dagger = \gamma_A$, $\gamma_B^\dagger = \gamma_B$, $\{\gamma_A,\gamma_B\}=0$ and $\gamma_A^2=\gamma_B^2=1$, where we used $\{c,c^\dagger\}=1$. If we invert [(5.17)](#eq-5-17), we obtain

$$c = \frac{1}{2}\left(\gamma_A + i\gamma_B\right), \qquad c^\dagger = \frac{1}{2}\left(\gamma_A - i\gamma_B\right). \tag{5.18}$$

At first this is only a change of variables, a mathematical trick without new physics. Every electron is *always* made of two Majorana operators that are tightly bound together into an ordinary fermion, and normally there is no way to observe $\gamma_A$ or $\gamma_B$ separately, only their fixed combination $c$. Superconductors are special because BdG eigenstates are already mixtures of electrons and holes by construction, since the Nambu spinor of section [5.8](#sec-5-8) explicitly combines $c_{\mathbf k\sigma}$ with $c_{-\mathbf k\sigma'}^\dagger$. So a superconductor is the kind of system where, with the right pairing symmetry and the right geometry, the two Majorana components of an electron can become spatially *separated*, or deconfined, instead of staying together at one site. This deconfinement is the topic of the rest of this section.
