# Gates of the lint and the sources of the lab boxes

The lint lists what a script can see on a page, so that a reviewer spends the reading on the physics. We will now
see the five categories added to `lint.py`. Three check the shape of a page, and two check the boxes "In the lab".
We also see `labsource.py`, which stores the abstract of every article that a lab box links, and what of it git keeps. Session 3 is the
model of the shape, and it gives no hit of the shape.

```
python3 webnotes/lint.py --session 4 --category opener --category key --category long-paragraph
python3 webnotes/lint.py --session 3 --category lab-source --category lab-number
```

## The shape of a page

These three categories check the section pages. The index page of a session is its introduction, so it is not
checked. The rules are those of "The shape of a page" in `lecture_notes/WEB_NOTES_PLAN.md`.

- `opener`, a page whose first three sentences of prose under its first heading hold no question. The blocks in
  between, such as a `recall` box, are skipped. The closing summary of a session is not checked. To fix a hit we
  write the question of the page first. One or two sentences after it say where we arrive, as in Section 3.5.
- `key`, a page that has a numbered equation, a `\tag{`, and no `::: key` box. A page of motivation has no
  numbered equation, so it is never reported. To fix a hit we put the main result of the page in a key box. The box
  keeps the `\tag` and adds one or two sentences on what the result means. When the numbered equation is only a
  step, the box holds the result that the step leads to.
- `long-paragraph`, a paragraph of more than 150 words outside the blocks. Each math fragment counts as one word,
  as in `long-sentence`. A display equation inside the paragraph also counts as one word. A list item is counted
  alone, and a figure with its caption is not a paragraph. To fix a hit we split the paragraph where its idea
  changes, or we move a derivation into a `steps` fold.

The index pages of six sessions have a paragraph over 150 words, and the lint does not report them. In Session 3
it is the plan of the session, in line 5 of `index.md`, with 163 words.

## The numbers of a lab box

A lab box ties the result of a page to one material. The number of that material has to come from the article,
and not from memory. The lint reads every `::: lab` box and compares its numbers with the stored abstract of its
links.

A number of a real material is a number followed by a unit. The units are K, mK, meV, eV, T, nm, GHz, kΩ, the
percent sign and a few more. A number with an error bar, such as `0.97(2)` or `0.9998\pm0.0006`, is also one. The
comparison does not see spaces, thin spaces, `~`, `\approx` or `\sim`. So `$27$ K` in the page matches `27~K` in
the abstract, and `$0.1\%$` matches `.1\%`. The words kelvin, percent and electron volt become their symbols, and
`+-` becomes `\pm`.

Three kinds of number need no source. The first is exact, the resistances $h/e^2=25.8$ kΩ and $h/2e^2=12.9$ kΩ,
and the conductance $e^2/h$ written as a symbol. Another plateau, such as $8.6$ kΩ, is marked as ours, so that the
rounding never lets a measured resistance through. The second is in the figures and schematics inside the box. They
show the model of the page, and their caption says so, so the lint does not read them. The third is a number that
is our own conversion. The author lists it on the box with the attribute `ours`, with a comma between two numbers.

```
::: {.lab ours="2.3 meV"}
... The gap that transport gives is about $27$ K, which is $2.3$ meV. The measurement is in
[this article](https://www.science.org/doi/10.1126/science.aay5533).
:::
```

Pandoc reads this box as a div of class `lab` with the attribute `ours`. The filter `filters/web.lua` renders it as
any other lab box, and the attribute does not reach the page. The two categories are the following.

- `lab-source`, a hit in four cases. The first is an external link of the box that is not in `sources/index.json`.
  We store it with `labsource.py`, as below. The second is a number that is not in the stored text of the sources
  of the box. We read the abstract again and write the number that it gives. When the number is our conversion, we
  mark it as ours. The third is a value that the source gives with another unit, with none or with another error
  bar. As an example, the arXiv abstract of the gap of graphene on SiC writes "a gap of ~ 0.26" with no eV. We then
  read the published abstract on the page of the journal. We attach it with `--paste`, as in the section "A text
  read by hand". The fourth is a box with no external link, which is also an error of the build.
- `lab-number`, a warning for a box with no number of a real material. The locked rule asks for one number with
  its unit. So the box gets one from the abstract, or the page keeps the box without a number for a good reason.

To see every number of the lab boxes of a session, we run the check of `labsource.py`. It prints each number with
the sentence of the abstract where it was found. A physics checker reads this list instead of fetching the
articles again.

```
python3 webnotes/labsource.py --check 3
```

## Storing a source

The script fetches the abstract of one article and stores it as plain text, without the markup of JATS and TeX.
It takes the URL as written in the page, so that the lint finds it, or a bare id. An arXiv id or URL is read from
the arXiv API. A DOI, or a publisher URL that holds a DOI, is read from Crossref. The link
`https://www.nature.com/articles/nmat2003` holds the DOI `10.1038/nmat2003`, and the script knows it. The fetch
uses `curl` with a timeout and a generic client name, and it sends nothing but the id.

