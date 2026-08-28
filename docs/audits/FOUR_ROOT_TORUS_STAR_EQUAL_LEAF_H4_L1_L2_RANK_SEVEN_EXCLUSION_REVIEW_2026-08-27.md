# GLD93 hostile review: H4 L1/L2 rank-seven exclusion

## Review disposition

**Accepted as an exact scoped theorem package, with the global status
unchanged at `UNRESOLVED`.**  The reviewed claim is

```text
B intersect V(I_7(A)) intersect H4 intersect V(L1)
  intersect D(Omega (p-q)d0 P) = empty,
B intersect V(I_7(A)) intersect H4 intersect V(L2)
  intersect D(Omega (p-q)d0 P) = empty.
```

Here `d0=p+q-1`, `P=p^2-p+1`, and the rational H4 chart has
`s=(p+q-pq)/d0`.  This is a geometric-point, characteristic-zero result in
the displayed equal-leaf chart.  It is not a claim about the other H4
boundaries, the full pulled-back GLD83 Fitting ideal, other charts or
components, source branches, profiles, roots, orders, or the global
conjecture.

## Evidence inspected

The primary verifier
`claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_l1_l2_rank_seven_exclusion.py`
reconstructs the complete `37 x 9` GLD71 syndrome matrix and checks exactly:

1. the H4 relation and the L1 parameterization
   `q=p(2-p)/(2p-1), s=p`, including all upstream factor restrictions;
2. the four L1 raw six-/bordered seven-minor identities and the auxiliary
   double-pivot seven-minor;
3. both L1 exceptional fibres `(p,q)=(2,0),(-1,1)` without dividing by the
   vanished pivot factor or by `T`;
4. the H4 L2 parameterization
   `p=q(2-q)/(2q-1), s=q`, directly rather than by a presumed symmetry;
5. the four L2 raw six-/bordered seven-minor identities and the auxiliary
   double-pivot seven-minor; and
6. both L2 exceptional fibres `(p,q)=(0,2),(1,-1)`, including the two
   coprime witness pairs on each vanishing-bracket branch.

The independent audit
`claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_l1_l2_rank_seven_exclusion.py`
imports neither the primary nor the GLD71 builder.  It stores the nine sparse
GLD71 relation supports touched by the certificates in a separate
representation, contracts those supports directly against the equal-leaf
frame, and recomputes every displayed selected determinant.  It also checks
the two rational parameterizations, determinant gates, double-pivot minors,
exceptional witnesses, and coprimality of the final linear factors.  It is
genuinely independent evidence for the selected identities, while honestly
not claiming an independent reconstruction of the other 28 GLD71 rows.

Both exact scripts pass on the reviewed candidate tree.

## Adversarial findings

### The H4 chart denominator is not silently inverted

On `L1=0`, the equation is

```text
(2p-1)q+p(p-2)=0.
```

At `2p-1=0` its residual is `-3/4`, so there is no omitted L1 point.  On
`L2=0`, the exchanged equation has the same property at `2q-1=0`.  The
separate `d0=0` overlap is not included in this rational calculation; it is
closed upstream by GLD89.

### The upstream localization is preserved

On L1, the exact restrictions are

```text
p-q=3p(p-1)/(2p-1),
d0=P/(2p-1),
L2=-3p(p-1)P/(2p-1)^2,
Q6=6p^2(p-1)^2P^3/(2p-1)^4.
```

On L2, writing `Q=q^2-q+1`, they are

```text
p-q=-3q(q-1)/(2q-1),
d0=Q/(2q-1),
P=Q^2/(2q-1)^2,
Q6=6q^2(q-1)^2Q^3/(2q-1)^4.
```

Thus `D((p-q)d0P)` removes precisely the displayed zero factors and makes
the common-pivot factor `Q6` nonzero on either divisor.  No unlisted factor
is silently inverted to obtain the result.

### The ordinary pivot case split is exhaustive

For L1, away from `p=2,-1`, the two raw brackets are `H10,H11`.  If either
is nonzero, the matching bordered seven-minor is nonzero after using
`det(G) != 0`.  If both vanish, the displayed linear solution in `a,b`
leads to the auxiliary seven-minor with factor `F1`; its frame determinant
is the same nonzero factor up to units.  The only points removed from this
ordinary argument by a pivot prefactor are exactly `p=2,-1`, and both are
checked directly.

For L2 the same exhaustive structure uses `H20,H21`, the double solution
with factor `F2`, and the exceptional values `q=2,-1`.  The exceptional
branches are not discarded: when the surviving bracket vanishes, two
seven-minors have distinct linear factors in `b`, so they cannot both vanish
under `b-c != 0`.

### Rank logic uses the proved bridge

The rank conclusion is not inferred from a numerical sample.  GLD86 gives

```text
B=0 iff M(G)C=0,
rank A=rank M(G)[:,0:8] on B,
C_8=1.
```

Membership in `V(I_7(A))` therefore makes the first eight syndrome columns
have rank at most six.  The ninth column is then a combination of those
columns because `M(G)C=0` and `C_8=1`; hence every full `7 x 7` syndrome
minor must vanish.  GLD93 supplies a nonzero seven-minor at every point of
the two divisor case splits, using only `det(G) != 0` from `D(Omega)`.  This
is a valid contradiction.  No claim that every ambient point has rank at
least seven is made.

### The failed naive symmetry is recorded, not used

Swapping the first two columns of the displayed frame gives

```text
G(p,q,a,b,c) P_(01) = G(q,p,1+b,a-1,c),
```

but that coordinate identity alone does not transport the fixed GLD71
syndrome carrier.  The primary and audit compute L2 directly in the `q`
chart and mark `naive_pq_symmetry_used=false`.  No carrier-equivariance claim
is hidden in the L2 closure.

## Remaining obligations

| residual | reviewed disposition |
| --- | --- |
| `p=q` / H1 and transported H2/H3 | closed upstream by GLD87; not reproved here |
| `P=0` and `d0=0` overlap | closed upstream by GLD89; not divided through here |
| `L1=0` | closed by GLD93 on `D(Omega (p-q)d0P)`, including its `e=T=0` points |
| `L2=0` | closed by GLD93 on `D(Omega (p-q)d0P)`, including its `T=0` points |
| `Q6=0` | retained; GLD90's common raw-pivot factor remains open |
| `e=0` away from L1/L2 exceptional intersections | retained for separate analysis |
| pulled-back GLD83 Fitting ideal | not computed |
| other H4 charts/gauges/components and rank-eight/lower-rank branches outside this chart | open |
| source branches, profiles, roots, orders, and global Krenn--Gu | open; global status **UNRESOLVED** |

The package is therefore a durable two-divisor rank-seven exclusion inside
the Gaussian equal-leaf chart, not a complete H4 or global proof.
