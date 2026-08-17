# Constant target-module and six-port physical Wick review

Date: 2026-08-17

Global status: **UNRESOLVED**

Reviewed claims:

- [`Four-root constant target-module selector quotient and maximum-root sharpness`](../../claims/arbitrary-order/FOUR_ROOT_CONSTANT_TARGET_MODULE_SELECTOR_QUOTIENT_AND_MAXIMUM_ROOT_SHARPNESS_THEOREM.md)
- [`Six-port physical Wick selector, two-active all-subwindow closure, and deeper response`](../../claims/arbitrary-order/SIX_PORT_PHYSICAL_WICK_SELECTOR_TWO_ACTIVE_ALL_SUBWINDOW_AND_DEEPER_RESPONSE_THEOREM.md)

## 1. Review question

The package was attacked against three distinct questions.

1. Does a full fixed-`Q` companion equation give a noncircular, exact
   constant target-attachment criterion with every nuisance label retained?
2. Does the `h=0` six-port Wick map give bounded direct-pair selectors beyond
   its generic determinant-open branch, including exact singular controls and
   all fifteen `K4` subwindows?
3. Do target-diagonal four-port rows force a genuine deeper mixed response on
   the fully two-active locus, without silently assuming the row is already
   attached to the GHZ target?

The review kept graph-side companion incidence, target incidence, physical
response identities, witness-locus forcing, and permanent extraction
separate.  Agreement among research lanes was not treated as proof.

## 2. Exact module-selector theorem

For four roots, `B=Q disjoint-union U`, `|Q|=2`, `|U|=4`, and fixed nonzero
residual contractions, the full deck domain has dimension `2079`.  For a pair
`S subset U` or `S=U`, the theorem defines

```text
A_S(lambda)=(lambda tensor id_S) Gamma_Q,
Theta_S=Gamma_Q-g_S tensor P_S,
N_S=span of every L_S coefficient slice of Theta_S.  (1)
```

The exact constant-open-port selector criterion is

```text
P_S in im A_S
  iff lambda(g_S)=1 for some lambda in N_S^perp
  iff [g_S]!=0 in L_S^*/N_S.                         (2)
```

The selector may depend on the fixed graph, root data, residual contractions,
and `Gamma_Q`.  It may not depend on the open port coordinates, be chosen
only after observing a diagonal output, or arise merely from a function-field
inverse.  Equation (2) is an identity on every labelled deck coordinate.

Failure of (2) is module nonmembership.  It does not imply an unrestricted
sensor kernel, a second regular hafnian deck, or a physical graph fibre.

### Sharp incidence controls

On the clean four-root chart, scaling every root--root block by `t` gives

```text
g_S=t a_(U-S)b_S tensor epsilon_(U-S)       for |S|=2,
g_U=3t^2 b_1b_2b_3b_4.                              (3)
```

Each is a unique no-`c` root-word pivot.  For `t!=0`, all seven exact
selectors exist simultaneously.  Adding `c`-letter helper rows preserves
those pivots while installing triple blockers; the assigned-edge and
outside-coordinate argument makes the displayed root set maximum over `C`.

A separate maximum-root triple-blocker chart has `g_U!=0`, but the nuisance
label `I=Q` contributes a tensor product of four identity blocks.  Its `81`
port-coordinate slices are all `81` root basis words, so `N_U=L_U^*` and no
four-port selector exists.  Therefore maximum roots plus blocker saturation
neither force nor forbid attachment.  Neither chart is asserted to meet the
hypothetical-witness locus.

## 3. Exact six-port Wick theorem

For one fixed scalar word on six ports, complementing four-set rows gives

```text
D_K(e,f)=K_(U-(e union f))   if e intersect f=empty,
          0                  otherwise.              (4)
```

This is the already-known residual-hafnian Hessian matrix.  The new physical
rank-two discriminant for `K_ij=a_i b_j+b_i a_j` is the displayed five-term
polynomial in `A,s_1,...,s_6` in the theorem.

The proof was checked at four levels.

1. Direct subset counting gives `J D=L`, with `J^2=I` and `det J=-1`, reducing
   the determinant to one fixed `6 x 6` matrix.
2. The determinant is symmetric, homogeneous of degree fifteen, and has
   individual variable degree at most five.  The corresponding monomial-
   symmetric space has dimension `32`.
