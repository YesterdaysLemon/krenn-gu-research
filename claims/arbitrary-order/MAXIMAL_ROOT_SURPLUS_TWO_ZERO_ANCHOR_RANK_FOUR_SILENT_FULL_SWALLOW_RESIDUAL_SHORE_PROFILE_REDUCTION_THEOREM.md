# Maximum-root surplus-two zero-anchor rank-four silent full-swallow residual-shore profile reduction

## Status and scope

**Exact characteristic-zero arbitrary-root pointwise profile reduction.**  On
the zero-anchor full-swallow branch, nuisance rank four and a silent root deck
leave only two residual-shore profiles:

```text
omega=0,
q=0,
q,r_0,r_1,r_2 in B_Q^anc,
rank B_Q^anc=4
  => (dim A,dim C)=(0,0)
     or
     (dim A,dim C)=(1,1) with one common active residual label.  (1)
```

In the second case, after exchanging the two residual labels if necessary and
choosing generators of the two shore lines,

```text
a_0=a,       b_0=t b,       a_1=b_1=0,       t!=0, (2)
```

for nonzero shore vectors `a,b`.  The only residual--port columns are then

```text
a tensor Y_u(v)+t X_u(v) tensor b.                  (3)
```

Here `t` only records the chosen generator `b` of the right shore line; it
can be absorbed into that abstract generator without changing a physical
residual vector.

The already proved `GLS44` makes `q=0` automatic at every rank-four
full-swallow point, so (1)--(3) classify the complete surviving residual
shore boundary there.

The theorem covers arbitrary promoted-label domains and every incidence-rank,
shore-rank, deck, divisor, and residual-contraction fibre.  Its only scalar
separation is an explicit dense-branch polarization by `2`, legal in
characteristic zero.  No response, incidence minor, port vector, or nuisance
denominator is selected.

The theorem does not exclude either surviving profile and does not assert
that a rank-four family realizing one exists.  It does not supply a legal
selector, response or selected activity, synchronization, nuisance survival,
attachment anchor, receiver, or source cover.  Ranks five through nine, raw
escape, and nonzero-anchor branches remain open.  The strategic node and the
global Krenn--Gu conjecture remain **UNRESOLVED**.

This is `GLS45`.

## Dependencies and provenance

The owning interfaces are:

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md)
  for the promoted chart and legal-attachment boundary;
- [`GLS35`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RAW_ROOT_DECK_QUOTIENT_AND_OUTPUT_COEFFICIENT_SEPARATION_NO_GO_THEOREM.md)
  for the root companion `q`, scalar `p=epsilon_A(q)`, and full-swallow split;
- [`GLS36`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_INCIDENCE_IMAGE_COMMON_ROW_SILENCE_AND_LABELWISE_LIFT_SHARPNESS_THEOREM.md)
  for the complete incidence presentation `B_Q^anc=im sigma_Q`;
- [`GLS39`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_COMPLETE_PAIRWISE_DIAGONAL_FAMILY_RANK_BOUND_AND_MINIMAL_RAW_SWALLOW_EXCLUSION_THEOREM.md)
  for the unconditional full-swallow rank floor four; and
- [`GLS44`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FOUR_FULL_SWALLOW_NONZERO_DIAGONAL_ROOT_DECK_COMPLETE_EXCLUSION_THEOREM.md)
  for the integrated rank-four conclusion `q=p=0`.

`GLS40` identifies the one-dimensional rank-four excess when `q in Delta`,
but its transverse-cylinder theorem and the `GLS41` pure-core receiver are on
`D(p)`.  They cannot be imported on the surviving `q=p=0` fibre.

No external literature claim is used.  The new content is the complete
zero-root-deck shore-rank classification, fixed-factor diagonal-intersection
obstruction, and dense rank-one/rank-one polarization endgame.

## 1. Complete incidence setting

Let `K` have characteristic zero and put

```text
E=K^3 tensor K^3,
r_i=e_i tensor e_i,
Delta=span{r_0,r_1,r_2}.                            (4)
```

At one fixed but arbitrary residual contraction, write

```text
a_s=xi_0^s,                    b_s=xi_1^s,
X_u:V_u -> K^3,                Y_u:V_u -> K^3,

q=a_0 tensor b_1+a_1 tensor b_0.                   (5)
```

Set

```text
A=span{a_0,a_1},       C=span{b_0,b_1},
X=sum_u im X_u,        Y=sum_u im Y_u,              (6)
d_0=dim A,             d_1=dim C.
```

The complete `GLS36` components are

```text
sigma_(s,u)(v)
 =a_s tensor Y_u(v)+X_u(v) tensor b_s,              (7)

sigma_(u,v)(x tensor y)
 =X_u(x) tensor Y_v(y)+X_v(y) tensor Y_u(x)         (8)
```

