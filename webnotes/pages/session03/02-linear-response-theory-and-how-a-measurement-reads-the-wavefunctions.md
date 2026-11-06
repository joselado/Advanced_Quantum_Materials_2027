## Linear response theory and how a measurement reads the wavefunctions {#sec-3-2 number="3.2"}

To see why a bulk band structure can have an invariant at all, we need a tool that connects the wavefunctions of a Hamiltonian to something that we can measure. This tool is linear response theory, and the idea behind it is very general. We perturb the system at a position $x$ and time $t$, and then we measure an observable, such as the charge, the current, the magnetization or the heat, at another position $x'$ and time $t'$. Linear response theory tells us that this measured response depends only on the electronic structure of the unperturbed material.

Before we specialize to the Hall conductivity, let us look at two examples. Let us put an impurity in a two-dimensional metal and look at how the electron density, or the local density of states, is modulated around it. Linear response theory shows that this modulation pattern, which is called the Friedel oscillation, directly contains the Fermi wavelength of the electron gas, and this is what scanning tunneling microscopy uses in practice. In a similar way, when we scatter neutrons on a magnetic material, the magnetic moment of the neutron couples to the local moments in the sample. The resulting scattering pattern gives both the magnetic structure and its excitations, in particular magnons. Both examples are illustrations that appear only on the slides, in the sense that the figures of the Friedel oscillation and of neutron scattering were shown on screen without a full explanation. However, the physics of both examples was explained in the lecture, and it is useful to keep it in mind as the general result of the formalism that we build next.

Formally, we start from an unperturbed Hamiltonian $H_0$ and add a perturbation controlled by a dimensionless parameter $\lambda$,

$$H(\lambda) = H_0 + \lambda V,$$

so that $\lambda = 0$ gives the original system and $\lambda = 1$ is the fully perturbed one. Any observable, such as the energy, the density, the magnetic moment, the current, or the wavefunctions themselves, can then be expanded in a Taylor series in $\lambda$. The derivative of an observable with respect to $\lambda$ at $\lambda = 0$ is what we call the response of the system, and in the case of a magnetic perturbation it is called the susceptibility. Since every observable can be built from the wavefunctions, the most useful object to expand is the ground-state wavefunction itself. For a state $|n\rangle$ of the unperturbed Hamiltonian $H_0$ with energy $\varepsilon_n$, standard first-order perturbation theory gives

$$|n\rangle_\lambda = |n\rangle + \lambda \sum_{m \neq n} \alpha_m\, |m\rangle + \mathcal{O}(\lambda^2),
\qquad \alpha_m = \frac{\langle m|V|n\rangle}{\varepsilon_n - \varepsilon_m}. \tag{3.1}$$

Everything that we do in the rest of this session, which is the Hall conductivity, the Berry curvature and the Chern number, comes directly from putting [(3.1)](#eq-3-1) into the definition of some observable.