3. The primary verifier's `32 x 32` evaluation matrix has determinant
   `188237 mod 1000003`; exact integer determinants agree with the formula at
   all `32` points.  Unisolvence proves the polynomial identity, rather than
   providing samples.
4. On the dense `a_i!=0` chart,
   `D_K=A diag(a_e^(-1))D(t)diag(a_e^(-1))` and
   `product_e a_e=A^5`; polynomiality extends the homogenized identity across
   every coordinate wall.

### Singular and common-row controls

After removing nonzero vertex scales, the two-shore ranks for
`6+0,5+1,4+2,3+3` are respectively `15,10,15,10`.  In `5+1`, every
singleton-to-majority pair has the exact ten-row selector

```text
m_(b,i)=(1/(6 alpha))(
  sum_(T contains i) z_({b} union T)
  -sum_(T not contains i) z_({b} union T)).          (5)
```

The remaining kernel is the five-dimensional five-shore inclusion kernel.
In `3+3`, the kernel is four cross-matrix rectangle cycles plus the weighted
internal direction

```text
alpha sum_(e in binom(A,2))e_e
-beta sum_(e in binom(B,2))e_e.                      (6)
```

Every coordinate varies on that isolated word.  This is not a global
obstruction: on every two-shore union of at least seven ports, each pair lies
in an invertible `6+0` or `4+2` subset or has the `5+1` selector (5).  In a
`6+1` union, every six-window containing a fixed cross pair is singular, yet
(5) still selects it.  Thus nonzero square minors are sufficient but not
necessary for common-row identification.

## 4. Tensor polarization and depth six

On the fully two-active nonvanishing line locus,

```text
K_ij(0,0)=alpha x_i x_j,
K_ij(1,1)=beta y_i y_j,                              (7)
```

with every other coefficient zero.  Each desired direct-pair coefficient
chooses its own six-port word:

- a same-active coefficient uses an invertible `4+2` word;
- a different-active or active--inactive coefficient uses (5); and
- an inactive--inactive coefficient uses one mixed four-port row.

This recovers every coefficient of every direct pair block from the fifteen
four-port tensors.  It bypasses rather than removes the fixed-word `3+3`
kernel.

If all attached four-port tensors are target-diagonal, the reconstructed
direct layer is diagonal in the same two colours.  Its mixed `2+2` equations
propagate on the connected bipartite double cover of `KG(6,2)` and force

```text
B^0=cK^0,                    B^1=-cK^1.              (8)
```

For a `0^2 1^4` six-port word, exact matching partition then gives

```text
z_6(0_e^2,1_R^4)=-c^2 k_e^0 C(K_R^1),
C(K_R^1)=3 beta^2 product_(i in R)y_i.               (9)
```

A nonzero pure four-port response forces `c!=0`, so (9) is nonzero.  It is an
actual GHZ mixed-coefficient contradiction only if the same physical `z_6`
tensor has already been attached by a legal constant selector.  The Wick
inverse cannot manufacture that attachment.

## 5. Hostile attacks and verdict

The fresh hostile review attacked:

- circular selectors chosen after target evaluation;
- contraction/order errors in `Gamma_Q`, `P_S`, and the `2079` coordinates;
- helper-row contamination of the seven clean pivots;
- promotion of a module nonmembership certificate to a graph fibre;
- silent extension of complex maximum-root constructions to arbitrary fields;
- scalar `15 x 15` claims promoted to full tensor supply;
- the determinant formula, coordinate walls, and unisolvent logic;
- the weighted sign in the `3+3` kernel;
- failure of a fixed `3+3` word to identify any coordinate;
- incomplete tensor-word coverage, six-port multiplicities, and the sign in
  (9);
- selected-window agreement promoted to full `M,Z` agreement;
- missing legal attachment of the `z_2,z_4,z_6` rows; and
- any inferred third-colour or permanent consequence.

Repairs made before the frozen review included the weighted kernel (6), the
full tensor polarization cover, the `32`-point identity certificate, explicit
diagonal scaling across coordinate walls, the exact count of fifteen `z_2`
tensors, and complex-field scope for the maximum-root controls.

Frozen hostile verdict: **ACCEPT**.  There were no P0 or mathematical P1
findings on the frozen formatted snapshot.  This verdict is conditional only
on assembling this review artifact and passing the repository validation
floor.

## 6. Evidence independence