For Nature and Science, Crossref often has no abstract of the authors. For Science it has an editor summary, which
the journal writes and which often has no number. The script then says so, and it stores the title and the
summary. With `--also` it attaches the arXiv abstract of the same article. It also checks that the arXiv record
names the same DOI. As a reference, this is the article of the lab box of Section 3.5.

```
python3 webnotes/labsource.py --session 3 https://www.science.org/doi/10.1126/science.aay5533
```
```
stored https://www.science.org/doi/10.1126/science.aay5533
    in sources/session03/serlin2020_science.aay5533.txt
Crossref has only an editor summary for 10.1126/science.aay5533, so the file holds the title and the journal and that summary. Pass --also ARXIV_ID to attach the arXiv abstract, or --paste FILE to attach the published abstract read by hand.
numbers with a unit or an error bar in it: none
```

The summary has none of the numbers of the box, so we fetch it again with the arXiv id of the same article.

```
python3 webnotes/labsource.py --session 3 https://www.science.org/doi/10.1126/science.aay5533 --also 1907.00261 --force
```
```
arXiv 1907.00261 names the DOI 10.1126/science.aay5533, which is the same article
stored https://www.science.org/doi/10.1126/science.aay5533
    in sources/session03/serlin2020_science.aay5533.txt
numbers with a unit or an error bar in it: .1%, 27 K, 9 K, 1 nA
```

The last line lists the numbers that the lint can find in this source. So the author sees at once which numbers a
box may quote. The keyword `--force` fetches a stored URL again, and `--name` sets the name of the file.

## A text read by hand

Sometimes neither Crossref nor arXiv has the number of the page. The arXiv abstract of the gap of graphene on SiC
writes the gap without its unit. The abstract on the page of Nature Materials has "≈0.26 eV". We then copy
the published abstract into a plain text file, and we attach it to the stored article with `--paste`. The keyword
`--origin` gives the address where the text was read, and by default it is the URL of the page. The block gets
this address and the date of the reading. An article that is not stored yet is fetched first.

```
python3 webnotes/labsource.py --session 3 https://www.nature.com/articles/nmat2003 --paste abstract.txt
```
```
attached the text of abstract.txt, read at https://www.nature.com/articles/nmat2003 on 2026-11-21
    to sources/session03/zhou2007_nmat2003.txt
numbers with a unit or an error bar in it: 0.26 eV
  quoted in the tracked file: "a gap of ≈0.26 eV is produced."
```

A text read by hand is the weakest source, since nobody can fetch it again by script. So we paste only a text that
the page of the journal shows to every reader, such as its abstract. A text from behind a paywall is not pasted.

## What git keeps

The repository is public, so it keeps of a publisher text only what backs the numbers of the pages. Each article is
written twice. The full copy in `sources/.full/sessionNN/NAME.txt` holds every text whole, and git ignores it. The
tracked file `sources/sessionNN/NAME.txt` holds the URL of the page, the DOI or the arXiv id, the date of the
fetch and the title. Then it holds one block per source, and the first line of a block says what the text is and
where it came from. An arXiv abstract is kept whole. A text written by a publisher or a journal is replaced by
short quotations, one clause for each number that a page quotes from it. This is the tracked file of the article
of the gap of graphene on SiC, with the arXiv abstract shortened here.

```
url: https://www.nature.com/articles/nmat2003
doi: 10.1038/nmat2003
fetched: 2026-11-21
title: Substrate-induced bandgap opening in epitaxial graphene

[no abstract, from https://api.crossref.org/works/10.1038/nmat2003]
Crossref holds the title and the journal only.

[abstract, from https://export.arxiv.org/api/query?id_list=0709.1706]
arxiv: 0709.1706
title: Substrate-induced band gap opening in epitaxial graphene
Graphene has shown great application potentials ... a gap of ~ 0.26 is produced. ...

[text pasted by hand, from https://www.nature.com/articles/nmat2003, read 2026-11-21, quotations]
"a gap of ≈0.26 eV is produced."
```

The lint reads only the tracked files, so it gives the same result on a fresh clone as on the machine that fetched
the sources. The quotations are chosen from the numbers that the pages quote at the moment of the fetch. When a lab
box gets a new number later, we write the quotations again from the full copies.

```
python3 webnotes/labsource.py --quotes
```

On a machine with no full copy, such as a fresh clone, `--quotes` keeps the quotations as they are and says so.
Then we fetch the article again with `--force`, which writes a new full copy. A text pasted by hand is kept by a new
fetch, but on a fresh clone only its quotations remain. The command `--check` shows the whole sentence from the
full copy when there is one. It also says when the full copy has a number that the quotations miss.

The file `sources/index.json` maps each URL written in a page to its file. A URL that two pages write is stored
once. The lint also matches another spelling of the same article, such as `arxiv.org/pdf/ID` for
`arxiv.org/abs/ID`.

## When the script stops

The script stops with a message, and stores nothing, in four cases. The network gives nothing, Crossref answers
404, arXiv has no entry, or the URL holds no DOI and no arXiv id. In the last case we pass the DOI of the article,
and the URL of the page with `--url`. In this way the index has the URL that the lint reads in the page.

```
python3 webnotes/labsource.py --session 4 10.1016/DOI_OF_THE_ARTICLE --url https://www.sciencedirect.com/science/article/pii/ID
```
