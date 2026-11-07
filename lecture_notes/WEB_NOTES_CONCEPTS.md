# Concepts that come back across the web notes

This table is the shared input for the "where this comes back" boxes and for the bridging sentences of the
web notes. Each row is one concept that appears in more than one session. The defining anchor is the place
where the concept is built with its equation, and a link to it is written `[...](#anchor)`, so the build
points it to the right page. The table was made on 2026-11-07 by a grep of `webnotes/pages/`, with every anchor
checked against `webnotes/labels.json`. A page is listed when its Markdown contains the name of the concept,
so a page that only names it in passing is listed too, and a page that uses the concept under another name is
not.

A page is written in short form. `s06/06` is the file of `webnotes/pages/session06/` whose name starts with
`06-`, `s03/10b` is the one that starts with `10b-`, and `s04/index` is the index page of the session. The
column "Met before" gives the place where the concept appears first, when this is earlier than the page
that defines it. Two concepts are built twice, and the choice of the defining page is a decision that can
be changed. The Landau levels appear first in `s03/06` and are derived in `s04/09`, and here the derivation
defines them. Linear response is built in `s03/02` and again in detail in `s09/03`, and here the first
construction defines it, as for the Haldane model, which is defined in `s03/10b` and recapped in `s04/19`.

The Jordan-Wigner transformation is in the list of the lecturer but the name appears only in Session 7. It
stays in the table since it is the bridge between the spin chains of Session 6 and Session 8 and the
fermions of Session 1, and a box on those pages can link it. Superexchange, the entanglement entropy and DMRG
were checked and appear in one session only, so they are not in the table.

The patterns of the grep are listed after the table, so that a column can be checked again after an edit.

