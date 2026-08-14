# Balanced `m=3` common-three-space lower-joint-rank transverse two-root uninvolved-rank-one complete pair-pole exclusion

## Status

**Exact characteristic-zero pair-pole and graph-extension exclusion of both
remaining uninvolved-row-rank-one cells in the joint-rank-three/four
transverse two-root branch.**  Let `U` be the total singleton span of a
normalized, target-consistent physical `m=3` common shore whose complete
four-column sensor has full function-field rank.  Put `K=image H`, assume

```text
dim U=3,                         rank H in {3,4},      (1)
```

and suppose exactly two root--root blocks are nonzero while the uninvolved
third-root row has rank one.  S2BM puts every such point in one exact
one-cell permanent frame.  The theorem below proves that its unique rational
pair lift always has a prime-divisor pole.  Consequently neither the
joint-rank-three nor the joint-rank-four cell extends to regular bilinear
pair blocks or to a six-vertex graph.

The proof is exhaustive.  It classifies the source support of the populated
one-cell square, computes every possible common-zero kernel, and then uses a
multigraded Cramer residue argument.  The exact S2BM controls remain valid
physical singleton/empty incidences and show the local equations are sharp;
this theorem proves that their poles are universal rather than artifacts of
the displayed representatives.

This closes the complete lower-rank transverse **two-root** branch.  It does
not close lower-rank three-root derivatives, another S2T component, another
S2Q pole stratum, any higher order, or the all-balanced rank-drop branch.  It
proves neither the global conjecture nor a counterexample.  Global
Krenn--Gu remains **UNRESOLVED**.

## 1. The exact S2BM one-cell frame

Let `{s,t,u}` be the three target colours.  After exchanging the two
involved roots and rescaling rows and blocks, S2BM gives

```text
B_23=e_t tensor e_t,
B_13=e_u tensor e_u,

P=span{(e_t,0),(0,e_u),(e_s,e_s)}.                  (2)
```

The only nonzero third-root row is `q=q_s`, and the involved rows are

```text
r_t=a,       r_s=v,       r_u=0,
p_u=b,       p_s=v,       p_t=0.                    (3)
```

For rows in the separated nonroot space

```text
W=X direct-sum Y direct-sum Z,                      (4)
```

write

```text
M_(c,d)(e)=per(c,d,e),
Alt(c,d,e)=Alt_XYZ(c,d,e).                          (5)
```

The complete empty target table is exactly

```text
M_(v,v)(q)=T_s=x_s tensor y_s tensor z_s,
M_(a,v)(q)=M_(v,b)(q)=M_(a,b)(q)=0.                 (6)
```

The three singleton columns, in the S2BM basis of `U`, are

```text
g_X=(a_X,b_X,v_X)^T,
g_Y=(a_Y,b_Y,v_Y)^T,
g_Z=(a_Z,b_Z,v_Z)^T.                                (7)
```

Physical singleton independence is

```text
Delta=det[g_X,g_Y,g_Z]=Alt(a,b,v)!=0.               (8)
```

The residual target is

```text
R=(T_t,T_u,0)^T,
T_c=x_c y_c z_c,                                    (9)
```

so the unique function-field pair candidate satisfies

```text
[g_X,g_Y,g_Z](C_X,C_Y,C_Z)^T=R.                    (10)
```

Here `C_X` has bidegree `YZ`, and cyclically.  At `m=3`, these are all the
nonempty pair components.  It remains to prove that (10) can never have
three global polynomial components.

## 2. Exhaustive tangent and common-zero atlas

Common nonzero scalar factors in this section are absorbed into `q` and
`T_s`.  They do not change a kernel, a determinant divisor, or pair
regularity.

### Lemma 1 (one-cell source atlas)

Assume (6) and (8).  After permuting `X,Y,Z`, exactly one of the following
charts holds.

1. **Two-source square, regular kernel.**  There are nonzero
   `x in X`, `y in Y`, `z in Z` and arbitrary `p in X`, `r in Z` such that

   ```text
   v=x+z,                         q=p+y+r,            (11)
   ```

   every common zero of `M_(-,v)(q)` has `Y` component proportional to
   `y`, and

   ```text
   ker M_(-,v)(q)
    =span{a_0=-x+z, b_0=-p+y-r}.                    (12)
   ```

   Consequently

   ```text
   Delta proportional x tensor y tensor z.          (13)
   ```

