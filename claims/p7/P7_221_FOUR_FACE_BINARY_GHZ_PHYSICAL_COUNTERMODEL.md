# The four-face binary GHZ tensor is physically realizable

## Status

**Exact countermodel to a proposed degree-five separator.**  Wick-deconvolving
the formal `2+2+1` ledger and applying the four-face functional

```text
Lambda(Phi)=Phi_125ab-Phi_145ab-Phi_235ab+Phi_345ab    (1)
```

gives

```text
Lambda(Phi_formal)=(rho-2)(D_0+D_1),      rho^2=21.     (2)
```

Thus the contraction is a binary seven-site GHZ tensor.  Nevertheless, one
explicit physical seven-core graph realizes (2) as a degree-five,
one-internal-edge hafnian response.  More strongly, it realizes the complete
non-`D_2` part of the four-face tuple:

```text
(Phi_125ab,Phi_145ab,Phi_235ab,Phi_345ab)
   =((rho-2)D_0,0,0,(rho-2)D_1).                        (3)
```

No mixed local-colour word occurs.  Consequently no polynomial or covariant
of the single contracted tensor (2) can separate physical local-colour
graphs from the formal global-idempotent model: the proposed point is itself
in the physical image.

The construction does **not** realize the common `D_2` baseline present in
all four formal faces, so it is not a countermodel for the full four-face
tuple or for the complete ledger.

## 1. Exact formal tensor on the four faces

Let `D_c=e_c^(tensor 7)`.  The exact squarefree Wick transform of the formal
ledger gives

```text
                    125ab       145ab       235ab       345ab
colour 0:           rho-2          0            0            0
colour 1:              0           0            0         rho-2
colour 2:        (rho+1)/7   (rho+1)/7    (rho+1)/7    (rho+1)/7. (4)
```

The alternating signs in (1) cancel the colour-2 row of (4), proving (2).
Equivalently, the full formal four-tuple is

```text
((rho-2)D_0+tD_2, tD_2, tD_2, (rho-2)D_1+tD_2),
t=(rho+1)/7.                                             (5)
```

## 2. The physical graph

Take seven core vertices `u_1,...,u_7`, with local colour space

```text
E_i=<e_0,e_1,e_2>                                       (6)
```

at `u_i`.  There are only two nonzero core--core tensors:

```text
A_12=(rho-2)e_0 tensor e_0,
A_34=(rho-2)e_1 tensor e_1.                             (7)
```

The nonzero core--terminal incidence vectors are

```text
u_3--1 :  e_0,        u_4--2 :  e_0,
u_5--5 :  e_0,        u_6--a :  e_0,
u_7--b :  e_0,

u_1--a :  e_1,        u_2--b :  e_1,
u_5--3 : -e_1,        u_6--4 : -e_1,
u_7--5 :  e_1.                                         (8)
```

All omitted incidences and core edges are zero.  The `e_2` direction is
unused; retaining it makes (6) the same three-colour local space as the
physical problem.

For a five-terminal set `S`, the no-terminal-edge response is the exact
one-edge Laplace sum

```text
Phi_S=sum_(i<j) A_ij per L[Z minus {i,j},S].             (9)
```

Only the two edges in (7) can contribute.

## 3. Why the two permanent matchings are unique

For `S=125ab`, the edge `u_1u_2` leaves the five incidence rows
`u_3,...,u_7`.  Their only possible bijection to `S` is

```text
u_3->1, u_4->2, u_5->5, u_6->a, u_7->b.                (10)
```

Every vector in (10) is `e_0`, so this contribution is `(rho-2)D_0`.
The edge `u_3u_4` cannot contribute: after the forced assignments
`u_1->a,u_2->b`, the row `u_6` has no unused terminal in `125ab`.

For `S=345ab`, the edge `u_3u_4` has the unique bijection

```text
u_1->a, u_2->b, u_5->3, u_6->4, u_7->5.                (11)
```

The two minus signs in (8) cancel, so (11) contributes `(rho-2)D_1`.
The edge `u_1u_2` cannot contribute because its remaining rows `u_3,u_4`
require terminals `1,2`.

For `S=145ab`, the edge `u_1u_2` again fails at `u_4`, while for
`S=235ab` it fails at `u_3`.  For the edge `u_3u_4`, the forced assignments
`u_1->a,u_2->b` leave respectively no terminal `1` source, or no available
incidence for `u_6`.  Both middle responses therefore vanish.

This proves (3) without listing local-colour words: uniqueness of the two
terminal matchings makes both nonzero tensors monochromatic from the outset.
Applying (1) to (3) proves (2) in the physical image.

### Theorem 1 (failure of the contracted degree-five separator)

Let `X` be the image of the physical seven-core, one-internal-edge response
map on the four-face contraction (1).  Then

```text
(rho-2)(D_0+D_1) in X.                                  (12)
```

Hence every polynomial that vanishes on all physical contracted responses
also vanishes at the formal tensor (2).

Proof.  Equations (7)--(11) give an actual parameter point of the physical
map whose image is (12).  Evaluation of any polynomial vanishing on the
image at that parameter point is zero.

## 4. Geometric interpretation

The global algebra `K^3` produces (2) by the idempotent rule
`epsilon_c epsilon_d=0` for `c!=d`.  The physical countermodel instead uses
terminal-support forcing: the two core edges select two different complements,
and each complement has one terminal perfect matching.  Thus the same GHZ
correlation is produced without a global copy/idempotent tensor.

This is a concrete image point, not a dimension or closure argument.  That
distinction matters for tensor-network state spaces, whose parametrized
images need not be Zariski closed; see Landsberg--Qi--Ye, *On the geometry of
tensor network states*, arXiv:1105.4449.

## Scope wall

Proved:

- the exact formal contraction (2);
- a physical one-edge realization of that contraction;
- a physical realization of the non-`D_2` four-face tuple (3);
- therefore, no separator depending only on the contracted tensor (2).

Not proved:

- a physical realization of the common `D_2` baseline in (5);
- a physical realization of the full four-face tuple;
- absence of a separator using the uncontracted four faces, joint degree-one
  and degree-five data, degree seven, or the complete ledger;
- a common-core realization or obstruction for arbitrary pure scalar lifts;
- the `P_7 -> Delta_3` restriction or the Krenn--Gu conjecture.

The exact boundary is

```text
single four-face contraction:       PHYSICALLY REALIZED;
non-D2 four-face component:         PHYSICALLY REALIZED;
full four-face formal tuple:        UNKNOWN;
full physical common core:          UNRESOLVED.          (13)
```

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_221_four_face_binary_ghz_physical_countermodel.py
python claims/p7/audit_p7_221_four_face_binary_ghz_physical_countermodel.py
python -m py_compile verify_p7_221_four_face_binary_ghz_physical_countermodel.py audit_p7_221_four_face_binary_ghz_physical_countermodel.py
uv run --with ruff ruff check verify_p7_221_four_face_binary_ghz_physical_countermodel.py audit_p7_221_four_face_binary_ghz_physical_countermodel.py
```

The primary verifier reconstructs (4) from the formal cofactor ledger and
the common terminal block, then evaluates the sparse tensor-valued physical
response (9).  The independent audit repeats both calculations with exact
rational-pair arithmetic in `Q[rho]/(rho^2-21)` and imports neither SymPy nor
the primary verifier.  Neither replay enumerates local-colour words, graph
supports, or parameter families.