The four-root primary enumerates root partial matchings and root-to-outside
assignments for all `31` companion columns and checks all seven selectors on
every one of the `2079` deck basis coordinates.  Its no-import audit derives
the supports from injection types and separately reconstructs the full
identity nuisance image.

The six-port primary uses SymPy for the symbolic `J D=L` identity, exact
unisolvent certificate, shore determinants, selector row spaces, kernel, and
response expansions.  Its no-import audit uses standard-library `Fraction`
arithmetic, Bareiss determinants, a separately written four-row recurrence,
direct perfect-matching enumeration, and exhaustive coefficient-word and
shore-count controls.  It imports neither the primary nor SymPy.

The scripts audit the displayed finite identities.  The arbitrary-field
module separation, matching partitions, maximum-root support argument,
common-row cover, and target-interface implications are proved in writing.

## 7. Frontier effect and exact remainder

The package adds two live conditional/boundary nodes.

- `GLD5` is the exact full-module attachment quotient and proves that the
  maximum-root triple-blocker incidence stratum meets both selector and
  nonselector branches.
- `GLD6` is the first all-fifteen-`K4` coefficientwise Wick supply theorem on
  the fully two-active `h=0` line locus and a conditional mixed depth-six
  detector.

The following remain **UNKNOWN**:

- whether all seven quotient classes survive on every relevant witness;
- whether the full mixed equations exclude every bad quotient locus;
- legal constant same-`Q` attachment of all required `z_2,z_4,z_6` tensors;
- whether every remaining two-active witness chart has the nonvanishing line
  form and a nonzero pure four-port response;
- the general simultaneous all-minors-singular physical/witness locus;
- any third-colour activity conclusion; and
- any weighted-diagonal permanent restriction.

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 8. Frozen hashes and validation contract

The accepted mathematical surfaces are pinned by:

```text
F6EFA9B304553F2E5294D4EBAC415ECB1E9F3AA831C3CAF87F332536B0DEF798  FOUR_ROOT_CONSTANT_TARGET_MODULE_SELECTOR_QUOTIENT_AND_MAXIMUM_ROOT_SHARPNESS_THEOREM.md
6524D8AA224643ACF4CCB8C1334BCA6007704A89B90E23B08B65DB907C9B04FC  verify_four_root_constant_target_module_selector_quotient_and_maximum_root_sharpness.py
8AAD1A833D2119CD69F76C7B5CF39E39913F97269F0357DDEC17D083230D5BD5  audit_four_root_constant_target_module_selector_quotient_and_maximum_root_sharpness.py
8F1847F3626FB3FD4AAEE479AE5C141E067E56F3611CDFB768CFEB639C378A53  SIX_PORT_PHYSICAL_WICK_SELECTOR_TWO_ACTIVE_ALL_SUBWINDOW_AND_DEEPER_RESPONSE_THEOREM.md
0E8C3A775B713F462BCAC0EFE4F157084C5782C3609D3DC0C50E8A960BDD9161  verify_six_port_physical_wick_selector_two_active_all_subwindow_and_deeper_response.py
8C81BC6650FBD27DD7B502F2F67B4A1114870AB3480FB9ADF469CF2AAFF29768  audit_six_port_physical_wick_selector_two_active_all_subwindow_and_deeper_response.py
```

Before publication, the index-complete candidate must pass:

- all four focused primary/audit commands;
- Ruff check and format check;
- `py_compile`;
- `python check_hygiene.py` on the staged tree;
- `tests.test_migration_tools`;
- `tests.test_fourteen_vertex_cycle_cover_lattice`;
- the link rewriter with zero diff; and
- cached and unstaged `git diff --check`/cleanliness checks.

The staged candidate passed the complete contract:

- both four-root commands: PASS;
- both six-port commands: PASS, including the `32`-point unisolvent identity
  certificate;
- Ruff check and format check: PASS;
- `py_compile`: PASS;
- `python check_hygiene.py`: PASS (`2116` Python files and `1254` Markdown
  files checked; `227/227` curated ledger hashes valid);
- `tests.test_migration_tools`: `191/191` PASS;
- `tests.test_fourteen_vertex_cycle_cover_lattice`: `14/14` PASS;
- link rewrite: zero link, replay, file, or ledger changes; and
- cached and unstaged diff checks: clean.

Final repository-wide validation: **PASS**.  These checks certify only the
scoped theorems above.  Universal witness-locus attachment and the global
Krenn--Gu conjecture remain **UNRESOLVED**.
