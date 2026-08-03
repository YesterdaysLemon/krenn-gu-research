# Root `m=7` simultaneous rank-one hidden-pair realization no-go

## Status

This is an exact characteristic-zero countermodel to one proposed next
lemma in the five-root/two-residual tangent cell.  Common root-edge
hafnians, a rank-two all-root frame, coprime all-root monomials, and the
sharp two-active-sector condition do **not** force any four-root hidden
pair `(h_k,q_k)` to have rank two.

The construction is a legal tangent-jet realization and uses the same
root-edge blocks simultaneously in every deletion sector.  It is not a
full realization of all lower cofactors or of `P_7 -> Delta_3`.  Its role is
therefore negative but decisive: any proof of a rank-two hidden pair must
use additional lower-cofactor values, not just common-edge consistency and
the all-root frame.

## Construction

On the binary tangent plane at root `r_i`, let `x_i,y_i` be independent
linear forms.  Choose nonzero scalars `a,b,c,d` and set the only nonzero
root--root tangent blocks to

```text
E_12=a x_1 x_2,       E_34=b x_3 x_4,
E_03=c y_0 y_3,       E_24=d y_2 y_4.                (1)
```

For residual endpoint `q_t`, put

```text
L_(0t)=A_t x_0,       L_(1t)=B_t y_1,                (2)
L_(kt)=0 for k=2,3,4.
```

Assume

```text
delta=A_0 B_1-A_1 B_0 !=0.                           (3)
```

If desired, also impose `sigma=A_0 B_1+A_1 B_0 !=0`; for example
`(A_0,A_1,B_0,B_1)=(1,1,1,2)` has `delta=1,sigma=3`.
Allow an arbitrary residual--residual value

```text
B_(q_0q_1)(z_0,z_1)=r.                               (4)
```

## The five internal four-root forms

Let `h_k` be the hafnian on the four roots other than `r_k`.  The three-term
four-vertex hafnian identity and (1) give

```text
h_0=ab x_1 x_2 x_3 x_4,
h_1=cd y_0 y_2 y_3 y_4,
h_2=0,
h_3=0,
h_4=ac y_0 y_3 x_1 x_2.                              (5)
```

The all-root form with endpoint `q_t` is obtained by exposing the root
paired to that endpoint:

```text
g_t=sum_k L_(kt) h_k
   =A_t ab X+B_t cd Y,                               (6)
X=product_i x_i,             Y=product_i y_i.
```

By (3), `g_0,g_1` span `X,Y`.  Thus the all-root frame has rank two, and
the two endpoint-active internal sectors are exactly `k=0,1`.  Their forms
are coprime.  This realizes, rather than merely formalizes, the sharp
two-active conclusion of the four-root hidden-pair theorem.

## The two-endpoint forms

Let `q_k` be the hafnian on the four roots other than `r_k`, together with
both residual endpoints.  Expand first according to whether the residuals
pair together.  Equations (1)--(4) give

```text
q_0=r h_0,
q_1=r h_1,
q_2=sigma b x_0 y_1 x_3 x_4,
q_3=sigma d x_0 y_1 y_2 y_4,
q_4=r h_4.                                            (7)
```

Consequently the five simultaneous hidden pairs are

```text
(h_0,rh_0), (h_1,rh_1), (0,q_2), (0,q_3), (h_4,rh_4). (8)
```

The specialization `r=0` gives the earlier zero entries, while `q_2,q_3`
also vanish when `sigma=0`.  Every pair in (8) spans at most one scalar-form
dimension.  There is no rank-two hidden pair despite the rank-two all-root
frame.

## Legal tangent realization

Take the fixed root vector to be `rho=(1,1,1)` and, on every root space,
realize

```text
x_i=e_0^*-e_2^*,       y_i=e_1^*-e_2^*.              (9)
```

Both forms vanish at `rho`.  Each block in (1) is therefore a genuine
tangent--tangent bilinear block.  Realize (2) as
`B_(r_iq_t)=ell_(it) tensor eta_t`, where `eta_t(z_t)=1`; it is a genuine
root-tangent/residual-value block and also vanishes at the fixed root.
These blocks preserve the fixed root zero-jet.  The root--residual blocks
do change first root-tangent derivatives, while the root--root blocks first
appear at higher root order; both effects are exactly the jet data used in
(5)--(7).  No claim is made that this countermodel preserves an independently
prescribed full first-jet frame.

This proves common-edge tangent realizability only.  It does not assert
that arbitrary prescribed complementary blocker cofactors extend to one
global graph.

## Verification

Run:

```text
uv run --with sympy python verify_root_m7_simultaneous_rank_one_hidden_pair_realization_nogo.py
python audit_root_m7_simultaneous_rank_one_hidden_pair_realization_nogo.py
```

The primary verifier reconstructs all five four-root hafnians, expands the
two-endpoint forms symbolically, and checks the all-root determinant.  The
audit repeats the calculation with an independent sparse-polynomial
implementation and fixed rational endpoint constants.  Both are bounded
symbolic checks of the displayed identities; no support search is used.

## Boundary

```text
common root-edge tangent realization:       YES;
rank-two all-root frame:                     YES;
coprime endpoint-active internal sectors:   YES, EXACTLY TWO;
rank of every hidden pair:                  AT MOST ONE;
rank two forced by these hypotheses:        FALSE;
extension to all lower blocker cofactors:   UNKNOWN;
full P_7 restriction:                       NOT CONSTRUCTED;
global Krenn--Gu conjecture:                 UNRESOLVED.
```
