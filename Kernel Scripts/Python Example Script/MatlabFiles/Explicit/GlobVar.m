%Made by J.T.B. Overvelde on 9 may 2011

function [e22ct,stepSize]=GlobVar(c,routine)

GlobPar

%constants
np=60;
phi=0.5;
wMin=0.15;
maxIncr=1;
maxNumIncr=500;

GridSpaceX=1;
GridSpaceY=1;
sizeMesh=0.05*min([GridSpaceX,GridSpaceY]);      %1,2,3
mo='noGUI';

%default values (if not used in routine)
numModes=1;
numHolesX=1;
numHolesY=1;
stepSize=1;
stepSize=1;
imperf=1;
saveData=1;
saveFig=1;
saveMov=1;

%material constants
E=1.0;
v=0.499;
muVar=E/(2.0*(1.0+v));
K=E/(3.0*(1.0-2.0*v));
%muVar=1.08e6;
%K=2.0e9;
rho=1.05e3;

if or(routine==3,routine==4)
    cd('./ConstFiles');
    load(['ConstPeriodic_',num2str(phi*100)],'c1m','c2m','e22c')
    cd('../');
    e22ct=interp2(c1m,c2m,e22c',c(1),c(2));
else
    e22ct=0;
end
if routine==4
    cd('./ConstFiles');
    load(['eContact_',num2str(wMin*100),'_',num2str(phi*100)],'c1m','c2m','eContact')
    cd('../');
    eContactt=interp2(c1m,c2m,eContact,c(1),c(2));  
else
    eContactt=0;
end

if routine==1 %Per
    numModes=1;
    numHolesX=1;
    numHolesY=1;
    stepSize=0.01;
    saveData=0;
elseif routine==2 %Ell
    numHolesX=1;
    numHolesY=1;
    stepSize=0.01;
    saveData=0;
elseif routine==3 %Pois
    numHolesX=2;
    numHolesY=2;
    stepSize=-e22ct+0.3;
    imperf=0.1;
    saveData=1;
    saveFig=0;
    saveMov=0;
elseif routine==4 %Band
    numModes=140; %if different then 60, change MainBruteBand
    numHolesX=2;
    numHolesY=2;
    stepSize=0;
    saveData=0;
    imperf=0.00;
elseif routine==5 %KInit
    numHolesX=1;
    numHolesY=1;
    saveData=0;
end

