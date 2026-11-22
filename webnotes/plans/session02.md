# Plan of Session 2 of the web notes

This plan is filled before any page is written, and the lecturer can change it. One block per page. A
field that does not apply says "none" with the reason. The rules are in
`lecture_notes/WEB_NOTES_PLAN.md`, and the conventions of the session in
`webnotes/conventions/session02.md`. That sheet did not exist when this plan was written, so the pyqula
facts that the plan uses are checked here by number, in the section "pyqula facts checked for this
plan", and they are confirmed against the sheet when it exists.

## The pages today

| file | sections | words | eqs | key | recall | steps | lab | problem | quiz | picture options | figures (with script) | lint hits |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `index.md` | intro | 452 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 (0) | 0 |
| `01-motivation-and-recap.md` | 2.1, 2.2 | 898 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | opener 1 |
| `03-symmetry-operators-in-a-formal-way.md` | 2.3 | 1155 | 3 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 (0) | key 1, opener 1 |
| `04-exercises-where-we-guess-eigenstates-from-symmetry-only.md` | 2.4 | 1194 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 (0) | key 1, long-paragraph 1, opener 1, quiz-long 1 |
| `05-blochs-theorem-and-the-first-band-structure.md` | 2.5 | 1368 | 5 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | key 1, long-paragraph 1, opener 1, quiz-long 1 |
| `06-the-meaning-of-the-phase-which-is-the-quasi-momentum.md` | 2.6 | 856 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | key 1, long-paragraph 1, opener 1 |
| `07-multi-orbital-band-structures.md` | 2.7 | 1386 | 3 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | key 1, opener 1 |
| `08-higher-dimensional-band-structures.md` | 2.8 | 989 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | key 1, opener 1, quiz-long 1 |
| `09-properties-of-an-electronic-dispersion.md` | 2.9, 2.10 | 1483 | 3 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 3 (0) | key 1, opener 1 |
| `11-the-dirac-cone-of-the-honeycomb-lattice-of-graphene-and-flat-band-lattices.md` | 2.11a | 1296 | 3 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | key 1, opener 1, quiz-long 1 |
| `11b-flat-bands-from-the-geometry-of-the-lattice.md` | 2.11b | 1054 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | long-paragraph 1, opener 1, quiz-long 1 |
| `12-measuring-band-structures-with-arpes.md` | 2.12, 2.13 | 1189 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 (0) | opener 1, quiz-long 1 |

The figure scripts named below get the prefix of their builder group, as in Session 3. Every script follows
the sign of its page, which is written next to it. The notebook `session2.ipynb` uses the opposite sign for the
chain, the square lattice and the kagome lattice, and the try-it boxes already say so.

## The introduction of the session

File `index.md`, 452 words, numbered equations none.

- Question of the page, and where we arrive: none to add. The page already asks how we solve a single-particle Hamiltonian, and it answers that symmetry turns one infinite problem into many small ones.
- Main result for the key box: none, since this is the introduction of the chapter.
- Equation of another page that it starts from, for the recall box: none. It names (1.2) and Section 1.12 in words, which is enough for an introduction.
- Derivation told in words, for a steps fold: none.
- Lab box, with the source and the number that the source states: none.
- Pen-and-paper problem: none.
- Quizzes to rewrite, and a picture question or equations as options: none, an introduction has no quiz.
- Figures to add, each with its pyqula script or the reason for numpy: none. `session_map` is a concept map and not a plot.
- Old figures of the page that break the plot rules: none.
- The page needs no edit, so it is in no builder group.

## 2.1 Motivation and recap and 2.2 Simplifying problems with symmetry in simple examples

File `01-motivation-and-recap.md`, 898 words, numbered equations none.

- Question of the page, and where we arrive: can we find the eigenstates of a Hamiltonian without diagonalizing it? In part yes, since a symmetry removes every answer that it does not leave the same, as the mirror fixes the field of a charged plane without the Coulomb integral.
- Main result for the key box: optional on a page of motivation. If used, one box with no equation, saying that a unique answer is unchanged by every symmetry of the problem, so on a mirror axis only the field along the axis survives.
- Equation of another page that it starts from, for the recall box: `eq="1.5"`, the general interacting Hamiltonian of Session 1, whose bilinear part the page writes again.
- Derivation told in words, for a steps fold: none, the page has no derivation.
- Lab box, with the source and the number that the source states: none, a page of motivation with no measured quantity.
- Pen-and-paper problem: four equal charges at the corners of a square. Show with the rotation by $90^\circ$ that the field at the center vanishes, and with a mirror that at the middle of an edge it is perpendicular to that edge. The answer is $E=0$ at the center.
- Quizzes to rewrite, and a picture question or equations as options: the first quiz leans on "the egg-shaped charge" of the text, so it becomes a picture quiz. The question shows a charge with one mirror axis and a point on the axis, and the three options are three field arrows, along the axis (right), perpendicular to it, tilted. The quiz on the rotations of the square stays.
- Figures to add, each with its pyqula script or the reason for numpy: the three arrow pictures of the quiz, numpy, since they are drawings with no calculation.
- Old figures of the page that break the plot rules: none, `mirror_field` is a schematic with no data axis.

## 2.3 Symmetry operators in a formal way

File `03-symmetry-operators-in-a-formal-way.md`, 1155 words, numbered equations (2.1), (2.2), (2.3).

- Question of the page, and where we arrive: what does it mean that a Hamiltonian has a symmetry, and what does it give us? We arrive at $[H,S]=0$, so $H$ and $S$ have a common eigenbasis, and every eigenvalue of $S$ is a phase.
- Main result for the key box: (2.3), with the sentence that every eigenstate of $H$ can be chosen as an eigenstate of $S$, with an eigenvalue $e^{i\varphi}$ as in (2.2).
- Equation of another page that it starts from, for the recall box: none, since the page starts from the mirror argument of Section 2.2, which has no numbered equation.
- Derivation told in words, for a steps fold: "From the commutator (2.3) to a common eigenbasis". The nondegenerate level first, where $S\psi$ has the same energy and so differs from $\psi$ by a phase. Then a degenerate level, where we diagonalize $S$ inside the level. The two lines that give $|\lambda|=1$ from (2.1) can open the fold.
- Lab box, with the source and the number that the source states: none, a formal page with no material.
- Pen-and-paper problem: the open chain of three sites $H=t(c_1^\dagger c_2+c_2^\dagger c_3+\text{h.c.})$ and the mirror $M$ that exchanges sites 1 and 3. Write $M$ as a matrix, check $[H,M]=0$, and give the mirror eigenvalue of each eigenstate. The answer is the energies $-\sqrt2\,t$, $0$, $\sqrt2\,t$ with the mirror eigenvalues $+1$, $-1$, $+1$.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the state $(1,i,-1,-i)$ says "as above", so the question defines the rotation itself. Its answer depends on the direction of the rotation, see "Open for the lecturer", so the builder keeps the direction of the page until that point is decided. The quiz on $[H,S]=0$ gets equations as options, $S\psi=e^{i\alpha}\psi$ (right), $\langle\psi|S\psi\rangle=0$, $HS\psi=-E\,S\psi$. A new picture quiz shows three states on a ring of four sites as arrows and asks which one is an eigenstate of the rotation by $90^\circ$. The options are arrows that turn by $90^\circ$ from site to site (right), arrows of different lengths, and arrows that turn by $60^\circ$. Its answer does not depend on the direction.
- Figures to add, each with its pyqula script or the reason for numpy: the three ring pictures, numpy, since they draw given amplitudes. The figure `block_diagonal` moves after (2.3), since today it cuts the sentence before (2.3).
- Old figures of the page that break the plot rules: `block_diagonal` shows $|H_{ij}|$ as a shade with no scale, and the indices of the matrix are not named. numpy is right there, since pyqula does not change to a symmetry basis.

## 2.4 Exercises where we guess eigenstates from symmetry only

File `04-exercises-where-we-guess-eigenstates-from-symmetry-only.md`, 1194 words, numbered equations (2.4).

