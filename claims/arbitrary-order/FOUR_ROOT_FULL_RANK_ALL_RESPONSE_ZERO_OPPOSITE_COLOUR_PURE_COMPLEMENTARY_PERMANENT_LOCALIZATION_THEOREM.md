# Four-root full-rank all-response-zero opposite-colour pure complementary-permanent localization

## Status

**Proved exact characteristic-zero localization on the full-rank residual-edge
chart; the localized witness branch remains open.**  Start with an actual
hypothetical ternary GHZ witness whose maximum-cardinality torus root has order
four and surplus two.  Fix the same residual pair \(Q\) supplied by GLS4 and
assume that its physical edge block \(H_Q\) has rank three.  If all six
same-\(Q\) physical pair-response tensors vanish identically, then every direct
edge among the four complementary ports is zero.  The two families of
\(Q\)-to-port blocks have one common nonempty support of size one or two.  On
that support their residual-side factors are coordinate covectors; in the
two-port case their coefficients have the forced opposite-sign normal form.
The physical four-port response then vanishes automatically.

Projecting the **complete** contracted GHZ tensor identity away from those two
residual coordinate factors excludes the equal-coordinate case.  In the only
surviving case the two factors use different colours, and the complementary
permanent \(\Pi_Q\) is forced onto the pure tensor line of the third colour.
The corresponding complementary \(2\) by \(2\) projection of \(H_Q\) is forced
onto the same third-colour line.  No response coordinate, residual
contraction, raw companion, nuisance minor, selector denominator, or
exceptional rank factor is divided away.

This theorem does **not** exclude the resulting opposite-colour pure-\(\Pi_Q\)
locus.  An exact maximum-root physical graph below realizes that locus,
the corank quota, nonzero raw incidence, and all seven response zeros, but one
displayed complete mixed coefficient equals one.  Thus the control is not a
witness and is not a counterexample.  The divisor \(\det H_Q=0\), every
nonzero-response pure-absorption branch, the supply-and-target-attachment
strategic node, and all downstream detector, permanent, extraction, and gluing
obligations remain **OPEN**.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## 1. Source, labelled tensor convention, and complete target identity

Work over a field \(K\) of characteristic zero.  In particular, \(K\) is
infinite.  Every vertex \(v\) has a fixed ternary space \(V_v=K^3\), with
target-coordinate covectors

~~~text
e_(v,0)^*, e_(v,1)^*, e_(v,2)^*.                     (1)
~~~

For distinct vertices \(v,w\), let

~~~text
W_vw in V_v^* tensor V_w^*                           (2)
~~~

be the physical edge block, with the reversed orientation understood by
transposing labelled slots.  A torus root is a set \(S\) with vectors
\(z_v\in(K^*)^3\), \(v\in S\), such that

~~~text
W_vw(z_v,z_w)=0                    for v!=w in S.      (3)
~~~

Let

~~~text
Omega=R disjoint-union B,       |R|=4,       |B|=6,   (4)
~~~

and assume that \((R,x_R)\) is a maximum-cardinality fully supported torus
root.  Thus no five-vertex torus root exists anywhere in \(\Omega\).  For each
\(u\in B\), put

~~~text
L_u(z)=(W_ru(x_r,z))_(r in R) in K^4.                 (5)
~~~

For \(P\in\binom B2\), the complementary permanent tensor is characterized by

~~~text
Pi_P((z_u)_(u in B-P))
 =sum_(sigma:R -> B-P bijective)
    product_(r in R) W_(r,sigma(r))(x_r,z_(sigma(r))). (6)
~~~

All tensor slots below are labelled.  If \(S,T\) are disjoint labelled sets
and

~~~text
X in tensor_(v in S)V_v^*,       Y in tensor_(v in T)V_v^*,
~~~

write

~~~text
sh_(S,T)(X tensor Y) in tensor_(v in S union T)V_v^*  (7)
~~~

for the unique permutation which inserts each factor into its named vertex
slot.  This **canonical shuffle** has coefficient one: there is no averaging,
sign, factorial, or unlabelled symmetrization.  We suppress `sh` only when the
labelled slots make it unambiguous.

Assume that the graph tensor is the ternary GHZ target.  Contracting the four
root slots with \(x_R\) gives the complete six-slot equality

~~~text
sum_(P in binom(B,2)) sh_(P,B-P)(H_P tensor Pi_P)
 =sum_(c=0)^2 mu_c product_(v in B)e_(v,c)^*,
mu_0 mu_1 mu_2 !=0,                                  (8)
~~~

