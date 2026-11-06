## The gauge transformation in explicit form {#sec-5-7 number="5.7"}

We already wrote the gauge transformation in second quantization in session 1 (eq. [1.10](#eq-1-10)), $c \to
c\, e^{i\varphi}$, $c^\dagger \to c^\dagger e^{-i\varphi}$. It is the second-quantized version of the statement that the phase of a first-quantized wave function has no physical meaning. Let us now check explicitly which terms of a realistic Hamiltonian stay invariant under this transformation and which do not. Ordinary hopping $c_i^\dagger c_j$ is invariant, since the two phases cancel, as $c_i^\dagger c_j \to
e^{-i\varphi}c_i^\dagger \cdot e^{i\varphi} c_j = c_i^\dagger c_j$. The same cancellation protects essentially every other bilinear term that we have seen so far, such as magnetic terms that depend on spin, spin-orbit coupling and any density-density interaction term $c_i^\dagger c_i c_j^\dagger
c_j$, because all of them are built from the same number of creation and annihilation operators, which pair up index by index.

The pairing term is the only exception. Under the same transformation,

$$\Delta\, c_{n\uparrow}^\dagger c_{n\downarrow}^\dagger \;\longrightarrow\; \Delta\, e^{-2i\varphi}\, c_{n\uparrow}^\dagger c_{n\downarrow}^\dagger, \tag{5.5}$$

it gets the phase *twice*, because both operators are creation operators and not one creation and one annihilation operator. No choice of $\varphi \ne 0 \pmod \pi$ leaves this term invariant, so a Hamiltonian with a nonzero $\Delta$ is not gauge invariant term by term. In an equivalent way, if we write the transformation as acting on the order parameter itself, $\Delta \to \Delta\,
e^{2i\varphi}$, then any fixed phase of $\Delta$ is a choice that the ground state makes spontaneously, which is the signature of continuous symmetry breaking. This is the same logic that session 1 used to show the gauge symmetry breaking of eq. [1.9](#eq-1-9), now applied in full detail, and we have now seen why the factor is $2\varphi$ and not $\varphi$.