| Concept | Defining anchor | Met before | Sessions | Other pages that use it |
|---|---|---|---|---|
| Haldane model | `session03/10b-the-haldane-coupling-and-a-real-chern-insulator.md#sec-3-10b` |  | 4 | s03/01, s03/05, s03/07, s03/13, s04/19, s04/20, s04/index, s06/16, s09/08 |
| SSH model | `session03/08-three-topological-material-classes.md#sec-3-9` (#sec-3-9c) | `s02/07#sec-2-7` | 5 | s02/07, s02/12, s03/01, s03/09b, s03/09c, s03/13, s03/index, s04/index, s05/16, s05/17, s05/20, s05/index, s09/08 |
| Stoner criterion | `session06/06-the-stoner-threshold-as-a-criterion-for-magnetism.md#eq-6-3` (#sec-6-6) |  | 3 | s02/11b, s06/17, s09/05, s09/05b, s09/11, s09/index |
| Nambu spinor and BdG | `session05/08-the-nambu-spinor-and-the-bogoliubov-de-gennes-hamiltonian.md#sec-5-8` |  | 5 | s01/05, s01/14, s02/08, s02/12, s05/12, s05/14, s05/15, s05/17, s05/19, s05/20, s05/index, s08/06, s10/07, s10/08 |
| Chern number and Berry curvature | `session03/05-the-berry-curvature-and-why-the-hall-conductivity-is-an-integer.md#eq-3-4` (#sec-3-5) |  | 7 | s02/09, s02/11b, s02/12, s03/02, s03/06, s03/07, s03/08, s03/10, s03/10b, s03/11, s03/11b, s03/12, s03/13, s03/index, s04/03, s04/05, s04/18, s04/19, s04/20, s04/index, s05/02, s05/12, s05/14, s05/20, s06/16, s06/index, s09/08, s10/06, s10/06b |
| Berry phase and Zak phase | `session03/09c-the-ssh-model-the-bloch-hamiltonian-and-the-zak-phase.md#eq-3-6` (#sec-3-9c) |  | 7 | s01/02, s02/09, s02/11, s03/12, s03/13, s04/16, s04/18, s05/17, s09/08, s10/06, s10/06b |
| Mean field | `session01/12-the-general-interacting-hamiltonian-and-the-tool-we-will-use-on-it.md#sec-1-12` |  | 8 | s01/01, s01/05, s01/08, s01/13, s01/14, s01/16, s01/index, s02/index, s05/01, s05/04, s05/06, s05/08, s05/11, s05/12, s05/20, s05/index, s06/02, s06/04, s06/06, s06/08, s06/09, s06/11, s06/17, s06/index, s07/01, s07/12, s07/index, s08/01, s08/06, s08/07, s08/09, s08/10, s08/11, s08/14, s08/index, s09/02, s09/05b, s09/09, s09/11, s09/index, s10/05, s10/07, s10/08 |
| Jordan-Wigner transformation | `session07/02b-the-jordan-wigner-transformation.md#sec-7-2b` |  | 1, see the note above the table | s07/01, s07/11, s07/12, s07/index |
| Landau levels | `session04/09-landau-levels-of-schrodinger-electrons.md#eq-4-6` (#sec-4-9) | `s03/06#sec-3-6` | 4 | s02/11b, s02/12, s03/05, s03/06, s03/06b, s03/10, s03/13, s04/01, s04/03, s04/05, s04/06, s04/10, s04/11, s04/13, s04/16, s04/18, s04/19, s04/20, s04/index, s10/07 |
| Bond dimension and MPS | `session07/04-the-matrix-product-state-ansatz.md#sec-7-4` |  | 2 | s07/03, s07/07, s07/08, s07/08b, s07/09, s07/10, s07/11, s07/12, s07/index, s10/03, s10/03b, s10/04, s10/08, s10/index |
| Dirac cone | `session02/11-the-dirac-cone-of-the-honeycomb-lattice-of-graphene-and-flat-band-lattices.md#eq-2-20` (#sec-2-11) |  | 6 | s01/02, s02/08, s02/09, s02/11b, s02/12, s02/index, s03/05, s03/10, s03/10b, s03/11, s03/13, s03/index, s04/10, s04/19, s04/index, s06/15, s08/09 |
| Flat bands | `session02/09-properties-of-an-electronic-dispersion.md#sec-2-10` (#sec-2-11b) |  | 6 | s02/11b, s02/12, s03/06b, s04/03, s04/09, s04/20, s04/index, s05/index, s06/06, s08/11, s08/13 |
| Hubbard model | `session01/14-worked-example-2-magnetism.md#eq-1-7` (#sec-1-14) |  | 7 | s01/12, s05/04, s05/20, s05/index, s06/01, s06/02, s06/04, s06/08, s06/09, s06/11, s06/17, s06/index, s07/04, s07/index, s08/03, s08/07, s09/05, s09/05b, s10/05 |
| Spin waves and magnons | `session06/13-magnons-as-fluctuations-of-the-order-parameter.md#sec-6-13` |  | 8 | s01/03, s01/11b, s01/12, s01/14, s02/08, s02/12, s03/02, s03/12, s03/13, s05/04, s05/13, s06/01, s06/02, s06/15, s06/16, s06/17, s06/index, s07/01, s07/index, s08/01, s08/05, s08/06, s08/07, s08/14, s08/index, s10/04, s10/07, s10/08 |
| Holstein-Primakoff transformation | `session06/13-magnons-as-fluctuations-of-the-order-parameter.md#sec-6-14` |  | 3 | s06/15, s06/17, s06/index, s07/index, s08/07, s08/14, s08/index |
| Nesting | `session09/04b-nesting-and-the-divergence-of-the-lindhard-function.md#sec-9-4b` |  | 3 | s02/09, s03/02, s09/04, s09/05b, s09/06, s09/11 |
| Majorana modes | `session05/15-majorana-bound-states-and-how-to-split-an-electron-into-two-majoranas.md#sec-5-15` |  | 5 | s01/02, s01/03, s03/01, s03/08, s04/20, s05/01, s05/12, s05/14, s05/16, s05/17, s05/18, s05/19, s05/20, s05/index, s09/08 |
| Kitaev chain | `session05/16-the-kitaev-chain-as-the-minimal-model-with-isolated-majoranas.md#eq-5-19` (#sec-5-16) |  | 3 | s03/08, s04/20, s05/17, s05/18, s05/19, s05/20, s05/index |
| Linear response and Kubo formula | `session03/02-linear-response-theory-and-how-a-measurement-reads-the-wavefunctions.md#sec-3-2` |  | 4 | s03/03, s03/13, s03/index, s04/03, s04/index, s09/03, s09/11, s09/index, s10/08, s10/index |
| Lindhard function and susceptibility | `session09/04-the-fermi-sea-and-the-lindhard-function.md#eq-9-4` (#sec-9-4) |  | 3 | s03/02, s05/04, s09/01, s09/02, s09/04b, s09/05b, s09/06, s09/11 |
| Heisenberg model | `session06/09-the-heisenberg-model-on-a-general-lattice.md#eq-6-5` (#sec-6-9) | `s06/08#sec-6-8` | 6 | s01/03, s06/08, s06/13, s06/17, s06/index, s07/01, s07/03, s07/04, s07/10, s07/index, s08/04, s08/05, s08/06, s08/07, s08/11, s09/09, s10/03 |
| Edge states and bulk-boundary correspondence | `session03/07-what-topology-means-for-a-hamiltonian-and-the-bulk-boundary-correspondence.md#sec-3-7` |  | 6 | s01/02, s03/01, s03/06, s03/06b, s03/08, s03/09c, s03/10b, s03/11, s03/11b, s03/12, s03/13, s03/index, s04/03, s04/05, s04/11, s04/19, s04/20, s04/index, s05/12, s05/14, s05/20, s06/16, s06/17, s06/index, s09/08, s09/11 |
| Bloch's theorem and Bloch Hamiltonian | `session02/05-blochs-theorem-and-the-first-band-structure.md#sec-2-5` |  | 7 | s01/16, s02/04, s02/07, s02/08, s02/11, s02/11b, s02/12, s02/index, s03/09c, s03/13, s04/19, s04/index, s05/17, s08/13, s10/07, s10/08 |
| Density of states | `session02/09-properties-of-an-electronic-dispersion.md#eq-2-16` (#sec-2-9) |  | 8 | s01/02, s01/08, s01/13, s02/05, s02/11b, s02/12, s03/02, s03/07, s04/05, s04/09, s05/15, s06/06, s09/04, s09/04b, s09/05b, s09/06, s09/06b, s09/07, s09/10b, s10/07 |
| Charge density wave | `session01/13-worked-example-1-the-charge-density-wave.md#sec-1-13` |  | 6 | s01/12, s01/16, s01/index, s02/09, s02/index, s05/01, s05/04, s05/index, s07/01, s09/04b, s09/05b, s10/08 |
| Spontaneous symmetry breaking | `session01/11-spontaneous-symmetry-breaking-and-why-a-symmetric-hamiltonian-can-have-an-asymmetric-ground-state.md#sec-1-11` |  | 4 | s01/01, s01/11b, s01/16, s01/index, s02/index, s05/index, s06/02 |
| Quantum spin Hall insulator | `session03/11-quantum-spin-hall-insulators.md#sec-3-11` |  | 5 | s01/02, s02/08, s02/09, s03/01, s03/08, s03/11b, s03/12, s03/13, s04/05, s05/18 |
| Topological order | `session10/06-phase-classification-with-local-order-parameters-and-topological-order.md#sec-10-6` |  | 3 | s01/16, s02/index, s10/06b, s10/08 |
| Spinons | `session08/07-why-the-holstein-primakoff-magnon-approach-fails-for-qsl-excitations.md#sec-8-8` (#sec-8-9) | `s08/01#sec-8-2` | 5 | s01/03, s01/04, s03/12, s03/13, s06/01, s06/17, s06/index, s08/01, s08/05, s08/06, s08/09, s08/10, s08/13, s08/14, s08/index, s09/09, s09/index |
| Kondo physics | `session08/11-from-a-single-kondo-impurity-to-the-kondo-lattice.md#sec-8-11` |  | 6 | s01/08, s02/11b, s03/01, s03/03, s06/01, s06/index, s08/01, s08/13, s08/14, s08/index, s09/03, s09/11, s09/index |
| ARPES | `session02/12-measuring-band-structures-with-arpes.md#sec-2-12` |  | 3 | s02/09, s03/index, s10/07 |

## The patterns of the grep

Each pattern is a Python regular expression, searched in the whole Markdown of a page.

- Haldane model, `Haldane (model|coupling|mass|term|phase)`.
- SSH model, `\bSSH\b|Su-Schrieffer-Heeger`.
- Stoner criterion, `Stoner`.
- Nambu spinor and BdG, `Nambu|Bogoliubov-de Gennes|\bBdG\b`.
- Chern number and Berry curvature, `Chern number|Berry curvature`.
- Berry phase and Zak phase, `Berry phase|Zak phase`.
- Mean field, `[Mm]ean[- ]field`.
- Jordan-Wigner transformation, `Jordan-Wigner`.
- Landau levels, `Landau level`.
- Bond dimension and MPS, `bond dimension|matrix product state|\bMPS\b`.
- Dirac cone, `Dirac cone|Dirac point`.
- Flat bands, `[Ff]lat band`.
- Hubbard model, `Hubbard`.
- Spin waves and magnons, `[Ss]pin waves?|[Mm]agnon`.
- Holstein-Primakoff transformation, `Holstein-Primakoff`.
- Nesting, `[Nn]esting`.
- Majorana modes, `Majorana`.
- Kitaev chain, `Kitaev chain`.
- Linear response and Kubo formula, `[Ll]inear response|Kubo`.
- Lindhard function and susceptibility, `Lindhard|susceptibilit`.
- Heisenberg model, `Heisenberg (model|Hamiltonian)`.
- Bloch's theorem and Bloch Hamiltonian, `Bloch's theorem|Bloch Hamiltonian`.
- Edge states and bulk-boundary correspondence, `bulk-boundary|edge states?`.
- Density of states, `density of states`.
- Charge density wave, `charge density wave`.
- Spontaneous symmetry breaking, `[Ss]pontaneous(ly)? (symmetry )?break`.
- Quantum spin Hall insulator, `[Qq]uantum spin Hall`.
- Topological order, `[Tt]opological order`.
- Spinons, `[Ss]pinons?`.
- Kondo physics, `Kondo`.
- ARPES, `ARPES`.