where \(H_P=W_P\) is the physical edge block on the pair \(P\).  Equation
(8) is one tensor equality, hence includes every pure and mixed outside
coefficient.  The nonzero scalars \(\mu_c\) are the nonzero GHZ pure weights
multiplied by the fully supported root coordinates.

GLS4 supplies a same-graph residual pair

~~~text
Q={q_0,q_1} subset B,         Pi_Q!=0.                (9)
~~~

Its stronger quotient-survival and raw-incidence conclusions remain part of
the source package but are not used in the proof below.  Put

~~~text
U=B-Q={u_0,u_1,u_2,u_3}.                              (10)
~~~

Write

~~~text
H=H_Q=W_(q0,q1),
A_u=W_(q0,u),       C_u=W_(q1,u),
B_uv=W_uv.                                              (11)
~~~

For \(u\ne v\), define the labelled products by

~~~text
(A_u boxtimes C_v)[a,b,s,t]=A_u[a,s] C_v[b,t],        (12)
~~~

where the slot order is \((q_0,q_1,u,v)\).  Thus the physical pair response
is the four-vertex hafnian tensor

~~~text
Z_uv=H boxtimes B_uv+A_u boxtimes C_v+A_v boxtimes C_u,
Z_uv[a,b,s,t]
 =H[a,b]B_uv[s,t]+A_u[a,s]C_v[b,t]+A_v[a,t]C_u[b,s].  (13)
~~~

For a covector \(a=\sum_c a_c e_c^*\), write

~~~text
supp(a)={c:a_c!=0}.                                    (14)
~~~

It is a **coordinate covector** when \(|\operatorname{supp}(a)|=1\).  For a
family of whole edge blocks, support means nonvanishing of the entire block,
not coordinate support.

## 2. Main theorem

### Theorem 1 (full-rank literal response-zero localization)

Under (1)--(13), assume

~~~text
det H!=0,                  Z_uv=0 for every {u,v} in binom(U,2). (15)
~~~

Then all of the following hold pointwise.

1. Every direct complementary-port edge is zero:

   ~~~text
   B_uv=0                              for u!=v in U.  (16)
   ~~~

2. The whole-block supports

   ~~~text
   X={u in U:A_u!=0},             Y={u in U:C_u!=0}   (17)
   ~~~

   agree.  Their common value \(T\) is nonempty and has

   ~~~text
   1<=|T|<=2.                                             (18)
   ~~~

3. If \(T=\{t\}\), there are indices \(i,j,a,b\in\{0,1,2\}\) and
   \(\alpha,\beta\in K^*\) such that

   ~~~text
   A_t=alpha e_(q0,i)^* tensor e_(t,a)^*,
   C_t=beta  e_(q1,j)^* tensor e_(t,b)^*.              (19)
   ~~~

4. If \(T=\{s,t\}\), there are indices \(i,j\), nonzero covectors
   \(\alpha_s\in V_s^*\), \(\alpha_t\in V_t^*\), and a scalar
   \(\tau\in K^*\) for which

   ~~~text
   A_s=e_(q0,i)^* tensor alpha_s,
   C_s=tau e_(q1,j)^* tensor alpha_s,
   A_t=e_(q0,i)^* tensor alpha_t,
   C_t=-tau e_(q1,j)^* tensor alpha_t.                 (20)
   ~~~

   At least one of \(\alpha_s,\alpha_t\) is a coordinate covector.

5. The physical six-vertex four-port response vanishes:

   ~~~text
   H_(Q union U)=0.                                    (21)
   ~~~

   This response is a conclusion, not an input.

6. The residual coordinate indices in (19) or (20) are distinct:

   ~~~text
   i!=j.                                               (22)
   ~~~

   Let \(k\) be the unique third colour.  Let

   ~~~text
   rho_i(e_i^*)=0,         rho_i(e_c^*)=e_c^* for c!=i,
   rho_j(e_j^*)=0,         rho_j(e_c^*)=e_c^* for c!=j. (23)
   ~~~

   Then a scalar \(\lambda\in K^*\) exists such that

   ~~~text
   (rho_i tensor rho_j)H
      =lambda e_(q0,k)^* tensor e_(q1,k)^*,

   lambda Pi_Q
      =mu_k product_(u in U)e_(u,k)^*.                 (24)
   ~~~

In particular, on \(D(\det H_Q)\), the literal all-seven response-zero branch
of GLS7 is contained in the union of the two support shapes (19)--(20), with
opposite residual colours and pure third-colour \(\Pi_Q\).  The theorem does
not assert that this remaining locus is empty.

