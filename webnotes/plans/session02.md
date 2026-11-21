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

These change a numbered equation, a statement of the old text or a convention, so a builder does not decide them.

1. The direction of the ring rotation in Sections 2.3 and 2.4. The rotation of Section 2.3 moves each amplitude to the next site, so $(1,-i,-1,i)$, which is $e^{-i\pi j/2}$, has the eigenvalue $i$. The key formula of Section 2.4, $\alpha_j\propto e^{i\varphi_n j}$ for the eigenvalue $e^{i\varphi_n}$, and the translation $T$ of Section 2.4 with (2.6) need the amplitude to move to the previous site. The set of modes is the same, and only the labels flip. The options are to keep both and name the direction on each page, to turn the rotation of Section 2.3 around, so that $(1,-i,-1,i)$ has $-i$ and the quiz state $(1,i,-1,-i)$ has $i$, or to write $\alpha_j\propto e^{-i\varphi_n j}$ in Section 2.4.
2. Section 2.3 says "Symmetry operators are always unitary", while time reversal, which the box "Where this comes back" of the same page links to Section 3.11b, is antiunitary.
3. Section 2.4 says that the weight $1/5$ holds "for every $n$, for the lowest energy and for all other states". The levels $n$ and $-n$ of the ring of five sites are degenerate, and the real combination $\cos(2\pi j/5)$ is also an eigenstate of $H$, with weights $0.40$, $0.04$, $0.26$, $0.26$, $0.04$. The statement holds for the eigenstates chosen as eigenstates of $R$.
4. Section 2.4 says that rings with few sites "have been built and measured" with STM and names the film "the smallest film ever made", with no source. The stored `nilius2002` is a chain of 20 gold atoms built with STM, not a ring, and it gives no number with a unit. The options are to keep the sentences, to write chains with this link, or to drop the sentence on the film.
5. The equations (2.6) and (2.7) have no factor $1/\sqrt N$, and the sum $\sum_n e^{in(\varphi'-\varphi)}$ in the derivation is $N\delta_{\varphi\varphi'}$. A fold can say "up to the normalization", or the equations get the factor, which changes numbered equations.
6. The equation (2.8) has a `\boxed` around $\epsilon_\varphi=-2t\cos\varphi$. Inside a key box the frame is doubled, so it stays or goes.
7. Section 2.9 says "A vanishing density of states means that interactions can hardly have any effect, however strong they are". Section 2.10 of the same page says that a finite interaction is needed, and the notebook cell "Phase transition with electronic interactions" opens a gap in the honeycomb lattice above a critical $U$.
8. Section 2.9 says that (2.18) "is the mass that is measured in essentially every transport or cyclotron-resonance experiment". The cyclotron mass equals (2.18) for a parabolic band. In graphene `elias2011` measures a finite cyclotron mass, while Section 2.11a says that (2.18) is infinite along the radius and not defined at the tip.
9. Section 2.12 says "the measured Dirac cone agrees well with the tight-binding derivation". `elias2011` finds a velocity three times larger at low density from interactions, and the ARPES abstract of Bostwick and coworkers (arXiv cond-mat/0609660, read and not stored) finds the cones "distorted by strong electron-electron, electron-phonon, and electron-plasmon coupling effects".
10. A key box on a page with no numbered equation, in Sections 2.10, 2.11b and 2.12, holds an untagged display. The rule of the numbering allows a lettered tag such as (2.21a) instead.
11. The old figures that break the plot rules are listed in the blocks, and they are `block_diagonal`, `ring_long_range`, `chain_eta`, `band_sign_t`, `aliasing`, `ssh_recipe`, `fold_three`, `square_bands`, `decoupled_chains`, `cos_velocity_mass`, `graphene_path`, `dirac_mass` and `kagome_dos`. They are redrawn now under the same names with the scripts of this plan, as `berry_haldane` was in Session 3, or left and reported. `square_bands` also has a caption that says more than its picture, which a redraw in the extended zone or a change of the caption fixes.
12. The scripts that the students download use `tij=[-1.0]`, the sign of (2.5), while the notebook uses $+1$ for the chain, the square and the kagome lattices. The other choice is the sign of the notebook, with every figure of these lattices turned upside down against the page.
