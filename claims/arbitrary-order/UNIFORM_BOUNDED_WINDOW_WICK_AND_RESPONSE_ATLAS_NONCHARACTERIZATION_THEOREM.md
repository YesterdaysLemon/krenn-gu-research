# Uniform bounded-window Wick and response-atlas noncharacterization

## Status

**Exact characteristic-zero sharpness theorem.**  No fixed maximum
port-support size characterizes arbitrary-order Wick completion from all
local windows, even when the family is permutation invariant,
restriction-natural, every retained window is one physical graph deck, and
all overlaps have trivial transition data.  The same failure occurs inside
the block-polarized `q=2` response-atlas setting with identifying overlaps
and trivial holonomy.

This is a no-go for ambient bounded-window certification.  It does not rule
out a bounded certificate after using the full ternary target equations or
another proved structural-degree theorem on the actual witness locus.  The
construction is not a graph witness or a Krenn--Gu counterexample.  The
global conjecture remains **UNRESOLVED**.

## 1. Scalar bounded-window no-go

Let `K` be a field of characteristic zero.  Fix an even integer `b>=2`, put

```text
k=b+2,
```

and choose `lambda in K^*`.  For every finite vertex set `V`, define the
normalized even scalar deck

```text
C_empty^V=1,

          lambda,  |I|=k,
C_I^V =
          0,       otherwise,                         (1)
```

for every nonempty even `I subset V`.

### Theorem 1 (uniform bounded-window noncharacterization)

The family (1) has all of the following properties.

1. It is permutation invariant and restriction-natural:

   ```text
   C^V restricted to S = C^S,             S subset V. (2)
   ```

2. If `|S|<=b`, the complete restriction to `S` is the principal hafnian
   deck of the zero-edge graph.  Thus every bounded window is physical and
   every scalar overlap agrees.
3. If `|V|>=k`, the deck is not the complete principal deck of any graph.
4. If `|V|>=k`, its first Wick failure has support exactly `k>b`.

### Proof

Both symmetry and (2) are immediate because (1) depends only on subset
cardinality.  A set of size at most `b` contains no `k`-subset, so every
nonempty coefficient on such a window is zero, exactly as for the zero-edge
graph.

Now let `Q subset V` have size `k=2s`.  Every pair coefficient `C_e` is zero.
Any realizing graph would therefore have every edge weight zero, since its
pair deck is its edge family, and hence would have every nonempty principal
hafnian zero.  This contradicts `C_Q=lambda`.

Equivalently, the Euler--Wick recurrence required of a complete graph deck is

```text
s C_Q=sum_(e subset Q, |e|=2) C_e C_(Q minus e).       (3)
```

At `Q`, the left side is `s lambda!=0` in characteristic zero and the right
side is zero.  All coefficients below support `k` agree with the zero-edge
deck, so this is the first failure.  This proves the theorem.

Since every integer support bound is at most some even `b`, Theorem 1 rules
out a uniform bound of either parity.

### Corollary 2 (symmetric mixed-only perturbations do not repair the route)

Give each vertex a ternary coordinate and work in the vertex-exclusive
square-zero algebra.  Let

```text
E_(V,k)^mix
 =sum_(I subset V, |I|=k)
    sum_(alpha:I->{0,1,2}, alpha nonconstant) x_(I,alpha).  (4)
```

Then `1+lambda E_(V,k)^mix` is invariant under `S_V x S_3`, is
restriction-natural, changes no pure-colour coefficient, and is invisible
on every window of size at most `b`, but is not a Wick deck when `|V|>=k`.
Thus vertex symmetry, colour symmetry, endpoint multihomogeneity, deletion
functoriality, and preservation of the displayed base deck's pure coordinates
do not imply a uniform window bound.  This example does not assert the
nonzero/unit pure-target normalization of a witness.

## 2. Identifying `q=2` response atlases still do not see the defect

Assume now `b>=4`.  Let

```text
V=C disjoint_union {p_0,p_1,p_2},
|C|=b-1,
U_i=C union {p_i}.                                    (5)
```

Thus `|V|=b+2=k`, every chart has `b` ports, and every pairwise overlap is
the common core `C`.  Give each ternary port the same residual frame

```text
P=[ [1,0,0],
    [0,1,0] ],

J=[ [0,1],
    [1,0] ],

K_uv=P^T J P.                                         (6)
```