2. **Two-source square, conjugate kernel.**  In (11), for one scalar
   `alpha`,

   ```text
   p=alpha x,                    r=-alpha z,          (14)

   ker M_(-,v)(q)=span(-x+z) direct-sum Y.           (15)
   ```

   Writing

   ```text
   a=lambda(-x+z)+A,       b=mu(-x+z)+B,
   A,B in Y,                                             (16)
   ```

   gives

   ```text
   Delta proportional
     x tensor (lambda B-mu A) tensor z,              (17)
   ```

   and the middle factor is nonzero by (8).

3. **Three-source square, transverse target factor.**  There are nonzero
   `x in X`, `y in Y`, `z in Z` and `z_s in Z` independent of `z` such that

   ```text
   v=x+y+z,
   T_s=x tensor y tensor z_s,
   q=alpha x+beta y+z_s-(alpha+beta)z.               (18)
   ```

   If `alpha+beta!=0`, the common-zero kernel is the two-plane

   ```text
   u(lambda,mu)=lambda x+mu y
      +[(alpha lambda+beta mu)z
        -(lambda+mu)z_s]/(alpha+beta),               (19)
   ```

   and for independent parameter pairs

   ```text
   Alt(u(lambda,mu),u(lambda',mu'),v)
    proportional
      (lambda mu'-mu lambda') x tensor y tensor z_s. (20)
   ```

   If `alpha+beta=0` but `alpha!=0`, the kernel is `Z`, contradicting
   (8).  If `alpha=beta=0`, then

   ```text
   ker M_(-,v)(q)=span(-x+y) direct-sum Z,            (21)
   Delta proportional x tensor y tensor L_Z          (22)
   ```

   for one nonzero `L_Z in Z`.

4. **Three-source square, aligned target factor.**  There are nonzero
   `x in X`, `y in Y`, `z in Z` such that

   ```text
   v=x+y+z,                  T_s=x tensor y tensor z,
   q=alpha x+beta y+gamma z,                         (23)
   delta=alpha+beta+gamma!=0.                        (24)
   ```

   Put

   ```text
   h_X=beta+gamma, h_Y=alpha+gamma, h_Z=alpha+beta.  (25)
   ```

   Since `h_X+h_Y+h_Z=2 delta`, not all three vanish.

   - If none vanishes, the kernel is the scalar two-plane

     ```text
     h_X lambda+h_Y mu+h_Z nu=0,                    (26)
     ```

     and `Delta` is proportional to `x tensor y tensor z`.
   - If exactly one vanishes, say `h_X=0`, then

     ```text
     ker M_(-,v)(q)
      =X direct-sum span(h_Z y-h_Y z),               (27)
     Delta=L_X tensor y tensor z,
     L_X!=0.                                         (28)
     ```

   - If exactly two vanish, say `h_X=h_Y=0`, then

     ```text
     ker M_(-,v)(q)=X direct-sum Y,
     Delta=(A tensor D-B tensor C) tensor z,          (29)
     ```

     where `a=A+C`, `b=B+D`, and the displayed `X tensor Y` factor is
     nonzero.

The alternatives are exhaustive.  Notice that the last zero in (6),
`M_(a,b)(q)=0`, is not needed for the divisor conclusions: the two common
zeros and full singleton determinant already force them.

### Proof

A one-source `v` has `M_(v,v)(q)=0`, so `v` uses two or three sources.

If `v=x+z`, the nonzero square is `x tensor q_Y tensor z`; normalize
`q=p+y+r`.  For `c=A+B+C`, direct polarization gives

```text
M_(c,v)(q)
 =A tensor y tensor z
  +x tensor B tensor r
  +x tensor y tensor C
  +p tensor B tensor z.                              (30)
```

Projecting first modulo `x` and then modulo `z` shows that `B` is
proportional to `y` unless `p=alpha x`, `r=beta z`.  In the former case,
putting `B=lambda y` in (30) gives

```text
c=lambda(-p+y-r)+rho(-x+z),                         (31)
```

which proves (12).  In the latter case, the same two quotient equations
first give `A=a x` and `C=c z`; equation (30) then becomes

