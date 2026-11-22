## The Stoner instability {#sec-9-5b number="9.5b"}

When does the spin response of a metal diverge, and at which wavevector $q$? We will now see that the random phase approximation, applied to the spin channel, gives the condition $U\chi_0(q,0)=1$ of [(9.8)](#eq-9-8). At $q=0$ it is the Stoner criterion $UD(E_F)=1$ of a ferromagnet, and on the nested Fermi surface of the half-filled square lattice it is met first at $Q=(\pi,\pi)$, which gives an antiferromagnet.

::: {.recall eq="9.6"}
This is the random phase approximation of Section [9.5a](#sec-9-5), the response $\chi$ of the interacting system built from the bare Lindhard function $\chi_0$ and a contact interaction $U$ of Hubbard type. In the density channel the static $\chi_0$ is positive, so the denominator $1+U\chi_0$ is larger than one and the interaction screens the charge response. In Session 6 we found the Stoner criterion [(6.3)](#eq-6-3), $UD(E_F)\geq1$, in another way, from the self-consistent magnetization.
:::

**The Stoner criterion as an instability of the response function.** Now we use the same RPA logic in the *spin* channel of an interaction of Hubbard type. Then $\chi_0$ in [(9.6)](#eq-9-6) becomes the non-interacting spin susceptibility. The sign is the opposite of the density channel, because $U n_\uparrow n_\downarrow = \tfrac{U}{4}(n^2 - m^2)$ is repulsive for the density and attractive for the magnetization. So the same $U$ screens the charge response and enhances the spin response, and the denominator of [(9.6)](#eq-9-6) becomes $1-U\chi_0$.

::: key
The interacting spin response diverges when

$$U\, \chi_0(q,0) = 1. \tag{9.8}$$

As $U$ grows, the paramagnet becomes unstable first at the $q$ where $\chi_0(q,0)$ is largest. A maximum at $q=0$ gives a ferromagnet, and a maximum at $Q=(\pi,\pi)$ gives an antiferromagnet.
:::

::: {.steps title="From the Hubbard term to the spin denominator"}
We use the identity of one site $Un_\uparrow n_\downarrow=\tfrac U4(n^2-m^2)$, with $n=n_\uparrow+n_\downarrow$ and $m=n_\uparrow-n_\downarrow$, which the problem below shows. Let us take the simplest case first, a uniform field $h$ that enters the Hamiltonian as $-h\sum_i m_i$. It lowers the energy of spin up by $h$ and raises the energy of spin down by $h$. In mean field the quartic term $-\tfrac U4m_i^2$ becomes

$$-\frac U4\,m_i^2 \;\to\; -\frac U2\,\langle m\rangle\, m_i + \frac U4\,\langle m\rangle^2,$$

which has the form of the field term. So each electron feels the field

$$h_{\rm eff}=h+\frac U2\,\langle m\rangle,$$

which is the external field plus the exchange field of the magnetization that it induces. Without interaction, a band that moves down by $h_{\rm eff}$ at a fixed chemical potential gains $D(E_F)\,h_{\rm eff}=\chi_0(0,0)\,h_{\rm eff}$ electrons per site. The band of spin up gains this number and the band of spin down loses it, so

$$\langle m\rangle = 2\chi_0\left(h+\frac U2\,\langle m\rangle\right), \qquad \langle m\rangle=\frac{2\chi_0\,h}{1-U\chi_0}.$$

The factor $2$ counts the two spins. It drops out of the ratio to the response $2\chi_0h$ without interaction, which is $1/(1-U\chi_0)$, and this ratio diverges at $U\chi_0(0,0)=1$, which is [(9.8)](#eq-9-8) at $q=0$. A field $h\cos(q\cdot r_i)$ that changes from site to site gives the same two lines with $\chi_0(q,0)$, since in a clean metal each $q$ responds alone. In the density channel the term $+\tfrac U4n_i^2$ has the opposite sign, and it gives the denominator $1+U\chi_0$ of [(9.6)](#eq-9-6).
:::

At $q=0$ we use the limit $q\to0$ of [(9.4)](#eq-9-4), $\chi_0(0,0) = D(E_F)$, so [(9.8)](#eq-9-8) becomes $U\,D(E_F) = 1$. This is the **Stoner criterion** for itinerant ferromagnetism, which we wrote in Session 6 as $U\,D(E_F)\geq1$ in [(6.3)](#eq-6-3), where we found it from the self-consistent magnetization. It says that an interacting metal becomes magnetic once the product of the density of states at the Fermi level and the interaction strength is larger than one.

However, [(9.8)](#eq-9-8) is more general than the special case $q=0$. For a Fermi surface with strong nesting, such as the half-filled square lattice of Section [9.4b](#sec-9-4b), $\chi_0(q,0)$ has its *maximum* not at $q=0$ but at the nesting vector $Q=(\pi,\pi)$, where it is already enhanced. At half filling $\chi_0(\pi,\pi)$ grows as the square of a logarithm, $\ln^2(1/T)$, as we cool down, while $\chi_0(0,0)$ grows only as $\ln(1/T)$. The instability threshold in [(9.8)](#eq-9-8) is then reached first at $Q=(\pi,\pi)$ and not at $q=0$. As a result, the system develops a *staggered* antiferromagnetic instability and not a uniform ferromagnetic one, and this happens at a smaller value of $U$ than the simple Stoner estimate predicts. The two patterns are drawn in [](#sch:s09:spin_patterns), and the Fermi surface that favors the second one is shown again below.

![The two spin patterns that the static spin response can favor. A response at $q=0$ builds a uniform magnetization. A response at $Q=(\pi,\pi)$ builds a magnetization that changes sign from site to site, which a uniform field does not feel.](figures/web/session09/spin_patterns.svg){#sch:s09:spin_patterns alt="A square lattice with all spins up, next to a square lattice with spins alternating up and down like a checkerboard."}

![At half filling the vector $Q$ maps whole edges of the diamond onto each other.](figures/s09f01_nesting.svg){panel="c" alt="The diamond Fermi surface of the half-filled square lattice with the vector Q joining parallel edges."}

![The static response $\chi_0(q,0)$ of the half-filled square lattice, from [(9.4)](#eq-9-4) with $T=0.1t$ on a $240\times240$ k-mesh, along the path $\Gamma$, $X$, $M$, $\Gamma$, in units of $1/t$. The criterion [(9.8)](#eq-9-8) is met when $1/U$ reaches the curve. The maximum is at $M=(\pi,\pi)$ with $\chi_0=0.68/t$, and at $\Gamma$ the value is $D(E_F)\approx0.26/t$. Here $D(E_F)$ is the density of states averaged over the thermal window at $T=0.1t$, since at half filling $D(E)$ itself diverges at $E=0$. The red line is met first, so the antiferromagnetic instability appears at $U\approx1.5t$, and the ferromagnetic one needs $U\approx3.8t$.](figures/web/session09/stoner.svg){#sch:s09:stoner alt="A curve of the static response along a path in the Brillouin zone, with a sharp maximum at the corner M and two horizontal lines at the heights 0.26 and 0.68 of the ferromagnetic and the antiferromagnetic thresholds."}

This is the connection that the course has been preparing. In Session 1 and Session 6 we obtained magnetism from the Hubbard model [(1.7)](#eq-1-7). We applied mean-field theory directly to the *ordered* state and solved self-consistently for a non-zero magnetization $m$, in Section [1.14](#sec-1-14) and in Section [6.6](#sec-6-6). In this session we have obtained the *same physics*, with the same threshold $U\,D(E_F)=1$ and the same preference for antiferromagnetism at half filling, without writing any ordered mean-field ansatz. Instead, we asked when the *paramagnetic*, disordered response function develops a divergence, which is the same logic as the classical susceptibility of Section [9.2](#sec-9-2). Mean-field theory and the response function are two ways to reach the same instability. The first one computes it from the side where the symmetry is broken, and the second one computes it only from the symmetric side, by following how this state becomes unstable.

The same method, applied to different response channels and to different signs of the interaction, classifies a whole family of instabilities, which the table below lists. We worked out the magnetic case in detail, and the other two lines are the charge density wave of Section [1.13](#sec-1-13) and the superconductivity of Session 5, with the attractive interaction of Section [5.4](#sec-5-4).

::: center
  Instability                          Response channel                        Interaction sign
  ------------------------------------ --------------------------------------- ------------------
  Magnetism                            spin response                           repulsive
  Dimerization / charge density wave   charge-phonon response                  repulsive
  Superconductivity                    electron-electron scattering response   attractive
:::

::: lab
Neutron diffraction measurements on single crystals of Cr$_{1-x}$V$_x$ show that the ordering moment and the Néel temperature are continuously suppressed as $x$ approaches $0.037$, a proposed quantum critical point. At the same time the wavevector of the spin density wave becomes more incommensurate as $x$ grows. At $x_c=0.037$ the authors find elastic scattering at four incommensurate wavevectors $Q=(1\pm\delta_{1,2},0,0)\,2\pi/a$, which correspond to two spin density waves with Néel temperatures of $19$ K and $300$ K. They write that tuning Cr to this point does not suppress the antiferromagnetism, but gives a new spin order due to a new nesting of the Fermi surface of Cr. The measurement is in [this article](https://arxiv.org/abs/0807.3586). Our reading is that [(9.8)](#eq-9-8) is met first at a nesting vector of the Fermi surface of Cr, which is neither $q=0$ nor a commensurate vector. So the order is a spin density wave with an incommensurate period, and not the ferromagnet of $q=0$ or the staggered order at $(\pi,\pi)$ of the square lattice of this page.
:::

::: quiz
For the half-filled square lattice we have $\chi_0(0,0)=0.26/t$ and $\chi_0(\pi,\pi)=0.68/t$ at $T=0.1t$. With [(9.8)](#eq-9-8), where does the first instability appear as we increase $U$?

- [ ] At $U\approx3.8t$, and it is ferromagnetic.

    This is false. The value $U=3.8t$ is $1/0.26t$, which is the threshold for the ferromagnetic channel. At $U=1.5t$ the antiferromagnetic channel already satisfies $U\chi_0(\pi,\pi)=1$, so the instability appears earlier.

- [x] At $U\approx1.5t$, and it is antiferromagnetic.

    This is true. The condition $U\chi_0(q,0)=1$ is first met at the largest $\chi_0$. At $Q=(\pi,\pi)$ we get $U=1/0.68t\approx1.5t$, and the response there is staggered.

- [ ] At $U\approx1.5t$, and it is ferromagnetic.

    This is false. At $U=1.5t$ the ferromagnetic channel gives $U\chi_0(0,0)=1.5\times0.26=0.39$, which is far from one. The ferromagnetic instability needs a larger $U$.
:::

::: quiz
The same $U$ reduces the charge response and enhances the spin response. Which relation explains this?

- [ ] The charge channel has the denominator $1-U\chi_0$ because it conserves particle number.

    This is false. Particle conservation holds for both channels, so it cannot decide. If the charge denominator were $1-U\chi_0$, then $U=1.5t$ would give a charge divergence at $Q$ for a repulsive $U$, which does not occur.

- [x] The identity $Un_\uparrow n_\downarrow=\tfrac{U}{4}(n^2-m^2)$ makes the interaction repulsive for $n$ and attractive for $m$.

    This is true. The identity gives $+\tfrac U4 n^2$ and $-\tfrac U4 m^2$. The charge denominator is $1+U\chi_0$, which is $1.68$ at $U=t$ and $\chi_0=0.68/t$, and the spin one is $1-U\chi_0=0.32$.

    ![The factor of [(9.6)](#eq-9-6) in the two channels, with the point $U\chi_0=0.68$ for $U=t$. The charge response drops to $0.60$ of $\chi_0$ and the spin response grows to $3.1$ times $\chi_0$.](figures/web/session09/rpa_factor.svg){alt="The ratio of the interacting to the bare response against U chi zero, falling slowly for the charge channel and diverging at one for the spin channel."}

- [ ] The spin response has no interaction contribution, so it stays at $\chi_0$.

    This is false. If the spin response stayed at $\chi_0$, there would be no Stoner instability at any $U$. The ferromagnet that appears above $U=1/\chi_0(0,0)$ would not exist.
:::

::: quiz
Each curve is $\chi_0(q,0)$ of the square lattice at one filling, at $T=0.1t$. It is in units of $1/t$, along the path $\Gamma$, $X$, $M$, $\Gamma$. As we increase $U$, the spin response first diverges where

$$U\,\chi_0(q,0)=1.$$

Which metal becomes an antiferromagnet with $Q=(\pi,\pi)$, the point $M$?

- [ ] ![A curve of chi zero along Gamma, X, M, Gamma with its highest point on the line from X to M, a dip at M and a lower peak after M.](figures/web/session09/g3_quiz_chi0_incomm.svg)

    This is false. The maximum is on the line from $X$ to $M$, at about $(\pi,0.6\pi)$, with $0.25/t$, while at $M$ the curve has only $0.16/t$. So the first instability, at $U\approx3.9t$, is a spin density wave with an incommensurate wavevector. This metal has $\mu=-t$.

- [x] ![A curve of chi zero along Gamma, X, M, Gamma with a sharp maximum at M.](figures/web/session09/g3_quiz_chi0_half.svg)

    This is true. The maximum is at $M=(\pi,\pi)$, with $0.68/t$ against $0.26/t$ at $\Gamma$. So $U\chi_0(q,0)=1$ is first met at $M$, at $U\approx1.5t$, and the order is staggered. This is the half-filled lattice, whose Fermi surface is the nested diamond.

- [ ] ![A low curve of chi zero along Gamma, X, M, Gamma, flat near Gamma, lower at X and lowest at M.](figures/web/session09/g3_quiz_chi0_low.svg)

    This is false. The curve stays between $0.09/t$ and $0.10/t$ on the first half of the path from $\Gamma$ to $X$, and it is only $0.025/t$ at $M$. The small Fermi surface has no nesting at $(\pi,\pi)$, and the threshold is about $U\approx10t$. This metal has $\mu=-3t$, with a small Fermi circle around $\Gamma$.
:::

:::: problem
Show that $Un_\uparrow n_\downarrow=\tfrac U4(n^2-m^2)$ on one site, with $n=n_\uparrow+n_\downarrow$ and $m=n_\uparrow-n_\downarrow$. Then take the half-filled chain $\varepsilon(k)=-2t\cos k$, with $\chi_0(0,0)=D(E_F)=1/(2\pi t)$ per spin. At which $U$ does [(9.8)](#eq-9-8) hold at $q=0$? Why is the instability at $q=\pi$ met first at low temperature?

::: solution
For a fermion $n_\sigma^2=n_\sigma$, since the occupation is $0$ or $1$. So $n^2=n_\uparrow+n_\downarrow+2n_\uparrow n_\downarrow$ and $m^2=n_\uparrow+n_\downarrow-2n_\uparrow n_\downarrow$, and the difference is $n^2-m^2=4n_\uparrow n_\downarrow$. On the four states of the site, $|0\rangle$, $|\uparrow\rangle$, $|\downarrow\rangle$ and $|\uparrow\downarrow\rangle$, both sides give $0$, $0$, $0$ and $U$.

At $q=0$ the condition is $U=1/D(E_F)=2\pi t\approx6.28t$, the value of the Stoner criterion of Session 6 for this chain. At $q=\pi$ the two Fermi points $\pm\pi/2$ are joined by $2k_F=\pi$, and $\chi_0$ at $q=\pi$ grows as $D(E_F)\ln(1/T)$ as we cool down. It is $0.86/t$ at $T=0.02t$, $0.97/t$ at $T=0.01t$ and $1.08/t$ at $T=0.005t$. So the condition at $q=\pi$ is met at $U=1.16t$, $1.03t$ and $0.92t$, and this value goes to zero as $T\to0$. In mean field the half-filled chain then becomes an antiferromagnet at any $U>0$, long before the ferromagnet of $q=0$.

In a calculation this means that we compute $\chi_0(q,0)$ on a k-path first. The position of its maximum tells which ordered state to start from in a self-consistent loop.
:::
::::

::: {.tryit notebook="session9.ipynb" cell="The charge-charge response function"}
Go to the second cell of this section, which adds the interaction $U$ to the chain of `geometry.bichain()`, a chain with two sites in its cell and equal hoppings, and solves it in mean field. Run it with `U = 2.0` and compare the two response panels. Without RPA the low-energy weight near $q=0$ is small. With RPA a strong peak appears there at low energy. Then set `U = 0.5` and check that the enhancement is much weaker.
:::

::: notebookbox
**Notebook check-in:** [`session9.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session9.ipynb), "The charge-charge response function" (Challenge)

The same notebook section that we used above for nesting is extended, in its second part, to the interacting case. You add a Hubbard interaction $U$ to the chain of `geometry.bichain()`, which has two sites in its cell and equal hoppings. You solve it in mean field from an antiferromagnetic starting guess, and you look at what happens to the response as $U$ increases. This is the version of equation [(9.8)](#eq-9-8) on the scale of a notebook. At half filling $\chi_0$ of this chain diverges at $q=\pi$ as $T\to0$, so in mean field it orders at any $U>0$, as the problem above finds. At small $U$ the gap is then set by the k-mesh of the cell, `nk = 100`, and it becomes smaller as the mesh grows.
:::

::: comesback
- In Section [9.6](#sec-9-6) we leave the interaction aside and take a real impurity as the perturbation, with the same $\chi_0$.
- In Section [9.11](#sec-9-11) the Stoner criterion is the result that joins this session to the magnetism of Session 1 and Session 6.
:::
