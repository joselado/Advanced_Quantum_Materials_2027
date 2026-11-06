## Interactions as a perturbation, with RPA, plasmons and the Stoner instability {#sec-9-5 number="9.5"}

So far the perturbation has been an external impurity. However, we can also treat the electron-electron interaction *itself* as the perturbation. We use $\chi_0$, the non-interacting response that we just built, as input, and we ask for the response $\chi$ of the full interacting system. For this we need two things. The first is a rule that connects $\chi$ to $\chi_0$, and the second is a criterion to find instabilities from $\chi$.

**From $\chi_0$ to $\chi$ with the random phase approximation.** Let us take a contact interaction, of Hubbard type, with strength $U$, which couples to the density. The physical picture is a diagrammatic one. The response to a probe is the bare response $\chi_0$, plus the bare response followed by one interaction event and another bare response, plus two interaction events, and so on, which is an infinite ladder of terms. The most efficient way to include all of them is not to sum the series term by term, but to write the self-consistent equation that the full response must satisfy,

$$\chi(q,\omega) = \chi_0(q,\omega) - \chi_0(q,\omega)\, U\, \chi(q,\omega),$$

and its algebraic solution gives the **random phase approximation (RPA)**,

$$\chi(q,\omega) = \frac{\chi_0(q,\omega)}{1 + U\,\chi_0(q,\omega)}. \tag{9.6}$$

