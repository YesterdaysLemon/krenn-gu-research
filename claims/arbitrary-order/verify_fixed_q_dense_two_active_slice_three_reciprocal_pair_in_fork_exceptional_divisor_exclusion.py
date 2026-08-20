"""Primary 945-match derivation for the GLD57 in-fork closure."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations

import sympy as sp
from sympy.polys.matrices import DomainMatrix


ROOTS=tuple(range(4)); Q0,Q1=4,5; PORTS=tuple(range(6,10)); VERTICES=ROOTS+(Q0,Q1)+PORTS
EDGES=tuple(combinations(ROOTS,2)); EDGE_INDEX={edge:index for index,edge in enumerate(EDGES)}
U,V,W=sp.symbols("u v w")
def rows(value): return tuple(tuple(item.split(":")) for item in value.split(","))
CASES={
 "u_minus":(rows("1000:0100,0001:0001,0001:0100,0010:0010,0001:0010,0100:0010,0002:0002,0011:0011,0000:0011,0100:0100,0011:0110,0000:0110,0101:0011,0101:0000,0101:0101,0100:0111"),2*V**3*W**2*(W-1)*(W+2)),
 "difference":(rows("1001:0101,0001:0100,0001:0001,0002:0002,0011:0011,0010:0010,0000:0011,0011:0110,0000:0110,0001:0010,0100:0010,0100:0100,0011:0000,0101:0011,0101:0000,0000:0101,0101:0101"),2*U**2*V**3*(U-2)*(U-1)**3*(U+1)*(U*V+V+1)),
 "sum":(rows("1000:0100,0001:0100,0010:0010,0000:0011,0011:0110,0001:0111,0001:0010,0100:0010,0002:0002,0011:0011,0001:0001,0100:0100,0011:0000,0101:0011,0101:0000,0101:0101,0000:0101"),4*U**2*V**3*(U+1)**2*(U+2)*(U*V+V+1)),
 "product":(rows("1000:0100,0001:0100,0001:0001,0002:0002,0011:0011,0001:0111,0000:0110,0011:0110,0010:0010,0001:0010,0100:0010,0100:0100,0011:0000,0101:0011,0101:0000,0101:0101,0000:0101"),2*U*W**2*(U+1)*(W-1)*(U-W-1)*(U+W+1)),
 "minus_difference":(rows("1001:0101,0001:0001,0001:0100,0010:0010,0001:0010,0002:0002,0100:0100,0100:0010,0011:0011,0000:0011,0011:0110,0000:0110,0101:0011,0101:0000,0100:0111,0101:0101"),8*V**3),
 "difference_product":(rows("1001:0101,0001:0100,0001:0001,0002:0002,0011:0011,0001:0111,0000:0110,0011:0110,0010:0010,0001:0010,0100:0010,0100:0100,0011:0000,0101:0011,0101:0000,0000:0101,0101:0101"),4*U**2*(U-2)*(U-1)**3*(U+1)),
 "sum_product":(rows("1000:0100,0001:0100,0002:0112,0011:0110,0010:0010,0001:0010,0100:0010,0002:0002,0011:0011,0001:0001,0001:0111,0100:0100,0011:0000,0101:0011,0101:0000,0101:0101,0000:0101"),4*U**2*(U+1)**2*(U+2)),
}
def word(v): return tuple(map(int,v))
def p_index(q,r,c): return 12*q+3*r+c
def w_index(a,b,ca,cb):
 if a>b:a,b,ca,cb=b,a,cb,ca
 return 24+9*EDGE_INDEX[(a,b)]+3*ca+cb
@lru_cache(maxsize=None)
def matchings(vertices):
 if not vertices:return ((),)
 first,answer=vertices[0],[]
 for i in range(1,len(vertices)):
  second=vertices[i]; rest=vertices[1:i]+vertices[i+1:]
  for tail in matchings(rest):answer.append(((first,second),)+tail)
 return tuple(answer)
MATCHINGS=matchings(VERTICES); assert len(MATCHINGS)==945
def amplitudes(case):
 if case in ("u_minus","minus_difference"): first=(-1,sp.Rational(1,2))
 else:first=(U,U/(U-1))
 if case in ("product","difference_product","sum_product"): second=(-1/(U+1),1/(U+2))
 else:second=(V,V/(V-1))
 if case=="difference" or case=="difference_product": third=(U-1,(U-1)/(U-2))
 elif case=="sum" or case=="sum_product": third=(-U-1,(U+1)/(U+2))
 elif case=="minus_difference": third=(-2,sp.Rational(2,3))
 else:third=(W,W/(W-1))
 return {(0,0,1):first[0],(1,1,0):first[1],(0,1,2):second[0],(1,2,1):second[1],(0,3,1):third[0],(1,1,3):third[1]}
def cross(root,port,rw,pw,case):
 c=pw[port]
 if rw[root]!=c:return 0
 if root==port:return sp.Integer(1)
 return amplitudes(case).get((c,root,port),sp.Integer(0))
def equation(pw,rw,case):
 x,y=(1,1,0),(1,-1,0); row={}; constant=0
 for matching in MATCHINGS:
  variable=None; coefficient=sp.Integer(1)
  for ra,rb in matching:
   a,b=sorted((ra,rb)); edge_variable=None
   if a in ROOTS and b in ROOTS:edge_variable=w_index(a,b,rw[a],rw[b])
   elif a in ROOTS and b in (Q0,Q1):edge_variable=p_index(b-Q0,a,rw[a])
   elif a in ROOTS and b in PORTS:coefficient*=cross(a,b-PORTS[0],rw,pw,case)
   elif a==Q0 and b==Q1:pass
   elif a in (Q0,Q1) and b in PORTS:coefficient*=(x if a==Q0 else y)[pw[b-PORTS[0]]]
   elif a in PORTS and b in PORTS:coefficient=0
   else:raise AssertionError((a,b))
   if coefficient==0:break
   if edge_variable is not None:
    if variable is not None:coefficient=0; break
    variable=edge_variable
  if coefficient==0:continue
  if variable is None:constant+=coefficient
  else:row[variable]=sp.expand(row.get(variable,0)+coefficient)
 if len(set(pw))==1 and rw==pw:row[78+pw[0]]=-1
 return row,sp.expand(-constant)
def main():
 for case,(keys,expected) in CASES.items():
  matrix=[]; rhs=[]
  for pw,rw in keys:
   row,value=equation(word(pw),word(rw),case); matrix.append([sp.factor(row.get(i,0)) for i in range(81)]); rhs.append(sp.factor(value))
  ns=DomainMatrix.from_Matrix(sp.Matrix(matrix).T).nullspace().to_Matrix(); assert ns.rows==1,case
  vector=[sp.factor(ns[0,i]) for i in range(ns.cols)]; detector=sp.factor(sum(a*b for a,b in zip(vector,rhs,strict=True))); assert detector!=0,case
  weights=[sp.factor(a/detector) for a in vector]; assert sp.factor(sum(a*b for a,b in zip(weights,rhs,strict=True)))==1
  denominator=sp.factor(sp.lcm([sp.denom(sp.cancel(a)) for a in weights])); assert denominator==sp.factor(expected),(case,denominator)
 print("PASS: 945-match expansion derives all seven GLD57 in-fork contradictions")
if __name__=="__main__":main()
