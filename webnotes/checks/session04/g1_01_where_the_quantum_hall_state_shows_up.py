"""Session 4, the numbers that page 01 (Sections 4.1 and 4.2) quotes, in the caption of g1_energy_scales, the two
quizzes and the problem. The figure script webnotes/figures/session04/g1_energy_scales.py asserts the numbers of its
caption too, and they are repeated here so that build.py --verify sees them.

The lab box quotes 3.5 T, 10 K and 1e-9 from the stored abstract of arXiv:1504.06511. labsource.py --check 4 shows
the first two and does not read 1x10^-9, so this script finds the three in one sentence of the stored file.

The GaAs bullet of Section 4.1 said "roughly one millielectronvolt" for the fields of a laboratory, and it was corrected
on 2026-11-22, after the choice of the lecturer to fix the errors of the old text, to "1.7 meV per tesla, so a few
millielectronvolts at a few tesla and 17 meV at 10 T". This script asserts the new numbers: 1.73 meV per tesla by two
routes, 3.5 to 8.6 meV for 2 to 5 T, which is "a few millielectronvolts", and 17 meV at 10 T.

The rest of the two bullets and the caption of hall_setup were decided on 2026-11-22, by the rule of the coordinator
for the points that the lecturer did not pick, and the block marked "decided on 2026-11-22" backs them. The kelvin of
GaAs now follows from the reason of the problem, a thermal energy much smaller than the spacing and a broadening by
disorder, and k_B times 1 K is 1/20 of hbar omega_c at 1 T. The graphene bullet keeps "roughly one order of magnitude"
and "around 100 millielectronvolts", since the ratio is 10 at 4.4 T and E_1 is 115 meV at 10 T. "Up to about 100 K"
had no stored source and was removed, and after an independent check the bullet says what the stored abstract of doi
10.1126/science.1137201 says, that the quantum Hall effect of graphene can be measured even at room temperature, with
115 meV at 10 T as 4.4 k_B T at 300 K for "high enough". The caption of hall_setup now says that its arrows are drawn
for electrons, and that for the charge +e the channels of the top contact end in the right contact. The check
computes the edge current of a square island with the field into the page for both charges, reads the sense of the
arrows from the coordinates of hall_setup.py, and counts the currents of the four contacts with Landauer-Buttiker
for both senses.

The plateau at 2 e^2/h of the feedback of the second quiz is computed with pyqula for the spinful honeycomb lattice
with the Fermi energy above its zero level and for the spinful square lattice with its lowest level filled, which are
graphene and a parabolic gas with the spin degenerate. pyqula writes files when it computes a Chern number, so that
part runs in a temporary folder that the script removes.

Every value comes from two routes, the SI constants and the conversion of the conventions sheet
(1.73 meV per tesla for GaAs, 36.3 meV for sqrt(B/T) in graphene). It needs numpy and pyqula, and writes no file in
the repository.

The blocks marked "corrected on 2026-11-22" back the sentences of the old text that were corrected on that day, after
the lecturer chose to fix the errors of the old text."""
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

# ---------------------------------------------------------------- the GaAs bullet, corrected on 2026-11-22
# "1.7 meV per tesla, so a few millielectronvolts at a few tesla and 17 meV at 10 T": the rate by the SI constants and
# by 2 mu_B / 0.067, the values for the fields of a few tesla, and the value at 10 T
few = [gaas(B) for B in (2, 3, 4, 5)]
check('bullet: GaAs has 1.7 meV per tesla by two routes, 3.5 to 8.6 meV for 2 to 5 T, a few millielectronvolts, and 17 meV '
      'at 10 T',
      round(gaas(1), 1) == 1.7 and round(2 * mu_b / 0.067, 1) == 1.7 and abs(gaas(1) - 2 * mu_b / 0.067) < 1e-6
      and 3 < min(few) and max(few) < 9 and round(few[0], 1) == 3.5 and round(few[-1], 1) == 8.6
      and round(gaas(10)) == 17 and round(20 * mu_b / 0.067) == 17, (np.round(few, 3), round(gaas(10), 3)))

# ---------------------------------------------------------------- the two bullets and hall_setup, decided on 2026-11-22
kT1 = KB * 1 / E * 1e3                                 # k_B times 1 K, in meV
check('decided on 2026-11-22, the GaAs kelvin: k_B times 1 K is 0.086 meV, 1/20 of hbar omega_c at 1 T, and 1.73 meV is 20 K',
      round(kT1, 3) == 0.086 and round(gaas(1) / kT1) == 20 and round(gaas(1) * 1e-3 * E / KB) == 20,
      (round(kT1, 4), round(gaas(1) / kT1, 2)))
b10 = (graphene(1) / gaas(1) / 10) ** 2                # the field where the ratio of the two scales is 10
check('decided on 2026-11-22, kept: the ratio of E_1 to hbar omega_c is 10 at 4.4 T, 21 at 1 T and 6.6 at 10 T, '
      '"roughly one order of magnitude"', round(b10, 1) == 4.4 and abs(graphene(b10) / gaas(b10) - 10) < 1e-9
      and round(r1) == 21 and round(r10, 1) == 6.6, round(b10, 3))
check('decided on 2026-11-22, kept: E_1 of graphene at 10 T is 115 meV, the "around 100 millielectronvolts"',
      round(graphene(10)) == 115 and 90 < graphene(10) < 125, round(graphene(10), 2))
