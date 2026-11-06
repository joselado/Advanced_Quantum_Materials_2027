## Spontaneous symmetry breaking and why a symmetric Hamiltonian can have an asymmetric ground state {#sec-1-11 number="1.11"}

Before we discuss interactions, let us ask a more general question, since everything that we do in the rest of the session is an example of it. Physical theories usually have a lot of symmetry. Space is symmetric, time is symmetric, and so on. However, reality is not symmetric, since an object is in one place and not in another, and a system evolves forward in time and usually not backward. So why do the symmetries of the Hamiltonian so often not survive in the ground state?

Let us start with an example from daily life, which is a group of colleagues who sit at a table for a meal, with bread on both sides of each person. Each person has to choose between the bread on the left and the bread on the right. There is of course a "correct" answer from etiquette, but let us say that nobody knows it. Some people will take the left one and others the right one, and once the choice is made, everybody at the table ends up in one of two equally good configurations, which are everybody-left or everybody-right. The initial setup, with bread on both sides, was perfectly symmetric. The final result is not. This difference, a symmetric problem with a solution that is not symmetric, is spontaneous symmetry breaking on a small scale.

The same logic, in an exact form, is what happens in a classical Ising ferromagnet. The set of ground states of the Hamiltonian is symmetric, since all spins up is as good a solution as all spins down. However, if we take a *very* large system, which formally means an infinitely large one, or the thermodynamic limit, the system has to choose one of the two, all spins up or all spins down. Which one we measure is decided by fluctuations and not by the Hamiltonian, and once it is decided, the state that we observe is no longer symmetric, even though the Hamiltonian that produced it was always symmetric. The requirement of the thermodynamic limit is essential. Strictly speaking, spontaneous symmetry breaking is a statement about infinite systems, and it is a generic feature of many-body interactions and correlations, not something that appears for a few particles. Figure [1.2](#fig:s01:ssb) puts all of this in one picture. It shows a symmetric energy landscape whose minima are not symmetric, with a barrier between them that becomes impossible to cross only in the thermodynamic limit.

![Spontaneous symmetry breaking. The energy as a function of the order parameter is symmetric under $m\to-m$, in the same way as the Hamiltonian, but its minima are not, since the system has to be at $+m_0$ or at $-m_0$. The system is the ball at $+m_0$, and the ghost ball at $-m_0$ is the minimum with the same energy that it did not choose. The choice is made by fluctuations and not by the Hamiltonian. The barrier between the minima grows with the system size, from the small system on the left to the large one on the right, which is why spontaneous symmetry breaking is strictly a statement about the thermodynamic limit.](figures/s01f02_ssb.svg){#fig:s01:ssb number="1.2"}

This gives us a useful way to classify states of matter, according to *which* symmetry they break spontaneously.

- Broken **time-reversal symmetry** gives classical magnets. The magnetization is odd under time reversal, so a magnetic ground state is not invariant when we run the movie backward.

- Broken **inversion symmetry** gives ferroelectrics. These are materials that develop an electric polarization spontaneously, which is the electric analog of a magnetization, and in this way they break the inversion symmetry of the underlying crystal.

- Broken **gauge symmetry** gives superconductors. The phase of the pairing order parameter, or equivalently the phase of the creation and annihilation operators, becomes physical once the order appears. Many observable superconducting phenomena, such as the Josephson effect, are direct consequences of fluctuations of this broken phase, and we will discuss this in detail in the session on superconductivity.

This classification by symmetry is useful, but it does not capture everything. Topological materials, such as topological insulators and fractional Chern insulators, can have *exactly* the same broken or unbroken symmetries as an ordinary trivial material and still behave in a completely different way. The reason for this is that they differ in their topological classification and not in their symmetry classification. This difference is the topic of a full session later in the course. For now, we only keep in mind that the question of "which symmetry is broken" does not give the full description of quantum matter.

Every case of spontaneous symmetry breaking also comes with its own emergent quasiparticle, which is the low-energy fluctuation of the order that has formed. The following table lists three cases.

::: center
  **Broken symmetry**        **Realized in**   **Quasiparticle**    **Spin**   **Charge**  **Gap**
  -------------------------- ----------------- ------------------- ---------- ------------ ----------------------------------
  Continuous translational   Crystals          Phonon                  0           0       Gapless (always)
  Spin-rotational $SO(3)$    Magnets           Magnon                  1           0       Gapless (gapped with anisotropy)
  Gauge                      Superconductors   Higgs mode              0           0       Gapped
:::

Note that magnons and the Higgs mode both have zero charge but very different spin, and that only the phonon is gapless in every material. Magnons are gapless when the broken spin-rotational symmetry is continuous, and they become gapped when a magnetic anisotropy breaks this symmetry explicitly. The Higgs mode, which is an oscillation of the amplitude of the order parameter, is always gapped.

Since we cannot run time backward in the lab to check if a material breaks time-reversal symmetry, we measure instead quantities that are themselves odd under time reversal. Two of them are especially useful. The first one is the **Hall conductivity**, which is a transverse current generated by a longitudinal voltage. The second one is the **magneto-optical Kerr effect**, which is a different optical reflection for left-handed and right-handed circularly polarized light. A nonzero signal in either of them is direct evidence of broken time-reversal symmetry.

With this we can finally give a precise and formal definition of a magnet, which goes beyond "the object that sticks to your fridge". A magnet is a many-body state whose wave function is not invariant under the time-reversal operator $\hat T$,

$$\hat T|\Psi\rangle = |\Psi\rangle \;\Rightarrow\; \text{not magnetic}, \qquad
\hat T|\Psi\rangle \neq |\Psi\rangle \;\Rightarrow\; \text{magnetic}. \tag{1.4}$$

The north and south poles of a bar magnet are exchanged under time reversal, since a magnetic pole is connected to an orbital angular momentum and angular momenta change sign under $\hat T$. For this reason a bar magnet does not pass the invariance test in [(1.4)](#eq-1-4), and it is magnetic according to this definition. A plain stick that is not magnetic, on the other hand, looks the same under time reversal and passes the test.

Let us now build this general picture explicitly, three times.
