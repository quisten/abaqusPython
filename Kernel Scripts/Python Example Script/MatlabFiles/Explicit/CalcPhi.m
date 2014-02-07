%Made by J.T.B. Overvelde on 9 may 2011

function phiMin=CalcPhi(c,t)

GlobPar

[C x0 y0]=ConVal(c,t);
A=abs(trapz(C(1,2:end),C(2,2:end)));
phiMin=A/(GridSpaceX*GridSpaceY)-phi;