Any three ports in `C`, taken as singleton groups, make every overlap
three-block identifying.  On every `U_i`, set

```text
choose h in K,
M_i=1,
Z_i=h+Q_K.                                            (7)
```

These are complete physical `q=2` response charts with one common frame.
All overlap transitions and all cycle holonomies are the identity.

On the full port set, however, prescribe

```text
M=1,
Z=h+Q_K+lambda E_(V,k)^mix.                           (8)
```

### Theorem 3 (bounded response-atlas noncharacterization)

Every restriction of (8) to one chart `U_i` is exactly (7); indeed the same
is true on every port subset of size at most `b`.  Nevertheless, (8) is not
the response of any physical two-residual graph.  Its first failure is at
port support `k=b+2`.

### Proof

The last summand in (8) uses all `k` ports, so it restricts to zero on every
`b`-port chart.  Hence the atlas sees the common physical data (6)--(7) and
has trivial holonomy.

For a physical `q=2` response the residual-relative polynomial

```text
Phi=M^(-1)Z
```

has port degree at most two.  Equation (8) has the nonzero degree-`k` term
`lambda E_(V,k)^mix`, so it is not physical.  In coefficient form, put
`N=Z-hM`.  The insertion recurrence at a nonconstant coloured `k`-set is

```text
n_S=sum_({u,v} subset S) n_uv m_(S minus {u,v}).       (9)
```

The left side is `lambda`; every term on the right contains a positive-degree
coefficient of `M=1` and is zero.  All smaller coefficients are exactly those
of (7), proving the final assertion.

## 3. Consequence for bounded obstruction and GL

Theorems 1 and 3 refute the implication

```text
all windows through one fixed support bound are physical
+ all overlaps agree with trivial holonomy
    => the arbitrary-order supplied family is one graph deck/response. (10)
```

They do not refute any of the following stronger routes:

1. **Actual same-graph provenance.**  If a family is already proved to be
   the complete principal deck of one graph, it is physical, but using this
   as the extraction premise is circular.
2. **Global generative equality.**  Bounded charts may reconstruct common
   parameters on all ports if a separate theorem proves, coefficient by
   coefficient, that the full supplied family is generated by them.
3. **Target-coupled descent.**  A new theorem could prove that every first
   nonzero higher cumulant or response defect legally exposes a bounded mixed
   GHZ coefficient with nonzero multiplier and controlled nuisance terms.
4. **Uniform structural degree.**  A uniform recurrence or generation bound
   proved on the actual witness locus could prevent (1) or (8).  Ordinary
   Noetherianity separately at each graph order supplies no such uniform
   bound.
5. **All-support Wick identities.**  The Euler/dual-Wick conditions are
   necessary and sufficient when imposed at every support.  A compact
   arbitrary-support schema is not a bounded-size certificate.

Accordingly, the two-residual atlas theorem's bounded content is its fixed
residual order, finite chart graph, and three-group overlap witness.  Its
physical-chart hypothesis retains the complete all-support dual-Wick tests;
it does not assert a uniformly bounded port-depth criterion.

## Replay

Run from repository root:

```powershell
python claims/arbitrary-order/verify_uniform_bounded_window_wick_and_response_atlas_noncharacterization.py
python -I claims/arbitrary-order/audit_uniform_bounded_window_wick_and_response_atlas_noncharacterization.py
python -m py_compile claims/arbitrary-order/verify_uniform_bounded_window_wick_and_response_atlas_noncharacterization.py claims/arbitrary-order/audit_uniform_bounded_window_wick_and_response_atlas_noncharacterization.py
python -m ruff check claims/arbitrary-order/verify_uniform_bounded_window_wick_and_response_atlas_noncharacterization.py claims/arbitrary-order/audit_uniform_bounded_window_wick_and_response_atlas_noncharacterization.py
```

The primary replay checks the arbitrary-parameter formulas on several exact
even bounds, the first Euler failure, every restriction in the `q=2` atlas,
the identifying overlap ranks, and the degree-`k` insertion defect.  The
independent `python -I` audit imports neither the primary nor a symbolic
package.  It uses bitmask deck restrictions and a separately written perfect-
matching recurrence.  These finite replays audit the conventions and
fixtures; the cardinality and recurrence arguments above prove the uniform
theorems.
