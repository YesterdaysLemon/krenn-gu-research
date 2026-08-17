# Fixed-Q contraction escape or function-field pure absorption dichotomy

## Status

**Exact characteristic-zero witness-locus generic-rank dichotomy.**  Fix one
ternary four-root hypothetical witness, one residual pair `Q`, and the full
uncontracted mixed GHZ equation.  Vary only the two fully supported residual
contractions.  If all seven physical responses are nonzero at one
contraction, then exactly one algebraic alternative holds:

1. every desired companion column survives the complete nuisance matrix over
   the contraction function field, and one common fully supported contraction
   has all seven pure quotient ranks equal to one; or
2. at least one target generically absorbs its desired column and all three
   pure target columns into the complete nuisance image.

The second branch is an exact finite obstruction test.  It supplies four
denominator-cleared polynomial nuisance identities for one named target.
It is **generic/function-field absorption**, not pointwise absorption at every
contraction: exceptional nuisance-rank-drop contractions may still admit a
selector.

This theorem refines the rank-one target quotient of
[`GLD7`](FIXED_Q_FULL_MODULE_TARGET_QUOTIENT_RANK_ONE_PURE_SURVIVAL_AND_SIX_PORT_ATTACHMENT_TRICHOTOMY_THEOREM.md)
and the maximal-rank synchronization theorem
[`GLD9`](FIXED_Q_MAXIMAL_NUISANCE_RANK_COMMON_CONTRACTION_SYNCHRONIZATION_THEOREM.md).
It does not exclude the generic-absorption branch, display a mixed target
coefficient, force `GLD3` activity, or imply a permanent restriction.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Full polynomial family

Let `K` be an infinite field of characteristic zero.  Fix one physical graph
and its complete uncontracted principal deck `H`, one residual pair
`Q={q0,q1}`, and four open ports `U`.  Assume that the full uncontracted graph
equation equals the GHZ target.  This polynomial identity is load-bearing; an
equation known only after one fixed contraction is insufficient.

Let

```text
T=(G_m)^6=Spec R,
R=K[z_(q,c)^{+-1}:q in Q, c=0,1,2],
F=Frac(R).                                                (1)
```

The six torus coordinates are the three nonzero coordinates of each
residual contraction.  Put

```text
F_7=binom(U,2) union {U}.                                 (2)
```

For `S in F_7`, use the complete fixed-`Q` module of `GLD5` and choose fixed
bases.  Write the complete nuisance coefficient slices as the columns of

```text
B_S(z) in Mat_(m_S x n_S)(R),                             (3)
```

and write the desired companion as `g_S(z) in R^(m_S)`.  No nuisance label
is removed.  The row dimensions are

```text
m_S=729 for |S|=2,             m_U=81.                    (4)
```

After the common fixed-`Q` evaluation-kernel compression, one uncompressed
coefficient-slice choice has `n_S=511*9=4599` for a pair and
`n_U=511*81=41391`; any fixed column compression with the same image is
equivalent.

Let

```text
D_S=[d_(S,0)|d_(S,1)|d_(S,2)] in Mat_(m_S x 3)(K),
P_S(H;z) in W_S tensor R,
r_S=rank_F B_S.                                           (5)
```

The columns of `D_S` are the three pure root/complement-port words.  Because
the uncontracted witness equation holds identically, the `GLD7` quotient
identity base-changes legally to `F`.

Assume that there is one point `z0 in T(K)` such that

```text
P_S(H;z0)!=0 for every S in F_7.                          (6)
```

Because the family is finite and `T(K)` is Zariski dense, (6) is equivalent to
every response tensor in (5) being a nonzero polynomial tensor.  Condition
(6) is the form naturally supplied by a proposed simultaneous swallowed-pure
point.

## 2. Exhaustive dichotomy

### Theorem 1 (common escape or generic pure absorption)

Under (1)--(6), exactly one of the following algebraic alternatives holds.

#### A. Common escape

For every `S in F_7`,

```text
rank_F[B_S|g_S]=r_S+1.                                   (7)
```

There is a nonempty Zariski-open `Omega subset T` such that every
`z in Omega(K)` satisfies, simultaneously for all seven targets,

```text
[g_S(z)]!=0,        P_S(H;z)!=0,        q_S(z)=1.          (8)
```

Thus one common fully supported contraction legally attaches the same
physical six pair tensors `D_uv` and four-port tensor `T` required by `GLD3`.

#### B. Function-field generic pure absorption

For at least one `S in F_7`,

```text
rank_F[B_S|g_S]=r_S.                                     (9)
```

For every such target, the full witness equation forces the stronger equality

```text
rank_F[B_S|g_S|D_S]=r_S.                                (10)
```

Equivalently, there are a nonzero Laurent polynomial `delta_S in R` and
vectors

```text
b_(S,g),b_(S,0),b_(S,1),b_(S,2) in R^(n_S)              (11)
```

such that

```text
B_S b_(S,g)=delta_S g_S,
B_S b_(S,c)=delta_S d_(S,c),        c=0,1,2.             (12)
```

After multiplying all terms by one Laurent monomial, `delta_S` and the
vectors in (11) may be taken in the ordinary polynomial ring.  On the
principal open `D(delta_S)`, the desired and all three pure columns are
pointwise nuisance-absorbed.

### Proof

Adjoining one column changes rank by zero or one.  Therefore either (7) holds
for all seven targets or (9) holds for at least one, and the two rank patterns
are mutually exclusive.

Assume (7).  For each `S`, choose a nonzero `r_S`-minor `Delta_S` of `B_S`
(take `Delta_S=1` if `r_S=0`) and a nonzero `(r_S+1)`-minor `A_S` of
`[B_S|g_S]`.  By (6), choose one fixed response coordinate `rho_S(z)` which
is nonzero at `z0`.  The Laurent polynomial

