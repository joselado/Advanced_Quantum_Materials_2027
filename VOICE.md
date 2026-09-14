# Writing in the course voice

How the Advanced Quantum Materials material is written, so that a new session can produce
lecture notes, notebook cells, slides or narration that read like the existing material and not
like a language model's default register. Everything here is grounded in the recorded lectures
(the primary evidence for the voice), the notebook markdown written by the lecturer, the slides,
and the approved lecture notes.

How to use this file: read sections 1 to 3 before writing anything. Use sections 4 to 8 as a
reference while writing. Run the checklist in section 10 before finishing. If a rule here
conflicts with what the transcript for a given session actually says, the transcript wins.

The process conventions (box density, figure pipeline, citation rules) live in the private
Dropbox repo, `~/unix/Aalto Dropbox/Jose Lado/adv_quantum_materials_2027/lecture_notes_style_guide.md`.
This file is about voice and complements it; its sections 1 and 2 (prose voice, sentence-level
rules) are assumed here and not repeated in full.

---

## 1. Where the voice comes from, and which layers are canonical

| Source | Path (relative to this repo) | Size | What it is | Status for imitation |
|---|---|---|---|---|
| Spoken lectures, 2026 (cleaned ASR) | `transcripts/subtitles_2026_clean/sessionN.txt` | 86k words, 10 files | The lecturer narrating the prerecorded slide decks, one file per topic | **Canonical.** Primary evidence for the voice |
| Notebook walkthroughs, 2026 (raw ASR) | `transcripts/subtitles_2026_notebooks/sessionN.txt` (1, 2, 3, 5 only) | 32k words | The lecturer solving the notebook exercises live on video | **Canonical** for the walkthrough register |
| Raw ASR, 2026 and 2025 | `transcripts/subtitles_2026/`, `transcripts/subtitles_2025/` | 90k words each | Uncleaned transcripts, plus `.srt` with timestamps. 2025 files are named by topic, not number | Canonical but noisy. Use to check what was literally said |
| Topic-segmented cleaned transcripts | `transcripts/transcripts_cleaned/topicNN_*.md` | same as 2026 clean | Same content, split by slide topic | Derived copy |
| Notebook markdown: session header, `##` titles, one-line intros, quiz bullets, "In the lab" | `jupyter-notebooks/sessionN.ipynb` | 17k words total | Written by the lecturer | **Canonical** for the notebook register |
| Notebook markdown: the explanatory paragraph under each one-line intro | same files | | Added after the 2026 edition in a textbook register with 73 em-dashes, then rewritten on 2026-09-14 in the notebook register (pattern in section 4.4) | Rewritten, not lecturer-written. Use as examples of the explanatory paragraph only, after the canonical layers |
| Slides | `slides_prerecordings/lectureN.pdf` | | Terse slide text, learning outcomes, take-home slides | Canonical for the slide register |
| Lecture notes | `lecture_notes/src/sessions/sessionNN.tex` | 58k words | Compiled from the transcripts and slides by Claude, then approved by the lecturer | **Approved written register.** Imitate its cleanliness; keep the transcript's warmth |

Three facts about the sources that matter before quoting or imitating them:

- `transcripts/` is gitignored and local only. It was copied from the private Dropbox repo
  (`subtitles_2025`, `subtitles_2026`, `subtitles_2026_clean`, `subtitles_2026_notebooks`,
  and `lecture_notes/transcripts_cleaned`). This repo is public on GitHub, so nothing from the
  transcripts is published; the notes and notebooks are.
- The cleaning pass that produced `subtitles_2026_clean` inserted 377 em-dashes. The lecturer
  does not use them (there are none in the raw ASR, none in the notebook markdown they wrote,
  none in the slides). Every quote in this file has had them removed, and no text written for
  this course should contain one.
- The written notes are a deliberately cleaned version of the spoken voice. The verbal glue
  ("in particular", "of course", "essentially") drops by a factor of 10 to 30 between transcript
  and notes (section 3). Copying the transcript's tic density into written notes produces a
  transcript, not notes; dropping the narrated build-up produces a textbook. The target is in
  between, and the approved chapters show where.

---

## 2. Who is speaking

