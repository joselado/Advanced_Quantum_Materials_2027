## Closing summary {#sec-5-20 number="5.20"}

- **Superconductivity is a mean-field, attractive-interaction phenomenon.** Starting from an attractive Hubbard chain [(5.2)](#eq-5-2), pairing mean-field theory gives the order parameter $\Delta_n = U\langle c_{n\downarrow}c_{n\uparrow}\rangle$ [(5.3)](#eq-5-3) and the mean-field Hamiltonian [(5.4)](#eq-5-4).

- **Pairing breaks particle-number conservation down to parity** (section [5.6](#sec-5-6)), and this is the same as the statement that gauge symmetry is spontaneously broken. The pairing term gets a phase $e^{-2i\varphi}$ under the gauge transformation [(5.5)](#eq-5-5), unlike ordinary bilinear terms.

- **Flux quantization**, $\Phi = n\, h/2e$ [(5.1)](#eq-5-1), is a direct and measurable macroscopic consequence of this broken gauge symmetry, at the same level as the conductance quantum of the quantum Hall effect from earlier sessions.

- **The Nambu spinor [(5.6)](#eq-5-6) and the Bogoliubov-de Gennes Hamiltonian [(5.7)](#eq-5-7)-[(5.8)](#eq-5-8)** are the tools that allow us to diagonalize any mean-field superconducting Hamiltonian. They give the quasiparticle dispersion $E(\mathbf k) = \pm\sqrt{\varepsilon(\mathbf k)^2 + |\Delta(\mathbf k)|^2}$ [(5.9)](#eq-5-9), and a gap opens at the original Fermi surface regardless of the details of the microscopic dispersion.

- **The symmetry of $\Delta(\mathbf k)$ classifies the superconductor.** It can be singlet, even in $\mathbf
  k$, or triplet, odd in $\mathbf k$, as in [(5.11)](#eq-5-11)-[(5.12)](#eq-5-12), with a further classification by angular momentum ($L=0,1,2,\dots$) [(5.14)](#eq-5-14) that gives s-, p- and d-wave order. The last one is realized in the cuprate high-$T_c$ superconductors through the nodal $d_{x^2-y^2}$ gap [(5.13)](#eq-5-13).

- **Gaps with the same spectrum can have different topology.** Trivial s-wave ($C=0$) and chiral p-wave ($C=\pm2$, eq. [5.15](#eq-5-15)) pairing both fully gap the same Fermi surface, but only the topological one has gapless edge modes, which is the bulk-boundary logic of the Chern number from the topological-band-structure and quantum-Hall sessions.

- **The Kitaev chain [(5.19)](#eq-5-19) is the SSH model in Majorana language.** At the fine-tuned point it reduces to $H = it\sum_n \gamma_{2n}\gamma_{2n+1}$ [(5.21)](#eq-5-21), which leaves two unpaired end Majoranas with zero energy. These survive away from the fine-tuned point in the whole topological phase $|\mu|<2t$ [(5.22)](#eq-5-22).

- **Majoranas are non-Abelian anyons.** Braiding them acts as a unitary [(5.23)](#eq-5-23) on a topologically degenerate ground-state manifold, and exchanges that share a Majorana do not commute, which is the basis of the proposed schemes for topological quantum computing. This last part is material from the slides and the transcript, with no counterpart in the notebook.

In this session we followed the topic of superconductivity from session 1, from the bare pairing order parameter to Nambu spinors, Bogoliubov-de Gennes Hamiltonians, the singlet and triplet classification and finally Majorana zero modes in the Kitaev chain. The division that we made in session 1 had a second branch that we have not considered since its first short treatment, which is magnetism, where time-reversal symmetry is broken instead of gauge symmetry. This is where we go next. Session 6 comes back to the same Hubbard Hamiltonian that opened section [5.5](#sec-5-5) of this session, now on its repulsive ($U>0$) side, and gives magnetism the same depth of treatment that we have now given to superconductivity.
