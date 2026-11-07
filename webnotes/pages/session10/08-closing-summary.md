## Closing summary {#sec-10-8 number="10.8"}

![The loop of the course, closed. The forward arrow from a Hamiltonian to an observable is what the first nine sessions built, and the network of this session runs it backwards, trained on the forward calculations themselves.](figures/s10f06_hamiltonianlearning.svg){alt="The forward arrow from the Hamiltonian to an observable, and the two stages of training on simulated data and applying the network to a measurement."}

In this session we used the variational principle and the matrix product states of Section [7.4](#sec-7-4) and Section [7.10](#sec-7-10), and the mean-field decoupling of Section [1.12](#sec-1-12). We also used the two ways of telling phases apart, a local order parameter as in Section [1.11](#sec-1-11) and a topological invariant as in Section [3.5](#sec-3-5). What we found is the following.

- A deep neural network is a parametric function that is trained by minimizing a loss function with gradient descent, equation [(10.1)](#eq-10-1). Every other construction in this session is a specific choice of input, output and loss built on top of this one template.

- **Neural network quantum states** replace the explicit storage of the $2^L$ coefficients of a wavefunction with a network $C_\theta(s)$, equation [(10.2)](#eq-10-2). This network is trained by using the variational energy as the loss function, equations [(10.3)](#eq-10-3) to [(10.5)](#eq-10-5). NNQS is above the matrix product states of Section [7.4](#sec-7-4) and the PEPS of Section [7.11](#sec-7-11) in the variational hierarchy, and it imposes the least structure of all the ansätze of this course. The same ansatz, fitted by maximum likelihood instead of energy minimization, solves quantum state tomography with far fewer than $2^L$ measurements.

- **Tensor networks**, built from the matrix product state ansatz [(10.6)](#eq-10-6) and its generalizations to trees, MERA and PEPS, can be used in the reverse direction as machine-learning architectures. For image classification on Fashion-MNIST, this reaches 95.38% training accuracy and 88.97% test accuracy, which is comparable with conventional neural networks.

- **Density functional theory** is based on the Hohenberg-Kohn functional [(10.7)](#eq-10-7) and the Kohn-Sham self-consistency loop [(10.8)](#eq-10-8). Machine learning enters in two ways. It can learn the unknown exchange-correlation part of [(10.8)](#eq-10-8), and then the self-consistency loop stays the same. Or it can learn the whole map from potential to density directly, and then the self-consistency loop is removed completely.

- **Phase classification** uses one more time the split of this course between local order parameters and topological order. The Ising model [(10.9)](#eq-10-9) is the easy case, which can be detected locally and follows the logic of Session 1, Session 5 and Session 6. The Ising gauge theory [(10.10)](#eq-10-10) is the hard case, where no local order parameter distinguishes the low-temperature and high-temperature regimes. These are separated only by a crossover, and the case follows the logic of Session 3 and Session 4. A trained network succeeds where the naive order parameter fails.

- **Hamiltonian learning** treats the inference of a Hamiltonian from measured observables, equation [(10.11)](#eq-10-11), as the inverse of the first step of Session 1, in Section [1.4](#sec-1-4). We train a network on synthetic forward data, equation [(10.12)](#eq-10-12), and apply it to real experimental observables, and in this way we close the loop in practice and not only in principle.

We started this course by asking how a small number of identical atoms, arranged in a lattice, can give rise to a phenomenology as rich as the one that we studied in ten sessions. This includes charge density waves, magnets, superconductors, topological insulators, fractional excitations, spin liquids and more, and none of it can be seen in a single atom alone. To answer this question we went through second quantization and the mean-field theory of Section [1.12](#sec-1-12), and through Bloch's theorem of Section [2.5](#sec-2-5) and the topological invariants of Section [3.5](#sec-3-5). Then came the Nambu spinors of Section [5.8](#sec-5-8), the magnon spectra of Section [6.13](#sec-6-13), the tensor networks of Section [7.4](#sec-7-4) and the parton constructions of Section [8.8](#sec-8-8). At the end we used linear response as a diagnostic for all of them, in Section [9.1](#sec-9-1). This session closed the arc in two ways. First, it showed that a neural network can take the place of the many-body wavefunction itself. Second, it showed that all the forward methods of the course, with a Hamiltonian as input and an observable as output, can be run backward to infer the Hamiltonians of real materials. This is a good place to end the course, not with a final answer, but with a general method to ask the question again, for the next quantum material that we want to understand.

::: quiz
Which choices define every construction of this session, from the cat-and-dog classifier to the neural network quantum state?

- [ ] The architecture only, since the training is always different.

    This is false. The cat-and-dog classifier and the phase classifier can use the same convolutional architecture. They differ in the input, the output and the loss, and the training step is the same.

- [x] The input, the output and the loss, with the training done by gradient descent as in [(10.1)](#eq-10-1).

    This is true. The classifier uses a spin array, a label and the loss of [(10.1)](#eq-10-1). The neural network quantum state uses a configuration, a coefficient and the energy, with the same gradient descent.

    ![The template that every construction uses, with an input, an output and a loss.](figures/s10f01_networktemplate.svg){alt="A deep network with an input picture, hidden layers and a one-hot output, next to the training loop of evaluation, loss, gradient and update."}

- [ ] The physical system only, since the network is always a tensor network.

    This is false. The same spin chain is used for the NNQS, with the energy as the loss, and for tomography, with the likelihood. The system is the same and the construction differs, and the NNQS can be a Boltzmann machine and not a tensor network.
:::

::: comesback
- This is the last page of the notes. The natural next step is the question of Section [1.1](#sec-1-1), how identical atoms on a lattice give rise to quantum materials, now with every tool of the course at hand.
- The forward arrow that Hamiltonian learning inverts is the one of Section [1.4](#sec-1-4).
:::