- Question of the page, and where we arrive: what do we know about the eigenstates of a ring of $L$ sites before we write its Hamiltonian? They can be chosen as the $L$ Fourier modes with $\varphi_n=2\pi n/L$, for any hopping that keeps the rotation, and the infinite chain turns this into Bloch's theorem.
- Main result for the key box: (2.4), with the sentence that on $L$ sites $R^L=1$ gives $\varphi_n=2\pi n/L$, and that the eigenstates can be chosen as eigenstates of $R$, which have the same modulus on every site. The sign of the exponent of $\alpha_j$ follows the open point on the direction of the rotation.
- Equation of another page that it starts from, for the recall box: `eq="2.2 2.3"`.
- Derivation told in words, for a steps fold: "From the rotation of a ring to its Fourier modes". First $\lambda^3=1$, then the ratio of the amplitudes of two neighbors is the phase, then the modulus is the same on all sites, so each site has the weight $1/L$. The fold names the direction of $R$ that it uses.
- Lab box, with the source and the number that the source states: none with a number. The stored `nilius2002` built a chain of 20 gold atoms one by one with STM and measured its band, but its abstract gives no value with a unit, and it is a chain and not a ring. See the open point on the STM sentences.
- Pen-and-paper problem: a ring of six sites with the hopping $-t$. Use the rotation to find the six energies with no matrix. The answer is $-2t$, $-t$, $-t$, $t$, $t$, $2t$, so four levels, and three spinless electrons have the total energy $-4t$.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the weight $1/L$ has a question of 21 words, so it becomes "An eigenstate of a ring of $L$ sites is a Fourier mode. What weight does one site have?". The quiz on the six phases stays. A new quiz has equations as options and asks which coefficients give an eigenstate of every Hamiltonian with the rotation of a ring of five sites, $\alpha_j\propto e^{2\pi i j/5}$ (right), $\alpha_j\propto e^{i\pi j/5}$, whose phase does not close after five sites, and $\alpha_j\propto\delta_{j0}$.
- Figures to add, each with its pyqula script or the reason for numpy: none new. `ring_six_phases` in the feedback stays.
- Old figures of the page that break the plot rules: `ring_long_range` is numpy for energies that pyqula gives, as a chain with a cell of five sites at $k=0$, `geometry.chain().get_supercell(5)` with `tij=[-1.0,-t2]`, which gives the five energies of the ring also for $t_2=0.8$. Its axes are fine.
- The paragraph of 171 words on the ring of five sites is split where it turns to the long-range hoppings. It holds the sentence of the open point on the weight $1/5$, which is not reworded.

## 2.5 Bloch's theorem and the first band structure

File `05-blochs-theorem-and-the-first-band-structure.md`, 1368 words, numbered equations (2.5), (2.6), (2.7), (2.8), (2.9).

- Question of the page, and where we arrive: what is the spectrum of an infinite chain, which no computer can diagonalize as a matrix? One Fourier transform gives $\epsilon_\varphi=-2t\cos\varphi$ (2.8), and a second-neighbor hopping adds $-2\eta\cos2\varphi$ (2.9).
- Main result for the key box: (2.8), with the sentence that the band has the width $4t$ and its bottom at $\varphi=0$ for $t>0$. Whether its `\boxed` stays inside the box is an open point.
- Equation of another page that it starts from, for the recall box: `eq="2.3"`, with the translation $T$ in the role of $S$.
- Derivation told in words, for a steps fold: "From the second-neighbor hopping to the band (2.9)". The term $c_n^\dagger c_{n+2}$ gives the phase $e^{2i\varphi}$ and so $-2\eta\cos2\varphi$. The same fold can hold the two expansions $\epsilon_\varphi\approx-2t+t\varphi^2$ near $\varphi=0$ and $2t-t\delta^2$ near $\varphi=\pi$.
- Lab box, with the source and the number that the source states: none. The chains built atom by atom of Fölsch and coworkers (Phys. Rev. Lett. 92, 056803) and of `nilius2002` were read, and neither abstract gives a value with a unit.
- Pen-and-paper problem: for the band (2.9), find above which $\eta$ the point $\varphi=\pi$ becomes a local minimum, and the width of the band below that value. The answer is $\eta>t/4$, from $\epsilon''(\pi)=-2t+8\eta$, and the width stays $4t$ for $\eta<t/4$. For $\eta=0.5\,t$ it is $4.5\,t$.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the sign of $t$ has a question of 17 words and leans on (2.8), so it becomes "The chain band is $\epsilon_\varphi=-2t\cos\varphi$. Where is its minimum when $t<0$?". The quiz on $\varphi=\pi/2$ refers to (2.9) by number, so (2.9) goes into the question as a display, and its options are already equations. A new picture quiz shows three bands for $t=1$ and $\eta=0$, $0.2$, $0.5$, and asks which one has a local minimum at $\varphi=\pi$.
- Figures to add, each with its pyqula script or the reason for numpy: `chain_second_neighbor.py`, with `geometry.chain()` and `tij=[-1.0,-eta]`, which is the sign of (2.5), for the three picture options.
- Old figures of the page that break the plot rules: `chain_eta` is numpy for a band that pyqula gives, and its energy axis has no ticks. `band_sign_t`, in the feedback of a quiz, names $\epsilon$ without its unit $t$ and has no ticks on that axis.
- The paragraph of 155 words on the features of the band is split where it turns from the two band edges to the middle of the band.

## 2.6 The meaning of the phase, which is the quasi-momentum

File `06-the-meaning-of-the-phase-which-is-the-quasi-momentum.md`, 856 words, numbered equations (2.10).

- Question of the page, and where we arrive: what is the phase $\varphi$ physically? It is $\varphi=ka$ (2.10), the crystal momentum times the lattice constant, and it is defined only up to $2\pi$.
- Main result for the key box: (2.10), with the sentence that $k$ and $k+2\pi/a$ are the same state on the lattice, so we keep $k$ in $(-\pi/a,\pi/a]$.
- Equation of another page that it starts from, for the recall box: `eq="2.2"`.
- Derivation told in words, for a steps fold: "From the Taylor series to the translation operator". The series $\sum_n a^n\partial_x^n/n!$ is $e^{a\partial_x}=e^{iap/\hbar}$, and the comparison with $e^{i\varphi}$ gives (2.10).
- Lab box, with the source and the number that the source states: none here, since the measurement of $k$ is the subject of Section 2.12.
- Pen-and-paper problem: a chain with $a=0.3$ nm. Give the first zone, and the $k$ inside it that is the same state as $k=25$ nm$^{-1}$. The answer is $|k|\le\pi/a=10.5$ nm$^{-1}$, and $25-2\pi/a=4.06$ nm$^{-1}$.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the cell $2a$ says "as we will see in the next section" in a feedback, which becomes a link to Section 2.7. The quiz on $k+2\pi/a$ stays. A new picture quiz shows the dots of $\cos(0.5x)$ on the sites, for $a=1$, and three waves, $\cos[(0.5+2\pi)x]$ (right), $\cos[(0.5+\pi)x]$ and $\cos(1.0x)$, and asks which one is the same state on the lattice.
- Figures to add, each with its pyqula script or the reason for numpy: the three wave pictures, numpy, since they sample a cosine and have no Hamiltonian.
- Old figures of the page that break the plot rules: `aliasing` has no name on its vertical axis.
- The paragraph of 165 words on the Löwdin basis is split where it turns to the finite rings.

## 2.7 Multi-orbital band structures

File `07-multi-orbital-band-structures.md`, 1386 words, numbered equations (2.11), (2.12), (2.13).

- Question of the page, and where we arrive: how do we get the bands of a lattice with several orbitals per cell? We arrive at the Bloch Hamiltonian $H(\varphi)$ (2.12), a matrix of the size of the number of orbitals, and at the two bands of the chain with alternating hoppings (2.13).
- Main result for the key box: (2.12), with the recipe in one or two sentences, which is to count the orbitals, put an intracell hopping in its entry with no phase and an intercell one with $e^{\pm i\varphi}$, and diagonalize.
- Equation of another page that it starts from, for the recall box: `eq="2.7"`, the Fourier transform of Section 2.5.
- Derivation told in words, for a steps fold: "From the Hamiltonian (2.11) to the Bloch Hamiltonian (2.12)". The transform (2.7) gets an orbital index, the intracell term gives $t_{\alpha\beta}$ and the intercell term $\gamma_{\alpha\beta}e^{i\varphi}$. Then the chain of (2.13), whose entry $1+\eta e^{-i\varphi}$ is checked by a number in the check script.
- Lab box, with the source and the number that the source states: none. No stored source with a number fits a chain with several orbitals, and the ribbon of `talirz2017` goes to Section 2.12.
- Pen-and-paper problem: a cell of two sites with the uniform hopping $-t$, the onsite energy $+\Delta$ on $A$ and $-\Delta$ on $B$. Write $H(\varphi)$ and find the gap at $\varphi=\pi$. The answer is $\epsilon_\pm=\pm\sqrt{\Delta^2+2t^2(1+\cos\varphi)}$, so the gap is $2\Delta$ at $\varphi=\pi$.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on $\eta=1$ and $\varphi=\pi$ refers to (2.13), so $\epsilon_\pm=\pm|1+\eta e^{-i\varphi}|$ goes into the question. The quiz on the cell of three sites stays. A new quiz has equations as options and asks which $H(\varphi)$ belongs to the chain with intracell hopping $1$ and intercell hopping $\eta$. The three options are $2\times2$ matrices, with $\eta$ on the diagonal, with the phase on the intracell term, and the right one.
- Figures to add, each with its pyqula script or the reason for numpy: none new. If `ssh_recipe` is redrawn, its script is `ssh_bands.py`, with `geometry.bichain()` and `h.inter = eta*h.inter`, as in Session 3.
- Old figures of the page that break the plot rules: `ssh_recipe` names $\epsilon$ without its unit in the band panel, and it is numpy for bands that the bichain of pyqula gives. `fold_three`, in a feedback, is numpy for the bands of `geometry.chain().get_supercell(3)`, which gives $-2$, $1$, $1$ at $k=0$ as the feedback says.

