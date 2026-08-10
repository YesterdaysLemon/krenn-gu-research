# A ten-equation affine core in the exact-three `C10` boundary

## Status

This is an exact, hand-reducible contradiction for one of the 11,751
support-semantic survivors in the exact-three-partial `C10` catalogue.
It is catalogue orbit 384 with local-signature witness

```text
(4784, 2458, 3717, 326, 5012).
```

The full exact-support system has 193 distinct forbidden mixed
coefficients.  An exact Singular lift used only 16 of them and did not
use the Laurent saturation equation.  Deletion minimization reduced the
lift support to ten equations.  The argument below verifies those ten
directly and shows that their affine ideal is already the unit ideal.

This excludes one support orbit and supplies a candidate reusable
algebraic template.  It does **not** close the other 11,750 `C10` cases
or the global Krenn--Gu conjecture.

## Support

Masks `1,2,4` mean singleton target colours; `3,5,6` mean the three
two-colour supports; and `7` means full support.  The five mode rows are

```text
6 6 1 4 1
2 7 5 1 4
4 4 7 7 2
1 2 2 7 7
7 1 4 2 7.
```

The three partial cells are the masks `6,5,6`; their missing colours
are respectively `0,1,0`.

## Ten forbidden coefficients

After the standard spanning-tree gauge, write

```text
a=u7, b=u16, h=u18, q=u0-1, r=u1, s=u3, t=u22,
L=u13+a*u15+a*u11,
B=u21+b*u19,
C=u9*b+u6+u4*u5+u2*u5,
M=u10+u8*b.
```

Ten regenerated mixed-colour coefficient equations have the following
forms.  The left column gives one inherited colour word for each
coefficient class.

```text
00020:  1 + a*b
00120:  1 + M
01012:  a*(t+h) + r*L
02221:  B + C
02222:  t + h + C
10121:  B + M + s*b
10122:  t + (1+h)*M + s*b
11000:  1 + r
20012:  t*(u13+a+a*u11+s) + u15*(1+a*h+u0*(a+s))
20122:  t + b + h*M + u0*(M+s*b).
```

Some of the short polynomials occur for several inherited words; the
verifier checks their exact positions in the full 193-equation
generator rather than assuming that the displayed representative word
is unique.

## Elementary contradiction

All ten displayed expressions are assumed zero.

First form

```text
(F10121-F00120)
  -(F02221-F02222)
  -(F10122-(1+h)F00120)
  = 2h.
```

Over characteristic zero this gives `h=0`.  The equations `F11000` and
`F01012` then give

```text
r=-1,  L=a*t.                                           (1)
```

Put

```text
R = F10122-(1+h)F00120.
```

At `h=0`, `R=0` is

```text
t+s*b=1.                                                (2)
```

The exact identity

```text
F20122 at h=0
  = b-q*t + u0*(F00120+R)
```

therefore gives

```text
b=q*t.                                                  (3)
```

The first equation says `a*b=-1`, so `a,b` are nonzero.
Equation (3) then makes both `q` and `t` nonzero.  Combining (2), (3),
and `a*b=-1` gives

```text
q*t*(a+s)=-t,
q*(a+s)=-1,
a*t=a+s.                                                (4)
```

Using (1) and (4), the ninth equation reduces exactly to

```text
F20012 = 2*t*(a+s).
```

Both factors are nonzero by (4), a contradiction.  Notice that no
variable saturation or nonzero pure-amplitude assumption was used: the
ten forbidden mixed coefficients have no common affine zero.

## Replay and next test

Run:

```text
python \
  claims/p5/frontier/verify_p5_c10_ten_equation_affine_core.py
```

The verifier regenerates the complete 193-equation system from the
support and signature data, checks the ten exact polynomials, and
symbolically verifies every displayed reduction.  As an independent
check on the hand reduction, SymPy recomputes the ten-polynomial
Gröbner basis and obtains `[1]`.

The obvious coarse generalization is false.  Orbit 384 shares both its
canonical coordinate backbone and its missing-colour geometry with 14
other catalogue cases.  Fresh unsaturated Singular calculations split
that 15-member class into

```text
11 affine unit ideals
 4 affine non-unit ideals.
```

The four non-unit affine systems may still be excluded after enforcing
the nonzero pure amplitudes; this probe deliberately does not test the
saturated ideals.  Replay it with

```text
python \
  tools/explore/probe_p5_c10_joint_affine_class.py
```

Thus geometry alone does not transport the ten-equation proof.  The
next structural test must refine the quotient by the coefficient
monomial-incidence template, or explicitly distinguish affine cores
from contradictions that require Laurent saturation.  A small number
of refined templates would turn the current 11,751-case algebra sweep
into a finite family of explicit identities; many unrelated templates
would instead justify completing the support-by-support fallback.
