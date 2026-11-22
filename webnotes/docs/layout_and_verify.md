# The layout check, plots without axes, and the kept checks

This page describes three tools that need no image. The layout check measures the built pages in the browser, the
build warns about a plot without axes, and `build.py --verify` runs the check scripts that we keep. As a result an
agent can check a session in less than a minute, and it reads a list of lines instead of screenshots.

## The layout check

The layout check loads each page of a private build in headless Chrome, at the width of a laptop and of a phone. It
opens every fold, clicks the first option of every quiz so that one feedback is open, and measures the boxes in the
browser. It prints one line per finding, then a count.

```
python3 webnotes/build.py --out /tmp/mynotes --session 3
python3 webnotes/layout.py /tmp/mynotes --session 3              # every page, at 1000 px and 390 px
python3 webnotes/layout.py /tmp/mynotes --session 3 --page 05-the-berry-curvature-and-why-the-hall-conductivity-is-an-integer.md
```

A session of 17 pages takes about 25 s, one page about 3 s, and the 136 pages of the ten sessions about 2.5 minutes
with `--jobs 6`. The keyword `--width` takes other widths, `--jobs`
sets how many Chrome runs go at the same time, and `-v` also prints what was opened and counted on each page.
Without `--session` every session of the build is checked. The redirect stubs are skipped. The exit code is 1 when
there is a finding or a page that could not be measured, and 0 otherwise.

The pages load MathJax from the CDN, so the check needs the network. Chrome does not make a window narrower than
500 px, so the page is loaded in an iframe of the width we ask for, and the check reads the width back from the
browser. When the width is another one, or MathJax did not load, the line says "not measured" instead of passing.

### What a finding means

Each line names the page, the width, the section where the element sits, and the number of pixels. The kinds of
lines are listed below.

- `the page is wider than the window`. The document scrolls sideways at that width. The lines after it name the
  elements that cause it.
- `sticks out of the window`. The element goes past the edge of the window and no block scrolls it. This is what a
  fixed width, a long formula in the text, a wide table or a long line of code gives on a phone. A formula near the
  end of a line can also move the page through the MathML that MathJax hides for screen readers, and the line then
  says so.
- `is cut by`. The element is wider than a box that hides its overflow, as a quiz does, so a part of it is not shown.
  The page does not scroll, which is why a screenshot misses it easily.
- `sticks out of its box`. The element fits the window, but it goes past the border of the box that holds it, for
  instance an image wider than its figure or a picture wider than its quiz option.
- `overlap`. Two elements of a quiz that sit side by side in the page are drawn on top of each other.
- `did not load`. The image is missing in the build, or its path is wrong.
- `not measured`. Chrome gave no report, MathJax did not load, or the window had another width. The page is
  measured again once the cause is gone.

The elements that are measured are the figures and their images, the quiz options and their pictures, the boxes
(`keybox`, `recall`, `lab`, `problem`, the folds, `comesback`, `tryit` and `quiz`), the tables, the code and the
math. A display equation that is wider than the page scrolls inside its own block, which is the intended behaviour,
so it is not a finding. The same holds for anything inside a block that scrolls, such as a table in `div.center`.
The text inside the SVG of a picture is not measured, so the size of its labels at 390 px is still read by eye.

### How it works

For each page and width the check writes a copy of the page in a new folder next to it. The copy has a `<base>` to
the folder of the page, so that every relative link works, and it loads its images at once instead of lazily. One
script is added at its end. It waits for MathJax and the images, opens the folds, clicks the quizzes, measures, and
sends a JSON report to a small wrapper page that holds the iframe. Chrome prints the wrapper with `--dump-dom`, and
the check reads the report from it. The copies are removed at the end, file by file.

To see that the check finds a defect, we give an image of a copy of a page a fixed width of 900 px and run the check
on that copy with `--page`. At 390 px the image sticks out of the window and the page scrolls, and at 1000 px the
image only sticks out of its figure, so the two widths test two different lines.

## A plot without axes

Every plot has its axes, as the rule of `lecture_notes/WEB_NOTES_PLAN.md` says in "Figures and captions". The function
`style.save` looks at each axes of a figure before it writes the SVG. An axes that holds data, meaning lines,
collections, images or bars, gets a warning when its axis is on and it names no quantity. A name is an xlabel, a
ylabel, or a label of `style.arrows(ax, xlabel=..., ylabel=...)`. A map, a `pcolormesh` or an image, also gets a
warning when its axis is switched off. The warning is a line that starts with `AXES-WARNING` and names the script,
and the build lists it among its warnings.

```
WARNING AXES-WARNING session03/NAME.py: axes 1 of 1 is a map (QuadMesh) with its axis switched off
WARNING AXES-WARNING session03/NAME.py: axes 2 of 2 (3 lines) has no axis names, neither xlabel nor ylabel nor style.arrows(xlabel=..., ylabel=...)
```

A drawing that is not a plot, such as a lattice sketch or a concept map, says so with `sketch=True`, and it gets no
warning.

```python
style.save(fig, __file__, sketch=True)          # a lattice sketch, not a plot
```

The check only reads the figure, so the SVG is the same with and without it. A warning appears when the script runs,
meaning when its SVG is stale or with `--redraw`. A name written by hand with `style.label` at the tip of an arrow is
not seen, so such a plot gets a warning, and the fix is to pass the name to `style.arrows`. Colorbars are not
checked, and the tags (a) and (b) under a panel are not names. A script that writes its SVG without `style.save` is
not checked at all. An axes with curves and its axis switched off gets no warning, since most sketches are drawn in
this way, so a curve plot drawn like a sketch still passes and is found only by reading the script.

## The kept checks

A physics check that is worth keeping is a script in `webnotes/checks/`, for a session in `checks/sessionNN/`. The
option `--verify` runs them all, builds nothing, and stops, as `--freeze` does.

```
python3 webnotes/build.py --verify                  # every script under checks/
python3 webnotes/build.py --verify --session 3      # checks/session03/ and the scripts directly in checks/
```

Each script runs in a temporary working folder of its own, so the files that it writes stay out of the tree, and with
a time limit of 40 minutes (`VERIFY_TIMEOUT` in `build.py`, raised from 15 on 2026-11-22, when about twenty agents on the machine made a check of 3 minutes take 15). A script passes when it exits with code 0, so a check
ends with an assertion or with `sys.exit(1)` when a number is wrong. A file of test functions calls them under
`if __name__ == '__main__'`, since nothing else runs them. A file `_NAME.py` is a helper that the checks import, and
it is not run on its own. The output is one line per script with the last line of its error, then a count, and the
exit code is 1 when one check failed.

```
OK     passes.py (0 s)
FAILED session03/fails.py (0 s): AssertionError: the gap is 0.5, expected 0.6
verify: 2 scripts, 1 OK, 1 FAILED
```