## 2.8 Higher-dimensional band structures

File `08-higher-dimensional-band-structures.md`, 989 words, numbered equations (2.14), (2.15).

- Question of the page, and where we arrive: what changes when the lattice has two or three directions? There is one phase for each direction, the zone is a torus, and the bands are (2.14) and (2.15).
- Main result for the key box: (2.14), with the sentence that each direction of hopping adds one cosine, so the width grows by $4t$ for each direction.
- Equation of another page that it starts from, for the recall box: `eq="2.8"`.
- Derivation told in words, for a steps fold: "From the square lattice to the band (2.14)". The Fourier transform along $x$ and along $y$, where the bonds along $x$ give $-2t\cos\varphi_x$ and the bonds along $y$ give $-2t\cos\varphi_y$.
- Lab box, with the source and the number that the source states: none, no stored source gives a number for a band with one orbital on a square lattice.
- Pen-and-paper problem: add the hopping $-t'$ along the diagonals of the square lattice. Find $\epsilon(\varphi_x,\varphi_y)$ and its values at $\Gamma$, $X$ and $M$. The answer is $-2t(\cos\varphi_x+\cos\varphi_y)-4t'\cos\varphi_x\cos\varphi_y$, which gives $-4t-4t'$, $4t'$ and $4t-4t'$.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the width of the cubic band has a question of 20 words and leans on (2.15), so the band goes into the question as a display. The quiz on the hopping along $y$ becomes a picture quiz with three maps of the energy over the zone, stripes that do not change along $\varphi_y$ (right), stripes that do not change along $\varphi_x$, and the map of (2.14).
- Figures to add, each with its pyqula script or the reason for numpy: `square_lattice.py`, with `geometry.square_lattice()` and `tij=[-1.0]`, the sign of (2.14), which gives the bands on $\Gamma$-$X$-$M$-$\Gamma$ and on a k-mesh, for a redraw of `square_bands` if it is picked, and for the map of (2.14) among the options of the quiz. The two maps of stripes are numpy, since the square lattice of pyqula has no argument that sets the hopping along one direction to zero. The three maps use a diverging scale with white at zero, one colorbar range for the three, and the extended zone with the first zone dashed.
- Old figures of the page that break the plot rules: `square_bands` is numpy for bands that pyqula gives. Its map stops at the first zone, while its caption says that the contours continue across the dashed border, and it has no ticks on $\varphi_x$, $\varphi_y$ and no value on the contour lines. `decoupled_chains`, in a feedback, shows a signed energy on a one-sided scale with no colorbar and no ticks, only inside the first zone.

## 2.9 Properties of an electronic dispersion and 2.10 Three types of dispersion, which are parabolic, Dirac and flat

File `09-properties-of-an-electronic-dispersion.md`, 1483 words, numbered equations (2.16), (2.17), (2.18).

- Question of the page, and where we arrive: what can we read from a band, and which of it is measured? We arrive at the density of states (2.16), the velocity (2.17), the effective mass (2.18) and the Fermi surface, and in Section 2.10 at the three local types, which differ by their density of states.
- Main result for the key box: two boxes. In Section 2.9, (2.16), with the sentence that (2.17) is the slope and (2.18) the curvature of the same band. In Section 2.10, an untagged display of the density of states in two dimensions of the three types, per unit area and for one spin, $m/2\pi\hbar^2$ for a parabolic band, $|E|/2\pi\hbar^2v_F^2$ for one Dirac cone, and a delta function for a flat band. The box states these conditions next to the formulas.
- Equation of another page that it starts from, for the recall box: `eq="2.8 2.14"`.
- Derivation told in words, for a steps fold: "From the density of states (2.16) to the three types". The chain first, $g(\omega)=1/(\pi\sqrt{4t^2-\omega^2})$ per site, then two dimensions with $g=(1/2\pi)\,k\,dk/dE$ for $E\propto k^2$ and for $E\propto k$.
- Lab box, with the source and the number that the source states: none. The stored sources with a mass or a velocity go where their probe is taught, ARPES in Section 2.12 and the cyclotron mass of graphene in Section 2.11a. The abstracts on van Hove peaks that were read (arXiv 0912.2102 and arXiv 1812.08776) give no energy for the peak.
- Pen-and-paper problem: the density of states per site of the chain (2.8). The answer is $g(\omega)=1/(\pi\sqrt{4t^2-\omega^2})$, so $g(0)=1/(2\pi t)\approx0.16/t$, and it diverges at $\pm2t$, where the velocity vanishes.
- Quizzes to rewrite, and a picture question or equations as options: no lint hit, both quizzes stay. A new picture quiz shows three Fermi surfaces of the square lattice, at $\epsilon=-3t$, $-t$ and $0$, and asks which one is nested by $Q=(\pi,\pi)$. A new quiz has equations as options, for the bottom of the band $\epsilon\approx-2t+ta^2k^2$, with $m^\ast=\hbar^2/2ta^2$ (right), $\hbar^2/ta^2$ and $-\hbar^2/2ta^2$.
- Figures to add, each with its pyqula script or the reason for numpy: `square_dos.py`, with `h.get_dos` of the square lattice and `tij=[-1.0]`, a new plot of (2.16) with its peak at $\epsilon=0$, where the Fermi surface at half filling is the nested square. Its caption gives the broadening and the k-mesh. `fermi_surface.py`, with `h.get_fermi_surface`, for the three pictures of the quiz.
- Old figures of the page that break the plot rules: `cos_velocity_mass` has titles in place of names on its three vertical axes and no ticks there, and its units are only in the caption. The panel of Session 9 shown again is not checked here.

## 2.11a The Dirac cone of the honeycomb lattice of graphene

File `11-the-dirac-cone-of-the-honeycomb-lattice-of-graphene-and-flat-band-lattices.md`, 1296 words, numbered equations (2.19), (2.20), (2.21).

- Question of the page, and where we arrive: why do the two bands of graphene touch, and what is the band close to the touching point? Three phases at $120^\circ$ cancel at $K$, so $f(K)=0$, and close to $K$ the band is the cone $E=\pm\hbar v_F|\mathbf q|$ with $v_F=3ta/2\hbar$.
- Main result for the key box: (2.20) and (2.21) in one box, with the sentence that $t$ and $a$ fix the velocity, and the geometry of the lattice fixes the position of $K$.
- Equation of another page that it starts from, for the recall box: `eq="2.12"`.
- Derivation told in words, for a steps fold: "From the off-diagonal entry (2.19) to the Dirac Hamiltonian (2.20)". The three phases at $K$, then the linear term $it\sum_j(\mathbf q\cdot\boldsymbol\delta_j)e^{i\mathbf K\cdot\boldsymbol\delta_j}$, whose modulus is $(3ta/2)|\mathbf q|$. The fold says that the form $q_x\sigma_x+q_y\sigma_y$ holds at $K$ after a choice of the axes and of the phase of the $B$ orbital, and that at $K'$ the sign of the $\sigma_y$ term changes. Both are checked by a number.
- Lab box, with the source and the number that the source states: `elias2011`, the link `https://www.nature.com/articles/nphys2049`. The probe is the cyclotron mass, measured for densities over three orders of magnitude. The sentence is "Our experiments also put an upper limit of ~0.1 meV on the possible gap in graphene." Our reading, marked as ours, is that massless means no gap down to this limit. The box can add that the velocity grows at low density from interactions, with the sentence "the Fermi velocity describing the spectral slope reaches ~3x10^6 m/s at n <10^10 cm^-2, three times the value commonly used for graphene", while (2.20) has a constant velocity. The lint has no unit m/s, so no script checks this second number. The abstract does not compare the cyclotron mass with (2.18). A sentence of ours on that comparison waits for the open point on Section 2.9, and it is marked as ours. No hopping in eV and no bond length is written from memory.
- Pen-and-paper problem: compute $|f(\mathbf k)|$ at $\Gamma$ and at $M$. The answer is $3t$ and $t$, so the bands span $-3t$ to $3t$, and the van Hove peaks of the density of states sit at $\pm t$.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the word massless has a question of 17 words and leans on (2.18), so it becomes "The cone $E=\pm\hbar v_F|\mathbf q|$ has no curvature along $\mathbf q$. Why is it called massless?". The quiz on the doubled hopping refers to (2.20) and (2.21), so the cone goes into the question. A new picture quiz shows three band structures on $\Gamma$-$K$-$M$-$\Gamma$ and asks which one is graphene with first-neighbor hopping only. The options are the honeycomb lattice (right), the same with `h.add_sublattice_imbalance(0.5)`, which has a gap of $1.0$ at $K$, and the triangular lattice, which has one band.
- Figures to add, each with its pyqula script or the reason for numpy: `graphene_bands.py`, with `geometry.honeycomb_lattice()` and the default hopping $+1$, which is the $+t$ of (2.19), for the three pictures and for a redraw of `graphene_path` if it is picked. `graphene_dos.py`, a new plot of the density of states, linear at zero energy and with peaks at $\pm t$, with the broadening in the caption.
- Old figures of the page that break the plot rules: `graphene_path` is numpy for bands that pyqula gives, and its axes are fine. `dirac_mass`, in a feedback, has no units and no ticks on $q_x$ and $E$, while its caption quotes $\hbar v_F=1$ and $m=0.5$.

