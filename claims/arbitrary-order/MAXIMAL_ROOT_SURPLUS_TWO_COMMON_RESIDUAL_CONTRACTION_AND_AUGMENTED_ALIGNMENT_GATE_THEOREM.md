# Maximal-root surplus-two common residual contraction and augmented-alignment gate

## Status

**Exact characteristic-zero source corollary and pointwise linear-algebra
gate.** The same-pair theorem supplies a residual pair \(Q\) with both a
nonzero physical edge block \(H_Q\) and a nonzero raw two-root residual
permanent \(p_{A,Q}\), but it states their nonvanishing at slightly different
levels. The first result below shows that one fully supported contraction of
that same \(Q\) can be chosen so that

~~~text
h=H_Q(z_Q)!=0                 and                 p_(A,Q)(z_Q)!=0.   (1)
~~~

Thus, in the four-root case, the GLS4 source really does reach the nonzero
'h' and nonzero raw-'p' input of the paired-grade GLD2 ledger on one common
contraction.

The second result exactly classifies the *ambient* augmented-alignment gate.
For the six root-pair weights \(p\), the complementary-pair involution \(J\),
and the GLD2 direct-cofactor map

~~~text
mathcal U:K^6 -> T,
~~~

there are a scalar 'kappa' and a weight vector 'l' satisfying

~~~text
l-kappa p in ker mathcal U,          l^T Jp!=0          (2)
~~~

if and only if the following two failures do not occur simultaneously:

~~~text
p^T Jp=0,                     Jp in im mathcal U^*.     (3)
~~~

This is a pointwise statement at every rank of \(\mathcal U\); no
generic-rank specialization, minor division, or saturation is hidden in it.
A version with an arbitrary homogeneous legal-weight subspace
\(M\subseteq K^6\) identifies the further constant-selector obstruction
exactly: the functional \(l\mapsto l^T Jp\) must be nonzero on

~~~text
M intersect (Kp+ker mathcal U).                         (4)
~~~

The theorem does **not** prove that the legal-weight space \(M\) is nonzero,
that a GLD5/GLD7 response selector survives, that any physical response is
nonzero, or that the aligned equations have the required synchronized
nuisance and target-pure anchor package. It only closes two previously
implicit gates and localizes ambient augmented-alignment failure to the
explicit isotropic determinantal locus (3). It supplies no permanent
restriction and closes no extraction or gluing obligation. The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Common nonzero residual contraction on the GLS4 pair

Let \(K\) be a characteristic-zero field. Let \(Q=\{q_0,q_1\}\) be a pair
of ternary modes with fixed target-coordinate bases. Its fully supported
contraction torus is

~~~text
T_Q={(z_0,z_1) in V_(q0) x V_(q1):
     z_q[c]!=0 for q in Q and c=0,1,2}.                (5)
~~~

Let \(H_Q\in V_{q_0}^*\otimes V_{q_1}^*\) be a nonzero physical edge block.
For a root pair \(A=\{i,j\}\), let

~~~text
p_(A,Q)(z_0,z_1)
 =W_(i,q0)(x_i,z_0)W_(j,q1)(x_j,z_1)
  +W_(i,q1)(x_i,z_1)W_(j,q0)(x_j,z_0).                (6)
~~~

This is the raw residual permanent in GLS3, GLS4, and GLD2.

### Theorem 1 (common-contraction nonvanishing)

Assume

~~~text
H_Q!=0                         as a bilinear tensor,
p_(A,Q) is not the zero polynomial.                   (7)
~~~

Then there is one \((z_0,z_1)\in T_Q(K)\) such that

~~~text
H_Q(z_0,z_1) p_(A,Q)(z_0,z_1)!=0.                    (8)
~~~

In particular, every actual maximum-root surplus-two complex witness has a
GLS4-supplied same pair \(Q\), a root pair \(A\), and one fully supported
residual contraction satisfying (1).

### Proof

The two factors in (8) are nonzero polynomials in the six residual
coordinates by (7). Their product is nonzero because the polynomial ring is
an integral domain. Localizing at the product of the six coordinates is
injective, so the product remains a nonzero regular function on the torus
\(T_Q\).

A characteristic-zero field is infinite, and \(T_Q(K)\) is Zariski dense in
\(T_Q\). Hence a nonzero regular function on \(T_Q\) cannot vanish at every
\(K\)-point. Choose a point where the product is nonzero; both factors are
then nonzero there.

For an actual complex witness, GLS4 supplies \(Q,A\) with \(H_Q\ne0\) and
with \(p_{A,Q}\) nonzero at some fully supported point, hence nonzero as a
polynomial. The first assertion applies. \(\square\)

### Scope of the corollary

Theorem 1 synchronizes only the residual contraction. It does not imply

~~~text
P_S(H;z_Q)!=0
~~~

for any GLD pair or four-port target \(S\), and it does not turn the
function-field quotient functional used by GLS4 into a constant target
selector. Those are separate gates.

