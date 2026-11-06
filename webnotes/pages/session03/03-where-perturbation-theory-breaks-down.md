## Where perturbation theory breaks down {#sec-3-3 number="3.3"}

Before we use [(3.1)](#eq-3-1), we should say when it fails, because several of the most important phenomena in this course appear in this failure. The expansion [(3.1)](#eq-3-1) assumes that we are in the *perturbative regime*, where a small change in the input, which is the strength of the perturbation, gives a small change in the output. This is not always the case. We name three cases now, because we will see each of them in detail later in the course.

- An impurity in a metal gives rise to the **orthogonality catastrophe**. The many-body ground state after the perturbation becomes exactly orthogonal to the original ground state, even for a very small perturbation, so no Taylor expansion of finite order in $\lambda$ can connect the two.

- A quantum spin, which is a local magnetic moment, coupled to a metal gives rise to the **Kondo effect**. The relevant energy scale, which is the Kondo temperature, is a non-perturbative function of the coupling constant, and no order of perturbation theory in this coupling gives it. We will study the Kondo lattice model in detail in session 8, and here we only mention it as a first sign that ordinary perturbation theory has a strict limit.

- **Superconductivity** is also non-perturbative, since the BCS gap does not appear at any finite order in the interaction strength if we start from the normal state. We will work this out in detail in session 5.

In this lecture, and for every model that we build in this session, we stay inside the regime where [(3.1)](#eq-3-1) holds. For now, it is enough to know that this is not always the case.