## 2.11b Flat bands from the geometry of the lattice

File `11b-flat-bands-from-the-geometry-of-the-lattice.md`, 1054 words, numbered equations none.

- Question of the page, and where we arrive: can a band be flat when every hopping is nonzero? Yes, in the Lieb and the kagome lattices a state on one plaquette cancels on every site outside it, which gives a flat band at $\epsilon=0$ for the Lieb lattice and at $\epsilon=2t$ for the kagome lattice, with the sign of (2.5).
- Main result for the key box: an untagged display, see the open point on tags. The state with the amplitudes $(+1,-1,+1,-1,+1,-1)$ around one kagome hexagon has $H\psi=2t\psi$ for any $t$, and the flat band holds one third of the states.
- Equation of another page that it starts from, for the recall box: `eq="2.16"`.
- Derivation told in words, for a steps fold: "Why the state on one hexagon has the energy 2t". Each site of the hexagon gets $-t$ times the sum of its two neighbors on the hexagon, which is $2t\psi_j$. A site outside gets $-t(a-a)=0$. Then the same argument for the state of the Lieb lattice at zero energy.
- Lab box, with the source and the number that the source states: `kang2020`, the link `https://www.nature.com/articles/s41467-020-17465-1`, ARPES on the kagome metal CoSn. The sentence is "The flat band manifests itself as a dispersionless electronic excitation along the G-M high symmetry direction, with an order of magnitude lower bandwidth (below 150 meV) compared to the Dirac bands originating from the same orbitals." Our reading, marked as ours, is that the first-neighbor model gives a width of zero and that the orbitals and the further hoppings of CoSn give a small one. The gap of 80 meV at the touching point in the same abstract comes from spin-orbit coupling, which belongs to Session 3.
- Pen-and-paper problem: the Lieb lattice with the hopping $-t$. Find the energies at $\Gamma$ and at $M$. The answer is $\pm2\sqrt2\,t\approx\pm2.83\,t$ and $0$ at $\Gamma$, and three times $0$ at $M$.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the hexagon state has a question of 17 words, and its feedback cites "panel (e) of the figure". The question gets the amplitudes of the hexagon, and the panel is shown inside the quiz with `panel=` or the reference is dropped. The quiz on the value of $t$ stays. A new picture quiz shows three band structures from pyqula, the kagome lattice with `tij=[-1.0]` (right, flat at $+2t$), the kagome lattice with `tij=[1.0]` (flat at $-2t$) and the Lieb lattice (flat at $0$), and asks which one is the kagome lattice with $H=-t\sum$ and $t>0$. A new quiz has equations as options for $H\psi$ of the hexagon state, $2t\psi$ (right), $-2t\psi$ and $0$.
- Figures to add, each with its pyqula script or the reason for numpy: `kagome_bands.py`, with `geometry.kagome_lattice()` and `tij=[-1.0]`, bands and density of states, for the three pictures and for a redraw of `kagome_dos` if it is picked. The Lieb picture uses `geometry.lieb_lattice()` in the same script.
- Old figures of the page that break the plot rules: `kagome_dos` is numpy for bands and a density of states that pyqula gives, and its density axis has no unit and no ticks.
- The first paragraph, of 242 words, is split between the Lieb and the kagome lattice.

## 2.12 Measuring band structures with ARPES and 2.13 Closing summary

File `12-measuring-band-structures-with-arpes.md`, 1189 words, numbered equations none.

- Question of the page, and where we arrive: can we measure $E(\mathbf k)$, and the quasi-momentum itself? ARPES measures both, since the energy and the momentum along the surface are kept when the electron leaves the material.
- Main result for the key box: an untagged display, $\hbar k_\parallel=\sqrt{2mE_\text{kin}}\,\sin\theta$, with the sentence that the kinetic energy gives the energy of the state and the angle gives its momentum.
- Equation of another page that it starts from, for the recall box: `eq="2.10"`.
- Derivation told in words, for a steps fold: "From the emission angle to the momentum". $E_\text{kin}=p^2/2m$ and $p_\parallel=p\sin\theta$ is kept, with $20$ eV and $10^\circ$ giving the $4.0$ nm$^{-1}$ of the figure.
- Lab box, with the source and the number that the source states: `talirz2017`, the link `https://pubs.acs.org/doi/full/10.1021/acsnano.6b06405`, which is the "In the lab" cell of the notebook. The probe is ARPES together with Fourier-transformed STS, on armchair ribbons nine atoms wide on Au(111). The sentence is "Angle-resolved photoemission spectroscopy and Fourier-transformed scanning tunneling spectroscopy reveal an electronic band gap of 1.4 eV and effective masses of ≈0.1 m e for both electrons and holes, constituting a substantial improvement over previous efforts toward the development of transistor applications." Our reading, marked as ours, is that the mass is the curvature (2.18) of the measured bands at their edges. The text was read from OpenAlex, since Crossref has no abstract and the journal page refuses a script.
- Pen-and-paper problem: ARPES with $E_\text{kin}=20$ eV on a crystal with $a=0.4$ nm. Which angle reaches the zone edge $\pi/a$, and which angle at $80$ eV? The answer is about $20^\circ$ and $9.9^\circ$.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on what ARPES gives has a question of 18 words, so it is split into short sentences. The closing quiz on four orbitals stays. A new quiz in Section 2.12 has numbers with units as options, $k_\parallel$ for $20$ eV and $10^\circ$, $4.0$ nm$^{-1}$ (right), $7.8$ nm$^{-1}$ and $0.40$ nm$^{-1}$. A new picture quiz in Section 2.13 shows three densities of states and asks which one belongs to graphene.
- Figures to add, each with its pyqula script or the reason for numpy: `dos_three.py`, with `h.get_dos` of the chain with `tij=[-1.0]`, of the honeycomb lattice and of the kagome lattice with `tij=[-1.0]`, on the same energy axis, for the closing picture quiz.
- Old figures of the page that break the plot rules: none, `arpes_geometry` has its axes and its ticks.
- What the student can now do, the list of Section 2.13, fixed here so that the builder does not wait for the other pages.
  - Use a symmetry that commutes with $H$ to label the eigenstates by phases. This is in Section 2.3.
  - Find the eigenstates and the energies of a ring without a diagonalization. This is in Section 2.4.
  - Derive the band of a chain with first- and second-neighbor hopping, and say where its extrema are. This is in Section 2.5.
  - Say why $k$ is defined up to $2\pi/a$, and how the zone changes with the cell. This is in Section 2.6.
  - Write the Bloch Hamiltonian of a lattice with several orbitals per cell, and count the bands of a larger cell. This is in Section 2.7.
  - Write the band of the square and the cubic lattices, with their widths $8t$ and $12t$. This is in Section 2.8.
  - Read the density of states, the velocity, the effective mass and the Fermi surface from a band, and tell the three types apart by their density of states. This is in Section 2.9 and Section 2.10.
  - Derive the Dirac cone of graphene and its velocity. This is in Section 2.11a.
  - Say why the kagome and the Lieb lattices have a flat band, and at which energy it sits for a given sign of $t$. This is in Section 2.11b.
  - Turn an emission angle and a kinetic energy into a momentum along the surface. This is in Section 2.12.

## Lab sources stored for this session

Every source was fetched with `webnotes/labsource.py --session 2`, and each planned number was found in the full
copy by the function `find` of `labsource.py`, which is what `--check 2` prints once a box exists. The URLs are
spelled as in `sources/index.json`.

