## Why the Holstein-Primakoff magnon approach fails for QSL excitations {#sec-8-7 number="8.7"}

It is hard to write the exact QSL ground state, so the natural next step, as in Session 6, is to ask about the excitations *on top of* the ground state, and not about the ground state itself. Up to now, the only tool that we have for this is the **Holstein-Primakoff transformation**, which writes

$$S_i^z = S - a_i^\dagger a_i, \qquad S_i^+ \approx \sqrt{2S}\,a_i, \qquad S_i^- \approx
\sqrt{2S}\,a_i^\dagger, \tag{8.8}$$

where we linearized under the assumption that the number of bosonic magnons is small, $\langle a_i^\dagger a_i\rangle \ll S$. This is a very good approximation close to a fully or nearly polarized magnet, which is the regime where we used it in Session 6.

A QSL is in the opposite limit. Its defining property, $\langle \mathbf S_i\rangle = 0$ on every site, gives through [(8.8)](#eq-8-8)

$$\langle a_i^\dagger a_i \rangle = S, \tag{8.9}$$

which is the regime where the condition of a small boson density, the basis of the linearized Holstein-Primakoff mapping, fails completely. For a QSL there is no ordered reference state that it is "close to" and around which we can expand. As a result, the magnon method that worked for the ordered magnets of Session 6 is not the right tool here, and we need a different approximation for the excitations of a quantum spin liquid.

::: notebookbox
**Notebook check-in:** [`session8.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session8.ipynb), "Magnetization of a large Heisenberg model" (Core)

Diagonalize a quantum Heisenberg chain of moderate size and check numerically that the local magnetization stays zero on every site. This also holds with a small external field, as long as the field is weaker than the finite-size gap to the neighboring sector of total spin. This is how the defining property behind [(8.5)](#eq-8-5) and [(8.9)](#eq-8-9) appears in a numerical calculation.
:::
