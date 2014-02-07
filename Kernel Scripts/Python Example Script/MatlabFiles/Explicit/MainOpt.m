%Made by J.T.B. Overvelde on 9 may 2011

clear, close all, clc;

GlobPar

FileNameSave

%options
options = optimset('Display','iter','LargeScale','off','Tolfun',1e-3,'tolcon',1e-3,'TolX',1e-3,'MaxFunEvals',1000,'Algorithm','active-set','DiffMaxChange',0.5e-1,'DiffMinChange',1e-3);
%optimize
[OptVar, Poisson, drie, vier, vijf, zes] = fmincon(@(c)ModelCalc(c,3),[0,0],[],[],[],[],[],[],@(c)InEqConstraint2(c),options);

%save mat file
cd(MatSaveDir);
save(saveFile);
cd(MatDir);