- `elias2011_nphys2049`, `https://www.nature.com/articles/nphys2049`, arXiv 1104.1396 attached. It has $0.1$ meV, found. It is planned for Section 2.11a.
- `kang2020_s41467-020-17465-1`, `https://www.nature.com/articles/s41467-020-17465-1`, arXiv 2002.01452 attached. It has $150$ meV and $80$ meV, found. It is planned for Section 2.11b.
- `talirz2017_acsnano.6b06405`, `https://pubs.acs.org/doi/full/10.1021/acsnano.6b06405`, the published abstract attached with `--paste` from `https://api.openalex.org/works/doi:10.1021/acsnano.6b06405`. It has $1.4$ eV, found. It is planned for Section 2.12. Its tracked file keeps only quotations of the numbers that a page quotes, and today it holds none. So after the box is written, `python3 webnotes/labsource.py --quotes` is run once by the coordinator, since builders do not write `sources/`.
- `ruffieux2016_nature17151`, `https://www.nature.com/articles/nature17151`, arXiv 1511.05037 attached, the zigzag ribbons of the notebook. No number with a unit, so no box. The pages also have no ribbon.
- `gonzalez-herrero2016_science.aad8038`, `https://www.science.org/doi/full/10.1126/science.aad8038`, arXiv 2009.13150 attached, hydrogen atoms on graphene in the notebook. It has $20$ meV, but it is a spin-split state from interactions, which no page of this session treats, so no box.
- `nilius2002_science.1075242`, `https://www.science.org/doi/10.1126/science.1075242`, the chain of gold atoms built with STM. Its abstract has "a 20-atom chain" and no value with a unit, so it backs a sentence and not a box.
- `bostwick2006_arxivcond-mat-0609660`, `https://arxiv.org/abs/cond-mat/0609660`, ARPES of graphene, stored on 2026-11-22 after the recheck d5 for the sentence of Section 2.12 on the measured cone. The arXiv record names no DOI, and its title differs from the one of Crossref for the paper in Nature Physics 3, 36, so the page links the arXiv abstract itself, which the tracked file keeps whole. It has no number with a unit, so it backs a sentence and not a box. labsource.py wrote this file and its line of `sources/index.json`, which the plan otherwise leaves to the coordinator.

## pyqula facts checked for this plan

These were run in the scratch folder of the plan with numbers, and they are confirmed against
`webnotes/conventions/session02.md` when that sheet exists.

- `geometry.chain()` with `tij=[-1.0,-0.5]` gives $-2\cos\varphi-2(0.5)\cos2\varphi$, with the momentum of `get_hk_gen` in units of $2\pi$. So `tij=[-1.0,-eta]` is the sign of (2.5) and (2.9).
- `geometry.square_lattice()` with `tij=[-1.0]` gives $-4$ at $\Gamma$ and $4$ at $M$. The path `["G","X","M","G"]` works, and `get_dos` has its peak at $\epsilon=0$.
- `geometry.honeycomb_lattice()` with the default hopping $+1$ has the bond length $1$, the energies $\pm3$ at $\Gamma$, $\pm1$ at $M$ and $0$ at $K$, and its density of states has its peaks at $\pm1$.
- `geometry.kagome_lattice()` with `tij=[-1.0]` has its flat band at $+2$, and `get_dos` peaks there. `geometry.lieb_lattice()` with `tij=[-1.0]` has its flat band at $0$, the energies $\pm2.83$ and $0$ at $\Gamma$ and three zeros at $M$.
- `h.get_fermi_surface(e=0.0, delta=0.1, nk=40)` returns three arrays of $1600$ points.
- `geometry.chain().get_supercell(5)` at $k=0$ gives the five energies of the ring, with and without a second-neighbor hopping, and `get_supercell(3)` gives $-2$, $1$, $1$ at $k=0$. `geometry.triangular_lattice()` takes the path `["G","K","M","G"]` and has one band, and the honeycomb lattice with `h.add_sublattice_imbalance(0.5)` has the gap $1.0$ at $K$.
- `geometry.bichain()` has the intracell and the intercell hopping $1$, so the chain of (2.13) is `h.inter = eta*h.inter`, as in the Session 3 script `g3_ssh_chains.py`.
- `get_bands` and `get_dos` write files such as `BANDS.OUT` in the folder where they run, so they run only inside a script that `style.run_script` runs. The recipes for the density of states, the Fermi surface and the supercell are not yet in `webnotes/scripts/RECIPES.md`.

## Builder groups

- `g1`, `01-motivation-and-recap.md`, `03-symmetry-operators-in-a-formal-way.md`, `04-exercises-where-we-guess-eigenstates-from-symmetry-only.md`. These pages share the rings of four, five and six sites and their pictures. The direction of the rotation is an open point that touches the quizzes of 2.3 and the key box of 2.4, so the builder keeps the direction of the page until it is decided and writes the new picture quiz so that its answer does not depend on it.
- `g2`, `05-blochs-theorem-and-the-first-band-structure.md`, `06-the-meaning-of-the-phase-which-is-the-quasi-momentum.md`, `07-multi-orbital-band-structures.md`. These pages share the chain, its band and its folded bands. The scripts use `tij=[-1.0,...]` for the sign of (2.5), and the chain with two sites uses the bichain of Session 3. The normalization of (2.6) and (2.7) and the `\boxed` of (2.8) are open points.
- `g3`, `08-higher-dimensional-band-structures.md`, `09-properties-of-an-electronic-dispersion.md`. These pages share the square lattice, its band, its density of states and its Fermi surface, with `tij=[-1.0]`. The file holds two sections, 2.9 and 2.10, each with its key box. Two sentences of Section 2.9 are open points.
- `g4`, `11-the-dirac-cone-of-the-honeycomb-lattice-of-graphene-and-flat-band-lattices.md`, `11b-flat-bands-from-the-geometry-of-the-lattice.md`, `12-measuring-band-structures-with-arpes.md`. These pages share the honeycomb and the kagome lattices, their bands and densities of states, and the closing picture quiz draws from both. They hold the three lab boxes of the session, and the box of Section 2.12 needs `labsource.py --quotes` from the coordinator after it is written. The list of Section 2.13 is fixed in this plan.
- `index.md` needs no edit and is in no group.

## Open for the lecturer

