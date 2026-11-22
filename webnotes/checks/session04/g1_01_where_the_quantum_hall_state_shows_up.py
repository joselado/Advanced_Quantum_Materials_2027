"""Session 4, the numbers that page 01 (Sections 4.1 and 4.2) quotes, in the caption of g1_energy_scales, the two
quizzes and the problem. The figure script webnotes/figures/session04/g1_energy_scales.py asserts the numbers of its
caption too, and they are repeated here so that build.py --verify sees them.

The lab box quotes 3.5 T, 10 K and 1e-9 from the stored abstract of arXiv:1504.06511. labsource.py --check 4 shows
the first two and does not read 1x10^-9, so this script finds the three in one sentence of the stored file.

The old bullets of Section 4.1 hold sentences that the plan of the session leaves to the lecturer (open points 3 and
4). This script does not confirm them. It asserts the numbers that bear on them, so that the lecturer sees them:
hbar omega_c of GaAs is 1 meV at 0.58 T, for "roughly one millielectronvolt", and k_B times 1 K is 1/20 of it at 1 T,
for "of the order of one kelvin". The ratio of graphene to GaAs is 10 at 4.4 T, for "roughly one order of
magnitude", and E_1 is 115 meV at 10 T, for "around 100 millielectronvolts". "Almost room temperature" is checked
against the stored abstract of doi 10.1126/science.1137201, which says room temperature. "Up to about 100 K" has no
stored source, so only k_B times 100 K against E_1 is printed.

The plateau at 2 e^2/h of the feedback of the second quiz is computed with pyqula for the spinful honeycomb lattice
with the Fermi energy above its zero level and for the spinful square lattice with its lowest level filled, which are
graphene and a parabolic gas with the spin degenerate. pyqula writes files when it computes a Chern number, so that
part runs in a temporary folder that the script removes.

Every value comes from two routes, the SI constants and the conversion of the conventions sheet
(1.73 meV per tesla for GaAs, 36.3 meV for sqrt(B/T) in graphene). It needs numpy and pyqula, and writes no file in
the repository."""
import json, os, re, tempfile
import numpy as np

WEBNOTES = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

HBAR, E, ME, H, KB = 1.054571817e-34, 1.602176634e-19, 9.1093837015e-31, 6.62607015e-34, 1.380649e-23
MSTAR, V = 0.067 * ME, 1e6


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def gaas(B):
    """hbar omega_c = hbar e B / m* of GaAs, in meV, B in T."""
    return HBAR * E * B / MSTAR / E * 1e3


def graphene(B):
    """E_1 = v sqrt(2 hbar e B) of graphene, in meV, B in T."""
    return V * np.sqrt(2 * HBAR * E * B) / E * 1e3


# second route: hbar omega_c = (hbar e / m_e) B / 0.067, with hbar e / m_e = 2 mu_B = 0.1158 meV per tesla
mu_b = 5.7883818060e-2                                   # meV per tesla
check('GaAs, two routes', abs(gaas(1) - 2 * mu_b / 0.067) < 1e-6, round(gaas(1), 4))
# second route for graphene: E_1 = hbar v / l_B * sqrt 2, with l_B = sqrt(hbar / e B) = 25.66 nm at 1 T
lB1 = np.sqrt(HBAR / E)
check('graphene, two routes', abs(graphene(1) - np.sqrt(2) * HBAR * V / lB1 / E * 1e3) < 1e-6 and abs(lB1 * 1e9 - 25.66) < 0.01,
      round(graphene(1), 3))

# the caption of g1_energy_scales
check('caption, GaAs 1.73 meV at 1 T and 17.3 meV at 10 T', abs(gaas(1) - 1.73) < 0.005 and abs(gaas(10) - 17.3) < 0.05,
      (round(gaas(1), 3), round(gaas(10), 2)))
check('caption, graphene 36.3 meV at 1 T and 115 meV at 10 T', abs(graphene(1) - 36.3) < 0.05 and abs(graphene(10) - 115) < 0.5,
      (round(graphene(1), 2), round(graphene(10), 2)))
