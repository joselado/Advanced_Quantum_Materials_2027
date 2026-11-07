## Closing summary {#sec-5-20 number="5.20"}

This session used three tools from before. These are the mean-field theory of Section [1.12](#sec-1-12), the pairing term and the broken gauge symmetry of Section [1.15](#sec-1-15), and the Chern number [(3.4)](#eq-3-4) and the SSH model of Section [3.9](#sec-3-9) from Session 3. With them we found the following results.

- **Superconductivity is a mean-field, attractive-interaction phenomenon.** Starting from an attractive Hubbard chain [(5.2)](#eq-5-2), pairing mean-field theory gives the order parameter $\Delta_n = U\langle c_{n\downarrow}c_{n\uparrow}\rangle$ [(5.3)](#eq-5-3) and the mean-field Hamiltonian [(5.4)](#eq-5-4).

- **Pairing breaks particle-number conservation down to parity**, as we saw in Section [5.6](#sec-5-6), and this is the same as the statement that gauge symmetry is spontaneously broken. The pairing term gets a phase $e^{-2i\varphi}$ under the gauge transformation [(5.5)](#eq-5-5), unlike ordinary bilinear terms.

- **Flux quantization**, $\Phi = n\, h/2e$ [(5.1)](#eq-5-1), is a direct and measurable macroscopic consequence of this broken gauge symmetry, at the same level as the conductance quantum of the quantum Hall effect of Session 4.

- **The Nambu spinor [(5.6)](#eq-5-6) and the Bogoliubov-de Gennes Hamiltonian [(5.7)](#eq-5-7) and [(5.8)](#eq-5-8)** are the tools that allow us to diagonalize any mean-field superconducting Hamiltonian. They give the quasiparticle dispersion $E(\mathbf k) = \pm\sqrt{\varepsilon(\mathbf k)^2 + |\Delta(\mathbf k)|^2}$ [(5.9)](#eq-5-9), and a gap opens at the original Fermi surface regardless of the details of the microscopic dispersion.

- **The symmetry of $\Delta(\mathbf k)$ classifies the superconductor.** It can be singlet, even in $\mathbf
  k$, or triplet, odd in $\mathbf k$, as in [(5.11)](#eq-5-11) and [(5.12)](#eq-5-12), with a further classification by angular momentum ($L=0,1,2,\dots$) [(5.14)](#eq-5-14) that gives s-, p- and d-wave order. The last one is realized in the cuprate high-$T_c$ superconductors through the nodal $d_{x^2-y^2}$ gap [(5.13)](#eq-5-13).

- **Gaps with the same spectrum can have different topology.** Trivial s-wave pairing ($C=0$) and chiral p-wave pairing [(5.15)](#eq-5-15) ($C=\pm2$) both fully gap the same Fermi surface. Only the topological one has gapless edge modes, which is the bulk-boundary correspondence of Section [3.7](#sec-3-7).

- **The Kitaev chain [(5.19)](#eq-5-19) is the SSH model in Majorana language.** At the fine-tuned point it reduces to $H = it\sum_n \gamma_{2n}\gamma_{2n+1}$ [(5.21)](#eq-5-21), which leaves two unpaired end Majoranas with zero energy. These survive away from the fine-tuned point in the whole topological phase $|\mu|<2t$ [(5.22)](#eq-5-22).

- **Majoranas are non-Abelian anyons.** Braiding them acts as a unitary [(5.23)](#eq-5-23) on a topologically degenerate ground-state manifold. Exchanges that share a Majorana do not commute, which is the basis of the proposed schemes for topological quantum computing.

![The two gaps of Section [5.14](#sec-5-14) once more. The phase of $\Delta(\mathbf k)$ does not wind for $s$-wave pairing and winds once for $p+ip$ pairing. The Chern number counts this winding once for each of the two spin blocks, which gives $C=\pm2$.](figures/s05f04_topology.svg){alt="Phase dials of the pairing function around a Fermi pocket for s-wave and chiral p-wave pairing, and the edge of a ribbon for each."}

::: quiz
In a spinless chain the onsite term $c_nc_n$ vanishes. Which pairing is then allowed, and what is its parity?

- [ ] Onsite pairing, which is even in $k$.

    This is false. The onsite term is $c_nc_n=0$ by the Pauli principle. If we write $\sum_k c_kc_{-k}$ we get zero as well, since $c_kc_{-k}=-c_{-k}c_k$ cancels pairs of terms.

- [x] Pairing on the bond $c_nc_{n+1}$, which is odd in $k$.

    This is true. The Pauli principle gives $c_n^2=0$, so the pairing lives on a bond. It gives $\Delta(k)=2i\Delta\sin k$, which is odd, so by [(5.12)](#eq-5-12) it is a spinless $p$-wave state.

- [ ] Pairing on the bond, which is even in $k$.

    This is false. The bond term $c_nc_{n+1}$ changes sign when we exchange the two fermions, so it can only give $\sin k$. A $\cos k$ function would multiply $c_kc_{-k}$ and cancel, as the sum vanishes by antisymmetry.
:::

In this session we followed superconductivity from the bare pairing order parameter of Session 1 to Nambu spinors, Bogoliubov-de Gennes Hamiltonians, the singlet and triplet classification and the Majorana zero modes of the Kitaev chain. The other branch of the Hubbard model, with $U>0$, gives magnetism, where time-reversal symmetry is broken instead of gauge symmetry. Session 6 starts from the same chain as [(5.2)](#eq-5-2), now on its repulsive side, and gives magnetism the same depth of treatment.

::: comesback
- In Section [6.3](#sec-6-3) the Hubbard chain comes back with $U>0$, and the magnetization takes the place of $\Delta$ as the order parameter.
- In Section [6.15](#sec-6-15) the magnons of an antiferromagnet need a Bogoliubov transformation, as the BdG Hamiltonian does here.
- In Section [8.6](#sec-8-6) a BCS state of spinons, written in Nambu space, is the first guess for a quantum spin liquid.
- In Section [9.7](#sec-9-7) and Section [9.8](#sec-9-8) magnetic impurities and vacancies tell an $s$-wave superconductor apart from a topological one.
:::
