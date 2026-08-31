# GLD100 B=0 C-open corollary hostile review

## Verdict

**Candidate-review verdict: PASS for freezing and external audit, not yet for
live promotion.**  The proposed statement is a direct exact consequence of
the accepted GLD96, GLD100, and GLD99 proof interfaces.  It isolates no new
CAS output and changes no upstream theorem.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

## Exact statement reviewed

Over `C`, on the normalized GLD88/F88 equal-leaf H4 offset chart, with
arbitrary `a`,

```text
V(B_offset,Q6) intersect D(C_offset*Delta)
  intersect {rank M(G) <= 6} = empty.
```

Equivalently, on `D(Delta)`, `B_offset=0` and complete syndrome rank at most
six force `C_offset=0`.

## Hostile questions

### 1. Is this silently using the GLD96 E31 localization?

No.  GLD96 uses `E31!=0` to force `B_offset=0` from a general offset point.
The corollary assumes `B_offset=0`.  Its H2deg-open proof begins after that
step, with the exact residual form

```text
Ttilde_i=D_i*T_i
        =f_i(B_offset)+C_offset*g_i(B_offset),
f_i(0)=0.
```

At `B_offset=0`, rank makes the actual minors `T_i` vanish and
the `D_i` clearing factors are units on `D(H2deg*Delta)`, so the cleared
minors also vanish.  Then `C_offset!=0` forces all four `g_i(0)` to vanish.
GLD100's gamma atlas, pair-resultant cover, and pointwise fibre closures
contain no `E31` premise.  Both the primary and independent upstream
implementations preserve that dependency boundary.

### 2. Is division by C_offset legitimate?

Yes, and only pointwise on the declared `D(C_offset)` chart.  The statement
does not divide by `C_offset` at its zero boundary.  That boundary is exactly
the desired conclusion `B_offset=C_offset=0`.

### 3. Are the primitive gamma clearings reversible?

Yes on `D(H2deg*Delta)`, exactly the open retained by the GLD100 gamma
calculation.  The package does not extend those identities to `H2deg=0` or
`Delta=0`.  The former is handled by the separate exact GLD99 theorem; the
latter remains open.

### 4. Does a necessary resultant cover prove the branch by itself?

No.  The corollary relies on all of GLD100's accepted pointwise branch
closures after the necessary cover.  The `p`, `p-1`, and `P` branches are
incompatible with the declared gamma/Delta chart; `H2deg` is outside the open;
the two quadratic and two quartic survivors are closed by exact gamma gcds or
direct `D0,D2` seven-minor identities.  The review would reject any version
that cited only the resultant support.

### 5. Is the H2deg removal cancellation?

No.  It is the exhaustive binary split `H2deg!=0` or `H2deg=0`.  GLD100 owns
the first case after `B_offset=0`; GLD99 owns the second for arbitrary `a`.

### 6. Is selected-minor vanishing used conversely?

No.  Complete syndrome rank at most six implies every selected seven-minor
vanishes.  No converse is asserted.  Direct minors in GLD100 are additional
necessary rank equations on the finite fibres.

### 7. What does this change for the E31 wall?

It removes only the complementary `B_offset=0,C_offset!=0` chart.  The new
pointwise computation may focus on

```text
V(E31,Q6) intersect D(B_offset*H2deg*Delta)
  intersect {rank M(G)<=6}.
```

That remaining `D(B_offset)` locus is not closed here.  Generic coprimality,
modular scouting, or a support-only degree-620 cover does not close it.

## Evidence and promotion gate

The package pins nine upstream theorem/verifier/audit/review files by
LF-normalized SHA-256.  Its primary checker validates the exact interface and
AST-inspects twelve named GLD100 gamma/pair/fibre functions for hidden `E31`
use.  Its independent audit imports no repository verifier; it instead
checks the complete GLD100 owner sections between the pair-resultant cover and
proof route, the GLD96 residual identity, the GLD99 arbitrary-`a` statement,
and the two-case implication.

Before live promotion, an immutable commit and tree require fresh-detached
external audits of the exact source pins, scope, rank direction, reversible
opens, H2deg exhaustion, no-E31 dependency, and all nonclaims.  Until then,
the certificate remains candidate and no frontier, theorem-ledger, or README
entry is allowed.

## Retained nonclaims

The review does not accept `D(B_offset)` E31-wall closure, `Delta=0`,
`Omega=0`, outside-F88 coverage, the GLD83 Fitting pullback, another
chart/component/source/root/order, source integrability, target attachment,
lifting, gluing, or global resolution.