- A lecturer at Aalto talking to master's and PhD students, as a colleague who happens to know
  more, not as a textbook. The student is assumed to have seen single-particle solid-state
  physics ("this is a type of material that you have already seen in basics of materials
  physics") and standard quantum mechanics ("from conventional quantum mechanics, you were
  probably using first quantization").
- A non-native (Spanish) English speaker with a fluent, distinctive English: long sentences
  chained with commas and "and", "so", "and in particular", "and of course"; a few plain
  phrasings a copy editor would smooth ("how does the spectra look like", "which change do you
  observe", "make the system bigger"). Keep the plainness. Do not manufacture errors, and do not
  polish quiz questions into formal academic prose.
- Enthusiastic and generous with intensifiers: exceptionally, extremely, incredibly, very, very,
  fascinating, exotic, fantastic, inspiring, non-trivial, sophisticated, way more challenging.
  At the same time honest and specific about what is hard: approximations are called
  uncontrolled when they are, open problems are called open.
- Inclusive "we" is the default subject (we are going to, let us, we will see, we have). "You"
  appears when the student's own reasoning is being traced ("if you think about", "you can think
  that", "what you actually see is"). "I" appears only at framing moments: the welcome, a
  recommendation ("I would strongly encourage you to watch this recording"), a personal aside
  ("if you are me and you're not aware of this choice"), and the closing request ("if I could
  ask you to remember something").
- Physics is told as building up: the simplest case first, then the general one; the symmetric
  Hamiltonian, then what breaks it; the tool, then what it predicts, then how you would measure
  it. Names come after the construction ("This is what is called the Bogoliubov-de Gennes
  Hamiltonian"), not before.
- Everything is tied to what can be computed (pyqula, Quantum Lattice, the Jupyter notebooks)
  and what can be measured (STM, ARPES, transport, "this is what one can measure with STM, for
  example").

---

## 3. Four registers, one voice

| Register | Used for | Feel | Signature |
|---|---|---|---|
| **Spoken lecture** | Narration scripts, re-recordings, video summaries | Long comma-chained sentences, "Okay, so let us..." seams, tics as glue | "Welcome to our session on...", "So the question is...", "What is important is that...", "if I could ask you to remember something" |
| **Notebook walkthrough** | Narrating a notebook exercise, answering quiz questions aloud | Short present-tense steps, "And so...", "right?", "bigger and bigger and bigger" | "So what we do is we create a chain. We compute the Hamiltonian. We plot...", "So let us go through the question.", "The answer to this question is that, well, ..." |
| **Written notes** | `lecture_notes/src/sessions/*.tex` | Narrated build-up with the tics stripped; rhythm carried by colons, semicolons, parentheses | "Let us start with...", "Here is the puzzle...", "It is worth being precise about...", "Numerically, this shows up exactly as you would hope" |
| **Notebook cells** | `##` titles, one-line intros, quiz bullets, "In the lab" | One sentence per intro, imperative quiz bullets ending in a question | "We will now see how...", "Let us now address...", "Make the system bigger. What happens, and why?" |
| **Slides** | Slide text | Two or three short lines per slide, titles as questions | "Today's learning outcomes", "Central idea:", "Take home" |

### 3.1 Calibration table

Occurrences per 1000 words, measured on the sources in section 1. Use it to spot-check a draft:
count "in particular" and "of course" in what you wrote and compare.

| Phrase | Spoken lecture | Walkthrough | Written notes | Notebook cells |
|---|---|---|---|---|
| of course | 3.1 | 1.7 | 0.1 | 0 |
| essentially | 3.0 | 0 | 0.4 | 0.4 |
| in particular | 2.4 | 2.0 | 0.1 | 0.2 |
| effectively | 1.9 | 2.0 | 0.2 | 0.2 |
| we are going to | 1.8 | 7.9 | 0.1 | 0 |
| let us | 1.5 | 2.9 | 0.5 | 2.7 |
| let's | 1.2 | 2.9 | 0 | 0 |
| we will | 0.9 | 0.5 | 1.2 | 4.6 |
| you can think | 1.0 | 0.2 | 0 | 0 |
| okay, | 1.0 | 2.0 | 0 | 0 |
| give(s) rise | 1.0 | 0.4 | 0.03 | 0.7 |
| let's say | 0.9 | 1.2 | 0 | 0 |
| in practice | 0.8 | 0.6 | 0.2 | 0 |
| the idea is | 0.8 | 0.3 | 0.1 | 0 |
| relatively | 0.8 | 0.4 | 0 | 0 |
| if you think | 0.7 | 0 | 0 | 0 |
| and so forth | 0.7 | 0.1 | 0 | 0 |
| meaning that | 0.6 | 0.4 | 0 | 0 |
| right? | 0 | 0.9 | 0 | 0 |
| very, very | 0.1 | 0.4 | 0 | 0 |
| rationalize | 0.1 | 0.03 | 0.02 | 0.5 |
| colon | 2.6 | n/a (raw ASR) | 14.4 | 4.7 |
| semicolon | 1.0 | n/a (raw ASR) | 4.2 | 1.1 |
| em-dash | 0 (377 inserted by cleaning) | 0 | 0 | 0 |
| Mean sentence length (words) | 35 (median 32) | 24 (median 16) | 32 (median 30) | n/a |
| Sentences that are questions | 2.5% | 6.4% | 1.0% | 47% |

Most common sentence openers: spoken lecture "This is", "If you", "So the", "You can", "Okay,
so", "So if", "Of course", "So in", "So now"; walkthrough "And so", "So we", "And then", "So the";
written notes "This is", "It is", "The same", "Let us", "Take a", "For a", "We will".

Vocabulary that changes with register (decide per document, never mix inside one):

| Spoken lecture | Written notes | Note |
|---|---|---|
| biquadratic (23 times; "quartic" never spoken) | quartic (17 times) | The lecturer's word is biquadratic. Speech and notebook text: biquadratic. The approved chapters use quartic; keep that inside the notes for consistency |
| single particle, mean field, tight-binding | single-particle, mean-field, tight-binding | Hyphenate compound modifiers in the notes only |
| non-trivial | non-trivial or nontrivial (both appear) | Prefer non-trivial |
| let's, don't, it's, you're | let us, do not, it is | Contractions are speech only. A few slipped into the notes ("we'll", "you'd"); do not add more |
| two-to-the-L, L equal to 20, U equal to zero | $2^L$, $L=20$, $U=0$ | Speech says numbers; notes typeset them |

---

## 4. How a session is built

### 4.1 Spoken lecture

**Opening** (all ten sessions follow it):

> Welcome to our session about second quantization, mean field, and spontaneous symmetry
> breaking. Today we are going to focus on a technique that allows us to understand how quantum
> mechanics can actually appear at macroscopic scales in a very specific type of materials
> called quantum materials, and in particular we are first going to understand what a quantum
> material is, which kinds of different quantum materials there are, and how we can rationalize
> their properties using this formalism.

Pattern: "Welcome to our session on X. Today we are going to [focus on / look at / see how] ...,
and in particular ... We will see ..., and afterwards ..., and finally we will ...". The learning
outcomes are sometimes read out as a list: "The learning outcomes for today are, first, to
recognize what is the nature of a superconducting state ...; to understand excitations in
superconductors using the Nambu formalism ...; and finally we will use this formalism to show
that ...". Session 2 adds a one-sentence recap ("As a brief reminder of the previous session, I
would like just to mention that we will be interested in Hamiltonians that are essentially
written in second quantization."); the other sessions go straight from the welcome to today's
plan. Nine sessions say "session"; session 3 says "our lecture on".

**Motivation before mathematics.** Session 1 spends several minutes on the stone, copper,
silicon and quantum ages, MRI magnets, solar cells, quantum computing and the UN goals before a
single equation. Session 4 opens with which materials show the quantum Hall effect and at what
temperature. The rule: say why anyone cares, in concrete materials and technologies, then start.

**A tour before the tools.** "Let me show you a variety of different types of quantum materials
that we will be able to rationalize", followed by a spoken list: "We have quantum spin Hall
insulators, that are systems that show a gap in the bulk but then helical states at the edges;
we have Chern insulators, which are systems that show a gap in the bulk but then chiral states at
the edges; we have chiral superconductors, that are superconducting systems that show propagating
Majorana excitations; crystalline topological insulators, and many others."

**Seams.** Every change of slide or subtopic is marked with "Okay": "Okay, so let us start from
the beginning.", "Okay, so let us now focus on a specific type of quantum many-body
Hamiltonian.", "Okay, so that was charge density waves. Let us now move on to magnets." About
once per 1000 words in a lecture, twice that in a walkthrough.

**Inside a segment**, in this order, most of the time:

1. The question. "So now the question is: let's imagine that we want to describe a quantum dot
   where the quantum dot sometimes has zero electrons and sometimes it has two electrons ... So
   the question is, how do we describe these types of systems?"
2. The simplest case. "Okay, so let us start with the simplest case, which is the case of a
   charge density wave."
3. The idea. "The idea is very simple." / "The basic idea is that ..." / "The whole idea is
   that ..."
4. What the mathematics means. "What this actually means is that you can no longer just deal
   with states that have one particle, but you need to consider the full Fock space."
5. The plot. "This plot shows the single particle energies of the effective single particle
   problem; let us remind ourselves that we have a mean field Hamiltonian, and the mean field
   Hamiltonian is effectively a single particle Hamiltonian, and the x-axis here is the strength
   of the electronic repulsion. At zero electronic repulsion you effectively have a metal, so
   there's no gap anywhere, and as you ramp up the repulsion, suddenly a gap opens up in your
   single particle spectrum."
6. What matters. "What is important about superconductors is that this gap opens up regardless
   of what is the specific electronic dispersion that you have, regardless of whether we have
   first- or second-neighbor hopping, regardless of where your chemical potential is."
7. The pointer. "This is, of course, something for which we are going to dedicate a whole
   session." / "but we will go through this more in detail in the lecture about
   superconductivity."

**Closing** (nearly verbatim in sessions 2, 3, 4, 5 and 9; sessions 1, 8 and 10 use a variant;
sessions 6 and 7 have none):

> So this is everything I wanted to tell you today, and if I could ask you to remember
> something, please remember that the response to perturbations in quantum materials allows us
> to understand the nature of the underlying state; that the response to perturbations actually
> depends on the underlying electronic structure; and that we can predict how fluctuations are
> going to behave in a quantum material just by understanding the underlying electronic
> structure. ... Thank you so much for your attention.

Variants: "So, just to summarize, if I could ask you to remember one thing, please remember
that ...", "So, to summarize, today we have seen how ...", "As a summary, I would like you to
remember that ...". Usually three points (two in session 2, four in session 5), phrased as a
request to remember or as "today we have seen how", never as "key takeaways". Sessions 6 and 7
end on their last subtopic with no summary at all; when writing from those, do not invent one
(see `index.md` in the Dropbox repo).

### 4.2 Notebook walkthrough

(The walkthrough transcripts are raw ASR; in the quotes below the recognition errors listed in
section 11 have been corrected, nothing else.)

Opens with "Hi, welcome to the first exercise session with Jupyter notebooks", reminds the
student that core exercises are the ones to understand and challenge exercises are optional,
and explains the template: "you have a template code, and this template code computes some
basic thing that we would like to consider ... and then afterwards this example, you have a few
questions that you need to answer. And so let's start with this code."

Per exercise:

1. What the code does, one step per short sentence, present tense, "we" as subject: "So what we
   do is we create a triangular lattice. We generate the Hamiltonian. We add Rashba coupling. We
   shift our chemical potential. We add the Zeeman field, superconductivity. Then we generate a
   one-dimensional system. So a ribbon, we compute the bands of our ribbon."
2. What the plot shows: "So what we see in this plot is that there are effectively four
   eigenvalues. This is because we have two sites times two from the spin degree of freedom."
3. The question, read out: "So let's go with the first question." / "So let us go through the
   question." / "Okay, so now let us go to the question."
4. The answer, starting with "well": "The answer to this question is that, well, as we make the
   system bigger and bigger and bigger, the tight-binding matrix that describes the system
   becomes also bigger and bigger and bigger." / "Well, the reason for that is because the
   interaction needs to overcome the bonding-antibonding hopping."
5. The change, done live: "So what we can do now is ...", "so instead of 0.1 let's take 0.05",
   "And you see that, well, we have a gap that becomes smaller and smaller and smaller."
6. The lesson: "So the bottom line is that these edge states are protected, meaning that we
   don't have to have a perfect island or a perfect edge to have them, but they are going to
   appear in general for any generic edge."

Also characteristic: "right?" as a check on the listener (30 times in 32k words), "these
calculations take a bit, so let us just wait until they finish", "for concreteness we can
recompute it again so that you see that we get the very same result", "let's create another copy
of this so that we can, let's say, compare one by one". Closes with "And so this is everything
for today. Thank you so much for joining."

### 4.3 Written lecture notes

One `\chapter` per session, in `lecture_notes/src/sessions/sessionNN.tex`. The approved
chapters show the shape:

- **Opening paragraph.** Pick up the previous session's thread (or say there is none: "This is
  the first session of the course, so there is no previous cliffhanger to pick up."), state the
  question of the day, preview what will be built ("By the end of today we will have used that
  tool three times, to build a charge density wave, a magnet, and a superconductor out of the
  very same starting Hamiltonian"), and flag what will and will not be revisited later.
- **Section titles** are descriptive and sometimes read like the spoken question: "Why quantum
  materials, and why now", "A warm-up in first quantization, and the puzzle that breaks it",
  "Where the two formalisms diverge: the exponential wall", "Worked example 1: the charge
  density wave".
- **Paragraphs** of five to ten sentences that narrate. Openers that recur: "Let us start
  with...", "Here is the puzzle that motivates everything that follows.", "Now here is the
  puzzle.", "It is worth being precise about which symmetry this breaks", "With this general
  picture in hand, let us now go build it explicitly, three times over.", "Numerically, this
  shows up exactly as you would hope".
- **Equations** are numbered and referred to by number in the prose; the prose says what each
  term is in words right after ("read as 'destroy an electron at 1, create one at 0' plus the
  reverse process").
- **Notebook callouts** use `\begin{notebookbox}{\texttt{sessionN.ipynb}, ``Exact exercise
  title'' (Core)}` and say in two or three sentences what to run and what to look for.
- **Figures** are `\input{figures/sNNfMM_name}` and are always referred to in the prose before
  they appear ("figure~\ref{fig:s01:fockspace} draws both sides of the comparison explicitly").
- **Bulleted lists** appear only for taxonomies (the tour of materials, the quasiparticles, the
  three broken symmetries) and for the closing summary. Explanations are prose.
- **Closing.** A `\section{Closing summary}` with five or six bullets, then one paragraph
  starting "Next session, ..." that says what comes next and what will not be recapped.
- The Dropbox style guide's rules apply on sight: no em-dashes, no "well-known" or "textbook" or
  "literature", no year citations, no narrative attributions not backed by the transcript, box
  density limits.

### 4.4 Notebook cells

**Session header cell:**

```markdown
# Advanced Quantum Materials, session 7: Quantum entanglement and tensor networks
In this session we will address systems showing entangled ground states, and how they can be solved with tensor networks

### Contents
- System-size scaling of exact diagonalization and matrix product states
- Convergence of tensor network results with the bond dimension

### Learning outcomes
- Rationalize the role of entanglement in ground state
- Understand the ability of tensor networks to parameterize many-body wavefunctions

### About the exercises
The notebooks contain two types of exercises, with each exercise containing **Quiz** questions to answer
- ***Core***: basic exercises you should understand in each session
- ***Challenge***: advanced exercises to dive deeper into concepts, not necessary to understand in full in each session
```

Session 5 adds a third tag, `***Reminder***: brief recall from previous sessions, you can skip it
if you remember it`. Session 7 adds "### It is not necessary to complete all the exercises, you
can just focus on those that sound most interesting for you." Learning outcomes start with
Understand, Rationalize, Identify.

**Exercise cell:**

```markdown
## Gap opening in the Hubbard model on the honeycomb lattice (***Challenge***)
We will now see how the Hubbard interaction give rise to a gap opening in an interacting honeycomb lattice
```

then the code cell, then

```markdown
### Quiz
- What difference do you see with respect to the linear chain above?
- At which value of the interaction you think that you have symmetry breaking?
- Replace the honeycomb lattice by a square lattice. How is it different from the honeycomb lattice?
```

then, sometimes,

```markdown
#### In the lab
- Zigzag graphene nanoribbons featuring edge states can be synthesized using on-surface synthesis, showing the correlated states noted above
https://www.nature.com/articles/nature17151
```

The one-line intro is one sentence, no period, starting "We will now see how ...", "Let us now
look at ...", "Let us now address ...", "Here we will show how ...", "First, we will show ...",
"We will start with ...", "Before we considered ... We will now see that ...", "So far we have
focused on ... Let us now address ...". Session 2 uses `### Exercise` instead of `### Quiz`.

**Explanatory paragraph** (between the intro and the code cell; these were rewritten on
2026-09-14 in this register and are not lecturer-written). One paragraph of 40 to 100 words, no
header, no closing formula. It says what the code cell does ("Here we take a chain with $L$
sites and open boundary conditions"), gives the one idea needed to read the plot, with the
equation inline or displayed if there is one, and ends by pointing at what to look at ("Look at
how the gap evolves as you increase $J$"). It does not answer the quiz bullets that follow it:
where the bullet asks why, the paragraph stops at the observation. Openers rotate between a
plain statement, "Here we take", "Now we", "You can think that", "What is important is that",
"Remember that", "Keep in mind that", with "The idea is that" at most once or twice per
notebook. It never says "the questions below ask", never cites, never uses an em-dash.

**Quiz bullet grammar** (from the 274 questions in the notebooks). One to five bullets; each is
short; most combine an instruction and a question:

- Why-questions: "Why does the magnetization saturate at large interactions?", "Why is there a
  gap even when there is no magnetization?"
- Instruction, then question: "Make the system bigger. What happens, and why?", "Replace the
  honeycomb lattice by a square lattice. How is the Fermi surface now?", "Increase the value of
  the Haldane coupling. At which energies you have now edge states", "Remove the magnetic field,
  do you still see states localized at the edges?", "Recompute the previous local density of
  states, but now with a narrower ribbon. What happens to the edge states?", "Take a supercell of
  the system, and repeat the calculations above. Do you observe the same phenomenology?"
- Verbs that open instructions: Make, Replace, Change, Increase, Decrease, Add, Remove, Take,
  Recompute, Compute, Identify, Discuss, Count, Show that, Perform, Put, Include.
- Reasoning prompts: "Discuss which solution you think it has the lowest energy, and why",
  "Discuss how this can be rationalized in terms of topological invariants", "Can you infer what
  is the functional form of the gap as a function of the width, and why?", "How can you infer
  from the spectra the nature of each ground state?"
- Two questions in one bullet joined by a comma: "Make the system narrower, what happens to the
  in-gap modes and why?"
- Function names in parentheses when the student needs them: "(honeycomb_zigzag_ribbon)",
  "(add_rashba)", "(add_pairing(mode="swave"))".
- "(Advanced)" prefix for an optional harder bullet.

### 4.5 Slides

Title slide with the topic. A "Today's learning outcomes" slide (eight of the ten decks) with
three or four bullets starting Explain, Understand, Identify, Describe, Rationalize, Recognize or
Derive. Slide titles are short noun phrases ("The idea of
second quantization", "Three types of many-body sites") or questions ("How do we describe
quantum matter?", "Which materials are we aiming to understand?", "How to know if a material is
magnetic?", "What a material being 'ferromagnetic' means?"). Bodies are two or three lines:
"Central idea: a ground state can break the symmetry of a Hamiltonian", "Let us do it for
graphene islands", "Lets see some examples using the two-levels presented before". Contrasts are
laid out side by side (First quantization | Second quantization; Magnet | Not a magnet; "It sticks
to your fridge" | "It breaks time-reversal symmetry"). The last slide is "Take home" with three
lines, the same points spoken in the closing (eight of ten decks; lectures 6 and 7 have none,
matching their transcripts).

---

## 5. The rhetorical moves

Each move, what it does, and quotes from the transcripts (em-dashes removed, nothing else
changed). Use these as patterns, not as text to reuse.

**5.1 Ask the question first, then answer it.** The question is spoken in full, often with
"So the question is" or "Now an important question is, well", and the answer follows at once.

> So now the question is, are all states of matter, or all the quantum materials of interest,
> classified according to symmetries that they break? And the answer to this question is no:
> there are some materials that have unique properties, that cannot be classified according to
> the symmetry that they break, and these materials are called topological materials.

> Now an important question is, well, how do you get those expectation values? The way to do
> this is just by solving a self-consistent problem, and the idea is very simple.

**5.2 Name the idea before the derivation.** "The idea is", "The basic idea is", "The whole
idea is", then the mechanism in one breath. Afterwards "The bottom line is" or "What is important
is that" closes the segment.

> The idea is that you define a spinor operator that takes the following form: the upper part is
> your conventional annihilation operators, and then you make a copy so that you have creation
> operators.

> So the bottom line is that this mean field Hamiltonian for the spinon excitations describes
> single particle excitations in a quantum spin liquid that have spin one half and that have a
> certain dispersion.

**5.3 Simplest case first, then generalize.** A dimer before a chain, three sites before L
sites, a square lattice before a triangular one, s-wave before nodal.

> Let's take a relatively simple Hamiltonian, a Hamiltonian of three sites, and when we have
> three sites we just have to consider three different levels. ... This is for three sites; if
> you keep doing this for bigger and bigger systems, in particular for systems with L sites, what
> you actually see is that ... you in general need to deal with a system that has two-to-the-L
> elements.

**5.4 Define by contrast.** Two things side by side, one property that separates them.

> biquadratic interactions are hard, but bilinear interactions are easy, so what we are going to
> do is take expectation values of two of the terms and leave the other two free

> in a superconductor you need to pay a finite amount of energy to put in a single electron, you
> don't have to pay any energy if you insert two electrons

> Semiconductors are different from insulators in the sense that the electrons can move, because
> they are slightly doped

Standing pairs used throughout the course: first vs second quantization; single particle vs
many-body; Hilbert space vs Fock space; bilinear vs biquadratic; symmetric Hamiltonian vs
non-symmetric ground state; symmetry classification vs topological classification; classical
magnets vs quantum magnets; conventional vs correlated (or unconventional) superconductors;
trivial vs topological; bulk vs edge; gapped vs gapless; physical copy vs spurious copy.

**5.5 Say it twice.** The same statement restated with one word changed, for emphasis and to
give the listener a second chance.

> magnets only exist because electrons interact with each other, magnets only exist because
> electrons are repelling each other due to Coulomb interaction

> Your Hamiltonian was originally symmetric, your Hamiltonian had initially equivalent
> solutions, but the solution of this Hamiltonian, each one individually, is not symmetric, and
> this is what spontaneous symmetry breaking means

> if you want to diagonalize a superconductor, if you want to find the eigenenergies and
> eigenstates of a superconductor, you simply have to write down this four-by-four matrix

In the written notes this becomes one sentence with an appositive or a parenthesis; do not
literally repeat.

**5.6 Spell it out with "meaning that".** Every abstract statement is followed by its concrete
content: "meaning that", "which in practice means that", "what this actually means is that",
"so in practice".

> there are some quantum materials where the number of electrons fluctuates, meaning that at
> some time you have one electron, then you have two electrons, then you have three electrons,
> then you have four electrons

> This property automatically implies that you cannot have two particles in the same level,
> because if i and j are the same, then the square is zero

**5.7 Everyday analogy, then straight back to the physics.** The analogy is told as a small
story, with the lecturer in it, and then mapped term by term.

> To understand this let us start with a very simple example, an example that you probably have
> experienced when going for lunch with your colleagues. Let us imagine that we go to a table, we
> all sit at the table, we have our plates in front of us, we have our bread in front of us, and
> at some point we need to choose a bread to pick. ... So we have a problem that is originally
> symmetric, but whose dynamics, in a way, give rise to a solution that is not symmetric.

> in magnets we actually have a ground state that breaks time reversal symmetry, meaning that if
> you somehow record your system and play the movie backwards, then the system would be the
> opposite of what it is

> magnets are these things that stick to your fridge, but if we want to look for a more
> mathematical definition, then the way we define them is as objects that break time reversal
> symmetry

> So the idea is, for example, let's imagine you want to classify clothes: you want to classify a
> purse and distinguish it from a shirt.

**5.8 Read the plot aloud.** Say what the axes are, what the colors are, where zero is, and
what happens as you move along the axis. "over here" and "over there" point at the slide.

> you are going to get your physical copy, which is the band structure shown here in red, but
> then you have this spurious copy, which is this band structure in blue

> This gap over here is what is called a Mott gap; it's a gap that appears due to repulsion in a
> spinful system, and it's associated with the emergence of a local moment at each site, and of
> course this gap becomes linearly proportional to the interaction at very large values of the
> interaction.

In the notes, "over here" becomes a figure reference and the reading stays: "at V=0 the
spectrum is gapless (a metal); as V grows, a gap opens in the single-particle spectrum and
widens, while the charge imbalance between even and odd sites grows from zero toward its
maximal, fully polarized value."

**5.9 Tie the mathematics to what it means and to what can be measured.**

> you can think that a spinon is only the spin sector of an electron: the charge is frozen but
> the spin is free

> This type of profile is not just a result of a calculation, but it's something that can be
> observed experimentally, using atomically resolved spectroscopy, in particular scanning
> tunneling microscopy.

> These two techniques allow us to see if a system breaks time reversal symmetry ... if the Hall
> conductivity is non-zero, or the magneto-optical Kerr effect is non-zero, then we know that
> time reversal symmetry is spontaneously broken.

**5.10 Be honest about approximations and open problems.** The hedge is specific, not
generic.

> This is, of course, in principle an uncontrolled approximation; there are, let's say, much
> more controlled ways of doing it, using, let's say, a path integral and a fixed point, but from
> a practical point of view, mean field theory just relies on this type of approximation.

> Unconventional superconductors are a major open challenge: we do not have a good theory to
> predict them, we are not capable of predicting what are the critical temperatures of systems
> that are unconventional superconductors, even though we've tried for many decades

> even though this is a relatively simple problem to write, it is an exceptionally hard problem
> to solve

**5.11 Point forward and backward inside the course.** The course is one story; every session
says what it borrows and what it defers.

> This is, of course, something for which we are going to dedicate a whole session.

> And this will become important later on in the lecture about magnetism.

> So this is effectively what you watched in the recording.

> This, in a way, is one of the most fascinating types of quantum materials, and it's also one
> of the most challenging ones, but we are going to discuss them more in detail in the next few
> sessions.

The correct pointers per session (what is a real cliffhanger, what is only thematic adjacency,
what was dropped this year) are documented in `lecture_notes/index.md` in the Dropbox repo.
Do not invent a recap or a callback that the transcript does not support.

**5.12 Hand the student an intuition with "you can think that".**

> You can think that an electric polarization is like an intrinsic electric field, it is the
> electric analog of a magnetization

> you can think of these different matrix elements as the free parameters for your machine
> learning problem, and in particular you can treat them as if they were parameters of a neural
> network

**5.13 Emphasis by repetition and intensifier.** Triples in speech ("bigger and bigger and
bigger", "many, many, many gaps"), doubled "very, very", and the intensifier set from section 2.
In the notes this becomes a single well-chosen adjective.

> Superconductivity, and in particular correlated superconductivity, is one of the biggest open
> challenges in science

> This, in a way, is one of the most fascinating types of quantum materials, and it's also one of
> the most challenging ones

---

## 6. Sentence-level habits

- **Length and glue.** Spoken sentences average 35 words and routinely run to 60, joined by
  ", and", ", so", ", and in particular", ", and of course", ", meaning that", ", which is".
  Written notes average 32 words but break the chain with colons, semicolons and parentheses
  instead. Notebook intros are one sentence. Quiz bullets are one or two short sentences.
- **Openers.** "So", "Okay, so", "And so", "Now", "Of course", "If you think about", "Let us",
  "This is", "The idea is", "What is important is that", "Something very interesting is that".
  In the notes: "Let us", "This is", "It is worth", "Take a", "Consider", "Here is", "Now".
- **Pronouns.** "We" by default; "you" for the student's reasoning and for the plot ("what you
  actually see"); "I" only for welcome, encouragement, closing; "one" occasionally for a generic
  agent ("one takes a chain", "one can measure").
- **Hedges.** "let's say" before an approximate word or number; "in a way", "in a sense",
  "somehow", "roughly", "relatively", "kind of", "at least", "in principle", "effectively",
  "essentially". Not "arguably", "perhaps somewhat", "to some extent".
- **Certainty.** "automatically", "exactly", "regardless of", "all the time", "always opens up
  a gap", "just by", "simply", "the only thing that you need". When something is certain the
  lecturer says so plainly.
- **Causal connectors.** "the reason for this is", "this is just because", "because of course",
  "and therefore", "and so", "that is why", "as a simple consequence of this".
- **Sequencing.** "first ..., then ..., and finally ..."; "afterwards"; "so far ..., now ...";
  "before we discussed that ..., now ...".
- **Contractions.** Speech: let's, don't, it's, you're, there's, we've. Notes and notebook
  cells: let us, do not, it is.
- **Punctuation.** Never an em-dash, in any register. Speech is commas; notes carry rhythm with
  colons (14 per 1000 words), semicolons and parentheses. Exclamation marks do not occur.
- **Numbers.** In speech: "two-to-the-L", "L equal to 20", "U bigger than zero", "a 50 by 50
  matrix", "on the order of one Kelvin". In notes: typeset mathematics.

---

## 7. Lexicon

Preferred words and constructions, with the alternatives a model would reach for instead.

| Use | Instead of | Example |
|---|---|---|
| rationalize | explain, make sense of | "how we can rationalize their properties using this formalism" |
| account for | describe, capture, model | "single particle physics is capable of accounting for much of the phenomena" |
| give rise to, driven by | lead to, produce, induce, cause | "this Coulomb interaction sometimes gives rise to ferromagnetism"; "gap opening driven by interactions" |
| phenomenology | behaviour, physics, features | "a very similar phenomenology happens"; "Do you observe the same phenomenology?" |
| emergent, emergence, appear | arise (fine too), manifest | "the emergence of a local moment at each site"; "a gap appears" |
| quantum many-body (as adjective) | strongly correlated, many-particle | "quantum many-body interactions", "quantum many-body wave function" |
| single particle / single-particle | one-body, free, non-interacting (used too, less) | "an effective single particle Hamiltonian" |
| biquadratic (speech), quartic (notes) | four-fermion, two-body | "the problematic term in the Hamiltonian, the challenging term, is the biquadratic term" |
| bilinear | quadratic | "biquadratic interactions are hard, but bilinear interactions are easy" |
| field operators, creation and annihilation operators (always in that order) | ladder operators, second-quantized operators | "a gauge transformation is just a transformation where we change the phase of our field operator" |
| mean field theory, mean field Hamiltonian, at the mean field level | Hartree-Fock (rarely said), self-consistent field | "mean field theory allows us to rationalize a variety of unconventional states" |
| self-consistent, solve it self-consistently, self-consistency | iterate to convergence, fixed-point iteration | "this is a self-consistent problem, in the sense that your Hamiltonian depends on the expectation values" |
| hopping, first-neighbor hopping, nearest-neighbor hopping, "hopping between site i and site j" | tunneling amplitude, transfer integral | "a term that essentially tells you that electrons from level one can go to level zero and vice versa" |
| on-site energy, on-site repulsion, Hubbard interaction, the Hubbard U | local potential, local Coulomb term | "the electronic repulsion is going to be an on-site repulsion between spin up and spin down" |
| sites, site number zero, site number one | atoms (unless a real material), orbitals (only when orbitals are meant) | "two sites connected by a hopping" |
| sublattice imbalance | staggered potential, mass term, Semenoff mass | "the sublattice imbalance opens a gap" |
| exchange field, Zeeman field | magnetic field (when it is a spin splitting in the Hamiltonian) | "as you increase the value of the exchange field, you start closing the superconducting gap" |
| electronic structure (umbrella), band structure, dispersion relation, spectral function, density of states, local density of states | spectrum (used too), DOS profile, LDOS map | "what happens to the electronic structure and why?" |
| a gap opens up, gap opening, the gap closes, opens up a gap | gapping out, gap formation, gaps the spectrum | "a gap opens up regardless of what is your chemical potential" |
| reciprocal space, Brillouin zone | k-space, momentum space (acceptable, less used) | "opens up gaps in some parts of reciprocal space" |
| in the bulk, at the edge, edge states, in-gap states, zero modes | boundary modes, midgap states | "a gap in the bulk but then chiral states at the edges" |
| correlated state, symmetry broken state, order parameter | ordered phase, broken-symmetry phase | "the appearance of a gap driven by strong electronic repulsion" |
| topological invariant, non-trivial, protected, robust | topologically nontrivial index, immune | "these edge states are protected" |
| chiral, helical (edge states) | unidirectional, counter-propagating spin-polarized | "helical states at the edges" |
| the thermodynamic limit, an infinitely large system, the non-interacting limit, the strongly interacting limit, at half filling, in units of t | the bulk limit, weak/strong coupling (used less) | "U equal to zero is what we call the non-interacting limit" |
| exotic, unconventional, sophisticated, non-trivial, exceptionally | novel, cutting-edge, remarkable, elegant | "very exotic phenomena in electronic systems" |
| platform, building block, harness, quantumness | enabler, leverage, exploit | "quantum materials are the platform that allows us to harness this quantumness" |
| the recording, this session, the next few sessions, the lecture about magnetism | this lecture (used, less), this module, this unit | "this is effectively what you watched in the recording" |
| pyqula, Quantum Lattice, the Jupyter notebooks, the template code | the code, the library | "we are going to run calculations with a numerical library that is called pyqula" |
| STM, atomically resolved spectroscopy, ARPES, transport, Hall conductivity | experimental probes, spectroscopic measurements | "This is what one can measure with STM, for example" |
| "the way we do this is by", "the reason for this is", "this is just because", "just by", "regardless of", "as long as", "at least", "in the limit of very large U", "for concreteness", "as a reference" | "by virtue of", "owing to", "notwithstanding", "for the sake of clarity" | |
| "to summarize", "if I could ask you to remember something", "Closing summary" | "in summary", "key takeaways", "TL;DR" | |
| "let us now look at", "we will now see how", "here we will show" | "in this section we discuss", "we now turn to", "in this notebook we explore" | |

Words the lecturer does not use in ten lectures and that should not appear: delve, unpack,
showcase, highlight (as a verb for ideas), underscore, elegant, intriguing, nuanced, robustly,
seamlessly, holistic, landscape (as metaphor), journey, dive (except the fixed "dive deeper into
concepts" in the notebook boilerplate). Near-absent: leverage (twice), beautiful (once).

---

## 8. What not to do

The defaults of a language model that read wrong next to this material. The first three are
also in the Dropbox style guide, section 2; the rest are additional.

1. **Em-dashes.** None, anywhere. Rewrite with a comma, colon, semicolon or parentheses.
2. **Appeals to authority.** No "well-known", "standard textbook result", "any standard
   textbook", "the literature", "it is easy to see". State the result.
3. **Year citations and narrative attributions.** No "(1931)", no "first proposed by X, later
   extended by Y" unless the transcript says it. Field eponyms (Haldane model, AKLT state, Bethe
   ansatz) are vocabulary and stay.
4. **Signposting adverbs.** No "It is worth noting that", "Notably", "Crucially", "Importantly",
   "Interestingly", "Remarkably" as sentence openers. The lecturer's versions are "What is
   important is that", "Something very interesting is that", "The interesting point is that",
   "Note that", "What matters is that".
5. **Definition-first paragraphs.** Not "A charge density wave is defined as a periodic
   modulation of the charge density." Build it: the chain, the repulsion, what mean field does
   to the term, what comes out, then "this is what is called a charge density wave".
6. **Label-colon bullets in explanations.** Not "**Key insight:** ..." or "**Physical
   picture:** ...". Bullets are for taxonomies and closing summaries only; everything else is
   prose.
7. **Generic headings.** Not "Introduction", "Overview", "Summary", "Key takeaways",
   "Conclusion". Use "Why quantum materials, and why now", "Closing summary", or the spoken
   question.
8. **Compressed encyclopedic sentences.** Not "The half-filled honeycomb Hubbard model
   undergoes a Mott transition at U_c ≈ 2.3t within mean-field theory." Narrate: the density of
   states vanishes at the Dirac point, so a small interaction does nothing, and only when the
   interaction becomes large enough does the gap open; in the notebook the value comes out
   around 2.3.
9. **Over-polished quiz questions.** Not "Investigate the dependence of the spectral gap on the
   interaction strength and provide a physical interpretation." Write "Increase the interaction.
   What happens to the gap, and why?"
10. **Invented structure.** No closing summary for sessions 6 and 7, no neural-network quantum
    states in session 7, no "as a reminder" framing in session 4's Kubo derivation. When the
    transcript stops, the notes stop.
11. **Formal hedging.** Not "arguably", "to some extent", "it could be argued". Use "let's say",
    "in a way", "roughly", "at least", "in principle".
12. **Contractions in the notes.** "let's", "don't", "we'll" are speech. Notes say "let us",
    "do not", "we will".
13. **Exclamation marks and emojis.** Never.
14. **Rhetorical flourishes.** Not "full stop", "the skeleton the rest of the course hangs on",
    "a rich zoo". A few of these are in the approved chapters; they are tolerated there, not a
    model to extend. When in doubt, use the plainer phrase closest to the transcript.
15. **Reframing the student.** Not "Consider a reader unfamiliar with..." or "For the
    uninitiated". The student is a colleague who has seen materials physics and quantum
    mechanics.

---

## 9. Before and after

Rewrites of a model's default text into the course voice, one per register. The "Before" blocks
are the only place in this file where em-dashes and the banned phrases appear, on purpose; a
grep for them should hit nothing outside this section.

### 9.1 Written notes

Before:

> Mean-field theory is a widely used approximation in which the quartic interaction term is
> replaced by an effective quadratic one — this is achieved by decoupling the operator product
> into expectation values. Notably, the resulting Hamiltonian must be solved self-consistently.
> It's worth noting that this approach is uncontrolled; however, it remains the standard textbook
> starting point.

After:

> The troublesome term is the quartic one, the term with four fermionic operators, because it is
> exactly what makes the problem exponentially hard. Mean-field theory keeps things simple: take
> the expectation value of two of the four operators and leave the other two free, so that the
> interaction becomes a bilinear term, an on-site energy that a single-particle calculation can
> handle. Nothing forces that expectation value to be the same on every site, and that is where
> the physics is going to come from. Since the Hamiltonian depends on the expectation values and
> the expectation values depend on the Hamiltonian, we solve it self-consistently: guess a
> Hamiltonian, compute the expectation values it implies, build a new Hamiltonian from those, and
> repeat until the process converges. This is, to be clear, an uncontrolled approximation (a path
> integral with a saddle point is the more rigorous route), but it is the practical workhorse we
> will use throughout the course.

### 9.2 Notebook cell

Before:

> ## Interaction-Driven Metal-Insulator Transition in the Honeycomb Lattice (Core)
> In this exercise, we explore how on-site Coulomb repulsion — parameterized by the Hubbard U —
> induces a metal-insulator transition in graphene-like systems. Key questions:
> 1. What is the critical value of U?
> 2. How does this compare to the one-dimensional case discussed earlier?

After:

> ## Gap opening in the Hubbard model on the honeycomb lattice (***Challenge***)
> We will now see how the Hubbard interaction gives rise to a gap opening in an interacting honeycomb lattice
>
> ### Quiz
> - What difference do you see with respect to the linear chain above?
> - At which value of the interaction do you think that you have symmetry breaking?
> - Replace the honeycomb lattice by a square lattice. How is it different from the honeycomb lattice?

### 9.3 Spoken narration (walkthrough)

Before:

> Next, we'll examine the effect of increasing the bond dimension. As shown in the plot, the
> energy variance decreases monotonically, confirming convergence of the MPS ansatz.

After:

> Okay, so now let us look at what happens when we make the bond dimension bigger and bigger.
> So what we are doing here is we take the same Heisenberg chain, we compute the ground state
> with a matrix product state for different bond dimensions, and for each one we compute the
> fluctuation of the energy, so the expectation value of H squared minus the expectation value of
> H, squared. And the whole idea is that for an exact eigenstate this fluctuation is exactly
> zero, right, so the smaller this number, the closer we are to the true ground state. And what
> you actually see in the plot is that as we increase the bond dimension the fluctuation becomes
> smaller and smaller and smaller, so already with a bond dimension of, let's say, 20, we are
> effectively converged. So let us go through the question.

### 9.4 Spoken narration (lecture)

Before:

> Superconductivity breaks U(1) gauge symmetry. This can be seen by applying a phase rotation to
> the fermionic operators: bilinear terms are invariant, whereas the anomalous pairing term
> acquires a phase factor of 2φ.

After:

> Something very important about this superconducting order is that it breaks something called
> gauge symmetry, and gauge symmetry is associated with the notion of the complex phase of a
> wave function, or the complex phase of our field operators. If we phrase this in terms of field
> operators, a gauge transformation is just a transformation where we change the phase of our
> field operator: the annihilation operator picks up a phase e to the i phi, and the creation
> operator picks up a phase e to the minus i phi. So if you have a term in the Hamiltonian that is
> c-dagger c, regardless of the different indices that you have, then the gauge transformation
> does not create any change; but if you have a term in the Hamiltonian that has two creation or
> two annihilation operators, then that term changes when you make a gauge transformation. And
> so, since a superconductor has a finite expectation value of c c, a superconductor breaks gauge
> symmetry.

---

## 10. Checklist before finishing

- [ ] Register chosen (lecture, walkthrough, notes, notebook cell, slide) and the draft matches
      that column of the calibration table, not another one.
- [ ] Opens by saying what we are going to do (and, for speech, "Welcome to our session on");
      closes with three things to remember (speech) or a Closing summary plus a "Next session"
      paragraph (notes).
- [ ] Every new object is built up before it is named; the simplest case comes before the
      general one.
- [ ] Every derivation has at least one "what this means" sentence, and at least one link to a
      plot, a notebook exercise or a measurement.
- [ ] Not a single em-dash. No "worth noting", "notably", "crucially", "delve", "unpack",
      "well-known", "literature", no year citations.
- [ ] Spot-checked "in particular" and "of course": near 2 to 3 per 1000 words in speech, near
      zero in notes and notebook cells.
- [ ] Quiz bullets are short, mostly an instruction plus "What happens, and why?", and use the
      verb set in section 4.4.
- [ ] Terms come from the lexicon; hyphenation and contractions follow the register.
- [ ] Nothing is claimed that the transcript and slides for that session do not support;
      forward and backward pointers agree with `index.md`.
- [ ] Quotes taken from `subtitles_2026_clean` have had their em-dashes removed.

---

## 11. Working from the transcripts

- For a session's notes, read `transcripts/subtitles_2026_clean/sessionN.txt` end to end first,
  then the slides. Follow the audio order (for session 9 the PDF page order differs from what
  was spoken).
- Reuse the lecturer's own analogies and examples; do not replace them with different ones.
- Use `transcripts/subtitles_2026/sessionN.srt` when a timestamp is needed, and
  `transcripts/subtitles_2025/` only to check whether something was said in an earlier year
  (its file names are by topic: `superconductivity.txt`, `magnetism.txt`, `tensornetworks.txt`,
  `excitations.txt`, `machinelearning.txt`, `quantumhall.txt`, plus `session1` to `session4`).
- The walkthrough transcripts are raw ASR. Common garbles and what they mean: "H-states" =
  edge states; "held-in", "halting", "holding coupling" = Haldane coupling; "chair number",
  "Cher number" = Chern number; "bary curvature" = Berry curvature; "berylong zone" = Brillouin
  zone; "Pycula" = pyqula; "timer" = dimer; "sides" = sites; "anti-pharmatic",
  "anti-pharmagnetic" = antiferromagnetic; "rush springer", "Rushba" = Rashba; "semanfield" =
  Zeeman field; "button structure" = band structure; "zircon" = Dirac cone; "hover module",
  "Habar model" = Hubbard model; "high bar timer" = Hubbard dimer; "Amcher ribbon" = armchair
  ribbon; "CMAP field" = Zeeman field; "MIM field" = mean field. The 2025 raw files have their
  own set ("minim field", "cager", "kulom", "graffine", "churn insulators", "by quadratic").
