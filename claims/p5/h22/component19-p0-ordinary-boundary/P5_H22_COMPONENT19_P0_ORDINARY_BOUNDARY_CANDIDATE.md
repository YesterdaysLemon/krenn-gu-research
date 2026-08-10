# Component 19 weighted `H22` on the finite ordinary `p=0` boundary — REFUTED FROZEN CERTIFICATE

```yaml
role: construction
date_utc: 2026-08-01T16:03:06Z
git_commit: 7a3eea50e311a163765750fa5f22f9d2b5c1b98e
claim_label: REFUTED
scope: component 19 finite ordinary p=0 boundary on q*phi*(q-phi)!=0
inputs: paths and SHA-256 hashes emitted by the bounded replay
method: regular intrinsic basis, exact characteristic-zero permanents and pair minors, finite/infinity elimination, complete shared kernel, projected and stacked one-marked minors
command: uv run --with sympy python derive_p5_h22_component19_p0_ordinary_boundary_candidate.py
outputs: this report, p5_h22_component19_p0_ordinary_boundary_certificate.json, and the bounded replay
limitations: frozen construction replay fails exact assertions; no H22 conclusion from this artifact; zero/projectivized/valuative boundaries deferred
```

## Replay verdict

**REFUTED as a replayable certificate.**  The final serialized construction
was not rerun by its author.  Root replay found two exact mismatches:

- the frozen `D23`, mode-two row-`0127` minor used `phi*C+E`, while direct
  reconstruction gives `C+phi*E`;
- after correcting that formula, the advertised `phi=1` stacked row witness
  on rows `(0,1,3,8,14)` is identically zero, not the stated nonzero
  polynomial.

The regular basis, tensor support, and pair geometry below agree with two
independent reconstructions, but this artifact does not certify its proposed
uniform weighted-`H22` obstruction or its claimed exhaustive residue.  The
separate proof-B theorem and no-import verifier are the only promotable
sources for the smaller obstruction open.

## Frozen ordinary statement

At `p=0`, use the regular basis

```
alpha=(Abar,B,Bbar,Abar),
beta =(Bbar+qB,A,A,B+phi Bbar).
```

Its mode-zero change has determinant `1`.  After every affine marking, the
only pure coefficient is

`T1111=4(q-phi)`.

Thus the ordinary tensor is nonzero off `q=phi`; it is not a transverse-zero
boundary.  Direct pair minors give generic profile

`(rank01,rank02,rank03,rank12,rank13,rank23)=(3,3,4,3,3,3)`.

On `q*phi=1`, edge `03` drops exactly to rank three and remains all-pair-open.
Consequently the exact finite ordinary nonzero all-pair-open locus is

`q*phi*(q-phi) != 0`.

## Exact shared branch

Finite/infinity elimination leaves only the finite shared orientation

`[lambda:1]=[1:1],  h=(0,0,t,0)`.

The combined mixed matrix has rank five.  With extension coordinates ordered
as four alpha coordinates followed by four beta coordinates, its complete
kernel is parameterized by

```
z=(0, -(C+qE)/(q-phi), (phi C+E)/(q-phi), 0; C,D,0,E).
```

Set

```
X=phi C+E,
Y=C+qE,
R=(q-phi)D-tX.
```

The four binary diagonals are

```
A01=0,       B01=4R,
A23=-4X/(q-phi),  B23=4Y.
```

Hence this branch is genuine only if `X*Y*R != 0`.  Its projected one-marked
minors force `D=0`, then `t!=0`, and leave precisely the necessary equations

```
E*(phi^2-1)*(2phi C+(phi q+1)E)=0,
C*(q^2-1)*((phi q+1)C+2qE)=0.
```

The frozen construction proposed that full two-contraction stacks obstruct
every solution on the uniform open

`q*phi*(q-phi)*(q^2-1)*(phi^2-1) != 0`.

That conclusion is **withdrawn** because the stated stack certificate fails
exact replay.  No weighted-`H22` conclusion is retained from this artifact.

## Unverified proposed rank-safe residue

Use projective extension coordinate `[C:E]`, with `D=0`, `t!=0`, and
`X*Y!=0`.  The necessary projected and stacked rank tests leave exactly:

1. `phi=epsilon`, `C=0`, for `epsilon=+1,-1` and `q!=0,epsilon`.
2. `q=epsilon`, `E=0`, for `epsilon=+1,-1` and `phi!=0,epsilon`.
3. `(phi,q)=(1,-2)` with `C+4E=0`, and `(-1,2)` with `C-4E=0`.
4. `(q,phi)=(1,-1/2)` with `E=2C`, and `(-1,1/2)` with `E=-2C`.
5. At `(q,phi)=(-1,1)` and `(1,-1)`, the full projective line `[C:E]`,
   excluding the two nongenuine points `X=0` or `Y=0`.

These were proposed as rank-safe necessary-condition survivors, not
constructed `H22` lifts.  Because the stack certificate fails, the assertion
that this list is complete is also withdrawn.  The loci remain **UNKNOWN**.

The zero sub-divisor `(p=0,q=phi)`, its projectivized normal directions, and
valuative limits are deliberately deferred.  No finite-field computation or
broad brute force is used, and no global Krenn–Gu conclusion follows.
