# Balanced full-sensor common-shore binary syzygy--permanent residual obstruction

## Status

**Exact characteristic-zero obstruction closing the binary residual isolated by
S2O.**  For three two-dimensional root spaces, suppose one nonzero pure tensor
lies in the image of the common-shore singleton map and a second nonzero pure
tensor is the polarized permanent of three singleton syzygies.  Then the two
pure tensors share at least one factor line.

The S2O residual asks for precisely such a pair with transverse basis factors
in all three root spaces.  It is therefore empty.  Consequently none of the
eight normalized `m=3` full-row S2M controls lies in the common-shore companion
matching-sum image.

This excludes eight particular ambient sharpness controls.  It does **not**
prove that every realized balanced target incidence passes a retained pair
jet, and it does not construct or exclude a physical Krenn--Gu witness.  The
universal S2 gate, all higher-order recurrences, and the global conjecture
remain open.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. The transverse-pure obstruction

Let `K` be a characteristic-zero field and let

```text
dim_K V_1=dim_K V_2=dim_K V_3=2.                    (1)
```

Fix three shore blocks

```text
C_12 in V_1 tensor V_2,
C_13 in V_1 tensor V_3,
C_23 in V_2 tensor V_3                              (2)
```

and define

```text
D_C(u_1,u_2,u_3)
 =u_1 tensor C_23
  +insert_2(C_13,u_2)
  +C_12 tensor u_3.                                 (3)
```

For three triples `h_x,h_y,h_r in V_1 direct-sum V_2 direct-sum V_3`, put

```text
Perm(h_x,h_y,h_r)
 =sum_(sigma in S_3)
    (h_(sigma(x)))_1 tensor
    (h_(sigma(y)))_2 tensor
    (h_(sigma(r)))_3.                               (4)
```

### Theorem 1 (transverse pure tensors cannot coexist)

Suppose

```text
P=p_1 tensor p_2 tensor p_3 !=0 lies in image(D_C), (5)
```

and there are `h_x,h_y,h_r in kernel(D_C)` such that

```text
Q=Perm(h_x,h_y,h_r)
  =q_1 tensor q_2 tensor q_3 !=0.                   (6)
```

Then

```text
K p_i = K q_i                                      (7)
```

for at least one `i in {1,2,3}`.  In particular, (5)--(6) are impossible
when `p_i,q_i` are linearly independent for every `i`.

The proof occupies Sections 2--5.  It is tensorial: no algebraic closure,
genericity, finite enumeration, or division by a parameter is used.

## 2. A nonzero permanent supplies an all-component syzygy

Let

```text
H=span_K(h_x,h_y,h_r) subset kernel(D_C).            (8)
```

Every coordinate projection `H -> V_i` is nonzero.  Otherwise every term of
(4) would vanish in its `i`-th factor, contrary to `Q!=0`.  The triples whose
`i`-th component is zero form a proper linear subspace of `H`.  Since a
characteristic-zero field is infinite, three proper linear subspaces cannot
cover `H`.  Hence there is

```text
k=(a,b,c) in H,       a!=0, b!=0, c!=0.             (9)
```

Apply the quotient `V_1 -> V_1/K a` to `D_C(k)=0`.  The two surviving terms
have the form

```text
b tensor y+x tensor c=0.                            (10)
```

The elementary rank-one equality in (10) says `x` is a multiple of `b` and
`y` is the opposite multiple of `c`.  Lifting from the quotient gives vectors

```text
s in V_1,       d in V_2,       e in V_3            (11)
```

such that

```text
C_12=a tensor d+s tensor b,
C_13=a tensor e-s tensor c,
C_23=-b tensor e-d tensor c.                        (12)
```

Substitution proves both (12) and the companion syzygy

```text
l=(s,-d,e) in kernel(D_C).                          (13)
```

For triples `x,y,z`, put `(t_1,t_2,t_3)=(x,y,z)` and write their mixed
alternating tensor as

```text
Alt(x,y,z)
 =sum_(sigma in S_3) sign(sigma)
    (t_(sigma(1)))_1 tensor (t_(sigma(2)))_2
                         tensor (t_(sigma(3)))_3.    (14)
```

where the three displayed triples are placed into the three root factors.
Direct expansion of (12) gives

```text
D_C(m)=-Alt(k,l,m).                                 (15)
```

Thus the kernel and image of `D_C` are controlled by one pair of triples.  If
`l` were proportional to `k`, substitution in (12) would make all three
blocks zero, contradicting (5).  Hence `W=span_K(k,l)` is a two-plane.

## 3. The three-nonzero-block normal forms

Assume first that all three blocks in (2) are nonzero.  Let `U=K^2` with
basis `u_0,u_1`, and define the coordinate-projection maps

```text
F_i:U -> V_i,
F_i(u_0)=k_i,       F_i(u_1)=l_i.                   (16)
```

