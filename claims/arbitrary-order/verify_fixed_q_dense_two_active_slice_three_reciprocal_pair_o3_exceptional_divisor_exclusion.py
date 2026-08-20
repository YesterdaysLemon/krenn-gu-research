"""Primary 945-match derivation for the GLD60 O3 closure."""
from __future__ import annotations
import sympy as sp
from sympy.polys.matrices import DomainMatrix
import verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_o6_exceptional_divisor_exclusion as base
U,V,W=base.U,base.V,base.W
def rows(s):return tuple(tuple(item.split(":")) for item in s.split(","))
CASES={
"equal":(rows("1010:0000,1000:0100,0100:0010,0010:0010,0020:0020,0100:0100,0011:0011,0001:0001,0011:0000,0000:0011,0002:0002,0110:0000,0101:0000,1001:0000"),U*W*(U-1)*(U+1)**2*(W-1)*(W+1)**2),
"sum":(rows("1001:0000,1000:0010,0100:0010,0010:0010,0020:0020,0002:0002,0120:0120,0200:0200,0100:0100,0101:0000,0011:0000,0011:0011,0001:0001,0000:0011"),W*(U+1)*(2*U+1)*(U*W-U+W)*(U*W-U-W-2)),
"minus":(rows("1001:0000,1000:0100,0010:0010,0020:0020,0100:0100,0011:0011,0001:0001,0011:0000,0000:0011,0002:0002,0110:0110,0110:0000,0000:0110,0120:0120,0101:0000"),2*U*W*(U-1)*(W+1)**2*(U*W-U-W-2)),
"plus":(rows("1001:0000,1000:0010,0010:0010,0100:0010,0020:0020,0120:0120,0110:0110,0000:0110,0012:0012,0101:0000,0011:0000"),2*W*(U+1)*(W+1)**2*(U*W-U+W)*(U*W+W+1)),
"eq_u_minus":(rows("1010:0110,0100:0100,0100:0010,0010:0010,0020:0020,0012:0012,0002:0002,1001:0000,0101:0000,0011:0000,0110:0000,0000:0110"),2*W*(W-1)*(W+1)),
"eq_w_minus":(rows("1010:0000,1000:0100,0100:0010,0010:0010,0020:0020,0100:0100,0011:0000,0110:0110,0000:0110,0012:0012,0101:0000,1001:0000,0002:0002"),6*U*(U-1)*(U+1)*(2*U+1)),
"eq_sum":(rows("1010:0000,1000:0100,0100:0010,0010:0010,0020:0020,0100:0100,0011:0011,0001:0001,0011:0000,0000:0011,0002:0002,0101:0000,1001:0000,0110:0000"),3*W*(W-1)*(W+1)**2),
"sum_minus":(rows("1001:0000,1000:0100,0010:0010,0020:0020,0100:0100,0011:0011,0001:0001,0011:0000,0000:0011,0002:0002,0120:0120,0200:0200,0101:0000"),2*U*(U-1)*(U+2)*(2*U+1)**2),
"sum_plus":(rows("1001:0000,1000:0010,0010:0010,0100:0010,0020:0020,0120:0120,0012:0012,0200:0200,0100:0100,0101:0000,0011:0000"),2*U*(U+1)*(2*U+1)**2),
"point_minus":(rows("1010:0110,0100:0010,0010:0010,0020:0020,0110:0110,1001:0000,0101:0000,0011:0000,0012:0012"),sp.Integer(4)),
"point_half":(rows("1010:0000,1000:0100,0100:0010,0010:0010,0012:0012,0002:0002,0100:0100,0011:0000,0120:0120,0101:0000,1001:0000,0110:0000"),sp.Integer(6)),}
def amplitudes(case):
 if case=="equal":u,v,w=U,U,W
 elif case=="sum":u,v,w=U,-U-1,W
 elif case=="minus":u,w=U,W;v=1+W-U*W
 elif case=="plus":u,w=U,W;v=-1-W-U*W
 elif case=="eq_u_minus":u,v,w=sp.Integer(-1),sp.Integer(-1),W
 elif case=="eq_w_minus":u,v,w=U,U,sp.Integer(-1)
 elif case=="eq_sum":u,v,w=sp.Rational(-1,2),sp.Rational(-1,2),W
 elif case=="sum_minus":u=U;v=-U-1;w=(U+2)/(U-1)
 elif case=="sum_plus":u=U;v=-U-1;w=U/(U+1)
 elif case=="point_minus":u=v=w=sp.Integer(-1)
 else:u=v=sp.Rational(-1,2);w=sp.Integer(-1)
 return {(0,0,1):u,(1,1,0):sp.cancel(u/(u-1)),(0,0,2):v,(1,2,0):sp.cancel(v/(v-1)),(0,1,2):w,(1,2,1):sp.cancel(w/(w-1))}
def main():
 base.amplitudes=amplitudes
 for case,(keys,expected) in CASES.items():
  matrix=[];rhs=[]
  for pw,rw in keys:
   row,value=base.equation(base.word(pw),base.word(rw),case);matrix.append([sp.factor(row.get(i,0)) for i in range(81)]);rhs.append(sp.factor(value))
  ns=DomainMatrix.from_Matrix(sp.Matrix(matrix).T).nullspace().to_Matrix();assert ns.rows==1,case
  vector=[sp.factor(ns[0,i]) for i in range(ns.cols)];detector=sp.factor(sum(a*b for a,b in zip(vector,rhs,strict=True)));assert detector!=0
  weights=[sp.factor(a/detector) for a in vector];den=sp.factor(sp.lcm([sp.denom(sp.cancel(a)) for a in weights]));assert den==sp.factor(expected),(case,den)
 print("PASS: 945-match expansion derives all eleven GLD60 O3 contradictions")
if __name__=="__main__":main()