## 2. The complementary-pair form

Now specialize to four roots. Let

~~~text
R={1,2,3,4},             E=K^(binom(R,2))=K^6.        (9)
~~~

Use the root-pair basis \(e_A\), \(A\in\binom R2\). Define the
complementary-pair involution

~~~text
J e_A=e_(R-A).                                         (10)
~~~

We identify \(E\) with \(E^*\) using the coordinate pairing. Thus the GLD2
augmented weight is

~~~text
Omega(l,p)=<l,Jp>=sum_(A in binom(R,2)) l_A p_(R-A). (11)
~~~

In coordinates,

~~~text
<p,Jp>=2(p_12 p_34+p_13 p_24+p_14 p_23).             (12)
~~~

The factor two is retained. Characteristic zero ensures that the displayed
quadric is not silently changed by characteristic two.

Let \(T\) be any finite-dimensional \(K\)-space and let

~~~text
mathcal U:E -> T                                      (13)
~~~

be the direct-cofactor map in the paired-grade identity. The alignment
condition from GLD2 is

~~~text
mathcal U(l-kappa p)=0.                               (14)
~~~

No injectivity or generic-rank hypothesis is imposed on \(\mathcal U\).

## 3. Exact ambient augmented-alignment classification

### Theorem 2 (augmented-alignment gate)

Let \(p\in E\) be nonzero. The following are equivalent.

1. There are \(l\in E\) and \(\kappa\in K\) such that

   ~~~text
   mathcal U(l-kappa p)=0,             <l,Jp>!=0.     (15)
   ~~~

2. The functional \(l\mapsto\langle l,Jp\rangle\) is nonzero on

   ~~~text
   A_p=Kp+ker mathcal U.                               (16)
   ~~~

3. It is not the case that both

   ~~~text
   <p,Jp>=0,                         Jp in im mathcal U^*.
                                                               (17)
   ~~~

Equivalently, ambient augmented alignment fails exactly on the locus

~~~text
<p,Jp>=0
and
rank[mathcal U^T | Jp]=rank mathcal U^T.              (18)
~~~

Here (18) is written in arbitrary fixed bases. Its meaning is independent
of those bases.

### Proof

Condition (14) holds exactly when

~~~text
l=kappa p+k                    for some k in ker mathcal U.
                                                               (19)
~~~

As \(\kappa\) and \(k\) vary, the possible aligned vectors \(l\) are exactly
\(A_p\). This proves the equivalence of 1 and 2.

The functional \(\langle -,Jp\rangle\) vanishes on
\(A_p=Kp+\ker\mathcal U\) exactly when it vanishes both on \(p\) and on
\(\ker\mathcal U\). The first condition is

~~~text
<p,Jp>=0.                                             (20)
~~~

Finite-dimensional duality gives

~~~text
(ker mathcal U)^perp=im mathcal U^*.                  (21)
~~~

Hence vanishing on the kernel is exactly
\(Jp\in\operatorname{im}\mathcal U^*\). This proves 2--3. In a matrix
representation, membership of the column \(Jp\) in the column space of
\(\mathcal U^T\) is precisely the rank equality in (18). \(\square\)

### Dual failure certificate

On the failure locus there is a \(\phi\in T^*\) such that

~~~text
mathcal U^*(phi)=Jp,                 <p,Jp>=0.         (22)
~~~

Then every aligned \(l=\kappa p+k\) obeys

~~~text
<l,Jp>
 =kappa<p,Jp>+<k,mathcal U^*(phi)>
 =<mathcal U(k),phi>
 =0.                                                       (23)
~~~

Conversely, if every aligned \(l\) has zero augmented weight, (20)--(21)
produce (22). Thus (22) is an exact linear certificate on each point of the
failure locus, not merely a generic obstruction.

### Rank specializations

If \(\mathcal U\) is injective, then \(A_p=Kp\), so (15) exists exactly when

~~~text
<p,Jp>!=0.                                             (24)
~~~

Raw nonvanishing of \(p\) is strictly weaker. For example,

~~~text
p=e_12
~~~

is nonzero but satisfies \(\langle p,Jp\rangle=0\). It is also a legitimate
raw symmetric-product pattern: take the two root--residual incidence vectors
to be the first and second coordinate vectors. Their only nonzero two-root
permanent is \(p_{12}\).

At the other extreme, even when \(\langle p,Jp\rangle=0\), a kernel direction
\(k\in\ker\mathcal U\) with \(\langle k,Jp\rangle\ne0\) supplies (15) by
taking \(\kappa=0\) and \(l=k\). Thus nuisance-map rank drop can repair
isotropy; it must not be discarded by a generic injective calculation.

## 4. The legal-weight subspace

Theorem 2 allows every vector of six shore weights. A genuine GLD detector
may have a smaller homogeneous space of weights obtainable from constant,
synchronized, target-derived root-grade selectors after all prescribed
nuisance annihilations. Let that space, or any proposed exact substitute for
it, be

