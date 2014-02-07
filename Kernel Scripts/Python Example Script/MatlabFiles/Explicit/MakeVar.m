%Made by J.T.B. Overvelde on 9 may 2011

function MakeVar(s,routine,c,e22ct,stepSize)

GlobPar

cd(AbDir)
%make variable file
delete('All-Var.py');
fid = fopen('All-Var.py', 'w');
fprintf(fid,'routine = %d\n',routine);
for i=1:length(c)
    fprintf(fid,['c',num2str(i),' = %1.5f\n'],c(i));
end
fprintf(fid,'numModes = %d\n',numModes);
fprintf(fid,'stepSize = %0.12f\n',stepSize);
fprintf(fid,'ec = %0.12f\n',e22ct);
fprintf(fid,'maxIncr = %d\n',maxIncr);
fprintf(fid,'maxNumIncr = %d\n',maxNumIncr);
fprintf(fid,'GridSpaceX = %0.12f\n',GridSpaceX);
fprintf(fid,'GridSpaceY = %0.12f\n',GridSpaceY);
fprintf(fid,'numHolesX = %d\n',numHolesX);
fprintf(fid,'numHolesY = %d\n',numHolesY);
fprintf(fid,'imperf = %0.12f\n',imperf);
fprintf(fid,'sizeMesh = %0.12f\n',sizeMesh);
fprintf(fid,'saveData = %d\n',saveData);
fprintf(fid,'saveFig = %d\n',saveFig);
fprintf(fid,'saveMov = %d\n',saveMov);
fprintf(fid,'mu = %1.8f\n',muVar);
fprintf(fid,'K = %1.8f\n',K);
fprintf(fid,'rho = %1.8f\n',rho);
fprintf(fid,'nS = %d\n',length(s));
for i=1:length(s)
    fprintf(fid,['valSpline',num2str(i),' = [(%0.12f,%0.12f)'],s(i).x(1)+GridSpaceX/2,s(i).y(1)+GridSpaceY/2);
    for j=2:length(s(i).x)
        fprintf(fid,',(%0.12f,%0.12f)',s(i).x(j)+GridSpaceX/2,s(i).y(j)+GridSpaceY/2);
    end
    fprintf(fid,']\n');
end
fclose(fid);
cd(MatDir)



