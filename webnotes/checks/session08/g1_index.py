"""Session 8, the numbers of the index page, which are the counts of the caption and of the alt text of the concept
map: six grey boxes from before, five blue boxes of this session, four red boxes of later sessions, and "mean field
feeds two sections", the spinons and the Kondo lattice.

The lists are read from webnotes/figures/session08/concept_map.py with ast, so the figure is not drawn and no file
is written. It needs only the standard library."""
import ast, os

WEBNOTES = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


src = open(os.path.join(WEBNOTES, 'figures', 'session08', 'concept_map.py')).read()
data = {}
for node in ast.parse(src).body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
        try:
            data[node.targets[0].id] = ast.literal_eval(node.value)
        except ValueError:
            pass
before, now, after, edges = data['before'], data['now'], data['after'], data['edges']
check('alt text, six grey boxes from before', len(before) == 6, len(before))
check('alt text, five blue boxes of this session', len(now) == 5, len(now))
check('alt text, four red boxes of later sessions', len(after) == 4, len(after))
mf = [i for i, n in enumerate(before) if n[0] == 'mean field']
targets = sorted(now[b[1]][0] for a, b in edges if a == (0, mf[0]))
check('caption, mean field feeds two sections, the spinons and the Kondo lattice',
      len(mf) == 1 and targets == ['Kondo lattice', 'spinons'], targets)
page = open(os.path.join(WEBNOTES, 'pages', 'session08', 'index.md')).read()
check('the caption and the alt on the page say these counts',
      'Mean field feeds two sections' in page and 'six grey boxes' in page and 'five blue boxes' in page
      and 'four red boxes' in page, 'ok')
