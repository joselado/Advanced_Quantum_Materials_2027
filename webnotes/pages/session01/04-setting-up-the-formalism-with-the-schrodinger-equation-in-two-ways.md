## Setting up the formalism with the Schrödinger equation in two ways {#sec-1-4 number="1.4"}

Why is the Schrödinger equation of one electron easy to solve, and the one of many electrons hard? We will now see that the many-electron problem can be written in two languages, first and second quantization. The one property that separates them is whether the number of particles is fixed.

Every quantum mechanical system is described by the Schrödinger equation, which is built from a Hamiltonian acting on a wave function, where for our purposes we can think of the Hamiltonian as a matrix. If we know the wave function at time zero and the Hamiltonian, in principle we can integrate this equation forward in time and know the state at any later time. This statement is completely general, and it holds both when the wave function describes one particle and when it describes a whole many-body system. In practice, however, the difference is very large. Single-particle problems can always be solved exactly, in every case that is relevant for us. Many-body problems in general cannot, and the difficulty grows very fast with the size of the system, as we will see in a concrete way below.

Most of the quantum matter that we are interested in is truly many-body. So we need a systematic way to deal with this difficulty, even if this way is often approximate, and this is what we build in this session.

### First quantization {#sec-1-4-1 number="1.4.1"}

When the electrons can be treated as independent of each other, we can describe the system with a single-particle wave function that lives in an ordinary Hilbert space. This is what is called *first quantization*, which is the language that you already know from a standard course on quantum mechanics. It is a very capable tool, and it is enough to describe metals, semiconductors, insulators and even topological insulators.

### Second quantization {#sec-1-4-2 number="1.4.2"}

First quantization assumes that the number of particles is fixed, and this assumption fails for a whole class of quantum materials. It fails for any system where the electrons are not independent, and also, which is more surprising, for systems where the *number* of electrons is itself not fixed. For these systems we need *second quantization*, which is a formalism that is not built around the question of "how many electrons are present" but around how electrons are created and destroyed. This formalism is essential for superconductors, superfluids and correlated materials in general, and it is what makes phenomena such as spinon fractionalization straightforward to describe at all. [](#sch:s01:fixed_vs_free_number) shows this difference for a small dot.

::: key
A wave function has a fixed number of coordinates, one for each particle, so first quantization keeps the number of particles $N$ fixed. Second quantization also describes states where $N$ fluctuates, such as a superposition of zero and two electrons.
:::

![A dot with two levels and its Fock states sorted by the number of electrons. First quantization stays inside one column, here the one with a single electron. Second quantization also allows states that mix columns, such as an equal superposition of zero and two electrons.](figures/web/session01/fixed_vs_free_number.svg){#sch:s01:fixed_vs_free_number alt="States of a dot with two levels, with zero, one and two electrons, and an arrow that links the empty and the full dot."}

::: quiz
A dot has two levels. Which state can we write as a wave function with a fixed number of coordinates?

- [x] One electron in a superposition of the lower and the upper level.

    This is true. The wave function is $\psi(x)=a\psi_0(x)+b\psi_1(x)$, and it has one coordinate. The number of electrons is one for both terms.

- [ ] An equal superposition of zero electrons and two electrons.

    This is false. The mean number of electrons is $1$, but one term has no coordinate and the other has two, $x_1$ and $x_2$. No single function $\psi(x_1,x_2)$ describes both terms.

- [ ] An equal superposition of one electron and two electrons.

    This is false. One term has the coordinate $x$ and the other has $x_1$ and $x_2$, so no single function describes both terms. The mean of $1.5$ electrons is not the reason, since the mean $1$ of zero and two electrons fails in the same way. Second quantization can write this state as a vector of the Fock space, but for electrons it is not a physical state, since it mixes an odd and an even number of fermions.

A wave function needs a fixed number of coordinates. States that mix different numbers of electrons need second quantization.
:::

:::: problem
A dot has $L$ levels for spinless electrons, and each level is empty or holds one electron. How many states with $N$ electrons does the dot have, and how many states in total? Compute both numbers for $L=4$.

::: solution
A state with $N$ electrons is fixed by the set of the $N$ occupied levels. The electrons are identical, so the order in which we pick the levels does not matter, and the number of states is the binomial coefficient

$$\binom{L}{N}=\frac{L!}{N!\,(L-N)!}.$$

For $L=4$ this gives $1$, $4$, $6$, $4$ and $1$ states for $N=0,1,2,3,4$, so there are $6$ states with two electrons. The total is the sum over $N$,

$$\sum_{N=0}^{4}\binom{4}{N}=1+4+6+4+1=16=2^4,$$

since each of the four levels is empty or occupied independently of the others.

First quantization works inside one of these sets, for instance the $6$ states with $N=2$, which are the $6$ antisymmetric wave functions $\psi(x_1,x_2)$ that we can build from four levels. Second quantization works with all $16$ states at once and with their superpositions. The total $2^L$ is the dimension of the Fock space, and its exponential growth with $L$ is the subject of Section [1.9](#sec-1-9).
:::
::::

::: comesback
- The fluctuating number of electrons comes back in Section [5.6](#sec-5-6), where the pairing term of a superconductor mixes states with $N$ and $N\pm2$ electrons.
- In Section [7.2](#sec-7-2) fermions and spins are two languages for the same physics, and the Jordan-Wigner transformation of Section [7.2b](#sec-7-2b) maps one onto the other.
- In Section [10.7](#sec-10-7) the Schrödinger equation of this section is used in the inverse direction, to learn the Hamiltonian from what we measure.
:::
