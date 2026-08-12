# Review of the binary syzygy--permanent residual obstruction

## Verdict

**PASS, with no P0--P3 finding.**

The exact three-file core was reviewed read-only at

```text
db21254fc4ac6aaee5b8e4871c2a24aebda0aa4e
```

over parent/base

```text
8fbc58ac773edd301c0539c09e44bded26882052.
```

It was then rebased byte-identically onto the A8 merged main

```text
722e93abaecec729b2ab160b77b3e1d1231c85f0
```

as core commit

```text
eab2db9830c02497228cd777b7b276d5e2c44937.
```

The raw Git-object SHA-256 values are

```text
theorem: 5795662b462f8def2aab72cbf38d5902ea67847e9b686c2715940c7b8fe7c7a7
primary: 167b79501b2e58ee7a2711b4892a60f012997cbf3d898bdf2c2c62fab68e254b
audit:   425264bdc6b5b2ebd1bafe4b48d7f024438395db22f5cdf34fdfd3dff362d111
```

The corresponding Git blobs are

```text
theorem: 85681670f19102029a91ab2750d4c7f4def25c3e
primary: 3d853929d1223acb15f598e57db372f7ba2f73c6
audit:   6c4682be302f54d6cea90c99baab6bfa93265dd0
```

Both hostile reviews were independent and made no edits.  Global Krenn--Gu
remains **UNRESOLVED**.

## 1. Theorem audit

Let

```text
D_C(u,v,w)=u tensor C_23+C_13 tensor v+C_12 tensor w.
```

The theorem assumes that a nonzero pure tensor `P` lies in `image(D_C)` and
that a second nonzero pure tensor `Q` is the polarized six-term permanent of
three vectors in `kernel(D_C)`.  It proves that `P` and `Q` share a factor
line.

The review checked the following load-bearing steps.

1. Since `Q` is nonzero, the span of its three kernel vectors projects
   nontrivially to all three root spaces.  Over the infinite
   characteristic-zero field, a kernel vector with all three components
   nonzero exists.
2. Quotienting its syzygy gives the exact three-block normal form and a
   companion kernel vector.  Direct expansion has the stated signs and gives
   `D_C(m)=-Alt(k,l,m)`.  Dependence of the companion on the first vector
   forces all three blocks to vanish, contrary to `P!=0`.
3. When all blocks are nonzero, the coordinate-projection ranks of the
   resulting kernel plane have, up to permutation, exactly the four forms
   `222`, `122`, `211`, and `111`.  The stated canonical representatives are
   valid over the original field; no algebraic closure is used.
4. In type `222`, commutative multiplication kills the image but not a
   nonzero pure tensor.  In the other three types, exact quotient maps force
   every image pure tensor to use a fixed rank-one factor, while every
   nonzero kernel permanent has that same fixed factor.
5. With exactly one zero block, the other two blocks have one common
   rank-one factor.  The full kernel and tangent image are exactly those
   displayed in the theorem, so the permanent and every image pure tensor
   again share one of the two remaining fixed factors.  Two zero blocks make
   the relevant kernel permanent zero; three make the image zero.

These cases exhaust the hypotheses and prove the shared-factor theorem.

## 2. S2O application and sharpness

S2O proves that a common-shore realization of any one of the eight normalized
S2M controls would produce binary pure tensors

```text
P=p_1 tensor p_2 tensor p_3,
Q=z_1 tensor z_2 tensor z_3
```

with `(p_i,z_i)` a basis in every root space.  Their factor lines are
transverse in all three positions, so the new theorem excludes the residual
and hence all eight common-shore realizations.

The review also replayed the `122` sharpness example.  Its image contains
`v_1 tensor u_1 tensor u_1`, while three proportional kernel vectors have,
after one exact rescaling, permanent `v_1 tensor u_0 tensor u_0`.  The two
pure tensors share exactly one factor line.  Thus the shared-factor
conclusion is sharp; the theorem does not falsely prohibit all pure
image/permanent coexistence.

## 3. Evidence and independence

The primary verifier uses SymPy dense matrices.  It derives the three shore
blocks from each canonical kernel plane, checks full kernels by rank-nullity,
checks the symmetric-multiplication and quotient certificates, verifies the
one-zero-block tangent model, and replays sharpness.

The independent audit imports neither SymPy, the primary verifier, nor
repository modules.  It reconstructs the shore blocks first, builds the
singleton map directly, performs a separately written exact `Fraction`
Gauss--Jordan reduction, checks every basis-polarized permanent needed by
trilinearity, covers the one-, two-, and three-zero-block strata, and tests
sharpness through exact column-span membership.

At the frozen core:

```text
primary replay:              PASS;
independent python -I audit: PASS;
Python compilation:          PASS;
Ruff 0.16.2:                 PASS;
git diff --check:            PASS;
clean exact-byte status:     PASS.
```

The scripts audit the displayed canonical identities.  The written quotient
and normal-form argument supplies the arbitrary-field exhaustion; no finite
enumeration is promoted into that proof.

## 4. Scope firewall

The review rejects every stronger reading below:

```text
the eight normalized S2M controls are common-shore realizable:       FALSE;
the eight controls are sharp inside the physical common-shore image: FALSE;
every realized target incidence satisfies the retained pair gate:   NOT PROVED;
the universal S2 full-sensor gate is closed:                         NOT PROVED;
a physical graph or Krenn--Gu witness is constructed or excluded:   NOT CLAIMED;
shared physical variables imply support-difference lattice coupling: NOT CLAIMED;
the all-balanced rank-drop branch is excluded:                       NOT PROVED;
the Krenn--Gu conjecture is resolved:                                FALSE.
```

The exact advance is narrower and useful: S2O's binary residual is empty, so
the eight known ambient coordinatewise sharpness controls do not survive the
physical common-shore equations.  A universal realized-incidence theorem
still requires an exhaustive argument beyond those controls.  Global
Krenn--Gu remains **UNRESOLVED**.

## 5. Final assessment

No mathematical, scope, independence, or portability defect was found in the
frozen core.  Promotion is appropriate after maintained navigation and ledger
integration, the complete candidate-tree floor, final exact-head repinning,
published-head CI, and merged-main replay.
