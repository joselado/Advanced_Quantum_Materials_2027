## Measuring entanglement with the entanglement entropy {#sec-7-5 number="7.5"}

To see why [(7.5)](#eq-7-5) works, we need a quantitative measure of how entangled a many-body state is. Let us split the system into two complementary parts, subsystem $A$ and subsystem $B$. A state is **not entangled**, which is also called a product state, if it can be written as $|\Psi\rangle = |\psi_A\rangle
\otimes
|\psi_B\rangle$. Two examples are the state $|{\uparrow\downarrow}\rangle$ and a product of two single-site states that are both polarized along $x$. The singlet [(7.3)](#eq-7-3) is the opposite case. It cannot be written as a product of this form, and it is our main example of an **entangled** state.

To turn the question "entangled or not" into a number, we define the full density matrix $\rho =
|\Psi\rangle
\langle\Psi|$, and we trace out subsystem $B$. This gives the **reduced density matrix** of $A$, $\rho_A =
\mathrm{Tr}_B\,\rho$. The **entanglement entropy** is then the von Neumann entropy of $\rho_A$,

$$S(\rho_A) = -\,\mathrm{Tr}\!\left(\rho_A \log \rho_A\right). \tag{7.6}$$

If $|\Psi\rangle$ is a product state, $\rho_A = |\psi_A\rangle\langle\psi_A|$ is a projector of rank one, so its only nonzero eigenvalue is $1$, and we directly get $S=0$. This means that there is no entanglement and the entropy is zero, which is what we expect.

Let us now check [(7.6)](#eq-7-6) on the singlet [(7.3)](#eq-7-3). We write $\rho = |\Psi\rangle\langle\Psi|$ in the product basis and trace over site $1$, which is our subsystem $B$, and we obtain

$$\rho_A = \tfrac{1}{2}\,|{\uparrow}\rangle\langle{\uparrow}| + \tfrac{1}{2}\,
|{\downarrow}\rangle\langle{\downarrow}|,$$

which is a maximally mixed single-site density matrix, with two eigenvalues both equal to $1/2$. Then

$$S = -\left(\tfrac12\log\tfrac12 + \tfrac12\log\tfrac12\right) = \log 2. \tag{7.7}$$

This is the maximum entanglement entropy that a single spin-1/2 can have, since a local Hilbert space of dimension $d$ can have at most $\log d$. This is the meaning of the statement that the singlet is "maximally entangled," since it uses all the capacity of the local Hilbert space for entanglement.
