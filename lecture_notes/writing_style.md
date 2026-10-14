# Writing style of the lecture notes

This file fixes the style of the prose in `src/sessions/*.tex` and of the figure captions in
`src/figures/*.tex`, and it wins over `VOICE.md` where the two disagree. It is the same style as
the notes of the sibling course, Advanced Computational Methods in Physics. The notes should read
as if they were written in simple English by a condensed matter physicist who is not a native
speaker, in the style of lecture notes, with "we" as the default pronoun. The reader knows physics, so the physics words stay technical, and only
the English around them gets simpler.

## Sentences and words

- **Plain words.** We write "use" and not "exploit", "remove" and not "throw away", "exact" and
  not "rigorous", "have spin" and not "carry spin", "looks the same" and not "visually
  indistinguishable".
- **No idioms and no images.** Phrases such as "set the stage", "a cautionary note", "the wall
  we keep bumping into", "the practical upshot", "made good on" or "dialed" are said directly.
- **No rhetorical turns.** We do not write "breaks nothing at all", "Today we stop
  approximating", an "honest" matrix, or "exact does not mean impossible". We say what happens.
- **One idea per sentence, medium length.** A long list of "how ... how ... how" is split into
  sentences that start with "First", "Then", "We will also see". Two clauses can still be joined
  with "and", "so", "since", "because" or "which is", but we vary these and do not use "since"
  for every join.
- **No stress words that carry no physics.** "Exactly", "simply", "precisely" and "just" are
  kept only when they state a physics fact (an exact mapping, a result that is exact).
- **"We" and the plan of the lecture.** "In this session we will", "Let us take", "At the end
  we will ask". "You" only when we speak about what the reader does with the notebook. No "I".
- **Name after construction.** The idea comes first and its name after it, as in "there is an
  exact mapping between spinless fermions and spins, which is called the Jordan-Wigner
  transformation".

## Punctuation

- **No colons, no semicolons and no em-dashes in prose.** A colon or semicolon becomes a new
  sentence, or the two parts are joined with "since", "so", "because", "which is" or "meaning
  that". A colon that introduces a list becomes a full sentence that ends with a period.
- **Parenthetical asides are folded into the sentence.** "(spin becomes just another orbital
  index)" becomes "where the spin is just one more orbital index", and "(think of a JPEG)"
  becomes "such as JPEG". Parentheses stay for a short symbol or value, such as "($d=2$ for
  spin-$\tfrac12$)".
- **No scare quotes.** We write "the role of the pixels is played by" and not "the raw pixels".
- **Bullet items start with a capital letter and end with a period**, with no semicolons
  between items.
- No contractions and no exclamation marks.

## What does not change

- Equations, inline mathematics, `\label`, `\ref`, `\eqref`, `\cite`, `\url`,
  `\includegraphics` and `\input` stay byte for byte as they are.
- Chapter and section titles keep their meaning. A title with a colon or an idiom is written as a
  plain phrase, as in "Emergent quasiparticles and what the lattice gives us".
- In the `notebookbox` titles, the notebook file and the quoted names of notebook sections stay
  exactly as they are, since they must match the titles of the notebook cells.
- In a figure file only the caption, the second argument of `aqmfigure`, is prose. The TikZ code
  and the text inside the drawing stay as they are.
- Every physics statement, number, figure reference and notebook pointer stays. Only the wording
  changes.

## Approved examples

These three rewrites were approved for the notes of Advanced Computational Methods in Physics,
and they are the reference for everything above. The session numbers refer to that course.

### Session 2, contents and goals

Before:

```
Last time we ended on a cautionary note: mean-field theory, built entirely out of product states,
cannot represent the true ground state of the Hubbard dimer, an entangled singlet that spontaneously
breaks nothing at all. Today we stop approximating. Instead of guessing a variational ansatz, we are
going to write down the many-body Heisenberg Hamiltonian that emerges from superexchange, represent it
as an honest matrix acting on the full $2^L$-dimensional many-body Hilbert space, and diagonalize it
exactly. Along the way we will learn to read a many-body spectrum: how the many-body gap tells us
whether a spin chain is gapped or gapless, how a field or a coupling constant can be dialed to drive
level crossings and even phase transitions, how symmetries let us block-diagonalize the Hamiltonian so
that ``exact'' does not immediately mean ``impossible,'' and how correlators, both static and
dynamical, let us extract order and excitations directly from the wave function. We will close by
asking whether the excitations of a quantum magnet admit their own single-particle description, in
terms of emergent fermionic quasiparticles called spinons. Everything here is numerically exact, no
product-state restriction anywhere, and that honesty comes at the price we will keep bumping into all
session: the Hilbert space grows as $2^L$, which is exactly the wall that motivates the tensor-network
methods we build starting in Session 4.
```

After:

