# The remaining exterior-coupling obligation

This note records the next parent-level obligation after
[PSCL cycle localization](../../claims/arbitrary-order/PROTECTED_SCAFFOLD_FULL_BINARY_CYCLE_LOCALIZATION.md)
and the [PSCT exact two-sided control](../../claims/arbitrary-order/PROTECTED_SCAFFOLD_TWO_SIDED_BINARY_CYCLE_NO_GO.md).
The source identities below have direct algebraic proofs. The proposed
incompatibility lemma at the end is **OPEN**. Neither an identity nor its
finite diagnostic is a proof of FB, CSQ4, or Krenn--Gu. Global status remains
**UNRESOLVED**. The [parent record](full-binary-parent-attempt-2026-09-20.md)
fixes the common-star hypotheses, upstream supply, and downstream consumer.

## Setup and the two full cuts

Work over C with the actual same-support matrices A,B for one ordered
color pair a,b. Assume S1 and both types of S2, and suppose for contradiction
that every binary cut for this pair has its target value. PSCS excludes
singleton ports. Thus the directed support D is strongly connected with
minimum indegree and outdegree at least two. Its shortest directed cycle
C is proper and induced. By PSCL one binary resource R contains both
states of every cycle component. Write its physical shores as L_R,M_R.

Choose y in C. There is an extra in-neighbor x->y with x outside C,
since the only incoming cycle arc at y is from its predecessor. Put

```
T=C\{y},       Y=M_R\T,       W=M_R\C.
```

The full binary word with a exactly on T has source Z(T,Y): every other
resource selects right states only and contributes one. The first target
is therefore Z(T,Y)=0. T is nonempty and proper.

Recolor x from b to a. Its left state joins the same resource R. If its
right state lies outside R, removing it affects a resource still having
only right states. If it lies inside R, its column x disappears from R.
The second source is consequently Z(T union {x},Y) in the first case,
and Z(T union {x},Y\{x}) in the second. These are also mixed words:
|T union {x}|=|C|<k. No resource factor is divided out.

## Exact row and column occupation

For x outside P and z outside Q define

```
R_x(P,Q)=Z(P union {x},Q)-Z(P,Q),
C_z(P,Q)=Z(P,Q union {z})-Z(P,Q).
```

The two zero targets give the necessary equations

```
x notin M_R:  R_x(T,Y)=0;                                  (1)
x in M_R:     R_x(T,Y\{x})=C_x(T,Y\{x}).                    (2)
```

The second case is essential. Adding a physical component's left state
also removes its selected right state; treating that operation as only
adding a row would be wrong. Transposition gives the dual identities for
extra out-neighbors of cycle vertices.

For distinct j,k outside Q0 put

```
M_(k,j)(P,Q0)=sum_(I subset P, K subset Q0, |I|=|K|+1)
                 per(A[I,K union {k}]) per(B[I,K union {j}]).
```

Laplace expansion along the new row in both permanent factors yields

```
R_x(P,Q)=sum_(j in Q) q_xj Z(P,Q\{j})
 +sum_(j,k in Q, j!=k) A_xj B_xk M_(k,j)(P,Q\{j,k}).       (3)
```

To prove (3), expand the part of Z(P union {x},Q) whose selected row set
contains x. When the two permutations assign the same column j to x,
the common factor is q_xj and the remaining row and column sets agree.
When their assigned columns differ, the A cofactor retains k and the B
cofactor retains j; removing both leaves the common set K. These are all
cases, each counted once. In particular, the mixed cofactors are actual
polynomials in the same A,B, not independently chosen exterior data.

In the case x notin M_R, Y={y} union W. Apply PSCL in the reverse
orientation to its proper cycle subset T:

```
Z(T,W)=(-1)^|T| product_(v in T) q_(v,succ(v)) != 0.
```

The j=y term in (3) is therefore nonzero. Equation (1) becomes

```
0 = q_xy (-1)^|T| product_(v in T) q_(v,succ(v))
  + sum_(j in W) q_xj Z(T,({y} union W)\{j})
  + sum_(j!=k in {y} union W)
        A_xj B_xk M_(k,j)(T,({y} union W)\{j,k}).           (4)
```