r1, r10 = graphene(1) / gaas(1), graphene(10) / gaas(10)
check('caption, the ratio 21 at 1 T and 6.6 at 10 T, falling as 1/sqrt(B)',
      round(r1) == 21 and round(r10, 1) == 6.6 and np.isclose(r1 / r10, np.sqrt(10)), (round(r1, 2), round(r10, 2)))

# the first quiz: a field four times larger
check('quiz 1, GaAs 1.7 meV at 1 T and 6.9 meV at 4 T, a factor 4', round(gaas(1), 1) == 1.7 and round(gaas(4), 1) == 6.9
      and np.isclose(gaas(4) / gaas(1), 4), (round(gaas(1), 2), round(gaas(4), 2)))
check('quiz 1, graphene 36 meV at 1 T and 73 meV at 4 T, a factor 2', round(graphene(1)) == 36 and round(graphene(4)) == 73
      and np.isclose(graphene(4) / graphene(1), 2), (round(graphene(1), 1), round(graphene(4), 1)))

# the second quiz: 17 meV against 115 meV at 10 T, roughly seven times
check('quiz 2, 17 and 115 meV at 10 T, roughly seven times', round(gaas(10)) == 17 and round(graphene(10)) == 115
      and 6.5 < r10 < 7.5, (round(gaas(10), 2), round(graphene(10), 2), round(r10, 2)))

# the problem, step by step with the rounded constants of the solution
num = 1.055e-34 * 1.602e-19 * 10 / (0.067 * 9.109e-31)
check('problem, hbar omega_c = 2.77e-21 J = 17.3 meV', abs(num - 2.77e-21) < 0.005e-21 and round(num / E * 1e3, 1) == 17.3,
      num)
kb_ev = KB / E
check('problem, k_B = 8.617e-5 eV/K and 17.3 meV is 201 K', abs(kb_ev - 8.617e-5) < 5e-9 and round(gaas(10) * 1e-3 / kb_ev) == 201,
      round(gaas(10) * 1e-3 / kb_ev, 2))
root = np.sqrt(2 * 1.055e-34 * 1.602e-19 * 10)
check('problem, sqrt(2 hbar e B) = 1.84e-26 kg m/s and E_1 = 1.84e-20 J = 115 meV, from the printed constants and the exact ones',
      round(root * 1e26, 2) == 1.84 and round(1.84e-20 / 1.602e-19 * 1e3) == 115 and round(V * root / E * 1e3) == 115
      and round(graphene(10)) == 115, (root, round(graphene(10), 2)))
kelvin = [115e-3 / 8.617e-5, 1.84e-20 / KB, graphene(10) * 1e-3 / kb_ev]
check('problem, 115 meV is about 1330 K by every route, within 5 K', all(abs(x - 1330) < 5 for x in kelvin), np.round(kelvin, 1))
check('problem, 17.3 meV is 201 K by the printed numbers and the exact one',
      round(17.3e-3 / 8.617e-5) == 201 and round(2.77e-21 / KB) == 201 and round(gaas(10) * 1e-3 / kb_ev) == 201
      and round(2.77e-21 / 1.602e-19 * 1e3, 1) == 17.3, (round(17.3e-3 / 8.617e-5, 2), round(2.77e-21 / KB, 2)))
check('problem, the ratio 115/17.3 = 6.6 at 10 T', round(115 / 17.3, 1) == 6.6 and round(r10, 1) == 6.6, round(115 / 17.3, 3))


# ---------------------------------------------------------------- the lab box, from the stored abstract
def stored(url):
    with open(os.path.join(WEBNOTES, 'sources', 'index.json')) as f:
        name = json.load(f)[url]
    with open(os.path.join(WEBNOTES, 'sources', name)) as f:
        return f.read()


text = stored('https://arxiv.org/abs/1504.06511')
sentence = [s for s in re.split(r'(?<=\.)\s+', text) if '1× 10^-9' in s]
check('lab box, 1x10^-9, 3.5 T and 10 K are in one sentence of the stored abstract, as separate conditions',
      len(sentence) == 1 and all(x in sentence[0] for x in ('3.5 T', 'temperatures as high as 10 K', ', or measurement')),
      sentence[0][:80] if sentence else None)
