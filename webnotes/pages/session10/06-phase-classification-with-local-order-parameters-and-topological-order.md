## Phase classification with local order parameters and topological order {#sec-10-6 number="10.6a"}

We now come to a section that is, in a real sense, a review of the classification scheme of the whole course, seen from the point of view of machine learning. In this course we have used two quite different tools to distinguish phases. Session 1, Session 5 and Session 6 used a **local order parameter**, which is a quantity built from a simple local expectation value that is zero in one phase and nonzero in the other. It comes with the spontaneous symmetry breaking of Section [1.11](#sec-1-11). Examples are the charge imbalance for the charge density wave of Section [1.13](#sec-1-13), the magnetization for the magnet and the pairing amplitude for the superconductor. Session 3 and Session 4 instead used a **topological invariant**, such as the Chern number of Section [3.5](#sec-3-5) or the Zak phase of Section [3.9c](#sec-3-9c). The reason is that the phases there are *not* distinguished by any local quantity at all, and the difference can only be seen in a non-local way. In this session the same contrast gives an easy and a hard worked example of machine learning.

**The easy case, the Ising model.** Let us take classical Ising spins $\sigma_i = \pm 1$ on a square lattice, with the standard nearest-neighbor Hamiltonian and a local order parameter,

$$H_{\rm Ising} = -J\sum_{\langle i,j\rangle} \sigma_i \sigma_j, \qquad m = \frac{1}{N}\sum_i \sigma_i, \tag{10.9}$$

which has ferromagnetic order ($|m|\to 1$) below a critical temperature $T_c$ and is disordered ($m\to 0$) above it. Note the sign, since here $J>0$ favors parallel spins, while in the Heisenberg model [(6.5)](#eq-6-5) of Session 6 a positive $J$ is antiferromagnetic. If we only have a single snapshot of the spin configuration, at some unknown temperature, we can see the phase even by eye. We sum the spins and check whether the result is close to $\pm N$ or close to $0$. Even so, it is a clean and controlled test case for machine learning. We train the same cat-versus-dog architecture of Section [10.2](#sec-10-2) on labeled snapshots below and above $T_c$, where the input is the $N\times N$ spin snapshot and the output is a one-hot label for ordered or disordered. The classifier then gives a transition that becomes sharper as the system size grows, for sizes from $L = 10$ up to $L = 60$, and this reproduces what we already know analytically.

![The order parameter of [(10.9)](#eq-10-9) from the exact solution of the Ising model on the square lattice, $|m|=(1-\sinh^{-4}(2J/k_BT))^{1/8}$ below $T_c=2J/\ln(1+\sqrt2)\approx2.27J$. A single snapshot has $|m|$ close to one below $T_c$ and close to zero above it, so a sum over the spins is already a good test. The network of Section [10.2](#sec-10-2) learns this test by itself.](figures/web/session10/onsager.svg){#sch:s10:onsager alt="The magnetization of the Ising model against temperature, close to one at low temperature, falling steeply to zero at the critical temperature."}

![The same order parameter on finite lattices, from Metropolis Monte Carlo with $L=8$, $16$ and $32$, with $1500$ sweeps to thermalize and $3000$ sweeps to average at each temperature. The grey curve is the exact result for the infinite lattice. Below $T_c$ the three sizes agree with it. Above $T_c$ a finite lattice keeps a magnetization of order $1/L$, so the drop at $T_c$ becomes sharper as $L$ grows. This is the finite-size behavior that the trained classifier shows too.](figures/web/session10/ising_sizes.svg){#sch:s10:ising_sizes alt="The mean absolute magnetization against temperature for three lattice sizes. The curves agree at low temperature and drop near the critical temperature, more steeply for the larger lattice."}

::: quiz
A snapshot of the two-dimensional Ising model has $|m|=0.93$. On which side of $T_c$ was it taken?

- [ ] Above $T_c$, since the spins look random from site to site.

    This is false. Random-looking spins give $m\approx0$. For $N=64^2=4096$ spins far above $T_c$ the typical value is $1/\sqrt N\approx0.016$, so $0.93$ is not random-looking.

- [x] Below $T_c$, in the ordered phase.

    This is true. For $N=4096$ the fluctuation of $m$ far above $T_c$ is about $0.016$, so $|m|=0.93$ is more than $50$ standard deviations. The snapshot comes from the ordered phase.

- [ ] We cannot say from one snapshot, since $m$ fluctuates.

    This is false. The fluctuations of $m$ are small for a large system, about $0.016$ for $N=4096$ far above $T_c$. A single snapshot with $0.93$ is therefore enough to decide.
:::

::: quiz
We train the classifier of Section [10.2](#sec-10-2) on Ising snapshots. What are the input and the output?

- [x] The $N\times N$ array of spins as input, and a one-hot label for ordered or disordered as output.

    This is true. The network sees the spin array, and the label is the phase at which it was sampled. With this the network can find the transition without being told the local order parameter.

- [ ] The temperature as input, and the magnetization as output.

    This is false. If the temperature is the input, the answer is a comparison with $T_c$, which we must already know. The network would learn nothing about the snapshot.

- [ ] The energy of the snapshot as input, and the critical temperature as output.

    This is false. The critical temperature $T_c=2.27J$ is a property of the model and not of a snapshot. An output that is the same constant for every input is not a classifier.
:::

Next we will see a model where this simple test fails.

::: comesback
- In Section [10.6b](#sec-10-6b) the Ising gauge theory has no local order parameter, and the same classifier has to find a non-local quantity.
- In Section [10.7](#sec-10-7) the output of the network is the set of parameters of a Hamiltonian, in place of a phase label.
:::
