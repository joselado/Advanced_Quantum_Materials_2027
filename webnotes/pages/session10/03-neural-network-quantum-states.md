## Neural network quantum states {#sec-10-3 number="10.3a"}

In this section we meet neural network quantum states (NNQS) for the first time in the course, and we treat them directly with the machine-learning methods of Section [10.2](#sec-10-2). The idea in one sentence is that a neural network can take the place of the exponentially many coefficients of a many-body wavefunction. In this way it has its own place in the hierarchy of variational many-body states that this course has been building since the matrix product states of session 7. In this section we make this idea precise. We will see what the network computes, which loss function is used to train it, and how it is related to the ansätze that we already know.

We start from a difficulty that we have met before, most recently in the discussion of entanglement growth in session 7. A wavefunction for $L$ spins,

$$|\psi\rangle = \sum_{s_1,\dots,s_L} C(s_1,\dots,s_L)\, |s_1,\dots,s_L\rangle, \tag{10.2}$$

is given by $2^L$ coefficients, and it is not possible to store them explicitly once $L$ is much bigger than 30 or 40. The idea of a neural network quantum state (NNQS) is to not store $C(s_1,\dots,s_L)$, and instead to *generate* it. We build a neural network $C_\theta$ that takes a spin configuration $(s_1,\dots,s_L)$ as input, which is formally an $L$-pixel "image," and returns the coefficient. For a wavefunction that is complex, it returns its real and imaginary parts as two output numbers, or in an equivalent way its modulus and phase. This is the same idea as the matrix product state of Section [10.4](#sec-10-4) below, where a compact generator takes the place of exponentially many numbers, but here it is built from the parameters of a neural network and not from a chain of matrices.

The question is then how to find the right $\theta$ for the ground state, and here the methods of Section [10.2](#sec-10-2) appear again with almost no change. The variational principle tells us that

$$E[\theta] \;=\; \frac{\langle \psi_\theta | H | \psi_\theta\rangle}{\langle \psi_\theta|\psi_\theta\rangle} \;=\; \frac{\sum_{s,s'} C_\theta^*(s)\, H_{s s'}\, C_\theta(s')}{\sum_s |C_\theta(s)|^2} \;\geq\; E_0, \tag{10.3}$$

where the equality holds only when $|\psi_\theta\rangle$ is the true ground state, or in practice the closest state that the ansatz can reach. Equation [(10.3)](#eq-10-3) *is* the loss function of [(10.1)](#eq-10-1), meaning that the "observable output" that the network is trained to minimize is the energy of the system.

![The template of Section [10.2](#sec-10-2), now used for a wavefunction. The picture on the input becomes a spin configuration $s$, the output becomes the single coefficient $C_\theta(s)$, and the loss of the training loop is the variational energy [(10.3)](#eq-10-3) in place of the squared error of [(10.1)](#eq-10-1).](figures/s10f01_networktemplate.svg){alt="A deep network with an input picture, hidden layers and a one-hot output, next to the training loop of evaluation, loss, gradient and update."}

::: quiz
A wavefunction of $L=40$ spins is stored as a table of complex coefficients in double precision. How much memory does the table need?

- [ ] About $40^2$ numbers, which is a few kilobytes.
- [ ] About $10^6$ numbers, which is a few megabytes.
- [x] About $10^{12}$ numbers, which is roughly $16$ terabytes.

The table has $2^{40}\approx1.1\times10^{12}$ coefficients, and each one takes $16$ bytes. A network with a few thousand parameters generates the same coefficients on demand and never stores the table.
:::

::: quiz
For a spin chain whose ground-state energy we know exactly, a student finds $E[\theta]$ clearly below it, well beyond the statistical error. What should we conclude?

- [ ] The network has found a state that is better than the ground state.
- [x] There is a mistake, since $E[\theta]\geq E_0$ for any state in [(10.3)](#eq-10-3).
- [ ] The network is too small, so it should be made larger.

The variational energy is bounded from below by the true ground-state energy for every state, whatever the architecture. A value below it signals an error in the Hamiltonian, in the local energy or in the sampling.
:::

Next we will see how to evaluate this energy without a sum over all the configurations.