~~~text
M subset E.                                           (25)
~~~

The normalization of a nonzero selector is affine, but its pre-normalized
homogeneous solution space is linear. The statement below applies to that
homogeneous space. It does not assert that a proposed selector construction
really has image \(M\); that correspondence must be proved separately.

### Theorem 3 (legal-subspace augmented-alignment gate)

Let

~~~text
A_(p,M)=M intersect (Kp+ker mathcal U).               (26)
~~~

The following are equivalent.

1. There are \(l\in M\) and \(\kappa\in K\) satisfying (15).
2. There is an \(l\in A_{p,M}\) with
   \(\langle l,Jp\rangle\ne0\).
3. The covector \(Jp\) does not annihilate \(A_{p,M}\):

   ~~~text
   Jp notin (A_(p,M))^perp.                           (27)
   ~~~

Equivalently, failure is the coordinate-free incidence

~~~text
Jp in M^perp + (p^perp intersect im mathcal U^*).     (28)
~~~

### Proof

The alignment equation says exactly that
\(l\in Kp+\ker\mathcal U\). Requiring in addition \(l\in M\) gives (26), so
1 and 2 are identical statements. Item 3 is the definition of a linear
functional being nonzero on a subspace.

For the final formulation, finite-dimensional annihilator identities give

~~~text
(M intersect A_p)^perp=M^perp+A_p^perp,               (29)
A_p^perp=(Kp)^perp intersect (ker mathcal U)^perp
         =p^perp intersect im mathcal U^*.            (30)
~~~

Substitution into (27) proves (28). \(\square\)

### Consequence for the proof DAG

There are now three distinct gates, in order:

~~~text
GLS4 same-pair source:
  one common fully supported z_Q has h!=0 and p!=0;        PROVED;

ambient augmented alignment:
  failure iff (17), equivalently (18);                     PROVED;

legal constant-selector alignment:
  failure iff Jp annihilates M intersect (Kp+ker U);       PROVED CRITERION;

nontrivial legal-weight space M forced on every witness:   OPEN;
same-Q physical response nonvanishing:                     OPEN;
GLD5/GLD7 target-selector survival:                        OPEN;
synchronized zero-grade/direct companion and nuisance:    OPEN;
target-pure H_U anchor or replacement identity:            OPEN.       (31)
~~~

In particular, (18) is a smaller explicit exceptional locus to test against
the complete mixed target equations, but excluding it would still not prove
attachment unless the legal-weight and response/anchor gates are also
discharged. Conversely, an exact point on (18) is not a witness
counterexample; it is only an augmented-alignment obstruction until every
physical GHZ coefficient and all source hypotheses are checked.

## 5. Verification boundary

Run from repository root:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_common_residual_contraction_and_augmented_alignment_gate.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_common_residual_contraction_and_augmented_alignment_gate.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_common_residual_contraction_and_augmented_alignment_gate.py claims/arbitrary-order/audit_maximal_root_surplus_two_common_residual_contraction_and_augmented_alignment_gate.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_common_residual_contraction_and_augmented_alignment_gate.py claims/arbitrary-order/audit_maximal_root_surplus_two_common_residual_contraction_and_augmented_alignment_gate.py
```

The proofs are the torus-density argument and finite-dimensional annihilator
identities above. The focused exact verifier and the genuinely independent
standard-library no-import audit check the following finite statements by
different derivations:

1. the complement-pair matrix \(J\) and formula (12);
2. every rank of small rational maps \(\mathcal U:K^6\to K^t\), comparing
   direct kernel search with (17)--(18);
3. legal subspaces \(M\) with transverse, contained, and zero intersections
   in (26), comparing direct search with (27)--(28); and
4. the isotropic raw pattern \(p=e_{12}\) and a rank-drop repair direction.

Such a replay audits the six-dimensional linear algebra. It cannot verify
that a hypothetical witness supplies a nonzero legal-weight space \(M\), a
nonzero response, or any of the remaining physical target package.

Dependencies:

- [maximal-root surplus-two same-pair quotient survival and complementary-permanent dominance](MAXIMAL_ROOT_SURPLUS_TWO_SAME_PAIR_QUOTIENT_SURVIVAL_AND_COMPLEMENTARY_PERMANENT_DOMINANCE_THEOREM.md)
- [four-root paired-grade constant target selector and single-shore cleanness boundary](FOUR_ROOT_PAIRED_GRADE_CONSTANT_TARGET_SELECTOR_AND_SINGLE_SHORE_CLEANNESS_BOUNDARY_THEOREM.md)
- [four-root constant target-module selector quotient](FOUR_ROOT_CONSTANT_TARGET_MODULE_SELECTOR_QUOTIENT_AND_MAXIMUM_ROOT_SHARPNESS_THEOREM.md)
