## The meaning of the phase, which is the quasi-momentum {#sec-2-6 number="2.6"}

Let us stop here and ask what the phase $\varphi$ in [(2.2)](#eq-2-2) means physically, and not only formally. We go back to the Schrödinger equation in the continuum and ask how a wavefunction translated by the lattice constant $a$, $\psi(x+a)$, is related to $\psi(x)$. A Taylor expansion gives

$$\psi(x+a) = \psi(x) + a\,\partial_x\psi(x) + \frac{a^2}{2}\partial_x^2\psi(x) + \cdots
= e^{a\partial_x}\psi(x) = e^{\frac{i}{\hbar}ap}\,\psi(x),$$

where $p=-i\hbar\partial_x$ is the momentum operator. If $\psi$ is an eigenstate of the translation operator with eigenvalue $e^{i\varphi}$, when we compare the two expressions we find

$$\varphi = \frac{a\,p}{\hbar} = k\,a, \tag{2.10}$$

meaning that the symmetry eigenvalue is directly the crystal momentum $k=p/\hbar$ times the lattice constant. This is the reason why $\varphi$ is called the *quasi-momentum*. It is directly related to the momentum operator of the original Schrödinger equation, only measured in units where the lattice constant is absorbed, and it takes values in $\varphi\in(-\pi,\pi]$, which is the first Brillouin zone.

This identification also tells us where the orthogonal basis with one orbital per site comes from, which we have used so far without saying it. The atomic orbitals of a real material, $s$, $p$, $d$, and so on, are not orthogonal between neighbouring sites. Before we write a clean tight-binding Hamiltonian, we first go to an orthogonal local basis with one orbital per site, which we obtain in a systematic way with what is called **Löwdin orthogonalization**. The contact session works this construction out properly, and here we only assume it, and the slides also call this basis "Wannier states". In this basis, symmetry alone already tells us that the eigenstates have the form $e^{in\varphi}c_n^\dagger|0\rangle$, which is the ansatz [(2.6)](#eq-2-6). This is true for a finite ring of $7$ sites, for $11$ sites, and for the infinite chain that we want in order to describe a solid. We can build the same intuition by working with finite rings that become larger and larger, before we take the limit $L\to\infty$.