The lecturer decided on 2026-11-22 how to handle the points that the builders, the fixers and the rechecks left in
the old text ("Fix old-text errors, ask the rest"). Their lists, the twelve points of this section and the open points
of the conventions sheet were merged into 27 distinct points, and one more was found in that pass. Twelve were
sentences that were false as written, or that contradicted another sentence of the session, and they are corrected on
the web. The other sixteen were questions. On 2026-11-22 the lecturer picked points 1 and 3 ("ask me the top 5, other
you decide by yourself"), and the coordinator decided the other fourteen by its rule. The rule takes the option that
makes the text true with the smallest change and changes no numbered equation, reduces a claim that no stored source
or calculation supports to what is supported, rewrites a notebook box that does not match its cell, and leaves a
converted Blender figure and its overlay untouched. This pass first read that clause as covering the caption too. The
recheck of the same day reversed that reading in its point d1, since the caption is text of the page and was false as
written, so the caption of Figure 2.1 is now corrected on the web, while its render and its overlay are not touched.
This can be undone by putting the old sentence back. Each change was checked first with a calculation, and the check
script of its page asserts it. The points d1, d2 and d5 to d8 of that recheck change pages, and each is in the bullet
of the change it concerns. The points d3 and d4 change only the conventions sheet and `conventions.py`, and d9
changes nothing. The list "Decided on 2026-11-22" gives the
choice of each point and who made it, and the list "Not applied" what the rule leaves out. The old figures were
redrawn under the same names, as the lecturer picked on 2026-11-21, and the redraw also fixed the caption of
`square_bands`. The conventions sheet is up to date since 2026-11-22, and its last section lists the points of the old
text as decided or corrected, in the order of `conventions.py`.

### Corrected on the web, to carry over to the .tex

Each correction was checked first with a calculation of its own, by two routes where a number is involved, and the
check script of its page asserts it. The lines are those of `lecture_notes/src/sessions/session02.tex`.

- Page `01`, the quiz on the rotations of the square, feedback of the option $8$. Old "A rotation by $45^\circ$ moves a
  corner to the middle of an edge, so the square becomes a diamond." New "A rotation by $45^\circ$ moves each corner to
  a point beyond the middle of an edge, so the square becomes a diamond." The corner $(a,a)$ goes to $(0,\sqrt2\,a)$,
  outside the square. Not in the .tex. Asserted in `g1_01_motivation_and_recap.py`.
- Page `03`, Section 2.3, which was point 2 of this list. Old "Symmetry operators are always unitary." New "The symmetry
  operators of this session are unitary." Time reversal, which the box "Where this comes back" of the same page links to
  Section 3.11b, is antiunitary. (2.1) stays as it is. Line 81. Asserted in `g1_03_symmetry_operators.py`.
- Page `03`, Section 2.3, the dimer $H=t(c_1^\dagger c_2+\text{h.c.})$. Old "the bonding and antibonding combinations
  $c_1^\dagger+c_2^\dagger$ and $c_1^\dagger-c_2^\dagger$ ... the bonding state has eigenvalue $+1$ and the antibonding
  state has eigenvalue $-1$." New "the symmetric and antisymmetric combinations $c_1^\dagger+c_2^\dagger$ and
  $c_1^\dagger-c_2^\dagger$ ... the symmetric state has eigenvalue $+1$ and the antisymmetric state has eigenvalue $-1$."
  For $t>0$ the symmetric state is the upper level at $+t$, as the caption of `dimer_ring_symmetry` says. Lines 106 to
  108. Asserted in `g1_03_symmetry_operators.py`. The page of Section 3.8 calls the same state at $+t$ bonding, and it was
  not touched in this pass.
- Page `04`, Section 2.4, the ring of five sites, which was point 3 of this list. Old "so this overlap is $1/5$ for every
  $n$, for the lowest energy and for all other states." New "so this overlap is $1/5$ for every $n$, for the lowest
  energy and for all other states. This holds once we choose the eigenstates as these Fourier modes. It follows from the
  symmetry only", where the next sentence began with "This follows" before. With the plus sign of this
  $H$ the lowest level $2\cos(4\pi/5)$ holds two modes, and the states of this level have a weight from 0 to 0.40 on
  site 1. Line 154. Asserted in `g1_04_ring_eigenstates.py`.
- Page `04`, the quiz on the weight of one site, feedback of the option "It depends on the hopping amplitudes". Old "The
  eigenstates are the same Fourier modes as for $\eta=0$, and each site has the weight $1/6$." New "The eigenstates can
  be chosen as the same Fourier modes as for $\eta=0$, and each site has the weight $1/6$ in them." The levels $-0.7t$
  and $1.3t$ hold two states each, and $\cos(2\pi j/6)$ is an eigenstate at $-0.7t$ with the weights $1/3$ and $1/12$.
  Not in the .tex. Asserted in `g1_04_ring_eigenstates.py`.
- Page `05`, the try-it of Section 2.5. Old "for example `tij=[1.0,0.3,0.0]`". New "for example `tij=[1.0,0.2,0.0]`".
  The value 0.3 is above $t/4$, so its band already has the extra extremum, $0.033t$ deep, while 0.2 has none and 0.5
  has it, so "Increase it to $0.5$" now holds. Not in the .tex. Asserted in `g2_05_bloch_chain.py` with pyqula.
- Page `07`, Section 2.7. Old "The symmetry that diagonalizes (2.11) is a slightly richer version of a pure translation.
  It shifts the unit-cell index $n\to n+1$ *and* applies a unitary rotation among the orbitals within each cell." New
  "The symmetry that splits (2.11) into blocks, one for each phase, is the translation by one cell, which shifts the
  unit-cell index $n\to n+1$. It fixes the phase from one cell to the next, but not the combination of the orbitals
  within each cell, which is a unitary rotation among them." The rotation $U(\varphi)$ changes with $\varphi$ and comes
  from $H(\varphi)$. The translation alone leaves one block $H(\varphi)$ per phase, as `block_diagonal` of Section 2.3
  shows, so the verb "diagonalizes" of the old text became "splits into blocks", the words of Section 2.3, after the
  recheck o3. Lines 306 and 307. Asserted in `g2_07_multi_orbital.py`, with the blocks of a chain of seven cells with
  three orbitals.
- Page `07`, the notebook box of Section 2.7. Old "in the same spirit as (2.13), and there you can check that the
  numerical bands agree with $\epsilon_\pm(\varphi)$." New "in the same spirit as (2.13). For the ladder with one cell,
  `NS=1` in the first column of the plots, you can check that the numerical bands are $2\cos\varphi\pm1$, with the
  hopping $+1$ of the notebook. These are not the bands $\epsilon_\pm(\varphi)$ of (2.13), and the reason is the bond to
  the next cell. In the ladder each site hops to its own copy in the next cell, while in (2.13) the site $B$ hops to the
  site $A$ of the next cell." The rung is inside the cell in both, as the recheck o2 found. The cell also draws the
  supercells `NS=2` and `NS=3`, whose levels at $k=0$ are $-3,-1,1,3$ and $-2,-2,0,0,1,3$, the same two bands folded.
  Lines 347 and 348. Asserted in `g2_07_multi_orbital.py` with `geometry.ladder()`, the supercells included.
- Page `09`, Section 2.9, which was point 7 of this list. Old "A vanishing density of states means that interactions can
  hardly have any effect, however strong they are." New "A vanishing density of states means that a weak interaction can
  hardly have any effect, and only an interaction above a finite strength can drive such an instability." This agrees
  with Section 2.10, with the caption of Figure 2.4, which stays, and with the notebook cell "Phase transition with
  electronic interactions". The mean-field antiferromagnet of the honeycomb lattice needs $U$ above about $2.2t$, while
  the half-filled chain orders already at $U=t$. Lines 407 and 408. Asserted in
  `g3_09_properties_of_an_electronic_dispersion.py`.
- Page `11`, Section 2.11a. Old "This is the low-energy physics of every material with a honeycomb lattice, and of
  graphene in the first place." New "The massless cone is the low-energy physics of graphene, and of every honeycomb
  monolayer whose Fermi level sits at $K$ and $K'$. This holds as long as no term, such as a sublattice imbalance, opens
  a gap there." The picture quiz of the same page has the imbalance $0.5$ and the gap $1.0$ at $K$. After the recheck
  o1 the sentence names its subject, since the sentence before it is on the mass term, and two more conditions. A
  Bernal stack of two layers with the interlayer hopping $0.14t$ has no gap at $K$, but its band grows as $q^2$. One
  layer with a second-neighbor hopping $t_2=0.4t$ keeps the touching at $-1.2t$, while the Fermi level of half filling
  is at about $-0.744t$. The paragraph, of 159 words with the first correction, is split before "Graphene is famous",
  which is a web-only change. Lines 510 and 511. Asserted in `g4_11_dirac_cone.py`, the bilayer and $t_2$ included.
- Page `12`, Section 2.12. Old "Conservation of momentum and energy relates the momentum and kinetic energy of the
  electron, which are both measured directly outside the material, to its momentum and energy when it was still inside."
  New "The kinetic energy and the emission angle of the electron are measured outside the material, and together they
  give its momentum there. Conservation of energy and of the momentum along the surface then gives its energy and its
  momentum along the surface when it was still inside." The component along the normal changes at the surface, as the
  fold of the same page says. After the recheck o5 the first sentence names the angle, as the quiz of the same page
  does, since the momentum is obtained from the angle and the energy and is not measured directly. Lines 552 to 554.
  Asserted in `g4_12_arpes.py`.
- Page `12`, Section 2.13. Old "Every real dispersion is built locally from three types, which are parabolic, Dirac and
  flat." New "Almost every band structure in this course is built locally from three types, which are parabolic, Dirac
  and flat." These are the words of Section 2.10, and the chain with $t_3=1/3$ of the notebook has the local form
  $E\propto q^3$, which is none of the three. Lines 581 and 582. Asserted in `g4_12_arpes.py`.
- Page `05`, the first notebook box of Section 2.5, corrected on the page in the commit of the new shape and not in this
  pass. The old text ends with "check that the numerical spectrum follows $\epsilon_\varphi=-2t\cos\varphi$ from (2.8)
  when you scan $\varphi$ across the Brillouin zone." The page adds "The notebook takes the hopping $+1$, which is $t=-1$
  here, so its band is $+2\cos\varphi$, with the bottom at $\varphi=\pi$. The notebook plots $\varphi$ from $0$ to
  $2\pi$, so the bottom is still in the middle of its plot, and the cell is spinful, so each level comes twice." Lines
  230 and 231. Asserted in `g2_05_bloch_chain.py`.
- Page `03`, Section 2.3, the two examples, from point 1 of the lecturer. Old "we apply a $90^\circ$ rotation that
  shifts the sites by one in a cyclic way" and "The transformed wavefunction is $i$ times the original, so it is an
  eigenstate with eigenvalue $i$, that is $\varphi=\pi/2$." New "We apply a $90^\circ$ rotation that moves the
  amplitude of each site to the previous site, in a cyclic way" and "The transformed wavefunction is $-i$ times the
  original, so it is an eigenstate with eigenvalue $-i$, that is $\varphi=-\pi/2$." The state $(+1,-1,+1,-1)$ keeps
  $-1$. Lines 94 to 99. Asserted in `g1_03_symmetry_operators.py`. The quiz on $(1,i,-1,-i)$, now with the answer $i$,
  the steps fold, and the captions and scripts of `dimer_ring_symmetry`, now labelled $R=-i$, and `block_diagonal`,
  whose picture of $|H_{ij}|$ is the same for both senses, are web-only. Since the recheck d7 the two rings of
  `dimer_ring_symmetry` number their sites from 1 to 4 counterclockwise, from the site on the right, and the caption
  says so, since the direction "to the previous site" could not be read from a ring with no numbers. The matrix of
  `_g1_ring.py` now moves every amplitude to the previous site too, and its pictures, which check both senses, did not
  change.
- Page `04`, Section 2.4, the ring of three sites, from point 1. Old "with a symmetry $R$ that rotates
  $1\to2\to3\to1$ by $120^\circ$." New "with a symmetry $R$ that rotates the triangle by $120^\circ$. As in Section
  2.3, $R$ moves the amplitude of each site to the previous site, $(R\psi)_j=\psi_{j+1}$ with $\psi_4=\psi_1$." The
  rotation that takes the site 1 to the site 2 gives $\alpha_j\propto e^{i\varphi_nj}$ the eigenvalue
  $e^{-i\varphi_n}$, while the next sentence and Figure 2.1 need $e^{i\varphi_n}$. Lines 131 and 132. Asserted in
  `g1_04_ring_eigenstates.py`. The steps fold of the page, web-only, now uses this direction.
- Page `04`, Section 2.4, from point 16. Old "The eigenstates of any Hamiltonian with this rotational symmetry are
  exactly the three discrete Fourier modes on the ring", where the web had already dropped "exactly". New "...can be
  chosen as the three discrete Fourier modes on the ring". Line 141. Old "As long as the rotational symmetry of the
  ring is present, the symmetry eigenvalues, the eigenstates and expectation values such as this one are all fixed by
  symmetry only, however complicated the Hamiltonian becomes." New "As long as the rotational symmetry of the ring is
  present, the symmetry eigenvalues are fixed by symmetry only. The eigenstates can then be chosen as the Fourier
  modes, with the weight $1/L$ on each site, however complicated the Hamiltonian becomes." Lines 157 to 159. With a
  real hopping $(2,-1,-1)/\sqrt6$ is an eigenstate of the twofold level of three sites, with the weight $2/3$ on one
  site, and it is no Fourier mode. Asserted in `g1_04_ring_eigenstates.py`. The caption of Figure 2.1 is corrected
  too, in the next bullet.
- Page `04`, the caption of Figure 2.1 (`s02f01_ringmodes`), from the recheck d1. Old "This means that the eigenstates
  are the discrete Fourier modes, for any values of the hopping amplitudes." New "This means that the eigenstates can be
  chosen as the discrete Fourier modes, for any values of the hopping amplitudes." The text two lines above says "can be
  chosen as" since point 16. With the hopping $-t$ of (2.5) the ring of three sites has the levels $-2t$, $t$, $t$, and
  $(2,-1,-1)/\sqrt6$ is an eigenstate of the level $t$ that is no Fourier mode. The render and its overlay are not
  changed. `lecture_notes/src/figures/s02f01_ringmodes.tex`, lines 6 and 7. Asserted in `g1_04_ring_eigenstates.py` and
  `conventions.py`.
- Page `04`, Section 2.4, the STM sentences, from point 2. Old "With scanning tunnelling microscopy one can place
  single atoms with essentially arbitrary precision, and tight-binding rings with few sites like these have been built
  and measured in this way. There is a famous stop-motion film [...] It shows how precisely such models can now be
  realized in the lab." New "With a scanning tunneling microscope (STM) one can place single atoms one by one, and
  chains of gold atoms built in this way have been measured, in
  [this article](https://www.science.org/doi/10.1126/science.1075242)." The name of STM is spelled out since the recheck
  d8, as the old text did. Lines 161 to 165. The stored `nilius2002` says "The ability of a scanning tunneling
  microscope to manipulate single atoms is used to build well-defined gold chains on NiAl(110)" and "Spatially resolved
  conductance measurements along a 20-atom chain provide the dispersion relation, effective mass, and density of states
  of the free electron-like band." Asserted against the stored text in `g1_04_ring_eigenstates.py`. The two phrases are
  only in the full copy, which git ignores, so on a clean clone the script prints NOT CHECKED for them and asserts the
  title and the URL only. The tracked file keeps only the clauses with a number that a page quotes, and this sentence
  quotes none.
- Page `05`, Section 2.5, the normalization, from point 3 of the lecturer. This changes the numbered equation (2.7).
  Old (2.7) $\Psi_\varphi^\dagger=\sum_ne^{in\varphi}c_n^\dagger$, $c_n^\dagger=\sum_\varphi e^{-in\varphi}
  \Psi_\varphi^\dagger$. New (2.7) with the factor $1/\sqrt L$ in front of both sums, and the `\tag` stays 2.7. After
  "which is an ordinary Fourier transform between real space and the space of Bloch phases." the new sentences "Here we
  close the chain into a ring of $L$ sites, as in Section 2.4, so that $\varphi$ takes the $L$ values $2\pi m/L$, and at
  the end we take $L\to\infty$. The factor $1/\sqrt L$ makes the transform unitary, so $\Psi_\varphi^\dagger|0\rangle$ is
  the state (2.6) normalized to one, and (2.8) below does not change with it." The unnumbered display gets $\frac1L$
  in front of $\sum_{n,\varphi,\varphi'}$, and the orthogonality relation becomes "$\sum_ne^{in(\varphi'-\varphi)}=
  L\,\delta_{\varphi\varphi'}$, and the factor $L$ cancels the $1/L$ of the two normalizations." (2.6) and (2.8) are
  not changed. Lines 195 to 205. Asserted in `g2_05_bloch_chain.py` on 5, 8 and 12 sites and in `conventions.py`. The
  steps fold of Section 2.7, web-only, writes $c_{\varphi,\alpha}^\dagger$ with the same factor, asserted in
  `g2_07_multi_orbital.py`. The recall box of Section 2.7, web-only, shows the new (2.7), and since the recheck d2 it
  adds "The chain is closed into a ring of $L$ sites, so that $\varphi$ takes the $L$ values $2\pi m/L$, and at the
  end $L\to\infty$.", so that $L$ is named where (2.7) is shown.
- Page `05`, the second notebook box of Section 2.5, from point 15. After "check that the band you compute
  numerically agrees with (2.9)." the new sentence "The cell itself changes the third-neighbor hopping $t_3$, in the
  third place of `tij`." The cell loops over $t_3=0$, $1/3$, $2/3$ in `tij=[1.0,0.,t3]`. Lines 243 to 247. Asserted in
  `g2_05_bloch_chain.py`, from the notebook and with pyqula.
- Page `09`, Section 2.9, from point 5. Old "is the curvature of the dispersion, and it is the mass that is measured in
  essentially every transport or cyclotron-resonance experiment, since the bare electron mass cannot be observed
  directly inside a solid." New "is the curvature of the dispersion. For an isotropic parabolic band it is also the mass
  that is measured in transport and cyclotron-resonance experiments, since the bare electron mass cannot be observed
  directly inside a solid. For an anisotropic parabolic band, with the masses $m_1$ and $m_2$ along its two main axes,
  transport along one axis measures the mass of that axis, and cyclotron resonance measures $\sqrt{m_1m_2}$." The word
  "isotropic" and the last sentence come from the recheck d6, since (2.18) is a tensor. The cyclotron mass
  $(\hbar^2/2\pi)\,\partial A/\partial E$ of the square lattice is $0.506$ at $E=-3.9t$ by a count and by the formula,
  and it tends to the $0.5$ of (2.18) at the bottom, as does the mass of the Drude weight, while the cone has the
  finite $\hbar k_F/v_F$ where (2.18) is infinite along the radius. For $m_1=1/2$ and $m_2=2$ a count on the continuum
  gives the cyclotron mass $1.0006$, and the lattice with $t_x=1$ and $t_y=1/4$, which has these masses at its bottom,
  gives $1.016$ at $0.05t$ above it, with the Drude masses $0.501$ and $2.02$ along $x$ and $y$. Lines 422 to 424.
  Asserted in `g3_09_properties_of_an_electronic_dispersion.py`.
- Page `09`, Section 2.9, from point 14, web-only. "The size of the velocity is largest in the middle of the band" and
  the quiz "where is the size of the group velocity largest?", with "its size is largest" in the feedback of the right
  option and in the closing line of the quiz. The signed velocity is $-2ta/\hbar$ at $\varphi=-\pi/2$, its smallest
  value. Asserted in `g3_09_properties_of_an_electronic_dispersion.py`. Not in the .tex.
- Page `12`, Section 2.12, from point 6 and the recheck d5. Old "This is how the band structure and the Fermi surface
  of graphene are measured in practice, and the measured Dirac cone agrees well with the tight-binding derivation of
  Section 2.11." New "This is how the band structure and the Fermi surface of graphene are measured in practice. The
  measured bands show the Dirac cone of Section 2.11, distorted by the coupling of the electrons to each other, to
  phonons and to plasmons, in [this article](https://arxiv.org/abs/cond-mat/0609660)." Lines 556 and 557. No stored source
  compared the measured cone with the model, and the lab box of Section 2.11a says from `elias2011` that the real
  spectrum is not linear. The recheck d5 found that the first new wording had no stored source either, so the arXiv
  abstract of `bostwick2006` is now stored, and it says "Using angle resolved photoelectron spectroscopy (ARPES), we
  find that the expected conical bands are distorted by strong electron-electron, electron-phonon, and
  electron-plasmon coupling effects." Asserted against the tracked file in `g4_12_arpes.py`, which holds the arXiv
  abstract whole. The paragraph grew to 152 words, so on the web it is split before "This is how".
- Page `12`, Section 2.13, from point 13. Old "$H(\mathbf{q})\approx\hbar v_F(q_x\sigma_x+q_y\sigma_y)$ with
  $E_\pm=\pm\hbar v_F|\mathbf{q}|$ in (2.20)-(2.21)". New "$H(\mathbf{q})\approx\hbar v_F(q_x\sigma_x+q_y\sigma_y)$
  at $K$, with the opposite sign of the $\sigma_y$ term at $K'$, and $E_\pm=\pm\hbar v_F|\mathbf{q}|$ at both, in (2.20)
  and (2.21)". Lines 583 and 584. Asserted in `g4_12_arpes.py`, with the phase of the $B$ orbital of each valley.

### Decided on 2026-11-22

One bullet per point of the former list "For the lecturer", with the choice and who made it. "The coordinator" means
the coordinator by its rule of 2026-11-22, given in the opening paragraph of this section. The changes of the text are
in the list above, with their lines in the .tex.

- 1, the direction of the ring rotation. The lecturer picked "Turn the rotation of Section 2.3 around". $R$ now moves
  every amplitude to the previous site, $(R\psi)_j=\psi_{j+1}$, as $T$ of Section 2.4 and (2.6) need. So $(1,-i,-1,i)$
  has $-i$ and the quiz state $(1,i,-1,-i)$ has $i$. The text of Section 2.3, its quiz, its steps fold, the captions
  and scripts of `dimer_ring_symmetry` and `block_diagonal`, the sentence of Section 2.4 that defined $R$ by
  $1\to2\to3\to1$, the steps fold of Section 2.4, the check scripts and the conventions sheet changed with it.
- 2, the STM sentences of Section 2.4. The coordinator took "With STM one can place single atoms one by one, and
  chains of gold atoms built in this way have been measured", with the link to `nilius2002`, by the clause that
  reduces a claim with no stored source to what is supported. The rings "built and measured" and the film have no
  stored source, so the new sentence replaces the one on the rings, and the two sentences on the film are gone. After
  the recheck d8 the sentence spells out "a scanning tunneling microscope (STM)".
- 3, the normalization of (2.6) and (2.7). The lecturer picked "The factor $1/\sqrt L$ in (2.7) and $L\,\delta$ in the
  sum". (2.7) is the only numbered equation that changed, (2.6) stays unnormalized and (2.8) as printed, and one
  sentence says that the transform is unitary and that (2.8) does not change.
- 4, the `\boxed` of (2.8) inside the key box. The coordinator kept it, since the text is true either way and the
  removal changes a numbered equation.
- 5, the mass of transport and cyclotron resonance. The coordinator took "...and for a parabolic band it is also the
  mass that is measured in transport and cyclotron-resonance experiments", as the smallest change that makes the text
  true. "Essentially every" was false for the cone of Section 2.11a, whose cyclotron mass $\hbar k_F/v_F$ is finite
  while (2.18) is infinite along the radius. The third option, a sentence of ours in the lab box of Section 2.11a, is a
  larger change and was not taken. After the recheck d6 the sentence says "isotropic", and one more sentence gives the
  anisotropic band, where cyclotron resonance measures $\sqrt{m_1m_2}$.
- 6, how well the measured Dirac cone agrees. The coordinator took "...and the measured bands show the Dirac cone of
  Section 2.11a", by the clause on claims with no stored source. "Agrees well" has none, and `elias2011` in the lab
  box of Section 2.11a says that the real spectrum is not linear. The recheck d5 found no stored source for the new
  words either, so by the same clause the arXiv abstract of `bostwick2006` was stored and linked, and the sentence now
  says what it says, a cone distorted by three couplings.
- 7, numbers for the key boxes of Sections 2.10, 2.11b and 2.12. The coordinator kept the displays untagged, since a
  lettered tag adds numbered equations.
- 8, the sign of the downloaded scripts. The coordinator kept `tij=[-1.0]`, the sign of (2.5). The try-it boxes of
  Sections 2.5, 2.8 and 2.11b already name the sign of the notebook, so nothing changed.
- 9, the six-site ring with long-range couplings in Section 2.4. The coordinator kept it, since the statement is true
  and the next sentence names the schematic of five sites. A ring of six sites with real hoppings to the first, second
  and third neighbors has every Fourier mode as an eigenstate, asserted in `g1_04_ring_eigenstates.py`.
- 10, "Weyl semimetals, which are Dirac points generalized to higher dimensions" in Section 2.8. The coordinator kept
  it, since it is true when "Dirac point" means the two-band crossing of graphene, which is the meaning of the page.
- 11, the Berry phase of a Dirac dispersion in item 2 of Section 2.10. The coordinator kept it, since a massless cone
  has the Berry phase $\pi$. A Wilson loop about $K$ of graphene gives $\pi$, and the same loop with a sublattice
  imbalance $0.5$ does not, asserted in `g3_09_properties_of_an_electronic_dispersion.py`.
- 12, the condition on the ground state in the first bullet of Section 2.13. The coordinator kept it, since the
  sentence is true as written and fits the mean-field reading of the paragraph before the list.
- 13, the form at $K'$ in the closing bullet of Section 2.13. The coordinator took "...$\hbar v_F(q_x\sigma_x+
  q_y\sigma_y)$ at $K$, with the opposite sign of the $\sigma_y$ term at $K'$, and $E_\pm=\pm\hbar v_F|\mathbf q|$ at
  both", since the bullet read as the form at both points, which the key box of Section 2.11a contradicts.
- 14, "largest" for the velocity in Section 2.9. The coordinator took "The size of the velocity is largest..." and
  "where is the size of the group velocity largest?", as the smallest change that makes the text true, and the same
  two words go into the feedback of the right option and the closing line of the quiz, which had the same error. The
  feedback of "It is the same everywhere", the third option, stays.
- 15, the second notebook box of Section 2.5. The coordinator took "The cell itself changes the third-neighbor hopping
  $t_3$, in the third place of `tij`", by the clause that a notebook box is rewritten to match its cell, as the smaller
  of the two options that do so.
- 16, "are" or "can be chosen as" for the eigenstates of the ring of three sites. The coordinator took the third
  option, "...can be chosen as the three discrete Fourier modes on the ring..." and the sentence of the recheck o4,
  split in two for the length of the sentence. The second option also changes the caption of Figure 2.1. The pass
  first read the rule as leaving that caption alone, and the recheck d1 reversed the reading, so the caption now says
  "can be chosen as" too, in the list above. The render and its overlay are not touched.

### Not applied

- The full copy of `nilius2002`, from the recheck d8. The two phrases that back the STM sentence of Section 2.4 are
  asserted only where `webnotes/sources/.full/` exists, which git ignores, as in Session 5 for `tsuei1994`. The
  tracked file keeps only clauses with a number that a page quotes, and `labsource.py --quotes` writes it again from
  the full copy, so a phrase added by hand would not stay. Whether such a sentence needs an assert on every clone is a
  point of the toolkit, and it is left to the coordinator.
- Section 3.8 of Session 3 still calls the sum of the two sites of the dimer, at the energy $+t$, the bonding
  combination (`session03/08-three-topological-material-classes.md`, line 81), while Section 2.3 now calls it the
  symmetric state. It is a point about Session 3 that touches a sign, so the rule leaves it.
