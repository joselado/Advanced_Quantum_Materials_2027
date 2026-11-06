## Training the network and quantum state tomography {#sec-10-3b number="10.3b"}

In the first part we met the ansatz and the variational loss. Let us now see how it is computed and how it is used.

To compute [(10.3)](#eq-10-3) without a sum over all the $2^L$ configurations, one samples $s$ from the Born distribution $p(s) = |C_\theta(s)|^2/\sum_{s'}|C_\theta(s')|^2$ and evaluates the energy as an average of the sampled local energy,

$$E_{\rm loc}(s) = \sum_{s'} H_{s s'}\, \frac{C_\theta(s')}{C_\theta(s)}, \qquad E[\theta] = \big\langle E_{\rm loc}(s)\big\rangle_{s\sim p}, \tag{10.4}$$

which only needs $H$ between the configurations that are connected by the Hamiltonian, which is usually sparse, and not the full $2^L\times 2^L$ matrix. The training is then done in the same way as in [(10.1)](#eq-10-1). We compute the energy and its gradient with respect to the parameters of the network,

$$\frac{\partial E}{\partial \theta_k} = 2\,\mathrm{Re}\Big[\big\langle E_{\rm loc}(s)\, O_k^*(s)\big\rangle - \big\langle E_{\rm loc}(s)\big\rangle\big\langle O_k^*(s)\big\rangle\Big], \qquad O_k(s) \equiv \frac{\partial \ln C_\theta(s)}{\partial \theta_k}, \tag{10.5}$$

and we update $\theta_k \to \theta_k - \eta\, \partial E/\partial\theta_k$ many times, with a learning rate $\eta$ as in any other training of a neural network, until the gradient vanishes and the energy has converged to its variational minimum.

We should now say clearly how NNQS is related to the other variational ansätze of this course. The slides show this as a set of nested regions. The full many-body Hilbert space is one region, and inside it there is a smaller region with all the states that an NNQS with a given architecture can reach. Projected entangled pair states are inside this NNQS region, and matrix product states, which we built in session 7, are inside the PEPS region. The parameterizations of gapped one-dimensional systems are in the innermost region, since a matrix product state is a particular and highly structured choice of "network." NNQS is therefore the most expressive of the variational families of this course, because it imposes the least structure on how the coefficients depend on the configuration. Equation [(10.3)](#eq-10-3) is the loss function, and [(10.4)](#eq-10-4)-[(10.5)](#eq-10-5) are the training procedure, and together they make this picture a working method and not only a structure. Figure [10.2](#fig:s10:nnqs) shows all three parts, which are what the network computes, how the sampled estimate of the energy is built, and the nested picture.

![Neural network quantum states. **(a)** What the ansatz is. The exponentially long table of coefficients in [(10.2)](#eq-10-2) is not compressed, it is never written down at all. The configuration $s$ is given as an $L$-pixel "image," here a row of up and down spins, and the network returns the one coefficient $C_\theta(s)$ that we ask for. This is the same structure as in figure [10.1](#fig:s10:template), where only the input and the output have a new label. **(b)** Training. The variational energy [(10.3)](#eq-10-3) is the loss, and we estimate it by sampling configurations from the Born distribution and averaging the local energy [(10.4)](#eq-10-4), the bars and their mean. This is what makes the method possible, since $E_{\rm loc}(s)$ only needs the few matrix elements $H_{ss'}$ that a sparse Hamiltonian connects to $s$, and never the full $2^L\times 2^L$ matrix. **(c)** The nested regions drawn on the slides. A matrix product state is a highly structured special case of a PEPS, a PEPS is in turn a state that a large enough NNQS can represent, and NNQS is the outer region because it imposes the least structure of all on how $C$ depends on $s$. This picture organizes the lecture and is not a theorem, since the outer inclusion is a statement about networks that are expressive enough and not about every architecture. Note also that expressiveness has a cost, because the order is the opposite one for how easy each family is to optimize.](figures/s10f02_nnqs.svg){#fig:s10:nnqs number="10.2"}

### Quantum state tomography {#sec-10-3-1 number="10.3.1"}

A second and different use of the same NNQS ansatz is **quantum state tomography**. Let us take a real experimental system in some unknown state $|\psi\rangle$, and let us say that the only access that we have to it is through projective measurements. We measure the state of every spin, and the system collapses to one configuration $s$ with probability $|C(s)|^2$. If we repeat the measurement many times, we obtain a set of observed configurations that are distributed according to $|C(s)|^2$. However, we never observe $C(s)$ itself but only its modulus squared, and to do this for all the $2^L$ configurations one by one is the same exponential problem that we started with.

The solution has the same structure as the ground-state search above. We parameterize the unknown amplitude and phase with a network, for instance a restricted Boltzmann machine, or with two separate networks, one for $|C_\theta(s)|$ and one for its phase. Then we fit $\theta$ by **maximum likelihood** to the observed measurement outcomes, instead of minimizing an energy. In practice, one maximizes $\sum_{s} n(s) \ln p_\theta(s)$ over $\theta$, where $n(s)$ counts how many times the configuration $s$ was observed and $p_\theta(s) =
|C_\theta(s)|^2/\sum_{s'}|C_\theta(s')|^2$ is the probability predicted by the network. This reconstructs a full approximation to the unknown wavefunction with far fewer than $2^L$ measurements, and this is what makes it useful as an experimental tool, since nobody can run a tomography experiment that needs an exponential number of measurements.

::: quiz
In the local energy [(10.4)](#eq-10-4) the sum over $s'$ has only a few terms. What makes this possible?

- [ ] The network $C_\theta$ is zero for most configurations.
- [x] The Hamiltonian is sparse, so only a few $s'$ have a non-zero $H_{ss'}$ for a given $s$.
- [ ] The configurations $s$ are sampled, and sampling removes the sum over $s'$.

For a local Hamiltonian, a given configuration is connected to a number of others that grows only linearly with $L$. The sampling replaces the sum over $s$, and the sparsity limits the sum over $s'$.
:::

::: quiz
In tomography we measure only the spin of every site along $z$, and we fit $\theta$ by maximum likelihood. Which information about $C(s)$ do these data never contain?

- [ ] The modulus $|C(s)|$.
- [x] The phase of $C(s)$.
- [ ] The relative weight of two configurations.

The counts $n(s)$ follow $|C(s)|^2$, so the phase drops out. To fix it we need measurements in other bases.
:::

This part comes from the slides and the transcript and has no notebook counterpart, in line with the fact that this session has no companion notebook. There is no `sessionN.ipynb` cell to point you to here, so [(10.3)](#eq-10-3)-[(10.5)](#eq-10-5) and the tomography likelihood above are the complete and self-contained derivation.
