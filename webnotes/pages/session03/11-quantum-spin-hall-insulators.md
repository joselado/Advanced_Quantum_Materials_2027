## Quantum spin Hall insulators {#sec-3-11 number="3.11a"}

A Chern insulator needs broken time-reversal symmetry. The quantum spin Hall insulator is what we obtain if we keep time-reversal symmetry and still want a topological gapped state. We take two copies of the massive Dirac construction [(3.7)](#eq-3-7), one for each spin, with **opposite** mass for opposite spins, $m_\uparrow = -m_\downarrow$. From [(3.8)](#eq-3-8), the two spin sectors then have opposite Chern numbers,

$$C_\uparrow = \pm 1, \qquad
C_\downarrow = -C_\uparrow, \qquad
C = C_\uparrow + C_\downarrow = 0, \qquad
C_s \equiv C_\uparrow - C_\downarrow = \pm 2. \tag{3.9}$$

Here $C_\uparrow$ is the Chern number of the whole spin-up sector of the lattice. Each Dirac point gives $\tfrac12$ by [(3.8)](#eq-3-8), and the two Dirac points add for each spin, as in the Haldane case of Section [3.10](#sec-3-10), so one spin sector has $C_\uparrow=\pm1$.

The total Chern number $C$ vanishes, in agreement with the unbroken time-reversal symmetry, but the **spin** Chern number $C_s$ does not vanish, and it is $C_s$ that controls the edge physics. At each edge, spin-up propagates in one direction and spin-down propagates in the other direction, which is a **helical** edge state and not a chiral one.

![A helical edge, which comes back in Section [5.18](#sec-5-18). On the same edge the spin-up electrons move in one direction. The spin-down electrons move in the other, and the two are drawn in a warm and a cold color. This is the pair of branches that follows from [(3.9)](#eq-3-9).](figures/s05f06_qsh.svg){alt="The edge of a quantum spin Hall insulator with spin-up and spin-down channels moving in opposite directions."}

::: quiz
The two spin sectors have $C_\uparrow=+1$ and $C_\downarrow=-1$. What are the charge Hall conductivity and the edge of this insulator?

- [ ] $e^2/h$ and one chiral mode at each edge.

    This is false. The charge Hall conductivity adds the two sectors, and gives $(e^2/h)(1-1)=0$. A value $e^2/h$ would need both spins to have $C=+1$.

- [x] Zero, and a helical pair of modes at each edge.

    This is true. The charge Hall conductivity is proportional to $C=0$. Each spin sector still has its own edge mode, and the two propagate in opposite directions on the same edge, which is a helical pair.

- [ ] Zero, and no edge states, since the two spins cancel.

    This is false. The cancellation is only in the charge current. Each spin sector alone is a Chern insulator with $|C|=1$ and has one edge mode, and only the sum of the two Hall conductivities vanishes.

:::

The natural mechanism that gives this opposite-sign mass is spin-orbit coupling. The relativistic spin-orbit term has the structure $\mathbf{L}\cdot\mathbf{S}$, and its $z$-component, $L_zS_z$, acts like an effective magnetic field that points in one direction for spin-up electrons and in the opposite direction for spin-down electrons. This is the opposite-sign mass structure that [(3.9)](#eq-3-9) needs, and it appears with no net magnetic field and no net breaking of time-reversal symmetry. Graphene itself, when we include its intrinsic spin-orbit coupling, which is very small, is technically a quantum spin Hall insulator through this mechanism. The effect is much larger, and accessible in experiments, in monolayer 1T$'$-WTe$_2$, where the quantum spin Hall effect survives up to 100 K.

![The two spin sectors of the quantum spin Hall insulator, computed on a zigzag ribbon with the intrinsic spin-orbit coupling $t_2=0.1$. Each sector is a Haldane model, with the phase $+\pi/2$ for spin up and $-\pi/2$ for spin down, so the two Chern numbers are opposite as in [(3.9)](#eq-3-9). The branches inside the gap are colored by the edge where they sit. Take the blue branch, which is on the lower edge. It moves to the right for spin up and to the left for spin down, and this is the helical pair of one edge.](figures/web/session03/spin_sectors.svg){#sch:s03:spin_sectors alt="Two band structures of a ribbon against the momentum, each with a blue and a red branch that cross the gap, with the slopes of the two colors reversed between the panels."}

::: {.tryit notebook="session3.ipynb" cell="The quantum spin Hall state"}
Run the cell. In the left panel the color gives the edge, top or bottom, and in the right panel it gives the spin. In the gap, take the two branches of one edge. They have opposite slopes and opposite spin, which is the helical pair of [(3.9)](#eq-3-9).
:::

::: comesback
- In Section [3.11b](#sec-3-11b) we see that the helical pair is protected by time reversal through Kramers' theorem, and not by the conservation of spin.
- In Section [5.18](#sec-5-18) the helical edge of a quantum spin Hall insulator, together with superconductivity, gives a topological superconductor.
:::