for every residual label, every promoted label, every distinct pair of
promoted labels, and every vector in the indicated domains.  On `omega=0`,

```text
B=B_Q^anc=im sigma_Q.                               (9)
```

Assume the hypotheses in (1).  Every tensor in (7)--(8) has left factors in
`A+X` and right factors in `C+Y`.  Since `Delta subset B`, quotienting either
factor shows

```text
A+X=K^3,                  C+Y=K^3.                  (10)
```

This is a statement about complete aggregate image spans; it does not choose
one active port vector.

## 2. Two elementary lemmas

### Lemma 1 (zero root-deck shore-rank atlas)

If `q=0`, then

```text
(d_0,d_1) in
{(2,0),(0,2),(1,1),(1,0),(0,1),(0,0)}.             (11)
```

In the `(1,1)` profile, exactly one of the following occurs:

1. **dense:** both residual labels are nonzero on both shores;
2. **sparse:** only one common residual label is nonzero on both shores, as
   in (2).

#### Proof

Let

```text
A_0=[a_0|a_1],        C_0=[b_0|b_1],
J=[[0,1],[1,0]].
```

Then

```text
q=A_0 J C_0^T.                                      (12)
```

If `d_0=2`, the map `A_0:K^2->K^3` is injective, so (12) and `q=0` imply
`J C_0^T=0`, hence `C=0`.  Transposition gives `d_1=2 => A=0`.  This proves
(11).

For `(d_0,d_1)=(1,1)`, choose nonzero `a,b` and nonzero coefficient vectors
`lambda,mu in K^2` with

```text
a_s=lambda_s a,              b_s=mu_s b.
```

Equation (5) becomes

```text
q=(lambda_0 mu_1+lambda_1 mu_0) a tensor b.         (13)
```

If both entries of `lambda` are nonzero, (13) and `mu!=0` force both entries
of `mu` to be nonzero; this is the dense case.  If, say, `lambda_1=0`, then
`lambda_0!=0` and (13) gives `mu_1=0`, while `mu_0!=0`; only residual label
zero is active on both shores.  The other case follows by label exchange.
Choosing generators of the abstract shore lines and retaining the physical
residual vectors gives (2); no graph weight or residual label is rescaled.
`square`

### Lemma 2 (fixed-factor diagonal intersection)

For nonzero `a in K^3` and any subspace `V subset K^3`,

```text
dim((K a tensor V) intersect Delta)<=1.             (14)
```

If equality holds and the intersection is `K r_i`, then `a` is proportional
to `e_i` and `e_i in V`.

The transposed statement holds for `V tensor K b`.

#### Proof

Every nonzero tensor in `K a tensor V` has matrix rank one and column space
`K a`.  A nonzero diagonal rank-one matrix is a scalar multiple of exactly
one `r_i`.  Two distinct diagonal axes cannot have the same column line.
This proves (14) and the equality statement.  Transposition gives the mate.
`square`

## 3. One residual shore cannot vanish alone

### Lemma 3 (profiles `(2,0)` and `(0,2)` are empty)

The profiles `(2,0)` and `(0,2)` cannot satisfy (1).

#### Proof

Suppose `(d_0,d_1)=(2,0)`.  Then `C=0`, and (10) gives `Y=K^3`.  The
residual--port columns (7), over both residual labels and all promoted-domain
vectors, span

```text
A tensor Y=A tensor K^3 subset B.
```

This subspace has dimension six, contradicting `dim B=4`.  Transposition
excludes `(0,2)`. `square`

### Lemma 4 (profiles `(1,0)` and `(0,1)` are empty)

The profiles `(1,0)` and `(0,1)` cannot satisfy (1).

#### Proof

Suppose `(d_0,d_1)=(1,0)` and write `A=K a`.  Again `C=0` and `Y=K^3`, so
(7) spans

```text
K a tensor K^3 subset B.                            (15)
```

The space in (15) has dimension three and, by Lemma 2, meets `Delta` in
dimension at most one.  Therefore

```text
dim(Delta+K a tensor K^3)>=3+3-1=5,
```

contradicting `dim B=4`.  Transposition excludes `(0,1)`. `square`

## 4. Dense rank-one/rank-one shores are impossible

### Lemma 5 (dense `(1,1)` exclusion)

The dense alternative of Lemma 1 cannot satisfy (1).

#### Proof

Since all four residual vectors are nonzero, name the physical vectors
`a=a_0` and `b=b_0`.  There is one `t!=0` such that

```text
a_1=t a,                     b_1=-t b.              (16)
```

Indeed, the two residual shores are lines, and (5) says the two nonzero
proportionality scalars sum to zero.  This names actual physical vectors; it
does not rescale a residual label.

