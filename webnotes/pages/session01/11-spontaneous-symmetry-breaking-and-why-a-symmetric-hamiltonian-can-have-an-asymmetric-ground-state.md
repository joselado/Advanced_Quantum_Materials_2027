## Spontaneous symmetry breaking and why a symmetric Hamiltonian can have an asymmetric ground state {#sec-1-11 number="1.11a"}

Before we discuss interactions, let us ask a more general question, since everything that we do in the rest of the session is an example of it. Physical theories usually have a lot of symmetry. Space is symmetric, time is symmetric, and so on. However, reality is not symmetric, since an object is in one place and not in another, and a system evolves forward in time and usually not backward. So why do the symmetries of the Hamiltonian so often not survive in the ground state?

Let us start with an example from daily life, which is a group of colleagues who sit at a table for a meal, with bread on both sides of each person. Each person has to choose between the bread on the left and the bread on the right. There is of course a "correct" answer from etiquette, but let us say that nobody knows it. Some people will take the left one and others the right one, and once the choice is made, everybody at the table ends up in one of two equally good configurations, which are everybody-left or everybody-right. The initial setup, with bread on both sides, was perfectly symmetric. The final result is not. This difference, a symmetric problem with a solution that is not symmetric, is spontaneous symmetry breaking on a small scale.

The same logic, in an exact form, is what happens in a classical Ising ferromagnet. The set of ground states of the Hamiltonian is symmetric, since all spins up is as good a solution as all spins down. However, if we take a *very* large system, which formally means an infinitely large one, or the thermodynamic limit, the system has to choose one of the two, all spins up or all spins down. Which one we measure is decided by fluctuations and not by the Hamiltonian, and once it is decided, the state that we observe is no longer symmetric, even though the Hamiltonian that produced it was always symmetric. The requirement of the thermodynamic limit is essential. Strictly speaking, spontaneous symmetry breaking is a statement about infinite systems, and it is a generic feature of many-body interactions and correlations, not something that appears for a few particles. Figure [1.2](#fig:s01:ssb) puts all of this in one picture. It shows a symmetric energy landscape whose minima are not symmetric, with a barrier between them that becomes impossible to cross only in the thermodynamic limit.

![Spontaneous symmetry breaking. The energy as a function of the order parameter is symmetric under $m\to-m$, in the same way as the Hamiltonian, but its minima are not, since the system has to be at $+m_0$ or at $-m_0$. The system is the ball at $+m_0$, and the ghost ball at $-m_0$ is the minimum with the same energy that it did not choose. The choice is made by fluctuations and not by the Hamiltonian. The barrier between the minima grows with the system size, from the small system on the left to the large one on the right, which is why spontaneous symmetry breaking is strictly a statement about the thermodynamic limit.](figures/s01f02_ssb.svg){#fig:s01:ssb number="1.2"}

::: quiz
Why is spontaneous symmetry breaking strictly a statement about infinite systems?

- [ ] In a finite system the Hamiltonian is not symmetric anymore.

    This is false. Take two Ising spins with $H=-J\sigma_1\sigma_2$. It is invariant under the flip of both spins for any finite size. The symmetry of $H$ does not depend on the size.

- [x] In a finite system the barrier is finite, so the system tunnels and the ground state stays symmetric.

    This is true. The system can cross the barrier between the two minima, and the true ground state is the symmetric superposition of both. The barrier grows with the system size, and in the thermodynamic limit it cannot be crossed.

    ![The two lowest states of a double well, with $\hbar^2/2m=1$ and $V=8(x^2-1)^2$. The lower one is even and has weight in both wells, and the odd one is $2\Delta=0.92$ higher. A higher barrier makes $\Delta$ smaller.](figures/web/session01/tunnel_split.svg){alt="A double well with its even ground state, its odd first excited state and the small energy splitting between them."}

- [ ] A finite system has no ground state.

    This is false. The matrix $\begin{pmatrix}0&-\Delta\\-\Delta&0\end{pmatrix}$ of the two minima has the ground state $(1,1)/\sqrt2$ with energy $-\Delta$. A finite matrix always has a lowest level, and here it is symmetric.

Tunneling between the minima restores the symmetry in any finite system.
:::
