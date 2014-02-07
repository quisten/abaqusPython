#Made by J.T.B. Overvelde on 9 may 2011

from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
from Numeric import *
from abaqus import *
from abaqusConstants import *
import visualization
import os
import datetime
import shutil
from odbAccess import *
import time

#constants
fac=100
nDefS=20
hStop=1e-5
nB=10
nP0=2
devMesh=1

#get date and time
now=datetime.datetime.now()

#make save and work directories
wDr=os.getcwd()
sDr1='../AbaqusOutputFiles'
TYear=str(now.year)
TMonth=str(now.month)
TDay=str(now.day)
THour=str(now.hour)
TMin=str(now.minute)
TSec=str(now.second)
if len(TMonth)==1:
	TMonth=str(0)+TMonth
if len(TDay)==1:
	TDay=str(0)+TDay
if len(THour)==1:
	THour=str(0)+THour
if len(TMin)==1:
	TMin=str(0)+TMin
if len(TSec)==1:
	TSec=str(0)+TSec

tDr=sDr1+'/'+TYear+'-'+TMonth+'-'+TDay+'_'+THour+'-'+TMin+'-'+TSec
if os.path.isdir(sDr1)==False:
	os.mkdir(sDr1)
os.mkdir(tDr)
os.mkdir(tDr+'/Output')
os.mkdir(tDr+'/Figures')
if os.path.isdir(wDr+'/Figures')==False:
	os.mkdir(wDr+'/Figures')

listBack=['Output-PerStress.txt','Output-PerAll.txt','Output-PerMin.txt',
    'Output-EllStress.txt','Output-EllL.txt','Output-EllMin.txt',
    'Output-PoisAll.txt','Output-PoisMode.txt',
    'Output-BandAll.txt','Ouput-BandStress.txt',
    'Output-KInit.txt']
for i in listBack:
	if os.path.exists(i)==True:
		os.remove(i)

#save var as text file
shutil.copy('All-Var.py',tDr+'/Output/All-Var.txt')

#names of name variables
modelName1='MODEL1'
modelName2='MODEL2'
partName1='PART1'
partName2='PART2'
matName='NEO'
refName1='REF1'
refName2='REF2'
secName='SECTION'
instName1='INST1'
instName2='INST2'
instRefName1='INSTREF1'
instRefName2='INSTREF2'
jobName1='JOB1'
jobName2='JOB2'
stepName1='STEP1-'
stepName2='STEP2-'

#execute routines all
execfile('All-Var.py')
execfile('All-Model.py')

#execute routines Full
execfile('Pois-Assembly.py')
execfile('Pois-BcSteps1.py')
execfile('Pois-Analysis1.py')
execfile('Pois-BcSteps2.py')
execfile('Pois-Analysis2.py')

for i in listBack:
	if os.path.exists(i)==True:
		shutil.copy(i,tDr+'/Output/'+i)

#save data
if saveData==0:		
	if os.path.isdir(tDr):
		execfile('All-DelFile.py')
#delete record files
listBack=['abaqus.rpy','abaqus.rec','abaqus_acis.log','save_abaqus.rec']
for i in range(1,100):
	listBack=listBack+['abaqus.rpy.'+str(i),'abaqus'+str(i)+'.rec','save_abaqus'+str(i)+'.rec']
for i in listBack:
	if os.path.exists(i)==True:
		os.remove(i)





 





