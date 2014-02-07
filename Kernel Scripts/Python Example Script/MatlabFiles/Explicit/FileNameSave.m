%Made by J.T.B. Overvelde on 9 may 2011

%directories
MatDir=pwd;
cd('../');cd('../');
cd('./AbaqusFiles');
AbDir=pwd;
cd('../');
cd('./MatlabOutputFiles');
if exist(date)
else
    mkdir(date)
end
cd(['./',date])
MatSaveDir=pwd;
cd(MatDir);

%name save files
saveFile='Test';
saveFileOld=saveFile;
cd(MatSaveDir)
rep=0;
while exist([saveFile,'.mat'])~=0
    rep=rep+1;
    saveFile=[saveFileOld,num2str(rep)];
end
cd(MatDir)