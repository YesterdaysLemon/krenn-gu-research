# Exact exclusion of the normalized `q5_311` branch

## Status

This is an exact tensor theorem over `C`.

There is no local restriction

```text
P_5 -> Delta_3
```

whose normalized high-coordinate mode has source-row multiplicities

```text
3,1,1.
```

Equivalently, the complete normalized `q5_311` branch is impossible.
This closes one of the three high-coordinate branches left after the
exact-three-coordinate `P_5` classification.  The normalized `q4_211`
and `q5_221` branches remain open, as does `P_5 -> Delta_3` and the
arbitrary-order Krenn--Gu prize conjecture.

## Rank-drop reduction

Let `M={m_0,m_1,m_2}` be the three majority source rows and `s_1,s_2`
the two rare rows.  For rare target direction `w_c`, deleting `s_c`
forces the other four modes to map the remaining `P_4` to

```text
lambda_c w_c tensor w_c tensor w_c tensor w_c,
lambda_c != 0.                                        (1)
```

The rank-drop theorem gives at least two rank-two maps in each deleted
slice.  Each original five-row local map has rank three because the
target contains nonzero pure tensors in all three target directions;
deleting one source row reduces rank by at most one, so every deleted
map has rank at least two.  The shared-drop obstruction in
[`P5_Q5_311_SHARED_DROP_OBSTRUCTION.md`](P5_Q5_311_SHARED_DROP_OBSTRUCTION.md)
shows that the two drop sets are disjoint.  After relabeling modes,

```text
D_1={0,1},   D_2={2,3}.                               (2)
```

For every remaining mode, its three rows on `M` span a plane.  Indeed,
if a mode belongs to `D_1`, then `M` together with `s_2` has rank two,
while `M` together with `s_1` has rank three.  Thus `M` itself has rank
exactly two.  The argument for `D_2` is symmetric.

Write

```text
B_r : C^3 -> P_r
```

for the common-row restriction in mode `r`, with two-dimensional image
plane `P_r`.  Let

```text
S_r=(tensor over modes other than r of B_i)P_3.        (3)
```

## Every common triple has tensor rank at most one

For `r in D_2`, mode `r` does not drop rank in the first rare slice.
Its exceptional `s_2` row lies outside `P_r`.  Contract (1) in mode `r`
with a covector that annihilates `P_r` and takes the exceptional row to
one.  On the source side this selects `s_2` and leaves `S_r`.  Hence

```text
S_r=0                         if w_1 in P_r,
S_r=mu_r w_1 tensor w_1 tensor w_1, mu_r != 0,
                              if w_1 notin P_r.        (4)
```

For `r in D_1`, the same argument in the second rare slice gives the
corresponding zero-or-pure alternative in target direction `w_2`.
Thus all four triple restrictions `S_r` are either zero or nonzero
decomposable.

The four-plane corollary in
[`P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md`](P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md)
is all-or-nothing:

```text
either every S_r is zero,
or every S_r is nonzero decomposable.                 (5)
```

## The all-zero case is impossible

If all four tensors in (3) are zero, the zero-`P_3` theorem makes the
four row spaces of the `B_r` one common coordinate plane
`e_j^perp`.  Consequently the common source row `m_j` is mapped to zero
by every one of the four modes.

Every permanent term in either deleted `P_4` slice must assign `m_j` to
one of those modes, where its coefficient is zero.  Both deleted slices
would therefore be the zero tensor, contradicting (1).

## The all-nonzero case is impossible

Take the two non-drop modes `2,3` in the first rare slice.  Since `S_2`
is nonzero, (4) says

```text
S_2=mu_2 w_1 tensor w_1 tensor w_1.
```

Its factor in mode 3 lies in the common image `P_3`, so

```text
w_1 in P_3.
```

But applying (4) in mode 3 now gives `S_3=0`, contradicting the
all-nonzero alternative in (5).

Both cases are impossible.  Therefore the normalized `q5_311` branch
has no solution.

## Verification

Run:

```text
python verify_p5_q5_311_exclusion.py
python audit_p5_q5_311_exclusion.py
```

The primary verifier reconstructs the deleted-permanent contractions,
the common-zero source obstruction, and the two-non-drop-mode
zero/nonzero incompatibility.  It pins the hashes of the three exact
structural inputs.  The independent audit checks the all-or-nothing
four-plane boundary and the target-plane incidence contradiction over
`F_3` and `F_5`.  The finite-field census audits the formulas; the
written proof above is over `C`.
