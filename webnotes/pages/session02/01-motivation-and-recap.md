## Motivation and recap {#sec-2-1 number="2.1"}

Let us recall the form of a many-body Hamiltonian once it is written in second-quantized, tight-binding form,

$$H = \sum_{ij} t_{ij}\, c_i^\dagger c_j,$$

where $t_{ij}$ are the hopping matrix elements between sites $i$ and $j$. In this language, to solve a quantum material means to diagonalize this Hamiltonian, which is to find the unitary transformation that brings it into the diagonal form

$$H = \sum_n \epsilon_n\, \Psi_n^\dagger \Psi_n, \qquad \Psi_n^\dagger = \sum_i a_{n,i}\, c_i^\dagger.$$

Symmetries allow us to find this diagonal form, or at least strong qualitative and quantitative properties of it, without doing the diagonalization explicitly. This is the motivation for everything in this session. We will use symmetry not to classify order, but to simplify how we solve a quantum many-body problem.

## Simplifying problems with symmetry in simple examples {#sec-2-2 number="2.2"}

We have all used this method before, also outside quantum mechanics. Let us take an infinite plane with a uniform positive charge, and let us ask in which direction the electric field points at some position away from the plane. It can point straight out, or it can be tilted by some angle. We can apply a mirror symmetry that exchanges left and right. The charge distribution does not change under this reflection, so the true field must also map to itself under the same reflection. A tilted field does not pass this test, since its mirror image is tilted in the other direction, while a field that points straight out does pass it. Since the electric field at that point is unique, symmetry alone removes every answer except the one perpendicular to the plane, and we never have to compute the integral from Coulomb's law.

The same argument also works for a less simple shape. Let us replace the infinite plane by an ellipse with a uniform charge, which is an egg-shaped charge distribution, and let us ask the same question about the field at some point on its mirror axis. Mirror symmetry again gives the answer without tilt, this time with the reflection axis of the ellipse, and again without any explicit integration. Note that this only works on the mirror axis, since at a point away from it the reflection maps the point to a different point, and symmetry alone does not fix the direction there. [](#sch:s02:mirror_field) draws both cases.

![The mirror argument for the electric field. In (a), a tilted field turns into a different tilted field under the mirror, so only the field perpendicular to the plane survives. In (b), the same argument works for a point on the mirror axis of an egg-shaped charge, and it fails for a point away from the axis.](figures/web/session02/mirror_field.svg){#sch:s02:mirror_field alt="A charged plane with a vertical mirror line and a field arrow, and an egg-shaped charge with a point on the mirror axis and a point off it."}

::: quiz
A point sits on the mirror axis of the egg-shaped charge. Which direction can the electric field have there?

- [x] Along the axis.
- [ ] Perpendicular to the axis.
- [ ] At $45^\circ$ to the axis.
- [ ] Any direction, since the charge is not a plane.

A component perpendicular to the axis is mapped by the mirror to the opposite component. The point lies on the axis, so both are the field at the same point, and this component has to vanish.
:::

Mirrors are only the simplest case. A circle stays the same under any rotation. A square stays the same only under rotations by $90^\circ$, $180^\circ$, and $270^\circ$, and a shape with less symmetry may stay the same only under a single mirror. Quantum systems can have much richer symmetries, which are also much less obvious than these, and in the following we turn this richer structure into a systematic tool.

::: quiz
How many rotations, counting the identity, leave a square unchanged?

- [ ] $2$
- [x] $4$
- [ ] $8$
- [ ] Infinitely many.

The rotations by $0^\circ$, $90^\circ$, $180^\circ$ and $270^\circ$ map the square to itself, and any other angle does not. A circle, on the other hand, has infinitely many.
:::