## 3. Rank three kills every direct port block

Fix \(u\ne v\) and arbitrary vectors \(\xi_u\in V_u\),
\(\xi_v\in V_v\).  Evaluate (13) in the two port slots and write

~~~text
b=B_uv(xi_u,xi_v),
a_u=A_u(-,xi_u),       a_v=A_v(-,xi_v),
c_u=C_u(-,xi_u),       c_v=C_v(-,xi_v).               (25)
~~~

The response equation becomes an equality of \(3\) by \(3\) matrices:

~~~text
bH+a_u c_v^T+a_v c_u^T=0.                             (26)
~~~

If \(b\ne0\), then \(bH\) has rank three, while the other side is a sum of
two rank-at-most-one matrices and has rank at most two.  This contradicts
\(\det H\ne0\).  Hence \(B_{uv}(\xi_u,\xi_v)=0\) for every pair of vectors,
so \(B_{uv}=0\).  Since \(u,v\) were arbitrary, (16) holds.

Substitution into (13) leaves the exact cross relation

~~~text
A_u boxtimes C_v+A_v boxtimes C_u=0       for u!=v.   (27)
~~~

No coordinate of \(A_u,C_u\), and no minor other than \(\det H\), was
inverted in this step.

## 4. Whole-block support and the characteristic-zero sign constraint

First establish the nonemptiness needed by the support comparison.  If
\(X=\varnothing\), then all internal blocks on \(\{q_0\}\cup U\) are zero:
the \(q_0\)-to-\(U\) blocks are zero by definition, and the
\(U\)-to-\(U\) blocks are zero by (16).  Taking the all-ones vector at all
five vertices gives a five-vertex torus root, contradicting maximality of
\(R\).  The same all-ones construction on \(\{q_1\}\cup U\) excludes
\(Y=\varnothing\).  Thus both \(X\) and \(Y\) are nonempty before Lemma 2 is
applied.

### Lemma 2 (the two block-family supports agree)

The nonempty supports \(X,Y\) in (17) satisfy \(X=Y\).

#### Proof

Suppose \(u\in X-Y\), and choose \(v\in Y\).  Then \(u\ne v\).  The first
term \(A_u\boxtimes C_v\) in (27) is a nonzero simple product.  Therefore the
second term must also be nonzero, which would give \(C_u\ne0\), a
contradiction.  Thus \(X\subseteq Y\).  Interchanging the two residual
vertices gives \(Y\subseteq X\).  \(\square\)

### Lemma 3 (two active ports force four rank-one blocks)

If \(u,v\in T\) are distinct, then

~~~text
rank A_u=rank C_u=rank A_v=rank C_v=1.                (28)
~~~

#### Proof

Flatten (27) with row slots \((q_0,u)\) and column slots \((q_1,v)\).  The
first term is

~~~text
vec(A_u) vec(C_v)^T,                                  (29)
~~~

a nonzero rank-one matrix.  After row and column permutations, the second
term is a Kronecker product of \(A_v\) and \(C_u^T\), so its rank is

~~~text
rank(A_v) rank(C_u).                                  (30)
~~~

Equality in (27) therefore makes both ranks on the right equal to one.
Interchanging \(u,v\) and using the opposite flattening gives rank one for
\(A_u,C_v\).  \(\square\)

Assume now that \(|T|\ge2\).  Lemma 3 applies to every active port after
choosing any other active port.  Uniqueness of the factor lines of the
nonzero simple tensors in (27) then gives covectors
\(a\in V_{q_0}^*\), \(c\in V_{q_1}^*\),
\(\alpha_u\in V_u^*\), and scalars \(s_u,t_u\in K^*\), for every
\(u\in T\), such that

~~~text
A_u=s_u a tensor alpha_u,
C_u=t_u c tensor alpha_u.                             (31)
~~~

Indeed, for two active ports the equality of the two nonzero four-factor
simple tensors in (27) identifies the \(q_0\)-factor lines, the
\(q_1\)-factor lines, and, at each port, the local factor lines.  Equation
(27) then becomes

~~~text
s_u t_v+s_v t_u=0                 for u!=v in T.      (32)
~~~

Since every \(t_u\) is nonzero on this support stratum, defining
\(r_u=s_u/t_u\) is legitimate and (32) gives \(r_u=-r_v\).  If three active
ports \(u,v,w\) existed, then

~~~text
r_v=r_w,                  r_v=-r_w,                   (33)
~~~