Equation [(9.6)](#eq-9-6) has a mixed character. It is derived order by order in $U$, so it is perturbative, but since we sum the whole geometric series it becomes non-perturbative. In this way it includes physics that no finite order in $U$ can give, which is a real pole, meaning a real phase transition.

**Two different sources of divergence.** The interacting response [(9.6)](#eq-9-6) can diverge for two quite different reasons. It is useful to separate them, because they correspond to two different emergent quasiparticles.

*From $\chi_0$ itself*, as in Section [9.4](#sec-9-4) This is an electron-hole excitation, which is a single-particle process that moves one electron from an occupied state to an empty state.

*From the RPA denominator*, $1+U\chi_0=0$, which is a new collective phenomenon that comes from the interaction. For a long-range Coulomb interaction, $U \to v(q)$, which depends strongly on $q$ and diverges as $q\to0$. The pole of [(9.6)](#eq-9-6) as a function of $\omega$ at fixed $q$ then defines a new quasiparticle, the **plasmon**, which is a collective charge oscillation of the whole electron gas. Its dispersion depends on the screening and on the dimensionality of the system. In the standard RPA treatment of the three-dimensional electron gas, which is the Bohm-Pines treatment, at long wavelength the dispersion has the form

$$\omega_{\rm pl}(q)^2 = \omega_p^2 + \tfrac{3}{5} v_F^2\, q^2 + O(q^4), \tag{9.7}$$

where $\omega_p$ is the classical plasma frequency. The plasmon exists even at $q=0$, which is different from the particle-hole continuum, because it is a collective mode of the whole charge density and not a single-particle excitation. Figure [9.2](#fig:s09:plasmon) shows both kinds of divergence in the same $(q,\omega)$ plane, and it shows explicitly the window at small $q$ where the pole exists and no single-particle excitation exists.

![The two divergences of the RPA response [(9.6)](#eq-9-6), drawn in the $(q,\omega)$ plane for the three-dimensional electron gas. The shaded region is where $\mathrm{Im}\,\chi_0(q,\omega)\neq 0$, which is the *particle-hole continuum*, the set of all $(q,\omega)$ at which a single electron can be moved from an occupied state $k$ to an empty state $k+q$. Its upper boundary is $\hbar\omega_+=\hbar v_Fq+\hbar^2q^2/2m$, and beyond $2k_F$ a lower boundary $\hbar\omega_-=\hbar^2q^2/2m-\hbar v_Fq$ appears. Both follow from the energy denominator of [(9.5)](#eq-9-5), and for $q<2k_F$ the continuum goes all the way down to $\omega=0$, which is the same statement as saying that $\chi_0$ is built only from states on the two sides of the Fermi surface. The plasmon [(9.7)](#eq-9-7) is a different object. It is a zero of the RPA *denominator* $1-v(q)\chi_0$, so it exists at $\omega_p$ even as $q\to 0$, in a window where no single-particle excitation exists at all. This window, marked in the figure, is the full meaning of the phrase "collective mode, not a particle-hole pair". Once the branch meets the continuum it can decay into particle-hole pairs, and it is Landau damped (dashed).](figures/s09f02_plasmon.svg){#fig:s09:plasmon number="9.2"}

**The Stoner criterion as an instability of the response function.** Now we use the same RPA logic in the *spin* channel of an interaction of Hubbard type, so that $\chi_0$ in [(9.6)](#eq-9-6) becomes the non-interacting spin susceptibility. The sign is the opposite of the density channel, because $U n_\uparrow n_\downarrow = \tfrac{U}{4}(n^2 - m^2)$ is repulsive for the density and attractive for the magnetization, so the same $U$ screens the charge response and enhances the spin response, and the denominator of [(9.6)](#eq-9-6) becomes $1-U\chi_0$. The interacting spin response diverges when

$$U\, \chi_0(q,0) = 1. \tag{9.8}$$

At $q=0$ we use the limit $q\to0$ of [(9.4)](#eq-9-4), $\chi_0(0,0) = D(E_F)$, so [(9.8)](#eq-9-8) becomes $U\,D(E_F) = 1$. This is exactly the **Stoner criterion** for itinerant ferromagnetism, which says that an interacting metal becomes magnetic once the product of the density of states at the Fermi level and the interaction strength is larger than one. However, [(9.8)](#eq-9-8) is more general than the special case $q=0$. For a Fermi surface with strong nesting, such as the half-filled square lattice of Section [9.4](#sec-9-4), $\chi_0(q,0)$ has its *maximum* not at $q=0$ but at the nesting vector $Q=(\pi,\pi)$, where it is already logarithmically enhanced. The instability threshold in [(9.8)](#eq-9-8) is then reached first at $Q=(\pi,\pi)$ and not at $q=0$. As a result, the system develops a *staggered* antiferromagnetic instability and not a uniform ferromagnetic one, and this happens at a smaller value of $U$ than the simple Stoner estimate predicts.

This is the connection that the course has been preparing. In Sessions 1 and 6 we obtained magnetism by writing the Hubbard model, applying mean-field theory directly to the *ordered* state, and solving self-consistently for a non-zero magnetization $m$, as in Equation [1.7](#eq-1-7) of Section [1.14](#sec-1-14) In this session we have obtained the *same physics*, with the same threshold $U\,D(E_F)=1$ and the same preference for antiferromagnetism at half filling, without writing any ordered mean-field ansatz. Instead, we asked when the *paramagnetic*, disordered response function develops a divergence, which is the same logic as the classical susceptibility of Section [9.2](#sec-9-2) Mean-field theory and the response function are two ways to reach the same instability. The first one computes it from the side where the symmetry is broken, and the second one computes it only from the symmetric side, by following how this state becomes unstable.

The same method, applied to different response channels and to different signs of the interaction, classifies a whole family of instabilities, which we write here explicitly. On the slides this classification into three cases is presented as a clear summary table, in a more systematic way than in the spoken lecture, which mainly worked out the magnetic case in detail.

::: center
  Instability                          Response channel                        Interaction sign
  ------------------------------------ --------------------------------------- ------------------
  Magnetism                            spin response                           repulsive
  Dimerization / charge density wave   charge-phonon response                  repulsive
  Superconductivity                    electron-electron scattering response   attractive
:::

::: notebookbox
**Notebook check-in:** [`session9.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session9.ipynb), "The charge-charge response function" (Challenge)

The same notebook section that we used above for nesting is extended, in its second part, to the interacting case. You add a Hubbard interaction $U$ and an external staggered, antiferromagnetic field to a dimerized chain, and you look at what happens to the response as $U$ increases. This is the version of equation [(9.8)](#eq-9-8) on the scale of a notebook, where the Stoner instability appears when $U$ goes above the threshold set by $\chi_0$.
:::
