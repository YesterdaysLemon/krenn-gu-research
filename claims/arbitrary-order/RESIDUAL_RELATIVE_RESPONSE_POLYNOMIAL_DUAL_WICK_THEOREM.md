# Residual-relative response polynomials and the dual-Wick theorem

## Status

**Exact arbitrary-even-residual characteristic-zero theorem.**  The common
cofactor--Gram identity is only the quadratic layer of a finite residual
response polynomial.  Let `U` be any finite set of scalar boundary ports and
let `Q` be an even residual set of order `q`.  After contracting all already
fixed vector modes, write

```text
B_uv      for a port--port edge,
R_pu      for a residual--port incidence,
A_pq      for a residual--residual edge.                (1)
```

Fix `U` to be a transversal chart containing at most one chosen scalar
coordinate from each physical port.  Within that chart, the square-zero
relation enforces that no physical vertex is used twice.  Keeping several
colours of one port simultaneously requires the block ideal
`x_(i,a)x_(i,b)=0`, as in the block-square-zero theorem.

If `M_B` is the full principal-hafnian moment family of `B` and `Z_Q` is the
family obtained with every residual vertex present, then

```text
Z_Q = M_B Phi_(A,R),
degree Phi_(A,R) <= q.                                  (2)
```

The coefficient of port set `S`, where `|S|=2t<=q`, is

```text
[x_S] Phi_(A,R)
 =sum_(T subset Q, |T|=|S|)
      haf(A[Q minus T]) per(R_(T,S)).                   (3)
```

Thus the constant layer is `haf(A)`, the quadratic layer is the common
cofactor--Gram response, and every deeper layer is an exact permanental
compound of the same incidence matrix weighted by the higher principal
hafnian cofactors of `A`.

For `q=2`, (2) has no hidden higher layer:

```text
Phi_(A,R)=h+Q_K,
K_uv=a_u b_v+b_u a_v.                                  (4)
```

Equivalently, after subtracting the direct term, the entire all-subset
response is one tangent vector to the Wick moment variety.  This gives a
complete dual-number cumulant criterion and explicit four-/six-point
compatibility equations below.

This is a local-to-global **test**, not a proof of the Krenn--Gu conjecture.
It constrains a synchronized family of principal deletion responses.  A
single top-order `P_5`, `P_6`, or `P_7` equation does not expose that family,
and the known coordinate-monomial and all-full-span boundary constructions
pass the criterion.  The global conjecture remains **UNRESOLVED**.

## Vertex-exclusive response algebra

Work in the commuting square-zero algebra

```text
Z_(U,Q)=C[x_u,y_p:u in U,p in Q]/(x_u^2,y_p^2).        (5)
```

Put

```text
Q_B=sum_(u<v) B_uv x_u x_v,
Q_R=sum_(p in Q,u in U) R_pu y_p x_u,
Q_A=sum_(p<r) A_pr y_p y_r.                            (6)
```

The vertex-exclusive Wick exponential is

```text
E=exp(Q_B+Q_R+Q_A).                                    (7)
```

Because every variable is square-zero, the coefficient of a square-free
monomial is exactly the weighted perfect-matching sum on its vertex set.
Define

```text
M_B(x)=exp(Q_B)
      =sum_(S subset U) haf(B[S]) x_S,

Z_Q(x)=[y_Q]E
      =sum_(S subset U) haf(G[S union Q]) x_S.          (8)
```

Here an odd-order hafnian is understood to be zero and the empty hafnian is
one.  The constant term of `M_B` is one, so it is invertible in the finite
square-zero algebra.

### Theorem 1 (residual-relative factorization)

Equations (2)--(3) hold, with

```text
Phi_(A,R)=[y_Q] exp(Q_A+Q_R)=M_B^(-1) Z_Q.             (9)
```

Proof.  The three quadrics commute, hence

```text
E=exp(Q_B) exp(Q_A+Q_R).
```

Taking `[y_Q]` gives (9) and (2).  To obtain `[x_S y_Q]` from the second
factor, every port in `S` must use one cross edge to a distinct residual
vertex.  Let `T` be the residual vertices used this way.  Necessarily
`|T|=|S|`; summing their bijections to `S` gives `per(R_(T,S))`, while the
remaining residual vertices contribute `haf(A[Q minus T])`.  Summing over
`T` proves (3).  Since `T subset Q`, no port degree greater than `q` occurs.
This is a matching partition by the cross-residual set, not a matching
enumeration.

The first three layers are therefore

