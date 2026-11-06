## Hamiltonian learning as the inverse of the first step of session 1 {#sec-10-7 number="10.7"}

We come at the end to the part of this session that closes the loop in the most explicit way. Let us go back to session 1, Section [1.4](#sec-1-4). Every quantum mechanical system is described by the Schrödinger equation, and if we have a Hamiltonian and an initial state we can integrate forward in time and obtain, in principle, every observable of the system, such as the density, the magnetization, the response functions and so on. This forward arrow, Hamiltonian $\to$ observable, is what almost this entire course has been built to compute, one physical setting at a time.

However, this is not the arrow that an experimentalist can use. A real measurement never gives you the Hamiltonian. It gives you an observable directly, such as a density, a conductivity, an ARPES spectrum or a neutron-scattering structure factor, and the Hamiltonian is the thing that you do *not* have and would like to infer. **Hamiltonian learning** writes this explicitly as the inverse problem. On the slides the Hamiltonian is written as $H(\lambda_i, w_i)$, where its dependence is split into two parts. The first part are the physical parameters of interest $\lambda$, such as magnetic or electric fields, hopping amplitudes and many-body interaction strengths. The second part is a set of "hidden," or nuisance, variables $w$ that one does *not* want to fit, such as smaller parameters, disorder realizations, artifacts of the computational method that generated the training data, and plain randomness. If we write $\mu
\equiv w$ for this vector of hidden variables, the forward direction is the map

$$\mathcal{O} = \mathcal{O}\big[H(\lambda,\mu)\big], \tag{10.11}$$

and Hamiltonian learning asks for the inverse map, $\mathcal{O} \mapsto \lambda$, where we marginalize over $\mu$ as well as we can instead of trying to fit it. In general this is a difficult inverse problem, since many different $\lambda$ can be compatible with the same measured $\mathcal{O}$, and there is little real experimental data to train on. The practical strategy is, once again, to use theory to compensate for the lack of experimental data. We simulate the observable $\mathcal{O}$ from many different and *known* Hamiltonians $H(\lambda_n)$ that cover the range of parameters of physical interest. These are the same forward calculations, such as the density, the magnetization and the spectroscopy, that we learned to compute directly in the earlier sessions. Then we train a neural network $\mathcal{N}_\theta$ on this synthetic data to invert [(10.11)](#eq-10-11), and we do this by minimizing

$$\mathcal{L}(\theta) = \sum_n \left\| \mathcal{N}_\theta\big(\mathcal{O}[H(\lambda_n)]\big) - \lambda_n \right\|^2. \tag{10.12}$$

Once the network is trained on simulated pairs, where the answer $\lambda_n$ is known by construction, the same network is applied to a real experimental observable $\mathcal{O}_{\rm
exp}$. The concrete example of the lecture was a two-dimensional spectroscopy of a quantum magnet. Then $\hat\lambda = \mathcal{N}_\theta(\mathcal{O}_{\rm exp})$ gives an estimate of the physical parameters of the Hamiltonian, for instance the first-, second-, and third-neighbor exchange couplings of that magnet, extracted directly from a measurement for which there is no closed-form inversion formula at all. Figure [10.6](#fig:s10:hamlearning) shows both stages, the synthetic training set and the use on real data, together with the forward arrow that the two stages invert.

![Hamiltonian learning, and why it closes the loop of the course instead of going outside it. **Top.** The forward arrow $H\mapsto\mathcal{O}$ of [(10.11)](#eq-10-11) is what sessions 1 to 9 built during all their time. The arrow that an experiment needs goes in the other direction, and there is no closed-form inversion of it. **(a)** The solution to the lack of experimental training data is to produce the data. We simulate $\mathcal{O}$ from many *known* Hamiltonians, so that every training pair comes with its answer $\lambda_n$ by construction, and we fit the network with [(10.12)](#eq-10-12). **(b)** Only after this step the trained network is applied to a real measurement. Note what the training set is made of, which is the forward methods of the whole course, run many times. The final method of the course and its first method are the same method, applied in opposite directions.](figures/s10f06_hamiltonianlearning.svg){#fig:s10:hamlearning number="10.6"}

::: quiz
Why do we train the network of [(10.12)](#eq-10-12) on simulated observables, and not on measured ones?

- [ ] Simulated data are always more accurate than measurements.

    This is false. A mean-field simulation of a strongly correlated model can be wrong compared to the experiment. Even so, it gives the exact $\lambda_n$ of its own input, which is what training needs.

- [x] There are few measurements, and the Hamiltonian that produced them is unknown, while a simulation gives the answer $\lambda_n$ by construction.

    This is true. A measurement does not come with its $\lambda_n$, since this is what we want to find. A simulation gives a pair $(\mathcal O,\lambda)$ for each run, so we can make $10^5$ pairs.

- [ ] Measured data cannot be written as arrays of numbers.

    This is false. A measured dI/dV is an array, for example $200$ values of the voltage, and it can be the input of the network. At the end it is the input of the trained network.
:::

::: quiz
Many different values of $\lambda$ give nearly the same observable $\mathcal{O}$. What is the consequence for the inverse map?

- [ ] The inverse map is not defined for any observable.

    This is false. For a chain with $t>0$ the bandwidth is $4t$, so $\mathcal O$ fixes $t$ and the inverse map exists. It is not defined only where the observable is not enough.

- [x] The network gives only an estimate with an uncertainty, and the hidden variables $\mu$ must be covered by the training set.

    This is true. A chain with $t$ and a chain with $-t$ have the same density of states. The network cannot give the sign, so it gives an estimate with an uncertainty and we must cover $\mu$ in training.

    ![The bands of the chains with $t=1$ and $t=-1$ are upside down with respect to each other, and the density of states $1/(\pi\sqrt{4t^2-E^2})$ is the same.](figures/web/session10/dos_sign.svg){alt="Two cosine bands that are upside down with respect to each other, next to one density of states curve that is the same for both."}

- [ ] The network must always give the exact $\lambda$, since the loss [(10.12)](#eq-10-12) is zero for the training pairs.

    This is false. The pairs $(\mathcal O,t)$ and $(\mathcal O,-t)$ have the same input and different labels. The mean-square loss is minimal when the network gives the mean of the two labels, which is $0$, and then the loss is $t^2$ and not zero.
:::

This is the mirror image of the starting point of session 1, and we want to stop for a moment on this symmetry. In nine sessions we built more and more sophisticated ways to go from a Hamiltonian to an observable. These are mean-field decoupling, Bloch's theorem, topological invariants, Landau levels, Nambu spinors, magnon spectra, tensor-network ground states, parton constructions and response functions. Hamiltonian learning does not leave any of these behind. Instead, it uses the same forward methods, run many times on synthetic data, as the training set to learn how to run the process in reverse. In this sense, the method of the course and the final method of the course are the same method, applied in opposite directions.
