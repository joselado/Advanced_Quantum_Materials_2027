## The meaning of the phase, which is the quasi-momentum {#sec-2-6 number="2.6"}

Let us stop here and ask what the phase $\varphi$ in [(2.2)](#eq-2-2) means physically, and not only formally. We go back to the Schrödinger equation in the continuum and ask how a wavefunction translated by the lattice constant $a$, $\psi(x+a)$, is related to $\psi(x)$. A Taylor expansion gives

$$\psi(x+a) = \psi(x) + a\,\partial_x\psi(x) + \frac{a^2}{2}\partial_x^2\psi(x) + \cdots
= e^{a\partial_x}\psi(x) = e^{\frac{i}{\hbar}ap}\,\psi(x),$$

where $p=-i\hbar\partial_x$ is the momentum operator. If $\psi$ is an eigenstate of the translation operator with eigenvalue $e^{i\varphi}$, when we compare the two expressions we find

$$\varphi = \frac{a\,p}{\hbar} = k\,a, \tag{2.10}$$

meaning that the symmetry eigenvalue is directly the crystal momentum $k=p/\hbar$ times the lattice constant. This is the reason why $\varphi$ is called the *quasi-momentum*. It is directly related to the momentum operator of the original Schrödinger equation, only measured in units where the lattice constant is absorbed, and it takes values in $\varphi\in(-\pi,\pi]$, which is the first Brillouin zone. From Session 3 on we take $a=1$, and we write the quasi-momentum as $k$.

![The allowed phases of the ring, shown again. The balls fill the circle as the ring grows, and the circle is the range $\varphi\in(-\pi,\pi]$ of the quasi-momentum.](figures/s02f01_ringmodes.svg){alt="Rings with three sites, and phase circles with balls at the allowed phases for three and five sites."}

The reason why $\varphi$ is defined only up to $2\pi$ can be seen directly on the sites of the chain, as we will now see in [](#sch:s02:aliasing).

![Two waves with $k=0.5/a$ and $k+2\pi/a$, for $a=1$. They take the same value on every site, which are the dots, so on the lattice they are one state. The wave with the larger $k$ oscillates between the sites, where there are no atoms.](figures/web/session02/aliasing.svg){#sch:s02:aliasing alt="A slow cosine and a fast cosine that pass through the same dots at the integer positions of the chain."}

::: quiz
A wave $e^{ikx}$ is sampled on the sites $x=na$. How do the eigenvalues of the translation $T$ compare for $k$ and for $k+2\pi/a$?

- [x] They are equal, since $\varphi=ka$ changes by $2\pi$.

    This is true. The eigenvalue is $e^{i\varphi}$ with $\varphi=ka$. A shift of $k$ by $2\pi/a$ changes $\varphi$ by $2\pi$, which does not change the eigenvalue. This is why we keep only one Brillouin zone.

- [ ] They differ by a sign.

    This is false. Take $a=1$ and $k=0.5$. Then $e^{i0.5}$ and $e^{i(0.5+2\pi)}$ are the same number. A sign would come from a shift of $k$ by $\pi/a$.

- [ ] They differ, and only one of the two values is allowed.

    This is false. On the sites $x=na$ the two waves are the same vector, since $e^{2\pi i n}=1$. There are not two different states, so there is nothing to forbid.

Two values of $k$ that differ by $2\pi/a$ describe the same state on the lattice.
:::

This identification also tells us where the orthogonal basis with one orbital per site comes from, which we have used so far without saying it. The atomic orbitals of a real material, $s$, $p$, $d$, and so on, are not orthogonal between neighboring sites. Before we write a clean tight-binding Hamiltonian, we first go to an orthogonal local basis with one orbital per site, which we obtain in a systematic way with what is called **Löwdin orthogonalization**. Here we only assume this construction. A basis of this kind is also called a basis of Wannier states. In this basis, symmetry alone already tells us that the eigenstates have the form $e^{in\varphi}c_n^\dagger|0\rangle$, which is the ansatz [(2.6)](#eq-2-6). This is true for a finite ring of $7$ sites, for $11$ sites, and for the infinite chain that we want in order to describe a solid. We can build the same intuition by working with finite rings that become larger and larger, before we take the limit $L\to\infty$.

::: quiz
We describe the same chain with a lattice constant $2a$ instead of $a$. What happens to the range of $k$ in the first Brillouin zone?

- [x] It becomes half as wide.

    This is true. The range is $(-\pi/a',\pi/a']$ with $a'=2a$, which is half as wide. The bands then fold into the smaller zone, as we will see in the next section.

- [ ] It becomes twice as wide.

    This is false. For $a=1$ the zone has the width $2\pi$, and for $a'=2$ it is $(-\pi/2,\pi/2]$, with the width $\pi$. A longer cell gives a narrower zone.

- [ ] It does not change.

    This is false. A ring of $100$ sites has $100$ values of $k$ in the zone of $a$, and only $50$ values in the zone of $2a$. The same number of states must fit in a smaller zone, so the range changed.

A longer unit cell in real space means a smaller zone in reciprocal space.
:::

::: comesback
- In Section [2.8](#sec-2-8) the Brillouin zone of a two-dimensional lattice is a torus, and Section [3.5](#sec-3-5) uses this to make the Chern number an integer.
- From Session 3 on the quasi-momentum is written $k$, as in the Bloch Hamiltonian of the SSH model in Section [3.9c](#sec-3-9c).
:::
