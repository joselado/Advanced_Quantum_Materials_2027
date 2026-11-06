# Web notes toolkit

This toolkit builds the lecture notes as web pages in `docs/notes/`. The plan is
`lecture_notes/WEB_NOTES_PLAN.md` and the tracker is `lecture_notes/WEB_NOTES_PROGRESS.md`. It needs
pandoc 3, python3 and `pdftocairo`. The math check also needs node, as we will now see.

## How to run it

To rebuild the pages we run one command, and the checks run at its end.

```
python3 webnotes/build.py
```

The keyword `--session N` builds only the pages of one session, `--check-only` runs the checks on the
existing `docs/notes/`, and `--serve` serves `docs/` on `localhost:8000` after the build. The build is
idempotent, so a second run changes nothing in `docs/`.

## The math check

The pages render the math in the browser with MathJax 3.2.2. The math check renders every fragment of
`docs/notes/` with the same version and the same TeX configuration, in node, and lists each fragment that
gives an error, with its page and its text. It needs node and one local package, installed once with the
command below. The packages stay in `webnotes/mathcheck/node_modules/`, which git ignores.

```
cd webnotes/mathcheck && npm install
```

After a build we run it with the command below, which is the same as `node webnotes/mathcheck/check.js`
plus the other checks. Without node or without the package, `build.py` skips the math check and says so.

```
python3 webnotes/build.py --check-only --math
```

The check does not load the `noundefined` package of the page, so an unknown macro is an error here, while
on the page it would show in red. A macro that is missing is fixed in `MATHJAX` of `template.py`, and a
mistake in the TeX of a fragment is fixed in the Markdown of the page. KaTeX is not checked, since the pages
use only MathJax.

## Converting a session

The conversion of a session from the LaTeX is done once, with the command below. It writes the Markdown of
the session in `pages/sessionNN/`, its frozen list of pages in `manifest/sessionNN.json` and its line in
`SYNC`. It refuses to overwrite a converted session, since from then on the Markdown is the master. The
keyword `--force` regenerates it and loses the web edits.

```
python3 webnotes/convert.py --session N
```

After a conversion or a change of the video pages that links the notes, we also run
`python3 docs/build_site.py`, which adds the link "Notes of this session" to the video pages of every
session that has a manifest.

## What is in the Markdown

The pages are plain pandoc Markdown, so any editor reads them. The numbers are written in the file, so
they do not move when the file is edited.

- A heading carries `{#sec-2-5 number="2.5"}`. The build writes the number before the title.
- A numbered display equation ends with `\tag{2.8}`. The build derives the anchor `eq-2-8` from the tag.
  A new equation takes the number before it with a letter, `\tag{2.8a}`, and a removed one leaves a gap.
- A figure is `![caption](figures/s02f02_cosband.svg){#fig:s02:cosband number="2.2"}`. The build adds
  "Figure 2.2." to the caption and converts `lecture_notes/src/figures/pdf/s02f02_cosband.pdf` by its date.
- A reference is a link to an anchor, `[(2.8)](#eq-2-8)`, `Section [2.11](#sec-2-11)`. The build points it
  to the page that holds the anchor, also in another session. If the session of the anchor is not built yet,
  the text stays without the link and `check.py` lists it as pending.
- The boxes `notebookbox`, `quiz`, `tryit` and `widget` are fenced divs. Only the notebook box is used
  today. The other three are the hooks for the later phases, and `widgets/notes.js` is where they will
  become interactive.

## Files

- `convert.py`, `filters/tex2md.lua`, the one-time conversion from the LaTeX.
- `build.py`, `filters/web.lua`, `template.py`, the build. The look is imported from `docs/build_site.py`.
- `check.py`, the checks of `docs/notes/`, which are missing files and anchors, missing images, "??", LaTeX
  left outside the math, equation numbers used twice and pages without a source in the manifest.
- `labels.json`, the map from anchor to page, written by the first pass of the build.
- `pages/`, `manifest/`, `SYNC`, the Markdown master, the frozen URLs and the commit of the `.tex` each
  session was last synced to.
- `mathcheck/check.js`, `mathcheck/package.json`, the math check above.
- `widgets/notes.js`, the shared script of the pages, copied to `docs/notes/notes.js`.