The nonzero first term alone is insufficient for a contradiction. The
remaining terms can have arbitrary complex signs and phases. In the
case x in M_R, (2) must also retain the column-occupation contribution;
(4) is not silently used for that case.

## What the third color supplies

Let c be the third color. For exterior component z, let alpha_z,beta_z
be the actual factors of the (a,c) gadget from x to z, and gamma_z,delta_z
the factors of the (b,c) gadget from y to z, using zero for absent labels.
Set

```
H_xy=sum_z alpha_z beta_z gamma_z delta_z,
X_xy=sum_z alpha_z delta_z,      Y_xy=sum_z beta_z gamma_z.
```

The proved distinct-color S2 identity is

```
q_xy=2 H_xy-X_xy Y_xy.                                      (5)
```

Substitution into (4) is valid without division. It does not itself relate
these third-color contractions to the mixed binary cofactors M_(k,j).
The support rule assigns different labels to their noncentral edges; it
does not identify their factor values. No factorization, sign inequality,
or vanishing of the remainder in (4) has been proved.

Shortest-cycle minimality removes noncycle arcs inside C by creating a
shorter directed cycle. The mixed terms in (4) also use edges from C to
W and from x to W; minimality does not delete those entries. PSCT has a
shortest induced triangle and nonzero mixed terms, so minimality alone
cannot justify dropping this part of the expansion.

There is also local freedom in (5). With two fresh common c-neighbors and
center factors one, let the leaf factors be p_1,p_2 at x and h_1,h_2 at y.
Then 2H-XY=(p_1-p_2)(h_1-h_2). For a prescribed nonzero q_xy choose

```
p_1=(-1+u)/2,       p_2=(-1-u)/2,
h_1=(-1+q_xy/u)/2, h_2=(-1-q_xy/u)/2,
```

where u avoids 0,1,-1,q_xy,-q_xy. Both port sums are -1, all four factors
are nonzero, and (5) holds. This observation supplies only these two local
port sums and one distinct-color row; it does not supply S1/S2 at the new
neighbors or across the entire array. It shows why a single edge equation
cannot identify the binary mixed cofactors. A successful bridge must use
the global compatibility of the third-color equations.

## Sharp control and an explicitly sufficient open lemma

In PSCT, choose C={0,1,2}, y=2, x=3. Then T={0,1}, W={5,6} and Y={2,5,6}.
The right state of x is outside the cycle resource, so (1) applies.
The base source F({0,1}) is zero but

```
R_3({0,1},{2,5,6})=F({0,1,3})-F({0,1})=(r^2+1)/(12r)!=0.
```

Thus both cycle faces and every binary singleton/double target do not imply
the additional equation (4). PSCT has no third-color supply, so it does
not refute a route using (5). Its failure is an explicit challenge for that
route, not a counterexample to the full parent.

One sufficient next proposition is the following; it is not claimed to
be necessary or equivalent to FB.

> **Exterior-coupling lemma (open).** For every common-star array over C
> satisfying S1 and both same-color and distinct-color S2, fix a color pair
> whose directed support is strongly connected. Let C be a shortest proper
> directed cycle with both states in one binary resource, and assume the
> two opposite PSCL exterior cycle systems. Then some extra in-neighbor
> or out-neighbor of a vertex of C violates (1) or (2), or their transposed
> versions, according to which resource contains its other color state.

A full FB array supplies every hypothesis of this lemma, while its full
binary targets supply (1) and (2) for every such neighbor. A proof of the
lemma would therefore prove FB. It would still require a separate bridge
from general protected arrays or arbitrary witnesses before resolving
Krenn--Gu. An exact array satisfying all the lemma's hypotheses and all
these added equations would refute this sufficient route, even if it
failed a later binary word. Neither outcome is established here.

The bounded analytic attempt reached this unresolved bridge. Reversing
the color orientation adds a second family of actual mixed cofactors;
no identity combining the two families with all third-color rows was
obtained. In the case where x's right state is also in R, removing its
column additionally prevents replacing Z(T,W\{x}) by the PSCL value for
Z(T,W). No exact control satisfying the full three-color hypotheses of
the proposed lemma has been constructed. These are the present obstacles,
not evidence that the lemma is true or false.

The [independent assessment](../audits/COMMON_STAR_EXTERIOR_COUPLING_REVIEW_2026-09-20.md)
separates the exact identities from this unproved implication.
