## Linear response theory and how a measurement reads the wavefunctions {#sec-3-2 number="3.2"}

To see why a bulk band structure can have an invariant at all, we need a tool that connects the wavefunctions of a Hamiltonian to something that we can measure. This tool is linear response theory, and the idea behind it is very general. We perturb the system at a position $x$ and time $t$, and then we measure an observable, such as the charge, the current, the magnetization or the heat, at another position $x'$ and time $t'$. Linear response theory tells us that this measured response depends only on the electronic structure of the unperturbed material.

Before we specialize to the Hall conductivity, let us look at two examples. Let us put an impurity in a two-dimensional metal and look at how the electron density, or the local density of states, is modulated around it. Linear response theory shows that this modulation pattern, which is called the Friedel oscillation, directly contains the Fermi wavelength of the electron gas, and this is what scanning tunneling microscopy uses in practice. In a similar way, when we scatter neutrons on a magnetic material, the magnetic moment of the neutron couples to the local moments in the sample. The resulting scattering pattern gives both the magnetic structure and its excitations, in particular magnons, which we build in Section [6.13](#sec-6-13). It is useful to keep both examples in mind as the general result of the formalism that we build next.

![The origin of the Friedel oscillation, which is the response of a metal to an impurity. In (a) the vector $2k_F$ connects the two Fermi points of a chain. In (b) the static response has its peak at this vector, so the density around the impurity oscillates with the wavevector $2k_F$. We derive this response in Section [9.4](#sec-9-4).](figures/s09f01_nesting.svg){panel="ab" alt="A one-dimensional band with its two Fermi points and the static response function with a logarithmic peak at twice the Fermi wavevector."}

Formally, we start from an unperturbed Hamiltonian $H_0$ and add a perturbation controlled by a dimensionless parameter $\lambda$,

$$H(\lambda) = H_0 + \lambda V,$$

so that $\lambda = 0$ gives the original system and $\lambda = 1$ is the fully perturbed one. Any observable, such as the energy, the density, the magnetic moment, the current, or the wavefunctions themselves, can then be expanded in a Taylor series in $\lambda$. The derivative of an observable with respect to $\lambda$ at $\lambda = 0$ is what we call the response of the system, and in the case of a magnetic perturbation it is called the susceptibility. Since every observable can be built from the wavefunctions, the most useful object to expand is the ground-state wavefunction itself. For a state $|n\rangle$ of the unperturbed Hamiltonian $H_0$ with energy $\varepsilon_n$, standard first-order perturbation theory gives

$$|n\rangle_\lambda = |n\rangle + \lambda \sum_{m \neq n} \alpha_m\, |m\rangle + \mathcal{O}(\lambda^2),
\qquad \alpha_m = \frac{\langle m|V|n\rangle}{\varepsilon_n - \varepsilon_m}. \tag{3.1}$$

Everything that we do in the rest of this session, which is the Hall conductivity, the Berry curvature and the Chern number, comes directly from putting [(3.1)](#eq-3-1) into the definition of some observable.

::: quiz
In [(3.1)](#eq-3-1) the state $|m\rangle$ is mixed into $|n\rangle$ with the amplitude $\alpha_m$. What happens to $\alpha_m$ if the level $m$ comes closer to the level $n$ while $V$ stays fixed?

- [ ] It decreases, since the two states become more similar.

    This is false. Take $\lambda|\langle m|V|n\rangle|=0.1$. At an energy distance $1$ the amplitude is $0.1$, and at a distance $0.1$ it is $1$, so it grew by a factor ten.

- [ ] It does not change, since it depends only on $V$.

    This is false. The energy difference $\varepsilon_n-\varepsilon_m$ is in the denominator of $\alpha_m$. For the same $V$, a distance ten times smaller gives an amplitude ten times larger.

- [x] It grows, and the expansion stops being valid once the amplitude is of order one.

    This is true. The amplitude goes as $1/(\varepsilon_n-\varepsilon_m)$ in [(3.1)](#eq-3-1). With $\lambda|\langle m|V|n\rangle|=0.1$ it reaches $1$ at a distance $0.1$, where the first-order result cannot be trusted.

:::

::: comesback
- In Section [3.4](#sec-3-4) we put [(3.1)](#eq-3-1) into the Hall conductivity, and in Section [4.3](#sec-4-3) the same Kubo formula gives the Hall conductance of the Landau levels.
- In Section [9.3](#sec-9-3) linear response and perturbation theory are derived again in detail, and Section [9.6](#sec-9-6) computes the Friedel oscillation around an impurity.
- In Section [6.13](#sec-6-13) we build the magnons that neutron scattering measures.
:::
