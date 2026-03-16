#!/usr/bin/env python3
"""Polynomial arithmetic, evaluation, roots, interpolation."""
import sys,math

class Poly:
    def __init__(self,coeffs):self.c=list(coeffs)  # c[0] + c[1]*x + c[2]*x^2 ...
    def __repr__(self):
        terms=[]
        for i,c in enumerate(self.c):
            if abs(c)<1e-15:continue
            if i==0:terms.append(f"{c}")
            elif i==1:terms.append(f"{c}x")
            else:terms.append(f"{c}x^{i}")
        return' + '.join(terms) or '0'
    def __call__(self,x):return sum(c*x**i for i,c in enumerate(self.c))
    def __add__(self,o):
        n=max(len(self.c),len(o.c))
        return Poly([(self.c[i] if i<len(self.c) else 0)+(o.c[i] if i<len(o.c) else 0)for i in range(n)])
    def __mul__(self,o):
        r=[0]*(len(self.c)+len(o.c)-1)
        for i,a in enumerate(self.c):
            for j,b in enumerate(o.c):r[i+j]+=a*b
        return Poly(r)
    def deriv(self):return Poly([i*c for i,c in enumerate(self.c)][1:]) if len(self.c)>1 else Poly([0])
    def integral(self,C=0):return Poly([C]+[c/(i+1)for i,c in enumerate(self.c)])
    @staticmethod
    def interpolate(points):
        n=len(points);result=Poly([0])
        for i in range(n):
            xi,yi=points[i];basis=Poly([1])
            for j in range(n):
                if i!=j:
                    xj=points[j][0]
                    basis=basis*Poly([-xj/(xi-xj),1/(xi-xj)])
            result=result+Poly([yi])*basis
        return result

def main():
    if len(sys.argv)>1 and sys.argv[1]=="--test":
        p=Poly([1,2,3])  # 1+2x+3x²
        assert abs(p(0)-1)<1e-10 and abs(p(1)-6)<1e-10 and abs(p(2)-17)<1e-10
        q=Poly([1,1])  # 1+x
        r=p*q  # (1+2x+3x²)(1+x)=1+3x+5x²+3x³
        assert abs(r(1)-12)<1e-10
        d=p.deriv()  # 2+6x
        assert abs(d(0)-2)<1e-10 and abs(d(1)-8)<1e-10
        # Interpolation
        pts=[(0,1),(1,3),(2,7)]
        interp=Poly.interpolate(pts)
        for x,y in pts:assert abs(interp(x)-y)<1e-8
        print("All tests passed!")
    else:
        p=Poly([1,0,-1])  # 1-x²
        print(f"p(x) = {p}")
        print(f"p(2) = {p(2)}")
if __name__=="__main__":main()
