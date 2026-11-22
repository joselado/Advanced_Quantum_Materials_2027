# Entanglement entropy of a block in the middle of a long chain of free fermions, critical and dimerized
from pyqula import geometry

N = 3002  # sites of the open chain, even, so that no level sits at zero energy
ells = [10, 32, 100, 316, 1000]  # lengths of the blocks, even, so whole cells of the dimerized chain
starts = [2*((N//2 - l//2)//2) for l in ells]  # first site of each block, an even site in the middle

g = geometry.chain()  # chain with one site per cell and first-neighbor hopping 1
h = g.get_hamiltonian(has_spin=False)  # spinless free fermions, the XX spin chain after Jordan-Wigner
hf = h.set_finite_system(n=N)  # open chain of N sites, the levels below zero are filled
S_critical = [hf.get_entanglement_entropy(region=list(range(s, s + l))) for (s, l) in zip(starts, ells)]  # in nats

g = geometry.bichain()  # chain with two sites per cell
h = g.get_hamiltonian(has_spin=False)  # hopping 1 inside the cell and between the cells
h.inter = 0.6*h.inter  # hopping 0.6 between the cells, the gap is 2|1 - 0.6| = 0.8
hf = h.set_finite_system(n=N//2)  # open chain of N/2 cells, N sites
S_dimerized = [hf.get_entanglement_entropy(region=list(range(s, s + l))) for (s, l) in zip(starts, ells)]  # both ends cut a bond 0.6

print(ells)
print(S_critical)
print(S_dimerized)