```text
[1] Phi = h=haf(A),

[x_u x_v] Phi
 =sum_(p<r) haf(A[Q minus {p,r}])
    (R_pu R_rv+R_pv R_ru)
 =R_u^T C(A)R_v,                                      (10)

[x_(u1)...x_(uq)] Phi=per(R_(Q,S))       when |S|=q.  (11)
```

Equation (10) recovers the corrected two-port theorem exactly, including its
common middle matrix and without a factor of two.  Equation (3) supplies all
of the deletion compatibility omitted at quadratic order.

### The simultaneous permanental-compound lift

For each even `2t<=q`, index rows by `2t`-subsets `T` of `Q` and columns by
transversal `2t`-subsets `S` of `U`.  Define

```text
c_T^(2t)(A)=haf(A[Q minus T]),
P_(2t)(R)_(T,S)=per(R_(T,S)).
```

Then the entire degree-`2t` response layer is the row-vector product

```text
Phi^(2t)=c^(2t)(A) P_(2t)(R).
```

The matrices `P_(2t)(R)` are **permanental/zeon compounds**, not exterior
compounds.  Ordinary Pluecker signs and Grassmannian equations cannot be
imported.  The actual constraint is that every degree comes from one common
incidence matrix `R` and the nested principal-hafnian tower of one common
`A`.  At `q=4`, `Phi^4=P_4(R)`; at `q=6`,

```text
Phi^4_S=sum_(|T|=4) A_(Q minus T) per(R_(T,S)),
Phi^6_S=per(R_(Q,S)).
```

This synchronized lift is the information not present in the common
quadratic Gram theorem.

### Theorem 1B (cross-depth one-leg rank)

Choose disjoint physical port families `L,V`.  For every `t`, define the
cross-localized flattening with rows `u in L` and columns the transversal
`(2t-1)`-subsets `W of V` by

```text
F_(2t)[u,W]=phi_({u} union W).
```

Then

```text
rank [F_2 | F_4 | ... | F_(2 floor(q/2))] <= rank R_L <= q.
```

Proof.  Expand the permanent in (3) along the column indexed by `u`:

```text
F_(2t)[u,W]=sum_(p in Q) R_pu G_(2t)[p,W],

G_(2t)[p,W]
 =sum_(T subset Q, |T|=2t, p in T)
    haf(A[Q minus T]) per(R_(T minus {p},W)).
```

Thus `F_(2t)=R_L^T G_(2t)` for every depth, and concatenation proves the
rank bound.  In particular, if `rank F_2=q`, every column of every higher
`F_(2t)` lies in `col(F_2)`.

The disjointness is essential.  A naive global flattening has structural
zeros where the row port is repeated in a column; zero-completing those holes
need not preserve the factorization.  Fully polarized copies give an
equivalent safe formulation.

### Corollary 1 (relative degree obstruction)

Write

```text
M_B=sum_S m_S x_S,       Z_Q=sum_S z_S x_S,
Phi=sum_S phi_S x_S.                                    (12)
```

Then the response data determine the relative coefficients recursively by

```text
phi_S=z_S-sum_(T proper_subset S) phi_T m_(S minus T),  (13)
```

where only even subsets contribute.  Every residual-order-`q` response must
satisfy

```text
phi_S=0                         whenever |S|>q.         (14)
```

This is an exact family of convolution equations on synchronized principal
deletions.  It can be tested without first reconstructing `A` or `R`.  It is
strictly stronger data than the two-port rank equations because it begins
only after enough compatible port subsets have been retained.

## The two-residual dual-Wick classification

Let `Q={p,r}`, put

```text
h=A_pr,          a_u=R_pu,          b_u=R_ru,
K_uv=a_u b_v+b_u a_v.                                 (15)
```

Then (3) leaves only degrees zero and two, proving (4).  If

```text
N=Z_Q-hM_B,                                            (16)
```

then

```text
N=Q_K M_B,
M_B+epsilon N=exp(Q_B+epsilon Q_K),    epsilon^2=0.    (17)
```

Thus `N` is literally a tangent vector at `M_B` to the loopless Wick moment
variety.

For an abstract pair of square-zero coefficient families

```text
M=1+sum_(nonempty S) m_S x_S,
N=  sum_(nonempty S) n_S x_S,                          (18)
```

define the base and tangent cumulants by

```text
kappa_S=[x_S] log M,
tau_S  =[epsilon x_S] log(M+epsilon N)
       =[x_S] N/M.                                     (19)
```

Equivalently,

