"""Primary 945-match derivation for the GLD59 O6 closure."""
from __future__ import annotations
from functools import lru_cache
from itertools import combinations
import sympy as sp
from sympy.polys.matrices import DomainMatrix
ROOTS=tuple(range(4));Q0,Q1=4,5;PORTS=tuple(range(6,10));VERTICES=ROOTS+(Q0,Q1)+PORTS;EDGES=tuple(combinations(ROOTS,2));EDGE_INDEX={e:i for i,e in enumerate(EDGES)};U,V,W=sp.symbols("u v w")
def rows(s):return tuple(tuple(item.split(":")) for item in s.split(","))
CASES={
"u_minus":(rows("1000:0010,0001:0001,0010:0010,0020:0020,0100:0100,0001:0100,0002:0002,0011:0000,0011:0110,0000:0110,0011:0011,0000:0011,0200:0200,0102:0102,0101:0000"),2*V*W**2*(V-1)*(V+1)*(V*W+V+W)),
"v_minus":(rows("1000:0010,0010:0010,0001:0100,0001:0001,0002:0002,0011:0110,0000:0110,0011:0011,0001:0111,0100:0100,0011:0000,0101:0101,0101:0000,0000:0101,0020:0020,0200:0200"),2*U**2*W**2*(U+1)*(W-1)),
"sum":(rows("1000:0010,0001:0001,0002:0002,0011:0011,0010:0010,0000:0011,0020:0020,0100:0100,0001:0100,0101:0101,0101:0000,0000:0101,0200:0200,0011:0000,0110:0000"),U**2*W*(U+1)*(U+2)*(W-1)),
"mixed":(rows("1000:0010,0001:0100,0001:0001,0002:0002,0011:0110,0001:0111,0000:0011,0011:0011,0010:0010,0020:0020,0100:0100,0011:0000,0101:0101,0101:0000,0000:0101,0200:0200"),2*V*W**3*(V-1)*(V+1)**2*(W-1)*(W+1)*(V*W+V+W)),
"both_minus":(rows("1000:0010,0010:0010,0001:0001,0100:0100,0001:0100,0002:0002,0011:0000,0011:0110,0000:0110,0011:0011,0001:0111,0020:0020,0200:0200,0102:0102,0101:0000"),2*W**2),
"u_mixed":(rows("1000:0010,0001:0001,0010:0010,0020:0020,0100:0100,0002:0002,0011:0000,0011:0110,0001:0111,0000:0011,0011:0011,0001:0100,0200:0200,0102:0102,0101:0000"),2*W**3*(2*W+1)),}
def word(v):return tuple(map(int,v))
def p_index(q,r,c):return 12*q+3*r+c
def w_index(a,b,ca,cb):
 if a>b:a,b,ca,cb=b,a,cb,ca
 return 24+9*EDGE_INDEX[(a,b)]+3*ca+cb
@lru_cache(maxsize=None)
def matchings(vertices):
 if not vertices:return ((),)
 first,answer=vertices[0],[]
 for i in range(1,len(vertices)):
  second=vertices[i];rest=vertices[1:i]+vertices[i+1:]
  for tail in matchings(rest):answer.append(((first,second),)+tail)
 return tuple(answer)
MATCHINGS=matchings(VERTICES);assert len(MATCHINGS)==945
def amplitudes(case):
 if case in ("u_minus","both_minus","u_mixed"):first=(-1,sp.Rational(1,2))
 elif case=="mixed":
  a=(V+1)*(W+1);first=(-a,a/(a+1))
 else:first=(U,U/(U-1))
 if case in ("v_minus","both_minus"):second=(-1,sp.Rational(1,2))
 elif case=="sum":second=(-U-1,(U+1)/(U+2))
 elif case=="u_mixed":second=(-W/(W+1),W/(2*W+1))
 else:second=(V,V/(V-1))
 third=(W,W/(W-1));return {(0,0,1):first[0],(1,1,0):first[1],(0,0,2):second[0],(1,2,0):second[1],(0,3,1):third[0],(1,1,3):third[1]}
def cross(r,p,rw,pw,case):
 c=pw[p]
 if rw[r]!=c:return 0
 if r==p:return sp.Integer(1)
 return amplitudes(case).get((c,r,p),sp.Integer(0))
def equation(pw,rw,case):
 x,y=(1,1,0),(1,-1,0);row={};constant=0
 for matching in MATCHINGS:
  variable=None;coefficient=sp.Integer(1)
  for ra,rb in matching:
   a,b=sorted((ra,rb));ev=None
   if a in ROOTS and b in ROOTS:ev=w_index(a,b,rw[a],rw[b])
   elif a in ROOTS and b in (Q0,Q1):ev=p_index(b-Q0,a,rw[a])
   elif a in ROOTS and b in PORTS:coefficient*=cross(a,b-6,rw,pw,case)
   elif a==Q0 and b==Q1:pass
   elif a in (Q0,Q1) and b in PORTS:coefficient*=(x if a==Q0 else y)[pw[b-6]]
   elif a in PORTS and b in PORTS:coefficient=0
   if coefficient==0:break
   if ev is not None:
    if variable is not None:coefficient=0;break
    variable=ev
  if coefficient==0:continue
  if variable is None:constant+=coefficient
  else:row[variable]=sp.expand(row.get(variable,0)+coefficient)
 if len(set(pw))==1 and rw==pw:row[78+pw[0]]=-1
 return row,sp.expand(-constant)
def main():
 for case,(keys,expected) in CASES.items():
  matrix=[];rhs=[]
  for pw,rw in keys:
   row,value=equation(word(pw),word(rw),case);matrix.append([sp.factor(row.get(i,0)) for i in range(81)]);rhs.append(sp.factor(value))
  ns=DomainMatrix.from_Matrix(sp.Matrix(matrix).T).nullspace().to_Matrix();assert ns.rows==1,case
  vector=[sp.factor(ns[0,i]) for i in range(ns.cols)];detector=sp.factor(sum(a*b for a,b in zip(vector,rhs,strict=True)));assert detector!=0
  weights=[sp.factor(a/detector) for a in vector];den=sp.factor(sp.lcm([sp.denom(sp.cancel(a)) for a in weights]));assert den==sp.factor(expected),(case,den)
 print("PASS: 945-match expansion derives all six GLD59 O6 contradictions")
if __name__=="__main__":main()
