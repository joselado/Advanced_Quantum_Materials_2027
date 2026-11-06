# Widgets

A widget is a small interactive calculation inside a page of the notes. The student moves one slider, and the plots and
one sentence of text follow. Ten of them exist, one per session, each tied to one section.

## What the student sees

The page shows the introduction written in the Markdown, the sliders, the plots and a readout sentence. The curves
come from a JSON computed in advance on the grid of the slider, so that they appear at once, also without network.
The button "Run live in the browser" loads Pyodide (Python in WebAssembly) from the jsDelivr CDN, installs what the
widget needs and runs the same code for any value of the slider. The Python code is shown under "Show the Python
code". Pyodide is loaded only when the button is pressed, so a page with a widget costs only `notes.js` and one JSON,
which is fetched when the widget is about to come into view.

## The block in the Markdown

```
::: {.widget name="chainband"}
Move the second-neighbor hopping $t_2$ of [(2.9)](#eq-2-9). For small $t_2$ the band keeps one minimum ...
:::
```

The text is the introduction, with the usual math and links. The ten blocks of the course are in `blocks/ID.md`, ready
to be pasted at the end of the section that is named in the table below.

| id | section | what it shows | packages |
|---|---|---|---|
| `island` | 1.10 | eigenstates of a finite chain against N, with PyQula | numpy, scipy, matplotlib, PyQula |
| `chainband` | 2.5 | band of the chain with second-neighbor hopping t2 | numpy |
| `sshwinding` | 3.9 | winding of d(k) and the levels of the open SSH chain | numpy |
| `landaufan` | 4.11 | lowest Landau bands of the lattice against the flux 1/q | numpy |
| `kitaevbdg` | 5.17 | BdG levels and zero-mode weight of the open Kitaev chain against mu | numpy |
| `stoner` | 6.6 | gap equation and magnetization against U | numpy |
| `dimerentropy` | 7.6 | entanglement entropy of 12 dimerized spins against J2 | numpy, scipy |
| `kondobands` | 8.13 | hybridized bands and gap against gamma_K | numpy |
| `friedel` | 9.6 | density around an impurity against the filling | numpy |
| `netfit` | 10.2 | one-hidden-layer network fitting sin(3 pi x) against H | numpy |

## Files

- `defs/ID.py`, the widget. It has `META`, a dictionary with the title, the sliders and the packages, and
  `compute(p)`, which takes the slider values as a dictionary and returns the plots. The same file runs on the machine
  and in Pyodide, so every import is inside `compute`.
- `data/ID.json`, written by `python3 webnotes/widgets/precompute.py [ID ...]`. It holds `META` with the hash of
  `defs/ID.py`, and the result of `compute` for every value on the grid of the sliders. `build.py` stops with an error
  when the hash does not match, so a changed def needs a new precompute.
- `blocks/ID.md`, the Markdown block of the widget.
- `notes.js`, the sliders, the plots and the Pyodide loader. `notes.css`, the look.

`build.py` copies `defs/ID.py` and `data/ID.json` of every widget a page uses to `docs/notes/widgets/`.

## META and the result of compute

```python
META = dict(id="chainband", title="...",
            params=[dict(name="t2", label="second-neighbor hopping t2", min=0.0, max=1.0, step=0.05, value=0.3, fmt=2)],
            packages=["numpy"],      # Pyodide packages, any of numpy, scipy, matplotlib
            pyqula=False)            # True installs PyQula from PyPI, pinned in notes.js
```

`compute` returns `dict(panels=[...], text="...")` with one or two panels. A panel has `title`, `xlabel`, `ylabel`,
optional `xlim`, `ylim`, `xticks` (a list of `[value, label]`), `equal` for the same scale on both axes, `series` and
`marks`. A series is `dict(x=..., y=..., kind=..., color=0 to 4, label=...)` with `kind` one of `line`, `dash`, `points`,
`both`. A mark is `dict(x=..., y=...)`, drawn as a ring. Arrays can be numpy arrays, `precompute.py` and the Pyodide
glue convert them and keep five significant digits. The words `phi`, `psi`, `mu`, `pi`, `omega`, `gamma`, `hbar`, `+-`
and `^2` in labels and in the text are written as the Greek letters and the symbols by `notes.js`.

The grid has one JSON entry per value of the sliders, so a widget with two sliders needs the product of their values.
Keep the grid small, the JSON of a widget is between 10 and 180 kB.

## How the live part works

`notes.js` loads `pyodide.js` from `https://cdn.jsdelivr.net/pyodide/v0.27.7/full/` (the version is pinned), loads
numpy and the packages of `META`, and for a widget with `pyqula=True` it also does the following.

- It puts two stand-in modules in place of `numba` and `jax`, which PyQula imports and Pyodide does not have. They only
  make `jit` do nothing, which is enough for the band structures and the finite systems of the widgets.
- It installs `dill`, `threadpoolctl`, `multiprocess` and `pyqula==0.0.96` with `micropip`, without the dependencies.

Then it fetches `widgets/ID.py`, runs it once and calls `compute` at each move of the slider. If anything fails,
the status line says so and the precomputed curves stay. Offline, the widget works from the JSON alone.

## A new widget

1. Write `defs/ID.py` and test `compute` for a few values on the machine.
2. Run `python3 webnotes/widgets/precompute.py ID`.
3. Write `blocks/ID.md` and paste it at the end of the section.
4. Build privately, `python3 webnotes/build.py --out DIR`, and look at the widget in a browser, with the button too.

Physics to check against the section. The numbers in the readout come from the same arrays as the plots, never typed.
