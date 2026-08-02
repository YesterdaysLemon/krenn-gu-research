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

Thus every arbitrary-order blocker cell containing a root whose incident
covectors across its full blocker union span at most two is excluded.  This
substantially narrows the five-root `P_5/P_6` and seven-blocker frontiers and
the four-root/six-blocker cofactor cell.  It does not exclude systems in
which every root-row family has full span, so the global Krenn--Gu conjecture
remains **UNRESOLVED**.

## The arbitrary-surplus cofactor

Let `H_u` be the `r x 3` root--blocker matrix

```text
H_u[i,c]=B_iu(x_i,e_c).                               (4)
```

For every `s`-subset `S` of the `m` blockers, let `W_S` be an arbitrary
`s`-linear form on the modes in `S`; when `s=0`, it is a scalar.  The local
surplus tensor is

```text
Lambda_(H,s)(W)
 =sum_(S subset B, |S|=s)
    W_S tensor P_r(H_u:u in B\S).                     (5)
```

Suppose it is a coefficient-torus diagonal:

```text
Lambda_(H,s)(W)=d_0 e_0^m+d_1 e_1^m+d_2 e_2^m,
d_0*d_1*d_2!=0.                                       (6)
```

The global matching forms from the arbitrary-order blocker reduction are a
special case of the `W_S`, but the local argument below permits completely
arbitrary port forms.

## Spans zero and one are impossible

Evaluate all output modes at the same target vector `t`.  Equation (5)
becomes

```text
E_W(t)=sum_(|S|=s) W_S(t,...,t)
        per([H_u[-,t]]_(u in B\S)).                   (7)
```

Every permanent assignment uses each root row exactly once.  Hence

```text
E_W belongs to (product_(i=1)^r L_i) Sym^s((C^3)^*).  (8)
```

This holds termwise over the coefficient ring of the arbitrary port forms.
If some `L_i` is zero, then `E_W=0`.  If `dim L_i=1`, its generator is a
linear factor of `E_W`.

The equal-input polynomial of (6) is

```text
D_m(t)=d_0 t_0^m+d_1 t_1^m+d_2 t_2^m.                (9)
```

It has no linear factor for `m>=3`.  For a proposed line
`alpha t_0+beta t_1+gamma t_2=0` with `gamma!=0`, substitute for `t_2` and
clear `gamma^m`.  The coefficients of `t_0^(m-1)t_1` and
`t_0 t_1^(m-1)` force `alpha beta=0`; either case leaves a nonzero pure
term.  If `gamma=0`, the free `d_2 t_2^m` term remains.  Therefore

```text
dim L_i>=2.                                             (10)
```

## The first polar excludes span two

Assume for contradiction that `dim L_i=2` for one root `i`.  Choose a
nonzero vector

```text
p in L_i^perp.                                         (11)
```

Fix a blocker mode `u`.  Evaluate mode `u` at a variable vector `t` and all
other blocker modes at `p`.

On the diagonal side (6), the contraction is the nonzero linear form

```text
g_p(t)=sum_(c=0)^2 d_c p[c]^(m-1) t[c].               (12)
```

It is nonzero because `p!=0` and all `d_c` are nonzero.

Now inspect one cofactor summand in (5).

- If `u in S`, every column of the complementary permanent is evaluated at
  `p`.  Its entire row `i` is zero by (11), so that summand vanishes,
  regardless of the port form `W_S`.
- If `u notin S`, all retained permanent columns except `u` are evaluated at
  `p`.  Any nonzero permanent assignment must therefore assign row `i` to
  column `u`.  The summand is a scalar multiple of `H_u[i,-](t)`.

After summing all subsets `S`, there is a scalar `C_(i,u)` such that

```text
g_p=C_(i,u) H_u[i,-].                                  (13)
```

Because `g_p` is nonzero, both `C_(i,u)` and `H_u[i,-]` are nonzero.  Equation
(13) holds for every blocker `u`, with the same left side.  Consequently all
covectors `H_u[i,-]` are proportional to `g_p`, and

```text
dim L_i=1,                                              (14)
```

contradicting the assumption `dim L_i=2`.  Combining (10) and (14) proves
the full-span conclusion (3).

The first-polar argument is modewise and does not depend on cancellations
between different port subsets.  Terms with the variable mode in the port
set die on the zero permanent row; all other terms carry the same displayed
root-row covector.

## Transfer to arbitrary ambient order

The matching bijection in
[`TWO_PORT_SEVEN_BLOCKER_REDUCTION.md`](TWO_PORT_SEVEN_BLOCKER_REDUCTION.md)
constructs (5) from the actual joint matching forms on the `s` unused
blocker ports after fixing every residual nonblocker at a simultaneous torus
kernel.  Its diagonal coefficients are

```text
d_c=product_(i in R) x_i[c] product_(q in Q) z_q[c],  (15)
```

and are nonzero.  The local proof therefore transfers verbatim to every even
ambient order.

Important specializations are:

```text
s=0: tight r-blocker permanent extraction;
s=1: one-port P_(r+1) extraction;
r=4,s=2: arbitrary-order four-root/six-blocker cofactor;
r=5,s=1: the five-root/six-blocker P_6 frontier;
r=5,s=2: the seven-blocker two-port frontier.          (16)
```

For the four-root/six-blocker cell this strengthens both the projectively
constant-row obstruction and the intermediate rank-two-annihilator ledger:
all four common-root row spaces must have rank three.

## Boundary

```text
root-row span zero or one at any surplus: EXCLUDED;
root-row span exactly two at any surplus: EXCLUDED;
every root-row space spans the full target dual: PROVED NECESSARY;
all-full-span cofactor systems: UNKNOWN;
mode-kernel survivor strata inside all-full-span systems: UNKNOWN;
P_5 and P_6 nonrestriction in full: UNKNOWN;
full arbitrary-order local-to-global reduction: UNKNOWN;
global Krenn--Gu conjecture: UNRESOLVED.
```

## Replay

Replay the exact arbitrary-surplus dependency first:

```text
python verify_two_port_seven_blocker_reduction.py
python audit_two_port_seven_blocker_reduction.py
```

Then run:

```text
uv run --with sympy python verify_arbitrary_surplus_common_row_full_span_obstruction.py
python audit_arbitrary_surplus_common_row_full_span_obstruction.py
```

The primary verifier checks the product grading in representative tight and
higher-surplus cases, every modewise first-polar factorization in the
four-root/six-blocker and five-root/seven-blocker cases, the nonzero diagonal
polar, and the degree-`m` no-linear-factor coefficients.  The independent
no-import audit enumerates the general surviving-assignment formula over a
wider range and reconstructs exact integer first polars with a genuinely
rank-two annihilator family.  The written matching and polarization proof
establish arbitrary `r,s` and ambient order.  No finite-field inference is
used.
