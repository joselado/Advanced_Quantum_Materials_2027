## Why pairing does not conserve the particle number {#sec-5-6 number="5.6"}

Let us now show in an exact way the statement from session 1 that the electron number fluctuates, instead of only stating it. We take the eigenvalue equation $H_{\text{MF}}|G\rangle = E|G\rangle$ for the Hamiltonian in [(5.4)](#eq-5-4), and we expand the ground state in the occupation-number basis, which is the Fock basis, ordered by the total particle number $N$, as $|G\rangle = \sum_N a_N |N\rangle$. The hopping and chemical-potential terms in [(5.4)](#eq-5-4) conserve $N$ exactly, since each of them has one $c^\dagger$ and one $c$. The pairing terms $\Delta_n
c_{n\uparrow}^\dagger c_{n\downarrow}^\dagger$ and $\Delta_n^* c_{n\downarrow}c_{n\uparrow}$ change $N$ by $+2$ and $-2$ respectively. The key point is that *no term in $H_{\text{MF}}$ ever changes $N$ by $\pm 1$*. So $H_{\text{MF}}$ only connects Fock states whose particle numbers differ by an even integer. For $|G\rangle$ to be an eigenstate, $a_N$ can then be nonzero only inside one fixed parity class of $N$, either all even or all odd. However, this says nothing about which even or odd values of $N$ appear, and in general $a_N \ne 0$ for several values of $N$ in that class, for example $N=0,2,4,\dots$ at the same time. The mean-field ground state is therefore *not* an eigenstate of the total number operator $\hat N$, even though it has a well-defined fermion parity. This is the exact meaning of the statement that a superconductor has a fluctuating electron number but a fixed parity, which session 1 pointed out in its discussion of the superposition puzzle of the quantum dot (session 1, section [1.5](#sec-1-5)).

![The Fock space of three sites, in columns of fixed particle number $N$. The pairing terms of [(5.4)](#eq-5-4) connect a column with the one two steps away, and no term connects neighboring columns.](figures/s01f01_fockspace.svg){alt="Eight many-body states of three sites ordered in four columns by the particle number N from 0 to 3."}

::: quiz
The mean-field ground state of [(5.4)](#eq-5-4) is measured many times, and the total electron number is read each time. What do we find?

- [ ] The same $N$ every time, since $\hat N$ commutes with the hopping.
- [x] Different even values from run to run, or different odd values, but never a mix of both.
- [ ] Even and odd values mixed at random.
- [ ] No result, since $\hat N$ is not defined in a superconductor.

No term of $H_\text{MF}$ changes $N$ by one, so the ground state lives in one parity class. The pairing terms change $N$ by two, so several values of $N$ of that class appear with some weight, and the number fluctuates.
:::

## The gauge transformation in explicit form {#sec-5-7 number="5.7"}

We already wrote the gauge transformation in second quantization in session 1 (eq. [1.10](#eq-1-10)), $c \to
c\, e^{i\varphi}$, $c^\dagger \to c^\dagger e^{-i\varphi}$. It is the second-quantized version of the statement that the phase of a first-quantized wave function has no physical meaning. Let us now check explicitly which terms of a realistic Hamiltonian stay invariant under this transformation and which do not. Ordinary hopping $c_i^\dagger c_j$ is invariant, since the two phases cancel, as $c_i^\dagger c_j \to
e^{-i\varphi}c_i^\dagger \cdot e^{i\varphi} c_j = c_i^\dagger c_j$. The same cancellation protects essentially every other bilinear term that we have seen so far, such as magnetic terms that depend on spin, spin-orbit coupling and any density-density interaction term $c_i^\dagger c_i c_j^\dagger
c_j$, because all of them are built from the same number of creation and annihilation operators, which pair up index by index.

The pairing term is the only exception. Under the same transformation,

$$\Delta\, c_{n\uparrow}^\dagger c_{n\downarrow}^\dagger \;\longrightarrow\; \Delta\, e^{-2i\varphi}\, c_{n\uparrow}^\dagger c_{n\downarrow}^\dagger, \tag{5.5}$$

it gets the phase *twice*, because both operators are creation operators and not one creation and one annihilation operator. No choice of $\varphi \ne 0 \pmod \pi$ leaves this term invariant, so a Hamiltonian with a nonzero $\Delta$ is not gauge invariant term by term. In an equivalent way, if we write the transformation as acting on the order parameter itself, $\Delta \to \Delta\,
e^{2i\varphi}$, then any fixed phase of $\Delta$ is a choice that the ground state makes spontaneously, which is the signature of continuous symmetry breaking. This is the same logic that session 1 used to show the gauge symmetry breaking of eq. [1.9](#eq-1-9), now applied in full detail, and we have now seen why the factor is $2\varphi$ and not $\varphi$.


![The condensate phase at points around the ring. The phase of the pair amplitude $\Delta$ is the same kind of variable, and the superconducting ground state chooses one value of it.](figures/s05f01_flux.svg){panel="b" alt="Arrows around a closed contour that show the phase of the condensate at several points."}

::: quiz
Under the gauge transformation of this section the pairing term gets the phase $e^{-2i\varphi}$. For which angle does $\Delta\, c_{n\uparrow}^\dagger c_{n\downarrow}^\dagger$ stay unchanged?

- [ ] $\varphi=\pi/2$
- [x] $\varphi=\pi$
- [ ] $\varphi=\pi/4$
- [ ] Every $\varphi$, since the term becomes Hermitian once we add its conjugate.

The factor $e^{-2i\varphi}$ equals one only for $\varphi=0$ and $\pi$. At $\varphi=\pi/2$ it equals $-1$, so $\Delta$ changes sign. A generic angle moves $\Delta$ to another phase, and this is why the ground state has to choose one.
:::