%Made by J.T.B. Overvelde on 9 may 2011

function [s]=FuncPer(c)

GlobPar

%figure
tf1=fzero(@(t)CalcPhi(c,t),0.5);
%figure
[C,x0,y0]=ConVal(c,tf1);

i=1; num=0;
while i<length(C)
   n=C(2,i);
   x=C(1,i+1:i+n);
   y=C(2,i+1:i+n);
   x1=[]; y1=[]; htot=[1];
   if and(sum(x)/n<=x0*1.04,sum(x)/n>=-x0*1.04)
       if and(sum(y)/n<=y0*1.04,sum(y)/n>=-y0*1.04)
            num=num+1;
            x(1)=x(end);
            y(1)=y(end);
            s(num).x=x;
            s(num).y=y;
            %hold on
            %plot(x,y,'-o')
       end
   end
   i=i+n+1;
end
pause(0.5)