```text
tau_S=sum_(pi in Partitions(S))
 (-1)^(|pi|-1)(|pi|-1)!
 sum_(D in pi) n_D product_(E in pi minus {D}) m_E.    (20)
```

### Theorem 2 (complete physical two-residual criterion)

Over `C`, let `M_empty=1` and set `h=z_empty`.  The triple `(h,M,Z)` is the
all-subset response of a loopless scalar port graph plus two residual
vertices if and only if, with `N=Z-hM`,

1. `kappa_S=0` for every `|S|!=2`;
2. `tau_S=0` for every `|S|!=2`;
3. the hollow pair array `(tau_{uv})_(u!=v)` has off-diagonal bosonic channel
   number at most one, meaning that it admits a diagonal completion
   `K~=a b^T+b a^T` of rank at most two.

When these conditions hold, the port edges are `B_uv=kappa_{uv}`, the two
residual incidence rows are `a,b`, and their mutual edge is `h`.

Proof.  Necessity is (17), because the logarithm is `Q_B+epsilon Q_K`.
Conversely, conditions 1--2 give

```text
M=exp(Q_B),              N=Q_K exp(Q_B).               (21)
```

Condition 3 factors the physically specified off-diagonal entries of `Q_K`
as in (15); diagonal entries multiply `x_u^2` and are invisible.  Installing
those edge weights realizes (17) coefficient by coefficient.  The complex
symmetric rank-two channel factorization is exact; positivity or Hermitian
conjugation is not being assumed.

The theorem is also a sufficiency result: there is no further
principal-hafnian integrability condition for this isolated scalar all-subset
response slice at residual order two.  The remaining difficulty is whether
the GHZ-derived deletion data and tangent/global constraints expose and
satisfy these dual-Wick equations simultaneously.

## First explicit compatibility equations

Write `m_empty=1`, `n_empty=0`, and let `i,j,k,l` be distinct.  The first
new tangent cumulant is

```text
n_ijkl
 =n_ij m_kl+m_ij n_kl
  +n_ik m_jl+m_ik n_jl
  +n_il m_jk+m_il n_jk.                                (22)
```

This is the linearization of the four-point Wick relation.  It couples one
four-vertex residual response to all six lower pair responses; it is not a
rank condition on a single two-port block.

For every even `S`, (17) gives the uniform insertion recursion

```text
n_S=sum_({u,v} subset S) n_uv m_(S minus {u,v}).        (23)
```

At six ports, (23) has fifteen symbolic terms.  Together with the ordinary
Wick equations for `m`, it is equivalent to the vanishing tangent cumulants,
not an approximation or a bounded-order guess.

If only the uncorrected two-port responses `z_uv` are used and `|S|=2m`, the
same equation can be written

```text
z_S=sum_({u,v} subset S) z_uv m_(S minus {u,v})
    -(m-1)h m_S.                                       (24)
```

Indeed, each matching contributing to `m_S` is counted once for each of its
`m` edges in the sum containing `hB_uv`.  Formula (24) is often the most
direct observable form of the dual-Wick obstruction.

For a nonzero residual edge, (19)--(20) apply to the **corrected** family
`n_S=z_S-hm_S`.  Consequently the coordinate-monomial residual branch is not
exempt merely because `h!=0`: it must pass the same synchronized response
test after the direct layer is subtracted.

## Four residuals: the first genuinely new compound

For `q=4`, the relative response is

```text
Phi=h+Phi_2+Phi_4,
[x_S]Phi_4=per(R_(Q,S))                 for |S|=4.      (25)
```

The torus-zero full-rank example in
`RESIDUAL_HAFNIAN_TORUS_ZERO_FULL_RANK_COFACTOR_BOUNDARY.md` proves that
`Phi_2` can have full canonical middle rank even when `h=0`.  Equation (25)
shows where new information first lives: the same incidence matrix must also
produce the four-port permanental compound.  An arbitrary Gram factorization
of `Phi_2` need not be accepted until its `Phi_4` layer is synchronized.

At six ports, Corollary 1 gives the first relative-degree equation

```text
z_S=h m_S
   +sum_(T subset S, |T|=2) phi_T m_(S minus T)
   +sum_(T subset S, |T|=4) phi_T m_(S minus T),
|S|=6.                                                  (26)
```

There is no independent `phi_S` term: it must vanish because `6>q`.  This is
the precise six-point compatibility test for a four-residual cell.

