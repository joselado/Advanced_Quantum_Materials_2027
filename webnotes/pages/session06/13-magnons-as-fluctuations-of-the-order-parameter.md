## Magnons as fluctuations of the order parameter {#sec-6-13 number="6.13"}

Until now we have only asked about ground states. Let us now ask about excitations. We take the Heisenberg model [(6.5)](#eq-6-5) with $J<0$, which is ferromagnetic, and we promote the spins to real quantum operators that satisfy the angular-momentum algebra $[S_i^a,S_j^b] = i\hbar\,\delta_{ij}\epsilon^{abc}S_i^c$. From here on we set $\hbar=1$, which is the standard choice for this kind of calculation, and we ask for the low-lying excited states. In contrast with the interacting electron problem, the exact ground state of the ferromagnetic Heisenberg model is known immediately. It is the fully polarized state with all spins aligned, since for $J<0$ no other configuration can lower $\langle \mathbf S_i\cdot\mathbf
S_j\rangle$ further. A **magnon** is a small fluctuation of the magnetization that propagates on top of this fully polarized state. Qualitatively, it is a single spin tilted slightly out of alignment, delocalized coherently over the whole lattice as a wave. The question is how to obtain these excitations systematically from a many-body spin Hamiltonian. The answer is a change of variables that turns the spin problem into a bosonic tight-binding problem.

## The Holstein-Primakoff transformation {#sec-6-14 number="6.14"}

There is an exact mapping between spin operators and bosonic creation and annihilation operators $a_i^\dagger, a_i$ with $[a_i,a_j^\dagger]=\delta_{ij}$, which is called the **Holstein-Primakoff transformation**. For a spin of magnitude $S$ on site $i$, it reads

$$S_i^z = S - a_i^\dagger a_i, \qquad S_i^+ = \sqrt{2S-a_i^\dagger a_i}\;a_i, \qquad S_i^- = a_i^\dagger\sqrt{2S-a_i^\dagger a_i}. \tag{6.6}$$

This is an *exact* rewriting. If we insert [(6.6)](#eq-6-6) and use the bosonic commutation relations, we obtain exactly the full $SU(2)$ spin algebra $[S_i^z,S_i^\pm]=\pm S_i^\pm$, $[S_i^+,S_i^-]=2S_i^z$, without any approximation so far. The physical picture is direct. The operator $a_i^\dagger a_i$ counts how many units of spin have been removed from the fully polarized value $S$ on site $i$, which means that it counts the **magnons** on that site, and $S_i^z=S-a_i^\dagger a_i$ states exactly this. The square-root operators are what make [(6.6)](#eq-6-6) exact even far from full polarization. They are also the reason why the Hamiltonian, written in this form, looks more complicated and not simpler.

The simplification comes from linearizing. When the expectation value of $a_i^\dagger a_i$ stays much smaller than $S$, which means when we stay close to the fully polarized ground state, we can expand the square roots and keep only the leading term. This is the regime that we want, since we are looking for low-lying excitations above this ground state, and the result is

$$S_i^+ \approx \sqrt{2S}\, a_i, \qquad S_i^- \approx \sqrt{2S}\, a_i^\dagger, \qquad S_i^z = S - a_i^\dagger a_i. \tag{6.7}$$

This linearized form is the one that is used in practice to compute magnon spectra. The counting that follows from it is the easiest way to remember the whole transformation, so we write it out. The operator $S^+$ *raises* $S^z$, meaning that it increases the local magnetization back toward saturation, and it *destroys* a magnon. The operator $S^-$ lowers the magnetization, and it *creates* a magnon. The total magnetization of the system is the fully saturated value minus the total number of magnons, $\sum_i \langle S_i^z\rangle = NS - \sum_i\langle a_i^\dagger a_i\rangle$. Each magnon has exactly one unit of spin, so magnons are $S=1$ excitations, in agreement with what we said about them in Section [6.1](#sec-6-1). They exist only because the ground state on which they live has already broken spin-rotation symmetry spontaneously. Figure [6.5](#fig:s06:magnon) shows the three parts, which are the fully polarized ground state, the delocalized precession wave that carries a single magnon, and this rule for raising and lowering.

![The states that [(6.6)](#eq-6-6) and [(6.7)](#eq-6-7) describe. (a) The ferromagnetic ground state, where every spin has its maximal value $S^z=S$, and so there are no magnons. (b) A single magnon is *not* one spin flipped on one site. Instead, every spin is tilted slightly out of alignment and precesses on its cone, and the precession phase advances by $\mathbf
k\cdot\boldsymbol\delta$ from one site to the next. This is seen most clearly in the view from above, where the transverse component turns at a constant rate and comes back to itself after one wavelength. The missing unit of spin is therefore shared coherently by the whole lattice, and $\sum_i\langle S_i^z\rangle=NS-1$. Since the tilting angle is small, we have $\langle a_i^\dagger
a_i\rangle\ll S$ everywhere, which is the condition under which we can expand the square roots in [(6.6)](#eq-6-6). In the drawing the tilting angle is much larger than in reality. (c) The counting rule that makes the transformation easy to remember. The boson number counts the spin removed from saturation, so the *lowering* operator $S^-$ creates a magnon and the *raising* operator $S^+$ destroys one.](figures/s06f05_magnon.svg){#fig:s06:magnon number="6.5"}

::: quiz
We create one magnon on top of the saturated ferromagnet. Which operator does it, and how does the total $S^z$ change?

- [x] $S^-$ creates it, and the total $S^z$ decreases by one.
- [ ] $S^+$ creates it, and the total $S^z$ increases by one.
- [ ] $S^-$ creates it, and the total $S^z$ does not change.
- [ ] $S^+$ creates it, and the total $S^z$ decreases by one.

The boson number counts the spin removed from saturation, and $\sum_i\langle S_i^z\rangle=NS-\sum_i\langle a_i^\dagger a_i\rangle$. The lowering operator $S^-$ creates a boson, so the total $S^z$ drops by one unit.
:::

We insert [(6.7)](#eq-6-7) into the ferromagnetic Heisenberg Hamiltonian, $H = J\sum_{\langle ij\rangle}
\mathbf S_i\cdot\mathbf S_j = J\sum_{\langle ij\rangle}\big[S_i^zS_j^z + \tfrac12(S_i^+S_j^-+S_i^-S_j^+)\big]$, and we keep the terms up to quadratic order in the bosonic operators,

$$S_i^zS_j^z \approx S^2 - S\big(a_i^\dagger a_i + a_j^\dagger a_j\big), \qquad
\tfrac12\big(S_i^+S_j^- + S_i^-S_j^+\big) \approx S\big(a_i^\dagger a_j + a_j^\dagger a_i\big),$$

and in this way the spin Hamiltonian becomes a bosonic tight-binding Hamiltonian for magnons, and its hopping amplitude is set directly by the exchange coupling $J$, as we said before. The magnon "hops" between sites with an amplitude proportional to $JS$, in direct analogy with the electronic tight-binding Hamiltonians that we have diagonalized during the whole course.