so \(2r_v=0\).  Characteristic zero and \(r_v\ne0\) give a contradiction.
Thus \(|T|\ge3\) is impossible.  Together with the already proved
nonemptiness, \(|T|\) is one or two.  For two active ports, absorb \(s_u\)
into \(\alpha_u\), then absorb one common nonzero ratio into \(c\).  This
gives an opposite-sign normal form with common residual factor lines \(Ka\)
and \(Kc\).  Section 5 identifies those lines with coordinate lines and
retains the one unavoidable relative scalar \(\tau\) displayed in (20).  No
factorization claim from this paragraph is used on the singleton branch;
that branch is handled directly by Lemma 5 in Section 5.

## 5. Maximum-root coordinate forcing

The following elementary torus facts make every maximum-root extension
explicit.

### Lemma 4 (torus kernel of a noncoordinate covector)

Let \(\ell=\sum_c \ell_c e_c^*\ne0\).  If at least two \(\ell_c\) are
nonzero, then there is \(z\in(K^*)^3\) with \(\ell(z)=0\).

#### Proof

Choose a pivot \(m\) with \(\ell_m\ne0\).  Choose the other two coordinates
in \(K^*\) so that

~~~text
S=sum_(c!=m) ell_c z_c !=0.                            (34)
~~~

Such a choice exists because at least one other coefficient is nonzero and
an infinite field is not covered by the single forbidden affine hyperplane.
Set \(z_m=-S/\ell_m\).  Every coordinate is nonzero and \(\ell(z)=0\).
\(\square\)

### Lemma 5 (zero-free bilinear forms on the torus)

A nonzero bilinear form \(M\in(K^3)^*\otimes(K^3)^*\) has no zero on
\((K^*)^3\times(K^*)^3\) if and only if

~~~text
M=lambda e_i^* tensor e_j^*             for lambda!=0. (35)
~~~

#### Proof

A coordinate monomial is nonzero on the torus.  Conversely, suppose first
that \(M\) has at least two nonzero rows.  Choose \(y\in(K^*)^3\) outside the
two corresponding nonzero row hyperplanes.  Then \(My\) has at least two
nonzero coordinates.  Lemma 4, applied to the covector with coefficient
vector \(My\), supplies \(x\in(K^*)^3\) with \(x^TMy=0\).

If \(M\) has exactly one nonzero row and is not a coordinate monomial, that
row has at least two nonzero entries.  Lemma 4 supplies a torus vector \(y\)
in its kernel, and any torus \(x\) gives \(x^TMy=0\).  Thus only (35) is
zero-free.  \(\square\)

We now prove the remaining coordinate statements.  Section 4 already proved
that \(T=X=Y\) is nonempty.

Suppose \(T=\{t\}\).  The only possibly nonzero internal edge on
\(\{q_0\}\cup U\) is \(A_t\).  If \(A_t\) had a torus zero
\((z_{q_0},z_t)\), append the all-ones torus vectors at the other three ports.
This would be a five-root.  Lemma 5 therefore makes \(A_t\) a coordinate
monomial.  The same argument on \(\{q_1\}\cup U\) makes \(C_t\) a coordinate
monomial, proving (19).

Suppose \(T=\{s,t\}\), with factorization (31).  If \(a\) were
noncoordinate, Lemma 4 would give a fully supported \(z_{q_0}\in\ker a\).
Together with arbitrary, for example all-ones, torus vectors at all four
ports, it annihilates every internal edge of \(\{q_0\}\cup U\), again giving
a five-root.  Hence \(a\) is a coordinate covector.  The same argument makes
\(c\) coordinate.

Finally, if both \(\alpha_s,\alpha_t\) were noncoordinate, choose fully
supported \(z_s\in\ker\alpha_s\) and
\(z_t\in\ker\alpha_t\) using Lemma 4.  With the all-ones vector at \(q_0\)
and the inactive ports, every internal edge of \(\{q_0\}\cup U\) vanishes.
Thus at least one local factor is coordinate.  Finally write
\(a=\lambda_0e_{q_0,i}^*\), \(c=\lambda_1e_{q_1,j}^*\).  Absorb
\(\lambda_0\) into the two local factors.  The surviving relative scalar
\(\tau=\lambda_1/\lambda_0\ne0\), with the sign already fixed in Section 4,
gives exactly (20).  This completes (18)--(20).

## 6. The four-port response is derived, not assumed

Consider a perfect matching of the six labelled vertices \(Q\cup U\).  If it
uses the edge \(q_0q_1\), then the four ports must be paired by two
\(U\)-to-\(U\) edges.  If it does not use \(q_0q_1\), each residual vertex is
paired to a port and the two remaining ports use one \(U\)-to-\(U\) edge.
Every matching monomial therefore contains at least one block \(B_{uv}\),
which is zero by (16).  Summing the matching monomials proves (21).  No
four-port equation, selector, or response coordinate entered the earlier
argument.

