## Superconductivity as a macroscopic quantum phenomenon {#sec-5-2 number="5.2"}

Before we write the Hamiltonian, let us see why superconductivity is one of the clearest ways that we have to observe quantum mechanics at the macroscopic scale. A superconductor is made of trillions of atoms, and still a measurement on the bulk sample can give, with a very high precision, the microscopic constants $\hbar$ and $e$. This works because gauge symmetry breaking gives the many-body wave function a single well-defined phase $\theta(\mathbf{r})$, and the condition that this phase is single-valued around a closed loop is a very strong constraint.

Let us take a superconducting ring threaded by magnetic flux, or in the same way a hole in a bulk superconductor. We take the loop deep enough inside the superconductor that the supercurrent density vanishes there because of Meissner screening. The supercurrent of Cooper pairs, which have charge $2e$ since a pair is made of two electrons, is proportional to the gauge-invariant combination $\hbar\nabla\theta -
2e\mathbf{A}$. If we set the current to zero on our loop, we obtain

$$\oint \nabla\theta \cdot d\boldsymbol\ell = \frac{2e}{\hbar}\oint \mathbf{A}\cdot d\boldsymbol\ell = \frac{2e}{\hbar}\Phi.$$

However, $\theta$ is the phase of a single-valued wave function, so after one turn around the loop it can only change by an integer multiple of $2\pi$, which means that $\oint \nabla\theta\cdot
d\boldsymbol\ell = 2\pi n$ for integer $n$. If we combine the two equations, we obtain flux quantization,

$$\Phi = n\,\Phi_0, \qquad \Phi_0 = \frac{h}{2e}. \tag{5.1}$$

Figure [5.1](#fig:s05:flux) shows the geometry and the argument based on the winding of the phase. The same physics is behind the precision of Josephson junctions. In the AC Josephson effect, a voltage $V$ across the junction gives a current that oscillates with frequency $2eV/h$, which is a direct macroscopic readout of $h/2e$. This is possible only because gauge symmetry is broken. Note the parallel with the quantum Hall state of Session 4. There, a macroscopic measurement also gives a ratio of the same two constants, which is the Hall conductance, quantized in units of $e^2/h$ by the Chern number of equation [(3.4)](#eq-3-4). However, the mechanism is completely different, since it is the quantization of a single-particle topological invariant and not the breaking of a continuous symmetry. In fact, if we combine the two measurements, the flux quantum and the conductance quantum of the Hall effect, we have one of the most precise ways to obtain $h$ and $e$ separately. This is a concrete example of the emergence that we keep coming back to in this course, where macroscopic measurements on billions of atoms give us exact microscopic constants.

![A drawing of flux quantization. On the left there is a superconducting ring. Deep in the bulk the Meissner effect has already removed the supercurrent, so on the dashed contour the gauge-invariant combination $\hbar\nabla\theta-2e\mathbf A$ vanishes and the phase gradient is locked to the vector potential. On the right, the arrows are the condensate phase $\theta$ at points of this contour. When we move once around it, the phase must come back to itself, so it can only wind by an integer number of turns. Together, the two statements give $\Phi=n\,h/2e$, which means that the flux through the hole is quantized, and the $2$ in the denominator is the charge $2e$ of a Cooper pair. None of this is a property of a single electron. It is a macroscopic sample that gives back a ratio of microscopic constants, only because gauge symmetry is broken.](figures/s05f01_flux.svg){#fig:s05:flux number="5.1"}

::: quiz
Experiments find that the trapped flux in a ring comes in steps of $h/2e$. Which step would [(5.1)](#eq-5-1) give if the supercurrent were carried by single electrons of charge $e$?

- [ ] $h/2e$, since the step does not depend on the charge.

    This is false. The loop condition gives the step $h/q$, so it depends on the charge. For $q=e$ we get $h/e\approx4.1\times10^{-15}$ Wb, which is twice the measured $h/2e$.

- [x] $h/e$, which is twice as large.

    This is true. The loop condition gives $(q/\hbar)\Phi=2\pi n$ and the step $h/q$. For $q=e$ this is $h/e$, and the measured step $h/2e$ then shows that the carriers have charge $2e$.

- [ ] $h/4e$, since one electron carries half of a pair.

    This is false. A step $h/4e$ needs the charge $q=4e$. A single electron has charge $e$, and a charge $e/2$ would give the larger step $2h/e$, so this choice goes in the wrong direction.
:::

## Zero resistance and the Meissner effect in a superconductor {#sec-5-3 number="5.3"}

In the history of the field, superconductivity was discovered through its transport signature. When we cool an ordinary metal, the resistivity goes down smoothly, because there are fewer phonons from which the electrons can scatter. A superconductor instead shows a *sudden* drop of the resistance to exactly zero at a critical temperature $T_c$. Below $T_c$ the resistance stays zero, and not only small. $T_c$ is the temperature at which gauge symmetry breaking starts. There is no notebook cell for these signatures, since the companion notebook starts from the Hamiltonian and not from transport measurements.

The second signature is the **Meissner effect**. Above $T_c$ a metal allows an external magnetic field inside without any problem, but below $T_c$ the superconductor actively expels the field from its bulk. In type-II superconductors, the only field that remains inside the material is confined to quantized vortices, which are dynamical topological defects of the order parameter of the broken gauge symmetry. Both signatures, zero resistance and the expulsion of the flux, come from the same event. This is the condensation of Cooper pairs into a single macroscopic quantum state, with a rigid phase that is chosen spontaneously. Schematic [](#sch:s05:tc_meissner) shows both signatures. The resistance drops to zero at $T_c$, and below $T_c$ the field lines bend around the sample and do not cross it.

![The two signatures of the superconducting state. (a) The resistance of a normal metal stays finite, and that of a superconductor is zero below $T_c$. (b) Above $T_c$ the field lines cross the sample. (c) Below $T_c$ the field is zero inside and the lines go around, here for a sphere that is a perfect diamagnet.](figures/web/session05/tc_meissner.svg){#sch:s05:tc_meissner alt="Three panels. The resistance against temperature drops to zero at the critical temperature. The field lines of a field cross a sample above the critical temperature and bend around it below."}

::: comesback
- In Section [5.7](#sec-5-7) we see why the phase of the pair amplitude changes by $2\varphi$ under a gauge transformation, which is the origin of the charge $2e$ in [(5.1)](#eq-5-1).
- In Section [8.10](#sec-8-10) the emergent gauge field of a quantum spin liquid has its own topological defects, the visons, in analogy with the vortices of the superconducting phase.
:::