This does not yet yield a closed polynomial relation involving `Phi_2` alone.
For full-rank `C(A)`, arbitrary incidence makes the quadratic layer
congruence-universal; the quartic compound is intentionally additional data.
The next obstruction should compare an actual GHZ-derived four-deletion value
with (25), rather than seek another universal quadratic rank drop.

## Consequences for the active problem

1. **General residual decomposition.**  The two-port cofactor--Gram theorem
   is now embedded in the complete finite tower (3).  Higher residual order
   means higher permanental compounds, not merely more quadratic channels.
2. **Two residuals.**  All principal response compatibility is exactly
   dual-Wick plus `chi_off<=1`.  Four-point equation (22) is the first test
   that can see lower deletions invisible to the top `P_(r+2)` extraction.
3. **Coordinate-monomial branch.**  The arbitrary-cofactor construction has
   `a=b=0`, hence `N=0`, and passes.  The embedded all-full-span permanent
   construction has `B=0`, hence `M=1` and `N=Q_K`, and also passes.  The
   theorem does not falsely exclude either boundary.
4. **`P_5/P_6/P_7`.**  No unconditional nonrestriction follows.  A useful
   application requires four compatible principal deletion slices from the
   same hypothetical witness.  Once supplied, violation of (22) is an exact
   characteristic-zero obstruction.
5. **Blocker surplus.**  Formula (3) is independent of a support census.  It
   remains valid after any legal contraction that leaves a common scalar
   residual graph and port set.

## Literature translation

The square-zero Wick exponential and cumulant criterion are developed in
`BLOCK_SQUARE_ZERO_WICK_COMPLETION_THEOREM.md`.  The present theorem changes
the object: it divides the residual-present response by the residual-absent
Wick family and identifies the finite relative polynomial left behind.  Thus
Theorem 1 is a specialization and repackaging of the master exponential, not
a claim that Wick coefficient extraction itself is new.  The new useful datum
is the synchronized permanental-compound lift and its cross-depth rank bound.

The hafnian/Gaussian correspondence used by Gaussian boson sampling appears
in [Hamilton et al.](https://arxiv.org/abs/1612.01199), while
[Efimov's sum-of-matrices hafnian
formula](https://arxiv.org/abs/2101.09722) is a scalar convolution relative
of (2).  Gaussian moment varieties provide the ambient algebraic-statistical
language ([Amendola--Faugere--Sturmfels](https://arxiv.org/abs/1510.04654)).
The new problem-specific object is the **residual-relative hafnian response
polynomial** `Phi`: its bounded degree records the number of residual
endpoints, and its coefficient tower consists of permanental incidence
compounds rather than classical Gaussian covariance moments alone.

At `q=2`, Theorem 2 identifies the physical slice with a tangent bundle plus
a symmetric minimum-rank completion condition.  This connects the observable
channel issue to complex symmetric matrix completion
([Bernstein--Blekherman--Lee](https://arxiv.org/abs/1909.06593)), but the exact
cofactor-derived values here are special rather than generic.

## Scope wall

```text
residual-relative factorization (2):                  PROVED;
all-degree coefficient formula (3):                   PROVED;
common cofactor--Gram quadratic layer:                 RECOVERED;
top degree-q permanental compound:                     PROVED;
q=2 dual-Wick all-subset classification:               PROVED;
q=2 four-/six-point insertion equations:               PROVED;
q=2 isolated-slice compatibility beyond dual-Wick+chi_off: NONE;
q=4 quadratic/quartic synchronization:                 NECESSARY;
q=4 six-point relative-degree equation:                PROVED;
disjoint-chart cross-depth rank <=q:                    PROVED;
q>=4 classification of possible relative polynomials: UNKNOWN;
four compatible GHZ deletion slices violating (22):    NOT YET FOUND;
partition-closed P_7 window exposing Phi^4/Phi^6:       NOT YET PROVED;
unrestricted P_5, P_6, or P_7 nonrestriction:          UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python verify_residual_relative_response_polynomial_dual_wick.py
python audit_residual_relative_response_polynomial_dual_wick.py
```

The primary verifier constructs the response in the square-zero algebra,
checks the full symbolic two-residual factorization on four ports, verifies
the four-point tangent-Wick equation, and checks the symbolic four-residual
cofactor tower on a diagonal incidence chart and the cross-depth one-leg
factorization on a disjoint chart.  The independent no-import
audit uses integer square-zero multiplication plus separate hafnian and
permanent subset recurrences for a four-residual, six-port instance.  These
are fixed small exact dynamic recurrences, not proof by a large matching,
port-support, or colour-word census.
