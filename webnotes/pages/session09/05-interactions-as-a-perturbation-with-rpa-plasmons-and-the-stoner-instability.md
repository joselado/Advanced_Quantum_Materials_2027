## Interactions as a perturbation, with RPA, plasmons and the Stoner instability {#sec-9-5 number="9.5a"}

So far the perturbation has been an external impurity. However, we can also treat the electron-electron interaction *itself* as the perturbation. We use $\chi_0$, the non-interacting response that we just built, as input, and we ask for the response $\chi$ of the full interacting system. For this we need two things. The first is a rule that connects $\chi$ to $\chi_0$, and the second is a criterion to find instabilities from $\chi$.

**From $\chi_0$ to $\chi$ with the random phase approximation.** Let us take a contact interaction, of Hubbard type, with strength $U$, which couples to the density. The physical picture is a diagrammatic one. The response to a probe is the bare response $\chi_0$, plus the bare response followed by one interaction event and another bare response, plus two interaction events, and so on, which is an infinite ladder of terms. The most efficient way to include all of them is not to sum the series term by term, but to write the self-consistent equation that the full response must satisfy,

$$\chi(q,\omega) = \chi_0(q,\omega) - \chi_0(q,\omega)\, U\, \chi(q,\omega),$$

and its algebraic solution gives the **random phase approximation (RPA)**,

$$\chi(q,\omega) = \frac{\chi_0(q,\omega)}{1 + U\,\chi_0(q,\omega)}. \tag{9.6}$$

Equation [(9.6)](#eq-9-6) has a mixed character. It is derived order by order in $U$, so it is perturbative, but since we sum the whole geometric series it becomes non-perturbative. In this way it includes physics that no finite order in $U$ can give, which is a real pole, meaning a real phase transition.

**Two different sources of divergence.** The interacting response [(9.6)](#eq-9-6) can diverge for two quite different reasons. It is useful to separate them, because they correspond to two different emergent quasiparticles.

*From $\chi_0$ itself*, as in Section [9.4](#sec-9-4). This is an electron-hole excitation, which is a single-particle process that moves one electron from an occupied state to an empty state.

*From the RPA denominator*, $1+U\chi_0=0$, which is a new collective phenomenon that comes from the interaction. For a long-range Coulomb interaction, $U \to v(q)$, which depends strongly on $q$ and diverges as $q\to0$. The pole of [(9.6)](#eq-9-6) as a function of $\omega$ at fixed $q$ then defines a new quasiparticle, the **plasmon**, which is a collective charge oscillation of the whole electron gas. Its dispersion depends on the screening and on the dimensionality of the system. In the standard RPA treatment of the three-dimensional electron gas, which is the Bohm-Pines treatment, at long wavelength the dispersion has the form

$$\omega_{\rm pl}(q)^2 = \omega_p^2 + \tfrac{3}{5} v_F^2\, q^2 + O(q^4), \tag{9.7}$$

where $\omega_p$ is the classical plasma frequency. The plasmon exists even at $q=0$, which is different from the particle-hole continuum, because it is a collective mode of the whole charge density and not a single-particle excitation. Figure [9.2](#fig:s09:plasmon) shows both kinds of divergence in the same $(q,\omega)$ plane, and it shows explicitly the window at small $q$ where the pole exists and no single-particle excitation exists.

![The two divergences of the RPA response [(9.6)](#eq-9-6), drawn in the $(q,\omega)$ plane for the three-dimensional electron gas. The shaded region is where $\mathrm{Im}\,\chi_0(q,\omega)\neq 0$, which is the *particle-hole continuum*, the set of all $(q,\omega)$ at which a single electron can be moved from an occupied state $k$ to an empty state $k+q$. Its upper boundary is $\hbar\omega_+=\hbar v_Fq+\hbar^2q^2/2m$, and beyond $2k_F$ a lower boundary $\hbar\omega_-=\hbar^2q^2/2m-\hbar v_Fq$ appears. Both follow from the energy denominator of [(9.5)](#eq-9-5), and for $q<2k_F$ the continuum goes all the way down to $\omega=0$, which is the same statement as saying that $\chi_0$ is built only from states on the two sides of the Fermi surface. The plasmon [(9.7)](#eq-9-7) is a different object. It is a zero of the RPA *denominator* $1-v(q)\chi_0$, so it exists at $\omega_p$ even as $q\to 0$, in a window where no single-particle excitation exists at all. This window, marked in the figure, is the full meaning of the phrase "collective mode, not a particle-hole pair". Once the branch meets the continuum it can decay into particle-hole pairs, and it is Landau damped (dashed).](figures/s09f02_plasmon.svg){#fig:s09:plasmon number="9.2"}

::: quiz
In the density channel the interaction is repulsive, $U>0$, and $\chi_0$ is positive. How does the RPA response [(9.6)](#eq-9-6) compare with $\chi_0$ at the same $q$ and $\omega$?

- [x] It is smaller, since the denominator $1+U\chi_0$ is larger than one.
- [ ] It is larger, since the interaction enhances every response.
- [ ] It is the same, since the interaction only shifts the poles.

A repulsive interaction opposes the density change that the probe induces, which is screening. The denominator is larger than one, so $\chi<\chi_0$. The opposite happens in the spin channel, as we will see next.
:::

::: quiz
At small $q$ the particle-hole continuum of figure [9.2](#fig:s09:plasmon) shrinks towards $\omega=0$, while the plasmon of [(9.7)](#eq-9-7) stays near $\omega_p$. Why is the plasmon not damped there?

- [ ] Because the interaction vanishes at $q=0$.
- [x] Because no electron-hole pair exists at that energy, so the mode has nothing to decay into.
- [ ] Because the plasmon is a single-particle excitation, which cannot decay.

Landau damping needs a particle-hole pair with the same $q$ and $\omega$. In the window at small $q$ and large $\omega$ there is none, and the mode is sharp. Once its branch enters the continuum, it decays.
:::

The same denominator, now in the spin channel, gives the Stoner instability, and we treat it next.
