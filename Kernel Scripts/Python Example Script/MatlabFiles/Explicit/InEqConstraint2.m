%Made by J.T.B. Overvelde on 9 may 2011

function [ConstVal,Nothing]=InEqConstraint2(c)

GlobPar

Nothing=[];

cd('./ConstFiles');

load(['ConstWall_',num2str(wMin*100),'_',num2str(phi*100)],'c1m','c2m','InEq')
ConstVal(1)=interp2(c1m,c2m,InEq,c(1),c(2));

load(['ConstPeriodic_',num2str(phi*100)],'c1m','c2m','ConstPer');
ConstVal(2)=interp2(c1m,c2m,ConstPer,c(1),c(2));

ConstVal
cd('../');