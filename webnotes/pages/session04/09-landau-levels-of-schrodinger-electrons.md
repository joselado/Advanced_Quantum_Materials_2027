## Landau levels of Schrödinger electrons {#sec-4-9 number="4.9"}

Let us now solve for the spectrum, and let us start with the simplest case. These are free electrons with no lattice and no potential apart from the field itself, and with dispersion $p^2/2m$ before we switch on the field. With minimal coupling and the Landau gauge $\mathbf{A}=(0,Bx,0)$ we have

$$H = \frac{\pi_x^2+\pi_y^2}{2m} = \frac{p_x^2}{2m} + \frac{(p_y-Bx)^2}{2m}. \tag{4.5}$$

We take the charge of the carriers to be $+e$ in [(4.3)](#eq-4-3) and we set $e=1$ in all this session, while we keep $\hbar$ explicit. This is a choice of convention, but it has consequences, since it fixes $[\pi_x,\pi_y]=+i\hbar^2/\ell_B^2$. The ladder operators of Section [4.10](#sec-4-10) and the holomorphic wavefunctions of Section [4.13](#sec-4-13) are built on this convention. For an electron, which has charge $-e$, every cyclotron orbit and every edge current below goes around in the other direction, and nothing else changes.

Since $\mathbf{A}$ does not depend on $y$, we have $[H,p_y]=0$, so we can look for eigenstates of the form $\psi(x,y) = e^{ik_y y}\phi(x)$. With the replacement $p_y\to\hbar k_y$, the Hamiltonian [(4.5)](#eq-4-5) becomes a one-dimensional problem in $x$,

$$H\phi(x) = \left[\frac{p_x^2}{2m} + \frac{B^2}{2m}\Big(x-\frac{\hbar k_y}{B}\Big)^2\right]\phi(x),$$

which is exactly the Hamiltonian of a quantum harmonic oscillator centered at $x_0 = \hbar
k_y/B$, with frequency $\omega_c = B/m$, the cyclotron frequency. The shift of the center is removed with a change of variable, as it is described in the lecture. When we solve it with the same ladder operators as the ordinary harmonic oscillator we obtain

$$E_n = \hbar\omega_c\left(n+\frac{1}{2}\right), \qquad n=0,1,2,\dots, \tag{4.6}$$

which does not depend on $k_y$ at all. Every value of $k_y$, or in other words every choice of the guiding center $x_0$, gives the same energy. This is the reason why the Landau levels are flat bands, and why each of them has a macroscopic degeneracy that is proportional to the area of the sample. Figure [4.3](#fig:s04:guidingcenter) shows this mechanism directly, with the same well placed at different positions, and with the degeneracy counted as one orbital for each flux quantum through the sample. When we put in the real physical constants for a field typical of GaAs, we obtain the millielectronvolt scale that we gave in Section [4.1](#sec-4-1)

![Why the Landau levels are flat. (a) In the Landau gauge each $k_y$ reduces [(4.5)](#eq-4-5) to a one-dimensional harmonic oscillator in $x$, which is the same in every respect except that it is centred on the guiding centre $x_0=\hbar k_y/B$. When $k_y$ increases, the whole well moves to the right without changing its curvature. Every well therefore has the same ladder $E_n=\hbar\omega_c(n+\tfrac 12)$, drawn here as the horizontal guides, and the ground-state wavepacket of each well, the red bump, has the same shape at a different position. (b) As a function of $k_y$, this is a set of bands with exactly no dispersion, and the three balls are the three values of $k_y$ of (a). The flatness is not an artefact of the gauge. It means that the energy does not depend on the position of the electron in the sample, and this is also the origin of the very large degeneracy of the Landau levels.](figures/s04f03_guidingcenter.svg){#fig:s04:guidingcenter number="4.3"}
