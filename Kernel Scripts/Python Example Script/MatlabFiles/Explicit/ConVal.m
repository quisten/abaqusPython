%Made by J.T.B. Overvelde on 9 may 2011

function [C,x0,y0]=ConVal(c,t)

GlobPar

theta=0:2*pi/(np-1):2*pi;
R=1+c(1)*cos(4*theta)+c(2)*cos(8*theta);%+c(3)*cos(12*theta);
C(1,:)=[0 t*R.*cos(theta)];
C(2,:)=[length(theta) t*R.*sin(theta)];

x0=GridSpaceX/2;
y0=GridSpaceY/2;

%plot(C(1,2:end),C(2,2:end))