check('lab box, the stored abstract ties the large spacing of the lowest levels of graphene to a resistance standard',
      'In graphene, the spacing between the lowest discrete energy levels' in text and 'exceptionally large' in text
      and 'promising for a quantum Hall resistance standard' in text, 'found')

# ---------------------------------------------------------------- the old bullets, open points 3 and 4 of the plan
b1 = 1 / gaas(1)                                       # the field where hbar omega_c of GaAs is 1 meV
check('old text, open point 4: hbar omega_c of GaAs is 1 meV at 0.58 T, 1.73 meV at 1 T and 17.3 meV at 10 T',
      round(b1, 2) == 0.58 and abs(gaas(b1) - 1) < 1e-12, round(b1, 4))
kT1 = KB * 1 / E * 1e3                                 # k_B times 1 K, in meV
check('old text, open point 4: k_B times 1 K is 0.086 meV, 1/20 of hbar omega_c at 1 T',
      round(kT1, 3) == 0.086 and round(gaas(1) / kT1) == 20, (round(kT1, 4), round(gaas(1) / kT1, 2)))
b10 = (graphene(1) / gaas(1) / 10) ** 2                # the field where the ratio of the two scales is 10
check('old text, open point 3: the ratio of E_1 to hbar omega_c is 10 at 4.4 T, 21 at 1 T and 6.6 at 10 T',
      round(b10, 1) == 4.4 and abs(graphene(b10) / gaas(b10) - 10) < 1e-9, round(b10, 3))
check('old text, open point 3: E_1 of graphene at 10 T is 115 meV, the "around 100 millielectronvolts"',
      round(graphene(10)) == 115, round(graphene(10), 2))
kT100 = KB * 100 / E * 1e3
check('old text, "up to about 100 K" has no stored source: k_B times 100 K is 8.6 meV, 1/13 of E_1 at 10 T',
      round(kT100, 1) == 8.6 and round(graphene(10) / kT100) == 13, (round(kT100, 3), round(graphene(10) / kT100, 2)))
check('old text, "almost room temperature": the stored abstract of doi 10.1126/science.1137201 says room temperature',
      'the QHE can reliably be measured even at room temperature' in stored('https://www.science.org/doi/10.1126/science.1137201'),
      'found')

# ---------------------------------------------------------------- quiz 2, the plateau at 2 e^2/h in both materials
from pyqula import geometry
TMP = tempfile.TemporaryDirectory(prefix='g1_01_')     # removed at the end, with what pyqula wrote in it
here = os.getcwd()
os.chdir(TMP.name)
n = 20                                                 # graphene, the rotated cell of 80 sites with one flux quantum
gg = geometry.honeycomb_lattice_square_cell().rotate(90).get_supercell((n, 1))
hg = gg.get_hamiltonian()                              # the two spins
hg.add_orbital_magnetic_field(1 / (3 * np.sqrt(3) * n))
eg = np.linalg.eigvalsh(hg.get_hk_gen()([0., 0., 0.]))
zero = np.sum(np.abs(eg) < 1e-6)
first = np.min(eg[eg > 1e-6])
hg.add_onsite(-first / 2)                              # the Fermi energy in the gap above the zero level
c_graphene = hg.get_chern(nk=8)
gs = geometry.square_lattice().get_supercell((1, 20))  # the parabolic gas, the band bottom of the square lattice
hs = gs.get_hamiltonian(tij=[-1.])                     # the two spins, degenerate
hs.add_orbital_magnetic_field(1 / 20)
es = np.linalg.eigvalsh(hs.get_hk_gen()([0., 0., 0.]))
hs.add_onsite(-(es[1] + es[2]) / 2)                    # the Fermi energy in the gap above the lowest level
c_square = hs.get_chern(nk=20)
os.chdir(here)
TMP.cleanup()
check('quiz 2, the plateau 2 e^2/h: spinful graphene above its zero level, which holds 4 states per flux quantum, '
      'and the spinful parabolic gas with its lowest level filled', abs(c_graphene - 2) < 1e-6 and abs(c_square - 2) < 1e-6
      and zero == 4 and abs(es[0] - es[1]) < 1e-9, (round(c_graphene, 6), round(c_square, 6), int(zero), round(first, 3)))
print('all checks of page 01 hold')