```text
(a+c)y+(alpha+beta)B=0.                              (32)
```

It still gives (12) when `alpha+beta!=0`; when the sum is zero it gives
(15).  Alternating the displayed bases with `v` proves (13) and (17).

Now let all three components of `v` be nonzero.  A decomposable tensor in
the Segre tangent space

```text
x tensor y tensor Z
 +x tensor Y tensor z
 +X tensor y tensor z                               (33)
```

shares at least two factor lines with `x tensor y tensor z`.  Indeed,
projecting a decomposable tensor modulo each pair of base lines shows that
at least two of its three factors lie on the corresponding base lines.
After a source permutation, write `T_s=x tensor y tensor z_s`.

If `z_s,z` are independent, the square identity forces (18).  For
`c=A+B+C`, polarization reduces to

```text
M_(c,v)(q)
 =A tensor y tensor (z_s-alpha z)
  +x tensor B tensor (z_s-beta z)
  +(alpha+beta)x tensor y tensor C.                 (34)
```

Projection modulo `x` and `y` first makes `A=lambda x`, `B=mu y`.
Solving (34) gives (19) when the sum is nonzero.  When the sum is zero,
independence of `z_s,z` gives either the kernel `Z` or (21).  Direct
alternation gives (20) and (22).

Finally, if `z_s=z`, write (23).  The common-zero map is

```text
M_(A+B+C,v)(q)
 =h_X A tensor y tensor z
  +h_Y x tensor B tensor z
  +h_Z x tensor y tensor C.                         (35)
```

If all weights are nonzero, quotienting by the three base lines gives
(26).  One zero weight frees exactly the corresponding source summand and
leaves one relation between the other two base lines, giving (27).  Two
zero weights free exactly two source summands.  Alternating two kernel rows
with `v` gives (28)--(29).  This proves the lemma.  QED.

## 3. The missing-coordinate Cramer residue

Work in the multigraded polynomial ring on the nine nonroot target
coordinates.  Let

```text
N_X=det[R,g_Y,g_Z],
N_Y=det[g_X,R,g_Z],
N_Z=det[g_X,g_Y,R].                                 (36)
```

Cramer's rule gives `C_X=N_X/Delta`, and cyclically.

### Lemma 2 (missing-coordinate residue)

If `x_s` divides `Delta` and `C_X` is a global `YZ`-bilinear section, then

```text
N_X=0,                         C_X=0.                (37)
```

The cyclic statements also hold.

### Proof

Neither `R=(T_t,T_u,0)` nor `g_Y,g_Z` contains the variable `x_s` because
`s,t,u` are distinct target colours and the singleton columns are separated
by source.  Hence `N_X` is independent of `x_s`.  A global pair component is
a polynomial and satisfies `N_X=Delta C_X`.  The right side is divisible by
`x_s`; an `x_s`-independent polynomial divisible by `x_s` is zero.  This
proves (37).  QED.

This is a divisorial statement in the full polynomial ring, not a pointwise
specialization and not a claim that every maximal minor has only coordinate
factors.

## 4. Every source chart has a pair pole

Assume for contradiction that all three components in (10) are global.

In the regular two-source chart, (13) and Lemma 2 give

```text
C_X=C_Y=C_Z=0,                                      (38)
```

contradicting `R!=0`.

In the conjugate two-source chart, (17) gives `C_X=C_Z=0`.  The remaining
equation would be

```text
(a_Y,b_Y,0)^T C_Y=(T_t,T_u,0)^T.                   (39)
```

Both target terms are nonzero.  Thus the same positive-bidegree polynomial
`C_Y` would divide the coprime monomials `T_t` and `T_u`.  This is impossible
in the polynomial UFD.  Equivalently, their `XZ` quotients use different
target coordinates in both factors.

In the transverse-target three-source chart, (20) again gives (38).  On the
exceptional chart (21)--(22), Lemma 2 gives `C_X=C_Y=0`; the third coordinate
of `g_Z C_Z=R` is `v_Z C_Z=z C_Z=0`, so `C_Z=0`, again impossible.

