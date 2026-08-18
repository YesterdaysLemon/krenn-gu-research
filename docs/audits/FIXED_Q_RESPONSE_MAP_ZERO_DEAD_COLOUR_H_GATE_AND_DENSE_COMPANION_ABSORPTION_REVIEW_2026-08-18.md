# Fixed-Q response-map-zero dead-colour h-gate and dense companion absorption hostile review -- 2026-08-18

## Verdict

**Accepted at the frozen theorem and script hashes below.**  No P0, P1, or
P2 defect remains.  The package proves an exact characteristic-zero exclusion
of the `h=0` divisor in one exhaustive `1347`-mask subcell of the `GLD20`
response-map-zero atlas, and an exact companion normal form on the surviving
`h!=0` branch.  It does not exclude that surviving branch, force a legal
`GLD15` operator row, integrate arbitrary companion coefficients into one
same graph, or imply a permanent restriction.  No witness or counterexample
was found.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Physical support and exhaustive subcell

On the exactly-two-corrected-colour channel, the review checked both the
ordinary orthogonal-nonisotropic-line case and the exceptional common-edge
case.  Cross-colour diagonality kills every shore in the third colour at the
one fixed fully supported residual contraction.  This conclusion is broader
than the selected subcell and is not an assertion about the uncontracted
`Q--U` edge tensors.

When one corrected colour has support `K_4`, the opposite edge of every
direct block carries that colour.  Replaying the complete `GLD19`
complementary alternatives therefore confines each nonzero direct block to
the complete colour.  The third colour is dead in every deck term relevant
to the fixed contraction, and no raw `B/K` support union contains all three
colours, so this is an `F=empty` subcell.

The support count is exhaustive at the mask level:

```text
secondary K2:  36 corrected types * 32 raw masks = 1152;
secondary K3:  24 corrected types *  8 raw masks =  192;
dense K4/K4:    3 corrected types *  1 raw mask  =    3;
total:          63 corrected types, 1347 raw masks.
```

The finite count is neither a graph-fibre count nor a witness enumeration.
Both exact implementations independently enumerate the raw complementary
choices and check that every direct mask is confined to the distinguished
complete colour; the dense cell has `B=0`.

## Full mixed coefficient and residual-scalar gate

The hostile review checked all `31` nonempty even deck labels in the complete
fixed-`Q` companion expansion.  On the all-third-colour port word, every
label except `I=Q` contains a vanished third-colour direct edge or contracted
shore.  Therefore a hypothetical witness satisfies the root-tensor identity

```text
h G_U(-_R;a^4)=alpha_a e_a^(tensor R).
```

Full support gives `alpha_a!=0`.  Hence `h=0` is impossible throughout all
`1347` masks, while `h!=0` forces one prescribed pure nonzero root coefficient
and the other eighty root coefficients to vanish.  This uses one coefficient
of the complete mixed GHZ equation on the same graph.  It does not vary the
residual contraction or reuse the pointwise support theorem at another point.

The Hamming-one label ledger is also exact.  On every port of the secondary
clique, its two active shore vectors are independent, so the two equations
solve the two one-`Q` companion tensors.  Outside a proper secondary clique,
the secondary shore is zero and the corresponding mixed target coefficient
forces the displayed `G_U(a^3d)` coordinate to vanish.

## Dense companion absorption

In the dense `K_4/K_4` cell the complementary alternatives force every
direct block to vanish.  For each of six repeated edges and either repeated
active colour, the theorem takes the two oriented `2+1+1` port words and all
`81` root words.  The resulting `162` rows have one desired companion column
and exactly nine nuisance columns.

The final reviewed statement defines those columns rowwise.  In particular,
the singleton-complement columns are explicitly masked to zero on the
orientation where that singleton has dead colour.  With

```text
nu=(h,(H_(q,t)(ell_t))_(q in Q,t in U)),
```

the literal coefficient equation is

```text
N_(e,s) nu + K_e(s,s) g_(e,s)=0.
```

Since `K_e(s,s)!=0`, the desired column lies in the nuisance image.  This
gives twelve simultaneous two-orientation absorptions, comprising twenty-four
port words and `1944` scalar root coefficients.  A nonzero augmented
`10 x 10` minor is a sufficient predetermined mixed detector, but is not
exhaustive when the nuisance rank is below nine.  These scalar coefficient
rows are not legal complete-nuisance `GLD15` operator rows.

During hostile review, an earlier bare-column presentation was rejected as
ambiguous because the two singleton columns occur in different orientations.
The frozen theorem repairs this with explicit orientation masks and defines
the coefficient vector and desired column.  An earlier canonical-package-only
script was also strengthened: both final implementations loop over all six
edges and both repeated active colours and assert exactly twelve packages.

## Controls and exact boundary

Exact rational shores realize the excluded dense `h=0` response window with
`K_e=diag(2,-2,0)` and `B=0`.  A private missing-colour root-to-port matching
realizes the forced pure companion slice at same-graph coefficient level for
`h!=0`; it is not a witness.  Dense desired-only and root-root-zero controls
show that the augmented-rank detector can respectively fire or be swallowed.
A no-`K_4` control retains a third-colour direct label on the all-third-colour
word, proving the complete-clique hypothesis is load-bearing.

Most importantly, at `h!=0` the complete fixed-`Q` linear companion equation
always has the abstract solution

```text
G_U=J_Q/h,             G_D=0 for D!=U.
```

This solution satisfies the displayed pure, Hamming-one, and dense absorption
equations but need not arise from the principal-permanent companion family of
the same graph.  Joint root-companion integrability is therefore the exact
remaining obstruction; fixed-`Q` linear algebra alone cannot exclude the
surviving branch.

## Independent checks and frozen evidence

The SymPy primary and standard-library no-import audit use separate sparse
hafnian, support-enumeration, and rational-rank implementations.  Both check
all twelve dense label packages.  Their rank fixtures audit abstract rank
semantics; they do not instantiate the actual `162 x 9` companion matrix of a
hypothetical witness.  The arbitrary-field shore argument, the use of the
full `GLD19` alternatives, and the same-graph coefficient interpretation
remain load-bearing written proofs.

The primary and independent scripts pass, as do Ruff check, Ruff
format-check, the `GLD15`, `GLD18`, `GLD19`, and `GLD20` predecessor
primary/audit pairs, and the repository validation tests.  README and live
frontier integrations preserve the `UNKNOWN` and `UNRESOLVED` boundaries.

Frozen at base HEAD `f547c3a1bd08967bde049649914a621d37c57ae4`:

```text
theorem  6e77435a9184b024187684f8eebd7af8a1ed885c32064e5d9290fa72ac23cc56
primary  154825ba62d96bcf22782c588285aaf4c8a29f242cbb2d35407ad246816a22ba
audit    c7d3cf9853e7f56c394a7804e1f1206114fdc7c182d6c6d8327b022cc85341b4
```

## Exact remainder

Still **UNKNOWN**: exclusion of the `h!=0` one-complete-clique subcell;
same-graph principal-permanent integration of the forced pure slice; a
universally nonzero dense augmented minor; a nonzero legal complete-nuisance
operator package; the other `F=empty` cells; the maximal star/triangle
pure-absorption cells; and every weighted-permanent consequence.