Thus `rank(F_i)` is the rank of the restriction `W -> V_i`.  The pair
alternants

```text
W_ij=F_i(u_0) tensor F_j(u_1)
     -F_i(u_1) tensor F_j(u_0)                      (17)
```

are, up to sign, `C_12,C_13,C_23`.  Hence every `W_ij` is nonzero.  Put
`rho_i=rank(F_i)`.  After permuting the root factors, changing the basis of
`U`, and changing bases in the `V_i`, the only possibilities are the four
rows below.  Here `v_i` denotes the first basis vector of a rank-one target.

```text
(rho_1,rho_2,rho_3)    F_1(u)       F_2(u)       F_3(u)

(2,2,2)                u            u            u
(1,2,2)                u_0 v_1      u            u
(2,1,1)                u            u_0 v_2      u_1 v_3
(1,1,1)                u_0 v_1      u_1 v_2      (u_0+u_1)v_3.   (18)
```

For the `(2,1,1)` row, nonvanishing of `W_23` says that the two rank-one
functionals are independent.  For the `(1,1,1)` row, all three functionals
are pairwise nonproportional; three distinct points of the projective line
give the last normal form.  These observations prove that (18) is exhaustive
over `K`, not merely after extending scalars.

Expanding (15) in each row of (18) gives

```text
kernel(D_C)={ (F_1(u),F_2(u),F_3(u)) : u in U }.    (19)
```

For completeness, if `m_i=(alpha_i,beta_i)` in the displayed bases, the
kernel equations are respectively

```text
(2,2,2): m_1=m_2=m_3;
(1,2,2): beta_1=0, alpha_1=alpha_2=alpha_3,
           beta_2=beta_3;
(2,1,1): alpha_1=alpha_2, beta_1=alpha_3,
           beta_2=beta_3=0;
(1,1,1): beta_1=beta_2=beta_3=0,
           alpha_3=alpha_1+alpha_2.                 (20)
```

Thus every `h_t` in (6) is `F(u_t)` for one `u_t in U`.

### Lemma 2 (pure tensors in the alternating image)

In the `(2,2,2)` row of (18), `image(D_C)` contains no nonzero pure tensor.
In every other row, if a nonzero pure tensor belongs to `image(D_C)`, one of
its factor lines equals the fixed image line of a rank-one `F_i`.

### Proof

In the full-rank row, identify all three `V_i` with `U` through `F_i`.  Let

```text
mu:U tensor U tensor U -> Sym^3(U)                  (21)
```

be commutative multiplication.  Every summand in (15) contains the
alternant `u_0 tensor u_1-u_1 tensor u_0` in two slots, so

```text
mu(image(D_C))=0.                                   (22)
```

But `mu(x tensor y tensor z)=xyz` is nonzero for nonzero `x,y,z`, because
the symmetric algebra of `U` is a polynomial domain.  Hence no nonzero pure
tensor lies in the image.

In the `(1,2,2)` row, quotient the first factor by `K v_1`.  The image of
(15) becomes

```text
(m_1 mod K v_1) tensor W_23.                        (23)
```

The tensor `W_23` has matrix rank two because `F_2,F_3` are isomorphisms.
If a pure tensor in the image had first factor transverse to `v_1`, its
nonzero quotient would have matrix rank one in factors two and three,
contradicting (23).  Its first factor is therefore in `K v_1`.

In the `(2,1,1)` row, project factors two and three modulo `K v_2,K v_3`.
Every term of (15) dies.  A pure tensor transverse to both fixed lines would
survive, so every image pure tensor uses `K v_2` or `K v_3`.  In the
`(1,1,1)` row, projecting all three factors modulo their fixed lines gives
the same conclusion for at least one factor.  This proves the lemma.

Now apply (19) to the permanent (6).  At every rank-one position `i`, every
summand of (4) has its `i`-th factor in `K v_i`.  Since `Q` is nonzero and
pure, uniqueness of the factor lines of a decomposable tensor gives

```text
K q_i=K v_i.                                        (24)
```

The full-rank row contradicts (5) outright by Lemma 2.  Every other row
forces a factor of `P` to equal one of the lines in (24).  Thus (7) holds
whenever all three blocks are nonzero.

## 4. A vanishing block

Suppose, after permuting factors, that `C_23=0`.  Equation (12) then says

```text
b tensor e=-d tensor c.                             (25)
```

Hence `d=lambda b` and `e=-lambda c` for one scalar `lambda`.  Replacing
`s` by `s+lambda a` reduces (12) to

```text
C_12=s tensor b,       C_13=-s tensor c,
C_23=0.                                             (26)
```

If the new `s` is zero, every block is zero and (5) is impossible.  Otherwise

`C_12,C_13` are both nonzero and

```text
kernel(D_C)=V_1 direct-sum K(0,b,c),                (27)

image(D_C)=K s tensor
             (b tensor V_3+V_2 tensor c).           (28)
```

