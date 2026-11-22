## The general pairing Hamiltonian and its symmetry classification {#sec-5-11 number="5.11"}

Up to now $\Delta$ has been a single number. If it depends on momentum and on spin, which combinations does Fermi statistics allow, and what sorts them? We will now see that the exchange of the two electrons of a pair gives one antisymmetry [(5.11)](#eq-5-11) for every pairing. From it follows the rule [(5.12)](#eq-5-12), meaning that a spin singlet is even in $\mathbf k$ and a spin triplet is odd in $\mathbf k$.

::: {.recall eq="5.4"}
This is the mean-field Hamiltonian of the attractive chain of Section [5.5](#sec-5-5). Its pairing term creates an $\uparrow$ and a $\downarrow$ electron on the same site $n$ with the amplitude $\Delta_n$, and in a uniform superconductor $\Delta_n=\Delta$ is the same number on every site. This onsite pairing is the simplest case of the classification of this page.
:::

In general the pairing order can depend on momentum and have a spin structure, $\Delta_{\mathbf k,\sigma_1\sigma_2}$ with $\sigma_1,\sigma_2 \in
\{\uparrow,\downarrow\}$. We can write it in a compact way as the $2\times 2$ pairing matrix $\Delta_{\mathbf
k} = \begin{pmatrix}\Delta_{\mathbf k,\uparrow\uparrow} & \Delta_{\mathbf k,\uparrow\downarrow}\\
\Delta_{\mathbf k,\downarrow\uparrow} & \Delta_{\mathbf k,\downarrow\downarrow}\end{pmatrix}$, and it is built from a general mean-field Hamiltonian

$$H_{\text{pair}} = -\frac{1}{2}\sum_{\mathbf k}{}^{\prime}\, \sum_{\sigma_1\sigma_2} \left[\Delta_{\mathbf k,\sigma_1\sigma_2}\, c_{\mathbf k\sigma_1}^\dagger c_{-\mathbf k\sigma_2}^\dagger + \Delta_{\mathbf k,\sigma_1\sigma_2}^*\, c_{-\mathbf k\sigma_2} c_{\mathbf k\sigma_1}\right]. \tag{5.10}$$

We use [(5.10)](#eq-5-10) only for its symmetry, since its overall sign is the opposite of the one of [(5.4)](#eq-5-4). The real-space and reciprocal-space pictures of $\Delta$ are related by a Fourier transform. So we can also think of this order in terms of the pair wave function, as a function of the distance between the two paired electrons. The key step is to classify superconducting order only by the *symmetry* of $\Delta_{\sigma\sigma'}(\mathbf k)$. This symmetry alone controls how the superconductor responds to perturbations, such as disorder or magnetic fields, independently of the microscopic details.

Fermionic antisymmetry, which comes from the fact that the operators $c_{\mathbf k\sigma}^\dagger
c_{-\mathbf k\sigma'}^\dagger$ anticommute, imposes

$$\Delta_{\sigma\sigma'}(\mathbf k) = -\Delta_{\sigma'\sigma}(-\mathbf k), \tag{5.11}$$

which is a minus sign under the *combined* operation of exchanging the spin indices and sending $\mathbf k \to
-\mathbf k$. This combined statement holds for any type of pairing. The classification that has a physical meaning comes from splitting $\Delta_{\sigma\sigma'}(\mathbf k)$ into a part that is symmetric and a part that is antisymmetric under spin exchange alone. Because of [(5.11)](#eq-5-11), this is the same as splitting it by its parity under $\mathbf k \to -\mathbf k$ alone.

::: key
Fermi statistics allows two kinds of pairing,

$$\textbf{Spin singlet (even parity):} \quad \Delta(\mathbf k) = \Delta(-\mathbf k), \qquad \Delta_{\sigma\sigma'} = -\Delta_{\sigma'\sigma}\ \text{(spin-antisymmetric)},$$

$$\textbf{Spin triplet (odd parity):} \quad \Delta(\mathbf k) = -\Delta(-\mathbf k), \qquad \Delta_{\sigma\sigma'} = +\Delta_{\sigma'\sigma}\ \text{(spin-symmetric)}. \tag{5.12}$$

Both lines come from the antisymmetry [(5.11)](#eq-5-11) of every pairing. A pair that is antisymmetric in spin has to be even in $\mathbf k$, and a pair that is symmetric in spin has to be odd in $\mathbf k$.
:::

::: {.steps title="From the anticommutation of the operators to (5.11) and (5.12)"}
Let us start with the simplest case, a single spin species, so that only $\Delta_{\mathbf k,\uparrow\uparrow}$ is there, and let us take the sum over all the momenta of the zone. We relabel $\mathbf k\to-\mathbf k$ in the sum, which does not change it, and then we exchange the two operators, which gives a minus sign,

$$\sum_{\mathbf k}\Delta_{\mathbf k,\uparrow\uparrow}\,c_{\mathbf k\uparrow}^\dagger c_{-\mathbf k\uparrow}^\dagger
= \sum_{\mathbf k}\Delta_{-\mathbf k,\uparrow\uparrow}\,c_{-\mathbf k\uparrow}^\dagger c_{\mathbf k\uparrow}^\dagger
= -\sum_{\mathbf k}\Delta_{-\mathbf k,\uparrow\uparrow}\,c_{\mathbf k\uparrow}^\dagger c_{-\mathbf k\uparrow}^\dagger.$$

So the operator does not change when we replace $\Delta_{\mathbf k,\uparrow\uparrow}$ by its odd part $\tfrac12(\Delta_{\mathbf k,\uparrow\uparrow}-\Delta_{-\mathbf k,\uparrow\uparrow})$, and its even part gives zero, meaning that a pairing of two equal spins is always odd in $\mathbf k$.

With two spins we relabel $\mathbf k\to-\mathbf k$ and exchange the names $\sigma_1$ and $\sigma_2$ of the two spin indices at the same time. The same two steps give

$$\sum_{\mathbf k,\sigma_1\sigma_2}\Delta_{\mathbf k,\sigma_1\sigma_2}\,c_{\mathbf k\sigma_1}^\dagger c_{-\mathbf k\sigma_2}^\dagger
= -\sum_{\mathbf k,\sigma_1\sigma_2}\Delta_{-\mathbf k,\sigma_2\sigma_1}\,c_{\mathbf k\sigma_1}^\dagger c_{-\mathbf k\sigma_2}^\dagger,$$

so only the part $\tfrac12(\Delta_{\mathbf k,\sigma_1\sigma_2}-\Delta_{-\mathbf k,\sigma_2\sigma_1})$ enters the Hamiltonian, and we can always take $\Delta$ equal to it. This is [(5.11)](#eq-5-11). We used only the anticommutation, and not the sign or the factor $\tfrac12$ in front of [(5.10)](#eq-5-10), so the antisymmetry holds for any normalization of the pairing.

The last step is [(5.12)](#eq-5-12). We split $\Delta_{\sigma\sigma'}(\mathbf k)=A_{\sigma\sigma'}(\mathbf k)+S_{\sigma\sigma'}(\mathbf k)$, with $A_{\sigma'\sigma}=-A_{\sigma\sigma'}$ and $S_{\sigma'\sigma}=S_{\sigma\sigma'}$. The operation of [(5.11)](#eq-5-11) keeps each part in its class, so each part satisfies it alone. For the antisymmetric part this gives $A_{\sigma\sigma'}(\mathbf k)=-A_{\sigma'\sigma}(-\mathbf k)=A_{\sigma\sigma'}(-\mathbf k)$, which is even, and for the symmetric part $S_{\sigma\sigma'}(\mathbf k)=-S_{\sigma'\sigma}(-\mathbf k)=-S_{\sigma\sigma'}(-\mathbf k)$, which is odd. The antisymmetric spin part is the singlet, and the symmetric one is the triplet.
:::

![The pair amplitude $\Delta(r)$ of a chain, as a function of the distance $r$ between the two paired electrons. It is the Fourier transform of the $\Delta(k)$ written above each panel, computed on a ring of 64 sites, with $r$ in units of the lattice constant and $\Delta(r)$ in units of $\Delta_0$. An even $\Delta(k)$ gives a pair amplitude that is even in $r$. The odd $p$-wave pairing, the one of [(5.20)](#eq-5-20), gives an odd pair amplitude. This one is zero at $r=0$, so the two electrons never sit on the same site, as Pauli exclusion requires for a spin-symmetric pair.](figures/web/session05/pair_function.svg){#sch:s05:pair_function alt="Three stem plots of the pair amplitude in units of Delta zero against the distance r. Onsite s-wave has one stem of height one at r equal to zero, extended s-wave has two equal stems at r equal to plus and minus one, and p-wave has two stems of opposite sign at plus and minus one."}

For concreteness, onsite s-wave pairing, with $\Delta(\mathbf k) = \Delta$ constant, which comes from a local attractive interaction as in Section [5.5](#sec-5-5), is even in $\mathbf k$, and so it is spin-singlet.

This symmetry classification has a direct physical consequence. A spin-singlet superconductor whose gap has one sign on the whole Fermi surface is essentially insensitive to non-magnetic disorder, which is called Anderson's theorem. The reason is that the pair wave function only depends on time-reversed partners, and non-magnetic disorder preserves them. A spin-triplet superconductor, on the other hand, is strongly suppressed even by weak non-magnetic disorder, because scattering mixes the different momentum directions between which the order parameter needs to keep coherent phase relations. This is the reason why spin-singlet s-wave superconductors are much more common in nature than spin-triplet ones. Essentially every real material has some level of non-magnetic disorder, and this disorder suppresses the triplet channel and the singlets that change sign, such as d-wave, and leaves the s-wave singlet intact.

![The sign structure of $\Delta(\mathbf k)$ for several orders. A half turn of a panel sends $\mathbf k\to-\mathbf k$, so panels that keep their signs have even parity and panels that flip them have odd parity, as in [(5.12)](#eq-5-12).](figures/s05f03_gapsymmetry.svg){alt="Several panels of the sign of the pairing function over the Brillouin zone, with positive regions raised and negative regions sunk."}

::: quiz
A pairing function is $\Delta(\mathbf k)=\Delta_0\sin k_x$, which is odd in $\mathbf k$. What does [(5.11)](#eq-5-11) require of its spin part?

- [ ] It has to be antisymmetric, which is a spin singlet.

    This is false. Take $\sum_k\sin k_x\,(c_{k\uparrow}c_{-k\downarrow}-c_{k\downarrow}c_{-k\uparrow})$. Relabeling $k\to-k$ in the second term shows that it cancels the first, so this singlet term is exactly zero.

- [x] It has to be symmetric, which is a spin triplet.

    This is true. The condition [(5.11)](#eq-5-11) needs the total function to change sign. Since $\sin k_x$ is already odd, the spin part has to be even, which is the triplet of [(5.12)](#eq-5-12).

- [ ] Nothing, since the spin part is independent of $\mathbf k$.

    This is false. Take a constant $\Delta_0$, which is even in $\mathbf k$. The triplet combination $\sum_k(c_{k\uparrow}c_{-k\downarrow}+c_{k\downarrow}c_{-k\uparrow})$ is exactly zero, so the spin part is fixed by the parity in $\mathbf k$.
:::

::: quiz
Each plot shows the pair amplitude $\Delta(r)$ of a chain, in units of $\Delta_0$. Here $r$ is the distance between the two paired electrons. Which pairing must be a spin triplet?

- [ ] ![Stems of the pair amplitude against r, with one stem of height one at r equal to zero and nothing at the other distances.](figures/web/session05/g3_quiz_pair_onsite.svg)

    This is false. A single stem at $r=0$ is even, $\Delta(-r)=\Delta(r)$, and its Fourier transform is the constant $\Delta_0$, which is even in $k$. Two electrons on the same site must have opposite spins, and this is the onsite singlet of the attractive chain.

- [ ] ![Stems of the pair amplitude against r, with two stems of the same height one at r equal to minus one and plus one.](figures/web/session05/g3_quiz_pair_ext.svg)

    This is false. The two stems are equal, so $\Delta(-r)=\Delta(r)$, and the Fourier transform is $2\Delta_0\cos k$, which is even in $k$. An even pairing is a spin singlet, the extended $s$-wave of the chain.

- [x] ![Stems of the pair amplitude against r, with two stems of opposite sign at r equal to minus one and plus one and nothing at r equal to zero.](figures/web/session05/g3_quiz_pair_p.svg)

    This is true. Here $\Delta(-r)=-\Delta(r)$, so the Fourier transform is proportional to $\sin k$, which is odd in $k$. An odd pairing is a spin triplet, and the zero at $r=0$ is what Pauli exclusion asks for two equal spins.
:::

:::: problem
Show that the onsite term $c_{n\uparrow}c_{n\uparrow}$ vanishes. Then take the bond pairing of the $\uparrow$ electrons of a ring of $N$ sites, with $\Delta>0$,

$$H_\Delta = \Delta\sum_n\left(c_{n\uparrow}c_{n+1,\uparrow} + c_{n+1,\uparrow}^\dagger c_{n\uparrow}^\dagger\right),$$

and write it in momentum space as $\tfrac12\sum_k\big[f(k)\,c_{k\uparrow}^\dagger c_{-k\uparrow}^\dagger+\text{h.c.}\big]$. Show that $f(k)$ is odd in $k$ and that $|f(k)|=2\Delta|\sin k|$.

::: solution
The operators anticommute, so $\{c_{n\uparrow},c_{n\uparrow}\}=2c_{n\uparrow}c_{n\uparrow}=0$. The onsite term vanishes, and two electrons of the same spin cannot pair on one site.

For the bond we first write the creation part with an amplitude that is antisymmetric in the two sites,

$$\Delta\sum_n c_{n+1,\uparrow}^\dagger c_{n\uparrow}^\dagger = \frac12\sum_{a,b}A(a-b)\,c_{a\uparrow}^\dagger c_{b\uparrow}^\dagger, \qquad A(1)=\Delta,\quad A(-1)=-\Delta,$$

and $A(r)=0$ for the other distances. This $A(r)$ is odd in $r$, with two values of opposite sign at $r=\pm1$, which is the shape of the $p$-wave panel of the figure above. In the figure, which of the two stems is positive depends on the sign conventions of [(5.20)](#eq-5-20) and of the transform, while the odd shape does not. We go to momentum space with $c_n^\dagger=N^{-1/2}\sum_k e^{\mp ikn}c_k^\dagger$, since the sign of the transform is a convention. The sum over the positions sets the second momentum to $-k$, and what is left is $f(k)=\sum_rA(r)\,e^{\mp ikr}$, the Fourier transform of $A(r)$. Since $A(-r)=-A(r)$, $f(k)$ is odd in $k$. Only $r=\pm1$ enter, so for either sign of the transform

$$|f(k)| = \Delta\,|e^{ik}-e^{-ik}| = 2\Delta|\sin k|.$$

This is the modulus of $\Delta(k)$ in [(5.20)](#eq-5-20), and the spectrum [(5.9)](#eq-5-9) needs only this modulus. With the hopping $-t$ and the chemical potential $\mu$ of the same chain, the BdG levels are $\pm\sqrt{(2t\cos k+\mu)^2+4\Delta^2\sin^2k}$. The pairing vanishes at $k=0$ and $k=\pi$, as any odd pairing does, so the levels reach zero only when the band crosses the Fermi level at one of these two momenta, which is at $|\mu|=2t$.
:::
::::

::: comesback
- In Section [5.12](#sec-5-12) we build a spin-triplet superconductor on purpose, from a magnet and an attractive interaction.
- In Section [9.7](#sec-9-7) a non-magnetic impurity leaves the density of states of an $s$-wave superconductor almost the same, which is Anderson's theorem seen in a measurement, and a magnetic impurity does not.
:::