For any promoted label `u` and `v in V_u`, abbreviate
`x=X_u(v)`, `y=Y_u(v)`, and let `m_0,m_1` be its two residual columns (7).
Equations (7) and (16) give

```text
t m_0+m_1
 =2t a tensor y,

t m_0-m_1
 =2t x tensor b.                                  (17)
```

The displayed scalars are nonzero in characteristic zero.  Taking all port
values in (17) proves

```text
R:=K a tensor Y subset B,
S:=X tensor K b subset B.                           (18)
```

Equation (10) gives `dim X,dim Y>=2`.  If `dim Y=3`, then Lemma 2 gives

```text
dim(Delta+R)>=3+3-1=5,
```

contrary to `dim B=4`; similarly `dim X!=3`.  Hence

```text
dim X=dim Y=2.                                      (19)
```

Now `Delta+R subset B` and (19) force `dim(Delta intersect R)>=1`.  Lemma 2
therefore gives an index `i` such that, after rescaling `a`,

```text
a=e_i,                  e_i in Y,
R=span{r_i,e_i tensor y'},       y'_i=0,            (20)
```

where `y'!=0`.  The dimensions in (20) give

```text
B=Delta+R.                                          (21)
```

Applying the transposed argument to `S` gives an index `j` and `x'!=0` with

```text
b=e_j,                  e_j in X,
S=span{r_j,x' tensor e_j},       x'_j=0,
B=Delta+S.                                          (22)
```

The quotient `B/Delta` is one-dimensional.  Its two nonzero representatives
in (20) and (22) are therefore proportional modulo `Delta`.  Both
`e_i tensor y'` and `x' tensor e_j` have zero diagonal, so their proportional
difference can lie in `Delta` only if it is zero.  Equality of the resulting
nonzero decomposable tensors forces

```text
y' proportional e_j,              x' proportional e_i.  (23)
```

Since `y'` is independent of `e_i` and `x'` is independent of `e_j`, one has
`i!=j`.  Equations (20), (22), and (23) then give

```text
X=Y=span{e_i,e_j}.
```

But `A=K e_i subset X` and `C=K e_j subset Y`, contradicting both equalities
in (10). `square`

## 5. Complete profile consequence

### Theorem 6 (silent rank-four residual-shore profile reduction)

Under the hypotheses in (1), exactly the following profiles are not excluded:

```text
(d_0,d_1)=(0,0),

(d_0,d_1)=(1,1) sparse with one common active residual label. (24)
```

In the second profile, (2), (3), and

```text
K a+X=K^3,                  K b+Y=K^3               (25)
```

hold.

#### Proof

Lemma 1 gives the exhaustive atlas (11).  Lemmas 3 and 4 exclude the four
one-shore-zero profiles with a nonzero mate.  Lemma 5 excludes dense `(1,1)`.
This leaves precisely (24).  Formula (3) is (7) in the sparse normal form,
and (25) is (10). `square`

### Corollary 6.1 (complete rank-four full-swallow boundary)

Every zero-anchor rank-four full-swallow point has one of the two profiles
in (24), and lies on `q=p=0`.

#### Proof

`GLS44` gives `q=p=0`; Theorem 6 applies. `square`

## 6. Frontier and unresolved remainder

```text
rank-four q!=0 full swallow:                          EMPTY (GLS43/44);
rank-four q=0 with one shore rank two:                EMPTY;
rank-four q=0 with one shore zero and the other nonzero: EMPTY;
rank-four q=0 dense rank-(1,1):                       EMPTY;
rank-four q=0 residual-free profile (0,0):            OPEN;
rank-four q=0 sparse one-label profile (1,1):         OPEN;
ranks five through rank nine:                         OPEN;
raw escape / nonzero anchor:                          OPEN;
response / synchronization / nuisance / receiver:    OPEN;
arbitrary-r source cover / strategic-node closure:    OPEN;
global Krenn--Gu conjecture:                          UNRESOLVED.
```

In the residual-free profile, all nuisance columns come from the complete
distinct-label pair family (8).  In the sparse profile, (3) is present in
addition to (8).  Deciding whether either family can have image
`Delta+K w` is the smallest remaining rank-four incidence obligation.  Even
an incidence exclusion would not settle ranks at least five, raw escape, or
the original response/attachment/source gates.

## Verification boundary

Run the focused exact primary verifier:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_four_silent_full_swallow_residual_shore_profile_reduction.py
```

Run the genuinely independent no-import audit:

```text
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_four_silent_full_swallow_residual_shore_profile_reduction.py
```

The primary uses exact SymPy matrices to replay the shore-rank factorization,
fixed-factor intersection bound, dense polarization, and quotient-line
endgame.  The audit imports no project module or third-party package and uses
a separate exact elimination and finite-field classification.  The
arbitrary-domain characteristic-zero theorem is the written proof, not a
finite census.
