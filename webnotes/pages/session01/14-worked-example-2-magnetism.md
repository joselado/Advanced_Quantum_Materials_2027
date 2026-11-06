## Worked example 2, magnetism {#sec-1-14 number="1.14"}

Let us now include again the spin degree of freedom, and let us change the interaction to an onsite Hubbard term between spin-up and spin-down electrons,

$$H = -t\sum_{n,\sigma}\left(c_{n\sigma}^\dagger c_{n+1,\sigma} + \text{h.c.}\right) + U\sum_n c_{n\uparrow}^\dagger c_{n\uparrow}\, c_{n\downarrow}^\dagger c_{n\downarrow}. \tag{1.7}$$

The sign of $U$ alone decides the physics. An attractive $U<0$ drives superconductivity, which we discuss in Section [1.15](#sec-1-15), and a repulsive $U>0$ drives magnetism, which is the topic of this section.

The mean-field decoupling is done in the same way as before, but now we apply it separately to $\langle c_{\uparrow}^\dagger c_\uparrow\rangle$ and $\langle c_\downarrow^\dagger
c_\downarrow\rangle$, and we obtain a bilinear Hamiltonian with onsite energies that depend on the spin. Let us define the magnetization

$$m = \langle c_\uparrow^\dagger c_\uparrow\rangle - \langle c_\downarrow^\dagger c_\downarrow\rangle. \tag{1.8}$$

Self-consistency gives $m=0$ automatically for $U<0$, and a finite $m$ for $U>0$, which is a real magnetic solution.

Let us say precisely *which* symmetry is broken here, using the formal definition in [(1.4)](#eq-1-4). Time-reversal symmetry reverses the direction of time and, together with it, every angular momentum in the system, including the spin. On the fermionic operators this means that it exchanges $c_\uparrow^\dagger c_\uparrow \leftrightarrow c_\downarrow^\dagger c_\downarrow$. Since $m$ in [(1.8)](#eq-1-8) changes sign under this exchange, a nonzero $m$ means that the ground state does not pass the invariance test in [(1.4)](#eq-1-4), so it is a magnet by definition. More generally, this is a breaking of the *continuous* spin-rotational symmetry, and this continuous symmetry breaking is what gives rise to the gapless magnon excitations that appear in the table of Section [1.11](#sec-1-11). We will study them in detail in a later session, and in this session we only need the mean-field ground state itself.

Numerically, when we increase $U$ a **Mott gap** opens in the spectrum, which grows linearly with $U$ at large $U$ and is associated with the formation of a real local moment on every site.

::: notebookbox
**Notebook check-in:** [`session1.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session1.ipynb), "The interacting Hubbard dimer" (Core), "Magnetic order driven by interactions in a chain" (Core), "Gap opening of the Hubbard model in a chain" (Challenge), and "Gap opening in the Hubbard model on the honeycomb lattice" (Challenge)

Start with the two-site case, the dimer, to see how the self-consistency loop converges in a small system that you can check by hand. Then go to the extended chain and finally to the honeycomb lattice, which uses the same finite-island geometries of Section [1.10](#sec-1-10) but now with interactions, and look at how the Mott gap opens and grows with $U$.
:::
