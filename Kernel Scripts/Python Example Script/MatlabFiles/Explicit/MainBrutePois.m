%Made by J.T.B. Overvelde on 9 may 2011

clear, close all, clc;

GlobPar

FileNameSave

%c1a=-0.2:0.005:0.4;
%c2a=-0.25:0.005:0.4;
c1a=0.08;
c2a=-0.1;
n=length(c1a)*length(c2a); rep=0; timeCalc=0;
PoissonFinal=-2*ones(length(c1a),length(c2a));

rep=0;i=0;
for c1=c1a
    i=i+1;
    j=0;
    for c2=c2a
        rep=rep+1;
        tic
        j=j+1;
        c=[c1 c2];
        GlobVar(c,3);
        
        answ=InEqConstraint2(c);
        if max(answ)<0
            PoissonFinal(i,j)=ModelCalc(c,3);
        end
        
        %save mat file
        cd(MatSaveDir);
        save(saveFile);
        cd(MatDir)
        timeNow=toc;
        timeCalc=timeCalc+timeNow;
        disp(['Time remaining (on all previous)= ',num2str((n*timeCalc/rep-timeCalc)/60),' min'])
        disp(['Time remaining (on last)=',num2str((n-rep)*timeNow/60),' min'])
    end
end

%save mat file
cd(MatSaveDir);
save(saveFile);
cd(MatDir);