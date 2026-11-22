## Impurities as diagnostics I, Friedel oscillations in a metal {#sec-9-6 number="9.6a"}

How does the density around one impurity in a metal decay, and what does this decay tell us about the metal? We will now see that it oscillates with the wavevector $2k_F$, the diameter of the Fermi surface, under an envelope that falls as $1/|x|^d$ in $d$ dimensions. This is the Friedel oscillation [(9.9)](#eq-9-9).

::: {.recall eq="9.4"}
This is the static Lindhard function of Section [9.4a](#sec-9-4). The sum runs over the $N$ momenta $k$ of the Brillouin zone, $\varepsilon(k)$ is the band and $n_F$ is the Fermi-Dirac function. Only pairs of states on the two sides of the Fermi surface contribute, $\chi_0(q)$ is positive, and at $q\to0$ it is the density of states $D(E_F)$.
:::

A real local impurity is the most physical realization of a perturbation. Four case studies follow, one for each broad class of ground state that we have built in the course. These are metals, superconductors, topological matter and quantum magnets. In each case the diagnostic logic is the same. We perturb the system locally, and we obtain the nature of the ground state from how the effect of the perturbation decays in space.

Let us start with a metal. An impurity is a local shift of the onsite energy. If we add one to a Hamiltonian with translational symmetry, this symmetry is necessarily broken. Note, however, that perturbation theory itself never needed translational symmetry, since equations [(9.2)](#eq-9-2) and [(9.3)](#eq-9-3) are valid for any $H_0$ and any $V$. If we apply them directly to the local density of states, we obtain a response that is proportional to matrix elements between states at the Fermi surface. For a generic band, close to a parabolic one, the oscillation that results is set only by the Fermi wavevector.

To see this in an exact way, note that the static Lindhard function of a one-dimensional free-electron gas has the closed form

$$\chi_0(q) = \frac{m}{\pi\hbar^2 q}\ln\left|\frac{2k_F + q}{2k_F - q}\right|,$$

which is smooth everywhere except for a logarithmic non-analyticity at $q = 2k_F$. This is the same nesting singularity that we found in Section [9.4b](#sec-9-4b). A standard result of Fourier analysis is that a non-analyticity of a function $\chi_0(q)$ at a wavevector $q^\star$ gives an oscillating tail with an algebraic decay in its real-space Fourier transform. The period of this tail is fixed by $q^\star$, and its envelope is set by the *type* of the singularity. We apply this to the change of density induced by the impurity, $\delta n(x) = -\int \frac{dq}{2\pi}\, e^{iqx}\, \chi_0(q)\, v_0$, in the Born approximation with impurity strength $v_0$, and we obtain the **Friedel oscillation**.

::: key
One impurity in a metal of dimension $d$ changes the density far from it as

$$\delta n(x) \;\xrightarrow{|x|\to\infty}\; A(v_0)\, \frac{\cos\!\big(2k_F |x| + \varphi_0\big)}{|x|^{\,d}} \qquad (d = 1,2,3). \tag{9.9}$$

The period $\pi/k_F$ is set only by the Fermi surface, and, for a Fermi surface with no flat parts, the power of the envelope only by the dimension. The amplitude $A(v_0)$ and the phase $\varphi_0$ depend on the impurity.
:::

::: {.steps title="From the singularity of chi0 at 2kF to the 1/x tail"}
We take the simplest case, the one-dimensional closed form of $\chi_0(q)$ above, at zero temperature. In the Born approximation the density change is proportional to $v_0$ times the Fourier transform

$$F(x)=\int\frac{dq}{2\pi}\,e^{iqx}\,\chi_0(q)=\frac{1}{\pi}\int_0^\infty \cos(qx)\,\chi_0(q)\,dq,$$

where we used that $\chi_0(q)$ is even in $q$. Near $q=2k_F$ the closed form is a logarithm plus terms that stay finite,

$$\chi_0(q)\approx-\frac{m}{2\pi\hbar^2k_F}\,\ln|q-2k_F| .$$

We integrate by parts once. The boundary terms vanish, since $\sin(qx)$ is zero at $q=0$ and $\chi_0(q)$ goes to zero at large $q$, so

$$F(x)=-\frac{1}{\pi x}\int_0^\infty \sin(qx)\,\chi_0'(q)\,dq .$$

The derivative of the logarithm is a simple pole, $\chi_0'(q)\approx-\frac{m}{2\pi\hbar^2k_F}\,\frac{1}{q-2k_F}$, and the rest of $\chi_0'(q)$ has no pole, so it only adds terms that fall faster than $1/x$. For the pole we use the principal value $\int\frac{\sin(qx)}{q-q_0}\,dq=\pi\cos(q_0x)$ for $x>0$, and we get

$$F(x)\approx\frac{m}{\pi\hbar^2}\,\frac{\cos(2k_Fx)}{2k_Fx}.$$

This has the form of [(9.9)](#eq-9-9) for $d=1$, meaning that the period $\pi/k_F$ comes from where the singularity sits, and the power $1/x$ from its type, a logarithm whose derivative is a simple pole. The integral can also be done in full, and it gives

$$F(x)=\frac{m}{\pi\hbar^2}\left[\frac{\pi}{2}-\mathrm{Si}(2k_F|x|)\right],\qquad \mathrm{Si}(z)=\int_0^z\frac{\sin u}{u}\,du .$$

For large $z$ we have $\mathrm{Si}(z)\approx\pi/2-\cos z/z$, which gives the same tail, and on the impurity the value is finite, $F(0)=m/(2\hbar^2)$. In the free-electron gas of $d=2$ and $d=3$ the singularity sits on the whole circle or sphere $|q|=2k_F$, which is made of the vectors that join opposite points of the Fermi surface. The same Fourier transform gives the envelopes $1/|x|^2$ and $1/|x|^3$, which we state here without the derivation. These powers hold when the Fermi surface has no flat parts. The half-filled square lattice with first-neighbor hopping has a flat, nested Fermi surface, and along the diagonal of the lattice its envelope falls more slowly than $1/|x|^2$.
:::

The oscillation has a universal wavevector that is fixed only by the Fermi surface, which is $2k_F$ in 1D, or more generally the diameter of the Fermi surface. It has an algebraic envelope, whose power depends on the dimensionality $d$, and it has an amplitude and a phase that are not universal and are set by the impurity strength and by microscopic details. This closes the argument that we started in Section [9.4b](#sec-9-4b). The same singularity at $q=2k_F$ in $\chi_0(q)$, which we found there as an instability channel, gives here a long-ranged real-space oscillation with a power-law decay, and not a real instability. The reason is that a single local impurity is a perturbation that is much too weak to reorganize the whole Fermi sea. The divergence in $\chi_0(q)$ only makes its Fourier partner decay slowly instead of exponentially. The two-dimensional case is drawn in [](#sch:s09:friedel2d).

![The change of the local density of states at the energy $E=-3.4t$ around one impurity of onsite energy $v_0=3t$, in the infinite square lattice with the hopping $-t$. It is computed with the embedding of pyqula, with a broadening of $0.05t$ on a $150\times150$ k-mesh. In (a) the Fermi contour at this energy is a circle around $k=0$, with $k_F=0.80$ along the axes in units of the inverse lattice constant, and the dashed square is the first Brillouin zone. In (b) the change is drawn in units of $10^{-3}/t$, with $x$ and $y$ in sites. The ripples are rings that repeat with the period $\pi/k_F\approx4$ sites. In two dimensions the LDOS at one energy falls as $1/r$ with the distance $r$ from the impurity, one power slower than the density of [(9.9)](#eq-9-9). The broadening damps it over about $14$ sites, so the map shows the period and not the power. The impurity site is left out, and the colors saturate close to it. Look at the distance between two red rings, since it is set by the diameter $2k_F$ of the contour.](figures/web/session09/friedel2d.svg){#sch:s09:friedel2d alt="On the left, a small circle in the middle of a dashed square, with an arrow across the circle, on the axes k x and k y. On the right, a map of red and blue rings around the impurity, on the axes x and y in sites, with a colorbar." script="g4_friedel_square.py"}

![The singularity that gives the Friedel oscillation. In panel (a) the vector $2k_F$ connects the two Fermi points of the chain, and in panel (b) the static Lindhard function has its logarithmic peak at that vector.](figures/s09f01_nesting.svg){panel="ab" alt="A one-dimensional band with its two Fermi points and the static Lindhard function with a logarithmic peak at twice the Fermi wavevector."}

To see this in a concrete case, we have drawn the plane above. The widget below takes a ring, and Section [9.6b](#sec-9-6b) takes a chain and an insulator.

::: {.widget name="friedel"}
Move the number of electrons $N_e$ of a ring with 201 sites and one impurity of strength $1.5t$ at site 0. The density oscillates around the impurity with the period $\pi/k_F$, as in [(9.9)](#eq-9-9), and the dashed envelope decays as $1/x$. An STM map at low bias around a single impurity shows the same period. Note that the period changes with the filling, and that it is the same $2k_F$ that gave the singularity of $\chi_0(q)$.
:::

::: lab
On a stepped Au(111) surface, thermovoltage STM is used to study the local density of states at the Fermi level, which forms standing waves on the terraces between the steps. The band diagram of Au(111) gives the expected period $\lambda_F/2=1.8$ nm, while the measured period varies between $1.5$ and $2.1$ nm with the width of the terrace. The article says that this result is understood from the superposition of the incident and the reflected electron waves, which have the period $\lambda_F/2$. It also says that the change of the period is a direct consequence of the decay of the Friedel oscillations. The measurement is in [this article](https://doi.org/10.1103/PhysRevB.103.245311).

In our own reading, which is not in the article, $\lambda_F/2=\pi/k_F$ is the period of [(9.9)](#eq-9-9), since $\lambda_F=2\pi/k_F$. The local density of states at the Fermi level has this period too, as in [](#sch:s09:friedel2d). The scatterer here is a step, which is a line on the surface, and not a single impurity.
:::

::: quiz
A chain has the Fermi wavevector $k_F=\pi/4$. Around an impurity the density oscillates as

$$\delta n(x)\propto\cos(2k_Fx).$$

What is the period, in units of the lattice constant?

- [ ] $8$, which is the Fermi wavelength $2\pi/k_F$.

    This is false. The Fermi wavelength is $2\pi/k_F=8$, but the density oscillates as $\cos(2k_Fx)$. The period of this function is $4$, so $8$ is the period of the wavefunction.

- [x] $4$, since the wavevector of the oscillation is $2k_F=\pi/2$.

    This is true. The singularity of $\chi_0$ is at $q=2k_F=\pi/2$, so the density goes as $\cos(\pi x/2)$. This repeats every $4$ lattice constants.

    ![The function $\cos(2k_Fx)$ for $k_F=\pi/4$ on the sites of the chain. The pattern $1,0,-1,0$ repeats after $4$ sites.](figures/web/session09/period.svg){alt="Values of a cosine on integer sites, one, zero, minus one, zero, repeating every four sites."}

- [ ] $2$, since the oscillation follows the lattice.

    This is false. A period of $2$ means $2k_F=\pi$, which is half filling with $k_F=\pi/2$. For $k_F=\pi/4$ the oscillation is twice slower.
:::

::: quiz
One impurity in a metal of dimension $d$ changes the density far from it as

$$\delta n(x) \;\xrightarrow{|x|\to\infty}\; A(v_0)\, \frac{\cos\!\big(2k_F |x| + \varphi_0\big)}{|x|^{\,d}}.$$

We compare the envelope at the distances $x$ and $2x$ for $d=2$. By which factor does it decrease?

- [ ] A factor $2$.

    This is false. A factor $2$ is the decay $1/|x|$ of $d=1$. In $d=2$ the envelope falls as $1/|x|^2$, so doubling $x$ gives $1/4$.

- [x] A factor $4$.

    This is true. With $d=2$ the envelope is $1/|x|^2$. At $x$ and $2x$ the ratio is $2^2=4$, and it is a power law because the Fermi surface makes $\chi_0$ non-analytic.

- [ ] A factor $8$.

    This is false. A factor $8$ is the decay $1/|x|^3$ of $d=3$. In $d=2$ the exponent is two, so the decrease is $2^2=4$.
:::

::: quiz
Each map shows the change of the LDOS at the Fermi level around one impurity. The three metals are the same square lattice, filled up to three Fermi levels. The color scale is the same, in units of $10^{-3}/t$. Which metal has the largest Fermi circle?

- [ ] ![A map of red and blue rings around the impurity on the axes x and y, from minus 12 to 12 sites, with rings about 7 sites apart.](figures/web/session09/g4_quiz_ripples_e38.svg)

    This is false. The rings repeat about every $7$ sites, the longest period of the three. This metal has the Fermi level $-3.8t$, where $k_F=0.45$ and $\pi/k_F=7.0$, so its circle is the smallest.

- [x] ![A map of red and blue rings around the impurity on the axes x and y, from minus 12 to 12 sites, with rings about 3 sites apart.](figures/web/session09/g4_quiz_ripples_e30.svg)

    This is true. The rings repeat every $3$ sites, the shortest period of the three. The change of the LDOS oscillates as $\cos(2k_Fr)$, so the period is $\pi/k_F$, and $\pi/k_F=3$ gives $k_F=\pi/3=1.05$, at the Fermi level $-3t$. In this way an STM map gives the size of the Fermi surface.

- [ ] ![A map of red and blue rings around the impurity on the axes x and y, from minus 12 to 12 sites, with rings about 4 sites apart.](figures/web/session09/g4_quiz_ripples_e34.svg)

    This is false. The rings repeat about every $4$ sites. This metal has the Fermi level $-3.4t$, where $k_F=0.80$ and $\pi/k_F=3.95$, so its circle is smaller than the one of the rings that repeat every $3$ sites.
:::

:::: problem
A spinless chain has $0.2$ electrons per site, and one impurity sits at $x=0$. Find the period of the Friedel oscillation of the density. Then find the factor by which its envelope falls from $x=10$ to $x=40$, and the same factor for a plane, which is $d=2$ in [(9.9)](#eq-9-9).

::: solution
In a spinless chain at zero temperature the filled states are the momenta $|k|<k_F$ of the zone $-\pi<k\le\pi$, so the number of electrons per site is $n=2k_F/2\pi=k_F/\pi$. For $n=0.2$ this gives $k_F=0.2\pi$. The density oscillates as $\cos(2k_Fx)=\cos(0.4\pi x)$, which has the period

$$\frac{2\pi}{2k_F}=\frac{\pi}{k_F}=5\ \text{sites}.$$

In $d=1$ the envelope falls as $1/|x|$, so from $x=10$ to $x=40$ it falls by $40/10=4$. In $d=2$ it falls as $1/|x|^2$, so by $4^2=16$. We can check this with an exact diagonalization of a chain of $4001$ sites at this filling, with an impurity of $0.1t$. It gives the period $5.0$ sites, and a fit between $10$ and $100$ sites gives a power of the envelope close to $1$.

This is how a map around an impurity is read. The distance between two ripples gives $k_F$, and with it the filling. An STM map gives the same period, since the local density of states at the Fermi level oscillates with the same $2k_F$.
:::
::::

::: {.tryit notebook="session9.ipynb" cell="Impurities in a 2d metal"}
Run the cell with `mu = 3.8`, where the Fermi circle is small, and measure the distance between two ripples of the LDOS. Then set `mu = 3.0` and run it again. The Fermi circle is larger, and the ripples become shorter, from about 7 sites to about 3 sites, since the wavelength is $\pi/k_F$.
:::

::: comesback
- In Section [9.6b](#sec-9-6b) the same oscillation is computed in a chain, and an insulator gives no slow tail.
- In Section [9.7](#sec-9-7) a superconductor has no Fermi surface, so an impurity gives no Friedel tail, and a magnetic one gives a bound state.
- In Section [9.9](#sec-9-9) the impurity in a quantum spin liquid is the same mathematical problem, with spinons in place of electrons.
:::