In the aligned-target chart with no zero weight, all three coordinate
factors divide `Delta`, giving (38).  With exactly one zero weight, say
`h_X=0`, (28) gives `C_Y=C_Z=0`; the third coordinate of `g_X C_X=R` is
`x C_X=0`, so the last component also vanishes.  The source-permuted cases
are identical.

It remains only the two-zero-weight chart (29).  Suppose, after source
permutation, `h_X=h_Y=0`.  Then

```text
g_X=(A,B,x)^T,       g_Y=(C,D,y)^T,       g_Z=(0,0,z)^T,
Delta=z(AD-BC).                                      (40)
```

The Cramer numerator of `C_Z` is

```text
N_Z=T_u(x C-y A)+T_t(y B-x D).                      (41)
```

It is independent of `z_s=z`.  If it vanished, independence of the target
`Z`-coordinates `z_t,z_u` would give

```text
x tensor C=A tensor y,
B tensor y=x tensor D.                              (42)
```

The two rank-one equalities force

```text
A=lambda x, C=lambda y,
B=mu x,     D=mu y,                                 (43)
```

and hence `AD-BC=0`, contrary to (8).  Therefore `N_Z!=0`; (40)--(41)
give a genuine pole along `z=0`.

Every source chart therefore violates the pair-regularity condition.  By
the exact Cramer--Euler pair-pole gate, no point in either `q=1` cell extends
to one physical graph.  The argument is rank-independent inside
`rank H in {3,4}` because S2BM gives the same one-cell frame in both
incidences.

## 5. Proof-topology consequence

The complete lower-rank transverse two-root frontier is now

```text
joint rank 4, uninvolved-row rank 2:                 IMPOSSIBLE (S2BN);
joint rank 3, uninvolved-row rank 2:
  local incidence controls:                         EXIST;
  regular graph extension:                          IMPOSSIBLE (S2BO);

joint rank 3 or 4, uninvolved-row rank 1:
  local incidence controls:                         EXIST (S2BM);
  exhaustive source atlas and pair regularity:      IMPOSSIBLE (this theorem);

lower-rank transverse two-root graph extension:     EMPTY;
lower-rank three-root derivatives / other branches: OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.        (44)
```

The next common-three-space obligation is therefore the joint-rank-three/four
**three-root** derivative census, not another two-root support cell.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_lower_joint_rank_transverse_two_root_uninvolved_rank_one_complete_pair_pole_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_lower_joint_rank_transverse_two_root_uninvolved_rank_one_complete_pair_pole_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_lower_joint_rank_transverse_two_root_uninvolved_rank_one_complete_pair_pole_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_lower_joint_rank_transverse_two_root_uninvolved_rank_one_complete_pair_pole_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_lower_joint_rank_transverse_two_root_uninvolved_rank_one_complete_pair_pole_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_lower_joint_rank_transverse_two_root_uninvolved_rank_one_complete_pair_pole_exclusion.py
```

The primary verifier symbolically replays every derivative-kernel chart,
the determinant factorizations, the two-zero-weight numerator, and exact
Cramer pole representatives.  The independent no-import audit rebuilds the
source tensors, kernel representatives, determinants, Cramer numerators, and
negative coordinate valuations with standard-library `Fraction` arithmetic
and a separate sparse-polynomial implementation.  The scripts replay the
displayed identities; the arbitrary-vector exhaustiveness is the written
quotient and tangent-space proof above.

## Dependencies

- [`lower-joint-rank transverse two-root localization and pole controls`](BALANCED_M3_COMMON_THREE_SPACE_LOWER_JOINT_RANK_TRANSVERSE_TWO_ROOT_LOCALIZATION_AND_POLE_CONTROLS_THEOREM.md)
- [`joint-rank-four uninvolved-rank-two complete exclusion`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_TRANSVERSE_TWO_ROOT_UNINVOLVED_RANK_TWO_COMPLETE_EXCLUSION_THEOREM.md)
- [`joint-rank-three uninvolved-rank-two exceptional normal form and pole controls`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_THREE_TRANSVERSE_TWO_ROOT_UNINVOLVED_RANK_TWO_EXCEPTIONAL_NORMAL_FORM_AND_POLE_CONTROLS_THEOREM.md)
- [`Cramer--Euler pair-pole gate`](BALANCED_FULL_SENSOR_CRAMER_EULER_PAIR_POLE_GATE_THEOREM.md)
