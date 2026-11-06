## The symmetric gauge and the lowest-Landau-level wavefunctions {#sec-4-13 number="4.13"}

To go from single-particle Landau levels to a real many-body quantum Hall wavefunction, we change to the symmetric gauge, $\mathbf{A}=\tfrac{B}{2}(-y,x,0)$, and to the complex coordinate $z=x+iy$. We write $\partial_z = \tfrac12(\partial_x-i\partial_y)$ and $\partial_{\bar z} =
\tfrac12(\partial_x+i\partial_y)$, and then the ladder operator of Section [4.12](#sec-4-12) in this gauge is proportional to $\partial_{\bar z} + z/4\ell_B^2$. The condition for the lowest Landau level (LLL), $a\psi=0$, is therefore the first-order differential equation

$$\left(\partial_{\bar z} + \frac{z}{4\ell_B^2}\right)\psi(z,\bar z) = 0
\quad\Longrightarrow\quad
\psi(z,\bar z) = f(z)\, e^{-|z|^2/4\ell_B^2}, \tag{4.9}$$

where $f(z)$ is an *arbitrary holomorphic function*, meaning any function built only from powers of $z$ and never from $\bar z$. This is the precise form of the statement "any power $z^m$ times a Gaussian is a zeroth-Landau-level wavefunction". Holomorphicity is not an extra assumption, since it follows directly when we solve the LLL condition in the symmetric gauge. The single-particle LLL orbitals are then

$$\psi_m(z) = z^m\, e^{-|z|^2/4\ell_B^2}, \qquad m=0,1,2,\dots, \tag{4.10}$$

and each of them has an angular momentum $m$, which is the eigenvalue of $L_z$ in this gauge. All of them have the same Gaussian envelope, but the polynomial prefactor $z^m$ moves the probability density of the orbital further from the origin when $m$ grows. The reason is that $|\psi_m|^2$ has its maximum where $\tfrac{d}{d|z|}\big(|z|^{2m}e^{-|z|^2/2\ell_B^2}\big)=0$, which is at the radius $r_m = \sqrt{2m}\,\ell_B$.