```
In the last session we saw that mean-field theory has a limitation, since it only uses product
states and the ground state of the Hubbard dimer is a singlet, which is an entangled state that
does not break any symmetry. In this session we will not do any approximation. We will take the
Heisenberg Hamiltonian that we obtained from superexchange, write it as a matrix in the full
many-body Hilbert space, which has dimension $2^L$, and diagonalize it exactly. With this, we will
learn how to read a many-body spectrum. First, we will use the many-body gap to see if a spin chain
is gapped or gapless. Then we will see how a magnetic field or a change in the couplings gives rise
to level crossings and phase transitions. We will also see how symmetries allow us to write the
Hamiltonian in blocks, so that we can solve bigger systems, and how static and dynamical correlators
tell us about the order and the excitations of the system. At the end we will ask if the
excitations of a quantum magnet can be described as single-particle excitations, in terms of
emergent fermions that are called spinons. All the results in this session are exact, and the price
we pay is that the Hilbert space grows as $2^L$. This exponential growth is the reason why, starting
in Session 4, we will use tensor-network methods.
```

### Session 4, tensor networks as data compression

Before:

```
Let us set the stage with an analogy before we write down any equations. Imagine you have a
high-resolution photograph and you want to store it using much less memory. You do not throw away
information at random; you exploit the fact that real photographs are highly structured, nearby
pixels are correlated with each other, and a compressed representation (think of a JPEG) can
reproduce something visually indistinguishable from the original using a small fraction of the
raw pixel count. Tensor networks do exactly the same thing, but for quantum many-body
wavefunctions. The ``raw pixels'' are the $2^L$ complex coefficients of the wavefunction in the
computational basis; the ``compression algorithm'' is a particular way of factorizing those
coefficients into small pieces, and the parameter that controls how aggressive the compression is
will turn out to be something called the \textbf{bond dimension}. The whole content of this
section is making that analogy precise.
```

After:

```
Before we write any equations, let us start with an analogy. Let us take a photograph with a high
resolution, and let us say that we want to store it with much less memory. We do not remove
information at random. Instead, we use the fact that real photographs have a lot of structure,
since pixels that are close to each other are correlated, and a compressed format such as JPEG can
give an image that looks the same as the original with only a small fraction of the original
pixels. Tensor networks do the same thing, but for the wavefunctions of quantum many-body systems.
The role of the pixels is played by the $2^L$ complex coefficients of the wavefunction in the
computational basis. The role of the compression algorithm is played by a specific way of writing
these coefficients as a product of small pieces, and the parameter that controls how much we
compress is what is called the \textbf{bond dimension}. In this section we will make this analogy
precise.
```

### Session 3, the spinful Fock space

Before:

```
If the fermions carry spin, each site has \emph{four} local states, $\ket{0}$, $\ket{\up}$,
$\ket{\dn}$, $\ket{\up\dn}$, exactly as in Session 1. Equivalently, we can think of a spinful chain
as $2L$ independent spinless orbitals (spin becomes just another orbital index), so the Fock space
has dimension $2^{2L} = 4^L$: twice the exponent of the spinless case, since every site now
contributes two binary choices instead of one, which is what panel (a) of
Figure~\ref{fig:fock-basis} puts side by side with the spin and the spinless fermion. Note how this lines up with the
spin chains of Session 2: an $L$-site spin-$\tfrac12$ chain also has a $2^L$-dimensional Hilbert
space, exactly matching the spinless-fermion count. The reason for this is that a rigorous mapping
(Jordan-Wigner, which we will meet properly in Session 5) sends spinless fermions to spin-$\tfrac12$
degrees of freedom one-for-one. For now, the practical upshot is simply this:
\begin{itemize}[nosep]
  \item solving an interacting \textbf{spinless} fermionic chain costs exactly as much as
    solving a quantum \textbf{spin} chain of the same length, $\sim 2^L$;
  \item solving an interacting \textbf{spinful} fermionic chain, like the Hubbard model, costs the
    square of that, $\sim 4^L$, so at fixed computational budget we can only reach about half the
    system size.
\end{itemize}
```

After:

```
If the fermions have spin, each site has \emph{four} local states, $\ket{0}$, $\ket{\up}$,
$\ket{\dn}$ and $\ket{\up\dn}$, as in Session 1. We can also think of a spinful chain as $2L$
spinless orbitals, where the spin is just one more orbital index, so the Fock space has dimension
$2^{2L} = 4^L$. The exponent is twice the one of the spinless case, since every site now has two
binary choices instead of one, and panel (a) of Figure~\ref{fig:fock-basis} shows this next to
the spin and the spinless fermion. Note that this is the same counting as for the spin chains of
Session 2, since a spin-$\tfrac12$ chain with $L$ sites also has a Hilbert space of dimension
$2^L$, the same as for spinless fermions. The reason for this is that there is an exact mapping
between spinless fermions and spin-$\tfrac12$ degrees of freedom, site by site, which is called
the Jordan-Wigner transformation, and we will see it in detail in Session 5. In practice, this
means two things for the cost of our calculations.
\begin{itemize}[nosep]
  \item Solving an interacting \textbf{spinless} fermionic chain costs the same as solving a
    quantum \textbf{spin} chain of the same length, $\sim 2^L$.
  \item Solving an interacting \textbf{spinful} fermionic chain, such as the Hubbard model, costs
    the square of that, $\sim 4^L$, so with the same computer we can only reach about half the
    system size.
\end{itemize}
```
