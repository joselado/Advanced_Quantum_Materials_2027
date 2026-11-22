"""Session 10, what page 08 (Section 10.8, the closing summary) states in its list of tasks and in its two quizzes.

The page quotes no new number. The list of tasks names, for each task, an equation and the section that teaches it,
and this script checks on the Markdown of the pages that each equation is on the page of that section. The display
of the first quiz is (10.1) without its tag, read from the page of Section 10.2. The feedback of the second quiz
says that the variational energy is never below E0, which is checked on the open Heisenberg chain of 8 spins with
random complex states. The Fashion-MNIST accuracies of the list of results have no stored source, so the script checks
only that they are the numbers of the page of Section 10.4. It writes no file."""
import json
import os
import re

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(HERE, '..', '..')
PAGES = os.path.join(WEB, 'pages', 'session10')


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


files = [p['file'] for p in json.load(open(os.path.join(WEB, 'manifest', 'session10.json')))['pages']]
text = {f: open(os.path.join(PAGES, f)).read() for f in files}
where_sec, where_eq = {}, {}
for f, s in text.items():
    for sec in re.findall(r'\{#(sec-10-[\w-]+) number=', s):
        where_sec[sec] = f
    for tag in re.findall(r'\\tag\{(10\.\d+)\}', s):
        where_eq['eq-' + tag.replace('.', '-')] = f
page = text['08-closing-summary.md']

# --- the list of tasks: each named equation is on the page of one of its sections ---------------------------------
start = page.index('After this session we can do the following tasks')
tasks = [line for line in page[start:].split('\n\n')[1].split('\n') if line.startswith('- ')]
check('the list has seven tasks, each with a capital letter and a period', len(tasks) == 7
      and all(t[2].isupper() and t.rstrip().endswith('.') for t in tasks), len(tasks))
for t in tasks:
    secs = re.findall(r'\(#(sec-10-[\w-]+)\)', t)
    eqs = re.findall(r'\(#(eq-10-\d+)\)', t)
    pages = {where_sec.get(s) for s in secs}
    ok = secs and None not in pages and all(where_eq.get(e) in pages for e in eqs)
    check('task "%s"' % t[2:60], ok, 'equations %s on %s' % (', '.join(eqs) or 'none',
                                                             ', '.join(sorted(p for p in pages if p))))
# the task on tomography points to the subsection of tomography, and the one on the memory to the table and the MPS
check('Section 10.3.1 is the subsection on quantum state tomography',
      re.search(r'### Quantum state tomography \{#sec-10-3-1 number="10.3.1"\}', text[where_sec['sec-10-3-1']]) is not None,
      where_sec['sec-10-3-1'])
check('the table (10.2) is on the page of 10.3a and the MPS (10.6) with its bond dimension on the page of 10.4',
      where_eq['eq-10-2'] == where_sec['sec-10-3'] and where_eq['eq-10-6'] == where_sec['sec-10-4'],
      (where_eq['eq-10-2'], where_eq['eq-10-6']))

# --- the first quiz: its display is (10.1) without the tag -----------------------------------------------------------
eq1 = re.search(r'\$\$(\\mathcal\{L\}\(\\theta\) = \\sum_n .*?), \\tag\{10\.1\}\$\$', text[where_sec['sec-10-2']]).group(1)
check('the display of the first quiz is (10.1) of Section 10.2 without its tag', ('$$' + eq1 + '.$$') in page, eq1[:40])

# the right feedback names the phase classifier, whose input on the page of 10.6a is a snapshot of the spins with a
# one-hot label and the loss (10.1)
recall6 = re.search(r'::: \{\.recall eq="10\.1"\}(.*?):::', text[where_sec['sec-10-6']], re.S)
check('the right feedback of the first quiz is the phase classifier, a spin snapshot, a one-hot label and the loss (10.1)',
      'The phase classifier uses a spin array, a label and the squared loss above.' in page and recall6 is not None
      and 'snapshot of the spins' in recall6.group(1) and 'one-hot' in recall6.group(1), where_sec['sec-10-6'])

# --- the list of results: the Fashion-MNIST accuracies are those of the page of 10.4 ------------------------------
# These have no stored source (an open point of the plan, Section VI of arXiv 1801.00315, read in its PDF and not in
# an abstract), so this checks only that the closing page repeats the numbers of Section 10.4, and not the source.
acc8 = re.findall(r'(\d+\.\d+)%', page)
acc4 = re.findall(r'(\d+\.\d+)%', text[where_sec['sec-10-4']])
check('the closing page gives the Fashion-MNIST accuracies of the page of 10.4, training first and test second',
      acc8 == ['95.38', '88.97'] and acc4 == ['95.38', '88.97'] and 'training accuracy' in page, (acc8, acc4))

# --- the second quiz: the variational energy is never below E0 -----------------------------------------------------
SX = np.array([[0, 1], [1, 0]]) / 2
SY = np.array([[0, -1j], [1j, 0]]) / 2
SZ = np.array([[1, 0], [0, -1]]) / 2
L = 8


def site(op, i):
    out = np.array([[1.0]])
    for j in range(L):
        out = np.kron(out, op if j == i else np.eye(2))
    return out


H = sum(site(S, i) @ site(S, i + 1) for i in range(L - 1) for S in (SX, SY, SZ))
E0 = np.linalg.eigvalsh(H)[0]
rng = np.random.default_rng(10)
C = rng.normal(size=(2000, 2 ** L)) + 1j * rng.normal(size=(2000, 2 ** L))
E = np.real(np.einsum('ns,st,nt->n', C.conj(), H, C) / np.einsum('ns,ns->n', C.conj(), C))
check('the variational energy of 2000 random complex states of the open Heisenberg chain of 8 spins is above E0',
      abs(E0 + 3.374933) < 1e-6 and E.min() > E0, 'E0 = %.6f, the lowest E[theta] %.3f' % (E0, E.min()))
# corrected on 2026-11-22, the first feedback of the first quiz: the two classifiers have the same squared loss (10.1)
# and a one-hot label, as pages 01 and 06 say, and differ in the input and the meaning of the label
p01 = text['01-machine-learning-and-many-body-physics-in-two-directions.md']
p06 = text['06-phase-classification-with-local-order-parameters-and-topological-order.md']
check('the cat-and-dog classifier minimizes (10.1) with a one-hot label, and the phase classifier has a one-hot label',
      'by minimizing [(10.1)](#eq-10-1), with $f_\\theta$ the output of the network and $y_n$ the one-hot label' in p01
      and 'the label $y_n$ is a one-hot vector for ordered or disordered' in p06, 'pages 01 and 06')
# corrected on 2026-11-22, the tomography sentence: far fewer parameters than 2^L, 1680 for an RBM with M = L = 40
check('an RBM with 40 visible and 40 hidden spins has 1680 parameters, far fewer than 2^40', 40 + 40 + 1600 == 1680
      and 1680 < 2.0 ** 40 / 1e8, 1680)
print('all checks of page 08 hold')