## 7. Complete-target projection and the opposite-colour pure locus

Use the residual coordinate indices \(i,j\) from (19) or (20), and apply
\(\rho_i\) in the \(q_0\)-slot and \(\rho_j\) in the \(q_1\)-slot of (8).
The terms split exhaustively as follows.

1. The \(P=Q\) term becomes
   \((\rho_i\otimes\rho_j)H\otimes\Pi_Q\).
2. If \(P\subset U\), then \(H_P=B_{uv}=0\).
3. If \(P=\{q_0,u\}\), then \(H_P=A_u\), which is zero or has residual
   factor \(e_{q_0,i}^*\), so \(\rho_iA_u=0\).
4. If \(P=\{q_1,u\}\), then \(H_P=C_u\), which is zero or has residual
   factor \(e_{q_1,j}^*\), so \(\rho_jC_u=0\).

Thus the projected **complete** target equality is

~~~text
H' tensor Pi_Q
 =sum_(c notin {i,j}) mu_c
    (e_(q0,c)^* tensor e_(q1,c)^*)
      tensor product_(u in U)e_(u,c)^*,
H'=(rho_i tensor rho_j)H.                              (36)
~~~

The tensor \(H'\) is nonzero.  If it were zero, the matrix of \(H\) would be
supported in row \(i\) union column \(j\), and could be written

~~~text
H=e_(q0,i)^* tensor r+s tensor e_(q1,j)^*             (37)
~~~

for suitable covectors \(r,s\).  This has rank at most two, contrary to
\(\det H\ne0\).  Hence both factors on the left of (36) are nonzero, and its
flattening across \(Q\mid U\) has rank one.

If \(i=j\), the right side of (36) has two summands.  Their \(Q\)-side pure
tensors are linearly independent, and their \(U\)-side pure tensors are
linearly independent.  Its \(Q\mid U\) flattening therefore has rank two,
contradicting the left side.  This proves (22).

If \(i\ne j\), exactly one colour \(k\) remains in (36).  All four displayed
factors are nonzero.  Uniqueness of the two factor lines in a nonzero simple
tensor gives a scalar \(\lambda\in K^*\) satisfying (24).  The second equality
is deliberately written as

~~~text
lambda Pi_Q=mu_k product_(u in U)e_(u,k)^*            (38)
~~~

rather than silently dividing by \(\lambda\).  This completes the proof of
Theorem 1.  \(\square\)

## 8. Exact saturation and divisor ledger

The theorem has the following exact pointwise ledger.

1. **Full-rank chart.**  The only physical-block divisor inverted by the
   theorem is

   ~~~text
   det H_Q!=0.                                         (39)
   ~~~

   The complete divisor \(V(\det H_Q)\) remains open.  Nothing in the proof
   specializes to it.

2. **Declared source nonzeros.**  The witness supplies

   ~~~text
   mu_0 mu_1 mu_2!=0,                 Pi_Q!=0.         (40)
   ~~~

   In an affine ideal encoding, (40) means saturation by the scalar
   \(\mu_0\mu_1\mu_2\) and a cover by the coordinate opens
   \(D(\Pi_Q[\gamma])\).  There is no canonical single scalar representing
   nonvanishing of the whole tensor \(\Pi_Q\).

3. **Zero-block strata.**  Whole blocks outside \(X,Y\), all \(B_{uv}\), and
   the forbidden empty-family branches are handled as exact zero equations.
   They are not removed by saturation.

4. **Active support charts.**  Lemmas 2--3 are coordinate-free.  If the
   rank-one factorization is encoded in coordinates, each active-block locus
   is covered by a selected nonzero-entry chart.  Only those selected entries,
   equivalently the nonzero scalars \(s_u,t_u\), may be inverted on that chart.
   The opposite-sign equation (32) itself is polynomial.

5. **Characteristic.**  The bound \(|T|\le2\) uses only that \(2\ne0\).
   Characteristic zero makes this factor a unit; no exceptional
   characteristic is suppressed.

6. **Projected residual block.**  No minor of \(H'\) is saturated.  Its
   nonvanishing follows from \(\det H\ne0\).  Its rank-one third-colour form is
   a conclusion of (36), not a generic-rank assumption.

7. **Derived factor.**  The scalar \(\lambda\ne0\) in (24) is derived from
   equality of nonzero simple tensors.  Equation (38) is denominator-free.

8. **Unused gates.**  There is no saturation or division by a contracted
   residual scalar \(h=H_Q(z_Q)\), a raw \(p_{A,Q}(z_Q)\), a response
   coordinate, a nuisance or augmented minor, an alignment factor, a legal
   selector coefficient, or a target-module denominator.  Target nuisance
   ranks and their exceptional fibres are not invoked.

9. **Discrete target branches.**  The case \(i=j\) is contradicted exactly.
   The case \(i\ne j\) survives on the explicit pure-\(\Pi_Q\) locus (24); it
   is not divided away or claimed empty.

## 9. Exact sharpness controls

These controls distinguish each load-bearing hypothesis from the remaining
witness obligation.

### 9.1 The determinant divisor is essential

Let \(H=e_0^*\otimes e_0^*\), and choose arbitrary port covectors
\(\alpha_u,\beta_u\).  Put

~~~text
A_u=e_0^* tensor alpha_u,
C_u=e_0^* tensor beta_u,
B_uv=-(alpha_u tensor beta_v+beta_u tensor alpha_v).  (41)
~~~

In the labelled \((u,v)\) slots, the three terms in (13) cancel exactly, so
every \(Z_{uv}=0\).  All four \(A,C\) blocks may be active.  Thus the
rank-three hypothesis cannot be deleted from (16) or (18).  This is an
algebraic divisor control, not a maximum-root witness.

### 9.2 The singleton support is realizable

Take \(H=I_3\), every \(B_{uv}=0\), and only

~~~text
A_t=e_0^* tensor e_0^*,             C_t=e_1^* tensor e_1^* (42)
~~~

nonzero.  Every pair response vanishes because no pair contains two active
ports.  The sole edge in each relevant five-set is a nowhere-zero coordinate
monomial on the torus.  This realizes the local shape (19), but it is not
asserted to satisfy the complete target identity.

### 9.3 The two-port sign is sharp

Take \(H=I_3\), every \(B_{uv}=0\), and two active ports with

~~~text
A_s=e_0^* tensor alpha_s,       C_s=e_1^* tensor alpha_s,
A_t=e_0^* tensor alpha_t,       C_t=-e_1^* tensor alpha_t. (43)
~~~

The two cross terms for \(\{s,t\}\) cancel, and every other pair response is
zero.  Coordinate choices for \(\alpha_s,\alpha_t\) also block the two simple
five-root extensions used in Section 5.  This realizes (20) locally.

### 9.4 Characteristic two permits three active ports

Over a field of characteristic two, take \(H=I_3\), \(B_{uv}=0\), and, at
three or four active ports,

~~~text
A_u=e_0^* tensor alpha_u,       C_u=e_1^* tensor alpha_u. (44)
~~~

Every cross relation has coefficient \(1+1=0\).  Thus the
characteristic-zero sign step is sharp.

### 9.5 Maximum-root off-target fixture on the surviving pure locus

Work over \(\mathbb Q\), hence also over \(\mathbb C\).  Let

~~~text
R={r_0,r_1,r_2,r_3},
Q={q_0,q_1},                  U={u_0,u_1,u_2,u_3},     (45)
~~~

and take \(x_{r_a}=(1,1,1)\) for every root.  All unspecified blocks below
are zero, as are every root--root and every \(U\)-to-\(U\) block.  Every
listed root--outside block has root factor \(e_{r,0}^*\).  The nonzero
root--\(U\) blocks are

~~~text
W_(r0,u0)=e_(r0,0)^* tensor e_(u0,2)^*,
W_(r1,u0)=e_(r1,0)^* tensor e_(u0,0)^*,
W_(r2,u0)=e_(r2,0)^* tensor e_(u0,1)^*,

W_(r1,u1)=e_(r1,0)^* tensor e_(u1,2)^*,
W_(r2,u1)=e_(r2,0)^* tensor e_(u1,0)^*,
W_(r3,u1)=e_(r3,0)^* tensor e_(u1,1)^*,

W_(r2,u2)=e_(r2,0)^* tensor e_(u2,2)^*,
W_(r3,u2)=e_(r3,0)^* tensor e_(u2,0)^*,
W_(r3,u3)=e_(r3,0)^* tensor e_(u3,2)^*.               (46)
~~~

The nonzero root--\(Q\) blocks are

~~~text
W_(r0,q0)=e_(r0,0)^* tensor e_(q0,0)^*,
W_(r1,q0)=e_(r1,0)^* tensor e_(q0,1)^*,
W_(r2,q1)=e_(r2,0)^* tensor e_(q1,0)^*,
W_(r0,q1)=e_(r0,0)^* tensor e_(q1,1)^*.               (47)
~~~

On the outside graph put

~~~text
H_Q=sum_(c=0)^2 e_(q0,c)^* tensor e_(q1,c)^*=I_3,

A_(u0)=e_(q0,0)^* tensor e_(u0,0)^*,
C_(u0)=e_(q1,1)^* tensor e_(u0,0)^*,
A_(u1)=e_(q0,0)^* tensor e_(u1,1)^*,
C_(u1)=-e_(q1,1)^* tensor e_(u1,1)^*,                 (48)
~~~

with \(A_{u_2}=A_{u_3}=C_{u_2}=C_{u_3}=0\).

#### Exact incidence and companion checks

Let \(f_0,f_1,f_2,f_3\) be the root-row basis of \(K^4\).  Evaluating (46)--
(47) at the root vectors gives the following columns, listed in port-colour
order \(0,1,2\):

~~~text
L_(u0)=[f_1,f_2,f_0],        L_(u1)=[f_2,f_3,f_1],
L_(u2)=[f_3,0,f_2],          L_(u3)=[0,0,f_3],
L_(q0)=[f_0,f_1,0],          L_(q1)=[f_2,f_0,0].      (49)
~~~

Their ranks are

~~~text
3,3,2,1,2,2,                                           (50)
~~~

so the total outside corank is

~~~text
0+0+1+2+1+1=5<=6.                                     (51)
~~~

The root--\(U\) support has a unique perfect matching: \(u_3\) first forces
\(r_3u_3\), then \(u_2\) forces \(r_2u_2\), then \(u_1\) forces
\(r_1u_1\), and finally \(u_0\) forces \(r_0u_0\).  All four selected port
colours are two.  Therefore

~~~text
Pi_Q=product_(a=0)^3 e_(u_a,2)^*                     (52)
~~~

with coefficient one.

For \(A=\{r_1,r_2\}\) and
\(z_{q_0}=z_{q_1}=(1,1,1)\), the residual incidence matrix is

~~~text
[[1,0],
 [0,1]],                                               (53)
~~~

so

~~~text
p_(A,Q)(z_Q)=1,                 H_Q(z_q0,z_q1)=3.     (54)
~~~

This verifies the displayed raw-incidence and common-contraction values.  It
does not verify GLS4 quotient survival modulo every higher column.

#### Exact maximum-root check

Every block in (46)--(48), except the deliberately ignored three-term block
\(H_Q=I_3\), is a nonzero coordinate monomial and is therefore nowhere zero
on the two endpoint tori.  Its nowhere-zero monomial subgraph contains the
following vertex-disjoint clique cover of all ten vertices:

~~~text
{r_2,u_2},        {r_3,u_3},
{r_0,q_1,u_0},    {r_1,q_0,u_1}.                      (55)
~~~

For the two triples, all three required edges occur respectively in
(46)--(48).  Additional monomial edges between the displayed cliques only
strengthen the bound.  A torus root can contain at most one vertex from each
covering clique, so it has size at most four.  Since all root--root blocks are
zero, \(R\) itself is a four-vertex torus root.  Hence \(R\) is
maximum-cardinality exactly.

#### Response and projected-target checks

The active \(Q\)-to-\(U\) blocks in (48) have the sign normal form (20) with

~~~text
i=0,             j=1,             k=2.                (56)
~~~

Every \(B_{uv}\) is zero, so all six pair responses vanish exactly; Section
6 then gives the four-port response zero.  Moreover

~~~text
(rho_0 tensor rho_1)H_Q
 =e_(q0,2)^* tensor e_(q1,2)^*.                       (57)
~~~

Together with (52), this realizes the surviving projected equality (24) with
\(\lambda=\mu_2=1\).

The graph is nevertheless off the complete target locus.  At the mixed
outside word, in slot order \((q_0,q_1,u_0,u_1,u_2,u_3)\),

~~~text
(0,0,2,2,2,2),                                        (58)
~~~

the \(P=Q\) summand of (8) is

~~~text
H_Q[0,0] Pi_Q[2,2,2,2]=1.                             (59)
~~~

Every \(P\subset U\) summand is zero because \(B_{uv}=0\).  Every cross-pair
summand is zero because the active \(A,C\) port coordinates in (48) are zero
or one, while all four port colours in (58) are two.  Thus the complete mixed
coefficient is exactly one instead of zero.  The fixture is not a hypothetical
witness, not an exact countermodel to Krenn--Gu, and not a proof that the
surviving pure locus meets the witness locus.

## 10. Proof-DAG consequence and exact open boundary

The source implication proved here is

~~~text
actual four-root maximum-root surplus-two witness
  + GLS4 pair Q
  + det H_Q!=0
  + all six pair responses identically zero
 -> all U-U blocks zero
 -> common Q-U support of size one or two
 -> four-port response identically zero
 -> opposite residual colours i!=j
 -> Pi_Q pure in the third colour and projected H_Q on the same line.
                                                               (60)
~~~

The exact status ledger is

~~~text
B_uv=0 on det H_Q!=0:                                  PROVED;
common support T with 1<=|T|<=2:                       PROVED;
maximum-root residual-coordinate forcing:             PROVED;
four-port response zero derived from pair zeros:       PROVED;
equal residual colour i=j:                             EXCLUDED;
opposite-colour pure-Pi_Q localization:                PROVED;
det H_Q=0 response-zero divisor:                       OPEN;
opposite-colour pure-Pi_Q witness locus empty:         OPEN;
nonzero-response desired/pure absorption branches:     OPEN;
legal useful target row on every four-root witness:    OPEN;
supply-and-target-attachment strategic node:           OPEN;
global Krenn--Gu conjecture:                           UNRESOLVED. (61)
~~~

The smallest remaining obligation inside this response-zero leaf is a
same-graph, target-coupled identity showing that the other companion tensors
in (8) cannot cancel all mixed coefficients on the locus (24), or else an
exact physical point on that locus satisfying **every** coefficient of (8).
The maximum-root fixture proves that maximum-root incidence, the corank quota,
raw \(p\), nonzero \(h\), and the isolated projected target equation do not
provide that identity.  The separate nonzero-response absorption leaves need
a different argument involving their complete nuisance modules and all
exceptional rank-drop fibres.

## 11. Verification, provenance, and dependencies

The written proof is support-free and valid for every point satisfying its
quantified hypotheses.  The focused exact verifier replays the rank-three
response identities, both support normal forms, the projection ranks, and all
fixture coefficients.  The independent no-import audit reconstructs the
shuffle tensors, flattenings, permanent, maximum-root clique bound, and mixed
coefficient through a separate representation.  Neither finite replay is the
proof of the arbitrary-point implication; that implication is the written
argument in Sections 3--7.

Run from repository root:

```powershell
python claims/arbitrary-order/verify_four_root_full_rank_all_response_zero_opposite_colour_pure_complementary_permanent_localization.py
python -I claims/arbitrary-order/audit_four_root_full_rank_all_response_zero_opposite_colour_pure_complementary_permanent_localization.py
python -m py_compile claims/arbitrary-order/verify_four_root_full_rank_all_response_zero_opposite_colour_pure_complementary_permanent_localization.py claims/arbitrary-order/audit_four_root_full_rank_all_response_zero_opposite_colour_pure_complementary_permanent_localization.py
```

Provenance: this theorem was derived on 2026-08-20 as a support-free attack on
the literal response-zero leaf left by GLS7 and the pointwise one-row failure
reduction.  The key new observation is that the **uncontracted** rank-three
block \(H_Q\), rather than a scalar contraction \(h\), makes each direct
\(U\)-to-\(U\) block vanish before any support analysis.  No external
literature premise is used.

Dependencies and boundary records:

- [maximum torus-root saturation and coordinate absorption](MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md)
- [GLS4 same-pair quotient survival and complementary-permanent dominance](MAXIMAL_ROOT_SURPLUS_TWO_SAME_PAIR_QUOTIENT_SURVIVAL_AND_COMPLEMENTARY_PERMANENT_DOMINANCE_THEOREM.md)
- [GLS7 four-root all-seven source cover](FOUR_ROOT_MAXIMAL_ROOT_SUPPLY_TO_ATTACHMENT_TRICHOTOMY_AND_OBSERVABLE_NONSELECTOR_BOUNDARY_THEOREM.md)
- [GLS8 promoted one-target pointwise failure reduction](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md)
- [GLD7 pure-quotient rank-one attachment trichotomy](FIXED_Q_FULL_MODULE_TARGET_QUOTIENT_RANK_ONE_PURE_SURVIVAL_AND_SIX_PORT_ATTACHMENT_TRICHOTOMY_THEOREM.md)

This theorem changes only the full-rank subbranch of the literal response-zero
leaf.  It supplies no theorem about the nonzero-response absorption leaves and
no downstream attachment, restriction, permanent, extraction, or gluing
conclusion.
