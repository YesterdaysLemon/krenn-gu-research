# Review of the balanced full-sensor common-shore compatibility theorem

## Verdict

**PASS at the frozen three-file core, with no P0--P3 finding.**

Reviewed commit:

```text
802e93cac8cf57eb06ab9f30221623a8d0ac6736
```

Its exact parent and base was

```text
fc38d7826a46108b1c2d35b5d49aa2df35261529.
```

Reviewed raw Git-object SHA-256 values:

```text
theorem:  ae4f286b99f3ca8825aca2d9ff58518e51878cd64f5b9cf0e4cc0565f337893e
primary:  fcbdc28c750193cc21c4746e8e7b6b943c992e5bd8ef3926c59e767d74ca5c2f
audit:    f6244be74861b3822a88ab803fb9930af4c9d2daf716c40b0d479dd94be8f64e
```

The theorem Git blob was

```text
624a096294afbdc985dcfa8c9e8a6f5b091c35f3.
```

The review was read-only.  The worktree remained clean and the reviewed bytes
were not edited.  Repository publication must repin the integrated theorem
through the canonical ledger hash and final exact commit.

The result is an exact `m=3` common-shore image characterization and an
ambient nonrealizability boundary.  It does not decide any retained S2M jet
control or exclude the balanced full-sensor branch.  Global Krenn--Gu remains
**UNRESOLVED**.

## 1. Exact theorem surface

For roots `R={1,2,3}` and nonroots `N={x,y,r}`, the complete even-deck sensor
has the four columns

```text
(G_r,G_y,G_x,G_N)
```

in the standard label order

```text
(xy,xr,yr,empty).
```

The theorem proves that one fixed physical shore produces a proposed
four-column sensor if and only if there are three root--root tensors and nine
root--nonroot blocks for which:

1. all nine singleton-complement slices lie in the same shared-factor
   subspace

   ```text
   S_B=A_1 tensor B_23+B_13 tensor A_2+B_12 tensor A_3;
   ```

2. each slice has the displayed three-summand factorization using those same
   root--root blocks; and
3. every coefficient of `G_N` is the sign-free six-term permanent of the same
   nine cross blocks.

At `m=3` these are all shore-sensor columns.  The nonroot--nonroot physical
blocks instead determine the scalar deck vector `C`; they are not omitted
data from this characterization of `Gamma`.

The theorem then constructs a degree-compatible `27 x 4` Latin-plane system
with exact GHZ target, `f_empty=1`, and function-field column rank four, but
proves that this matrix is outside the common-shore image.

## 2. Matching-partition audit

For one singleton companion `G_u`, exactly one root is matched across the
balanced cut.  If that root is `1`, `2`, or `3`, the other two roots contribute
respectively the unique internal edge `B_23`, `B_13`, or `B_12`.  Summing the
three choices gives the shared-factor formula, with one fixed triple of
root--root blocks across every nonroot and colour slice.

For the empty companion `G_N`, all three roots cross the cut.  Its six
matchings are exactly the six bijections from the roots to `N`, so every
coefficient is the displayed `3 x 3` permanent.  Conversely, the coefficient
triples assemble into the nine root--nonroot bilinear blocks in the chosen
bases.  The two formulas therefore reconstruct all four columns.  No target
equation, rank assumption, division, or generic specialization enters this
if-and-only-if statement.

The notation firewall is correct and load-bearing:

```text
Gamma_empty=G_N       is the shore sensor column;
C_empty=1             is the separate empty deck normalization.
```

The proof does not identify these two objects.

## 3. Latin-plane separator audit

The three singleton columns use the nine coordinate tensors

```text
(c,u,-c-u),          c,u in Z/3Z.
```

They therefore have the exact deck-complement multidegrees

```text
(0,0,1), (0,1,0), (1,0,0).
```

The empty column is the contracted ternary GHZ section of multidegree
`(1,1,1)`.  With

```text
f=(0,0,0,1),
```

the complete row equation is exactly `Gamma f=J` and `f_empty=1`.

On the four displayed root rows, direct determinant expansion gives

```text
r_0^2 x_0 x_1 y_0^2,
```

which is nonzero in the rational function field.  Hence the full matrix has
column rank four.

The nine singleton slices are independent and span the coordinate subspace
`U_Lambda` on

```text
Lambda={(a,b,c):a+b+c=0 mod 3}.
```

Every coordinate line parallel to any tensor axis meets `Lambda` in exactly
one point.  If the system came from one common shore, then

```text
U_Lambda subset S_B,       dim U_Lambda=9,       dim S_B<=9,
```

so equality would hold.  In particular `A_1 tensor B_23` would lie in
`U_Lambda`.  Any nonzero coefficient of `B_23` would put all three points of
one first-axis line in that coordinate subspace, contradicting the one-point
intersection.  Thus `B_23=0`, after which `dim S_B<=6`, the final
contradiction.

The obstruction occurs already in the singleton slices; the separator does
not claim to satisfy the empty-permanent formula.

## 4. Evidence and independence

The primary verifier uses SymPy to compare the singleton matching enumeration
with the shared-factor tensors using algebraically independent symbols.  It
also expands the universal six-term permanent, verifies every separator row
and multidegree, computes the rank minor, and checks the nine-slice rank and
all axis-line intersections.

The independent audit imports neither SymPy nor repository code.  It uses
exact `Fraction` arithmetic and separate deterministic block data for the
matching identities.  It checks all nine singleton slices and every one of
the `27 x 27` empty-column coefficient cases, then reconstructs all separator
rows with an independent sparse-polynomial determinant and coordinate-support
implementation.

At the reviewed commit:

```text
primary replay:                  PASS;
independent python -I audit:     PASS;
Ruff 0.16.2:                     PASS;
Python compilation:              PASS;
exact diff check:                PASS.
```

The written matching proof carries the arbitrary symbolic quantifiers.  The
stdlib exact-data checks are independent pointwise corroboration rather than
a substitute for that universal proof.

## 5. Scope firewall

The characteristic-zero assumption is conservative.  The displayed proof
does not silently divide by a characteristic-dependent integer or pass from
generic to pointwise data.

The review rejects every stronger reading below:

```text
the Latin separator realizes a retained projective jet pattern:    NOT PROVED;
one of the eight S2M controls is realizable or nonrealizable:       NOT PROVED;
the separator includes a physical nonroot deck:                    NOT PROVED;
the separator is a physical tensor equality or witness:            FALSE / NOT CLAIMED;
every realized target incidence fails the pair-pole gate:          NOT PROVED;
the m=3 characterization extends unchanged to arbitrary m:         NOT PROVED;
the all-balanced rank-drop branch is excluded:                      NOT PROVED;
the Krenn--Gu conjecture is proved or disproved:                    FALSE.
```

The exact advance is narrower: it writes the missing common-shore incidence
at the first nontrivial full-sensor order and proves that the ambient Cramer
format is genuinely larger than that image.  Pulling the S2M controls back to
this incidence, or proving a universal retained-jet failure on every realized
target, remains open.

## 6. Final assessment

No mathematical, scope, independence, or portability defect was found in the
frozen core.  Promotion is appropriate after rebasing onto the latest verified
main, integrating the maintained frontier and ledger without collision,
rerunning the complete candidate-tree floor, and completing exact-head and
merged-main publication verification.  Global Krenn--Gu remains
**UNRESOLVED**.