```text
Phi=product_(S in F_7) Delta_S A_S rho_S                 (13)
```

is nonzero because `R` is an integral domain.  Hence `Omega=D(Phi)` is a
nonempty open and has a `K`-point because `T(K)` is Zariski dense.  On
`Omega`, every nuisance rank is exactly `r_S`, every desired augmented rank
is `r_S+1`, and every selected response coordinate is nonzero.  The full
uncontracted witness identity contracts at every `z in T`.  Applying `GLD7`
to `[g_S(z)]!=0` and `P_S(H;z)!=0` proves `q_S(z)=1`, yielding (8).

Now assume (9) and work over `F`.  Quotient `L_S^* tensor F` by
`im_F B_S`.  Equality (9) says `[g_S]=0`.  The base-changed `GLD7` witness
identity is

```text
sum_(c=0)^2 alpha_c[d_(S,c)] tensor w_(S,c)
   =[g_S] tensor P_S(H)=0.                               (14)
```

Every `alpha_c=z_(q0,c)z_(q1,c)` is a unit in `F`, and the three pure port
words `w_(S,c)` are independent.  Therefore every `[d_(S,c)]` is zero,
proving (10).  Choose rational nuisance solutions for the four columns in
(10) and clear their finitely many denominators with one nonzero
`delta_S`.  Multiplying by a Laurent monomial removes negative exponents and
proves (11)--(12). `square`

### Corollary 1.1 (a swallowed point either escapes or persists generically)

If `z0` in (6) also satisfies `q_S(z0)=0` for all seven targets, then either
changing only the common contraction reaches the open all-seven rank-one
branch (8), or at least one named target satisfies the four-column
function-field absorption test (10).

Failure of every common escape implies the second alternative, but the
converse is false without controlling nuisance-rank-drop loci: a generically
absorbed target may survive at an exceptional contraction.

## 3. Response-zero exception

Without (6), the exact exhaustive statement has a third branch:

```text
C. P_S(H;z) is identically zero for at least one S.       (15)
```

If (7) holds for all seven targets and no response is identically zero, the
same principal-open proof gives (8).  Vanishing at one contraction is
harmless when another coordinate value makes the response polynomial
nonzero.  Only polynomial-identical zero prevents the open-intersection
argument.  This is why selector survival alone must not be called quotient
rank one.

## 4. Sharp formal controls

These controls are exact module families, not physical graphs or witnesses.

### 4.1 Pointwise swallowed but generically escapable

On `T=G_m`, take `L^*=K^2`, let `e1=(1,0)^T`, and set

```text
g=d_0=d_1=d_2=e1,
B_1(t)=(1,t-1)^T,
B_2(t)=(1,(t-1)^2)^T.                                   (16)
```

Take three independent pure output words and response equal to their sum, so
the abstract quotient identity is exact.  At `t=1`, both desired and all pure
columns are swallowed.  Over `K(t)`, each nuisance rank is one and each
desired augmented rank is two; every `t!=1` is a common escape.  Replicating
these two families gives exact seven- and thirty-one-target controls.

### 4.2 Generic absorption with exceptional escape

Take

```text
B(t)=[t-1],          g=d_0=d_1=d_2=[1].                  (17)
```

Over `K(t)`, `B` already spans the target line and (10) holds.  The identities
in (12) use `delta=t-1` and coefficient vector one.  At the exceptional point
`t=1`, however, the nuisance rank drops to zero and the desired and pure
classes survive.  Thus function-field absorption is not failure at every
specialization.

### 4.3 Identically zero response

Take `L^*=K^2`, `B=e1`, `d_c=e1`, `g=e2`, and `P=0`.  The desired class
survives but all pure classes vanish in the quotient, exactly as the
response-zero branch of `GLD7` permits.

## 5. Frontier and UNKNOWN remainder

```text
seven generic rank bits form an exhaustive dichotomy:     PROVED;
all seven generic survival bits give one common q=1 point: PROVED;
generic desired absorption forces three-pure absorption:  PROVED;
four denominator-cleared nuisance identities:             PROVED;
pointwise swallowed implies generic absorption:            FALSE;
generic absorption excludes exceptional escape:            FALSE;
generic absorption excluded on hypothetical witnesses:    UNKNOWN;
bounded mixed detector on the absorbed branch:             UNKNOWN;
GLD3 three-colour activity:                                UNKNOWN;
weighted permanent attachment:                            UNKNOWN;
global Krenn--Gu conjecture:                               UNRESOLVED.
```

The breadth is one fixed physical graph, one residual pair `Q`, all seven
four-root target modules, and the whole six-dimensional fully supported
contraction torus.  The depth is the complete `2079`-coordinate surplus-two
deck and every nuisance slice, with the full uncontracted target identity.
The good branch reconstructs the exact six `D_uv` tensors and `T` at one
common contraction.  The bad branch reconstructs no response; its obstruction
is one of seven exact function-field rank equalities and the four polynomial
identities (12).  There is no transition gauge.  The target implication is
conditional attachment or algebraic localization of the residual branch.
The permanent implication is none.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_fixed_q_contraction_escape_or_function_field_pure_absorption_dichotomy.py
python -I claims/arbitrary-order/audit_fixed_q_contraction_escape_or_function_field_pure_absorption_dichotomy.py
```

The primary verifier uses exact symbolic polynomial matrices to replay the
generic ranks, common principal-open products, exceptional specializations,
and denominator-cleared identities in (16)--(17), including seven- and
thirty-one-target copies.  The independent no-import audit uses integer
coefficient dictionaries, direct determinant formulas, and
`fractions.Fraction` specialization ranks.  These programs audit the bounded
controls; the integral-domain, base-change, and quotient proof is
load-bearing.
