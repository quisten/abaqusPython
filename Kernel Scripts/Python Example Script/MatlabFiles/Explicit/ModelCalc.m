%Made by J.T.B. Overvelde on 9 may 2011

function Values=ModelCalc(c,routine)

GlobPar

[e22ct,stepSize]=GlobVar(c,routine);

s=FuncPer(c);
MakeVar(s,routine,c,e22ct,stepSize);

%run mode analysis (run Abaqus)
disp(['c = (',num2str(c(1)),',',num2str(c(2)),')'])
cd(AbDir)
unix(['abaqus cae ',mo,'=All-Main.py']);

%make Matlab Output Files
if exist('Output-PoisAll.txt')
    fid1 = fopen('Output-PoisAll.txt','r');
    A=fscanf(fid1,'%f ',[6 inf]);
    fclose(fid1);

    Poisson=A(1,end);
    e22=A(2,end);
    kInit=A(5,1)/A(6,1);

    cd(MatSaveDir);
    fid=fopen([saveFile,'All'],'a+'); 
    sss=[];
    for i=1:length(c)+6
        sss=[sss,'%f '];
    end
    for i=1:length(A(1,:))
        fprintf(fid,sss,[c,A(:,i)']);
        fprintf(fid,'\n');
    end
    fclose(fid);
    Values=Poisson;
else
    cd(MatSaveDir);
    fid=fopen([saveFile,'Err'],'a+');
    sss=[];
    for i=1:length(c)
        sss=[sss,'%f '];
    end
    fprintf(fid,sss,[c]);
    fprintf('\n')
    fclose(fid);
    Values=-2;
end

cd(MatDir);