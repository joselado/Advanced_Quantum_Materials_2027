"""Session 7, Section 7.6. The entanglement entropy of a dimerized Heisenberg chain of 12 spins 1/2, by exact diagonalization.
The bonds alternate J1=1 (inside a dimer) and J2 (between dimers)."""
META = dict(
    id="dimerentropy", title="Entanglement entropy of the dimerized chain",
    params=[dict(name="J2", label="coupling between dimers J2 (J1 = 1)", min=0.0, max=1.5, step=0.1, value=0.0, fmt=1)],
    packages=["numpy", "scipy"], pyqula=False,
)


def compute(p):
    import numpy as np
    import scipy.sparse as sp
    from scipy.sparse.linalg import eigsh
    J2 = float(p["J2"])
    N = 12
    # S_i . S_j on two neighboring spins, in the basis up-up, up-down, down-up, down-down
    bond = sp.csr_matrix(np.array([[.25, 0, 0, 0], [0, -.25, .5, 0], [0, .5, -.25, 0], [0, 0, 0, .25]]))
    H = sp.csr_matrix((2 ** N, 2 ** N))
    for i in range(N - 1):
        J = 1.0 if i % 2 == 0 else J2
        H = H + J * sp.kron(sp.kron(sp.identity(2 ** i), bond), sp.identity(2 ** (N - i - 2)))
    e, v = eigsh(H.tocsc(), k=1, which="SA")
    psi = v[:, 0]
    S = []
    for cut in range(1, N):                      # the first `cut` spins form the subsystem A
        s = np.linalg.svd(psi.reshape(2 ** cut, 2 ** (N - cut)), compute_uv=False) ** 2
        s = s[s > 1e-14]
        S.append(float(-(s * np.log(s)).sum() / np.log(2)))
    cuts = np.arange(1, N)
    S = [abs(x) for x in S]
    if J2 < 1e-9:
        text = "J2=0. The chain is a product of singlets. A cut through a dimer gives exactly log 2, and a cut between dimers gives zero."
    elif abs(J2 - 1) < 1e-9:
        text = ("J2=1. This is the uniform Heisenberg chain, which is critical. The entropy is of order log 2 for every cut, "
                "with an even-odd alternation that comes from the open ends. With 12 spins we cannot resolve the slow growth with the size of A.")
    elif J2 < 1:
        text = ("J2=%.1f. The cut through a dimer gives %.2f log 2, and the cut between dimers gives %.2f log 2. "
                "The weak bond J2 entangles neighboring dimers a little, so the cut between dimers is small but no longer zero."
                % (J2, S[0], S[1]))
    else:
        text = ("J2=%.1f. The bonds J2 are now the strong ones, so the dimers are formed between sites 2 and 3, 4 and 5, and so on. "
                "The cuts through a J2 bond have the largest entropy, up to %.2f log 2." % (J2, max(S)))
    return dict(
        panels=[dict(title="Entropy of the first l spins, N=12", xlabel="cut l", ylabel="S (units of log 2)",
                     xlim=[0.5, N - 0.5], ylim=[0, 2.2],
                     series=[dict(x=cuts, y=S, kind="both", color=0)])],
        text=text,
    )
