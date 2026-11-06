## The Hubbard model and mean-field magnetism, revisited {#sec-6-3 number="6.3"}

The minimal Hamiltonian for all of this is the one-dimensional Hubbard chain that we first saw in session 1,

$$H = -t\sum_{n,\sigma}\left(c_{n\sigma}^\dagger c_{n+1,\sigma} + \text{h.c.}\right) + U\sum_n c_{n\uparrow}^\dagger c_{n\uparrow}\, c_{n\downarrow}^\dagger c_{n\downarrow}, \tag{6.1}$$

which is the hopping $t$ plus a purely local onsite density-density interaction between opposite spins, called the Hubbard term. A negative $U$, which is attractive, gives rise to superconductivity, which was the topic of session 5. A positive $U$, which is repulsive, gives rise to magnetism, which is our topic in this session.

The mean-field decoupling is done in the same way as before. We replace $c_{n\uparrow}^\dagger c_{n\uparrow}$ and $c_{n\downarrow}^\dagger c_{n\downarrow}$ by their expectation values, and we obtain a bilinear Hamiltonian with onsite energies that depend on the spin. Nothing forces these two expectation values to be equal, and the difference between them is the magnetization,

$$m = \langle c_\uparrow^\dagger c_\uparrow\rangle - \langle c_\downarrow^\dagger c_\downarrow\rangle, \tag{6.2}$$

which plays the role of an exchange field. In a schematic form, the resulting mean-field Hamiltonian is $H_\text{MF} \sim -\tfrac{U}{2}\, m\, \boldsymbol\sigma\cdot c$, where $\boldsymbol\sigma$ is the vector of Pauli matrices. Self-consistency gives $m=0$ for $U<0$ and a magnetic solution with $m\neq 0$ for $U>0$, as in session 1.

There is a more careful point here, which the slides show but the spoken explanation only mentions. Nothing in this construction chooses the $z$ axis. For a single site, the Hubbard interaction can be rewritten exactly in terms of the local spin operator $\mathbf{S} = \tfrac12 c_\alpha^\dagger \boldsymbol\sigma_{\alpha\beta} c_\beta$ and the total occupation $n = n_\uparrow + n_\downarrow$, as $U\, n_\uparrow n_\downarrow = \tfrac{U}{2}n - \tfrac{2U}{3}\mathbf{S}^2$, where we used that a single site has $\mathbf{S}^2=\tfrac34(n-2n_\uparrow n_\downarrow)$, since only a singly occupied site has a spin. Mean-field theory then factorizes the quadratic operator $\mathbf{S}^2$ in the same way as any product of two operators, $\mathbf{S}^2 \approx
2\langle\mathbf{S}\rangle\cdot\mathbf{S} - \langle\mathbf{S}\rangle^2$, and the resulting exchange field points along $\mathbf{m} \equiv \langle\mathbf{S}\rangle$, in *any* direction where this expectation value is nonzero. If we choose $\langle c_\uparrow^\dagger c_\uparrow\rangle \neq
\langle c_\downarrow^\dagger c_\downarrow\rangle$, as in [(6.2)](#eq-6-2), we select $m_z\neq 0$. If we choose instead $\langle c_\uparrow^\dagger c_\downarrow\rangle \neq 0$, we select $m_x$ or $m_y$. For this reason mean-field magnetism is not restricted to the $z$ axis. It gives magnets with a magnetization along any direction in space, and this includes noncollinear arrangements where $\mathbf{m}$ points in different directions on different sites. This is the "non-collinear mean-field Hamiltonian" figure on the slides, which the spoken lecture only names briefly.

Mean field can only be trusted when $U \ll t$. We will see in Section [6.6](#sec-6-6) that magnetism usually needs the opposite regime, and this is the reason why the strongly localized limit, from Section [6.7](#sec-6-7) on, is so important.
