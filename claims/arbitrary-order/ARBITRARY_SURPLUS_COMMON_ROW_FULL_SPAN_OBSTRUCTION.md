# Every root row spans the full target dual at every blocker surplus

## Status

**Exact arbitrary-order characteristic-zero necessary theorem.**  Let `r`
fully supported pairwise-zero roots in a hypothetical three-colour GHZ
realization have blocker union `B` of size

```text
m=r+s,       m>=3.                                    (1)
```

For every root `i`, form its common row space across the blockers,

```text
L_i=span{B_iu(x_i,-):u in B} subset (C^3)^*.           (2)
```

Then

```text
L_i=(C^3)^*       and       dim L_i=3                 (3)
```

for every root.  The conclusion holds for tight, one-port, two-port, and
all higher-surplus cofactor extractions, with arbitrary residual
nonblockers.  It uses the exact matching cofactor formula, a termwise product
grading, and a first-polar contraction.  No effective factorization of the
port forms is assumed.

If the `s`-port forms do admit a simultaneous permanent factorization by
`s` common port-row families, the same theorem forces every one of those
port-row families to span `(C^3)^*` as well.  This factorization is automatic
for `s=1`.  For `s=2` it is exactly the effective form

```text
W_uv=a_u tensor b_v+b_u tensor a_v.                   (4)
```

Thus every arbitrary-order blocker cell containing a root whose incident
covectors across its full blocker union span at most two is excluded.  This
substantially narrows the five-root `P_5/P_6` and seven-blocker frontiers and
the four-root/six-blocker cofactor cell.  It does not exclude systems in
which every root-row family has full span, so the global Krenn--Gu conjecture
remains **UNRESOLVED**.

## The arbitrary-surplus cofactor

Let `H_u` be the `r x 3` root--blocker matrix

```text
H_u[i,c]=B_iu(x_i,e_c).                               (5)
```

For every `s`-subset `S` of the `m` blockers, let `W_S` be an arbitrary
`s`-linear form on the modes in `S`; when `s=0`, it is a scalar.  The local
surplus tensor is

```text
Lambda_(H,s)(W)
 =sum_(S subset B, |S|=s)
    W_S tensor P_r(H_u:u in B\S).                     (6)
```

Suppose it is a coefficient-torus diagonal:

```text
Lambda_(H,s)(W)=d_0 e_0^m+d_1 e_1^m+d_2 e_2^m,
d_0*d_1*d_2!=0.                                       (7)
```

The global matching forms from the arbitrary-order blocker reduction are a
special case of the `W_S`, but the local argument below permits completely
arbitrary port forms.

## Spans zero and one are impossible

Evaluate all output modes at the same target vector `t`.  Equation (6)
becomes

```text
E_W(t)=sum_(|S|=s) W_S(t,...,t)
        per([H_u[-,t]]_(u in B\S)).                   (8)
```

Every permanent assignment uses each root row exactly once.  Hence

```text
E_W belongs to (product_(i=1)^r L_i) Sym^s((C^3)^*).  (9)
```

This holds termwise over the coefficient ring of the arbitrary port forms.
If some `L_i` is zero, then `E_W=0`.  If `dim L_i=1`, its generator is a
linear factor of `E_W`.

The equal-input polynomial of (7) is

```text
D_m(t)=d_0 t_0^m+d_1 t_1^m+d_2 t_2^m.               (10)
```

It has no linear factor for `m>=3`.  For a proposed line
`alpha t_0+beta t_1+gamma t_2=0` with `gamma!=0`, substitute for `t_2` and
clear `gamma^m`.  The coefficients of `t_0^(m-1)t_1` and
`t_0 t_1^(m-1)` force `alpha beta=0`; either case leaves a nonzero pure
term.  If `gamma=0`, the free `d_2 t_2^m` term remains.  Therefore

```text
dim L_i>=2.                                             (11)
```

## The first polar excludes span two

Assume for contradiction that `dim L_i=2` for one root `i`.  Choose a
nonzero vector

```text
p in L_i^perp.                                         (12)
```

Fix a blocker mode `u`.  Evaluate mode `u` at a variable vector `t` and all
other blocker modes at `p`.

On the diagonal side (7), the contraction is the nonzero linear form

```text
g_p(t)=sum_(c=0)^2 d_c p[c]^(m-1) t[c].              (13)
```

It is nonzero because `p!=0` and all `d_c` are nonzero.

Now inspect one cofactor summand in (6).

- If `u in S`, every column of the complementary permanent is evaluated at
  `p`.  Its entire row `i` is zero by (12), so that summand vanishes,
  regardless of the port form `W_S`.
- If `u notin S`, all retained permanent columns except `u` are evaluated at
  `p`.  Any nonzero permanent assignment must therefore assign row `i` to
  column `u`.  The summand is a scalar multiple of `H_u[i,-](t)`.

After summing all subsets `S`, there is a scalar `C_(i,u)` such that

```text
g_p=C_(i,u) H_u[i,-].                                 (14)
```

Because `g_p` is nonzero, both `C_(i,u)` and `H_u[i,-]` are nonzero.  Equation
(14) holds for every blocker `u`, with the same left side.  Consequently all
covectors `H_u[i,-]` are proportional to `g_p`, and

```text
dim L_i=1,                                             (15)
```

contradicting the assumption `dim L_i=2`.  Combining (11) and (15) proves
the full-span conclusion (3).

The first-polar argument is modewise and does not depend on cancellations
between different port subsets.  Terms with the variable mode in the port
set die on the zero permanent row; all other terms carry the same displayed
root-row covector.

