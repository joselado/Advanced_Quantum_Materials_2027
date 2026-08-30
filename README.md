# Advanced Quantum Materials 2027
Teaching material for the Advanced Quantum Materials course at Aalto University 2027

## Lecture notes
Condensed lecture notes covering the ten topics of the course, in `lecture_notes/tex`
- [Lecture notes (PDF)](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/lecture_notes/tex/main.pdf)

The notes are written in LaTeX, one file per topic in `lecture_notes/tex/sessions`, with the
schematics as standalone TikZ figures in `lecture_notes/tex/figures`. They are built with

```bash
cd lecture_notes/tex && latexmk -pdf main.tex
```

## Interactive exercise sessions
The folder `jupyter-notebooks` contains the Jupyter notebooks for the different sessions of the course
- [Session 1: Second quantization, mean field and spontaneous symmetry breaking](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session1.ipynb)
- [Session 2: Symmetries, band structure theory and effective models](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session2.ipynb)
- [Session 3: Topological band structure theory](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session3.ipynb)
- [Session 4: Electrons in magnetic fields, the quantum Hall effect and Landau levels](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session4.ipynb)
- [Session 5: Superconductivity, Nambu representation and Majorana physics](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session5.ipynb)
- [Session 6: Classical magnetism and magnons](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session6.ipynb)
- [Session 7: Quantum entanglement and tensor networks](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session7.ipynb)
- [Session 8: Quantum magnetism, spinons and Kondo physics](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session8.ipynb)
- [Session 9: Excitations and defects in quantum materials](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session9.ipynb)

Topic 10 (machine learning quantum materials) has no notebook yet.
[`minimal_test.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/minimal_test.ipynb) is a minimal example of the
underlying library, useful to check that the installation works.

## Install
The Jupyter notebooks use [pyqula](https://github.com/joselado/pyqula), and can be installed from a terminal with pip as

```bash
pip install --upgrade pyqula
```

Sessions 7 and 8 use also [dmrgpy](https://github.com/joselado/dmrgpy)

## Tutorial recordings
Recordings of video tutorials explaining the solutions of the exercises of the Jupyter notebooks,
from the previous edition of the course
- [Session 1: Second quantization, mean field and spontaneous symmetry breaking](https://youtu.be/EOhNyXA3rX8)
- [Session 2: Symmetries, band structure theory and effective models](https://youtu.be/W_7ETh7WpGE)
- [Session 3: Topological band structure theory](https://youtu.be/4WkBHhOfWwE)
- [Session 5: Superconductivity, Nambu representation and Majorana physics](https://youtu.be/qZcwsdk6Y3U)