page01 = open(os.path.join(WEBNOTES, 'pages', 'session04', '01-where-the-quantum-hall-state-shows-up.md')).read()
check('decided on 2026-11-22: "up to about 100 K" had no stored source and is no longer on the page, and "can be measured '
      'even at room temperature" is what the stored abstract of doi 10.1126/science.1137201 says, with no "best samples"',
      '100 K' not in page01 and 'the quantum Hall effect of graphene can be measured even at room temperature' in page01
      and 'best samples' not in page01 and 'almost room temperature' not in page01
      and 'the QHE can reliably be measured even at room temperature' in stored('https://www.science.org/doi/10.1126/science.1137201'),
      'found')
# "This is high enough": E_1 = 115 meV at 10 T is 4.4 k_B T at 300 K, the number of Session 3, Section 3.6, by the SI
# constants and by the rounded k_B of the problem
kT300 = KB * 300 / E * 1e3
check('decided on 2026-11-22, "high enough": E_1 of graphene at 10 T is 4.4 k_B T at 300 K, as Session 3 says',
      round(graphene(10) / kT300, 1) == 4.4 and round(115e-3 / (8.617e-5 * 300), 1) == 4.4,
      (round(kT300, 3), round(graphene(10) / kT300, 3)))


def island_current(sign, L=14, phi=1 / 16):
    """Current along +x in the upper half of an L x L island of the square lattice, hopping -1, in the edge state of
    the first gap. The hop from (x, y) to (x, y+1) has the phase sign * 2 pi phi x, which is (q/hbar) times the line
    integral of A = (0, s B x), with sign = q s: +1 for the charge +e in the field out of the page or for an electron
    in the field into the page, -1 for the charge +e in the field into the page."""
    idx = lambda x, y: x * L + y
    Hm = np.zeros((L * L, L * L), complex)
    for x in range(L):
        for y in range(L):
            if x + 1 < L:
                Hm[idx(x + 1, y), idx(x, y)] = Hm[idx(x, y), idx(x + 1, y)] = -1
            if y + 1 < L:
                Hm[idx(x, y + 1), idx(x, y)] = -np.exp(1j * sign * 2 * np.pi * phi * x)
                Hm[idx(x, y), idx(x, y + 1)] = np.conj(Hm[idx(x, y + 1), idx(x, y)])
    e, v = np.linalg.eigh(Hm)
    st = v[:, np.argmin(np.abs(e - (-4 + 4 * np.pi * phi)))]          # the gap between the two lowest levels
    # particle current from (x, y) to (x+1, y), 2 Im(psi_b^* H_ba psi_a), summed over the bonds of the upper half
    return sum(2 * np.imag(np.conj(st[idx(x + 1, y)]) * Hm[idx(x + 1, y), idx(x, y)] * st[idx(x, y)])
               for x in range(L - 1) for y in range(L) if y > (L - 1) / 2)


j_plus, j_electron = island_current(-1), island_current(+1)          # the field into the page, as hall_setup.py draws it
src = open(os.path.join(WEBNOTES, 'figures', 'session04', 'hall_setup.py')).read()
loop_src = re.search(r'for \(p, q\) in \((.*?)\):\n', src, re.S).group(1)
pts = eval('(' + loop_src + ')', {}, dict(x0=1.0, y0=0.6, S=4.0, d=0.28))        # the four arrows of the edge channels, tail to head
starts = np.array([p for p, q in pts])
area = 0.5 * sum(starts[i, 0] * starts[(i + 1) % 4, 1] - starts[(i + 1) % 4, 0] * starts[i, 1] for i in range(4))
chain = all(np.allclose(pts[i][1], pts[(i + 1) % 4][0]) for i in range(4))
check('decided on 2026-11-22, hall_setup: with the field into the page the charge +e goes along +x in the upper half, '
      'clockwise, and an electron along -x, counterclockwise, which is the sense of the arrows that hall_setup.py draws',
      j_plus > 0.1 and j_electron < -0.1 and abs(j_plus + j_electron) < 1e-9 and chain and area > 0
      and 'into the page (a cross)' in src, (round(j_plus, 4), round(j_electron, 4), round(area, 3)))


def four_contacts(order, V, N=3, floating=()):
    """Landauer-Buttiker for N chiral channels that go from each contact to the next one in `order`. The current
    into the sample from contact i, in units of e^2/h times a volt, is N (V_i - V_prev(i)), where prev(i) is the
    contact whose channels arrive at i. A floating contact draws no current, so it takes the potential of the
    contact before it. Returns the current that leaves the sample into each contact."""
    V = dict(V)
    for c in floating:                                  # a floating contact sits at the potential of the one before it
        V[c] = V[order[(order.index(c) - 1) % 4]]
    return {c: -N * (V[c] - V[order[(order.index(c) - 1) % 4]]) for c in order}


Vy = 1.0
ccw = ('bottom', 'right', 'top', 'left')               # the arrows of hall_setup.py, the electron sense
cw = ccw[::-1]                                         # the charge +e in the same field
grounded = dict(top=Vy, bottom=0.0, left=0.0, right=0.0)
I_e, I_p = four_contacts(ccw, grounded), four_contacts(cw, grounded)
I_pf = four_contacts(cw, grounded, floating=('right',))
check('decided on 2026-11-22, hall_setup: with the top contact at V_y and the others at 0, the channels of the top contact '
      'end in the left contact for the drawn sense, which takes N (e^2/h) V_y, and in the right contact for the charge +e, '
      'which then takes it while the left one takes 0',
      I_e['left'] == 3 * Vy and I_e['right'] == 0 and I_p['right'] == 3 * Vy and I_p['left'] == 0
      and cw[(cw.index('top') + 1) % 4] == 'right' and ccw[(ccw.index('top') + 1) % 4] == 'left'
      and I_pf['left'] == 0 and I_pf['bottom'] == 3 * Vy, (I_e, I_p, I_pf))

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