## Factored port rows also have full span

Suppose the port forms in (6) arise from `s` common row families

```text
g_(a,u) in (C^3)^*,       a=1,...,s, u in B,          (16)
```

through

```text
W_S((z_u)_(u in S))
 =per([g_(a,u)(z_u)]_(a=1,...,s; u in S)).            (17)
```

Append these rows below `H_u` to form an `m x 3` matrix

```text
M_u=[H_u;g_(1,u);...;g_(s,u)].                        (18)
```

The unsigned Laplace expansion of the `m x m` permanent along the final `s`
source rows is

```text
P_m(M_u:u in B)
 =sum_(|S|=s) P_s(g_(a,u):u in S)
                tensor P_r(H_u:u in B\S)
 =Lambda_(H,s)(W).                                    (19)
```

This is a termwise bijection: a full permanent assignment is uniquely split
by the set `S` of columns used by the port rows, a port-row bijection onto
`S`, and a root-row bijection onto `B\S`.  There are no determinant signs.

Equation (19) is a direct `P_m` restriction to the torus diagonal (7).  Apply
the already proved `s=0` algebraic argument to every one of its `m` persistent
source rows.
Besides the root conclusion (3), it gives

```text
span{g_(a,u):u in B}=(C^3)^*       for every a.       (20)
```

For first surplus, every `W_{u}` is itself a linear form `g_u`, so (17) is
automatic and the one common port-row family must have full span.  For two
ports, (17) reads exactly

```text
W_uv(z_u,z_v)
 =a_u(z_u)b_v(z_v)+b_u(z_u)a_v(z_v),                 (21)
```

and both families `{a_u}` and `{b_u}` must span three.  This is conditional
for `s>=2`: arbitrary joint matching forms need not possess (17).

## Transfer to arbitrary ambient order

The matching bijection in
[`TWO_PORT_SEVEN_BLOCKER_REDUCTION.md`](TWO_PORT_SEVEN_BLOCKER_REDUCTION.md)
constructs (6) from the actual joint matching forms on the `s` unused
blocker ports after fixing every residual nonblocker at a simultaneous torus
kernel.  Its diagonal coefficients are

```text
d_c=product_(i in R) x_i[c] product_(q in Q) z_q[c], (22)
```

and are nonzero.  The local proof therefore transfers verbatim to every even
ambient order.

Important specializations are:

```text
s=0: tight r-blocker permanent extraction;
s=1: one-port P_(r+1), including full port-row span;
r=4,s=2: arbitrary-order four-root/six-blocker cofactor;
r=5,s=1: five-root/six-blocker P_6, including full port-row span;
r=5,s=2: seven-blocker two-port frontier, with port-row span
  conditional on simultaneous factorization.                         (23)
```

For the four-root/six-blocker cell this strengthens both the projectively
constant-row obstruction and the intermediate rank-two-annihilator ledger:
all four common-root row spaces must have rank three.

The six common-port missing-colour profiles

```text
empty, 1, 1+1, 1+1+1, 2, 2+1
```

from
[`P6_SIMULTANEOUS_KERNEL_AND_NATURAL_LIFT_OBSTRUCTIONS.md`](../p6/P6_SIMULTANEOUS_KERNEL_AND_NATURAL_LIFT_OBSTRUCTIONS.md)
remain compatible with full root-row and port-row span at the linear
incidence level.  Three full blocker modes can cycle a coordinate basis
through every root row and through the port row, while each exceptional mode
realizes its prescribed rank-two coordinate-kernel plane.  Therefore the
new span theorem narrows those profiles but does not by itself exclude any
one of the six; their simultaneous permanent equations remain essential.

## Boundary

```text
root-row span zero or one at any surplus: EXCLUDED;
root-row span exactly two at any surplus: EXCLUDED;
every root-row space spans the full target dual: PROVED NECESSARY;
first-surplus common port-row span three: PROVED NECESSARY;
factored s-port row-family spans three: PROVED NECESSARY;
six common-port missing-colour profiles at incidence level: ALL SURVIVE;
unfactored higher joint-port forms: UNKNOWN;
all-full-span cofactor systems: UNKNOWN;
mode-kernel survivor strata inside all-full-span systems: UNKNOWN;
P_5 and P_6 nonrestriction in full: UNKNOWN;
full arbitrary-order local-to-global reduction: UNKNOWN;
global Krenn--Gu conjecture: UNRESOLVED.
```

## Replay

Replay the exact arbitrary-surplus dependency first:

```text
python claims/arbitrary-order/verify_two_port_seven_blocker_reduction.py
python claims/arbitrary-order/audit_two_port_seven_blocker_reduction.py
```

Then run:

```text
uv run --with sympy python claims/arbitrary-order/verify_arbitrary_surplus_common_row_full_span_obstruction.py
python claims/arbitrary-order/audit_arbitrary_surplus_common_row_full_span_obstruction.py
```

The primary verifier checks the product grading in representative tight and
higher-surplus cases, every modewise first-polar factorization in the
four-root/six-blocker and five-root/seven-blocker cases, the nonzero diagonal
polar, the degree-`m` no-linear-factor coefficients, symbolic Laplace
factorizations through three ports, and exact full-span incidence models for
all six common-port profiles.  The independent no-import audit enumerates the
general surviving-assignment and Laplace bijections over a wider range,
reconstructs exact integer first polars with a genuinely rank-two annihilator
family, and independently rebuilds the profile models.  The written matching,
Laplace, and polarization proofs establish arbitrary `r,s` and ambient order.
No finite-field inference is used.
