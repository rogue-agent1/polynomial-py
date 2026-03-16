class Poly:
    def __init__(s,coeffs): s.c=list(coeffs)
    def __repr__(s):
        terms=[]
        for i,c in enumerate(s.c):
            if abs(c)<1e-12: continue
            if i==0: terms.append(f"{c:.3g}")
            elif i==1: terms.append(f"{c:.3g}x")
            else: terms.append(f"{c:.3g}x^{i}")
        return " + ".join(terms) or"0"
    def __call__(s,x):
        r=0;xp=1
        for c in s.c: r+=c*xp;xp*=x
        return r
    def __add__(s,o):
        n=max(len(s.c),len(o.c));r=[0]*n
        for i in range(len(s.c)): r[i]+=s.c[i]
        for i in range(len(o.c)): r[i]+=o.c[i]
        return Poly(r)
    def __mul__(s,o):
        r=[0]*(len(s.c)+len(o.c)-1)
        for i,a in enumerate(s.c):
            for j,b in enumerate(o.c): r[i+j]+=a*b
        return Poly(r)
    def derivative(s): return Poly([i*s.c[i] for i in range(1,len(s.c))]) if len(s.c)>1 else Poly([0])
    def integral(s,C=0): return Poly([C]+[s.c[i]/(i+1) for i in range(len(s.c))])
    def roots_newton(s,x0=1.0,tol=1e-10,maxiter=100):
        dp=s.derivative();x=x0
        for _ in range(maxiter):
            fx=s(x);dfx=dp(x)
            if abs(dfx)<1e-15: break
            x-=fx/dfx
            if abs(fx)<tol: break
        return x
def demo():
    p=Poly([-6,1,1]);print(f"p(x) = {p}");print(f"p(2) = {p(2)}")
    print(f"p'(x) = {p.derivative()}");r=p.roots_newton(5);print(f"Root near 5: {r:.6f}")
    q=Poly([1,0,1]);print(f"p*q = {p*q}")
if __name__=="__main__": demo()
