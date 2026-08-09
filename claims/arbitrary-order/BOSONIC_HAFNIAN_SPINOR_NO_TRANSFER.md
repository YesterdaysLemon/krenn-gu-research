# Why the principal-hafnian family is not a spinor family

## Status

**Verified characteristic-not-two route exclusion.**  From six vertices on,
no fixed signing, phase choice, or nonzero edge reweighting converts the
generic principal-hafnian family into principal Pfaffians.  Moreover, the
support of nonzero complex principal hafnians need not be a delta-matroid.

Thus matchgate/spinor identities and delta-matroid exchange cannot be
imported into the Krenn--Gu problem without an additional support-specific
Pfaffian orientation, no-cancellation hypothesis, or valuation degeneration.
The correct universal replacement is the block-square-zero Wick completion
theorem, whose logarithm is quadratic but whose four-point signs are all
positive.

This excludes a proof route, not a Krenn--Gu witness.

## The four-vertex defect

Write `h_S=haf(A[S])` for a generic hollow symmetric matrix.  On four
vertices,

```text
h_1234 = h_12 h_34 + h_13 h_24 + h_14 h_23.          (1)
```

The Pfaffian/spinor Wick polynomial would instead alternate signs.  With one
standard sign convention its value on the hafnian family is

```text
h_1234-h_12 h_34+h_13 h_24-h_14 h_23
 = 2 h_13 h_24,                                      (2)
```

which is generically nonzero.  Vertex- or edge-sign choices can repair one
four-set, so order four alone is not a universal exclusion.  Order six is.

## No universal edge signing

### Theorem 1

Let `K` have characteristic different from two and let the vertex set contain
six vertices.  There are no fixed edge multipliers `t_ij` and nonzero subset
rescalings `c_S` such that, for every generic hollow symmetric matrix `A`,

```text
c_S haf(A[S])
```

are the principal Pfaffians of a single skew matrix whose pair coordinate on
`{i,j}` is `t_ij A_ij`.

Proof.  Restrict six vertices to the cross edges of `K_(3,3)`, with edge
variables `X=(x_ij)`.  The full hafnian is `per(X)`.  The full Pfaffian of a
skew matrix supported on the same bipartition is, up to one global sign,
`det(T hadamard X)`.  Coefficient equality would give one nonzero `lambda`
such that

```text
product_i t_(i,sigma(i)) = lambda sign(sigma)         (3)
```

for every permutation `sigma in S_3`.  Every cross multiplier is nonzero
because it occurs in a permanent monomial.  Comparing three pairs of
permutations gives

```text
t_11 t_22 = -t_12 t_21,
t_12 t_23 = -t_13 t_22,
t_11 t_23 = -t_13 t_21.                              (4)
```

The first two equations imply, after cancelling the nonzero `t_12 t_22`,

```text
t_11 t_23 = t_13 t_21,                               (5)
```

contradicting the third equation in (4).  The same six-vertex restriction
excludes a universal transfer at every larger order.

Support-specific Pfaffian orientations are not excluded.  The theorem says
that the dense bosonic family has no fixed spinor coordinate change of this
natural edgewise kind.

## Cancellation destroys delta-matroid support

### Theorem 2

The set system

```text
F(A)={S : |S| even and haf(A[S]) != 0}                (6)
```

need not be a delta-matroid over `C`.

Proof.  On vertices `{0,1,2,3,4,5}`, take the only nonzero symmetric edge
weights to be

```text
a_01=a_02=a_03=a_05=a_14=a_24=1,
a_34=-1,
a_45=2.                                               (7)
```

For

```text
X={0,3,4,5},   Y={0,1,2,4},                           (8)
```

we have

```text
h_X = a_03 a_45+a_04 a_35+a_05 a_34 = 2-1 = 1,
h_Y = a_01 a_24+a_02 a_14+a_04 a_12 = 1+1 = 2.       (9)
```

Now `X symmetric_difference Y={1,2,3,5}`.  Choose `e=5`.  Every possible
symmetric exchange fails:

```text
h_(X triangle {5,1}) = h_0134 = -1+1 = 0,
h_(X triangle {5,2}) = h_0234 = -1+1 = 0,
h_(X triangle {5,3}) = h_04   = 0.                   (10)
```

If the convention permits `f=e`, then `X triangle {5}` is odd and is not in
`F(A)`.  Thus the symmetric-exchange axiom fails.

The unweighted matchability support of a graph and a valuation-leading
support may retain delta-matroid structure.  Exact nonvanishing after complex
cancellation does not.

## The bosonic replacement

The block-square-zero theorem gives the correct universal identity:

```text
M=exp(Omega),
log M=Omega,
Omega=sum_(i<j) B_ij.                                 (11)
```

All higher connected square-zero cumulants vanish, but the four-point
relation is the all-plus hafnian equation (1), not a spinor Pluecker
relation.  At six points the replacement is

```text
h_6-sum_(2+4 partitions) h_2 h_4
   +2 sum_(2+2+2 partitions) h_2 h_2 h_2=0.           (12)
```

This distinction matters at the active frontier.  A fixed layer of scalar
principal cofactors can be locally independent; (12) becomes restrictive
only when the root/mixed-jet equations force a partition-closed family
containing several deletion depths or retain mixed-colour tensor values.

## Literature boundary

Pfaffian Wick relations cut out the spinor variety and have a
delta-matroid-valued tropical counterpart; see Rincon
([arXiv:1004.4950](https://arxiv.org/abs/1004.4950)).  Matchgate identities
give the relevant planar Pfaffian signature characterization; see
Cai--Gorenstein
([arXiv:1303.6729](https://arxiv.org/abs/1303.6729)).  Those are genuine
theorems for their fermionic class.  Theorems 1--2 show exactly why their
sign and support conclusions do not transfer to generic bosonic hafnians.

Hirota's hafnian overlay identities provide a closer bosonic analogue: the
Pfaffian four-terminal defect becomes a difference of two hidden overlay
classes rather than zero.  Such an identity can become useful only after
the GHZ zero coefficients kill or identify those classes.  Without that
extra input it supplies no relation among the four visible hafnian products.

## Verification

Run:

```text
uv run --with sympy python claims/arbitrary-order/verify_bosonic_hafnian_spinor_no_transfer.py
python claims/arbitrary-order/audit_bosonic_hafnian_spinor_no_transfer.py
```

The primary verifier checks the generic four-point defect, the exact
six-vertex sign contradiction, and every hafnian in the delta-matroid
counterexample.  The independent audit reconstructs the same contradiction
and exchange failure using only integer arithmetic and a separately written
hafnian recursion.