Every triple in (27) has the form `(u,lambda b,lambda c)`.  Therefore a
nonzero permanent of three such triples has second and third factor lines
`K b,K c`.  On the other hand, quotienting the last two factors of (28) by
`K b,K c` shows that every pure tensor in (28) has second factor `K b` or
third factor `K c`.  Thus (7) again holds.  If a second block in (26)
vanished, nonzero `b,c` would force the new `s=0`, and then all three blocks
would vanish.  Equivalently, given the all-component syzygy (9), exactly two
blocks cannot vanish while the third remains nonzero.  If all three vanish,
(5) is impossible.  The other choices of zero block follow by permutation.

Sections 2--4 exhaust all block patterns and prove Theorem 1.

## 5. Application to the S2O residual

In the S2O notation, the two pure tensors are

```text
P=p_1 tensor p_2 tensor p_3,
Q=z_1 tensor z_2 tensor z_3,                         (29)
```

where `(p_i,z_i)` is a basis of the binary root space `V_i`.  Thus their
factor lines are transverse at all three positions.  Theorem 1 proves:

### Corollary 3 (the S2O binary residual is empty)

There are no blocks `C_12,C_13,C_23` satisfying simultaneously

```text
p_1 tensor p_2 tensor p_3 in image(D_C)
```

and

```text
Perm(h_x,h_y,h_r)=z_1 tensor z_2 tensor z_3
```

for `h_x,h_y,h_r in kernel(D_C)`.

By the exact pullback theorem, a common-shore realization of any one of the
eight normalized S2M controls would produce precisely such binary data.
Therefore all eight controls are outside the common-shore companion
matching-sum image.

This conclusion is only about the eight displayed ambient controls.  Those
controls prove coordinatewise independence from degree, target, rank, and
normalization data; they are not an exhaustive parametrization of every way
a realized balanced incidence could fail the pair gate.  Their exclusion
therefore removes the known sharp controls from the physical image but does
not prove the universal S2 pair-pole theorem.

## 6. Sharpness of the shared-factor conclusion

The transversality hypothesis cannot be dropped.  In the `(1,2,2)` normal
form take

```text
F_1(u_0)=v_1, F_1(u_1)=0,       F_2=F_3=identity.   (30)
```

Three proportional kernel triples `F(u_0)` have polarized permanent

```text
6 v_1 tensor u_0 tensor u_0.                        (31)
```

After rescaling one triple, this is any chosen nonzero tensor on those
factor lines.  Meanwhile (15), with only the third component of `m` equal to
`-u_1`, gives

```text
v_1 tensor u_1 tensor u_1 in image(D_C).            (32)
```

Both tensors are pure and they share exactly the first factor line.  Thus
Theorem 1 proves the sharp geometric obstruction needed by S2O, not a false
claim that pure image and pure permanent tensors can never coexist.

## 7. Proof-topology consequence

The exact boundary is now

```text
eight normalized full-row controls                         PROVED (S2M);
exact m=3 common-shore image formulas                       PROVED (S2N);
common binary pullback                                      PROVED (S2O);
binary transverse syzygy--permanent residual                EMPTY HERE;
common-shore realization of the eight controls              EXCLUDED HERE;
universal pair-jet failure on every realized incidence      OPEN;
higher-order physical matching-sum recurrences              OPEN.       (33)
```

No physical graph is reconstructed, and no inference from shared physical
variables to support-difference lattice coupling is made.  The result acts
only on the common-shore tensor incidence isolated by S2N--S2O.  The
all-balanced rank-drop branch and every unrelated proof-DAG leaf retain their
previous status.  Global Krenn--Gu remains **UNRESOLVED**.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_full_sensor_common_shore_binary_syzygy_permanent_residual_obstruction.py
python -I claims/arbitrary-order/audit_balanced_full_sensor_common_shore_binary_syzygy_permanent_residual_obstruction.py
python -m py_compile claims/arbitrary-order/verify_balanced_full_sensor_common_shore_binary_syzygy_permanent_residual_obstruction.py claims/arbitrary-order/audit_balanced_full_sensor_common_shore_binary_syzygy_permanent_residual_obstruction.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_full_sensor_common_shore_binary_syzygy_permanent_residual_obstruction.py claims/arbitrary-order/audit_balanced_full_sensor_common_shore_binary_syzygy_permanent_residual_obstruction.py
```

The primary verifier builds the four canonical alternating maps with SymPy,
checks their exact kernels, checks the quotient/rank certificates used in
Lemma 2, verifies the one-zero-block kernel and tangent image, and replays the
sharp shared-factor example.

The independent audit imports neither SymPy nor repository code.  It uses a
separately written rational matrix implementation to rebuild all five maps,
verify their ranks and kernel bases, check every support-level quotient
certificate, and evaluate the sharp permanent directly from its six terms.
The scripts audit the displayed normal forms; the written quotient and
normal-form arguments supply the arbitrary-field theorem.
